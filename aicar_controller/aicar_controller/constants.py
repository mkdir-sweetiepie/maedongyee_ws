"""
Driving constants (ported from 2024_turtlebot robit_driving.hpp mode3)
"""

# --- LineTracing core gains ---
STRAIGHT_GAIN     = 0.1
LEFT_CURVE_GAIN   = 0.047
RIGHT_CURVE_GAIN  = 0.05

P_GAIN = 1.0
D_GAIN = 6.0

ANGLE_PIXEL_RATE = 0.7
STRAIGHT_ANGLE_RATE = 0.9

# --- Angular limits ---
MIN_ANGLE = 0.1
MAX_ANGLE = 3.6
MAX_REVERSE = 2.0

# --- Output mixing ---
F1 = 0.3
F2 = 1.0 - F1

# --- Speed coupling ---
ANGULAR_LINEAR_RATE = 3.0

# --- Slew rate ---
STRAIGHT_LINEAR_INCREASE_GAIN = 0.1
STRAIGHT_LINEAR_DECREASE_GAIN = 0.08

# --- Speed profile ---
MIN_LINEAR_RATIO = 0.3
MAX_LINEAR_RATIO = 0.7

# --- BEV image dims ---
BEV_WIDTH = 640
BEV_HEIGHT = 480
ROBOT_CENTER_PX = BEV_WIDTH / 2.0

# --- Default learned pixel_offset ---
DEFAULT_PIXEL_OFFSET = 180

# --- State machine timings ---
STOP_SIGN_WAIT_SEC = 3.5
TRAFFIC_RED_WAIT_SEC = 3.0
SLOW_MODE_DURATION_SEC = 6.0

# --- Turn (split / smooth) ---
# 한 번에 90도 휙 도는 대신, "30도 회전 + 약한 직진" 을 3번 반복.
# 사람 운전 느낌으로 부드러운 코너링.
TURN_ANGULAR_VEL = 2.0          # rad/s (회전 단계의 각속도)
TURN_STEP_DURATION_SEC = 0.70   # 한 번에 회전 시간 (2.0 × 0.30 ≈ 34°)
TURN_PAUSE_DURATION_SEC = 0.3  # 회전 사이 약한 직진 시간
TURN_PAUSE_LINEAR = 0.5        # 회전 사이 직진 속도 (작게)
TURN_STEPS = 3                  # 회전 분할 횟수 (3번 = 약 90도)

# Legacy: 통회전용 (사용 안 함, 호환성 유지)
TURN_DURATION_SEC = 1.0

# --- Post turn straight ---
POST_TURN_STRAIGHT_SEC = 1.0

SLOW_SPEED_RATIO = 0.2

# --- Buzzer ---
BUZZER_PIN = 12
BUZZER_FREQ = 1500
BUZZER_DURATION_SEC = 1.0

# --- Finish line detection ---
RED_DETECT_LOCKOUT_SEC = 8.0
RED_DETECT_DENSITY = 0.40

# --- Auto corner detection (both lanes lost = corner) ---
CORNER_BOTH_LOST_FRAMES = 5
CORNER_PRE_TURN_DELAY_SEC = 0.5
CORNER_COOLDOWN_SEC = 4.0