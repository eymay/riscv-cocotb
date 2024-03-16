

module immed_gen (cword, inst, imm);

input wire [22:0] cword;
input wire [31:0] inst;
output reg [31:0] imm;

`define instType cword[3:0]

always @(*) begin
    case (`instType)

        // lui & auipc
        4'd4, 4'd5:         imm = {inst[31:12], {12{1'b0}}};
        // jal
        4'd8:               imm = {{12{inst[31]}},  inst[19:12], inst[20], inst[30:21], 1'b0};
        // brnch
        4'd6:               imm = {{20{inst[31]}},  inst[7], inst[30:25], inst[11:8], 1'b0};
        // store
        4'd2:               imm = {{21{inst[31]}},  inst[30:25], inst[11:7]};
        // load, imm, jalr
        4'd0, 4'd1, 4'd7:   imm = {{21{inst[31]}},  inst[30:20]};

        default:            imm = 32'b1;
    endcase
end

endmodule

// load, imm, store, reg, lui, auipc, brnch, jalr, jal
// 0     1    2      3    4    5      6      7     8
