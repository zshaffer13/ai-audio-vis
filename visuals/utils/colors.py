# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 15:44:57 2025

@author: zshaf
"""

import numpy as np
import cv2

def get_cycle_color(t, saturation=1.0, value=1.0, boost=False):
    """
    Returns a cycling BGR color based on time t.
    boost: If True, exaggerate saturation and value for high energy pop.
    """
    hue = (t * 20) % 360

    # Clamp min saturation and brightness
    sat = max(0.7, min(saturation, 1.0))
    val = max(0.8, min(value, 1.0))

    # Boost for more pop
    if boost:
        sat = min(1.0, sat * 1.2)
        val = min(1.0, val * 1.3)

    # Convert HSV to BGR
    hsv = np.uint8([[[hue / 2, int(sat * 255), int(val * 255)]]])
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)[0][0]
    return tuple(int(c) for c in bgr)