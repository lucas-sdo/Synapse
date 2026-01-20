from reader import *
from compiler import *
from errors import Error


def main():
    syn = Read('Synapse_compiler/exemplo.syn')
    result = Compiler(syn.return_content())
    return result


if __name__ == "__main__":
    main()
