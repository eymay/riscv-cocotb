
def debug_instr(dut, addr):
    for i in range(4):
        print(hex(dut.instr_mem.imem[addr+i].value))
    print("PC:", hex(dut.o_PC.value))
    print("Instr mem:", hex(dut.o_instruction_mem.value))

def debug_signals(dut, addr):
    for i in range(4):
        print(hex(dut.instr_mem.imem[addr+i].value))
    print("PC:", hex(dut.o_PC.value))
    print("Instr mem:", hex(dut.o_instruction_mem.value), dut.o_instruction_mem.value)
    print("Reg1:", dut.dp.regfile.regs[2].value)
    print("Reg2:", dut.dp.regfile.regs[4].value)
    print("ALU A:", dut.dp.ALU.A.value)
    print("ALU B:", dut.dp.ALU.B.value)
    print("Regfile out 2:", dut.dp.o_regfile_rreg2.value)
    print("CW", dut.cu.ctrl_wrd.value)
    print("CW4_2", dut.dp.CW4_2.value)
    print("Imm out:", dut.dp.o_imm.value)
    print("ALU out:", dut.o_ALU.value)

def debug_shifter(dut):
    print("Shift Result:", dut.dp.ALU.Shift_result.value)
    print("Shift Result:", dut.dp.ALU.s.H.value)


def set_instruction(instr_obj,dut,addr):
    instr = instr_obj.instr.get_instr_byte()
    print("Instr emmitted is", instr[0], instr[1], instr[2], instr[3])
    for i in range(4):
        instr_obj.dut.instr_mem.imem[addr+i].value = int(instr[i], 16)

