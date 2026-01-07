---

# RISC-V Assembler and Simulator

This project provides a comprehensive **RISC-V Assembler and Simulator** built in Python. It is designed to bridge the gap between human-readable assembly language and hardware-level execution, making it an ideal tool for students and hobbyists learning about computer architecture and the RISC-V ISA.

---

## Features

### 🛠 Assembler

* **Binary Conversion:** Translates RISC-V assembly into standard 32-bit machine code.
* **Label Resolution:** Implements a two-pass system to handle labels for jumps (`jal`) and branches (B-type).
* **Validation:** Performs syntax checking for instruction mnemonics and register naming (e.g., `x0` through `x31`).
* **Immediate Handling:** Automatically manages two’s complement conversion for signed decimal and hexadecimal values.

### 💻 Simulator

* **Virtual CPU:** Simulates a 32-bit RISC-V processor including the Program Counter (PC) and a 32-register file.
* **Memory Management:** Simulates a dedicated memory space for data storage and retrieval (`lw`/`sw`).
* **Execution Tracking:** Outputs the state of all registers after every instruction cycle to help with debugging.
* **Hardware Integrity:** Hardwires the `x0` register to zero, ensuring architectural compliance.

---

## Supported Instructions

The following instructions are implemented according to the RISC-V RV32I Base Integer Instruction Set:

| Type | Instructions |
| --- | --- |
| **R-Type** | `add`, `sub`, `slt`, `srl`, `or`, `and` |
| **I-Type** | `addi`, `lw`, `jalr` |
| **S-Type** | `sw` |
| **B-Type** | `beq`, `bne`, `blt` |
| **J-Type** | `jal` |

---

## How to Run

### 1. Assembler (Interactive Mode)

The Assembler is designed for interactive use. It will prompt you for the input file path once it starts.

1. Open your terminal and run:
```bash
python assembler.py

```


2. When the prompt appears, enter the name of your assembly file (e.g., `test.asm`).
3. The program will generate a binary output file containing the 32-bit machine code.

### 2. Simulator (Command Line Interface)

The Simulator is a non-interactive tool that accepts input and output paths via command-line arguments. **It will not prompt for input.**

1. Run the simulator using the following syntax:
```bash
python simulator.py <input_binary_file> <output_state_file>

```


2. **Example:**
```bash
python simulator.py binary.txt state_output.txt

```



---

## Project Structure

* `assembler.py`: The Python logic for parsing text and generating binary.
* `simulator.py`: The logic for the virtual CPU and memory execution.
* `assets/`: Suggested directory for storing your `.asm` test files.

---
