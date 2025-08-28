"""
File for audio project functions.
"""
import time

count = 0
start_time = time.time()
times = []
def process_audio(input_data: bytes):
    """
    Processes input mic data, returning processed audio.
    """
    global count, start_time, times
    count += 2048
    if count >= 22050:
        current = time.time()
        times.append(current - start_time)
        if len(times) > 1:
            print(f"average time: {sum(times[1:]) / (len(times) - 1)}")
        start_time = current
        count = 0

    return input_data
