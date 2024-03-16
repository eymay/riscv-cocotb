module full_adder_LL_nodelay(
    input A, B, Cin, output S, Cout
    );
    
    wire axorb, aandb, axorbandcin;

    
    xor  (axorb, B, A);
    and (aandb, B, A);
    xor  (S, Cin, axorb);
    and (axorbandcin, Cin, axorb);
    or (Cout, aandb, axorbandcin);
endmodule