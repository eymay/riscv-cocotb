from instr_types import Arch

def print_out(instr_obj, mod_name):
    o_mod = instr_obj.arch.get_output(mod_name)
    print(mod_name, o_mod.value)

def debug_instr(instr_obj, addr):
    instr = instr_obj.instr.get_instr_byte()
    print("Instr emmitted is", instr[0], instr[1], instr[2], instr[3])

    o_PC = instr_obj.arch.get_output("pc")
    print("PC:", hex(o_PC.value))
    o_instr_mem = instr_obj.arch.get_output("instr_mem")
    print("Instr mem:", hex(o_instr_mem.value))

def debug_signals(instr_obj, addr):

    debug_instr(instr_obj, addr)



