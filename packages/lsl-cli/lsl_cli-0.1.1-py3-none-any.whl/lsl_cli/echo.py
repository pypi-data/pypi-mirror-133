import pylsl
import time 
from datetime import datetime
from .utils import suppress_stdout_stderr

def echo(args): 
	stream_name = args.name

	infos = pylsl.resolve_streams(args.timeout)
	names = [i.name() for i in infos]

	if stream_name not in names: 
		print('Stream not found.')
		return

	stream_info = infos[names.index(stream_name)]

	if stream_info.nominal_srate() != pylsl.IRREGULAR_RATE:
		delay = 0.9 / stream_info.nominal_srate() 
	else: 
		delay = 0.1
	
	with suppress_stdout_stderr():
		inlet = pylsl.StreamInlet(stream_info)
	
	running = True
	while running:
		try: 
			res = inlet.pull_chunk(0)
			if len(res[0]) > 0:
				for sample, timestamp in zip(*res):
					print('{time:<10} {sample}'.format(
						time=datetime.fromtimestamp(float(timestamp)).strftime('%H:%M:%S.%f'), 
						sample=sample))
			time.sleep(delay)
		except KeyboardInterrupt:
			running = False
			
	