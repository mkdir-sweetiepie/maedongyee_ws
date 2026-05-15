#!/usr/bin/env python3
"""
Driving Controller Node (matches the 매동이 evaluation rubric).

State machine:
  WAITING_FOR_SYSTEM -> NORMAL -> {STOP_WAIT, TURNING, SLOW, FINISHED}

Signs handled:
  - stop                -> STOP_WAIT (~3.5s) then NORMAL
  - traffic_light       -> STOP_WAIT (~3s) then TURNING right (red light rule)
  - traffic_light_green -> TURNING right (no stop)
  - left_turn / right_turn -> TURNING
  - horn                -> beep buzzer (no state change)
  - slow (20)           -> linear *= SLOW_SPEED_RATIO until crosswalk

Finish: red line detected after RED_DETECT_LOCKOUT_SEC from start.

Line tracing uses the ported turtlebot algorithm in line_tracer.LineTracer.
"""

import time

import numpy as np
import rclpy
from cv_bridge import CvBridge
from geometry_msgs.msg import Twist
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String

from aicar_msgs.msg import LaneInfo

from . import constants as C
from .line_tracer import LineTracer

try:
    import lgpio
    LGPIO_AVAILABLE = True
except ImportError:
    LGPIO_AVAILABLE = False


# --- States ---
STATE_WAITING_FOR_SYSTEM = 'WAITING_FOR_SYSTEM'
STATE_NORMAL = 'NORMAL'
STATE_STOP_WAIT = 'STOP_WAIT'
STATE_TURNING = 'TURNING'
STATE_POST_TURN_STRAIGHT = 'POST_TURN_STRAIGHT'
STATE_FINISHED = 'FINISHED'


