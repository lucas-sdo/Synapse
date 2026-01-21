from reader import *
from compiler import *
from errors import Error
from vm import *


def main():
    syn = Read('Synapse_compiler/exemplo.syn')
    result = Compiler(syn.return_content())

    vm = VirtualMachine(
        bytecode=result.bytecode,
        constants=result.constants,
        var_count=len(result.variables)
    )
    print("BYTECODE FINAL:", result.bytecode)
    print("CONSTANTS:", result.constants)
    print("VARS:", result.variables)
    vm.run()
    return result


if __name__ == "__main__":
    main()
