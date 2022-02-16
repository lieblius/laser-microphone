Contents:
    data:
        - raw unfiltered recordings
        output:
            - folders containing processed recordings with different configurations of processing
    src:
        FIR_Lab3:
            - code for teensy filtering
        kernels:
            - folders containing frequency profiling kernels
        profiling:
            - profile.py (generates kernels)
            - profile_utils.py (helpers for profile.py)
        - apply_profile.py (contains function to apply the generated kernels to the audio signal)
        - spectral.py (contains functions for spectral subtraction and spectral gating)
        - utils.py (general helper functions for normalization, frequency profiling wrapper, etc.)
        - main.py (main program driver: handles recording, file input, file output, playback)
        - INSTALL.txt (install instructions)
        - USAGE.txt (usage instructions)
        - OVERVIEW.txt (detailed descriptions of source code)
    - videos (video of recorded demo)
    - COPYRIGHT.txt

Andrew Sager (adsager@umich.edu), Ryan Aridi (raridi@umich.edu), Evan Arora (ear@umich.edu), Kyle Liebler (liebler@umich.edu)
