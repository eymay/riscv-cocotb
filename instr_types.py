from as2hex import *
from functools import lru_cache

class Arch:
    module_paths = {}
    modules = {"regfile": "regfile",
               "alu": "FU",
               "data_mem": "data_mem",
               "pc": "PC", 
               "instr_mem": "instr_mem",
               "immed_gen": "immed_gen"}
    comb_modules = set()
    seq_modules = set()

    def __init__(self, dut):
        self.dut = dut

    @lru_cache(maxsize=None)
    def recurse_handles(self, top, module):
        if top._name == module:
            return top
        top._discover_all()
        if module in top._sub_handles:
            return top._sub_handles[module]
        else:
            for handle in top._sub_handles.values():
                if handle._type == "GPI_MODULE":
                    path = self.recurse_handles(handle, module)
                    if path != None:
                        return path
            return None

    def get_path(self, module_name):
        print("Module Name: ", module_name)
        if module_name not in Arch.modules:
            raise Exception("Input module not in module dict, please add your module")

        local_module = Arch.modules[module_name]
        if local_module == None:
            raise Exception("Not found in module list")
        if local_module in Arch.module_paths:
            print("Cached Path: ", Arch.module_paths[local_module])
            return Arch.module_paths[local_module]
        else:
            path = self.recurse_handles(self.dut, local_module)
            print("Calculated Path: ", path)
            if path != None:
                Arch.module_paths[local_module] = path
            else:
                raise Exception("Verilog module path not found")
            return path
    
    @lru_cache(maxsize=None)
    def get_regs(self, module):
        parent = self.get_path(module)
        if parent == None:
            raise Exception("Verilog module path not found")
        parent._discover_all()
        for elem in parent._sub_handles.values():
            if elem._type == "GPI_ARRAY":
                return elem
        #dirty fix for 1D arrays
        for elem in parent._sub_handles.values():
            if elem._type == "GPI_REGISTER":
                return elem

    def get_mem(self, module):
        return self.get_regs(module)

    def is_comb(self, module):
        if module in Arch.comb_modules:
            return True
        elif module in Arch.seq_modules:
            return False
        else:
            if module._type != "GPI_MODULE":
                raise Exception("Only module type elements can be comb or seq")
            module._discover_all()
            if 'clk' not in module._sub_handles:
                Arch.comb_modules.add(module)
                return True
            else:
                Arch.seq_modules.add(module)
                return False


    @lru_cache(maxsize=None)
    def get_output(self, module):
        parent = self.get_path(module)
        if parent == None:
            raise Exception("Verilog module path not found")
        parent._discover_all()
        #print(parent._sub_handles)
        #for elem in parent._sub_handles.values():
        #    print(elem._type, elem._name)

        #if self.is_comb(parent):
        #It is assumed that if the module is combinational,
        #it will have an output with reg type. 
        #However, simple seq modules can also have single reg type signals which are output
        max_len_reg = None
        subdict = {k:v for (k,v) in parent._sub_handles.items() if v._type == "GPI_REGISTER"}
        #Another heuristic is to assume the largest length of bits to be the output
        # and not some internal reg used for computation
        return max(subdict.values(), key=lambda x: len(x))


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
    def __init__(self, arch, rd, rs1,  op, opstring):
        reg = arch.get_regs("regfile")
        self.rd_idx = rd
        self.rs1_idx = rs1
        self.rd = reg[rd]
        self.rs1 = reg[rs1]
        self.op = op
        self.ideal_result = 0
        self.ideal_operand1 = 0
        self.ideal_operand2 = 0

        self.arch = arch

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
        out_ALU = self.arch.get_output("alu")
        assert out_ALU.value == self.ideal_result, "ALU output not correct {} != {}".format(out_ALU.value, self.ideal_result)

    def check_rd(self):
        assert self.rd.value == self.ideal_result, "Destination register has wrong result {} != {}".format(self.rd.value, self.ideal_result)


class Alu_rr(Alu_type):
    def __init__(self, dut, rd, rs1, rs2, op, opstring):
        arch = Arch(dut)
        reg = arch.get_regs("regfile")
        super().__init__(arch, rd, rs1, op, opstring)
        self.rs2_idx = rs2
        self.rs2 = reg[rs2]
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
        arch = Arch(dut)
        super().__init__(arch, rd, rs1, op, opstring)
        self.set_operand2(imm)
        self.imm = self.ideal_operand2
        self.instr = Instruction(
                opstring, 
                "x{}".format(rd),
                "x{}".format(rs1),
                str(imm))

    def check_imm(self):
        out_imm = self.arch.get_output("immed_gen")
        assert out_imm.value == self.imm, "Immediate produced is not correct {} != {}".format(out_imm.value, self.imm)

    def debug_imm(self):
        out_imm = self.arch.get_output("immed_gen")
        print("Imm:", out_imm.value)
