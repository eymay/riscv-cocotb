import random
import cocotb

import debug_utils as dbg
from generic_tests import initialize, set_instruction
from generic_tests import generic_itype_test, generic_rtype_test


from instr_types import Instruction

from cocotb.triggers import FallingEdge, Timer

class mem_type:
    def __init__(self, dut, rs1, offset, len, opstring):
        self.rs1_idx = rs1
        self.rs1 = dut.dp.regfile.regs[rs1]
        self.offset = offset
        self.byte_addr = 0
        self.transf_value = 0
        self.mem = 0

        self.dut = dut

    def check_x0(self, reg, value):
        #x0 register is hardwired to 0 in RISC-V
        return 0 if reg == 0 else value

    def set_rs1(self, value):
        self.rs1.value = self.check_x0(self.rs1_idx, value)
        self.ideal_operand1 = value

    def set_addr(self):
        self.byte_addr = self.rs1.value + self.offset

    def set_memref(self):
        self.mem = self.dut.data_mem.dmem[self.byte_addr]

    def set_mem(self, val):
        self.mem.value = val


class load_type(mem_type):
    def __init__(self, dut, rd, rs1, offset, len, opstring):
        super().__init__(dut, rs1, offset, len, opstring)
        self.rd_idx = rd
        self.rd = dut.dp.regfile.regs[rd]
        self.instr = Instruction(
                opstring, 
                "x{}".format(rd),
                str(offset) + "(x{})".format(rs1),
                "")

    def get_value(self):
        print("mem:", self.mem)
        print("mem buff:", self.mem.buff)
        self.transf_value = self.mem[len-1:0].value

    def check_rd(self):
        self.get_value()
        assert self.rd.value == self.transf_value , "Loaded value not correct {}!={}".format(self.rd.value, self.transf_value)


async def generic_load_test(dut, len, opstring, debug = False):
    await initialize(dut)
    rd = 1
    rs1 = 2
    offset = 4
    addr = 4

    instr_obj = load_type(dut, rd, rs1, offset,len, opstring)
    instr_obj.set_rs1(5)
    instr_obj.set_memref()
    set_instruction(instr_obj, dut, addr)

    #debug_instr(dut, addr)

    await FallingEdge(dut.clk)
    if(debug):
        dbg.debug_signals(dut, addr)
    #debug_shifter(dut)
    instr_obj.check_rd()

    #debug_instr(dut, addr)

    dut.PC.Q.value = 4


@cocotb.test()
async def lw_test(dut):
    await generic_load_test(dut, len=32 ,opstring="lw", debug=False)

@cocotb.test()
async def lh_test(dut):
    await generic_load_test(dut, len=16 ,opstring="lh", debug=False)

@cocotb.test()
async def addi_test(dut):
    await generic_itype_test(dut, lambda x,y: x+y, "addi", debug=False)

@cocotb.test()
async def slti_test(dut):
    await generic_itype_test(dut, lambda x,y: 1 if x<y else 0, "slti")

@cocotb.test()
async def sltiu_test(dut):
    await generic_itype_test(dut, lambda x,y: 1 if (x+2**32)<(y+2**32) else 0, "sltiu")

@cocotb.test()
async def xori_test(dut):
    await generic_itype_test(dut, lambda x,y: x^y, "xori")

@cocotb.test()
async def ori_test(dut):
    await generic_itype_test(dut, lambda x,y: x|y, "ori")

@cocotb.test()
async def andi_test(dut):
    await generic_itype_test(dut, lambda x,y: x&y, "andi")

#shifts on the value in
#register rs1 by the shift amount held in the lower 5 bits of register rs2
@cocotb.test()
async def slli_test(dut):
    await generic_itype_test(dut, lambda x,y: x<<y, "slli")

@cocotb.test()
async def srli_test(dut):
    await generic_itype_test(dut, lambda x,y: (x % 0x100000000) >> y, "srli")

@cocotb.test()
async def srai_test(dut):
    await generic_itype_test(dut, lambda x,y: x>>y, "srai")

@cocotb.test()
async def add_test(dut):
    await generic_rtype_test(dut, lambda x,y: x+y, "add")

@cocotb.test()
async def sub_test(dut):
    await generic_rtype_test(dut, lambda x,y: x-y, "sub")
#shifts on the value in
#register rs1 by the shift amount held in the lower 5 bits of register rs2
@cocotb.test()
async def sll_test(dut):
    await generic_rtype_test(dut, lambda x,y: x<<y, "sll")

@cocotb.test()
async def slt_test(dut):
    await generic_rtype_test(dut, lambda x,y: 1 if x<y else 0, "slt")

@cocotb.test()
async def sltu_test(dut):
    await generic_rtype_test(dut, lambda x,y: 1 if (x+2**32)<(y+2**32) else 0, "sltu")

@cocotb.test()
async def xor_test(dut):
    await generic_rtype_test(dut, lambda x,y: x^y, "xor")

@cocotb.test()
async def srl_test(dut):
    await generic_rtype_test(dut, lambda x,y: (x % 0x100000000) >> y, "srl")

@cocotb.test()
async def sra_test(dut):
    await generic_rtype_test(dut, lambda x,y: x>>y, "sra")

@cocotb.test()
async def or_test(dut):
    await generic_rtype_test(dut, lambda x,y: x|y, "or")

@cocotb.test()
async def and_test(dut):
    await generic_rtype_test(dut, lambda x,y: x&y, "and")
