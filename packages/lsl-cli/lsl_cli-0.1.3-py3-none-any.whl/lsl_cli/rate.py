import pylsl
import numpy as np
import time
from .utils import suppress_stdout_stderr

MAX_BUFFER_SIZE = 20_000

def rate(args): 
    name = args.name

    if args.continuous: 
        count = -1
    else:
        count = max(args.number, 5)

    with suppress_stdout_stderr():
        infos = pylsl.resolve_byprop("name", name, timeout=args.timeout)
    
    if len(infos) == 0:
        print("Cannot find outlet.")
        return 0

    info = infos[0]
    rate = info.nominal_srate()

    print(f'Announced rate for stream "{name}": {rate if rate > 0 else "IRREGULAR_RATE"}')

    # inlet = silent_output(
    with suppress_stdout_stderr():
        inlet = pylsl.StreamInlet(info)


    times = []
    timestamps = []

    sleep_time = 0.5/rate


    while len(times) < count or count == -1:
        try:
            res = inlet.pull_chunk(0)

            if res[0] is None:
                continue
            else: 
                timestamps.extend(res[1])
                times.append(time.perf_counter())

                if len(times) > MAX_BUFFER_SIZE:
                    times = times[-MAX_BUFFER_SIZE:]

                if len(timestamps) > MAX_BUFFER_SIZE:
                    timestamps = timestamps[-MAX_BUFFER_SIZE:]

                if count == -1 and len(timestamps) > 1 and len(times) > 1:
                    times_ = np.asarray(times)
                    timestamps_ = np.asarray(timestamps)

                    arrival_rate = 1./np.mean(times_[1:] - times_[:-1])
                    tstamp_rate = 1. / np.mean(timestamps_[1:] - timestamps_[:-1])
                    print(f"Timestamp rate:  {tstamp_rate:.3f}Hz - Arrival rate: {arrival_rate:.3f}Hz", end="\r")

            time.sleep(sleep_time)

        except KeyboardInterrupt:
            break

    times_ = np.asarray(times)
    timestamps_ = np.asarray(timestamps)

    arrival_rate = 1./np.mean(times_[1:] - times_[:-1])
    tstamp_rate = 1. / np.mean(timestamps_[1:] - timestamps_[:-1])
    print(f"Timestamp rate:  {tstamp_rate:.3f}Hz - Arrival rate: {arrival_rate:.3f}Hz")