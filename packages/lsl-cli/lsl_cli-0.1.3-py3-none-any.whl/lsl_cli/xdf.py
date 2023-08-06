import pyxdf
import pylsl
from collections import defaultdict
from pprint import pprint
from .utils import suppress_stdout_stderr, print_infos
import threading
import time
import asyncio
import numpy as np

def xdf_resolve_to_info(data):
	try:
		channel_format = pylsl.__getattribute__(f"cf_{data['channel_format']}")
	except:
		channel_format = pylsl.cf_undefined

	with suppress_stdout_stderr():
		info = pylsl.StreamInfo(
			name=data['name'],
			type=data['type'],
			channel_count=data['channel_count'],
			channel_format=channel_format,
			nominal_srate=data['nominal_srate'], 
			source_id=data['source_id'],
		)
	return info

def add_xdf_desc(info: pylsl.StreamInfo, xdf_desc):
	xdf_desc = dict(xdf_desc[0])
	info_desc = info.desc()

	for k in xdf_desc.keys():
		xdf_subdesc = xdf_desc[k][0]

		if not hasattr(xdf_subdesc, "keys"):  
			info_desc.append_child_value(k, xdf_subdesc)
		else:
			xdf_subdesc = dict(xdf_subdesc)
			child = info_desc.append_child(k)
			for k2 in xdf_subdesc.keys():
				if isinstance(xdf_subdesc[k2], list):
					for item in xdf_subdesc[k2]: 
						if hasattr(item, 'keys'): 
							item_desc = child.append_child(k2)
							for key in item.keys():
								item_desc.append_child_value(key, item[key][0])



def xdf_info(args):
	res = pyxdf.resolve_streams(args.file)
	
	for r in res:
		print_infos(xdf_resolve_to_info(r))


class XDFPlayer: 
	def __init__(self, stream_info, data, loop=False):
		# TODO: for high speed stream, use push chunk
		self._stream_info = stream_info

		self._stopped = True
		self._data = data
		self._timestamps = data['time_stamps'] - data['time_stamps'][0]
		self._samples = data['time_series']
		if len(self._samples.shape) == 1:
			self._samples = self._samples.reshape((self._samples.shape[0], 1))
		self._samples = self._samples.tolist()
		self._current_index = 0
		self._number_samples = self._timestamps.shape[0]

		self._thread = None
		self._event_loop = None
		self._loop  = loop

	def start(self):
		self._stopped = False

		self._thread = threading.Thread(target=XDFPlayer._spin, args=(self,))
		self._thread.start()

	def stop(self):
		self._stopped = True
		self._thread.join()

	async def join(self):
		if self._event_loop is not None:
			self._event_loop.run_in_executor(None, self._thread.join)

	def _prepare(self):
		with suppress_stdout_stderr():
			self._stream_outlet = pylsl.StreamOutlet(self._stream_info)	

		print("Outlet open! Now streaming...")
		print_infos(self._stream_info)

	def _send_data(self):
		self._stream_outlet.push_sample(
			x=self._samples[self._current_index]
		)

	def _spin(self):
		self._prepare()
		tstart = time.perf_counter()
		ttarget = tstart

		self._event_loop = asyncio.new_event_loop()
		asyncio.set_event_loop(self._event_loop)

		while not self._stopped:	
			self._send_data()

			self._current_index += 1
			if self._current_index == self._number_samples: 
				if self._loop: 
					self._current_index = 0
					tstart = time.perf_counter()

				else: 
					self._stopped = True
					break
			
			ttarget = tstart + self._timestamps[self._current_index]
			tsleep = ttarget - time.perf_counter()
			if tsleep > 0: 
				time.sleep(tsleep)

	def __del__(self): 
		self.stop()

def xdf_play(args):
	stuff = pyxdf.load_xdf(args.file)[0]
	infos = pyxdf.resolve_streams(args.file)
	handlers = []

	for info, data in zip(infos, stuff):
		stream_info = xdf_resolve_to_info(info)

		add_xdf_desc(stream_info, data['info']['desc'])

		handlers.append(XDFPlayer(stream_info, data, loop=args.loop))
		handlers[-1].start()


	try: 
		loop = asyncio.get_event_loop()
		loop.run_until_complete(asyncio.wait([h.join() for h in handlers], return_when=asyncio.ALL_COMPLETED))
	except KeyboardInterrupt:
		pass


def xdf_rate(args):

	stuff = pyxdf.load_xdf(args.file)[0]
	infos = pyxdf.resolve_streams(args.file)

	name_size = max(len(info['name']) for info in infos)
	fstring = "{name:<%s} - announced rate: {srate:.3f} - effective rate {effrate:.3f}" % name_size

	for info, data in zip(infos, stuff): 
		delay = np.mean(data['time_stamps'][1:] - data['time_stamps'][:-1])
		effrate = 1./delay
		print(fstring.format(
			name=info['name'], srate=info['nominal_srate'], effrate=effrate
		))

			# f"{info['name']:<} - announced rate: {info['nominal_srate']:.3f} - effective rate {effrate:.3f}")
