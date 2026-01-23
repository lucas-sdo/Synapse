from errors import Error


class VirtualMachine:
    def __init__(self, bytecode, constants, var_count):
        self.bytecode = bytecode
        self.constants = constants
        self.vars = [None] * var_count
        self.stack = []
        self.ip = 0

    def run(self):
        while self.ip < len(self.bytecode):
            opcode = self.bytecode[self.ip]
            self.ip += 1

            if opcode == 64:  # LOAD_CONST
                idx = self.bytecode[self.ip]
                self.ip += 1
                self.stack.append(self.constants[idx])

            elif opcode == 81:  # STORE_VAR
                idx = self.bytecode[self.ip]
                self.ip += 1
                self.vars[idx] = self.stack.pop()

            elif opcode == 80:  # LOAD_VAR
                idx = self.bytecode[self.ip]
                self.ip += 1
                self.stack.append(self.vars[idx])

            elif opcode == 112:  # PRINT
                print(self.stack.pop())

            elif opcode == 32:  # ADD
                try:
                    idx = self.bytecode[self.ip]

                    b = self.stack.pop()
                    a = self.stack.pop()

                    result = int(a) + int(b)

                    self.stack.append(result)
                except ValueError:
                    Error.error('SYN_005', [a, b])

            elif opcode == 33:  # SUB
                try:
                    idx = self.bytecode[self.ip]

                    b = self.stack.pop()
                    a = self.stack.pop()

                    result = int(a) - int(b)

                    self.stack.append(result)
                except ValueError:
                    Error.error('SYN_005', [a, b])

            elif opcode == 34:  # MUL
                try:
                    idx = self.bytecode[self.ip]

                    b = self.stack.pop()
                    a = self.stack.pop()

                    result = int(a) * int(b)

                    self.stack.append(result)
                except ValueError:
                    Error.error('SYN_005', [a, b])

            elif opcode == 35:  # DIV
                try:
                    idx = self.bytecode[self.ip]

                    b = self.stack.pop()
                    a = self.stack.pop()

                    result = int(a) / int(b)

                    self.stack.append(result)
                except ValueError:
                    Error.error('SYN_005', [a, b])

            elif opcode == 0:  # HALT
                break

            # print(self.vars)
            # print(self.stack)
            # print(self.vars)
