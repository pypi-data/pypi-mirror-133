import pylsl
import numpy as np
import time
from datetime import datetime
from .utils import suppress_stdout_stderr

MAX_BUFFER_SIZE = 20_000



def delay(args): 
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

    delays = []
    sleep_time = 0.5/rate

    while len(delays) < count or count == -1:
        try:            
            res = inlet.pull_sample(0)
            if res[0] is None:
                continue
            else: 
                tnow = datetime.now().timestamp()
                tstamp = res[1]

                delay = tnow - tstamp

                delays.append(delay)

                if len(delays) > MAX_BUFFER_SIZE:
                    delays = delays[-MAX_BUFFER_SIZE:]

                if count == -1:
                    print(f"Timestamp delay: {np.mean(delays) * 1e3:.3f}ms", 
                        end="\r"
                    )

                time.sleep(sleep_time)

        except KeyboardInterrupt:
            break

    print(f"Timestamp delay: {np.mean(delays) * 1e3:.3f}ms")
