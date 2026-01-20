from errors import Error


def convert(nickname):
    dictionary = {
        'HALT': b'0x00',
        'NOP': b'0x01',
        'LOAD_VAR': b'0x50',
        'STORE_VAR': b'0x51',
        'PRINT': b'0x70',
        'INPUT': b'0x71',
        'TYPEOF': b'0x80',

        'EQ': b'0x30',
        'NE': b'0x31',

        'POP': b'0x11',
        'DIV': b'0x23',
        'MUL': b'0x22',
        'SUB': b'0x21',
        'ADD': b'0x20',

        'LOAD_CONST': b'0x40',
    }

    if nickname in dictionary:
        return dictionary[nickname]
    else:
        Error.error('SYN_004', f"Instrução desconhecida: '{nickname}'")
        return b'0x00'
