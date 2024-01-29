from assembler import *

def main():
    #replace with your files
    inputname = "filename.asm"
    outputname = "filename.hack"

    parser = Parser(inputname)
    code = Code()
    symbol_table = SymbolTable()

    # First pass
    rom_address = 0
    while parser.hasMoreLines():
        parser.advance()
        if parser.instructionType() == 'L-instruction':
            symbol = parser.symbol()
            if not symbol_table.contains(symbol):
                symbol_table.addEntry(symbol, rom_address)
        elif parser.instructionType() in ['A-instruction', 'C-instruction']:
            rom_address += 1

    
    parser.file.seek(0)

    # second pass 
    binary_code = []
    while parser.hasMoreLines():
        parser.advance()
        instruction_type = parser.instructionType()
        if instruction_type == 'A-instruction':
            symbol = parser.symbol()
            if symbol.isdigit():
                address = int(symbol)
            else:
                if not symbol_table.contains(symbol):
                    symbol_table.addEntry(symbol)
                address = symbol_table.getAddress(symbol)
            binary_instruction = '0' + format(address, '015b')
        elif instruction_type == 'C-instruction':
            comp_mnemonic = parser.comp()
            dest_mnemonic = parser.dest()
            jump_mnemonic = parser.jump()
            binary_instruction = '111' + code.comp(comp_mnemonic) + code.dest(dest_mnemonic) + code.jump(jump_mnemonic)
        else:
            continue
        binary_code.append(binary_instruction)

    # Write the binary code to the output file
    with open(outputname, 'w') as output_file:
        for line in binary_code:
            output_file.write(line + '\n')

    parser.close()

if __name__ == '__main__':
    main()
