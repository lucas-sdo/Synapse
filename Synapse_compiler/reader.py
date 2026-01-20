"""
    Reads the .syn file, returning all separate lines with `return_content()`
"""


class Read:
    def __init__(self, file_name):
        self.lines = []
        with open(file_name, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                self.lines.append(linha)

    def return_content(self):
        return self.lines
