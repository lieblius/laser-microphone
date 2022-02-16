#WRITTEN BY ANDREW SAGER FOR EECS 452
#Includes all functions to allow for mirror profiling

from numpy import *
from scipy.signal import stft


def boost(input, output):
    return input, output * (sum(input) / sum(output))


def makeSameLength(input, output):
    if len(input) > len(output):
        return input, output[:len(input)]
    else:
        return input[:len(input)], output


def invertThreshholdNormalize(g_vec, threshold):
    g_vec = 1 / g_vec
    g_vec[(g_vec / min(g_vec)) > threshold] = 0
    return g_vec / max(g_vec)


def combine(f_vecs, g_vecs):
    f_tot = []
    g_tot = []
    f_tot.append(f_vecs[0][0])

    for idx in range(0, len(f_vecs)):
        for idx2, f in enumerate(f_vecs[idx]):
            if f == f_tot[-1]:
                continue
            f_tot.append(f)
            g_tot.append(g_vecs[idx][idx2])

    return asarray(f_tot, dtype=int), asarray(g_tot, dtype=float)


def profile(input, output, f_start, f_end, fs, freqRes=50):
    f, t, Zxx_input = stft(input, fs, nperseg=fs / freqRes)
    f, t, Zxx_output = stft(output, fs, nperseg=fs / freqRes)
    df = f[1] - f[0]

    start_idx = round(f_start / df)
    end_idx = round(f_end / df)

    f_vec = f[start_idx:end_idx]
    gain_vec = zeros(shape(f_vec), dtype=float)

    numFreqBins = floor((f_end - f_start) / df)
    samplesPerBin = floor(len(t) / numFreqBins)

    for idx in range(start_idx, end_idx):
        inputSlice = (Zxx_input[idx, :]).flatten()
        outputSlice = (Zxx_output[idx, :]).flatten()
        peak_idx = argmax(inputSlice)

        peak_idx_left = round(max(0, peak_idx - floor(samplesPerBin / 2)))
        peak_idx_right = round(min(peak_idx + floor(samplesPerBin / 2), len(t) - 1))

        sum_input = sum(inputSlice[peak_idx_left:peak_idx_right])
        sum_output = sum(outputSlice[peak_idx_left:peak_idx_right])

        gain = abs(sum_output) / abs(sum_input)

        gain_vec[idx - start_idx] = gain

    return f_vec, gain_vec, df
