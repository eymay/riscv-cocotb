`timescale 1ns / 1ps

module cpu (clk,rst);

input wire clk;
input wire rst;

wire [31:0] r_for_pc;
wire [22:0] cword;
wire [31:0] inst;
wire [31:0] imm;
wire [31:0] pc;
wire [3:0] ZCNVFlags;

// parts of datamem
wire datamem_we0;
wire [6:0] datamem_rd_addr0;
wire [31:0] datamem_rd_dout0;
wire [6:0] datamem_wr_addr0; // note: this value selects the word, not the byte. wr_addr0=1 -> risc-v addresses 4,5,6,7
wire [31:0] datamem_wr_din0;
wire [2:0] datamem_wr_strb;

control_unit cu (
    .clk(clk),
    .rst(rst),
    .cword(cword),
    .pc(pc),
    .imm(imm),
    .inst(inst),
    .r_for_pc(r_for_pc),
    .ZCNVFlags(ZCNVFlags));

Datapath dp (
    .clk(clk),
    .rst(rst),
    .cword(cword),
    .pc(pc),
    .imm(imm),
    .r_for_pc(r_for_pc),
    .funit_ZCNVFlags(ZCNVFlags),
    // parts connecting datapath and data_mem
    .datamem_rd_addr0(datamem_rd_addr0),
    .datamem_wr_addr0(datamem_wr_addr0),
    .datamem_wr_din0(datamem_wr_din0),
    .datamem_we0(datamem_we0),
    .datamem_rd_dout0(datamem_rd_dout0),
    .datamem_wr_strb(datamem_wr_strb));

instr_mem instr_mem (
    .r_addr_imem(pc[6:0]), // note: this must be changed according to the inst mem size
    .r_data_imem(inst));

data_mem data_mem (
    .clk(clk),
    .rst(rst),
    .rd_addr0(datamem_rd_addr0),
    .wr_addr0(datamem_wr_addr0),
    .wr_din0(datamem_wr_din0),
    .we0(datamem_we0),
    .rd_dout0(datamem_rd_dout0),
    .wr_strb(datamem_wr_strb));
endmodule
