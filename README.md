# Python Assembly-x86-Decompiler


## Introduction
This project is a Python-based decompiler for disassembling binary executable files. The decompiler translates assembly instructions back into human-readable assembly code. This tool can be useful for understanding the behavior of binary executables, especially when source code is unavailable.

## Project Details

### File Information
- **File**: `decompiler_asm.py`
- **Author**: Elhanan Haenel
- **Description**: A Python script that decompiles binary executable files into assembly language instructions.
- **Notes**: This project was developed as a personal challenge to create a functional decompiler in Python.

### Functionality
The decompiler includes the following features:
1. **Instruction Decoding**: Decodes various x86 assembly instructions.
2. **Binary Parsing**: Reads binary executable files byte by byte.
3. **Output Generation**: Writes the disassembled instructions to an output text file.

## Development Environment

### Tools and Software
- **Development Environment**: Any text editor or IDE that supports Python.
- **Python Version**: Python 2.7
- **Dependencies**: No external dependencies are required for this project.

### How to Run

### Prerequisites
- Ensure you have Python 2.7 installed on your system.

### Installation
1. Clone or download the repository containing `decompiler_asm.py`.
2. Place the `decompiler_asm.py` file in your working directory.

### Running the Program
1. Open a terminal or command prompt.
2. Navigate to the directory containing `decompiler_asm.py`:
   ```sh
   cd [your-directory]
   ```
3. Run the decompiler script:
   ```sh
   python decompiler_asm.py [path_to_binary_file]
   ```
   Replace `[path_to_binary_file]` with the path to the binary executable file you want to decompile.

### Usage
- The decompiler will generate an output file named `main.txt` in the same directory. This file will contain the disassembled assembly instructions.

## Acknowledgements
- **Instructor and Course Staff**: For guidance and support throughout the project.

## Contact
For any questions or further information, please contact Elhanan.

