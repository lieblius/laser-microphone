import sys

import sounddevice as sd
from logmmse import logmmse
from scipy.io import wavfile

from spectral import spectral_subtract, spectral_gate
from utils import *


def process_audio(audio, noise, fs):
    """
    Apply noise reduction and speech enhancement functions. Comment out extra_filter and spectral_gate if used with
    Teensy and Raspberry Pi setup.

    :param audio: vector containing audio
    :param noise: vector containing noise
    :param fs: sampling frequency
    :return: vector containing processed audio
    """
    audio = audio.astype('int16')
    audio = extra_filter(audio)
    audio = spectral_subtract(audio, fs, noise, fs)
    audio = spectral_gate(audio, noise, fs)
    audio = noise_profiling(audio, fs, session=2)
    audio = logmmse(audio, fs)
    audio = extra_filter(audio)
    audio = normalize(audio)
    return audio


def main():
    write = False
    play = True

    filename = '../data/conversation-direct-laser'
    sd.default.channels = 1

    if len(sys.argv) == 2:
        live = True

        # Allow for at least 3 seconds of noise recorded at the beginning
        duration = max(int(sys.argv[1]), 3)
    else:
        live = False

    if live:
        print(f'Recording for {duration} seconds.')
        fs = 44100
        sd.default.samplerate = fs
        audio = sd.rec(duration * fs, dtype='int16').flatten()
        sd.wait()
    else:
        fs, audio = wavfile.read(f'{filename}.wav')
        sd.default.samplerate = fs
        audio = audio.astype('int16')

    audio = normalize(audio)
    audio = process_audio(audio, audio[:fs * 3], fs)

    if play:
        print('Playing recorded audio.')
        sd.play(audio, fs)
        sd.wait()

    if write:
        print('Saving recorded audio.')
        wavfile.write(f'{filename}_processed.wav', fs, audio)


if __name__ == "__main__":
    main()
