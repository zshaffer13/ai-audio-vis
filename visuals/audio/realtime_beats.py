# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 10:54:02 2025

@author: zshaf
"""

# visuals/audio/realtime_beats.py

import numpy as np
import wavio
import wave
import pyaudio
import threading

class RealTimeBeatDetector:
    def __init__(self, filepath):
        self.wf = wave.open(filepath, 'rb')
        self.fs = self.wf.getframerate()
        self.channels = self.wf.getnchannels()
        self.bytes_per_sample = self.wf.getsampwidth()

        self.beat_flags = {
            "sub_bass": False,
            "bass": False,
            "midrange": False
            # add more if needed
        }

        self.max_values = {k: 10 for k in self.beat_flags}
        self.lock = threading.Lock()
        self._stop = False

    def _detect_beats(self, data):
        audio = wavio._wav2array(self.channels, self.bytes_per_sample, data)
        audio_fft = np.abs(np.fft.fft(audio)[0:int(len(audio)/2)]) / len(audio)
        freqs = self.fs * np.arange(len(audio_fft)) / len(audio_fft) / 2

        bands = {
            "sub_bass": (20, 60),
            "bass": (60, 250),
            "midrange": (500, 2000),
        }

        for band, (low, high) in bands.items():
            indices = np.where((freqs >= low) & (freqs <= high))[0]
            max_val = np.max(audio_fft[indices]) if len(indices) > 0 else 0
            with self.lock:
                self.max_values[band] = max(self.max_values[band], max_val)
                if max_val >= self.max_values[band] * 0.9:
                    self.beat_flags[band] = True
                elif max_val < self.max_values[band] * 0.3:
                    self.beat_flags[band] = False

    def _callback(self, in_data, frame_count, time_info, status):
        data = self.wf.readframes(frame_count)
        if not data:
            self._stop = True
            return (data, pyaudio.paComplete)
        self._detect_beats(data)
        return (None, pyaudio.paContinue)

    def start(self):
        p = pyaudio.PyAudio()
        self.stream = p.open(
            format=p.get_format_from_width(self.bytes_per_sample),
            channels=self.channels,
            rate=self.fs,
            output=True,
            stream_callback=self._callback
        )
        self.stream.start_stream()

    def get_beats(self):
        with self.lock:
            return self.beat_flags.copy()

    def is_active(self):
        return not self._stop
