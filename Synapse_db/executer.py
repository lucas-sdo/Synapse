class Read:
    def __init__(self, sync_path):
        self.path = sync_path

    def read(self) -> list:
        with open(self.path, 'r', encoding='utf-8') as f:
            return [linha.strip() for linha in f if linha.strip()]


class Executer:
    def __init__(self, lines: list):
        self.current_id: int = 1
        self.lines: list = lines
        self.info_to_write = b''
        self.cols = dict()
        self.tabels = dict()

    def execute(self):
        for line in self.lines:
            line_parts = line.split('/', 2)

            match line_parts[0]:
                case 'col':
                    self.cols[line_parts[1]] = line_parts[2]
                case 'tab':
                    self.create_table(line_parts)
                    self.info_to_write += Writer(
                        self.cols, self.tabels, self.current_id).write_building()
                case 'commit':
                    with open(line_parts[2], "wb") as f:
                        f.write(self.info_to_write)
                case 'add':
                    self.info_to_write += Writer(self.cols, self.tabels,
                                                 self.current_id).write_info(line_parts)
                    self.current_id += 1
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
    def __init__(self, cols: dict, tabs: dict, current_id: int):
        self.current_id: int = current_id
        self.cols: dict = cols
        self.tabs: dict = tabs
        self.type_codes = {
            "bool": b"\x01",
            "int": b"\x02",
            "float": b"\x03",
            "str": b"\x04",
            "id": b"\x05",
        }

    def write_building(self):
        cols_to_write = b'\x2f\x73\x79\x6e\x2f\n'
        tabs_to_write = b''
        for col_name, col_type in self.cols.items():
            cols_to_write += col_name.encode('utf-8') + \
                b"\x00" + self.type_codes[col_type] + b"\n"

        for tab_name, tab_cols in self.tabs.items():
            tabs_to_write += tab_name.encode('utf-8') + b'\x2f'
            for col in tab_cols:
                tabs_to_write += col.encode('utf-8') + b'\x00'
            tabs_to_write += b"\n"
        return cols_to_write + tabs_to_write

    def write_info(self, line_parts):
        table = line_parts[1]
        info = line_parts[2]
        if info.startswith('(') and info.endswith(')'):
            info = info[1:-1].split('/')
            row_to_write = b'\x72\x6f\x77\x2f' + \
                table.encode('utf-8') + b'\x2f' + \
                self.current_id.to_bytes() + b'\x00'
            for info_aux in info:
                row_to_write += info_aux.encode('utf-8') + b'\x00'
            row_to_write += b'\n'
            return row_to_write
        else:
            print("Here there will be a standardized error msg.")


Executer(Read('Synapse_db/commands.sync').read()).execute()
