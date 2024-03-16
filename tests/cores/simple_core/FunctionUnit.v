module FunctionUnit (
    input [31:0] A,
    input [31:0] B,
    input [3:0] FS,
    output [3:0] ZCNVFlags,
    output reg [31:0] S
);
    wire [31:0] ALU_result, Shift_result;
    wire signed [31:0]  A_signed = A, B_signed = B;

        parameter 
    ADD = 4'b0000,
    SUB = 4'b0001,
    SLL = 4'b0010,
    SLT = 4'b0100,
    SLTU = 4'b0110,
    XOR = 4'b1000,
    SRL = 4'b1010,
    SRA = 4'b1011,
    OR = 4'b1100,
    AND = 4'b1110;

    ALU_LL alu(.G_sel(FS), .A(A), .B(B), .G(ALU_result), .ZCNVFlags(ZCNVFlags));
    shifter s(.S({FS[3], FS[0]}), .shift(B[4:0]), .B(A), .H(Shift_result));

    always @(*) begin
        case (FS)
            ADD, SUB, XOR, OR, AND:
                S = ALU_result;
            SLL, SRL, SRA:
                S = Shift_result;
            SLT:
                S = (A_signed < B_signed) ? 1:0;
            SLTU:
                S = (A < B) ? 1:0;

        endcase
    end


    
endmodule
