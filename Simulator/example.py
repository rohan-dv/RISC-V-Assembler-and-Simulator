import sys

# Define instruction formats
r_type_instructions = {
    "0110011": {
        "000": {"0000000": "add", "0100000": "sub"},
        "001": {"0000000": "sll"},
        "010": {"0000000": "slt"},
        "011": {"0000000": "sltu"},
        "100": {"0000000": "xor"},
        "101": {"0000000": "srl", "0100000": "sra"},
        "110": {"0000000": "or"},
        "111": {"0000000": "and"}
    }
}

i_type_instructions = {
    "0000011": {"010": "lw"},
    "0010011": {"000": "addi"},
    "1100111": {"000": "jalr"}
}

s_type_instructions = {
    "0100011": {"010": "sw"}
}

b_type_instructions = {
    "1100011": {
        "000": "beq",
        "001": "bne",
    }
}

j_type_instructions = {
    "1101111": "jal"
}

# Initialize registers and memory
registers = [0] * 32
memory = {i: 0 for i in range(32)}  # 32x32-bit memory
program_counter = 0

def decode_instruction(instruction):
    opcode = instruction[25:32]
    if opcode in r_type_instructions:
        func3 = instruction[17:20]
        func7 = instruction[0:7]
        if func3 in r_type_instructions[opcode]:
            if func7 in r_type_instructions[opcode][func3]:
                return r_type_instructions[opcode][func3][func7]
    elif opcode in i_type_instructions:
        func3 = instruction[17:20]
        if func3 in i_type_instructions[opcode]:
            return i_type_instructions[opcode][func3]
    elif opcode in s_type_instructions:
        func3 = instruction[17:20]
        if func3 in s_type_instructions[opcode]:
            return s_type_instructions[opcode][func3]
    elif opcode in b_type_instructions:
        func3 = instruction[17:20]
        if func3 in b_type_instructions[opcode]:
            return b_type_instructions[opcode][func3]
    elif opcode in j_type_instructions:
        return j_type_instructions[opcode]
    return "unknown"

def execute_instruction(instruction):
    # Placeholder for instruction execution logic
    global program_counter
    program_counter += 4  # Increment program counter by 4 (assuming 4-byte instructions)

def write_registers(outfile):
    outfile.write(f"0b{format(program_counter, '032b')} ")
    outfile.write(" ".join(f"0b{format(reg, '032b')}" for reg in registers) + "\n")

def write_memory(outfile):
    address = 0x00010000
    for i in range(32):
        outfile.write(f"0x{format(address, '08X')}: 0b{format(memory[i], '032b')}\n")
        address += 4

def main():
    if len(sys.argv) != 3:
        print("Usage: python Simulator.py <input_file> <output_file>")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        with open(input_file, "r") as infile, open(output_file, "w") as outfile:
            for line in infile:
                binary_instruction = line.strip()
                decoded = decode_instruction(binary_instruction)
                execute_instruction(binary_instruction)  # Update registers and memory
                write_registers(outfile)

            # Write memory contents after Virtual Halt
            write_memory(outfile)

    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
    # Add helper function to parse binary instruction into fields
    def parse_instruction(instruction):
        return {
            "opcode": instruction[25:32],
            "rd": int(instruction[20:25], 2),
            "func3": instruction[17:20],
            "rs1": int(instruction[12:17], 2),
            "rs2": int(instruction[7:12], 2),
            "func7": instruction[0:7],
            "imm": int(instruction[0:12], 2) if instruction[0] == '0' else -((1 << 12) - int(instruction[0:12], 2))
        }
