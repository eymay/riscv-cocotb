# riscv-cocotb

RISC-V unit testing for instructions with Python based on Cocotb. This project provides an easy to use API to customize tests for your RISC-V core. The tests are aimed to monitor the inner signals of modules to provide rich error information to hardware developers.

The final goal is to support all instructions in RV32I base instruction set. Currently all Register-Register and Register-Immediate instructions are supported.

The generic tests can be used for single cycle cores with simple timings. 
```python
async def generic_itype_test(dut, op, opstring, debug = False):
    await initialize(dut)
    rd = 1
    rs1 = 2
    imm = 4
    addr = 4

    instr_obj = Alu_ri(dut, rd, rs1, imm, op, opstring)
    instr_obj.set_rs1(5)
    instr_obj.set_ideal_result()
    set_instruction(instr_obj, addr)

    await FallingEdge(dut.clk)

    instr_obj.check_imm()
    instr_obj.check_ALU()

    await FallingEdge(dut.clk)
    instr_obj.check_rd()

    pc = instr_obj.arch.get_regs("pc")
    pc.value = 4
```
Now, this generic immediate test can be invoked as the following:

```python
@cocotb.test()
async def addi_test(dut):
    await generic_itype_test(dut, lambda x,y: x+y, "addi")

@cocotb.test()
async def slti_test(dut):
    await generic_itype_test(dut, lambda x,y: 1 if x<y else 0, "slti")

@cocotb.test()
async def xori_test(dut):
    await generic_itype_test(dut, lambda x,y: x^y, "xori")
```

The advantage of this approach is that every instruction can be developed in isolation and tracing errors in programs can be easier.

## Getting Started
`riscv-cocotb` currently uses llvm to get bytecode of assembly strings and cocotb as a dependency.
Install llvm and cocotb on debian based distros:

```shell
sudo apt install llvm-14
pip3 install cocotb
```
Configure your project by modifying the `Makefile`
```Makefile
VERILOG_SOURCES += YOUR_VERILOG_SRC/*.v

TOPLEVEL = YOUR_TOP_MODULE
```
Additional settings can be done in Makefile such as choosing a different simulation backend. Refer to Cocotb for additional configuration.

## Development
This project is under development, any contribution is welcome. To see an working and integrated version of this project to a RISC-V core please check [here](https://github.com/Eymay/RV32I_Core).
