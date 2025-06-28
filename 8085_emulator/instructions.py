# flag updater
def update_flags_arithmetic(cpu, result):
    cpu.flags['Z'] = int(result == 0)
    cpu.flags['S'] = int((result & 0x80) != 0)
    cpu.flags['P'] = int(bin(result & 0xFF).count('1') % 2 == 0)
    cpu.flags['CY'] = int(result > 0xFF)

# function to implement HLT
def hlt(cpu):
    cpu.halted = True
    print("HLT encountered. CPU halted.\n")

# mapping 8085 opcodes to MVI targets
mvi_opcodes = {
    0x3E: 'A',
    0x06: 'B',
    0x0E: 'C',
    0x16: 'D',
    0x1E: 'E',
    0x26: 'H',
    0x2E: 'L'
}

# function to implement MVI instruction
def mvi(cpu, opcode):
    if opcode in mvi_opcodes:
        reg = mvi_opcodes[opcode]
        data = cpu.fetch_byte()
        cpu.registers[reg] = data
        print(f"MVI {reg}, {hex(data)} executed. {reg} = {hex(data)}")
    else:
        print(f"Invalid MVI opcode: {hex(opcode)}")

# in 8085 every register have values assigned between 000 to 111(3 bit binary)
register_codes = ['B', 'C', 'D', 'E', 'H', 'L', 'M', 'A']

# method to implement MOV instruction
def mov(cpu, opcode):
    # the opcode of MOV is in form of 01xxxxxx (01 always for MOV next 3 bits for destination  and last 3 for source)
    dst_code = (opcode >> 3) & 0b111 
    src_code = opcode & 0b111
    
    dst = register_codes[dst_code]
    src = register_codes[src_code]
    
    cpu.registers[dst] = cpu.registers[src]
    print(f"MOV {dst}, {src} executed. {dst} = {hex(cpu.registers[dst])}")

# method to implement LDA instruction    
def lda(cpu):
    # 16 address gets stored in following form : lower byte gets stored and higher byte then gets stored in next block after updation of PC
    low = cpu.fetch_byte()  # reads lower byte
    high = cpu.fetch_byte()  # reads higher byte
    address = (high << 8) | low
    cpu.registers['A'] = cpu.memory[address]
    print(f"LDA {hex(address)} executed. A = {hex(cpu.registers['A'])}")

# method to implement STA instruction
def sta(cpu):
    low = cpu.fetch_byte()
    high = cpu.fetch_byte()
    address = (high << 8) | low
    cpu.memory[address] = cpu.registers['A']
    print(f"STA {hex(address)} executed. Memory[{hex(address)}] = {hex(cpu.registers['A'])}")

# method to implement ADD
def add(cpu, opcode):
    src_code = opcode & 0b111  # wrapping to 3 bit binary
    src = register_codes[src_code]

    if src == 'M':
        address = (cpu.registers['H'] << 8) | cpu.registers['L']  #lower byte is H and higher one is L
        value = cpu.memory[address]
    else:
        value = cpu.registers[src]

    result = cpu.registers['A'] + value
    update_flags_arithmetic(cpu, result)
    cpu.registers['A'] = result & 0xFF  # wrapping to 8bit
    print(f"ADD {src} executed. A = {hex(cpu.registers['A'])}")

# method to implement ADI
def adi(cpu):
    value = cpu.fetch_byte()
    result = cpu.registers['A'] + value
    update_flags_arithmetic(cpu, result)
    cpu.registers['A'] = result & 0xFF
    print(f"ADI {hex(value)} executed. A = {hex(cpu.registers['A'])}")

# method to implement SUB
def sub(cpu, opcode):
    src_code = opcode & 0b111
    src = register_codes[src_code]

    if src == 'M':
        addr = (cpu.registers['H'] << 8) | cpu.registers['L']
        value = cpu.memory[addr]
    else:
        value = cpu.registers[src]

    result = cpu.registers['A'] - value
    update_flags_arithmetic(cpu, result)
    cpu.registers['A'] = result & 0xFF
    print(f"SUB {src} executed. A = {hex(cpu.registers['A'])}")

# method to implement INR
def inr(cpu, opcode):
    code = (opcode >> 3) & 0b111
    reg = register_codes[code]
    
    result = cpu.registers[reg] + 1
    cpu.registers[reg] = result & 0xFF
        
    update_flags_arithmetic(cpu, result)
    print(f"INR {reg} executed.")
    
# method to implement DCR
def dcr(cpu, opcode):
    code = (opcode >> 3) & 0b111
    reg = register_codes[code]

    result = cpu.registers[reg] - 1
    cpu.registers[reg] = result & 0xFF

    update_flags_arithmetic(cpu, result)
    print(f"DCR {reg} executed.")


# method to implement JUMP instructions
def jmp(cpu):
    low = cpu.fetch_byte()
    high = cpu.fetch_byte()
    addr = (high << 8) | low
    cpu.PC = addr
    print(f"JMP to {hex(addr)}")

def jz(cpu):
    low = cpu.fetch_byte()
    high = cpu.fetch_byte()
    addr = (high << 8) | low
    if cpu.flags['Z'] == 1:
        cpu.PC = addr
        print(f"JZ taken to {hex(addr)}")
    else:
        print(f"JZ not taken")

def jnz(cpu):
    low = cpu.fetch_byte()
    high = cpu.fetch_byte()
    addr = (high << 8) | low
    if cpu.flags['Z'] == 0:
        cpu.PC = addr
        print(f"JNZ taken to {hex(addr)}")
    else:
        print(f"JNZ not taken")

def jc(cpu):
    low = cpu.fetch_byte()
    high = cpu.fetch_byte()
    addr = (high << 8) | low
    if cpu.flags['CY'] == 1:
        cpu.PC = addr
        print(f"JC taken to {hex(addr)}")
    else:
        print(f"JC not taken")

def jnc(cpu):
    low = cpu.fetch_byte()
    high = cpu.fetch_byte()
    addr = (high << 8) | low
    if cpu.flags['CY'] == 0:
        cpu.PC = addr
        print(f"JNC taken to {hex(addr)}")
    else:
        print(f"JNC not taken")