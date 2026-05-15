#!/usr/bin/env python3
"""
Lane Detector Node (Turtlebot-style port)
- BEV transform (Bird's Eye View)
- Yellow lane detection via HSV
- Red finish line detection
- Lane fitting via polyfit -> position (x) + angle for left/right
- Publishes LaneInfo (custom msg)
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
        self.declare_parameter('image_topic', '/camera_node/image_raw')
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
            (170, 350),
            (470, 350),
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
        # Yellow lane (V floor lowered for shadow robustness)
        self.lower_yellow = np.array([18, 80, 80])
        self.upper_yellow = np.array([38, 255, 255])
        # Red finish line (wraps around in HSV)
        self.lower_red1 = np.array([0, 40, 100])
        self.upper_red1 = np.array([15, 255, 255])
        self.lower_red2 = np.array([165, 40, 100])
        self.upper_red2 = np.array([180, 255, 255])

        self.kernel = np.ones((5, 5), np.uint8)

        # --- 4. Polyfit ROI parameters ---
        # Sample rows from bottom up to mid-screen
        self.fit_y_start = int(self.img_h * 0.40)  # top of ROI
        self.fit_y_end = self.img_h - 5            # bottom of ROI
        self.fit_step = 10                          # row sampling step
        self.min_pixels_per_row = 3                 # min yellow pixels per row to count
        self.min_rows_for_fit = 5                   # min rows to attempt polyfit

        # --- 5. Subscriptions ---
        img_topic = self.get_parameter('image_topic').get_parameter_value().string_value
        self.sub_img = self.create_subscription(Image, img_topic, self.image_cb, 10)

        # --- 6. Publishers ---
        self.pub_bev_lane = self.create_publisher(Image, '/image_bev_binary', 10)
        self.pub_bev_red = self.create_publisher(Image, '/image_red_bev', 10)
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
        """
        Polyfit one side of the BEV lane mask.
        side: 'left' or 'right'
        Returns: (detected, x_at_bottom, angle_deg, pixel_count)
                 angle_deg: 90 = vertical, <90 = leans right, >90 = leans left
        """
        h, w = bev_binary.shape
        mid_x = w // 2

        if side == 'left':
            roi = bev_binary[:, :mid_x]
            x_offset = 0
        else:
            roi = bev_binary[:, mid_x:]
            x_offset = mid_x

        # Per-row median x of nonzero pixels (robust to outliers)
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

        # Fit x = a*y + b  (linear in y; BEV makes lines near-straight)
        a, b = np.polyfit(ys_np, xs_np, 1)

        x_at_bottom = a * (h - 1) + b + x_offset
        # angle measured from horizontal: dx/dy = a -> theta = atan(a)
        # We want "vertical = 90 deg" convention to match turtlebot
        # If line is vertical (a small), theta near 0 -> angle = 90 - 0 = 90
        # If line slopes right as y increases (a>0), theta>0 -> angle<90
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

        # 2. Yellow lane (BEV)
        mask_yellow = self.make_yellow_mask(hsv)
        bev_yellow = self.warp(mask_yellow)

        # 3. Red finish line (BEV)
        mask_red = self.make_red_mask(hsv)
        bev_red = self.warp(mask_red)

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

        # 5. Publish BEV images for debug + red detection
        m_yellow = self.bridge.cv2_to_imgmsg(bev_yellow, 'mono8')
        m_yellow.header = msg.header
        self.pub_bev_lane.publish(m_yellow)

        m_red = self.bridge.cv2_to_imgmsg(bev_red, 'mono8')
        m_red.header = msg.header
        self.pub_bev_red.publish(m_red)

        m_proc = self.bridge.cv2_to_imgmsg(undist, 'bgr8')
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
