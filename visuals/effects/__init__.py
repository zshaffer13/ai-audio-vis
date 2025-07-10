# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 14:54:34 2025

@author: zshaf
"""

from .particles import particle_field
from .spirals import spiral_tunnel
from .waves import wave_rings
from .plasma import plasma_tunnel
from .grid import warping_grid
from .pulse_grid import pulse_grid
from .lava_lamp import lava_lamp
from .audio_ring import audio_bar_ring
from .strobe_tunnel import strobe_tunnel
from .wavy_lines import wavy_lines

EFFECTS = [
    wave_rings,
    spiral_tunnel,
    particle_field,
    plasma_tunnel,
    warping_grid,
    pulse_grid,
    lava_lamp,
    audio_bar_ring,
    strobe_tunnel,
    wavy_lines
]