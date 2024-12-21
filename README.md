# Pipeline Simulator

This project implements a simple MIPS-like pipeline simulator to execute assembly-like instructions. It supports instruction fetch, decode, execute, memory access, and write-back stages, including forwarding and stalling mechanisms for handling hazards.

## Features

- Simulates a 5-stage MIPS pipeline:
  - Instruction Fetch (IF)
  - Instruction Decode (ID)
  - Execution (EX)
  - Memory Access (MEM)
  - Write Back (WB)
- Implements forwarding to resolve data hazards.
- Handles stalls for unresolved hazards such as load-use hazards.
- Includes a memory and register dump for debugging.
- Flexible input file handling via command-line arguments.

## Requirements

- Python 3.7 or above

### Python Libraries

The project requires no additional third-party libraries. All functionality is implemented using Python's standard library.

## Installation

Clone the repository:
   ```bash
   git clone <repository_url>
   cd mips-simulator
   ```

## Usage

Run the pipeline simulator with the desired input file:

```bash
python src/main.py <input_file_path>
```

### Example:

```bash
python src/main.py input/test6.txt
```

## Input Format

The input file should contain assembly-like instructions in the following format:

```
add $1, $2, $3
sub $4, $5, $6
lw $7, 4($8)
sw $9, 8($10)
beq $11, $12, label
```

## Pipeline Execution

The pipeline simulator processes instructions in cycles. At each cycle, it performs the following operations:

1. Write Back (WB)
2. Memory Access (MEM)
3. Execution (EX)
4. Instruction Decode (ID)
5. Instruction Fetch (IF)

### Forwarding

The simulator implements forwarding to resolve hazards:

- Data hazards between EX/MEM and ID/EX stages.
- Support for `add`, `sub`, `beq`, `lw`, and `sw` instructions.

### Stalling

The simulator inserts stalls for unresolved hazards, such as:

- Load-use hazards when a `lw` instruction's result is needed in the next instruction.
- Branch hazards when encountering dependencies with `lw` or other preceding instructions.

## Debugging

Enable debugging to inspect pipeline registers and memory state during execution:

1. Toggle `debug_reg_mem` or `debug_pipeline_reg` flags in `PipelineSimulator`:
   ```python
   pipeline = PipelineSimulator(instruct_memory, debug_reg_mem=True, debug_pipeline_reg=True)
   ```

2. Use the `dump()` method to inspect pipeline register states:
   ```python
   pipeline.dump()
   ```

## Project Structure

```
.
├── input/                   # Input files with assembly-like instructions
├── src/
│   ├── memory.py            # Memory class implementation
│   ├── instructions.py      # All support instructions
│   ├── pipeline.py          # Pipeline simulator and register classes
│   ├── registers.py         # Registers used for data
│   ├── PipelineRegister.py  # Registers used in Pipeline
│   ├── main.py              # Entry point for running the simulator
└── README.md                # Project documentation
```


## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

Feel free to report issues or suggest improvements!

Hope I can graduate successfully!


