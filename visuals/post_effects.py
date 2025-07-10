# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 23:24:30 2025

@author: zshaf
"""

import cv2
import numpy as np


def kaleidoscope_warp(frame, intensity):
    h, w = frame.shape[:2]
    num_segments = 8
    angle_step = 360 / num_segments
    animated_angle = (intensity * 60) % 360

    # Create a larger tile for transformation
    tile_size = max(h, w) * 2
    tile = np.zeros((tile_size, tile_size, 3), dtype=np.uint8)

    # Paste frame into center of the tile
    offset_x = (tile_size - w) // 2
    offset_y = (tile_size - h) // 2
    tile[offset_y:offset_y + h, offset_x:offset_x + w] = frame

    tile_center = (tile_size // 2, tile_size // 2)
    result = np.zeros_like(tile)

    for i in range(num_segments):
        angle = angle_step * i + animated_angle
        M = cv2.getRotationMatrix2D(tile_center, angle, 1.0)
        rotated = cv2.warpAffine(tile, M, (tile_size, tile_size))

        if i % 2 == 0:
            rotated = cv2.flip(rotated, 1)

        mask = np.zeros((tile_size, tile_size), dtype=np.uint8)
        cv2.ellipse(mask, tile_center, (tile_size, tile_size), 0, angle_step * i, angle_step * (i + 1), 255, -1)

        seg = cv2.bitwise_and(rotated, rotated, mask=mask)
        result = cv2.add(result, seg)

    # Crop final result back to original frame size
    crop_x = (tile_size - w) // 2
    crop_y = (tile_size - h) // 2
    np.copyto(frame, result[crop_y:crop_y + h, crop_x:crop_x + w])



def pixel_flow_distort(frame, intensity):
    h, w = frame.shape[:2]
    distort = np.sin(np.linspace(0, np.pi * 4, h)) * 20 * intensity
    for y in range(h):
        shift = int(np.clip(distort[y], -w//4, w//4))
        frame[y] = np.roll(frame[y], shift, axis=0)


def glitch_flash(frame, intensity):
    if np.random.rand() < 0.7 * intensity:
        shift = int(np.random.uniform(-20, 20))
        b, g, r = cv2.split(frame)
        g = np.roll(g, shift, axis=1)
        r = np.roll(r, -shift, axis=0)
        merged = cv2.merge([b, g, r])
        cv2.addWeighted(merged, 0.7, frame, 0.3, 0, dst=frame)


def color_trail_shift(frame, intensity):
    blur = cv2.GaussianBlur(frame, (0, 0), sigmaX=6 * intensity)
    cv2.addWeighted(blur, 0.5, frame, 0.5, 0, dst=frame)


POST_EFFECTS = [
    #kaleidoscope_warp,
    pixel_flow_distort,
    glitch_flash,
    color_trail_shift,
]

