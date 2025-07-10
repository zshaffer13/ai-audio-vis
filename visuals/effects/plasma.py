# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 15:03:13 2025

@author: zshaf
"""

import cv2
import numpy as np
from visuals.utils.colors import get_cycle_color

def plasma_tunnel(frame, beats_elapsed, center, vol, drop_mode, beat_flags):
    h, w = frame.shape[:2]
    cx, cy = center
    y, x = np.indices((h, w))
    x = x - cx
    y = y - cy

    # Convert to polar coordinates
    radius = np.sqrt(x**2 + y**2)
    angle = np.arctan2(y, x)

    # Time-based animation synced to BPM
    swirl = angle + np.sin(radius * 0.02 - beats_elapsed * 0.5)

    # Plasma wave pattern with radial stretching
    waves = np.sin(radius * 0.04 - beats_elapsed * 2 + swirl * 2)

    # Normalize and scale to color value
    norm = ((waves + 1) / 2)
    hue_shift = (beats_elapsed * 10) % 360
    hsv = np.zeros((h, w, 3), dtype=np.uint8)
    hsv[..., 0] = ((norm * 180 + hue_shift) % 180).astype(np.uint8)
    hsv[..., 1] = np.clip(150 + vol * 100, 0, 255).astype(np.uint8)
    hsv[..., 2] = np.clip(100 + norm * 155 * vol, 0, 255).astype(np.uint8)

    color = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    frame[:] = color
