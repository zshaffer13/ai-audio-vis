# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 14:52:52 2025

@author: zshaf
"""

import cv2
import numpy as np
from visuals.utils.colors import get_cycle_color

def spiral_tunnel(frame, beats_elapsed, center, vol, drop_mode, beat_flags):
    cx, cy = center
    num_arms = 5
    points_per_arm = 40
    beats_per_rotation = 8  # 1 full spin every 4 beats
    angular_velocity = (2 * np.pi) / beats_per_rotation

    for arm in range(num_arms):
        for i in range(points_per_arm):
            angle = beats_elapsed * angular_velocity + i * 0.3 + arm * (2 * np.pi / num_arms)
            radius = 20 + i * 8 + int(40 * vol)
            x = int(cx + radius * np.cos(angle))
            y = int(cy + radius * np.sin(angle))

            boost = drop_mode or beat_flags.get("midrange", False)
            color = get_cycle_color(beats_elapsed + i * 0.1, saturation=vol, value=1.0, boost=boost)
            cv2.circle(frame, (x, y), 3, color, -1, cv2.LINE_AA)

