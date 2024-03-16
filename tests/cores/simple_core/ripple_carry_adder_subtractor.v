module ripple_carry_adder_subtractor #(
    parameter N = 32
) (
    input Cin,
    input [N-1:0] A,
    input [N-1:0] B,
    output Cout,
    output [N-1: 0] S
);
    
    wire [N:0] carry_connector;
    wire [N-1:0] B_xor;
    assign carry_connector[0] = Cin;

    genvar i;
    generate
    for (i = 0; i< N; i= i+ 1) begin: ripple
        xor(B_xor[i], B[i], carry_connector[0]);
        full_adder_LL_nodelay full_adder(.A(A[i]), .B(B_xor[i]), .Cin(carry_connector[i]),
         .S(S[i]), .Cout(carry_connector[i+1]));
    end
    endgenerate

    assign Cout = carry_connector[0] ^ carry_connector[N];
endmodule
