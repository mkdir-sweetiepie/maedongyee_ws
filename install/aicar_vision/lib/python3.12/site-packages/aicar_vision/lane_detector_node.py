#!/usr/bin/env python3
"""
Lane Detector Node (Turtlebot-style port)
- BEV transform (Bird's Eye View)
- Lane detection via HSV (black/yellow configurable)
- Red finish line detection
- Lane fitting via polyfit -> position (x) + angle for left/right
- Publishes LaneInfo (custom msg)
- Debug: BEV color image + src_points trapezoid overlay
"""

import os
import pickle

import cv2
import numpy as np
import rclpy
from ament_index_python.packages import get_package_share_directory
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image

from aicar_msgs.msg import LaneInfo


class LaneDetectorNode(Node):
    def __init__(self):
        super().__init__('lane_detector_node')
        self.get_logger().info('Lane Detector (BEV + polyfit) started.')

        self.bridge = CvBridge()

        # --- 1. Camera calibration ---
        self.declare_parameter('image_topic', '/camera/image_raw')
        pkg_share = get_package_share_directory('aicar_vision')
        default_calib = os.path.join(pkg_share, 'calibration_data', 'calibration.p')
        self.declare_parameter('calibration_file', default_calib)
        calib_path = self.get_parameter('calibration_file').get_parameter_value().string_value

        try:
            with open(calib_path, 'rb') as f:
                calib = pickle.load(f)
                self.mtx = calib['mtx']
                self.dist = calib['dist']
            self.get_logger().info(f'Calibration loaded: {calib_path}')
        except Exception as e:
            self.get_logger().fatal(f'Failed to load calibration: {e}')
            rclpy.shutdown()
            return

        # --- 2. BEV parameters ---
        self.img_w = 640
        self.img_h = 480
        self.src_points = np.float32([
            (0, 480),
            (100, 380),
            (540, 380),
            (640, 480),
        ])
        self.dst_points = np.float32([
            (int(self.img_w * 0.2), int(self.img_h)),
            (int(self.img_w * 0.2), 0),
            (int(self.img_w * 0.8), 0),
            (int(self.img_w * 0.8), int(self.img_h)),
        ])
        self.M = cv2.getPerspectiveTransform(self.src_points, self.dst_points)

        # --- 3. HSV thresholds ---
        # Current config: BLACK lane (S<80, V<60)
        # For yellow lane, use: lower=[18,80,80], upper=[38,255,255]
        self.lower_yellow = np.array([0, 0, 0])
        self.upper_yellow = np.array([180, 80, 60])

        # Red finish line
        self.lower_red1 = np.array([0, 40, 100])
        self.upper_red1 = np.array([15, 255, 255])
        self.lower_red2 = np.array([165, 40, 100])
        self.upper_red2 = np.array([180, 255, 255])

        self.kernel = np.ones((5, 5), np.uint8)

        # --- 4. Polyfit ROI parameters ---
        self.fit_y_start = int(self.img_h * 0.40)
        self.fit_y_end = self.img_h - 5
        self.fit_step = 10
        self.min_pixels_per_row = 3
        self.min_rows_for_fit = 5

        # --- 5. Subscriptions ---
        img_topic = self.get_parameter('image_topic').get_parameter_value().string_value
        self.sub_img = self.create_subscription(Image, img_topic, self.image_cb, 10)

        # --- 6. Publishers ---
        self.pub_bev_lane = self.create_publisher(Image, '/image_bev_binary', 10)
        self.pub_bev_red = self.create_publisher(Image, '/image_red_bev', 10)
        self.pub_bev_color = self.create_publisher(Image, '/image_bev_color', 10)
        self.pub_processed = self.create_publisher(Image, '/image_processed', 10)
        self.pub_lane_info = self.create_publisher(LaneInfo, '/lane_info', 10)

    # ------------------------------------------------------------------
    def undistort(self, img):
        return cv2.undistort(img, self.mtx, self.dist, None, self.mtx)

    def warp(self, img):
        return cv2.warpPerspective(img, self.M, (self.img_w, self.img_h))

    def make_yellow_mask(self, hsv):
        m = cv2.inRange(hsv, self.lower_yellow, self.upper_yellow)
        m = cv2.dilate(m, self.kernel, iterations=1)
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, self.kernel)
        return m

    def make_red_mask(self, hsv):
        m1 = cv2.inRange(hsv, self.lower_red1, self.upper_red1)
        m2 = cv2.inRange(hsv, self.lower_red2, self.upper_red2)
        return cv2.dilate(m1 | m2, self.kernel, iterations=1)

    # ------------------------------------------------------------------
    def fit_one_side(self, bev_binary, side):
        h, w = bev_binary.shape
        mid_x = w // 2

        if side == 'left':
            roi = bev_binary[:, :mid_x]
            x_offset = 0
        else:
            roi = bev_binary[:, mid_x:]
            x_offset = mid_x

        ys, xs_med = [], []
        total_pixels = 0
        for y in range(self.fit_y_start, self.fit_y_end, self.fit_step):
            row = roi[y, :]
            idx = np.nonzero(row)[0]
            if len(idx) >= self.min_pixels_per_row:
                ys.append(y)
                xs_med.append(np.median(idx))
                total_pixels += len(idx)

        if len(ys) < self.min_rows_for_fit:
            return False, 0.0, 90.0, total_pixels

        ys_np = np.array(ys, dtype=np.float32)
        xs_np = np.array(xs_med, dtype=np.float32)
        a, b = np.polyfit(ys_np, xs_np, 1)

        x_at_bottom = a * (h - 1) + b + x_offset
        angle_deg = 90.0 - np.degrees(np.arctan(a))

        return True, float(x_at_bottom), float(angle_deg), total_pixels

    # ------------------------------------------------------------------
    def image_cb(self, msg):
        try:
            cv_img = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        except Exception as e:
            self.get_logger().error(f'cv_bridge fail: {e}')
            return

        # 1. Undistort + HSV
        undist = self.undistort(cv_img)
        blurred = cv2.GaussianBlur(undist, (5, 5), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # 2. Masks
        mask_yellow = self.make_yellow_mask(hsv)
        bev_yellow = self.warp(mask_yellow)

        mask_red = self.make_red_mask(hsv)
        bev_red = self.warp(mask_red)

        # 3. BEV color (debug) - 원본 컬러를 BEV로 변환
        bev_color = self.warp(undist)

        # 4. Polyfit -> LaneInfo
        l_det, l_x, l_ang, l_cnt = self.fit_one_side(bev_yellow, 'left')
        r_det, r_x, r_ang, r_cnt = self.fit_one_side(bev_yellow, 'right')

        info = LaneInfo()
        info.header = msg.header
        info.left_detect = l_det
        info.left_x = l_x
        info.left_angle = l_ang
        info.right_detect = r_det
        info.right_x = r_x
        info.right_angle = r_ang
        info.left_pixel_count = int(l_cnt)
        info.right_pixel_count = int(r_cnt)
        self.pub_lane_info.publish(info)

        # 5. Camera 원본에 src_points 사다리꼴 그려서 publish (튜닝 시각화)
        debug_orig = undist.copy()
        pts = self.src_points.astype(np.int32).reshape(-1, 1, 2)
        cv2.polylines(debug_orig, [pts], True, (0, 0, 255), 2)
        for i, p in enumerate(self.src_points.astype(int)):
            cv2.circle(debug_orig, tuple(p), 6, (0, 255, 255), -1)
            cv2.putText(debug_orig, str(i + 1), (p[0] + 8, p[1] - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        # 6. Publish images
        m_yellow = self.bridge.cv2_to_imgmsg(bev_yellow, 'mono8')
        m_yellow.header = msg.header
        self.pub_bev_lane.publish(m_yellow)

        m_red = self.bridge.cv2_to_imgmsg(bev_red, 'mono8')
        m_red.header = msg.header
        self.pub_bev_red.publish(m_red)

        m_bev_color = self.bridge.cv2_to_imgmsg(bev_color, 'bgr8')
        m_bev_color.header = msg.header
        self.pub_bev_color.publish(m_bev_color)

        m_proc = self.bridge.cv2_to_imgmsg(debug_orig, 'bgr8')
        m_proc.header = msg.header
        self.pub_processed.publish(m_proc)


def main(args=None):
    rclpy.init(args=args)
    node = LaneDetectorNode()
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