class DrivingControllerNode(Node):
    def __init__(self):
        super().__init__('driving_controller_node')
        self.get_logger().info('Driving Controller (turtlebot-port) started.')

        self.bridge = CvBridge()

        # --- Parameters ---
        self.declare_parameter('vehicle_speed', 0.20)
        self.declare_parameter('skip_system_handshake', False)
        self.base_speed = self.get_parameter('vehicle_speed').value
        self.skip_handshake = self.get_parameter('skip_system_handshake').value

        # --- Subscriptions ---
        self.sub_lane = self.create_subscription(LaneInfo, '/lane_info', self.lane_cb, 10)
        self.sub_red_bev = self.create_subscription(Image, '/image_red_bev', self.red_cb, 10)
        self.sub_sign = self.create_subscription(String, '/sign_detection', self.sign_cb, 10)
        self.sub_status = self.create_subscription(String, '/system_status', self.status_cb, 10)
        self.sub_emergency = self.create_subscription(String, '/emergency_command', self.emergency_cb, 10)

        # --- Publishers ---
        self.pub_cmd = self.create_publisher(Twist, '/cmd_vel', 10)
        self.pub_state = self.create_publisher(String, '/drive_state', 10)        # for UI
        self.pub_telemetry = self.create_publisher(String, '/telemetry', 10)      # for UI

        # --- LineTracer ---
        self.tracer = LineTracer(base_speed=self.base_speed, logger=self.get_logger())

        # --- State machine ---
        if self.skip_handshake:
            self.drive_state = STATE_NORMAL
            self.start_time = time.time()
        else:
            self.drive_state = STATE_WAITING_FOR_SYSTEM
            self.start_time = None
        self.state_entered_time = time.time()

        # Sign tracking
        self.detected_signs = set()       # signs that have already triggered behavior
        self.current_sign = None
        self.next_state_after_stop = STATE_NORMAL
        self.turn_direction = 1.0         # +1 left, -1 right
        self.stop_wait_duration = C.STOP_SIGN_WAIT_SEC

        # Slow mode (runs in parallel to NORMAL)
        self.slow_mode_until = 0.0
        self.last_buzzer_time = 0.0
        self.slow_sign_name = 'slow'      # or '20', adjust if your detector outputs different

        # Buzzer (raspberry pi)
        self.gpio_h = None
        self.buzzer_on_until = 0.0
        if LGPIO_AVAILABLE:
            try:
                self.gpio_h = lgpio.gpiochip_open(4)
                lgpio.gpio_claim_output(self.gpio_h, C.BUZZER_PIN)
            except Exception as e:
                self.get_logger().warn(f'Buzzer GPIO init failed: {e}')
                self.gpio_h = None

        # --- Main control loop at 30 Hz ---
        self.last_lane_info = None
        self.timer = self.create_timer(1.0 / 30.0, self.control_loop)

        self.get_logger().info(f'Initial state: {self.drive_state}')

    # ==================================================================
    # Callbacks (passive — just store latest data)
    # ==================================================================
    def lane_cb(self, msg):
        self.last_lane_info = msg

    def status_cb(self, msg):
        if msg.data == 'system_ready' and self.drive_state == STATE_WAITING_FOR_SYSTEM:
            self.get_logger().info('System ready signal received. Starting drive.')
            self._set_state(STATE_NORMAL)
            self.start_time = time.time()

    def emergency_cb(self, msg):
        """Receive START / STOP / RESET commands from UI."""
        cmd = msg.data.lower().strip()
        self.get_logger().info(f'[UI] Emergency command: {cmd}')
        if cmd == 'start':
            if self.drive_state in (STATE_WAITING_FOR_SYSTEM, STATE_FINISHED):
                self._set_state(STATE_NORMAL)
                self.start_time = time.time()
                self.tracer.reset_state()
        elif cmd == 'stop':
            self._set_state(STATE_FINISHED)
        elif cmd == 'reset':
            self.detected_signs.clear()
            self.current_sign = None
            self.slow_mode_until = 0.0
            self.tracer.reset_state()
            self._set_state(STATE_WAITING_FOR_SYSTEM)
            self.start_time = None

    def sign_cb(self, msg):
        new_sign = msg.data
        now = time.time()

        if self.drive_state != STATE_NORMAL:
            return

        # Horn: standalone, no state change
        if new_sign == 'horn':
            if now - self.last_buzzer_time > 2.0:
                self._beep_buzzer(now)
                self.last_buzzer_time = now
            return

        # Slow: starts/refreshes slow window
        if new_sign == self.slow_sign_name or new_sign == '20':
            self.slow_mode_until = now + C.SLOW_MODE_DURATION_SEC
            self.get_logger().info(f'>>> Slow mode active until {self.slow_mode_until:.1f}')
            return

        # Each non-horn, non-slow sign triggers at most once
        if new_sign in self.detected_signs:
            return
        self.detected_signs.add(new_sign)
        self.current_sign = new_sign
        self.get_logger().info(f'>>> NEW SIGN: {new_sign}')

        if new_sign == 'stop':
            self.stop_wait_duration = C.STOP_SIGN_WAIT_SEC
            self.next_state_after_stop = STATE_NORMAL
            self._set_state(STATE_STOP_WAIT)

        elif new_sign in ('traffic_light', 'traffic_light_red'):
            # Red light: stop then right turn
            self.stop_wait_duration = C.TRAFFIC_RED_WAIT_SEC
            self.next_state_after_stop = STATE_TURNING
            self.turn_direction = -1.0   # right turn
            self._set_state(STATE_STOP_WAIT)

        elif new_sign == 'traffic_light_green':
            # Green light: right turn without stop
            self.turn_direction = -1.0
            self._set_state(STATE_TURNING)

        elif new_sign in ('left_turn', 'right_turn'):
            self.turn_direction = 1.0 if new_sign == 'left_turn' else -1.0
            self._set_state(STATE_TURNING)

    def red_cb(self, msg):
        """Detect red finish line in BEV (after lockout)."""
        if self.drive_state != STATE_NORMAL:
            return
        if self.start_time is None:
            return
        if (time.time() - self.start_time) < C.RED_DETECT_LOCKOUT_SEC:
            return

        try:
            red_bev = self.bridge.imgmsg_to_cv2(msg, 'mono8')
        except Exception:
            return
        h, w = red_bev.shape
        zone = red_bev[int(h * 0.80):h, int(w * 0.20):int(w * 0.80)]
        density = float(np.sum(zone) / 255.0) / float(zone.size)
        if density > C.RED_DETECT_DENSITY:
            self.get_logger().warn('🔴 FINISH LINE DETECTED. Stopping.')
            self._set_state(STATE_FINISHED)

    # ==================================================================
    # Control loop (drives state machine; publishes cmd_vel)
    # ==================================================================
    def control_loop(self):
        now = time.time()
        state_duration = now - self.state_entered_time

        linear = 0.0
        angular = 0.0

        if self.drive_state == STATE_WAITING_FOR_SYSTEM:
            pass  # stay still

        elif self.drive_state == STATE_NORMAL:
            if self.last_lane_info is None:
                pass
            else:
                # Apply slow window if active
                target_speed = self.base_speed
                if now < self.slow_mode_until:
                    target_speed = self.base_speed * C.SLOW_SPEED_RATIO
                linear, angular = self.tracer.compute(self.last_lane_info, speed=target_speed)

            # Buzzer auto-off
            if self.buzzer_on_until > 0 and now > self.buzzer_on_until:
                self._buzzer_off()

        elif self.drive_state == STATE_STOP_WAIT:
            linear = 0.0
            angular = 0.0
            if state_duration >= self.stop_wait_duration:
                self._cleanup_current_sign()
                self._set_state(self.next_state_after_stop)
                # If next state is NORMAL, reset tracer filter to avoid stale D term
                if self.next_state_after_stop == STATE_NORMAL:
                    self.tracer.reset_state()

        elif self.drive_state == STATE_TURNING:
            linear = 0.0
            angular = self.turn_direction * C.TURN_ANGULAR_VEL
            if state_duration >= C.TURN_DURATION_SEC:
                self._set_state(STATE_POST_TURN_STRAIGHT)

        elif self.drive_state == STATE_POST_TURN_STRAIGHT:
            # Drive straight briefly to let the tracer see fresh lanes,
            # then return to NORMAL (which will pick up line tracing)
            linear = self.base_speed
            angular = 0.0
            if state_duration >= C.POST_TURN_STRAIGHT_SEC:
                self._cleanup_current_sign()
                self.tracer.reset_state()
                self._set_state(STATE_NORMAL)

        elif self.drive_state == STATE_FINISHED:
            linear = 0.0
            angular = 0.0

        # Publish
        twist = Twist()
        twist.linear.x = float(linear)
        twist.angular.z = float(angular)
        self.pub_cmd.publish(twist)

        # Telemetry for UI (JSON-like compact text)
        tel = String()
        l_det = self.last_lane_info.left_detect if self.last_lane_info else False
        r_det = self.last_lane_info.right_detect if self.last_lane_info else False
        lx = self.last_lane_info.left_x if self.last_lane_info else 0.0
        rx = self.last_lane_info.right_x if self.last_lane_info else 0.0
        la = self.last_lane_info.left_angle if self.last_lane_info else 0.0
        ra = self.last_lane_info.right_angle if self.last_lane_info else 0.0
        tel.data = (
            f'{{"state":"{self.drive_state}","sign":"{self.current_sign or "none"}",'
            f'"linear":{linear:.3f},"angular":{angular:.3f},'
            f'"pixel_offset":{self.tracer.pixel_offset:.1f},'
            f'"l_det":{int(l_det)},"r_det":{int(r_det)},'
            f'"l_x":{lx:.1f},"r_x":{rx:.1f},'
            f'"l_ang":{la:.1f},"r_ang":{ra:.1f},'
            f'"slow":{int(now < self.slow_mode_until)}}}'
        )
        self.pub_telemetry.publish(tel)

    # ==================================================================
    # State helpers
    # ==================================================================
    def _set_state(self, new_state):
        if new_state != self.drive_state:
            self.get_logger().info(f'STATE: {self.drive_state} -> {new_state}')
            self.drive_state = new_state
            self.state_entered_time = time.time()
            # Publish state for UI
            sm = String()
            sm.data = new_state
            self.pub_state.publish(sm)

    def _cleanup_current_sign(self):
        # Keep sign in detected_signs to prevent re-trigger; just clear pointer
        self.current_sign = None

    # ==================================================================
    # Buzzer
    # ==================================================================
    def _beep_buzzer(self, now):
        if self.gpio_h is None:
            self.get_logger().info('BEEP! (no GPIO)')
            return
        try:
            lgpio.tx_pwm(self.gpio_h, C.BUZZER_PIN, C.BUZZER_FREQ, 50)
            self.buzzer_on_until = now + C.BUZZER_DURATION_SEC
            self.get_logger().info('BEEP!')
        except Exception as e:
            self.get_logger().warn(f'Buzzer error: {e}')

    def _buzzer_off(self):
        if self.gpio_h is None:
            return
        try:
            lgpio.tx_pwm(self.gpio_h, C.BUZZER_PIN, C.BUZZER_FREQ, 0)
        except Exception:
            pass
        self.buzzer_on_until = 0.0

    # ==================================================================
    def destroy_node(self):
        # Final stop
        twist = Twist()
        try:
            self.pub_cmd.publish(twist)
        except Exception:
            pass
        if self.gpio_h is not None and LGPIO_AVAILABLE:
            try:
                lgpio.tx_pwm(self.gpio_h, C.BUZZER_PIN, C.BUZZER_FREQ, 0)
                lgpio.gpiochip_close(self.gpio_h)
            except Exception:
                pass
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = DrivingControllerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()


if __name__ == '__main__':
    main()
