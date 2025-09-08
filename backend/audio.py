"""
File for audio project functions.
"""
import time
import librosa
import numpy as np

count = 0
start_time = time.time()
times = []
SAMPLE_RATE = 22050
BYTE_RATE = SAMPLE_RATE * 4 # 4 bytes per sample
INPUT_SIZE = 2048

# each input_data is 2048 samples -> 8192 bytes
# at 22050 samples/s, we should get 11 input_data per 1.021 seconds
# so, we can print the delay after every 11 inputs
time_per_11_inputs = 1.021678

def input_audio(input_data: bytes):
    """
    Receives input mic data from the frontend, then returns processed audio.
    """
    global count, start_time, times, BYTE_RATE, time_per_11_inputs
    
    # confirming each chunk is 1s
    if count != 11:
        count += 1
    else:
        count = 0
        delay = time.time() - start_time - time_per_11_inputs
        start_time = time.time()
        times.append(delay)
        if len(times) > 25: # rolling window of last 25 delays
            print(f"average delay: {sum(times[-25:]) / 25}")
        elif len(times) > 1:
            print(f"average delay: {sum(times[1:]) / (len(times) - 1)}")

    # processing audio
    D = np.abs(librosa.stft(np.frombuffer(input_data, dtype=np.float32), n_fft=INPUT_SIZE))
    freq_bins = librosa.fft_frequencies(sr=SAMPLE_RATE, n_fft=INPUT_SIZE)

    # perform fft, then send the data to the frontend
    # input_audio constantly takes in audio from the mic, some processing is
    #  done, then return_audio constantly takes the processed audio and sends to frontend

