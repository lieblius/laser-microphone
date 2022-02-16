# WRITTEN BY ANDREW SAGER FOR EECS 452
# FUNCTION: READS INPUT AND OUTPUT SIGNALS AND GENERATES A GAIN VECTOR (as a .txt)
# Requires: Matching input / outputs and profiling_utils

from numpy import *
from scipy.io.wavfile import read

from profile_utils import invertThreshholdNormalize, makeSameLength, boost, profile, combine

# GLOBALS
fs = 44100
dfreq = 25
amp_threshold = 10

tSweep = 5

f_start1 = 50
f_end1 = 500

f_start2 = 500
f_end2 = 1400

f_start3 = 1200
f_end3 = 2000


def profile_2k(fs=fs, dfreq=dfreq, amp_threshold=amp_threshold):
    input1 = array(read("input50_500.wav")[1], dtype=float).flatten()
    output1 = array(read("output50_500.wav")[1], dtype=float).flatten()

    input1, output1 = boost(makeSameLength(input1, output1)[0], makeSameLength(input1, output1)[1])
    f_1, g_1, df_1 = profile(input1, output1, f_start1, f_end1, fs=fs, freqRes=dfreq)
    g_1 = invertThreshholdNormalize(g_1, threshold=amp_threshold)

    input2 = array(read("input500_1400.wav")[1], dtype=float).flatten()
    output2 = array(read("output500_1400.wav")[1], dtype=float).flatten()

    input2, output2 = boost(makeSameLength(input2, output2)[0], makeSameLength(input2, output2)[1])
    f_2, g_2, df_2 = profile(input2, output2, f_start2, f_end2, fs=fs, freqRes=dfreq)
    g_2 = invertThreshholdNormalize(g_2, threshold=amp_threshold)

    # note overlap
    input3 = array(read("input1200_2000.wav")[1], dtype=float).flatten()
    output3 = array(read("output1200_2000.wav")[1], dtype=float).flatten()

    input3, output3 = boost(makeSameLength(input3, output3)[0], makeSameLength(input3, output3)[1])
    f_3, g_3, df_3 = profile(input3, output3, f_start3, f_end3, fs=fs, freqRes=dfreq)
    g_3 = invertThreshholdNormalize(g_3, threshold=amp_threshold)

    f_tot, g_tot = combine([f_1, f_3, f_3], [g_1, g_2, g_3])

    return f_tot, g_tot


f_tot, g_tot = profile_2k()
outNameF = "f_vec_" + str(f_start1) + "_" + str(f_end3) + "_" + str(int(dfreq)) + ".txt"
outNameG = "g_vec_" + str(f_start1) + "_" + str(f_end3) + "_" + str(int(dfreq)) + ".txt"
savetxt(outNameF, f_tot)
savetxt(outNameG, g_tot)
