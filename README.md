# 매동이 (Maedong-i) — Turtlebot lineTracing Port

광운대 임베디드 AI 시스템 최적화 자율주행 차량 프로젝트.
2024 TurtleBot3 프로젝트의 `lineTracing` 알고리즘을 라즈베리파이 5 + ROS 2 Jazzy 환경에 포팅한 버전.

## 핵심 아이디어

터틀봇 코드(`robit_master/src/robit_driving.cpp`)의 검증된 `lineTracing` 함수를 그대로 가져옴:

1. **각도+위치 가중합 에러** — 픽셀 1개 outlier에 안 흔들림
2. **pixel_offset 자가학습** — 양쪽 차선 보일 때마다 트랙 폭(픽셀) 학습 → 한쪽만 보일 때 활용
3. **angular_z LPF** — `f1=0.3 * prev + f2=0.7 * new`
4. **곡률 기반 속도 감속** — 핸들 많이 꺾으면 자동으로 느려짐
5. **슬루율 제한** — 급가속/급감속 방지
6. **좌커브/우커브/직진 게인 분리**
7. **MAX_REVERSE 클램프** — 곡선 모드 early-return으로 진동 억제

## 패키지 구조

```
maedongyee_ws/src/
├── aicar_msgs/              # LaneInfo 커스텀 메시지
│   ├── msg/LaneInfo.msg
│   ├── CMakeLists.txt
│   └── package.xml
├── aicar_vision/            # BEV + polyfit 라인 검출
│   ├── aicar_vision/
│   │   ├── lane_detector_node.py    ← 좌/우 polyfit → LaneInfo 발행
│   │   └── sign_detector_node.py    ← (기존 유지)
│   ├── setup.py
│   └── package.xml
├── aicar_controller/        # ⭐ 핵심: 터틀봇 lineTracing 포팅
│   ├── aicar_controller/
│   │   ├── constants.py             ← 모든 게인값 (튜닝 포인트)
│   │   ├── line_tracer.py           ← LineTracer 클래스
│   │   └── driving_controller_node.py ← 메인 노드 (상태머신 통합)
│   ├── setup.py
│   └── package.xml
├── aicar_driver/            # (기존 differential_drive_node 그대로)
└── aicar_bringup/
    └── launch/aicar_drive.launch.py
```

## 데이터 흐름

```
camera → /camera/image_raw
            ├→ lane_detector_node    → /image_bev_binary
            │                        → /image_red_bev
            │                        → /lane_info (LaneInfo) ⭐
            └→ sign_detector_node    → /sign_detection
                                     → /system_status

/lane_info ───┐
/image_red_bev├→ driving_controller_node → /cmd_vel
/sign_detection│                              │
/system_status ┘                              ↓
                                  differential_drive_node → 모터
```

## 빌드 & 실행

```bash
cd ~/ros2_ws
# (메시지 패키지부터 빌드)
colcon build --packages-select aicar_msgs
source install/setup.bash
colcon build --packages-select aicar_vision aicar_controller aicar_bringup
source install/setup.bash

# 실행
ros2 launch aicar_bringup aicar_drive.launch.py vehicle_speed:=0.18
# 시스템 핸드셰이크 건너뛰고 즉시 출발:
ros2 launch aicar_bringup aicar_drive.launch.py skip_handshake:=true
```

## 튜닝 가이드

모든 게인은 `aicar_controller/aicar_controller/constants.py`에 모음.

**1단계: 직선 (양쪽 차선 보일 때)**
- `STRAIGHT_GAIN` (0.1 시작) — 너무 크면 진동, 너무 작으면 응답 느림
- `STRAIGHT_ANGLE_RATE` (0.9) — 각도 신호 비중. 직진성 좋으려면 ↑

**2단계: 곡선 (한쪽 차선만 보일 때)**
- `LEFT_CURVE_GAIN`, `RIGHT_CURVE_GAIN` — 좌/우 비대칭 보정 가능
- `ANGLE_PIXEL_RATE` (0.7) — 곡선에선 위치 신호도 무시 못 함

**3단계: PD**
- `P_GAIN=1.0`, `D_GAIN=6.0` — 터틀봇 검증값. D가 P의 6배인 게 핵심
- `F1=0.3` — LPF 강도. 출력 노이즈 심하면 ↑ (단, 응답성 ↓)

**4단계: 속도**
- `MAX_LINEAR_RATIO=0.7`, `MIN_LINEAR_RATIO=0.3`
- `ANGULAR_LINEAR_RATE=3.0` — 조향이 너무 약하면 ↑

**5단계: 회전 (표지판 우/좌회전)**
- `TURN_DURATION_SEC` — **메모리에 1.9s가 ~218°였다고 기록됨**. 1.45s로 시작해서 실측 보정.
- `TURN_ANGULAR_VEL=2.0`

**6단계: 정지/감속**
- `STOP_SIGN_WAIT_SEC=3.5` (평가표: 1-3s = -10, <1s = -20 → 3.5s 안전)
- `SLOW_SPEED_RATIO=0.2` (평가표: 20% 모터 출력)

## 평가표 미션 매핑

| 미션 | 처리 위치 | 상태 |
|---|---|---|
| 1. 차선 추종 | `LineTracer.compute` | ✅ |
| 2. 방향 표지판 (left/right/straight) | `sign_cb` → STATE_TURNING | ✅ |
| 3. Stop 사인 | `sign_cb` → STATE_STOP_WAIT(3.5s) | ✅ |
| 4. 신호등 (적색=정지+우회전, 녹색=정차 없이 우회전) | `sign_cb` traffic_light / traffic_light_green | ✅ |
| 5. 경적 (1초) | `_beep_buzzer` (BUZZER_DURATION_SEC=1.0) | ✅ |
| 6. 감속 (20%) | slow_mode_until 윈도우 | ✅ |
| 7. 통과 시간 | (vehicle_speed로 조절) | ✅ |
| 8. 출발 위치 정차 | red_cb → STATE_FINISHED | ✅ |

## 기존 매동이 코드 대비 변경점

- ❌ 제거: `pid_controller_node.py`의 단일 row 기반 PID
- ❌ 제거: `half_track_width_pixels=250` 하드코딩
- ✅ 추가: 각도 정보를 위한 `LaneInfo` 메시지 + polyfit
- ✅ 추가: angular_z LPF, 슬루율 제한, 곡률 감속
- ✅ 추가: pixel_offset 자가학습 (트랙 폭 변동에 자동 적응)
- ✅ 수정: 빨간선 lockout 시간 → 오작동 방지
- ✅ 수정: 회전 시간 1.9s → 1.45s (메모리상 ~218° 문제 해결)
