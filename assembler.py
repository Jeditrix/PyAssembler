import re

class Parser:
    def __init__(self, filepath):
        try:
            self.file = open(filepath, 'r')
            self.current_line = ''
        except FileNotFoundError:
            print(f"File {filepath} not found.")
            exit(1)

    def hasMoreLines(self) -> bool:
        position = self.file.tell()
        line = self.file.readline()
        self.file.seek(position)
        return bool(line)

    def advance(self):
        self.current_line = self.file.readline()
        self.current_line = re.sub(r'//.*', '', self.current_line).strip()

    def instructionType(self):
        if self.current_line.startswith('@'):
            return 'A-instruction'
        elif self.current_line.startswith('('):
            return 'L-instruction'
        elif self.current_line:
            return 'C-instruction'
        return None

    def symbol(self):
        if self.instructionType() == 'A-instruction':
            return self.current_line[1:]
        elif self.instructionType() == 'L-instruction':
            return self.current_line[1:-1]
        return None

    def dest(self):
        if self.instructionType() == 'C-instruction':
            parts = self.current_line.split('=')
            return parts[0] if len(parts) > 1 else 'null'
        return None

    def comp(self):
        if self.instructionType() == 'C-instruction':
            parts = self.current_line.split(';')[0]
            parts = parts.split('=')[1] if '=' in parts else parts
            return parts
        return None

    def jump(self):
        if self.instructionType() == 'C-instruction':
            parts = self.current_line.split(';')
            return parts[1] if len(parts) > 1 else 'null'
        return None

    def close(self):
        self.file.close()


class Code:
    def __init__(self):
        self.dest_table = {"null": "000", "M": "001", "D": "010", "MD": "011", "A": "100", "AM": "101", "AD": "110", "AMD": "111"}
        self.comp_table = {"0": "0101010", "1": "0111111", "-1": "0111010", "D": "0001100", "A": "0110000", "!D": "0001101", "!A": "0110001", "-D": "0001111", "-A": "0110011", "D+1": "0011111", "A+1": "0110111", "D-1": "0001110", "A-1": "0110010", "D+A": "0000010", "D-A": "0010011", "A-D": "0000111", "D&A": "0000000", "D|A": "0010101", "M": "1110000", "!M": "1110001", "-M": "1110011", "M+1": "1110111", "M-1": "1110010", "D+M": "1000010", "D-M": "1010011", "M-D": "1000111", "D&M": "1000000", "D|M": "1010101"}
        self.jump_table = {"null": "000", "JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}

    def dest(self, mnemonic):
        return self.dest_table.get(mnemonic, "000")

    def comp(self, mnemonic):
        return self.comp_table.get(mnemonic, "0101010")

    def jump(self, mnemonic):
        return self.jump_table.get(mnemonic, "000")


class SymbolTable:
    def __init__(self):
        self.table = {
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
            "R0": 0,
            "R1": 1,
            "R2": 2,
            "R3": 3,
            "R4": 4,
            "R5": 5,
            "R6": 6,
            "R7": 7,
            "R8": 8,
            "R9": 9,
            "R10": 10,
            "R11": 11,
            "R12": 12,
            "R13": 13,
            "R14": 14,
            "R15": 15,
            "SCREEN": 16384,
            "KBD": 24576
        }
        self.next_available_address = 16

    def addEntry(self, symbol, address=None):
        if address is not None:
            self.table[symbol] = address
        else:
            self.table[symbol] = self.next_available_address
            self.next_available_address += 1

    def contains(self, symbol):
        return symbol in self.table

    def getAddress(self, symbol):
        return self.table.get(symbol, None)

