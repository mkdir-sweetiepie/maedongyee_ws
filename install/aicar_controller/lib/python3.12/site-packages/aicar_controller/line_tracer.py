"""
LineTracer: Python port of 2024_turtlebot's RobitDriving::lineTracing().

Key features carried over from the C++ original:
1. Angle + position weighted error
2. pixel_offset self-learning (track width learned from both-lanes frames)
3. angular_z LPF (f1*prev + f2*new) - 1st order low-pass
4. PD on pixel_gap
5. Asymmetric clamps for one-side-only modes (MAX_REVERSE)
6. Curvature-based speed reduction (sharper steer => slower)
7. Linear speed slew rate limiting
8. Separate gains for left-curve / right-curve / straight modes
"""

import math
from . import constants as C


class LineTracer:
    """
    Stateless interface: feed lane info per frame, get (linear, angular) command.
    Internal state is kept between calls (LPF history, learned offset, etc).
    """

    def __init__(self, base_speed=0.2, logger=None):
        self.base_speed = base_speed
        self.logger = logger

        # Persistent state (turtlebot used static vars; we keep as members)
        self.pre_pixel_gap = 0.0
        self.angular_z = 0.0
        self.before_linear_x = 0.0
        self.pixel_offset = float(C.DEFAULT_PIXEL_OFFSET)  # learned half-track-width

    # ------------------------------------------------------------------
    def reset_state(self):
        """Reset filter state (call after a stop / turn so old values don't leak in)."""
        self.pre_pixel_gap = 0.0
        self.angular_z = 0.0
        self.before_linear_x = 0.0

    # ------------------------------------------------------------------
    def compute(self, lane_info, speed=None):
        """
        lane_info: LaneInfo msg-like object with fields:
            left_detect, left_x, left_angle
            right_detect, right_x, right_angle
        speed: target base speed for this frame (overrides self.base_speed if set)
        Returns: (linear_x, angular_z)
        """
        if speed is None:
            speed = self.base_speed

        # Speed envelope for this frame
        min_lin_v = speed * C.MIN_LINEAR_RATIO
        max_lin_v = speed * C.MAX_LINEAR_RATIO

        linear_x = speed
        pixel_gap = 0.0
        early_return = False

        l_det = lane_info.left_detect
        r_det = lane_info.right_detect
        lx = lane_info.left_x
        rx = lane_info.right_x
        l_ang = lane_info.left_angle
        r_ang = lane_info.right_angle

        # ============================================================
        # CASE A: Both lanes visible -> straight mode + learn offset
        # ============================================================
        if l_det and r_det:
            middle_pt = (lx + rx) / 2.0
            middle_ang = (l_ang + r_ang) / 2.0

            # Self-learning: store half-track-width in pixels
            # In turtlebot: pixel_offset = (320 - right + left) / 2
            # Adapted to 640-wide BEV: same formula, half-distance from center
            self.pixel_offset = (C.BEV_WIDTH - rx + lx) / 2.0

            # Error: angle-weighted + position-weighted
            angle_err = (middle_ang - 90.0) * C.STRAIGHT_ANGLE_RATE
            pos_err = (C.ROBOT_CENTER_PX - middle_pt) * (1.0 - C.STRAIGHT_ANGLE_RATE)
            pixel_gap = (angle_err + pos_err) * C.STRAIGHT_GAIN

        # ============================================================
        # CASE B: Right lane only -> left-curve incoming
        # ============================================================
        elif r_det and not l_det:
            target_x_for_right = C.BEV_WIDTH - self.pixel_offset
            angle_err = (r_ang - 90.0) * (1.0 - C.ANGLE_PIXEL_RATE)
            pos_err = (target_x_for_right - rx) * C.ANGLE_PIXEL_RATE
            pixel_gap = (angle_err + pos_err) * C.LEFT_CURVE_GAIN

            # Turtlebot original: if pixel_gap<0 means hard-clamp + early return
            # (prevents oscillation when robot is far past the curve point)
            if pixel_gap < 0:
                if pixel_gap < -C.MAX_REVERSE:
                    pixel_gap = -C.MAX_REVERSE
                pixel_gap = -pixel_gap                 # flip sign
                self.pre_pixel_gap = pixel_gap         # freeze D term
                self._apply_pd_and_publish(pixel_gap, speed, early=True)
                return self.before_linear_x, self.angular_z * self.before_linear_x * C.ANGULAR_LINEAR_RATE

        # ============================================================
        # CASE C: Left lane only -> right-curve incoming
        # ============================================================
        elif l_det and not r_det:
            target_x_for_left = self.pixel_offset
            angle_err = (l_ang - 90.0) * (1.0 - C.ANGLE_PIXEL_RATE)
            pos_err = (target_x_for_left - lx) * C.ANGLE_PIXEL_RATE
            pixel_gap = (angle_err + pos_err) * C.RIGHT_CURVE_GAIN

            if pixel_gap > 0:
                if pixel_gap > C.MAX_REVERSE:
                    pixel_gap = C.MAX_REVERSE
                pixel_gap = -pixel_gap                 # turtlebot quirk: flip
                self.pre_pixel_gap = -pixel_gap        # store the negative
                self._apply_pd_and_publish(pixel_gap, speed, early=True)
                return self.before_linear_x, self.angular_z * self.before_linear_x * C.ANGULAR_LINEAR_RATE

        # ============================================================
        # CASE D: No lane visible -> hold last D term, smooth toward zero
        # ============================================================
        else:
            self.pre_pixel_gap = 0.0

        # ------------------------------------------------------------------
        # Normal path: PD + LPF + speed coupling
        # ------------------------------------------------------------------
        self._update_angular(pixel_gap)
        self._clamp_angular()

        # Curvature-based speed reduction (turtlebot original)
        if abs(self.angular_z) > C.MIN_ANGLE:
            # Linear interpolation: more steering -> slower linear vel
            linear_x = (((max_lin_v - min_lin_v) / (C.MIN_ANGLE - C.MAX_ANGLE))
                        * (abs(self.angular_z) - C.MIN_ANGLE)) + max_lin_v

        # Slew rate limit on linear vel
        self._apply_slew(linear_x)

        # Final command
        cmd_linear = self.before_linear_x
        cmd_angular = self.angular_z * self.before_linear_x * C.ANGULAR_LINEAR_RATE

        # Save state
        self.pre_pixel_gap = pixel_gap

        return cmd_linear, cmd_angular

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _apply_pd_and_publish(self, pixel_gap, speed, early=False):
        """
        Used by curve-mode early-return path.
        Updates angular_z + applies LPF and clamps; keeps before_linear_x as-is.
        """
        self._update_angular(pixel_gap)
        self._clamp_angular()
        # No linear slew change on early return — keep before_linear_x stable

    def _update_angular(self, pixel_gap):
        p_term = pixel_gap * C.P_GAIN
        d_term = (pixel_gap - self.pre_pixel_gap) * C.D_GAIN
        raw = p_term + d_term
        # 1st order LPF — terminology matches turtlebot: angular_z = f2*new + f1*prev
        self.angular_z = C.F2 * raw + C.F1 * self.angular_z

    def _clamp_angular(self):
        if self.angular_z > C.MAX_ANGLE:
            self.angular_z = C.MAX_ANGLE
        elif self.angular_z < -C.MAX_ANGLE:
            self.angular_z = -C.MAX_ANGLE

    def _apply_slew(self, target_linear):
        if self.before_linear_x > target_linear + C.STRAIGHT_LINEAR_DECREASE_GAIN:
            self.before_linear_x -= C.STRAIGHT_LINEAR_DECREASE_GAIN
        elif self.before_linear_x < target_linear - C.STRAIGHT_LINEAR_INCREASE_GAIN:
            self.before_linear_x += C.STRAIGHT_LINEAR_INCREASE_GAIN
        else:
            self.before_linear_x = target_linear
