# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 14:52:17 2025

@author: zshaf
"""

import cv2
import numpy as np
from visuals.utils.colors import get_cycle_color

active_rings = []
last_ring_beat = -10  # prevent spamming

def wave_rings(frame, beats_elapsed, center, vol, drop_mode, beat_flags):
    global active_rings, last_ring_beat

    # Only add a ring if midrange beat fires and 2+ beats have passed since last ring
    if beat_flags.get("midrange", False) and (beats_elapsed - last_ring_beat >= 2):
        active_rings.append(beats_elapsed)
        last_ring_beat = beats_elapsed

    # Keep only the last 3 rings
    active_rings = [b for b in active_rings if beats_elapsed - b < 4][-3:]

    for birth_beat in active_rings:
        age = beats_elapsed - birth_beat
        radius = int(age * 100)
        intensity = max(0.3, 1 - age * 0.25)
        boost = drop_mode or vol > 0.6
        color = get_cycle_color(beats_elapsed + birth_beat * 0.3, saturation=vol * intensity, value=0.7 + 0.3 * vol, boost=boost)
        cv2.circle(frame, center, radius, color, 2, cv2.LINE_AA)

