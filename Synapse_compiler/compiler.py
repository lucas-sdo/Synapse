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
        self.functions = {}
        self.pending_calls = []
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

    def emit_value(self, value):
        value = value.strip()

        if value.isdigit():
            const_idx = self.add_const(int(value))
            self.bytecode += convert('LOAD_CONST')
            self.bytecode += bytes([const_idx])

        elif value in self.variables:
            var_idx = self.variables[value]
            self.bytecode += convert('LOAD_VAR')
            self.bytecode += bytes([var_idx])

        else:
            Error.error('SYN_007', value)

    def emit_const_value(self, value):
        value = value.strip()
        const_idx = self.add_const(value)

        self.bytecode += convert('LOAD_CONST')
        self.bytecode += bytes([const_idx])

    def parse_string(self, value: str) -> str:
        value = value.strip()

        if (
            (value.startswith('"') and value.endswith('"')) or
            (value.startswith("'") and value.endswith("'"))
        ):
            return value[1:-1]

        return value

    def compile_to_bytecode(self):
        if self.is_valid:
            for i, line in enumerate(self.file):
                line: str

                if line.startswith('/syn/'):
                    line = BINARY_SIGNATURE

                elif line.startswith('/end/'):
                    print(self.bytecode)
                    self.bytecode += convert('HALT')

                elif line.startswith('var/'):
                    # var/int/x/1

                    parts = line.split('/')
                    if len(parts) >= 3:
                        var_type = parts[1]
                        var_name = parts[2]
                        var_value = parts[3]

                        if var_type == 'int':
                            const_idx = self.add_const(var_value)
                            var_idx = self.add_var(var_name)

                            self.bytecode += convert('LOAD_CONST')
                            self.bytecode += bytes([const_idx])

                            self.bytecode += convert('STORE_VAR')
                            self.bytecode += bytes([var_idx])

                        elif var_type == 'str':
                            const_idx = self.add_const(
                                self.parse_string(parts[3]))

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
                        var_type = parts[1]
                        var_value = parts[2]

                        var_value = var_value.strip()
                        if var_value.startswith('(') and var_value.endswith(')'):
                            var_value = var_value[1:-1]

                        if var_type == 'int':
                            if var_value in self.variables:
                                var_idx = self.variables[var_value]

                                self.bytecode += convert('LOAD_VAR')
                                self.bytecode += bytes([var_idx])
                                self.bytecode += convert('PRINT')
                            else:

                                if '+' in var_value:
                                    left, right = var_value.split('+')
                                    self.emit_value(left)
                                    self.emit_value(right)

                                    self.bytecode += convert('ADD')
                                    self.bytecode += convert('PRINT')

                                elif '-' in var_value:
                                    left, right = var_value.split('-')
                                    self.emit_value(left)
                                    self.emit_value(right)

                                    self.bytecode += convert('SUB')
                                    self.bytecode += convert('PRINT')

                                elif '*' in var_value:
                                    left, right = var_value.split('*')
                                    self.emit_value(left)
                                    self.emit_value(right)

                                    self.bytecode += convert('MUL')
                                    self.bytecode += convert('PRINT')

                                elif '/' in var_value:
                                    left, right = var_value.split('/')
                                    self.emit_value(left)
                                    self.emit_value(right)

                                    self.bytecode += convert('DIV')
                                    self.bytecode += convert('PRINT')

                                else:
                                    Error.error(
                                        'SYN_003', var_value)

                        elif var_type == 'str':
                            self.emit_const_value(self.parse_string(var_value))
                            self.bytecode += convert('PRINT')

                        else:
                            Error.error(
                                'SYN_004', var_type)

                    else:
                        Error.error(
                            'SYN_003', 'Ensure if your varialbles follow this pattern: "return/type/value"')

                elif line.startswith('if/'):
                    # TODO: Add code controlers.
                    print('TODO: Add flux controlers.')

                elif line.startswith('func/'):
                    # func/func_name/params (future)
                    parts = line.split('/')
                    func_name = parts[1]
                    # params = parts[2]

                    self.bytecode += convert('FUNC')
                    self.functions[func_name] = i
                    self.bytecode += bytes(i)

                elif line.startswith('end/'):
                    # end/func_name
                    self.bytecode += convert('FUNC_END')

                elif line.startswith('call/'):
                    # call/func_name/params (future)
                    parts = line.split('/')
                    func_name = parts[1]
                    # params = parts[2]

                    self.bytecode += convert('CALL')
                    print(self.functions)
                    if func_name in self.functions:
                        self.bytecode += bytes(self.functions.get(func_name))
                    else:
                        Error.error('SYN_005', func_name)

                elif line == '':
                    line = convert('NOP')

                else:
                    Error.error('SYN_006', line)
