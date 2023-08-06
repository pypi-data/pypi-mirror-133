import pylsl
import time
import numpy as np
import threading
import signal
import os
from .utils import suppress_stdout_stderr, print_infos


def stub(args):
    name = args.name
    channel_count = args.channel_count
    rate = args.nominal_srate
    chunk_size = args.chunk_size

    with suppress_stdout_stderr():
        info = pylsl.StreamInfo(name=name, source_id=f'stub-{os.getpid()}', channel_count=channel_count, nominal_srate=rate)
        outlet = pylsl.StreamOutlet(info)

    print("Started stub ", end="")
    print_infos([info])

    exit_event = threading.Event()

    if rate > 0:
        delay = 1./rate

    def signal_handler(signum, frame):
        exit_event.set()

    def send_data(): 
        data = np.random.randn(chunk_size, channel_count).tolist()
        tstamp = time.perf_counter()

        while not exit_event.is_set():
            outlet.push_chunk(data)
            data = np.random.randn(chunk_size, channel_count).tolist()

            if rate > 0:
                tstamp = tstamp + delay 
                tsleep = tstamp - time.perf_counter()
                if tsleep > 0:
                    time.sleep(tsleep)

            elif rate == pylsl.IRREGULAR_RATE:
                time.sleep(np.random.uniform(0.1, 1))   
                tstamp = time.perf_counter() 

    signal.signal(signal.SIGINT, signal_handler)
    thread = threading.Thread(target=send_data)
    thread.start()
    thread.join()