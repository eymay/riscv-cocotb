import sys
import cocotb
# sys.path.append('../../../src/riscv_cocotb/')
from riscv_cocotb.unit_test_instrs import generate_tests_for_type, RTypeInstr, ITypeInstr
from riscv_cocotb.instr_types import Arch

simple_core_arch = Arch(custom_modules={
    "regfile": "regfile",
    "alu": "funit",
}, littleEndian=False)

generate_tests_for_type(RTypeInstr, simple_core_arch)
generate_tests_for_type(ITypeInstr, simple_core_arch)
