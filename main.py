# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 12:20:01 2025

@author: zshaf
"""

from visuals.engine import run_visualizer
from playsound import playsound
import threading
import librosa

AUDIO_PATH = "Boogie T x Izzy Vadim - Psych (EKLYPSE x Zouth Flip).wav"

def play_audio(audio_path):
    playsound(audio_path)

def main():
    y, sr = librosa.load(AUDIO_PATH)
    duration_sec = librosa.get_duration(y=y, sr=sr)

    audio_thread = threading.Thread(target=play_audio, args=(AUDIO_PATH,))
    audio_thread.start()
    run_visualizer(AUDIO_PATH, duration_sec)
    audio_thread.join()

if __name__ == "__main__":
    main()