# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 12:18:41 2025

@author: zshaf
"""

import librosa
import numpy as np

def extract_audio_features(audio_path):
    y, sr = librosa.load(audio_path)
    
    # Beat detection
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    # RMS (volume)
    hop_length = 512
    rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
    rms_times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop_length)

    # Mel spectrogram (frequency content)
    mel = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=40, hop_length=hop_length)
    mel_db = librosa.power_to_db(mel, ref=np.max)
    mel_times = librosa.frames_to_time(np.arange(mel_db.shape[1]), sr=sr, hop_length=hop_length)

    return {
        "beat_times": beat_times,
        "rms": rms,
        "rms_times": rms_times,
        "mel": mel_db,
        "mel_times": mel_times
    }