import os
import subprocess
from riscv_assembler.convert import AssemblyConverter as AC

src_dir = os.path.dirname(os.path.realpath(__file__))
dis_script = os.path.join(src_dir, "dis.sh")

def llvm_mc_available():
    try:
        subprocess.run(["llvm-mc", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def as2hex_llvm_mc(asm, inst):
    result = subprocess.run([dis_script, asm, inst], stdout=subprocess.PIPE)
    #returns list of byte strings 
    return result.stdout.decode('utf-8').split(), False # not little_endian, MSB at first index of list

def as2hex_fallback(asm):
    # Instantiate AssemblyConverter with hex_mode enabled
    convert = AC(output_mode='a', nibble_mode=False, hex_mode=True)
    result = convert.convert(asm)
    
    # Assuming result is in the desired format; adjust if necessary
    return result, False #TODO verify this 

def as2hex(asm, inst):
    if llvm_mc_available():
        return as2hex_llvm_mc(asm, inst)  # Your existing function that uses llvm-mc
    else:
        return as2hex_fallback(asm) 
