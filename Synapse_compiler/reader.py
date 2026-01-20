"""
    Reads the .syn file, returning all separate lines with `return_content()`
"""
from errors import *


class Read:
    def __init__(self, file_name):
        self.lines = []
        try:
            with open(file_name, 'r', encoding='utf-8') as arquivo:
                for linha in arquivo:
                    self.lines.append(linha)
        except FileNotFoundError:
            Error.error('SYN_002', file_name)

    def return_content(self):
        return self.lines
