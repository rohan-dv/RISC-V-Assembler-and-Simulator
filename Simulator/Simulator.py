import sys

r_type_instructions = {
    "0110011": {
        "000": {"0000000": "add", "0100000": "sub"},
        "010": {"0000000": "slt"},
        "101": {"0000000": "srl"},
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

registers = [0] * 32
registers[0] = 0  
registers[2] = 380
memory = {i: 0 for i in range(32)}  
program_counter = 0

def decimal_binary(n):
    sum=0
    pow=1
    while n>0:
        a= n%2
        q=n//2
        sum+=pow*a
        n=q
        pow=pow*10
    return sum

def binary_decimal(n):
    return int(n, 2)

def parse_instruction(instruction):
    if instruction[25:32] in r_type_instructions:    
        return {
            "opcode": instruction[25:32],
            "rd": int(instruction[20:25], 2),
            "func3": instruction[17:20],
            "rs1": int(instruction[12:17], 2),
            "rs2": int(instruction[7:12], 2),
            "func7": instruction[0:7],
        }
    
    elif instruction[25:32] in i_type_instructions:
        imm = int(instruction[0:12], 2)
        if instruction[0] == '1':
            imm = imm - (1 << 12)
        return {
            "opcode": instruction[25:32],
            "rd": int(instruction[20:25], 2),
            "func3": instruction[17:20],
            "rs1": int(instruction[12:17], 2),
            "imm": imm,
        }
    elif instruction[25:32] in s_type_instructions:
        imm = (int(instruction[0:7], 2) << 5) | int(instruction[20:25], 2)
        return {
            "opcode": instruction[25:32],
            "func3": instruction[17:20],
            "rs1": int(instruction[12:17], 2),
            "rs2": int(instruction[7:12], 2),
            "imm": imm,
        }
    elif instruction[25:32] in b_type_instructions:
        imm = instruction[24] + instruction[0] + instruction[1:7] + instruction[20:24] + "0"
        imm = int(imm, 2)
        # print(imm)
        if imm & (1 << 12):  
            imm -= (1 << 13)
        return {
            "opcode": instruction[25:32],
            "func3": instruction[17:20],
            "rs1": int(instruction[12:17], 2),
            "rs2": int(instruction[7:12], 2),
            "imm": imm,
        }
    elif instruction[25:32] in j_type_instructions:
        imm = (int(instruction[0], 2) << 20) | (int(instruction[1:11], 2) << 1) | (int(instruction[11], 2) << 11) | (int(instruction[12:20], 2) << 12)
        if instruction[0] == '1':
            imm = imm - (1 << 21)
        return {
            "opcode": instruction[25:32],
            "rd": int(instruction[20:25], 2),
            "imm": imm,
        }
    
    else:
        raise Exception("Invalid instruction")



def execute_instruction(instruction):
    global program_counter
    fields = parse_instruction(instruction)
    opcode = fields["opcode"]

    if opcode in r_type_instructions:
        func3 = fields["func3"]
        func7 = fields["func7"]
        if func3 in r_type_instructions[opcode] and func7 in r_type_instructions[opcode][func3]:
            operation = r_type_instructions[opcode][func3][func7]
            if operation == "add":
                registers[fields["rd"]] = registers[fields["rs1"]] + registers[fields["rs2"]]
            elif operation == "sub":
                registers[fields["rd"]] = registers[fields["rs1"]] - registers[fields["rs2"]]
            elif operation == "slt":
                registers[fields["rd"]] = 1 if registers[fields["rs1"]] < registers[fields["rs2"]] else 0
            elif operation == "srl":
                registers[fields["rd"]] = registers[fields["rs1"]] >> registers[fields["rs2"]]
            elif operation == "or":
                registers[fields["rd"]] = registers[fields["rs1"]] | registers[fields["rs2"]]
            elif operation == "and":
                registers[fields["rd"]] = registers[fields["rs1"]] & registers[fields["rs2"]]
            else:
                raise Exception("Invalid instruction")
        else:
            raise Exception("Invalid instruction")
            

    elif opcode in i_type_instructions:
        func3 = fields["func3"]
        if func3 in i_type_instructions[opcode]:
            operation = i_type_instructions[opcode][func3]
            if operation == "addi":
                registers[fields["rd"]] = registers[fields["rs1"]] + fields["imm"]
            elif operation == "lw":
                address = registers[fields["rs1"]] + fields["imm"]
                temp_add = (address % 65536)//4
                registers[fields["rd"]] = memory.get(temp_add,0)
            elif operation == "jalr":
                temp = program_counter + 4
                program_counter = (registers[fields["rs1"]] + fields["imm"]) & ~1
                registers[fields["rd"]] = temp
                registers[0] = 0
                return  
            else:
                raise Exception("Invalid instruction")
        else:
            raise Exception("Invalid instruction")

    elif opcode in s_type_instructions:
        func3 = fields["func3"]
        if func3 in s_type_instructions[opcode]:
            operation = s_type_instructions[opcode][func3]
            if operation == "sw":
                address = registers[fields["rs1"]] + fields["imm"]
                temp_add = (address % 65536)//4
                memory[temp_add] = registers[fields["rs2"]]
            else:
                raise Exception("Invalid instruction")
        else:
            raise Exception("Invalid instruction")

    elif opcode in b_type_instructions:
        func3 = fields["func3"]
        if func3 in b_type_instructions[opcode]:
            operation = b_type_instructions[opcode][func3]
            if operation == "beq":
                if registers[fields["rs1"]] == registers[fields["rs2"]]:
                    program_counter += fields["imm"]
                    registers[0] = 0
                    return  
            elif operation == "bne":
                # print("he")
                if registers[fields["rs1"]] != registers[fields["rs2"]]:
                    program_counter += fields["imm"]
                    registers[0] = 0
                    return 
            else:
                raise Exception("Invalid instruction")  
        else:
            raise Exception("Invalid instruction")

    elif opcode in j_type_instructions:
        operation = j_type_instructions[opcode]
        if operation == "jal":
            registers[fields["rd"]] = program_counter + 4
            program_counter += fields["imm"]
            registers[0] = 0
            return
        else:
            raise Exception("Invalid instruction")

    else:
        raise Exception("Invalid instruction")  
        
    registers[0] = 0
    program_counter += 4  

def to_twos_complement(value, bits=32):
    """Convert a signed integer to its 2's complement binary representation."""
    if value < 0:
        value = (1 << bits) + value
    return format(value, f'0{bits}b')

def write_registers(outfile, decimal_outfile=None):
    outfile.write(f"0b{to_twos_complement(program_counter)} ")
    outfile.write(" ".join(f"0b{to_twos_complement(reg)}" for reg in registers) + "\n")
    if decimal_outfile:
        decimal_outfile.write(f"{program_counter} ")
        decimal_outfile.write(" ".join(str(binary_decimal(to_twos_complement(reg))) for reg in registers) + "\n")

def write_memory(outfile, decimal_outfile=None):
    address = 0x00010000
    for i in range(32):
        outfile.write(f"0x{format(address, '08X')}:0b{to_twos_complement(memory[i])}\n")
        if decimal_outfile:
            decimal_outfile.write(f"0x{format(address, '08X')}:{str(binary_decimal(to_twos_complement(memory[i])))}\n")
        address += 4


def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    output_decimal = output_file.replace(".txt", "_r.txt")

    intput_arr = []
    n = 0

    counter = program_counter // 4

    try:
        with open(input_file, "r") as infile:
            for line in infile:
                binary_instruction = line.strip()
                intput_arr.append(binary_instruction)
                n += 1
            
        with open(output_file, "w") as outfile, open(output_decimal, "w") as decimal_outfile:
            previous_program_counter = -1 
            while counter < n:
                binary_instruction = intput_arr[counter]
                execute_instruction(binary_instruction) 
                write_registers(outfile, decimal_outfile) 
                counter = program_counter // 4  

                if program_counter == previous_program_counter or binary_instruction == "00000000000000000000000001100011":
                    break
                previous_program_counter = program_counter 
            write_memory(outfile, decimal_outfile)

    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

main()
