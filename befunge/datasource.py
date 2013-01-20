import os
import sys    
import termios
import fcntl

class Terminal(object):
    def __init__(self):
        pass

    def __iter__(self):
        return self

    def next(self):
        return sys.stdin.read(1)
         
    def write(self, c):
        return sys.stdout.write(c)

