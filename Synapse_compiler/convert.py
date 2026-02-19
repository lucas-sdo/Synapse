from errors import Error


def convert(nickname):
    dictionary = {
        'HALT': b'\x00',
        'NOP': b'\x01',
        'RET': b'\x02',

        'PUSH': b'\x10',
        'POP': b'\x11',

        'LOAD_VAR': b'\x50',
        'STORE_VAR': b'\x51',

        'PRINT': b'\x70',
        'INPUT': b'\x71',
        'TYPEOF': b'\x80',

        'EQ': b'\x30',
        'NE': b'\x31',

        'ADD': b'\x20',
        'SUB': b'\x21',
        'MUL': b'\x22',
        'DIV': b'\x23',

        'EQ': b'\x30',
        'NE': b'\x31',
        'LT': b'\x32',
        'GT': b'\x33',

        'JMP': b'\x40',
        'JMP_IF_TRUE': b'\x41',
        'JMP_IF_FALSE': b'\x42',

        'LOAD_CONST': b'\x40',

        'FUNC': b'\x60',
        'CALL': b'\x61',
        'FUNC_END': b'\x62',
    }

    if nickname in dictionary:
        return dictionary[nickname]
    else:
        Error.error('SYN_004', f"Instrução desconhecida: '{nickname}'")
        return b'0x00'
