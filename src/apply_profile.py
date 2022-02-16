# WRITTEN BY ANDREW SAGER FOR EECS 452
# FUNCTION: APPLIES A GAIN VECTOR TO AN INPUT

from numpy import argwhere, newaxis, concatenate
from scipy.signal import stft, istft


def apply_profile(input, f_vec, gainVec, fs):
    """
    Applies the gain vector to the input

    :param input: input audio signal
    :param f_vec: vector generated in profile.py
    :param gainVec: vector generated in profile.py
    :param fs: sampling frequency
    :return: processed audio signal
    """
    df = f_vec[1] - f_vec[0]
    f, t, Zxx = stft(input, fs, nperseg=fs / df)

    if ((f[1] - f[0]) != (f_vec[1] - f_vec[0])):
        print("Size ERROR")
        raise

    lowIdx = argwhere(f == f_vec[0]).flatten()[0]
    highIdx = lowIdx + len(f_vec)

    gainVec = gainVec[:, newaxis]
    newMiddle = Zxx[lowIdx:highIdx, :] * gainVec
    total = concatenate((Zxx[:lowIdx, :], newMiddle, Zxx[highIdx:, :]))

    return istft(total, fs=fs)[1]
