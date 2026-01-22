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
        self.bytecode: bytearray = []
        self.file = [line.strip() for line in file]
        self.verify()
        pass

    def add_const(self, value):
        if value not in self.constants:
            self.constants.append(value)
        return self.constants.index(value)

    def add_var(self, name):
        if name not in self.variables:
            self.variables[name] = len(self.variables)
        return self.variables[name]

    def verify(self):
        if (self.file[0] == ASCII_SIGNATURE):
            self.is_valid = True
            self.compile_to_bytecode()
        else:
            Error.error('SYN_001', self.file[0])

    def compile_to_bytecode(self):
        if self.is_valid:
            for i, line in enumerate(self.file):

                if line.startswith('/syn/'):
                    line = BINARY_SIGNATURE

                elif line.startswith('/end/'):
                    self.bytecode += convert('HALT')

                elif line.startswith('var/'):
                    # var/int/x/1
                    parts = line.split('/')
                    if len(parts) >= 3:
                        var_type = parts[1]
                        var_name = parts[2]
                        var_value = parts[3]

                        const_idx = self.add_const(var_value)
                        var_idx = self.add_var(var_name)

                        self.bytecode += convert('LOAD_CONST')
                        self.bytecode += bytes([const_idx])

                        self.bytecode += convert('STORE_VAR')
                        self.bytecode += bytes([var_idx])
                    else:
                        Error.error(
                            'SYN_003', 'Ensure if your varialbles follow this pattern: "var/type/value"')

                elif line.startswith('return/'):
                    # return/int/x
                    parts = line.split('/')
                    if len(parts) >= 2:
                        type = parts[1]
                        var_value = parts[2]
                        var_value = var_value[1:-1]

                        if var_value in self.variables:
                            var_idx = self.variables[var_value]

                            self.bytecode += convert('LOAD_VAR')
                            self.bytecode += bytes([var_idx])
                            self.bytecode += convert('PRINT')
                        else:

                            if '+' in var_value:
                                left, right = var_value.split('+')

                                # LOAD_VAR x
                                left_idx = self.variables[left.strip()]
                                self.bytecode += convert('LOAD_VAR')
                                self.bytecode += bytes([left_idx])

                                # LOAD_VAR y
                                right_idx = self.variables[right.strip()]
                                self.bytecode += convert('LOAD_VAR')
                                self.bytecode += bytes([right_idx])

                                self.bytecode += convert('ADD')
                                self.bytecode += convert('PRINT')

                            elif '-' in var_value:
                                left, right = var_value.split('-')

                                # LOAD_VAR x
                                left_idx = self.variables[left.strip()]
                                self.bytecode += convert('LOAD_VAR')
                                self.bytecode += bytes([left_idx])

                                # LOAD_VAR y
                                right_idx = self.variables[right.strip()]
                                self.bytecode += convert('LOAD_VAR')
                                self.bytecode += bytes([right_idx])

                                self.bytecode += convert('SUB')
                                self.bytecode += convert('PRINT')

                            elif '*' in var_value:
                                left, right = var_value.split('*')

                                # LOAD_VAR x
                                left_idx = self.variables[left.strip()]
                                self.bytecode += convert('LOAD_VAR')
                                self.bytecode += bytes([left_idx])

                                # LOAD_VAR y
                                right_idx = self.variables[right.strip()]
                                self.bytecode += convert('LOAD_VAR')
                                self.bytecode += bytes([right_idx])

                                self.bytecode += convert('MUL')
                                self.bytecode += convert('PRINT')

                            elif '/' in var_value:
                                left, right = var_value.split('/')

                                # LOAD_VAR x
                                left_idx = self.variables[left.strip()]
                                self.bytecode += convert('LOAD_VAR')
                                self.bytecode += bytes([left_idx])

                                # LOAD_VAR y
                                right_idx = self.variables[right.strip()]
                                self.bytecode += convert('LOAD_VAR')
                                self.bytecode += bytes([right_idx])

                                self.bytecode += convert('DIV')
                                self.bytecode += convert('PRINT')

                            else:
                                Error.error(
                                    'SYN_005', var_value)

                    else:
                        Error.error(
                            'SYN_003', 'Ensure if your varialbles follow this pattern: "return/type/value"')

                elif line == '':
                    line = convert('NOP')

                else:
                    Error.error('SYN_004', line)

            # print(self.bytecode)
