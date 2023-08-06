import pylsl
import numpy as np
import time
from .utils import suppress_stdout_stderr

def rate(args): 
    name = args.name
    count = max(args.count, 5)


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


    tstamp_ivals = []
    time_ivals = []
    last_tstamp = None
    last_tnow = None
    # i = 0


    while len(tstamp_ivals) < count:
        try:
            res = inlet.pull_sample(0)
            if res[0] is None:
                continue
            else: 
                tnow = time.perf_counter()
                tstamp = res[1]
                if last_tstamp is None: 
                    last_tstamp = tstamp
                    last_tnow = tnow
                else: 
                    tstamp_ivals.append(tstamp - last_tstamp)
                    last_tstamp = tstamp

                    time_ivals.append(tnow - last_tnow)
                    last_tnow = tnow
        except KeyboardInterrupt:
            break

    if len(tstamp_ivals) > 10:

        tstamp_rates = 1. / np.asarray(tstamp_ivals)
        print(f"Evaluated timestamp rate:  {tstamp_rates.mean():.3f} ({tstamp_rates.std(ddof=1.):.3f})")

        arrival_rates = 1./np.asarray(time_ivals)
        print(f"Evaluated arrival rate: {arrival_rates.mean():.3f} ({arrival_rates.std(ddof=1.):.3f})")