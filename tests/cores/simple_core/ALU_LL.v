module ALU_LL (
    input [3:0] G_sel,
    input [31:0] A,
    input [31:0] B,
    output reg [31:0] G,
    output [3:0] ZCNVFlags
);
    //reg carry_in;
    wire carry_out;
    wire [31:0] Arithmetic_result, Logical_result;
    
    //TODO new adder topology needed
    ripple_carry_adder_subtractor #(.N(32)) rcas(.A(A), .B(B), .Cin(G_sel[0]),
     .Cout(ZCNVFlags[2]), .S(Arithmetic_result));

    logical_unit lu(.L_sel(G_sel[2:1]), .A(A), .B(B), .G(Logical_result));

    parameter 
    ADD = 4'b0000,
    SUB = 4'b0001,
    XOR = 4'b1000,
    OR =  4'b1100,
    AND = 4'b1110;

    wire signed [31:0]  A_signed = A, B_signed = B;
    
    
    always @(*) begin
        if(G_sel[3])
            G = Logical_result;
        else
            G = Arithmetic_result;        
    end

    //Overflow detection circuit
    //ADD => G_sel[0] == 0
    //SUB => G_sel[0] == 1
    //if in addition both A and B are positive and the result is negative or both A and B are negative and the result is positive OR
    //in subtraction A is negative and B is positive and the result is positive or A is positive and B is negative and the result is negative
    //then overflow is detected
    assign ZCNVFlags[0] =   (!G_sel[0] & A_signed[31] & B_signed[31] & !Arithmetic_result[31]) |
                            (!G_sel[0] & !A_signed[31] & !B_signed[31] & Arithmetic_result[31])|
                            (G_sel[0] & A_signed[31] & !B_signed[31] & !Arithmetic_result[31])|
                            (G_sel[0] & !A_signed[31] & B_signed[31] & Arithmetic_result[31]);
    //Negative flag checks the sign bit of the result
    assign ZCNVFlags[1] = Arithmetic_result[31];

    //Zero detection is done by ORing the bits of the result
    assign ZCNVFlags[3] = !(|Arithmetic_result);
endmodule
