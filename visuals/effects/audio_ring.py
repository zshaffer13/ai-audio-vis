# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 15:57:15 2025

@author: zshaf
"""

import cv2
import numpy as np
from visuals.utils.colors import get_cycle_color

def audio_bar_ring(frame, beats_elapsed, center, vol, drop_mode, beat_flags):
    h, w = frame.shape[:2]
    num_bars = 40
    radius = min(w, h) // 3
    for i in range(num_bars):
        angle = 2 * np.pi * i / num_bars
        bar_height = int(40 + 100 * np.abs(np.sin(beats_elapsed * 2 + i))) * vol
        x1 = int(center[0] + radius * np.cos(angle))
        y1 = int(center[1] + radius * np.sin(angle))
        x2 = int(center[0] + (radius + bar_height) * np.cos(angle))
        y2 = int(center[1] + (radius + bar_height) * np.sin(angle))
        color = get_cycle_color(beats_elapsed + i * 0.05, saturation=1.0, value=1.0, boost=drop_mode)
        cv2.line(frame, (x1, y1), (x2, y2), color, 2, cv2.LINE_AA)