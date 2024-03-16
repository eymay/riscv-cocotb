module mux_2to1 (
    input in_mux_x, in_mux_y, s, output reg o_mux
);
    always @(*) begin
        if(s)
            o_mux = in_mux_x;
        else
            o_mux = in_mux_y;
    end
    
endmodule