import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, Timer

from instr_types import Arch, Instruction, Alu_type, Alu_rr, Alu_ri


def set_instruction(instr_obj, dut, addr):
    instr = instr_obj.instr.get_instr_byte()
    print("Instr emmitted is", instr[0], instr[1], instr[2], instr[3])
    instr_mem = instr_obj.arch.get_mem("instr_mem")
    for i in range(4):
        instr_mem[addr+i].value = int(instr[i], 16)

async def initialize(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    dut.rst.value = 0
    await Timer(5, units="ns")
    dut.rst.value = 1
    await Timer(5, units="ns")

async def generic_itype_test(dut, op, opstring, debug = False):
    await initialize(dut)
    rd = 1
    rs1 = 2
    imm = 4
    addr = 4

    instr_obj = Alu_ri(dut, rd, rs1, imm, op, opstring)
    instr_obj.set_rs1(5)
    instr_obj.set_ideal_result()
    set_instruction(instr_obj, dut, addr)

    #debug_instr(dut, addr)

    await FallingEdge(dut.clk)
    if(debug):
        dbg.debug_signals(dut, addr)
        instr_obj.debug_imm()
    #debug_shifter(dut)
    instr_obj.check_imm()
    instr_obj.check_ALU()

    await FallingEdge(dut.clk)
    instr_obj.check_rd()
    #debug_instr(dut, addr)

    dut.PC.Q.value = 4

async def generic_rtype_test(dut, op, opstring):
    
    await initialize(dut)

    rd = 1
    rs1 = 2
    rs2 = 4
    addr = 4

    instr_obj = Alu_rr(dut, rd, rs1, rs2, op, opstring)
    instr_obj.set_rs1(5)
    instr_obj.set_rs2(3)
    instr_obj.set_ideal_result()
    set_instruction(instr_obj, dut, addr)

    #debug_instr(dut, addr)

    await FallingEdge(dut.clk)
    #debug_signals(dut, addr)
    #debug_shifter(dut)
    instr_obj.check_ALU()

    await FallingEdge(dut.clk)
    instr_obj.check_rd()
    #debug_instr(dut, addr)

    dut.PC.Q.value = 4
