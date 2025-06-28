from instructions import (
    hlt,
    mvi,
    mov,
    lda,
    sta,
    add,
    adi,
    sub,
    inr,
    dcr,
    jmp,
    jz,
    jnz,
    jc,
    jnc
)

class CPU8085:
    def __init__(self):
        # assigning values to general purpose registers 
        self.registers = {
            'A': 0x00,  # Accumulator
            'B': 0x00,
            'C': 0x00,
            'D': 0x00,
            'E': 0x00,
            'H': 0x00,
            'L': 0x00
        }
        
        # flags
        self.flags = {
            'S': 0,   # Sign flag
            'Z': 0,   # Zero flag
            'AC': 0,  # Auxiliary Carry flag
            'P': 0,   # Parity flag
            'CY': 0   # Carry flag
        }
        
        # specific purpose 16 bit numbers 
        self.PC = 0x0000 
        self.SP = 0xFFFF
        
        # creating memory(0x10000 i.e 65536 blocks of memory of 8 bit each initialised with 0x00 i.e 0)
        self.memory = [0x00]*0x10000 # 65536 = 64kb
        
        self.halted=False
        
    # method to update memory and PC according to a specific function
    def load_program(self, program, start_address=0x0000):  # default start address is 0x0000
        # program is a list of values that must be stored in memory according to the instructions
        for i, byte in enumerate(program):  # enumerate function gives index of an element and its data in a list
            self.memory[start_address + i] = byte
        self.PC = start_address  # Set PC to the start of the program
        
    # incrementing the PC to point to the next instruction
    def fetch_byte(self):
        byte = self.memory[self.PC]  # fetching opcode or the data in the PC
        self.PC = (self.PC + 1) & 0xFFFF # this ensures that the result is within 16 bit no. range
        return byte
        
    # method to fetch next instruction and execute it
    def execute_next(self):
        if self.halted:  # HLT
            return  
        opcode = self.fetch_byte()
        self.execute_instruction(opcode)
       
    # method to mark the termination or completion of an instruction 
    def execute_instruction(self, opcode):
        if opcode == 0x76:  # official 8085 opcode for HLT
            hlt(self)
        elif opcode in [0x3E, 0x06, 0x0E, 0x16, 0x1E, 0x26, 0x2E]:
            mvi(self, opcode)
        elif 0x40 <= opcode <= 0x7F and opcode != 0x76:
            mov(self, opcode)
        elif opcode == 0x3A:
            lda(self)
        elif opcode == 0x32:
            sta(self)
        elif 0x80 <= opcode <= 0x87:
            add(self, opcode)
        elif opcode == 0xC6:
            adi(self)
        elif 0x90 <= opcode <= 0x97:
            sub(self, opcode)
        elif opcode in [0x04, 0x0C, 0x14, 0x1C, 0x24, 0x2C, 0x34, 0x3C]:
            inr(self, opcode)
        elif opcode in [0x05, 0x0D, 0x15, 0x1D, 0x25, 0x2D, 0x35, 0x3D]:
            dcr(self, opcode)
        elif opcode == 0xC3:
            jmp(self)
        elif opcode == 0xCA:
            jz(self)
        elif opcode == 0xC2:
            jnz(self)
        elif opcode == 0xDA:
            jc(self)
        elif opcode == 0xD2:
            jnc(self)
        else:
            print(f"Unknown opcode: {hex(opcode)} at address {hex(self.PC - 1)}")