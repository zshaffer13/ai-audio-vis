import cv2
import numpy as np
import math

def strobe_tunnel(frame, beats_elapsed, center, vol, drop_mode, beat_flags=None):
    h, w = frame.shape[:2]
    cx, cy = center
    num_rings = 30
    max_radius = int(np.hypot(cx, cy))

    spacing = 60
    # Phase determines forward motion, synced to beats
    phase = (beats_elapsed * spacing) % spacing

    # Rotation angle shifts gradually with beat
    rotation_speed = 0.4 if drop_mode else 0.1  # radians per beat
    angle_offset = beats_elapsed * rotation_speed

    # Slight warping on spokes during drop
    warp_amplitude = 0.08 if drop_mode else 0.02

    # BPM-synced hue shifting
    hue_base = int((beats_elapsed * (80 if drop_mode else 8)) % 180)
    brightness = int(min(255, max(60, vol * 800)))

    for i in range(num_rings):
        radius = int((i * spacing - phase))
        if radius <= 0 or radius >= max_radius:
            continue

        hue = (hue_base + i * 3) % 180
        color_bgr = cv2.cvtColor(np.uint8([[[hue, 255, brightness]]]), cv2.COLOR_HSV2BGR)[0][0]
        cv2.circle(frame, center, radius, tuple(int(c) for c in color_bgr), 2, lineType=cv2.LINE_AA)

    # Spokes for drops only
    if drop_mode:
        num_spokes = 20
        for i in range(num_spokes):
            angle = 2 * np.pi * i / num_spokes + angle_offset
            warped_radius = max_radius * (1 + warp_amplitude * math.sin(i + beats_elapsed * 2))
            x = int(cx + np.cos(angle) * warped_radius)
            y = int(cy + np.sin(angle) * warped_radius)

            hue = (hue_base + i * 5) % 180
            spoke_color = cv2.cvtColor(np.uint8([[[hue, 255, brightness]]]), cv2.COLOR_HSV2BGR)[0][0]
            cv2.line(frame, center, (x, y), tuple(int(c) for c in spoke_color), 1, cv2.LINE_AA)
