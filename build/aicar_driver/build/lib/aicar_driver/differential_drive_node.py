#!/usr/bin/env python3
"""
Differential Drive Node (매동이 원본 살림 + 약간의 안전 보강).

Twist /cmd_vel -> 차동 구동 역기구학 -> GPIO PWM.

NOTE: 매동이 원본의 두 버전 중 부호 일관성이 맞는 쪽으로 통합함.
      (한 버전은 linear_x = -msg.linear.x 처럼 부호 반전이 있었는데,
       이는 모터 배선 방향 보정용이므로 invert 파라미터로 빼냄)
"""

import rclpy
import numpy as np
from rclpy.node import Node
from geometry_msgs.msg import Twist

try:
    import lgpio
    LGPIO_AVAILABLE = True
except ImportError:
    LGPIO_AVAILABLE = False


# --- 하드웨어 핀 정의 (매동이 원본 그대로) ---
PWMA = 18
AIN1 = 22
AIN2 = 27
PWMB = 23
BIN1 = 25
BIN2 = 24
GPIOCHIP = 4
PWM_FREQ = 1000


class MotorControllerNode(Node):
    def __init__(self):
        super().__init__('differential_drive_node')
        self.get_logger().info('Motor Node (Twist) started.')

        # --- 파라미터 ---
        self.declare_parameter('wheel_separation', 0.106)
        self.declare_parameter('speed_gain', 150.0)
        self.declare_parameter('angular_gain', 1.85)
        self.declare_parameter('invert_linear', False)
        self.declare_parameter('invert_angular', False)
        self.declare_parameter('swap_motors', False)  # 좌/우 모터 바꿔달았을 경우

        self.wheel_sep = self.get_parameter('wheel_separation').value
        self.speed_gain = self.get_parameter('speed_gain').value
        self.angular_gain = self.get_parameter('angular_gain').value
        self.invert_linear = self.get_parameter('invert_linear').value
        self.invert_angular = self.get_parameter('invert_angular').value
        self.swap_motors = self.get_parameter('swap_motors').value

        # --- GPIO 초기화 ---
        self.h = None
        if LGPIO_AVAILABLE:
            try:
                self.h = lgpio.gpiochip_open(GPIOCHIP)
                for pin in [PWMA, AIN1, AIN2, PWMB, BIN1, BIN2]:
                    lgpio.gpio_claim_output(self.h, pin)
                self.motor_stop()
                self.get_logger().info('GPIO initialized.')
            except Exception as e:
                self.get_logger().fatal(f'GPIO init failed: {e}')
                self.h = None
        else:
            self.get_logger().warn('lgpio not available — running in dry mode.')

        # --- 구독 ---
        self.subscription = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_vel_callback, 10)

    def cmd_vel_callback(self, msg):
        linear_x = msg.linear.x
        angular_z = msg.angular.z

        if self.invert_linear:
            linear_x = -linear_x
        if self.invert_angular:
            angular_z = -angular_z

        angular_amplified = angular_z * self.angular_gain

        # 차동 구동 역기구학
        vl_ms = linear_x - (angular_amplified * self.wheel_sep / 2.0)
        vr_ms = linear_x + (angular_amplified * self.wheel_sep / 2.0)

        duty_l = float(np.clip(vl_ms * self.speed_gain, -100, 100))
        duty_r = float(np.clip(vr_ms * self.speed_gain, -100, 100))

        if self.swap_motors:
            duty_l, duty_r = duty_r, duty_l

        self.set_motor(AIN1, AIN2, PWMA, duty_l)
        self.set_motor(BIN1, BIN2, PWMB, duty_r)

    def set_motor(self, in1, in2, pwm_pin, duty):
        if self.h is None:
            return
        if duty >= 0:
            lgpio.gpio_write(self.h, in1, 0)
            lgpio.gpio_write(self.h, in2, 1)
        else:
            lgpio.gpio_write(self.h, in1, 1)
            lgpio.gpio_write(self.h, in2, 0)
        lgpio.tx_pwm(self.h, pwm_pin, PWM_FREQ, abs(duty))

    def motor_stop(self):
        self.set_motor(AIN1, AIN2, PWMA, 0)
        self.set_motor(BIN1, BIN2, PWMB, 0)

    def destroy_node(self):
        if self.h is not None:
            self.motor_stop()
            try:
                lgpio.gpiochip_close(self.h)
            except Exception:
                pass
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = MotorControllerNode()
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
