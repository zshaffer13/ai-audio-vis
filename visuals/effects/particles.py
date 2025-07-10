# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 14:53:05 2025

@author: zshaf
"""

import cv2
import numpy as np
from visuals.utils.colors import get_cycle_color

def particle_field(frame, beats_elapsed, center, vol, drop_mode, beat_flags):
    h, w = frame.shape[:2]
    cx, cy = center
    num_rings = 4
    particles_per_ring = 50 if not drop_mode else 70
    base_radius = min(w, h) // 6
    beats_per_loop = 16
    angle_speed = (2 * np.pi) / beats_per_loop
    drift_amplitude = 30 + vol * 20  # How far they move in/out

    for r in range(num_rings):
        ring_base = base_radius + r * 40
        drift = np.sin(beats_elapsed * 2 + r) * drift_amplitude
        ring_radius = ring_base + drift
        direction = 1 if r % 2 == 0 else -1  # Alternate rotation

        for i in range(particles_per_ring):
            angle_offset = i * (2 * np.pi / particles_per_ring)
            angle = direction * beats_elapsed * angle_speed + angle_offset

            x = int(cx + ring_radius * np.cos(angle))
            y = int(cy + ring_radius * np.sin(angle))

            size = 2 if not drop_mode else 3
            boost = drop_mode or beat_flags.get("presence", False)
            color = get_cycle_color(beats_elapsed + i * 0.01 + r, saturation=vol, value=0.8, boost=boost)
            cv2.circle(frame, (x, y), size, color, -1, cv2.LINE_AA)


