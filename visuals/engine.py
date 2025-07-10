import cv2
import numpy as np
import time
import random
from visuals.effects import EFFECTS
from visuals.effects import (
    lava_lamp,
    wavy_lines,
    spiral_tunnel,
    wave_rings,
    particle_field,
    pulse_grid,
    audio_bar_ring,
    strobe_tunnel,
    warping_grid,
    plasma_tunnel
)
from visuals.post_effects import POST_EFFECTS
from visuals.audio.realtime_beats import RealTimeBeatDetector

def blend_effects(effects, t, center, vol, drop_mode, beat_flags, size, mode='add'):
    layers = []
    for effect in effects:
        layer = np.zeros(size, dtype=np.uint8)
        effect(layer, t, center, vol, drop_mode, beat_flags)
        layers.append(layer)

    result = layers[0]
    for layer in layers[1:]:
        if mode == 'add':
            result = cv2.addWeighted(result, 0.6, layer, 0.6, 0)
        elif mode == 'multiply':
            result = cv2.multiply(result, layer)
        elif mode == 'lighten':
            result = np.maximum(result, layer)
        elif mode == 'screen':
            result = 255 - ((255 - result) * (255 - layer) // 255)
    return result

EFFECT_NAMES = {
    wave_rings: "Wave Rings",
    spiral_tunnel: "Spiral Tunnel",
    particle_field: "Particle Field",
    plasma_tunnel: "Plasma Tunnel",
    warping_grid: "Warping Grid",
    pulse_grid: "Pulse Grid",
    lava_lamp: "Lava Lamp",
    audio_bar_ring: "Audio Bar Ring",
    strobe_tunnel: "Strobe Tunnel",
    wavy_lines: "Wavy Lines",
}

def run_visualizer(audio_path, duration):
    width, height = 800, 600
    win_name = "AI DJ Visuals"
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    center = (width // 2, height // 2)

    beat_detector = RealTimeBeatDetector(audio_path)
    beat_detector.start()

    start_time = time.time()
    current_effects = [EFFECTS[0]]
    last_effect_switch = 0
    active_post_effect = None
    previous_effects = []

    while True:
        elapsed = time.time() - start_time
        if elapsed > duration:
            break

        beat_flags = beat_detector.beat_flags
        sub_bass_beat = beat_flags.get("sub_bass", False)

        vol = 0.8 if sub_bass_beat else 0.4  # placeholder volume proxy
        drop_mode = sub_bass_beat
        beats_elapsed = elapsed * 2  # estimated for demo

        if sub_bass_beat and elapsed - last_effect_switch > 2.0:
            previous_effects = current_effects.copy()
            shuffled_pool = EFFECTS[:]
            random.shuffle(shuffled_pool)
            new_effects = shuffled_pool[:2]
            while set(new_effects) == set(previous_effects):
                random.shuffle(shuffled_pool)
                new_effects = shuffled_pool[:2]
            current_effects = new_effects
            last_effect_switch = elapsed
            print(f"[SELECTED FX] {' + '.join(EFFECT_NAMES.get(e, 'Unknown') for e in current_effects)}")

        elif elapsed - last_effect_switch > 8.0:
            previous_effects = current_effects.copy()
            shuffled_pool = EFFECTS[:]
            random.shuffle(shuffled_pool)
            current_effects = shuffled_pool[:2]
            last_effect_switch = elapsed
            print(f"[FALLBACK FX] {' + '.join(EFFECT_NAMES.get(e, 'Unknown') for e in current_effects)}")

        frame = blend_effects(current_effects, beats_elapsed, center, vol, drop_mode, beat_flags, (height, width, 3), mode='add')

        effect_name = " + ".join(EFFECT_NAMES.get(e, "Unknown") for e in current_effects)
        cv2.putText(
            frame, effect_name, (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA
        )

        print(f"[ACTIVE FX]  {elapsed:.2f}s | {effect_name} | Drop: {drop_mode}")

        cv2.imshow(win_name, frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    beat_detector.stop()
    cv2.destroyAllWindows()
