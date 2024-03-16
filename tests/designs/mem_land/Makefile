# Makefile

# defaults
SIM ?= icarus
TOPLEVEL_LANG ?= verilog

PWD=$(shell pwd)

RISCV_COCOTB?=$(PWD)/../..
VERILOG_SOURCES += $(RISCV_COCOTB)/tests/designs/mem_land/*.v

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
TOPLEVEL = top_mem

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
