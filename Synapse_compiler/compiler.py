"""
    Compiles the .syn to bytecode.
"""
from errors import *

BINARY_SIGNATURE = b'0x2F0x730x790x6E0x2F'
ASCII_SIGNATURE = '/syn/\n'


class Compiler:
    def __init__(self, file: list):
        self.is_valid = False
        self.file = file
        self.verify()
        pass

    def verify(self):
        if (self.file[0] == ASCII_SIGNATURE):
            self.is_valid = True
        else:
            Error.error('SYN_001', self.file[0])
