module top_mem();
    // Dummy inputs for demonstration purposes

    reg [6:0] addr;
    wire [31:0] data_out_1byte;
    wire [31:0] data_out_2byte;
    wire [31:0] data_out_4byte;

    instr_mem_1byte u_instr_mem_1byte(
        .r_addr_imem(addr),
        .r_data_imem(data_out_1byte)
    );

    instr_mem_2byte u_instr_mem_2byte(
        .r_addr_imem(addr),
        .r_data_imem(data_out_2byte)
    );

    instr_mem_4byte u_instr_mem_4byte(
        .r_addr_imem(addr),
        .r_data_imem(data_out_4byte)
    );
endmodule
