# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 15:57:32 2025

@author: zshaf
"""

# wavy_lines.py

import cv2
import numpy as np
from visuals.utils.colors import get_cycle_color

def wavy_lines(frame, beats_elapsed, center, vol, drop_mode, beat_flags=None):
    h, w = frame.shape[:2]
    spacing = 20
    frequency = 2  # number of waves per width
    wave_speed = beats_elapsed * np.pi  # BPM-based movement
    amplitude = 10 + int(20 * vol)  # larger wave size scaled by volume

    for y in range(0, h, spacing):
        pts = []
        for x in range(0, w, 10):
            offset = int(amplitude * np.sin(frequency * x * 2 * np.pi / w + wave_speed))
            pts.append((x, y + offset))
        color = get_cycle_color(beats_elapsed + y * 0.01, saturation=0.8, value=0.9, boost=drop_mode)
        for i in range(1, len(pts)):
            cv2.line(frame, pts[i - 1], pts[i], color, 2, cv2.LINE_AA)
