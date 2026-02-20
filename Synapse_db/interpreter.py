class Read:
    def __init__(self, sync_path):
        self.path = sync_path

    def read(self) -> list:
        with open(self.path, 'r', encoding='utf-8') as f:
            return [linha.strip() for linha in f if linha.strip()]


class Interpreter:
    def __init__(self, lines: list):
        self.lines: list = lines
        self.cols = dict()
        self.tabels = dict()

    def find_operation(self):
        for line in self.lines:
            line_parts = line.split('/', 2)

            match line_parts[0]:
                case 'col':
                    self.cols[line_parts[1]] = line_parts[2]
                case 'tab':
                    self.create_table(line_parts)
                case 'commit':
                    Writer(self.cols, self.tabels, line_parts).write_tables()
                case 'com':
                    pass

    def create_table(self, line: list):
        name = line[1]
        cols: str = line[2]
        if cols.startswith('(') and cols.endswith(')'):
            cols = cols[1:-1].split('/')

            col_buffer = []
            for col in cols:
                if col in self.cols:
                    col_buffer.append(col)
                else:
                    print("Here there will be a standardized error msg.")

            self.tabels[name] = col_buffer
        else:
            print("Here there will be a standardized error msg.")


class Writer:
    def __init__(self, cols: dict, tabs: dict, db_path: str):
        self.cols: dict = cols
        self.tabs: dict = tabs
        self.db_path: str = db_path
        self.type_codes = {
            "bool": b"\x01",
            "int": b"\x02",
            "float": b"\x03",
            "str": b"\x04",
        }

    def write_tables(self):
        print(self.cols)
        with open(self.db_path[2], "wb") as f:
            cols_to_write = b'\x2f\x73\x79\x6e\x2f\n'
            tabs_to_write = b''
            for col_name, col_type in self.cols.items():
                cols_to_write += col_name.encode('utf-8') + \
                    b"\x00" + self.type_codes[col_type] + b"\n"

            for tab_name, tab_cols in self.tabs.items():
                tabs_to_write += tab_name.encode('utf-8') + b'\x2f'
                for col in tab_cols:
                    tabs_to_write += col.encode('utf-8') + b'\x00'

            f.write(cols_to_write + tabs_to_write)


Interpreter(Read('Synapse_db/commands.sync').read()).find_operation()
