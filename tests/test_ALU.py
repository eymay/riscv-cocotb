import pytest
from cocotb_test.simulator import run
import glob
import os, sys

sys.path.append('../src/riscv_cocotb/')

current_dir = os.path.dirname(os.path.realpath(__file__))

# def test_simple_core():
#     verilog_dir = os.path.join(current_dir, "cores", "simple_core")
#     sources = glob.glob(os.path.join(verilog_dir, "*.v"))
#     run(
#         verilog_sources=sources,
#         toplevel="cpu",  # Top-level Verilog module
#         module="unit_test_instrs",  # Name of the cocotb test module
#         simulator="icarus",  # Specify the simulator you're using, e.g., "icarus", "verilator"
#         waves=True,
#     )

def test_simple_core():
    verilog_dir = os.path.join(current_dir, "cores", "simple_core")
    sys.path.append(verilog_dir)
    sources = glob.glob(os.path.join(verilog_dir, "*.v"))
    run(
        verilog_sources=sources,
        toplevel="cpu",  # Top-level Verilog module
        module="simple_core_cocotb",  # Name of the cocotb test module
        simulator="icarus",  # Specify the simulator you're using, e.g., "icarus", "verilator"
        waves=True,
    )

# def test_riscv_simple_sv():
#     verilog_dir = os.path.join(current_dir, "cores", "riscv-simple-sv")
#     sys.path.append(verilog_dir)
#     sources = glob.glob(os.path.join(verilog_dir, "*.sv"))
#     sources += glob.glob(os.path.join(verilog_dir, "common/*.sv"))
#     run(
#         verilog_sources=sources,
#         includes=[verilog_dir, verilog_dir + "/common"],
#         toplevel="toplevel",  # Top-level Verilog module
#         module="riscv_simple_sv_cocotb",  # Name of the cocotb test module
#         simulator="icarus",  # Specify the simulator you're using, e.g., "icarus", "verilator"
#         waves=False,
#     )
