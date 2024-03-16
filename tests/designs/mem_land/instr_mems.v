module instr_mem_1byte(
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

module instr_mem_2byte(
  input [6:0] r_addr_imem,
  output reg [31:0] r_data_imem
);

  reg [15:0] imem [0:63]; // 128 elements of 1 byte each (can hold 64 2-byte instructions)

initial begin
    integer i;
    for (i = 0; i < 64; i = i + 1) begin
        imem[i] = 16'b0; // Zero initialize each element
    end
end

  always @(*) begin
    // Combine two consecutive elements for 16-bit instruction
    r_data_imem = {imem[r_addr_imem + 1], imem[r_addr_imem]};
  end
endmodule


module instr_mem_4byte(
  input [6:0] r_addr_imem,
  output reg [31:0] r_data_imem
);

  reg [31:0] imem [0:31]; // 128 elements of 1 byte each

initial begin
    integer i;
    for (i = 0; i < 32; i = i + 1) begin
        imem[i] = 32'b0; // Zero initialize each element
    end
end

  always @(*) begin
    // Access only the addressed element
    r_data_imem = imem[r_addr_imem];
  end
endmodule
