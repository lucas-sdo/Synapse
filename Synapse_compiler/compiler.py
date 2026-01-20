"""
    Compiles the .syn to bytecode.
"""
from errors import *
from convert import *

BINARY_SIGNATURE: bytes = b'/syn/'
ASCII_SIGNATURE: str = '/syn/'


class Compiler:
    def __init__(self, file: list):
        self.is_valid = False
        self.constants = []
        self.variables = {}
        self.file = [line.strip() for line in file]
        self.verify()
        pass

    def verify(self):
        if (self.file[0] == ASCII_SIGNATURE):
            self.is_valid = True
            self.compile_to_bytecode()
        else:
            Error.error('SYN_001', self.file[0])

    def compile_to_bytecode(self):
        if self.is_valid:
            bytecode_lines = []

            for i, line in enumerate(self.file):

                if line.startswith('/syn/'):
                    line = BINARY_SIGNATURE

                elif line.startswith('/end/'):
                    line = convert('HALT')

                elif line.startswith('var/'):
                    parts = line.split('/')
                    if len(parts) >= 3:
                        var_name = parts[1]
                        var_value = parts[2]

                        load_const = convert('LOAD_CONST')
                        store_var = convert('STORE_VAR')

                        if load_const is not None and store_var is not None:
                            combined_bytecode = load_const + b' ' + var_value.encode() + b' ' + store_var + \
                                b' ' + var_name.encode()
                            bytecode_lines.append(combined_bytecode)
                    else:
                        Error.error(
                            'SYN_003', 'Ensure if your varialbles follow this pattern: "var/type/value"')

                elif line.startswith('return/'):
                    # return/int/6 + 7
                    content = line[6:]
                    print_bytecode = convert('PRINT')

                    if print_bytecode is not None:
                        combined = print_bytecode + b' ' + content.encode()
                        bytecode_lines.append(combined)

                elif line == '':
                    line = convert('NOP')

                else:
                    Error.error('SYN_004', line)

            print(bytecode_lines)
            return bytecode_lines
