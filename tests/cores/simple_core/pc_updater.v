
// iverilog src/pc_updater.v src/ripple_carry_adder_subtractor.v src/full_adder_LL_nodelay.v 

module pc_updater (clk, rst, cword, imm, r, pc, ZCNVFlags);

input wire [31:0] r;
input wire [31:0] imm;
input wire clk, rst;
input wire [3:0] ZCNVFlags;
output reg [31:0] pc;

input wire [22:0] cword;

`define instType cword[3:0]
`define fun3 cword[6:4]

`define Z_flag ZCNVFlags[3]
`define C_flag ZCNVFlags[2]
`define N_flag ZCNVFlags[1]
`define V_flag ZCNVFlags[0]

`define BEQ 3'b000
`define BNE 3'b001
`define BLT 3'b100
`define BGE 3'b101
`define BLTU 3'b110
`define BGEU 3'b111


reg [31:0] A, B;
wire [31:0] S;
wire Cout;

ripple_carry_adder_subtractor adder ( .Cin(1'b0), .A(A), .B(B), .Cout(Cout), .S(S));

initial begin
    A = 0;
    B = 0;
    pc = 0;
end

always @(posedge clk or negedge rst) begin
    if (!rst) begin
        // Reset logic
        A <= 0;
        B <= 0;
        pc <= 0;
    end
    else begin
        if (`instType == 4'd7) begin // if jalr
            A <= r;
        end
        else begin
            A <= pc;
        end

        if (`instType==4'd8 || `instType==4'd7 || `instType==4'd5 || `instType==4'd6 && (
            (`fun3==`BEQ && `Z_flag==1'b1) || 
            (`fun3==`BNE && `Z_flag==1'b0) || 
            (`fun3==`BLT && (`N_flag^`V_flag)==1'b1) || 
            (`fun3==`BGE && (`N_flag^`V_flag)==1'b0) || 
            (`fun3==`BLTU && `C_flag==1'b1) || 
            (`fun3==`BGEU && `C_flag==1'b0)  // TODO: check on real bgeu instructions
        ) ) begin // if branch, jal, jalr, auipc
            B <= imm;
        end
        else begin
            B <= 32'd4; // compressed instructions are not supported
        end
    end
end

always @(S) begin
    pc = {S[31:2], 2'b0};
end

endmodule

// load, imm, store, reg, lui, auipc, brnch, jalr, jal
// 0     1    2      3    4    5      6      7     8
