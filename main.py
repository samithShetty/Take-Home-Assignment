from utils import poll_clinician_statuses
import time
from config import POLLING_INTERVAL_SECS

if __name__ == "__main__":
    prev_call_time_secs = 0 
    while True:
        current_time_secs = time.time()
        if current_time_secs - prev_call_time_secs >= POLLING_INTERVAL_SECS:
            print("Current Time:", time.asctime())
            poll_clinician_statuses()
            prev_call_time_secs = current_time_secs