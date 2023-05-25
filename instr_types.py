from as2hex import *

class Arch:
    module_paths = {}
    modules = {regfile: "regfile",
                        alu: "ALU",
                        data_mem: "data_mem",
                        pc: "PC"}
    def __init__(self, dut):
        self.dut = dut
        
        

    def get_module (self, module_name):
        if module_name in Arch.modules:
            return Arch.module_paths[module_name]
        else:
            path = self.dut.__get_sub_handle_by_name(module_name)
            print(path)
            Arch.module_paths[module_name] = path
            return path

class Instruction():
    def __init__(self, op, place1, place2, place3): 
        #place1, place2, place3 are the places where the operands are in the instruction
        self.op = op
        self.place1 = place1
        self.place2 = place2
        self.place3 = place3
        self.assembly = op +" "+ place1 +", "+ place2 + ((", "+ place3) if place3 != "" else "")
        self.instr_byte = as2hex(self.assembly , op)

    def get_instr_byte(self):
        return self.instr_byte
    def get_assembly(self):
        return self.assembly


class Alu_type:
    """Class that does computation, R and I type instrs"""
    def __init__(self, dut, rd, rs1,  op, opstring):
        self.rd_idx = rd
        self.rs1_idx = rs1
        self.rd = dut.dp.regfile.regs[rd]
        self.rs1 = dut.dp.regfile.regs[rs1]
        self.op = op
        self.ideal_result = 0
        self.ideal_operand1 = 0
        self.ideal_operand2 = 0

        self.dut = dut

    def check_x0(self, reg, value):
        #x0 register is hardwired to 0 in RISC-V
        return 0 if reg == 0 else value

    def set_rs1(self, value):
        self.rs1.value = self.check_x0(self.rs1_idx, value)
        self.ideal_operand1 = value

    def set_operand2(self, value):
        self.ideal_operand2 = value

    def set_ideal_result(self):
        self.ideal_result = self.check_x0(self.rd_idx, self.gold())



    def gold(self):
        return self.op(self.ideal_operand1,self.ideal_operand2)

    def check_ALU(self):
        assert self.dut.dp.o_ALU.value == self.ideal_result, "ALU output not correct {} != {}".format(self.dut.dp.o_ALU.value, self.ideal_result)

    def check_rd(self):
        assert self.rd.value == self.ideal_result, "Destination register has wrong result {} != {}".format(self.rd.value, self.ideal_result)

class Alu_rr(Alu_type):
    def __init__(self, dut, rd, rs1, rs2, op, opstring):
        super().__init__(dut, rd, rs1, op, opstring)
        self.rs2_idx = rs2
        self.rs2 = dut.dp.regfile.regs[rs2]
        self.instr = Instruction(
                opstring, 
                "x{}".format(rd),
                "x{}".format(rs1),
                "x{}".format(rs2))

    def set_rs2(self, value):
        self.set_operand2(value)
        self.rs2.value = self.check_x0(self.rs2_idx, value)


class Alu_ri(Alu_type):
    def __init__(self, dut, rd, rs1, imm, op, opstring):
        super().__init__(dut, rd, rs1, op, opstring)
        self.set_operand2(imm)
        self.imm = self.ideal_operand2
        self.instr = Instruction(
                opstring, 
                "x{}".format(rd),
                "x{}".format(rs1),
                str(imm))

    def check_imm(self):
        assert self.dut.dp.o_imm.value == self.imm, "Immediate produced is not correct {} != {}".format(self.dut.dp.o_imm.value, self.imm)

    def debug_imm(self):
        print("Imm:", self.dut.dp.o_imm.value)
        print("Immed Gen Field:", self.dut.immed_gen.field.value)
        print("Immed Gen Select:", self.dut.immed_gen.select.value)
