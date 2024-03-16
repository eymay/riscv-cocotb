
module instr_dec ( inst, cword);

input wire [31:0] inst;
output reg [22:0] cword;

`define instType cword[3:0]
`define fun3 cword[6:4]
`define fun7 cword[7]
`define rd cword[12:8]
`define rs1 cword[17:13]
`define rs2 cword[22:18]

// TODO: not tested
always @(*) begin
    if (inst[2]==1'b1) begin
        case (inst[6:3])
            4'b0110: `instType = 4; // lui
            4'b0010: `instType = 5; // auipc
            4'b1101: `instType = 8; // jal
            default: `instType = 7; // jalr
        endcase
    end
    else begin
        case (inst[6:4])
            3'b110: `instType = 6; // brnch
            3'b000: `instType = 0; // load
            3'b010: `instType = 2; // store
            3'b001: `instType = 1; // imm
            3'b011: `instType = 3; // r
        endcase
    end

    `fun3 = inst[14:12];
    `rd = inst[11:7];
    `rs1 = inst[19:15];
    `rs2 = inst[24:20];
    `fun7 = inst[30];

end

endmodule

// load, imm, store, reg, lui, auipc, brnch, jalr, jal
// 0     1    2      3    4    5      6      7     8
