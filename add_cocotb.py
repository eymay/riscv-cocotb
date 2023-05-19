import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, Timer

from as2hex import *

instr = as2hex("add x1, x2, x4", "add")

@cocotb.test()
async def add_test(dut):
    """Try accessing the design."""
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    dut.rst = 0
    await Timer(5, units="ns")
    dut.rst = 1
    await Timer(5, units="ns")
    dut.dp.regfile.regs[2].value = 3
    dut.dp.regfile.regs[4].value = 5

    addr = 0
    for i in range(4):
        print(instr[i])
        dut.instr_mem.imem[addr+i].value = int(instr[i], 16)
        print(hex(dut.instr_mem.imem[addr+i].value))

    
    await Timer(5, units="ns")
    await Timer(5, units="ns")
    await Timer(5, units="ns")
    await Timer(5, units="ns")

    assert dut.dp.regfile.regs[1].value == 8, "{} != {}".format(dut.dp.regfile.regs[1].value, 8)


