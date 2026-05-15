#!/usr/bin/env python3
"""
Sign Detector Node (YOLOv8 TFLite) — 매동이 원본 그대로 살린 버전.

기존 매동이 코드에서 수정한 부분:
1. image_topic 파라미터화 (default '/camera/image_raw'로 통일)
2. traffic_light 매핑 주석으로 명시 (모델이 단일 클래스라 driving_controller에서 처리)
3. debug_image_publisher 유지 (/image_sign_debug)
"""

import os

import cv2
import rclpy
from ament_index_python.packages import get_package_share_directory
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from ultralytics import YOLO


class SignDetectorNode(Node):
    def __init__(self):
        super().__init__('sign_detector_node')
        self.get_logger().info('Sign Detector Node (YOLOv8 TFLite) started.')

        self.bridge = CvBridge()
        self.is_model_loaded = False

        # --- 1. 모델 경로 ---
        package_name = 'aicar_vision'
        try:
            pkg_share = get_package_share_directory(package_name)
            model_path = os.path.join(pkg_share, 'models', 'best_float32.tflite')
        except Exception:
            model_path = '/root/aicar_ws/src/aicar_vision/models/best_float32.tflite'

        self.declare_parameter('model_path', model_path)
        final_model_path = self.get_parameter('model_path').get_parameter_value().string_value
        self.get_logger().info(f'Loading model from: {final_model_path}')

        # --- 2. YOLO 모델 로드 ---
        try:
            self.model = YOLO(final_model_path, task='detect')
            self.is_model_loaded = True
            self.get_logger().info('>>> Model Loaded Successfully! System Ready.')
        except Exception as e:
            self.get_logger().fatal(f'Failed to load YOLO model: {e}')
            return

        # --- 3. 라벨 매핑 ---
        # NOTE: 모델이 traffic_light을 단일 클래스로 학습했음.
        # driving_controller_node에서 'traffic_light' 받으면 정지+우회전(빨간불 동작)을
        # 하도록 처리해두었음. 안전한 디폴트 = 빨간불 대응.
        # 만약 평가 당일 신호등 색을 따로 판단하고 싶으면 별도 HSV ROI 검출 로직을 추가해
        # 'traffic_light_green' / 'traffic_light_red' 둘 중 하나로 분기 발행하면 됨.
        self.last_published_sign = None
        self.confidence_threshold = 0.60
        self.class_mapping = {
            'stop_sign': 'stop',
            'left_turn_sign': 'left_turn',
            'right_turn_sign': 'right_turn',
            'horn_sign': 'horn',
            '20_sign': 'slow',
            'traffic_light': 'traffic_light',  # ← controller에서 정지+우회전으로 처리
        }

        # --- 4. ROS 구독/발행 ---
        self.declare_parameter('image_topic', '/camera/image_raw')
        image_topic = self.get_parameter('image_topic').get_parameter_value().string_value
        self.subscription = self.create_subscription(
            Image, image_topic, self.image_callback, 10)
        self.get_logger().info(f'Subscribing to image topic: {image_topic}')

        self.publisher_ = self.create_publisher(String, '/sign_detection', 10)
        self.debug_image_publisher = self.create_publisher(Image, '/image_sign_debug', 10)
        self.status_publisher_ = self.create_publisher(String, '/system_status', 10)
        self.create_timer(1.0, self.publish_status)

    def publish_status(self):
        if self.is_model_loaded:
            msg = String()
            msg.data = "system_ready"
            self.status_publisher_.publish(msg)

    def image_callback(self, msg):
        if not self.is_model_loaded:
            return

        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except Exception as e:
            self.get_logger().error(f'CV Bridge error: {e}')
            return

        debug_image = cv_image.copy()

        # --- 5. YOLO 추론 ---
        try:
            results = self.model(cv_image, verbose=False)
        except Exception as e:
            self.get_logger().error(f'YOLO inference error: {e}')
            return

        # --- 6. 최고 신뢰도 검출 1개만 발행 ---
        best_sign = None
        best_conf = 0.0
        if len(results) > 0 and results[0].boxes is not None:
            boxes = results[0].boxes
            names = results[0].names
            for i in range(len(boxes)):
                conf = float(boxes.conf[i])
                cls_idx = int(boxes.cls[i])
                cls_name = names.get(cls_idx, str(cls_idx))
                if conf >= self.confidence_threshold:
                    mapped = self.class_mapping.get(cls_name)
                    if mapped is not None and conf > best_conf:
                        best_sign = mapped
                        best_conf = conf
                        # debug box
                        xyxy = boxes.xyxy[i].cpu().numpy().astype(int)
                        cv2.rectangle(debug_image, (xyxy[0], xyxy[1]),
                                      (xyxy[2], xyxy[3]), (0, 255, 0), 2)
                        cv2.putText(debug_image, f'{mapped} {conf:.2f}',
                                    (xyxy[0], max(0, xyxy[1] - 6)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        if best_sign is not None and best_sign != self.last_published_sign:
            out = String()
            out.data = best_sign
            self.publisher_.publish(out)
            self.last_published_sign = best_sign
            self.get_logger().info(f'Sign detected: {best_sign} (conf={best_conf:.2f})')

        # 디버그 이미지 발행
        try:
            dbg_msg = self.bridge.cv2_to_imgmsg(debug_image, 'bgr8')
            dbg_msg.header = msg.header
            self.debug_image_publisher.publish(dbg_msg)
        except Exception:
            pass


def main(args=None):
    rclpy.init(args=args)
    node = SignDetectorNode()
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
