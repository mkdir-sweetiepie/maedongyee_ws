"""
Driving constants (ported from 2024_turtlebot robit_driving.hpp mode3)
NOTE: These are starting values. Tune on the real robot.

Coordinate convention (BEV, 640x480):
- robot_center_px = 320 (BEV image center)
- left_x in [0, 320), right_x in [320, 640)
- pixel_offset: learned half-track-width in pixels
- angle: 90 deg = vertical line (lane parallel to driving direction)

Turtlebot used 320x240 image (mid=160). We use 640x480 BEV (mid=320),
so position-derived numbers are scaled x2. Gains kept the same as
starting points; tune as needed.
"""

# --- LineTracing core gains ---
STRAIGHT_GAIN     = 0.1     # both lanes visible
LEFT_CURVE_GAIN   = 0.047   # right lane only (left curve incoming)
RIGHT_CURVE_GAIN  = 0.05    # left lane only (right curve incoming)

P_GAIN = 1.0
D_GAIN = 6.0

ANGLE_PIXEL_RATE = 0.7      # angle vs position weight on curve mode (turtlebot value)
STRAIGHT_ANGLE_RATE = 0.9   # on straight (both lanes), angle weighted higher

# --- Angular limits ---
MIN_ANGLE = 0.1
MAX_ANGLE = 3.6
MAX_REVERSE = 2.0           # clamp on curve-mode pixel_gap

# --- Output mixing ---
F1 = 0.3                    # previous angular weight (LPF)
F2 = 1.0 - F1               # new angular weight

# --- Speed coupling ---
ANGULAR_LINEAR_RATE = 3.0   # angular_z = raw * before_linear * RATE

# --- Slew rate (speed change per cycle) ---
STRAIGHT_LINEAR_INCREASE_GAIN = 0.1
STRAIGHT_LINEAR_DECREASE_GAIN = 0.08

# --- Speed profile (relative to base_speed) ---
MIN_LINEAR_RATIO = 0.3      # in heavy turn
MAX_LINEAR_RATIO = 0.7      # near straight

# --- BEV image dims ---
BEV_WIDTH = 640
BEV_HEIGHT = 480
ROBOT_CENTER_PX = BEV_WIDTH / 2.0   # 320.0

# --- Default learned pixel_offset (half track width) ---
# Track is 20cm wide. BEV calibration dependent; tune for your setup.
DEFAULT_PIXEL_OFFSET = 180

# --- State machine timings ---
STOP_SIGN_WAIT_SEC = 3.5    # mission: 1-3s = -10, <1s = -20, so target ~3.5
TRAFFIC_RED_WAIT_SEC = 3.0  # red light: stop then right turn
SLOW_MODE_DURATION_SEC = 6.0   # 20% speed window after slow sign

# --- Turn (left/right_turn sign) ---
TURN_ANGULAR_VEL = 2.0      # rad/s during in-place turn
TURN_DURATION_SEC = 1.45    # tune for ~90 deg (1.9 was ~218 deg per memory)

# --- Post turn straight ---
POST_TURN_STRAIGHT_SEC = 1.0

# --- Slow sign motor scale ---
SLOW_SPEED_RATIO = 0.2      # mission: 20% motor output

# --- Buzzer ---
BUZZER_PIN = 12
BUZZER_FREQ = 1500
BUZZER_DURATION_SEC = 1.0

# --- Finish line detection ---
RED_DETECT_LOCKOUT_SEC = 8.0      # ignore red line during first N sec from start
RED_DETECT_DENSITY = 0.40         # white pixel ratio threshold in detection zone
