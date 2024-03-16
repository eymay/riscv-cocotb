module instr_mem(
    input [6:0] r_addr_imem,
    output reg [31:0] r_data_imem
);

reg [7:0] imem [0:127];

initial begin
    integer i;
    for (i = 0; i < 128; i = i + 1) begin
        imem[i] = 8'b0; // Zero initialize each element
    end
end

always @(*) begin
    // output is not 4-aligned but we assume pc%4==0 always holds
    r_data_imem = {imem[r_addr_imem + 3],imem[r_addr_imem + 2],imem[r_addr_imem + 1],imem[r_addr_imem]};    
end
endmodule
