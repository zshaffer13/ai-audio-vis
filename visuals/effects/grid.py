# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 15:03:36 2025

@author: zshaf
"""

import cv2
import numpy as np
from visuals.utils.colors import get_cycle_color

def warping_grid(frame, beats_elapsed, center, vol, drop_mode, beat_flags):
    h, w = frame.shape[:2]
    spacing = 40
    wave_speed = beats_elapsed * (1.5 if drop_mode else 0.7)

    for y in range(0, h, spacing):
        for x in range(0, w, spacing):
            dx = int(15 * np.sin(wave_speed + y * 0.05) * vol)
            dy = int(15 * np.cos(wave_speed + x * 0.05) * vol)

            pt1 = (int(x), int(y))
            pt2 = (int(x + dx), int(y + dy))

            color = get_cycle_color(beats_elapsed + x * 0.01 + y * 0.01,
                                    saturation=0.8 + 0.2 * vol,
                                    value=0.9,
                                    boost=drop_mode)
            cv2.line(frame, pt1, pt2, color, 1, cv2.LINE_AA)

    # Drop mode overlay lines
    if drop_mode:
        for i in range(0, h, spacing):
            offset = int(10 * np.sin(beats_elapsed + i * 0.1) * vol)
            pt1 = (0, int(i + offset))
            pt2 = (w, int(i - offset))
            color = get_cycle_color(beats_elapsed + i * 0.05, boost=True)
            cv2.line(frame, pt1, pt2, color, 1, cv2.LINE_AA)

