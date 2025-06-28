# displaying the status of registers
def print_registers(cpu):
    print("\n--- Registers ---")
    for reg in ['A', 'B', 'C', 'D', 'E', 'H', 'L']:
        print(f"{reg}: {hex(cpu.registers[reg])}")
    print(f"PC: {hex(cpu.PC)}")
    print(f"SP: {hex(cpu.SP)}")

# displaying the status of flags 
def print_flags(cpu):
    print("\n--- Flags ---")
    for flag in ['S', 'Z', 'AC', 'P', 'CY']:
        print(f"{flag}: {cpu.flags[flag]}")

# resetting all the memory blocks 
def clear_memory(cpu):
    cpu.memory = [0x00] * 0x10000
    print("\n--- Memory cleared ---")