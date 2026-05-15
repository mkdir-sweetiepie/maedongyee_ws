#!/usr/bin/env python3
"""
Dashboard Node — Tkinter local GUI for 매동이 debugging / 시연.

Layout:
  ┌──────────────────────────────────────────┐
  │ 매동이 대시보드            [● connected]  │
  ├──────────────────────┬───────────────────┤
  │ STATE     : NORMAL   │ ◯ All ◉ Camera   │
  │ SIGN      : stop     │ ◯ BEV ◯ Sign     │
  │ LINEAR    : 0.180    │ ◯ Red BEV         │
  │ ANGULAR   : 0.053    │                   │
  │ OFFSET    : 180.0    │  ┌─────────────┐  │
  │ SLOW MODE : OFF      │  │             │  │
  │                      │  │   IMAGE     │  │
  │ LANE L: ✓ x=180.2    │  │             │  │
  │       a=89.2°        │  │             │  │
  │ LANE R: ✓ x=460.5    │  └─────────────┘  │
  │       a=90.5°        │                   │
  ├──────────────────────┴───────────────────┤
  │  [START]   [STOP]   [RESET]              │
  ├──────────────────────────────────────────┤
  │ LOG:                                     │
  │ 12:01:23  NEW SIGN: stop                 │
  │ 12:01:26  STATE: STOP_WAIT -> NORMAL     │
  └──────────────────────────────────────────┘

Run via:
  ros2 run aicar_ui dashboard_node
or as part of bringup launch.
"""

import threading
import time
from collections import deque
from datetime import datetime

import cv2
import numpy as np
import rclpy
import tkinter as tk
from tkinter import ttk
from cv_bridge import CvBridge
from PIL import Image as PILImage, ImageTk
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String


# --- Display sizing ---
DISP_W_BIG = 480       # single-image view width
DISP_H_BIG = 360
DISP_W_SMALL = 240     # 2x2 grid cell width
DISP_H_SMALL = 180

UI_REFRESH_MS = 80     # ~12 Hz UI redraw

# Color palette
COLOR_BG       = '#0f0f10'
COLOR_PANEL    = '#1a1a1c'
COLOR_TEXT     = '#e8e8e8'
COLOR_DIM      = '#8a8a8a'
COLOR_ACCENT   = '#FFD600'    # 매동이 노란선 컬러
COLOR_OK       = '#4caf50'
COLOR_WARN     = '#ff9800'
COLOR_ERR      = '#ff5252'


class DashboardNode(Node):
    def __init__(self):
        super().__init__('dashboard_node')
        self.get_logger().info('Dashboard Node (Tkinter local UI) started.')

        self.bridge = CvBridge()

        # Latest raw frames (cv2 ndarray)
        self._frame_cam = None
        self._frame_bev = None
        self._frame_sign = None
        self._frame_red = None
        self._frame_lock = threading.Lock()

        # Telemetry
        self.telemetry = {
            'state': 'UNKNOWN', 'sign': 'none',
            'linear': 0.0, 'angular': 0.0,
            'pixel_offset': 0.0,
            'l_det': 0, 'r_det': 0,
            'l_x': 0.0, 'r_x': 0.0,
            'l_ang': 0.0, 'r_ang': 0.0,
            'slow': 0,
        }
        self.tel_lock = threading.Lock()

        # Log buffer
        self.log_buffer = deque(maxlen=80)
        self._log('Dashboard started.')

        # Connection tracking
        self.last_telemetry_time = 0.0

        # Subscriptions
        self.create_subscription(Image, '/camera_node/image_raw', self._cam_cb, 5)
        self.create_subscription(Image, '/image_bev_binary', self._bev_cb, 5)
        self.create_subscription(Image, '/image_sign_debug', self._sign_dbg_cb, 5)
        self.create_subscription(Image, '/image_red_bev', self._red_cb, 5)
        self.create_subscription(String, '/drive_state', self._state_cb, 10)
        self.create_subscription(String, '/sign_detection', self._sign_cb, 10)
        self.create_subscription(String, '/telemetry', self._tel_cb, 10)

        # Publishers (control)
        self.pub_emergency = self.create_publisher(String, '/emergency_command', 10)
        self.pub_status = self.create_publisher(String, '/system_status', 10)

    # ==================================================================
    # ROS callbacks
    # ==================================================================
    def _cam_cb(self, msg):
        try:
            img = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
            with self._frame_lock:
                self._frame_cam = img
        except Exception:
            pass

    def _bev_cb(self, msg):
        try:
            img = self.bridge.imgmsg_to_cv2(msg, 'mono8')
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            with self._frame_lock:
                self._frame_bev = img
        except Exception:
            pass

    def _sign_dbg_cb(self, msg):
        try:
            img = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
            with self._frame_lock:
                self._frame_sign = img
        except Exception:
            pass

    def _red_cb(self, msg):
        try:
            img = self.bridge.imgmsg_to_cv2(msg, 'mono8')
            # Tint red for visibility
            colored = np.zeros((*img.shape, 3), dtype=np.uint8)
            colored[:, :, 2] = img   # B=0, G=0, R=mask
            with self._frame_lock:
                self._frame_red = colored
        except Exception:
            pass

    def _state_cb(self, msg):
        self._log(f'STATE -> {msg.data}')

    def _sign_cb(self, msg):
        self._log(f'SIGN: {msg.data}')

    def _tel_cb(self, msg):
        import json
        try:
            data = json.loads(msg.data)
            with self.tel_lock:
                self.telemetry.update(data)
            self.last_telemetry_time = time.time()
        except Exception as e:
            self.get_logger().debug(f'Telemetry parse fail: {e}')

    # ==================================================================
    # Helpers
    # ==================================================================
    def _log(self, text):
        ts = datetime.now().strftime('%H:%M:%S')
        self.log_buffer.append(f'{ts}  {text}')

    def send_command(self, cmd):
        """Send START / STOP / RESET to controller."""
        m = String()
        m.data = cmd
        self.pub_emergency.publish(m)
        if cmd == 'start':
            # Also send system_ready in case controller is waiting
            s = String()
            s.data = 'system_ready'
            self.pub_status.publish(s)
        self._log(f'[BTN] {cmd.upper()}')


