from cocotb.binary import BinaryValue
from riscv_cocotb.as2hex import as2hex
from functools import lru_cache


class Arch:
    def __init__(self, custom_modules=None, custom_nets=None, littleEndian=True):
        self.module_paths = {}
        self.modules = {
            "regfile": "regfile",
            "alu": "funit",
            "data_mem": "data_mem",
            "pc": "pc_updater",
            "instr_mem": "instr_mem",
            "immed_gen": "immed_gen",
        }
        self.comb_modules = set()
        self.seq_modules = set()
        self.net_paths = {}
        self.nets = {
            "clk": "clk",
            "rst": "rst",
        }
        self.littleEndian=littleEndian

        if custom_modules:
            self.modules.update(custom_modules)
        if custom_nets:
            self.nets.update(custom_nets)

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

    def get_path(self, dut, module_name):
        print("Module Name: ", module_name)
        if module_name not in self.modules:
            raise Exception("Input module not in module dict, please add your module")

        local_module = self.modules[module_name]
        if local_module is None:
            raise Exception("Not found in module list")
        if local_module in self.module_paths:
            print("Cached Path: ", self.module_paths[local_module])
            return self.module_paths[local_module]
        else:
            path = self.recurse_handles(dut, local_module)
            print("Calculated Path: ", path)
            if path is not None:
                self.module_paths[local_module] = path
            else:
                raise Exception("Verilog module path not found")
            return path

    @lru_cache(maxsize=None)
    def find_entity_path(self, top, name, entity_type="module"):
        """
        Recursively searches for an entity (module, net, or register) within the given top module.

        :param top: The top module or hierarchy level to start the search.
        :param name: The name of the entity to find.
        :param entity_type: The type of entity ('module', 'net', 'register', or 'all' for any type).
        :return: The found entity or None if not found.
        """
        top._discover_all()
        for handle in top._sub_handles.values():
            if entity_type == "all" or handle._type == self._gpi_type_map(entity_type):
                if handle._name == name:
                    return handle
            # Recurse if it's a module, regardless of the entity type, because entities might be nested within
            if handle._type == "GPI_MODULE":
                found_entity = self.find_entity_path(handle, name, entity_type)
                if found_entity:
                    return found_entity
        return None

    def _gpi_type_map(self, entity_type):
        """
        Maps a high-level entity type to the corresponding GPI type.
        """
        return {
            "module": "GPI_MODULE",
            "net": "GPI_NET",
            "register": "GPI_REGISTER",
        }.get(entity_type, None)

    def get_entity(self, dut, name, entity_type="module"):
        """
        Retrieves an entity (module, net, or register) from the DUT based on its name and type.

        :param dut: The DUT object.
        :param name: The name of the entity.
        :param entity_type: The type of the entity ('module', 'net', 'register', or 'all' for any type).
        :return: The entity if found, raises an exception otherwise.
        """
        if name not in self.net_paths:
            entity = self.find_entity_path(dut, name, entity_type)
            if entity:
                self.net_paths[name] = entity
                return entity
            else:
                raise Exception(
                    f"{entity_type.capitalize()} named '{name}' not found in the DUT."
                )
        return self.net_paths[name]

    @lru_cache(maxsize=None)
    def get_regs(self, dut, module):
        parent = self.get_path(dut, module)
        if parent == None:
            raise Exception("Verilog module path not found")
        parent._discover_all()
        for elem in parent._sub_handles.values():
            if elem._type == "GPI_ARRAY":
                return elem
        # dirty fix for 1D arrays
        for elem in parent._sub_handles.values():
            if elem._type == "GPI_REGISTER":
                return elem

    def get_mem(self, dut, module):
        return self.get_regs(dut, module)

    def is_comb(self, module):
        if module in Arch.comb_modules:
            return True
        elif module in Arch.seq_modules:
            return False
        else:
            if module._type != "GPI_MODULE":
                raise Exception("Only module type elements can be comb or seq")
            module._discover_all()
            if "clk" not in module._sub_handles:
                Arch.comb_modules.add(module)
                return True
            else:
                Arch.seq_modules.add(module)
                return False

    @lru_cache(maxsize=None)
    def get_output(self, dut, module):
        parent = self.get_path(dut, module)
        if parent == None:
            raise Exception("Verilog module path not found")
        parent._discover_all()
        # print(parent._sub_handles)
        # for elem in parent._sub_handles.values():
        #    print(elem._type, elem._name)

        # if self.is_comb(parent):
        # It is assumed that if the module is combinational,
        # it will have an output with reg type.
        # However, simple seq modules can also have single reg type signals which are output
        max_len_reg = None
        subdict = {
            k: v for (k, v) in parent._sub_handles.items() if v._type == "GPI_REGISTER"
        }
        # Another heuristic is to assume the largest length of bits to be the output
        # and not some internal reg used for computation
        return max(subdict.values(), key=lambda x: len(x))

    def get_clock(self, dut):
        return self.get_entity(dut, self.nets["clk"], entity_type="net")

    def get_reset(self, dut):
        return self.get_entity(dut, self.nets["rst"], entity_type="net")


