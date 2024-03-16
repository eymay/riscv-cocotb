
// iverilog -g2005-sv Datapath.sv hw6/FunctionUnit.v hw5/Datamemory.sv hw5/Regfile.v

module Datapath (clk, rst, cword, pc, imm, r_for_pc, funit_ZCNVFlags,
                datamem_rd_addr0, datamem_wr_addr0, datamem_wr_din0, datamem_we0, datamem_rd_dout0, datamem_wr_strb
);

// control word
input wire clk, rst;
input wire [22:0] cword;

`define instType cword[3:0]
`define fun3 cword[6:4]
`define fun7 cword[7]
`define rd cword[12:8]
`define rs1 cword[17:13]
`define rs2 cword[22:18]

// other stuff from control unit
input wire [31:0] pc;
input wire [31:0] imm;
output wire [31:0] r_for_pc;

// parts of function unit
reg [31:0] funit_A;
reg [31:0] funit_B;
reg [3:0] funit_FS;
output wire [3:0] funit_ZCNVFlags;
wire [31:0] funit_S;

// parts of datamem
output reg datamem_we0;
output reg [6:0] datamem_rd_addr0;
input wire [31:0] datamem_rd_dout0;
reg [31:0] datamem_out;
output reg [6:0] datamem_wr_addr0; // note: this value selects the word, not the byte. wr_addr0=1 -> risc-v addresses 4,5,6,7
output reg [31:0] datamem_wr_din0;
output reg [2:0] datamem_wr_strb;

// parts of regfile
reg regfile_we0;
reg [4:0] regfile_rd_addr0;
wire [31:0] regfile_rd_dout0; // rs1
reg [4:0] regfile_rd_addr1;
wire [31:0] regfile_rd_dout1;  // rs2
reg [4:0] regfile_wr_addr0;
reg [31:0] regfile_wr_din0;


FunctionUnit funit (
    .A(funit_A), .B(funit_B), .FS(funit_FS), .S(funit_S), .ZCNVFlags(funit_ZCNVFlags) );

regfile regfile (
    .clk(clk), 
    .rst(rst),
    .rd_addr0(regfile_rd_addr0),
    .rd_addr1(regfile_rd_addr1), 
    .wr_addr0(regfile_wr_addr0), 
    .wr_din0(regfile_wr_din0), 
    .we0(regfile_we0), 
    .rd_dout0(regfile_rd_dout0),
    .rd_dout1(regfile_rd_dout1));

assign r_for_pc = regfile_rd_dout0;

initial begin
    funit_A = 0;
    funit_B = 0;
    funit_FS = 0;
    datamem_we0 = 0;
    datamem_rd_addr0 = 0;
    datamem_wr_addr0 = 0;
    datamem_wr_din0 = 0;
    datamem_wr_strb = 0;
    regfile_we0 = 0;
    regfile_rd_addr0 = 0;
    regfile_rd_addr1 = 0;
    regfile_wr_addr0 = 0;
    regfile_wr_din0 = 0;
end

always @(*) begin

    // funit bindings
    case (`instType)
        // jal, jalr, auipc
        4'd8, 4'd7, 4'd5: funit_A <= pc;
        // load, imm, store, reg, lui, brnch
        4'd0, 4'd1, 4'd2, 4'd3, 4'd4, 4'd6: funit_A <= regfile_rd_dout0;
        default: funit_A <= -1; // this should never happen
    endcase

    case (`instType)
        // reg, branch
        4'd3, 4'd6: funit_B <= regfile_rd_dout1;
        // store, load, auipc, lui, imm
        4'd2, 4'd0, 4'd5, 4'd4, 4'd1: funit_B <= imm;
        // jal, jalr
        4'd7, 4'd8: funit_B <= 4;
        default: funit_B <= -1; // this should never happen
    endcase

    case (`instType)
        // reg
        4'd3: funit_FS <= {`fun3, `fun7};
        // imm
        4'd1: funit_FS <= {`fun3, 1'b0};
        // branch
        4'd6: funit_FS <= {4'b0001};
        default: funit_FS <= 4'b0; // in all other cases do addition
    endcase

    // datamem bindings

    // if store
    if (`instType == 4'd2) datamem_we0 <= 1;
    else datamem_we0 <= 0;

    datamem_rd_addr0 <= funit_S[31:2]; // TODO: test this :2 part
    datamem_wr_addr0 <= funit_S[31:2];
    datamem_wr_din0 <= regfile_rd_dout1;

    case (`fun3)
        // store word
        3'b010: datamem_wr_strb <= 3'b000;
        // store half
        3'b001: datamem_wr_strb <= {1'b0, imm[1], 1'b1};
        // store byte
        3'b000: datamem_wr_strb <= {1'b1, imm[1:0]};
    endcase

    case (`fun3)
        // LW
        3'b010: datamem_out <= datamem_rd_dout0;
        // LHU
        3'b101: begin
            // lower half
            if (imm[1] == 1'b0) datamem_out <= {{16{1'b0}}, datamem_rd_dout0[15:0]};
            // upper half
            else datamem_out <= {{16{1'b0}}, datamem_rd_dout0[31:16]};
        end
        // LH
        3'b001: begin
            // lower half
            if (imm[1] == 1'b0) datamem_out <= {{16{datamem_rd_dout0[15]}}, datamem_rd_dout0[15:0]};
            // upper half
            else datamem_out <= {{16{datamem_rd_dout0[31]}}, datamem_rd_dout0[31:16]};
        end
        // LBU
        3'b100: begin
            // lowest byte
            if      (imm[1:0] == 2'b00) datamem_out <= {{24{1'b0}}, datamem_rd_dout0[7:0]};
            else if (imm[1:0] == 2'b01) datamem_out <= {{24{1'b0}}, datamem_rd_dout0[15:8]};
            else if (imm[1:0] == 2'b10) datamem_out <= {{24{1'b0}}, datamem_rd_dout0[23:16]};
            else datamem_out <= {{24{1'b0}}, datamem_rd_dout0[31:24]};
        end
        // LB
        3'b000: begin
            // lowest byte
            if      (imm[1:0] == 2'b00) datamem_out <= {{24{datamem_rd_dout0[7]}}, datamem_rd_dout0[7:0]};
            else if (imm[1:0] == 2'b01) datamem_out <= {{24{datamem_rd_dout0[15]}}, datamem_rd_dout0[15:8]};
            else if (imm[1:0] == 2'b10) datamem_out <= {{24{datamem_rd_dout0[23]}}, datamem_rd_dout0[23:16]};
            else datamem_out <= {{24{datamem_rd_dout0[31]}}, datamem_rd_dout0[31:24]};
        end
    endcase


    // regfile bindings

    regfile_rd_addr0 <= `rs1;
    regfile_rd_addr1 <= `rs2;
    regfile_wr_addr0 <= `rd;
    
    case (`instType)
        // reg, imm, auipc, jal, jalr
        4'd3, 4'd1, 4'd5, 4'd7, 4'd8: regfile_wr_din0 <= funit_S;
        // load
        4'd0: regfile_wr_din0 <= datamem_out;
        // lui
        4'd4: regfile_wr_din0 <= imm;
        default: regfile_wr_din0 <= -1;
    endcase

    case (`instType)
        // branch, store
        4'd6, 4'd2: regfile_we0 <= 1'b0;
        default: regfile_we0 <= 1'b1;
    endcase
     
end

endmodule


// load, imm, store, reg, lui, auipc, brnch, jalr, jal
// 0     1    2      3    4    5      6      7     8
