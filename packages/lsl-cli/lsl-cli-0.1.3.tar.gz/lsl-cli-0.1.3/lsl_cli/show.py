import pylsl
from .utils import suppress_stdout_stderr

def show(args):
	stream_name = args.name
	
	with suppress_stdout_stderr():
		infos = pylsl.resolve_streams(args.timeout)
	names = [i.name() for i in infos]

	if stream_name not in names: 
		print('Stream not found.')
		return

	stream_info = infos[names.index(stream_name)]
	with suppress_stdout_stderr():
		inlet = pylsl.StreamInlet(stream_info)

	print(inlet.info().as_xml())