class Instruction:
    def __init__(self, op, place1, place2, place3, arch_little_endian=True):
        # place1, place2, place3 are the places where the operands are in the instruction
        self.op = op
        self.place1 = place1
        self.place2 = place2
        self.place3 = place3
        self.assembly = (
            op
            + " "
            + place1
            + ", "
            + place2
            + ((", " + place3) if place3 != "" else "")
        )
        self.instr_byte, self.hex_little_endian = as2hex(self.assembly, op)
        if arch_little_endian and not self.hex_little_endian:
            self.set_little_endian() # Default endiannes 

    def set_little_endian(self):
        if not self.hex_little_endian:
            self.instr_byte = self.instr_byte[::-1]
            self.hex_little_endian = True

    def get_instr_byte(self):
        return self.instr_byte

    def get_instr_hex(self):
        if isinstance(self.instr_byte, list):
            hex_str = ''.join([f"{int(byte, 16):02x}" for byte in reversed(self.instr_byte)])
            formatted_hex = f"0x{hex_str:0>8}"
            return formatted_hex
        print("Instruction not returned as list")

    def get_assembly(self):
        return self.assembly


class Alu_type:
    """Class that does computation, R and I type instrs"""

    def __init__(self, dut, arch, rd, rs1, op, opstring):
        reg = arch.get_regs(dut, "regfile")
        self.rd_idx = rd
        self.rs1_idx = rs1
        self.rd = reg[rd]
        self.rs1 = reg[rs1]
        self.op = op
        self.ideal_result = 0
        self.ideal_operand1 = 0
        self.ideal_operand2 = 0

    def check_x0(self, reg, value):
        # x0 register is hardwired to 0 in RISC-V
        return 0 if reg == 0 else value

    def set_rs1(self, value):
        self.rs1.value = self.check_x0(self.rs1_idx, value)
        self.ideal_operand1 = value

    def set_operand2(self, value):
        self.ideal_operand2 = value

    def set_ideal_result(self):
        self.ideal_result = self.check_x0(self.rd_idx, self.gold())

    def gold(self):
        return self.op(self.ideal_operand1, self.ideal_operand2)

    def check_ALU(self, dut, arch):
        out_ALU = arch.get_output(dut, "alu")
        assert (
            out_ALU.value == self.ideal_result
        ), f"ALU output not correct {out_ALU.value} != {self.ideal_result}"

    def check_rd(self):
        assert (
            self.rd.value == self.ideal_result
        ), f"Destination register has wrong result {self.rd.value} != {self.ideal_result}"


class Alu_rr(Alu_type):
    def __init__(self, dut, arch, rd, rs1, rs2, op, opstring):
        reg = arch.get_regs(dut, "regfile")
        super().__init__(dut, arch, rd, rs1, op, opstring)
        self.rs2_idx = rs2
        self.rs2 = reg[rs2]
        self.instr = Instruction(opstring, f"x{rd}", f"x{rs1}", f"x{rs2}", arch.littleEndian)

    def set_rs2(self, value):
        self.set_operand2(value)
        self.rs2.value = self.check_x0(self.rs2_idx, value)


class Alu_ri(Alu_type):
    def __init__(self, dut, arch, rd, rs1, imm, op, opstring):
        super().__init__(dut, arch, rd, rs1, op, opstring)
        self.set_operand2(imm)
        self.imm = self.ideal_operand2
        self.instr = Instruction(opstring, f"x{rd}", f"x{rs1}", str(imm), arch.littleEndian)

    def check_imm(self, dut, arch):
        out_imm = arch.get_output(dut, "immed_gen").value.integer
        expected_imm = self.imm

        if self.instr.op in ["slli", "srli", "srai"]:
            # For shift instructions, only the least significant 5 bits are relevant
            mask = 0x1F
            out_imm &= mask
            expected_imm &= mask

        assert (
            out_imm == expected_imm
        ), f"Immediate produced is not correct {out_imm} != {self.imm}"

    def debug_imm(self, dut, arch):
        out_imm = arch.get_output(dut, "immed_gen")
        print("Imm:", out_imm.value)
