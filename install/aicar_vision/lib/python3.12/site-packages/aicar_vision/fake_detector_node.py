#!/usr/bin/env python3
"""
Fake Sign Detector — 키보드로 표지판 신호를 수동 발행하는 디버그용 노드.
YOLO 없이 라인트레이싱 + 상태머신을 테스트할 때 사용.
"""

import sys
import threading

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

SIGN_MAP = {
    '1': 'stop',
    '2': 'left_turn',
    '3': 'right_turn',
    '4': 'traffic_light_green',
    '5': 'traffic_light',      # = red light 동작 (정지+우회전)
    '6': 'horn',
    '7': 'slow',
}

MENU = """
---------------------------------
 Fake Sign Detector (aicar_vision)
---------------------------------
[1] stop
[2] left_turn
[3] right_turn
[4] traffic_light_green
[5] traffic_light (red)
[6] horn
[7] slow
---------------------------------
[r] system_ready (handshake)
[q] Quit
---------------------------------
Enter: """


class FakeDetectorNode(Node):
    def __init__(self):
        super().__init__('fake_detector_node')
        self.get_logger().info('Fake Sign Detector Node started.')
        self.publisher_ = self.create_publisher(String, '/sign_detection', 10)
        self.status_publisher_ = self.create_publisher(String, '/system_status', 10)

        self.input_thread = threading.Thread(target=self.input_loop)
        self.input_thread.start()

    def input_loop(self):
        print(MENU, end='', flush=True)
        while rclpy.ok():
            try:
                user_input = sys.stdin.readline().strip()

                if user_input == 'q':
                    break

                if user_input == 'r':
                    msg = String()
                    msg.data = "system_ready"
                    self.status_publisher_.publish(msg)
                    self.get_logger().info('Published: system_ready')
                elif user_input in SIGN_MAP:
                    sign_name = SIGN_MAP[user_input]
                    msg = String()
                    msg.data = sign_name
                    self.publisher_.publish(msg)
                    self.get_logger().info(f'Published sign: "{sign_name}"')
                elif user_input:
                    print("\nInvalid input.")

                print(MENU, end='', flush=True)

            except EOFError:
                break
            except Exception as e:
                self.get_logger().error(f'Input loop error: {e}')
                break

        self.get_logger().info('Shutting down fake detector node...')
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = FakeDetectorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if node.input_thread.is_alive():
            node.input_thread.join(timeout=1.0)
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
