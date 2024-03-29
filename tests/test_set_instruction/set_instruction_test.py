import pytest
import cocotb

from riscv_cocotb.generic_tests import set_instruction
from riscv_cocotb.instr_types import Arch, Instruction, Alu_rr

arch_instr_mem_1byte = Arch(custom_modules={
    "instr_mem": "u_instr_mem_1byte",
})

arch_instr_mem_2byte = Arch(custom_modules={
    "instr_mem": "u_instr_mem_2byte",
})

arch_instr_mem_4byte = Arch(custom_modules={
    "instr_mem": "u_instr_mem_4byte",
})

@cocotb.test()
async def instr_mem1_test(dut):
    rd = 1
    rs1 = 2
    rs2 = 4
    addr = 4
    opstring = "add"
    arch = arch_instr_mem_1byte
    instr_obj = Instruction(opstring, f"x{rd}", f"x{rs1}", f"x{rs2}")
    set_instruction(dut, arch, instr_obj, addr)
    dut.addr.value = addr
    await cocotb.triggers.Timer(1, units='ns')  # Allow time for the simulation to update
    o_instr_mem = arch.get_output(dut, "instr_mem")
    o_instr_mem_hex = f"0x{o_instr_mem.value.integer:0>8x}"
    
    expected_hex = instr_obj.get_instr_hex()  # Get formatted hex string of the instruction
    
    print(f"Simulated instr_mem: {o_instr_mem_hex}")
    print(f"Expected instr_hex: {expected_hex}")
    
    assert o_instr_mem_hex == expected_hex, "Instruction memory is not set correctly"

@cocotb.test()
async def instr_mem2_test(dut):
    rd = 1
    rs1 = 2
    rs2 = 4
    addr = 4
    opstring = "add"
    arch = arch_instr_mem_2byte
    instr_obj = Instruction(opstring, f"x{rd}", f"x{rs1}", f"x{rs2}")
    set_instruction(dut, arch, instr_obj, addr)
    dut.addr.value = addr
    await cocotb.triggers.Timer(1, units='ns')  # Allow time for the simulation to update
    o_instr_mem = arch.get_output(dut, "instr_mem")
    o_instr_mem_hex = f"0x{o_instr_mem.value.integer:0>8x}"
    
    expected_hex = instr_obj.get_instr_hex()  # Get formatted hex string of the instruction
    
    print(f"Simulated instr_mem: {o_instr_mem_hex}")
    print(f"Expected instr_hex: {expected_hex}")
    
    assert o_instr_mem_hex == expected_hex, "Instruction memory is not set correctly"
    

@cocotb.test()
async def instr_mem4_test(dut):
    rd = 1
    rs1 = 2
    rs2 = 4
    addr = 4
    opstring = "add"
    arch = arch_instr_mem_4byte
    instr_obj = Instruction(opstring, f"x{rd}", f"x{rs1}", f"x{rs2}")
    set_instruction(dut, arch, instr_obj, addr)
    dut.addr.value = addr
    await cocotb.triggers.Timer(1, units='ns')  # Allow time for the simulation to update
    o_instr_mem = arch.get_output(dut, "instr_mem")
    o_instr_mem_hex = f"0x{o_instr_mem.value.integer:0>8x}"
    
    expected_hex = instr_obj.get_instr_hex()  # Get formatted hex string of the instruction
    
    print(f"Simulated instr_mem: {o_instr_mem_hex}")
    print(f"Expected instr_hex: {expected_hex}")
    
    assert o_instr_mem_hex == expected_hex, "Instruction memory is not set correctly"

