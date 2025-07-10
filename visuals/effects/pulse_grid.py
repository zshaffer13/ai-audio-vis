# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 15:56:43 2025

@author: zshaf
"""

import cv2
import numpy as np
from visuals.utils.colors import get_cycle_color

def pulse_grid(frame, beats_elapsed, center, vol, drop_mode, beat_flags=None):
    h, w = frame.shape[:2]
    rows, cols = 10, 14
    tile_w, tile_h = w // cols, h // rows

    # Use beats_elapsed for rhythmic pulse control
    global_phase = np.sin(2 * np.pi * beats_elapsed)  # oscillates between -1 and 1 every beat

    for i in range(rows):
        for j in range(cols):
            # Offset each tile's phase slightly for a flowing effect
            local_phase = global_phase + np.sin((i + j) * 0.5 + beats_elapsed * 0.3)
            brightness = 0.5 + 0.5 * local_phase  # range from 0 to 1
            brightness = np.clip(brightness * vol * 1.2, 0, 1)

            boost = drop_mode or brightness > 0.8
            color = get_cycle_color(
                beats_elapsed + i * 0.1 + j * 0.1,
                saturation=0.8,
                value=brightness,
                boost=boost
            )

            x, y = j * tile_w, i * tile_h
            cv2.rectangle(frame, (x, y), (x + tile_w, y + tile_h), color, -1, cv2.LINE_AA)