# ======================================================================
# Tkinter App (runs in main thread, polls ROS data via after())
# ======================================================================
class DashboardApp:
    def __init__(self, node: DashboardNode):
        self.node = node

        self.root = tk.Tk()
        self.root.title('매동이 대시보드')
        self.root.configure(bg=COLOR_BG)
        self.root.geometry('1100x720')

        # PhotoImage refs (must keep refs to prevent GC)
        self._photo_main = None
        self._photo_grid = [None, None, None, None]

        # View mode
        self.view_mode = tk.StringVar(value='all')

        self._build_ui()
        self._tick()

    # ------------------------------------------------------------------
    def _build_ui(self):
        # Top bar
        topbar = tk.Frame(self.root, bg=COLOR_BG, height=40)
        topbar.pack(side='top', fill='x', padx=10, pady=(10, 0))
        tk.Label(topbar, text='매동이 (Maedong-i) 대시보드',
                 fg=COLOR_ACCENT, bg=COLOR_BG,
                 font=('TkDefaultFont', 16, 'bold')).pack(side='left')
        self.conn_label = tk.Label(topbar, text='● disconnected',
                                   fg=COLOR_ERR, bg=COLOR_BG,
                                   font=('TkFixedFont', 10))
        self.conn_label.pack(side='right')

        # Main split: left telemetry, right image
        main = tk.Frame(self.root, bg=COLOR_BG)
        main.pack(side='top', fill='both', expand=True, padx=10, pady=10)

        # --- LEFT: Telemetry panel ---
        left = tk.Frame(main, bg=COLOR_PANEL, width=340)
        left.pack(side='left', fill='y', padx=(0, 10))
        left.pack_propagate(False)

        tk.Label(left, text='STATUS', fg=COLOR_ACCENT, bg=COLOR_PANEL,
                 font=('TkFixedFont', 11, 'bold')).pack(anchor='w', padx=14, pady=(10, 4))

        self.telem_labels = {}
        for key, label in [
            ('state', 'STATE'),
            ('sign', 'SIGN'),
            ('linear', 'LINEAR'),
            ('angular', 'ANGULAR'),
            ('pixel_offset', 'OFFSET'),
            ('slow', 'SLOW MODE'),
        ]:
            row = tk.Frame(left, bg=COLOR_PANEL)
            row.pack(fill='x', padx=14, pady=2)
            tk.Label(row, text=f'{label:<11}', fg=COLOR_DIM, bg=COLOR_PANEL,
                     font=('TkFixedFont', 11), anchor='w').pack(side='left')
            val = tk.Label(row, text='—', fg=COLOR_TEXT, bg=COLOR_PANEL,
                           font=('TkFixedFont', 11, 'bold'), anchor='w')
            val.pack(side='left')
            self.telem_labels[key] = val

        # Lane info section
        tk.Label(left, text='LANES', fg=COLOR_ACCENT, bg=COLOR_PANEL,
                 font=('TkFixedFont', 11, 'bold')).pack(anchor='w', padx=14, pady=(14, 4))

        self.lane_left_label = tk.Label(left, text='L: —',
                                        fg=COLOR_TEXT, bg=COLOR_PANEL,
                                        font=('TkFixedFont', 11), anchor='w', justify='left')
        self.lane_left_label.pack(anchor='w', padx=14, pady=2)
        self.lane_right_label = tk.Label(left, text='R: —',
                                         fg=COLOR_TEXT, bg=COLOR_PANEL,
                                         font=('TkFixedFont', 11), anchor='w', justify='left')
        self.lane_right_label.pack(anchor='w', padx=14, pady=2)

        # View mode selector
        tk.Label(left, text='VIEW', fg=COLOR_ACCENT, bg=COLOR_PANEL,
                 font=('TkFixedFont', 11, 'bold')).pack(anchor='w', padx=14, pady=(14, 4))
        for value, text in [
            ('all', 'All (2×2)'),
            ('camera', 'Camera'),
            ('bev', 'BEV (Yellow)'),
            ('sign', 'Sign Debug'),
            ('red', 'Red BEV'),
        ]:
            rb = tk.Radiobutton(left, text=text, value=value,
                                variable=self.view_mode,
                                fg=COLOR_TEXT, bg=COLOR_PANEL,
                                selectcolor=COLOR_BG,
                                activebackground=COLOR_PANEL,
                                activeforeground=COLOR_ACCENT,
                                font=('TkFixedFont', 10),
                                anchor='w')
            rb.pack(fill='x', padx=20)

        # Buttons
        btn_frame = tk.Frame(left, bg=COLOR_PANEL)
        btn_frame.pack(side='bottom', fill='x', padx=10, pady=10)

        def mkbtn(parent, text, color, cmd):
            return tk.Button(parent, text=text,
                             bg=color, fg='#000',
                             activebackground=color,
                             font=('TkFixedFont', 11, 'bold'),
                             relief='flat', bd=0,
                             padx=10, pady=8,
                             command=cmd)

        mkbtn(btn_frame, 'START', COLOR_OK,
              lambda: self.node.send_command('start')).pack(fill='x', pady=2)
        mkbtn(btn_frame, 'STOP', COLOR_ERR,
              lambda: self.node.send_command('stop')).pack(fill='x', pady=2)
        mkbtn(btn_frame, 'RESET', COLOR_WARN,
              lambda: self.node.send_command('reset')).pack(fill='x', pady=2)

        # --- RIGHT: image canvas + log ---
        right = tk.Frame(main, bg=COLOR_BG)
        right.pack(side='left', fill='both', expand=True)

        self.image_frame = tk.Frame(right, bg='#000', height=DISP_H_BIG + 20)
        self.image_frame.pack(side='top', fill='both', expand=False)

        # Single label (used in single-view mode)
        self.img_main = tk.Label(self.image_frame, bg='#000')
        # Grid labels (used in all-view mode)
        self.img_grid = []
        self.grid_frame = tk.Frame(self.image_frame, bg='#000')
        self.grid_labels = []
        captions = ['Camera', 'BEV Yellow', 'Sign Debug', 'Red BEV']
        for i in range(4):
            cell = tk.Frame(self.grid_frame, bg='#000')
            cell.grid(row=i // 2, column=i % 2, padx=3, pady=3, sticky='nsew')
            lbl = tk.Label(cell, bg='#000')
            lbl.pack(side='top')
            cap = tk.Label(cell, text=captions[i], fg=COLOR_DIM, bg='#000',
                           font=('TkFixedFont', 9))
            cap.pack(side='top')
            self.grid_labels.append(lbl)

        # Log
        log_frame = tk.Frame(right, bg=COLOR_PANEL)
        log_frame.pack(side='top', fill='both', expand=True, pady=(10, 0))
        tk.Label(log_frame, text='LOG', fg=COLOR_ACCENT, bg=COLOR_PANEL,
                 font=('TkFixedFont', 11, 'bold')).pack(anchor='w', padx=10, pady=(6, 2))
        self.log_text = tk.Text(log_frame, bg='#0a0a0b', fg=COLOR_TEXT,
                                font=('TkFixedFont', 10),
                                bd=0, highlightthickness=0,
                                wrap='none', height=10)
        self.log_text.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        self.log_text.config(state='disabled')

    # ------------------------------------------------------------------
    def _to_photo(self, cv_img, w, h):
        if cv_img is None:
            # Black placeholder
            arr = np.zeros((h, w, 3), dtype=np.uint8)
            cv2.putText(arr, 'NO SIGNAL', (w // 2 - 60, h // 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (80, 80, 80), 1)
            rgb = arr
        else:
            resized = cv2.resize(cv_img, (w, h))
            rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        pil = PILImage.fromarray(rgb)
        return ImageTk.PhotoImage(pil)

    # ------------------------------------------------------------------
    def _update_images(self):
        mode = self.view_mode.get()

        with self.node._frame_lock:
            cam = self.node._frame_cam
            bev = self.node._frame_bev
            sign = self.node._frame_sign
            red = self.node._frame_red

        if mode == 'all':
            # Hide single, show grid
            self.img_main.pack_forget()
            self.grid_frame.pack(side='top')
            frames = [cam, bev, sign, red]
            for i, f in enumerate(frames):
                photo = self._to_photo(f, DISP_W_SMALL, DISP_H_SMALL)
                self._photo_grid[i] = photo  # keep ref
                self.grid_labels[i].configure(image=photo)
        else:
            # Hide grid, show single
            self.grid_frame.pack_forget()
            self.img_main.pack(side='top', padx=4, pady=4)
            frame_map = {'camera': cam, 'bev': bev, 'sign': sign, 'red': red}
            f = frame_map.get(mode)
            photo = self._to_photo(f, DISP_W_BIG, DISP_H_BIG)
            self._photo_main = photo
            self.img_main.configure(image=photo)

    # ------------------------------------------------------------------
    def _update_telemetry(self):
        with self.node.tel_lock:
            t = dict(self.node.telemetry)

        # State color cue
        state = t.get('state', 'UNKNOWN')
        color = COLOR_TEXT
        if state == 'NORMAL':
            color = COLOR_OK
        elif state in ('STOP_WAIT', 'TURNING', 'POST_TURN_STRAIGHT'):
            color = COLOR_WARN
        elif state == 'FINISHED':
            color = COLOR_ERR
        elif state == 'WAITING_FOR_SYSTEM':
            color = COLOR_DIM
        self.telem_labels['state'].configure(text=state, fg=color)
        self.telem_labels['sign'].configure(text=t.get('sign', 'none'))
        self.telem_labels['linear'].configure(text=f"{t.get('linear', 0.0):+.3f} m/s")
        self.telem_labels['angular'].configure(text=f"{t.get('angular', 0.0):+.3f} rad/s")
        self.telem_labels['pixel_offset'].configure(text=f"{t.get('pixel_offset', 0.0):.1f} px")
        slow = bool(t.get('slow', 0))
        self.telem_labels['slow'].configure(
            text='ON ' if slow else 'OFF',
            fg=COLOR_WARN if slow else COLOR_DIM)

        # Lane info
        l_det = '✓' if t.get('l_det', 0) else '✗'
        r_det = '✓' if t.get('r_det', 0) else '✗'
        self.lane_left_label.configure(
            text=f"L: {l_det}  x={t.get('l_x', 0):.1f}  ang={t.get('l_angle', t.get('l_ang', 0)):.1f}°",
            fg=COLOR_OK if t.get('l_det', 0) else COLOR_DIM)
        self.lane_right_label.configure(
            text=f"R: {r_det}  x={t.get('r_x', 0):.1f}  ang={t.get('r_angle', t.get('r_ang', 0)):.1f}°",
            fg=COLOR_OK if t.get('r_det', 0) else COLOR_DIM)

        # Connection
        age = time.time() - self.node.last_telemetry_time
        if self.node.last_telemetry_time > 0 and age < 1.0:
            self.conn_label.configure(text='● connected', fg=COLOR_OK)
        else:
            self.conn_label.configure(text='● disconnected', fg=COLOR_ERR)

    # ------------------------------------------------------------------
    def _update_log(self):
        # Rewrite log text widget (simple, ok at 80 lines)
        lines = list(self.node.log_buffer)
        text = '\n'.join(lines)
        self.log_text.config(state='normal')
        self.log_text.delete('1.0', 'end')
        self.log_text.insert('1.0', text)
        self.log_text.see('end')
        self.log_text.config(state='disabled')

    # ------------------------------------------------------------------
    def _tick(self):
        try:
            self._update_images()
            self._update_telemetry()
            self._update_log()
        except Exception as e:
            self.node.get_logger().warn(f'UI tick error: {e}')
        self.root.after(UI_REFRESH_MS, self._tick)

    # ------------------------------------------------------------------
    def run(self):
        self.root.protocol('WM_DELETE_WINDOW', self._on_close)
        self.root.mainloop()

    def _on_close(self):
        self.root.destroy()


# ======================================================================
def main(args=None):
    rclpy.init(args=args)
    node = DashboardNode()

    # ROS spin in a daemon thread; Tk runs on main thread
    spin_thread = threading.Thread(
        target=lambda: rclpy.spin(node), daemon=True)
    spin_thread.start()

    try:
        app = DashboardApp(node)
        app.run()
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()


if __name__ == '__main__':
    main()
