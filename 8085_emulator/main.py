from cpu import CPU8085
from utils import print_registers,print_flags,clear_memory

def main():
    cpu = CPU8085()  #creating instance 
    
    # Sample program:
    program = [
        0x3E, 0x05,       # MVI A, 05
        0x06, 0x03,       # MVI B, 03
        0x80,             # ADD B
        0x32, 0x50, 0x30, # STA 3050H
        0x76              # HLT
    ]
    '''program = [
    0x3E, 0x0A,   # MVI A, 0A
    0x06, 0x05,   # MVI B, 05
    0x90,         # SUB B
    0x32, 0x50, 0x30,  # STA 3050
    0x76          # HLT
    ]'''
    # we have to write the opcodes according to the instruction

    cpu.load_program(program, start_address=0x0000)

    while not cpu.halted:
        cpu.execute_next()

    print("Final values of registers:")
    print_registers(cpu)
    print("\nFinal values of flags")
    print_flags(cpu)
    print(f"\nMemory[0x3050] = {hex(cpu.memory[0x3050])}")

if __name__ == "__main__":
    main()