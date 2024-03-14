import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, Timer

from debug_utils import debug_instr
from instr_types import Arch, Instruction, Alu_type, Alu_rr, Alu_ri


def set_instruction(dut, arch, instr_obj, addr):
    instr = instr_obj.instr.get_instr_byte()
    print("Instr emmitted is", instr[0], instr[1], instr[2], instr[3])
    instr_mem = arch.get_mem(dut, "instr_mem")
    # print("Instr Mem: ", instr_mem)
    for i in range(4):
        instr_mem[addr + i].value = int(instr[i], 16)


async def initialize(dut, arch):
    clock = Clock(arch.get_clock(dut), 10, units="ns")
    cocotb.start_soon(clock.start())

    rst = arch.get_reset(dut)

    rst.value = 0
    await Timer(5, units="ns")
    rst.value = 1
    await Timer(5, units="ns")


async def generic_itype_test(dut, arch, op, opstring, debug=True):
    await initialize(dut, arch)
    rd = 1
    rs1 = 2
    imm = 4
    addr = 4

    instr_obj = Alu_ri(dut, arch, rd, rs1, imm, op, opstring)
    instr_obj.set_rs1(5)
    instr_obj.set_ideal_result()
    set_instruction(dut, arch, instr_obj, addr)

    if debug:
        debug_instr(dut, arch, instr_obj, addr)

    await FallingEdge(dut.clk)
    if debug:
        debug_instr(dut, arch, instr_obj, addr)
        instr_obj.debug_imm(dut, arch)

    instr_obj.check_imm(dut, arch)
    instr_obj.check_ALU(dut, arch)

    await FallingEdge(dut.clk)
    instr_obj.check_rd()

    pc = arch.get_regs(dut, "pc")
    pc.value = 4


async def generic_rtype_test(dut, arch, op, opstring):
    await initialize(dut, arch)

    rd = 1
    rs1 = 2
    rs2 = 4
    addr = 4

    instr_obj = Alu_rr(dut, arch, rd, rs1, rs2, op, opstring)
    instr_obj.set_rs1(5)
    instr_obj.set_rs2(3)
    instr_obj.set_ideal_result()
    set_instruction(dut, arch, instr_obj, addr)

    # debug_instr(instr_obj, addr)

    await FallingEdge(dut.clk)
    # await FallingEdge(dut.clk)
    debug_instr(dut, arch, instr_obj, addr)
    # print("Instr Mem: ", dut.instr_mem.imem[addr].value)
    instr_obj.check_ALU(dut, arch)

    await FallingEdge(dut.clk)
    instr_obj.check_rd()
    # debug_instr(dut, addr)

    pc = arch.get_regs(dut, "pc")
    pc.value = 4
