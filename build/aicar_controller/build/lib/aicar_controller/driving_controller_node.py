#!/usr/bin/env python3
"""
Driving Controller Node (매동이 evaluation rubric).

Split-turn algorithm:
  TURNING → TURN_PAUSE → TURNING → TURN_PAUSE → TURNING → POST_TURN_STRAIGHT
  (30° × 3 = ~90°)  사이마다 약한 직진을 끼워 부드럽게 회전.

Auto corner detection (both lanes lost):
  - 양쪽 차선 모두 N프레임 연속 안 보이면 코너로 판정.
  - 회전 방향은 track_direction 파라미터 (cw=우, ccw=좌)로 결정.
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
STATE_TURN_PAUSE = 'TURN_PAUSE'           # 분할 회전 사이의 짧은 직진
STATE_POST_TURN_STRAIGHT = 'POST_TURN_STRAIGHT'
STATE_FINISHED = 'FINISHED'


class DrivingControllerNode(Node):
    def __init__(self):
        super().__init__('driving_controller_node')

        self.bridge = CvBridge()

        # --- Parameters ---
        self.declare_parameter('vehicle_speed', 0.20)
        self.declare_parameter('skip_system_handshake', False)
        self.declare_parameter('auto_corner', True)
        self.declare_parameter('track_direction', 'cw')

        self.base_speed = self.get_parameter('vehicle_speed').value
        self.skip_handshake = self.get_parameter('skip_system_handshake').value
        self.auto_corner_enabled = self.get_parameter('auto_corner').value
        track_dir_str = self.get_parameter('track_direction').value.lower().strip()

        if track_dir_str == 'cw':
            self.corner_turn_dir = -1.0
            track_label = 'CW (clockwise / right turns)'
        elif track_dir_str == 'ccw':
            self.corner_turn_dir = +1.0
            track_label = 'CCW (counter-clockwise / left turns)'
        else:
            self.get_logger().warn(
                f'Unknown track_direction "{track_dir_str}", defaulting to CW')
            self.corner_turn_dir = -1.0
            track_label = 'CW (default)'

        self.get_logger().info(f'Track direction: {track_label}')
        self.get_logger().info(
            f'Turn config: {C.TURN_STEPS} steps × '
            f'{C.TURN_STEP_DURATION_SEC}s @ {C.TURN_ANGULAR_VEL}rad/s, '
            f'pause {C.TURN_PAUSE_DURATION_SEC}s @ {C.TURN_PAUSE_LINEAR}m/s')

        # --- Subscriptions ---
        self.sub_lane = self.create_subscription(
            LaneInfo, '/lane_info', self.lane_cb, 10)
        self.sub_red_bev = self.create_subscription(
            Image, '/image_red_bev', self.red_cb, 10)
        self.sub_sign = self.create_subscription(
            String, '/sign_detection', self.sign_cb, 10)
        self.sub_status = self.create_subscription(
            String, '/system_status', self.status_cb, 10)
        self.sub_emergency = self.create_subscription(
            String, '/emergency_command', self.emergency_cb, 10)

        # --- Publishers ---
        self.pub_cmd = self.create_publisher(Twist, '/cmd_vel', 10)
        self.pub_state = self.create_publisher(String, '/drive_state', 10)
        self.pub_telemetry = self.create_publisher(String, '/telemetry', 10)

        # --- LineTracer ---
        self.tracer = LineTracer(
            base_speed=self.base_speed, logger=self.get_logger())

        # --- State machine ---
        if self.skip_handshake:
            self.drive_state = STATE_NORMAL
            self.start_time = time.time()
        else:
            self.drive_state = STATE_WAITING_FOR_SYSTEM
            self.start_time = None
        self.state_entered_time = time.time()

        # Sign tracking
        self.detected_signs = set()
        self.current_sign = None
        self.next_state_after_stop = STATE_NORMAL
        self.turn_direction = 1.0
        self.stop_wait_duration = C.STOP_SIGN_WAIT_SEC

        # Split-turn counter (몇 번째 회전 단계인지)
        self._turn_step_count = 0

        # Slow mode
        self.slow_mode_until = 0.0
        self.last_buzzer_time = 0.0
        self.slow_sign_name = 'slow'

        # ----- Auto-corner state -----
        self._corner_cooldown_until = 0.0
        self._both_lost_count = 0
        self._pre_turn_until = 0.0
        self._pending_turn_dir = 0.0

        # Buzzer
        self.gpio_h = None
        self.buzzer_on_until = 0.0
        if LGPIO_AVAILABLE:
            try:
                self.gpio_h = lgpio.gpiochip_open(4)
                lgpio.gpio_claim_output(self.gpio_h, C.BUZZER_PIN)
            except Exception as e:
                self.get_logger().warn(f'Buzzer GPIO init failed: {e}')
                self.gpio_h = None

        # Main control loop
        self.last_lane_info = None
        self.timer = self.create_timer(1.0 / 30.0, self.control_loop)

        self.get_logger().info(
            f'Initial state: {self.drive_state}, '
            f'auto_corner={self.auto_corner_enabled}')

    # ==================================================================
    # Callbacks
    # ==================================================================
    def lane_cb(self, msg):
        self.last_lane_info = msg

    def status_cb(self, msg):
        if msg.data == 'system_ready' and self.drive_state == STATE_WAITING_FOR_SYSTEM:
            self.get_logger().info('System ready signal received. Starting drive.')
            self._set_state(STATE_NORMAL)
            self.start_time = time.time()

    def emergency_cb(self, msg):
        cmd = msg.data.lower().strip()
        self.get_logger().info(f'[UI] Emergency command: {cmd}')
        if cmd == 'start':
            if self.drive_state in (STATE_WAITING_FOR_SYSTEM, STATE_FINISHED):
                self._reset_all_state()
                self._set_state(STATE_NORMAL)
                self.start_time = time.time()
                self.tracer.reset_state()
        elif cmd == 'stop':
            self._set_state(STATE_FINISHED)
        elif cmd == 'reset':
            self.detected_signs.clear()
            self.current_sign = None
            self.slow_mode_until = 0.0
            self._reset_all_state()
            self.tracer.reset_state()
            self._set_state(STATE_WAITING_FOR_SYSTEM)
            self.start_time = None

    def sign_cb(self, msg):
        new_sign = msg.data
        now = time.time()
        if self.drive_state != STATE_NORMAL:
            return

        if new_sign == 'horn':
            if now - self.last_buzzer_time > 2.0:
                self._beep_buzzer(now)
                self.last_buzzer_time = now
            return

        if new_sign == self.slow_sign_name or new_sign == '20':
            self.slow_mode_until = now + C.SLOW_MODE_DURATION_SEC
            self.get_logger().info(
                f'>>> Slow mode active until {self.slow_mode_until:.1f}')
            return

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
            self.stop_wait_duration = C.TRAFFIC_RED_WAIT_SEC
            self.next_state_after_stop = STATE_TURNING
            self.turn_direction = -1.0
            self._turn_step_count = 0
            self._set_state(STATE_STOP_WAIT)
        elif new_sign == 'traffic_light_green':
            self.turn_direction = -1.0
            self._turn_step_count = 0
            self._set_state(STATE_TURNING)
        elif new_sign in ('left_turn', 'right_turn'):
            self.turn_direction = 1.0 if new_sign == 'left_turn' else -1.0
            self._turn_step_count = 0
            self._set_state(STATE_TURNING)

    def red_cb(self, msg):
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
    # Auto-corner detection
    # ==================================================================
    def _reset_all_state(self):
        """Reset corner detection + split-turn state."""
        self._corner_cooldown_until = 0.0
        self._both_lost_count = 0
        self._pre_turn_until = 0.0
        self._pending_turn_dir = 0.0
        self._turn_step_count = 0

    def _check_lane_corner(self, now):
        if not self.auto_corner_enabled:
            return False
        if now < self._corner_cooldown_until:
            return False

        # ----- PRE_TURN 시간 체크 -----
        if self._pre_turn_until > 0.0:
            if now >= self._pre_turn_until:
                self.turn_direction = self._pending_turn_dir
                self._pre_turn_until = 0.0
                self._pending_turn_dir = 0.0
                self._corner_cooldown_until = now + C.CORNER_COOLDOWN_SEC
                self._turn_step_count = 0
                dir_str = 'L' if self.turn_direction > 0 else 'R'
                self.get_logger().info(f'🔄 AUTO TURN starting (dir={dir_str})')
                self._set_state(STATE_TURNING)
                return True
            return False

        # ----- 양쪽 동시 미검출 카운트 -----
        info = self.last_lane_info
        if info is None:
            return False

        if (not info.left_detect) and (not info.right_detect):
            self._both_lost_count += 1
        else:
            self._both_lost_count = 0

        if self._both_lost_count >= C.CORNER_BOTH_LOST_FRAMES:
            self._pre_turn_until = now + C.CORNER_PRE_TURN_DELAY_SEC
            self._pending_turn_dir = self.corner_turn_dir
            self._both_lost_count = 0
            dir_str = 'L' if self.corner_turn_dir > 0 else 'R'
            self.get_logger().info(
                f'🔄 CORNER triggered (both lanes lost, '
                f'delay={C.CORNER_PRE_TURN_DELAY_SEC}s, then turn {dir_str})')
            return False

        return False

    # ==================================================================
    # Control loop
    # ==================================================================
    def control_loop(self):
        now = time.time()
        state_duration = now - self.state_entered_time

        linear = 0.0
        angular = 0.0

        if self.drive_state == STATE_WAITING_FOR_SYSTEM:
            pass

        elif self.drive_state == STATE_NORMAL:
            if self.last_lane_info is not None:
                state_changed = self._check_lane_corner(now)
                if not state_changed:
                    target_speed = self.base_speed
                    if now < self.slow_mode_until:
                        target_speed = self.base_speed * C.SLOW_SPEED_RATIO
                    linear, angular = self.tracer.compute(
                        self.last_lane_info, speed=target_speed)

            if self.buzzer_on_until > 0 and now > self.buzzer_on_until:
                self._buzzer_off()

        elif self.drive_state == STATE_STOP_WAIT:
            linear = 0.0
            angular = 0.0
            if state_duration >= self.stop_wait_duration:
                self._cleanup_current_sign()
                self._set_state(self.next_state_after_stop)
                if self.next_state_after_stop == STATE_NORMAL:
                    self.tracer.reset_state()
                elif self.next_state_after_stop == STATE_TURNING:
                    self._turn_step_count = 0

        elif self.drive_state == STATE_TURNING:
            # 분할 회전: 한 번 돌고 PAUSE 또는 종료
            linear = 0.0
            angular = self.turn_direction * C.TURN_ANGULAR_VEL
            if state_duration >= C.TURN_STEP_DURATION_SEC:
                self._turn_step_count += 1
                self.get_logger().info(
                    f'  turn step {self._turn_step_count}/{C.TURN_STEPS} done')
                if self._turn_step_count >= C.TURN_STEPS:
                    # 모든 회전 완료
                    self._turn_step_count = 0
                    self._set_state(STATE_POST_TURN_STRAIGHT)
                else:
                    # 다음 회전 전 잠깐 직진
                    self._set_state(STATE_TURN_PAUSE)

        elif self.drive_state == STATE_TURN_PAUSE:
            # 회전 사이의 약한 직진
            linear = C.TURN_PAUSE_LINEAR
            angular = 0.0
            if state_duration >= C.TURN_PAUSE_DURATION_SEC:
                self._set_state(STATE_TURNING)

        elif self.drive_state == STATE_POST_TURN_STRAIGHT:
            linear = self.base_speed
            angular = 0.0
            if state_duration >= C.POST_TURN_STRAIGHT_SEC:
                self._cleanup_current_sign()
                self.tracer.reset_state()
                self._set_state(STATE_NORMAL)

        elif self.drive_state == STATE_FINISHED:
            linear = 0.0
            angular = 0.0

        # Publish cmd_vel
        twist = Twist()
        twist.linear.x = float(linear)
        twist.angular.z = float(angular)
        self.pub_cmd.publish(twist)

        # Telemetry
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
    # Helpers
    # ==================================================================
    def _set_state(self, new_state):
        if new_state != self.drive_state:
            self.get_logger().info(f'STATE: {self.drive_state} -> {new_state}')
            self.drive_state = new_state
            self.state_entered_time = time.time()
            sm = String()
            sm.data = new_state
            self.pub_state.publish(sm)

    def _cleanup_current_sign(self):
        self.current_sign = None

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

    def destroy_node(self):
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