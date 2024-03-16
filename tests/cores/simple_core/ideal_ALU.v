module ALU (
    input [3:0] G_sel,
    input [31:0] A,
    input [31:0] B,
    output reg [31:0] G,
    output  [3:0] ZCNVFlags
);
    
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

    wire signed [31:0]  A_signed = A, B_signed = B;
    
    
    always @(*) begin
        case(G_sel)
        ADD: G = A + B;
        SUB: G = A - B;
        SLL: G = A << B;
        SLT: G = (A_signed > B_signed) ? 1:0;
        SLTU: G = (A > B) ? 1:0;
        XOR: G = A^B;
        OR: G= A|B;
        AND: G = A&B; 
        endcase
        
    end


endmodule
