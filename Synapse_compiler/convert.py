from errors import Error


def convert(nickname):
    dictionary = {
        'HALT': b'\x00',
        'NOP': b'\x01',
        'LOAD_VAR': b'\x50',
        'STORE_VAR': b'\x51',
        'PRINT': b'\x70',
        'INPUT': b'\x71',
        'TYPEOF': b'\x80',

        'EQ': b'\x30',
        'NE': b'\x31',

        'POP': b'\x11',
        'DIV': b'\x23',
        'MUL': b'\x22',
        'SUB': b'\x21',
        'ADD': b'\x20',

        'LOAD_CONST': b'\x40',
    }

    if nickname in dictionary:
        return dictionary[nickname]
    else:
        Error.error('SYN_004', f"Instrução desconhecida: '{nickname}'")
        return b'0x00'
