# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 15:57:02 2025

@author: zshaf
"""

import cv2
import numpy as np
from visuals.utils.colors import get_cycle_color

def lava_lamp(frame, beats_elapsed, center, vol, drop_mode, beat_flags=None):
    h, w = frame.shape[:2]
    num_blobs = 10
    np.random.seed(42)  # For reproducibility of blob patterns

    for i in range(num_blobs):
        # Each blob moves on a circular path based on beats_elapsed
        angle = beats_elapsed * 0.2 + i  # BPM-based rotation
        cx = int(w / 2 + np.sin(angle + i) * w * 0.35)
        cy = int(h / 2 + np.cos(angle + i * 1.5) * h * 0.35)

        # Radius pulsates with BPM and volume
        base_radius = 30 + 10 * np.sin(beats_elapsed * 2 + i)
        r = int(base_radius * (0.8 + vol * 0.5))

        # Trippy color cycle
        color = get_cycle_color(
            beats_elapsed + i * 0.2,
            saturation=0.9,
            value=0.7 + 0.3 * np.sin(beats_elapsed + i),
            boost=drop_mode
        )

        # Draw semi-transparent blobs to allow overlap blending
        overlay = frame.copy()
        cv2.circle(overlay, (cx, cy), r, color, -1, cv2.LINE_AA)
        alpha = 0.6 if drop_mode else 0.4
        frame[:] = cv2.addWeighted(frame, 1.0, overlay, alpha, 0)