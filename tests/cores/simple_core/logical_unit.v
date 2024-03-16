module logical_unit (
    input [1:0] L_sel,
    input [31:0] A,
    input [31:0] B,
    output reg [31:0] G
);

    parameter 
    XOR = 2'b00,
    NOT = 2'b01,
    OR = 2'b10,
    AND = 2'b11;
    wire [31:0] AandB, AorB, AxorB, Anot;
    assign AandB = A&B;
    assign AorB = A|B;
    assign AxorB = A^B;
    assign Anot = ~A;
    always @(*) begin
        case(L_sel)
        XOR: G = AxorB;
        NOT: G = Anot;
        OR: G = AorB;
        AND: G = AandB;
        endcase
    end

endmodule
