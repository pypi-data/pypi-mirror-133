STREAM_INFO_FIELDS = (
    'name',
    'type', 
    'source_id', 
    'channel_count', 
    'channel_format', 
    'nominal_srate', 
    'hostname', 
    'uid', 
    'version', 
    'session_id', 
    'created_at'
)


def print_infos(infos, fields=STREAM_INFO_FIELDS): 
    fields = {fields} if isinstance(fields, str) else fields
    infos = [infos] if not hasattr(infos, '__iter__') else infos 

    for field in fields:
        if field not in STREAM_INFO_FIELDS:
            raise ValueError(f"Unkown field: {field}")

    for info in infos: 
        print(info.name())
        for field in fields:
            print(f'  {field}: {getattr(info, field)()}')
            
def infos_to_dict(infos): 
    if not hasattr(infos, '__iter__'):
        infos = [infos]
    return [{
        f: getattr(info, f)() 
        for f in STREAM_INFO_FIELDS
    } for info in infos]

def filter_stream_fields(infos, **fields): 
    for info in infos:
        pass

import os

# Define a context manager to suppress stdout and stderr.
class suppress_stdout_stderr(object):
    '''
    A context manager for doing a "deep suppression" of stdout and stderr in 
    Python, i.e. will suppress all print, even if the print originates in a 
    compiled C/Fortran sub-function.
       This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).      

    '''
    def __init__(self):
        # Open a pair of null files
        self.null_fds =  [os.open(os.devnull,os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0],1)
        os.dup2(self.null_fds[1],2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0],1)
        os.dup2(self.save_fds[1],2)
        # Close all file descriptors
        for fd in self.null_fds + self.save_fds:
            os.close(fd)