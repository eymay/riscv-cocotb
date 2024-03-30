# riscv_cocotb

RISC-V unit testing for instructions with Python based on Cocotb. This project provides an easy to use API to customize tests for your RISC-V core. The tests are aimed to monitor the inner signals of modules to provide rich error information to hardware developers.

The final goal is to support all instructions in RV32I base instruction set. Currently all Register-Register and Register-Immediate instructions are supported.

Tests can be generated for your architecture with minimal configuration. Enter the instantiation names of your modules as such:
```python
from riscv_cocotb.unit_test_instrs import generate_tests_for_type, RTypeInstr, ITypeInstr
from riscv_cocotb.instr_types import Arch

simple_core_arch = Arch(custom_modules={
    "regfile": "regfile",
    "alu": "funit",
    "instr_mem": "text_memory",
    "pc": "program_counter",
}, custom_nets={
    "clk": "clock",
    "rst": "reset",
    })

generate_tests_for_type(RTypeInstr, simple_core_arch)
generate_tests_for_type(ITypeInstr, simple_core_arch)
```

The advantage of this approach is that every instruction can be developed in isolation and tracing errors in programs can be easier.

## Getting Started

### Installing Dependencies
`riscv_cocotb` currently uses `llvm-mc` to get bytecode of assembly strings and cocotb as a dependency.
Install LLVM:

```shell
sudo apt install llvm
```

The default simulation runner is Icarus Verilog. To install iverilog:

```shell
sudo apt install iverilog
```
Check out the installed version of `iverilog`, it should be higher than 12.0:

```shell
iverilog -v
Icarus Verilog version 12.0 (stable) ()
```
If it is version 11.0 or lower, please install `iverilog`  [from source](https://github.com/steveicarus/iverilog?tab=readme-ov-file#compiling-from-github):
```
git clone https://github.com/steveicarus/iverilog
cd iverilog
sh autoconf.sh
./configure
make
sudo make install
```
After making sure `llvm-mc --version` and `iverilog -v` commands work, continue on installing Python packages:
```shell
cd riscv-cocotb
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```
### Running the Tests

To run the test suite:
```shell
cd riscv-cocotb/tests
make
```

## Roadmap
|Goal|Progress|
|----|----|
|R type Instrs|:heavy_check_mark:|
|I type Instrs|:heavy_check_mark:|
|Architecture Abstraction|:heavy_check_mark:|
|Load Store Instrs|:heavy_multiplication_x:|
|Timing Abstractions (for Pipeline)|:heavy_multiplication_x:|
