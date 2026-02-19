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
                    Writer(self.cols, self.tabels).write_tables()
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
    def __init__(self, cols: dict, tabs: dict):
        self.cols: dict = cols
        self.tabs: dict = tabs
        pass

    def write_tables(self):
        print('Here will be the next part of the code =)')


Interpreter(Read('Synapse_db/commands.sync').read()).find_operation()
