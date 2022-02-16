import noisereduce as nr
import numpy as np
from numpy import asarray, where
from scipy import signal


def spectral_gate(data, noise, rate):
    """
    Performs spectral gating

    :param data: data vector of signal
    :param noise: noise vector of signal
    :param rate: rate of signal
    :return: time-domain noise reduced data
    """

    return nr.reduce_noise(y=data, sr=rate, freq_mask_smooth_hz=1000, time_mask_smooth_ms=200, stationary=True,
                           n_std_thresh_stationary=2.0, prop_decrease=1.0, y_noise=noise).astype('int16')


def spectral_subtract(sig_data, sig_rate, noise, noise_rate, SD_f_l=0, SD_f_u=1000):
    """
    Performs spectral subtraction

    :param sig_data: data vector of signal
    :param sig_rate: rate of signal
    :param noise: noise data vector
    :param noise_rate: rate of noise signal
    :param SD_f_l: how many lower standard deviations below magnitude average to keep, default is none (0)
    :param SD_f_u: how many upper standard deviations above magnitude average to keep, default is nearly all (1000)
    :return: time-domain noise reduced data
    """

    # STFT
    f, t, Zxx_noise = signal.stft(noise, noise_rate, nperseg=850)
    _, _, Zxx_signal = signal.stft(sig_data, sig_rate, nperseg=850)

    # Noise portion
    ns = Zxx_noise
    nss = np.abs(ns)
    mns = np.mean(nss, axis=1)

    # Non-noise portion
    s = Zxx_signal
    ss = np.abs(s)  # get magnitude
    angle = np.angle(s)  # get phase
    b = np.exp(1.0j * angle)  # use this phase information for inverse transform

    # Subtract noise spectral mean from input spectral
    sa = ss - mns.reshape((mns.shape[0], 1))  # reshape for broadcast to subtract
    sa_std = np.std(sa)  # standard deviation of data times factor
    sa_mean = np.mean(sa)  # get total mean
    sa[where(sa > (sa_mean + SD_f_u * sa_std))] = 0  # remove above SD_f_u std
    sa[where(sa < (sa_mean - SD_f_l * sa_std))] = 0  # remove below SD_f_l std
    sa0 = sa * b  # apply phase information

    # ISTFT
    _, xrec = signal.istft(sa0, sig_rate)
    return asarray(xrec).astype('int16')
