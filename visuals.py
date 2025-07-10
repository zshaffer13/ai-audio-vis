# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 12:19:49 2025

@author: zshaf
"""

import cv2
import numpy as np
import time

def get_nearest_index(timestamps, current_time):
    idx = np.searchsorted(timestamps, current_time) - 1
    return np.clip(idx, 0, len(timestamps) - 1)

def kaleidoscope_effect(img, slices=6):
    h, w = img.shape[:2]
    center = (w // 2, h // 2)
    output = np.zeros_like(img)

    angle = 360 / slices
    for i in range(slices):
        M = cv2.getRotationMatrix2D(center, angle * i, 1)
        rotated = cv2.warpAffine(img, M, (w, h))
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.ellipse(mask, center, (w//2, h//2), angle*i, 0, angle, 255, -1)
        for c in range(3):
            output[:, :, c] = np.where(mask > 0, rotated[:, :, c], output[:, :, c])
    return output

def alpha_blend(base, overlay, alpha=0.5):
    return cv2.addWeighted(base, 1 - alpha, overlay, alpha, 0)

def shader_trails(prev_frame, decay=0.92):
    # Fakes a trail by fading previous frame slightly
    return (prev_frame.astype(np.float32) * decay).astype(np.uint8)

def run_visualizer(features, duration):
    width, height = 800, 600
    win_name = "AI DJ Visuals"
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

    beat_times = features["beat_times"]
    rms = features["rms"]
    rms_times = features["rms_times"]
    mel = features["mel"]
    mel_times = features["mel_times"]

    beat_index = 0
    start_time = time.time()
    prev_frame = np.zeros((height, width, 3), dtype=np.uint8)

    while True:
        elapsed = time.time() - start_time
        if elapsed > duration:
            break

        # Get current audio features
        rms_idx = get_nearest_index(rms_times, elapsed)
        mel_idx = get_nearest_index(mel_times, elapsed)

        vol = rms[rms_idx]
        mel_band = mel[:, mel_idx]
        mel_norm = (mel_band - mel_band.min()) / (mel_band.ptp() + 1e-6)

        # === Base canvas (trails from last frame)
        frame = shader_trails(prev_frame)

        # === BEAT CIRCLE LAYER ===
        pulse = beat_index < len(beat_times) and elapsed >= beat_times[beat_index]
        if pulse:
            beat_index += 1
        beat_radius = 40 + int(60 * vol)
        beat_color = (255, 50, 200)
        layer1 = np.zeros_like(frame)
        cv2.circle(layer1, (width // 2, height // 2), beat_radius, beat_color, -1)
        frame = alpha_blend(frame, layer1, 0.4)

        # === MEL FREQUENCY RADIAL LINES ===
        layer2 = np.zeros_like(frame)
        num_lines = len(mel_norm)
        for i, val in enumerate(mel_norm):
            angle = 2 * np.pi * i / num_lines
            length = int(100 + val * 180)
            x1 = int(width//2 + np.cos(angle) * 60)
            y1 = int(height//2 + np.sin(angle) * 60)
            x2 = int(width//2 + np.cos(angle) * (60 + length))
            y2 = int(height//2 + np.sin(angle) * (60 + length))
            color = (int(255 * val), 255 - int(255 * val), 180)
            cv2.line(layer2, (x1, y1), (x2, y2), color, 2)
        frame = alpha_blend(frame, layer2, 0.5)

        # === KALEIDOSCOPE EFFECT ===
        kaleido = kaleidoscope_effect(frame)
        frame = alpha_blend(frame, kaleido, 0.3)

        # === Save previous frame for trails ===
        prev_frame = frame.copy()

        # === Display ===
        cv2.imshow(win_name, frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()