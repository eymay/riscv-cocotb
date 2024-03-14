from instr_types import Arch

def debug_instr(dut, arch, instr_obj, addr):
    instr = instr_obj.instr.get_instr_byte()
    print("Instr emmitted is", instr[0], instr[1], instr[2], instr[3])

    o_PC = arch.get_output(dut, "pc")
    print("PC:", o_PC.value)
    print("PC:", hex(o_PC.value))
    o_instr_mem = arch.get_output(dut, "instr_mem")
    print("Instr mem:", hex(o_instr_mem.value))
