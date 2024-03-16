module n_bit_mux #(
    parameter N = 32
) (
    input s, input [N -1 :0] i_n_mux_x, input [N-1:0] i_n_mux_y, output reg [N-1:0] o_n_mux
);

    always @(*) begin
        
        if(!s)
            o_n_mux = i_n_mux_x;
        else
            o_n_mux = i_n_mux_y;
    end
    
endmodule
