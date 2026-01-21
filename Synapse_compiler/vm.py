import convert


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
                print(">>> PRINT OPCODE EXECUTADO")
                print(self.stack.pop())

            elif opcode == 0:  # HALT
                break
