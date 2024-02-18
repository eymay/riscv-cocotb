# riscv-cocotb

RISC-V unit testing for instructions with Python based on Cocotb. This project provides an easy to use API to customize tests for your RISC-V core. The tests are aimed to monitor the inner signals of modules to provide rich error information to hardware developers.

The final goal is to support all instructions in RV32I base instruction set. Currently all Register-Register and Register-Immediate instructions are supported.

Tests can be generated for your architecture with minimal configuration. Enter the instantiation names of your modules as such:
```python
from unit_test_instrs import generate_tests_for_type, RTypeInstr, ITypeInstr
from instr_types import Arch

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
`riscv-cocotb` currently uses llvm to get bytecode of assembly strings and cocotb as a dependency.
Install llvm and cocotb on debian based distros:

```shell
sudo apt install llvm
pip install -r requirements.txt
```

#TODO Cocotb runners
~~Configure your project by modifying the `Makefile`~~
```Makefile
VERILOG_SOURCES += YOUR_VERILOG_SRC/*.v

TOPLEVEL = YOUR_TOP_MODULE
```
Additional settings can be done in Makefile such as choosing a different simulation backend. Refer to Cocotb for additional configuration.

## Roadmap
|Goal|Progress|
|----|----|
|R type Instrs|:heavy_check_mark:|
|I type Instrs|:heavy_check_mark:|
|Architecture Abstraction|:heavy_check_mark:|
|Load Store Instrs|:heavy_multiplication_x:|
|Timing Abstractions (for Pipeline)|:heavy_multiplication_x:|

## Development
This project is under development, any contribution is welcome. To see a working and integrated version of this project with a RISC-V core please check [here](https://github.com/Eymay/RV32I_Core).
