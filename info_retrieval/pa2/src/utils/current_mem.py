from os import getpid
import psutil

proc = psutil.Process(getpid())

def current_mem():
    # current memory usage in bytes 
    return proc.memory_info().rss
