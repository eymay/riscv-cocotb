import sys
import cocotb
sys.path.append('../../../src/riscv_cocotb/')
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
