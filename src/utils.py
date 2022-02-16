import numpy as np
from scipy.signal import butter, sosfilt

from apply_profile import apply_profile


def extra_filter(audio):
    """
    An extra filter to throw over the audio for quality purposes or if the Teensy is recording raw data.

    :param audio: vector containing audio
    :return: vector containing filtered audio
    """
    sos = butter(20, [150, 1500], 'bandpass', fs=44100, output='sos')
    return sosfilt(sos, audio).astype('int16')


def normalize(audio):
    """
    Normalizes the audio so that the largest value is the maximum for a 16 bit signed integer.

    :param audio: vector containing audio
    :return: vector containing normalized audio
    """
    assert audio.dtype == 'int16'
    return audio * int(32767 / np.max(np.abs(audio)))


def noise_profiling(audio, fs, session=0):
    """
    Wrapper for applying the noise profile based on individual recording sessions or 0 to just return the input.

    :param audio: vector containing audio
    :param fs: sampling frequency
    :param session: session number to choose which kernel based on the reflective surface and total setup.
    :return: vector containing processed audio
    """
    if session == 1:
        fvec = np.loadtxt('kernels/session-1/f_vec_50_2000_50.txt', dtype=float).flatten()
        gvec = np.loadtxt('kernels/session-1/g_vec_50_2000_50.txt', dtype=float).flatten()
    elif session == 2:
        fvec = np.loadtxt('kernels/session-2/f_vec_50_2000_d50_t50.txt', dtype=float).flatten()
        gvec = np.loadtxt('kernels/session-2/g_vec_50_2000_d50_t50.txt', dtype=float).flatten()
    else:
        return audio

    return apply_profile(audio, fvec, gvec, fs).astype('int16')
