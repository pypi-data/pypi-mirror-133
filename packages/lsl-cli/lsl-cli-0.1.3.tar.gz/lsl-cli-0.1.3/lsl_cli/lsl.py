from .utils import *
from .list import list
from .echo import echo
from .show import show
from .find import find
from .stub import stub
from .rate import rate
from .delay import delay
from .xdf import xdf_info, xdf_play, xdf_rate
import argparse

DEFAULT_TIMEOUT = 0.2 # 200ms should be enough for most applications


def complete(args): 
	import subprocess
	import os
	path = os.path.dirname(os.path.abspath(__file__))
	os.chdir(path)

	if args.zsh:
		_args = ['zsh']
	elif args.bash:
		_args = ['bash']
	else: 
		_args = []
	subprocess.call([os.path.join(path, 'extra/lsl_complete_script.sh')] + _args, env=os.environ.copy())
	

def main():
	parser = argparse.ArgumentParser()

	subparser = parser.add_subparsers(dest='command')

	complete_parser = subparser.add_parser('complete')
	complete_parser_group = complete_parser.add_mutually_exclusive_group()
	complete_parser_group.add_argument('--zsh', '-z', action='store_true', dest='zsh')
	complete_parser_group.add_argument('--bash', '-b', action='store_true', dest='bash')

	complete_parser.set_defaults(func=complete)

	list_parser = subparser.add_parser('list')
	list_parser.add_argument('--all', '-a', dest='all', action='store_true')
	list_parser.add_argument('--list', '-l', dest='list', action='store_true')
	list_parser.add_argument('--timeout', '-t', dest='timeout', type=float, default=DEFAULT_TIMEOUT)

	for field in STREAM_INFO_FIELDS:
		list_parser.add_argument(f'--{field}', dest=field, action='store_true', help=f"Display stream {field}")
	
	list_parser.set_defaults(func=list)

	echo_parser = subparser.add_parser('echo', description="Print to screen messages from a stream.")
	echo_parser.add_argument('name', help='Stream name')
	echo_parser.add_argument('--timeout', '-t', dest='timeout', type=float, default=DEFAULT_TIMEOUT)

	echo_parser.set_defaults(func=echo)

	show_parser = subparser.add_parser('show')
	show_parser.add_argument('name', help='Stream name')
	show_parser.add_argument('--timeout', '-t', dest='timeout', type=float, default=DEFAULT_TIMEOUT)

	show_parser.set_defaults(func=show)

	find_parser = subparser.add_parser('find')
	for field in STREAM_INFO_FIELDS:
		find_parser.add_argument(f'--{field}', dest=field, type=str, help=f"Display stream {field}")
	find_parser.add_argument('--timeout', '-t', dest='timeout', type=float, default=DEFAULT_TIMEOUT)
	find_parser.set_defaults(func=find)

	stub_parser = subparser.add_parser('stub')
	stub_parser.add_argument('name', help='Stream name')
	stub_parser.add_argument('-n', '--nominal_srate', dest='nominal_srate', type=float, default=100)
	stub_parser.add_argument('-c', '--channel_count', dest='channel_count', type=int, default=1)
	stub_parser.add_argument('-s', '--chunk_size', dest='chunk_size', type=int, default=1)
	stub_parser.set_defaults(func=stub)

	rate_parser = subparser.add_parser('rate')
	rate_parser.add_argument('name', help='Stream name')
	rate_parser.add_argument('-c', '--continuous', dest="continuous", action="store_true")
	rate_parser.add_argument('-n', '--number', dest="number", type=int, default=50)
	rate_parser.add_argument('-t', '--timeout', dest='timeout', type=float, default=DEFAULT_TIMEOUT)
	rate_parser.set_defaults(func=rate)

	delay_parser = subparser.add_parser('delay')
	delay_parser.add_argument('name', help='Stream name')
	delay_parser.add_argument('-c', '--continuous', dest="continuous", action="store_true")
	delay_parser.add_argument('-n', '--number', dest="number", type=int, default=50)
	delay_parser.add_argument('-t', '--timeout', dest='timeout', type=float, default=DEFAULT_TIMEOUT)
	delay_parser.set_defaults(func=delay)

	xdf_parser = subparser.add_parser('xdf')
	xdf_parser.set_defaults(func=lambda _: xdf_parser.print_help())

	xdf_subparser = xdf_parser.add_subparsers(dest='xdf_command')
	
	xdf_info_parser = xdf_subparser.add_parser('info')
	xdf_info_parser.add_argument('file', type=str)
	xdf_info_parser.set_defaults(func=xdf_info)

	xdf_play_parser = xdf_subparser.add_parser('play')
	xdf_play_parser.add_argument('file', type=str)
	xdf_play_parser.add_argument('-l', '--loop', action='store_true')
	xdf_play_parser.set_defaults(func=xdf_play)

	xdf_rate_parser = xdf_subparser.add_parser('rate')
	xdf_rate_parser.add_argument('file', type=str)
	xdf_rate_parser.set_defaults(func=xdf_rate)

	args = parser.parse_args()
	if args.command is None:
		parser.print_help()
	else: 
		res = args.func(args)
		if res is False:
			parser.print_help()



