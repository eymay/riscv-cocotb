import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, Timer

from riscv_cocotb.debug_utils import debug_instr
from riscv_cocotb.instr_types import Arch, Instruction, Alu_type, Alu_rr, Alu_ri


def set_instruction(dut, arch, instr_obj, addr):
    instr = instr_obj.get_instr_byte()
    print("Instr emmitted is", instr[0], instr[1], instr[2], instr[3])
    instr_mem = arch.get_mem(dut, "instr_mem")
    print("Instr Mem: ", instr_mem)
    print("Instr Mem 0: ", instr_mem[0])
    mem_width = len(instr_mem[0].value.binstr)
    print("Memory width:", mem_width)

    # Prepare the instruction data based on memory width
    if mem_width == 8:  # 8-bit memory width
        for i in range(4):
            instr_mem[addr + i].value = int(instr[i], 16)
    elif mem_width == 16:  # 16-bit memory width
        for i in range(0, 4, 2):
            # Swap the order of bytes when combining them for little-endian storage
            combined_value = int(instr[i+1], 16) << 8 | int(instr[i], 16)
            instr_mem[addr + i//2].value = combined_value
    elif mem_width == 32:  # 32-bit memory width
        combined_value = (int(instr[3], 16) << 24 | int(instr[2], 16) << 16 |
                          int(instr[1], 16) << 8 | int(instr[0], 16))
        instr_mem[addr].value = combined_value
    else:
        raise ValueError(f"Unsupported memory width: {mem_width}")


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

    instr_class = Alu_ri(dut, arch, rd, rs1, imm, op, opstring)
    instr_class.set_rs1(5)
    instr_class.set_ideal_result()
    instr_obj = instr_obj.instr
    set_instruction(dut, arch, instr_obj, addr)
    # Allow simulation to read the new set instruction
    await cocotb.triggers.Timer(1, units="ns")

    if debug:
        debug_instr(dut, arch, instr_obj, addr)

    await FallingEdge(dut.clk)
    if debug:
        debug_instr(dut, arch, instr_obj, addr)
        instr_class.debug_imm(dut, arch)

    instr_class.check_imm(dut, arch)
    instr_class.check_ALU(dut, arch)

    await FallingEdge(dut.clk)
    instr_class.check_rd()

    pc = arch.get_regs(dut, "pc")
    pc.value = 4


async def generic_rtype_test(dut, arch, op, opstring):
    await initialize(dut, arch)

    rd = 1
    rs1 = 2
    rs2 = 4
    addr = 4

    instr_class = Alu_rr(dut, arch, rd, rs1, rs2, op, opstring)
    instr_class.set_rs1(5)
    instr_class.set_rs2(3)
    instr_class.set_ideal_result()
    instr_obj = instr_class.instr
    set_instruction(dut, arch, instr_obj, addr)

    # debug_instr(instr_obj, addr)

    await FallingEdge(dut.clk)
    # await FallingEdge(dut.clk)
    debug_instr(dut, arch, instr_obj, addr)
    # print("Instr Mem: ", dut.instr_mem.imem[addr].value)
    instr_class.check_ALU(dut, arch)

    await FallingEdge(dut.clk)
    instr_class.check_rd()
    # debug_instr(dut, addr)

    pc = arch.get_regs(dut, "pc")
    pc.value = 4
