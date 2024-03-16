// `define DEBUG_MEM



module data_mem (clk, rst, rd_addr0, wr_addr0, wr_din0, we0, rd_dout0, wr_strb);
    parameter DEPTH=128;
    // note: we remove WIDTH as a parameter and give it a fixed 32 bit value, because it's integral in the logic
    // of the memory how it should respond to storing bytes and halfwords.

    input wire clk, rst, we0;
    // read port 0
    input wire [$clog2(DEPTH)-1:0] rd_addr0;
    output [31:0] rd_dout0;
    // write port 0
    input wire [$clog2(DEPTH)-1:0] wr_addr0; // note: this value selects the word, not the byte. wr_addr0=1 -> risc-v addresses 4,5,6,7
    input wire [31:0] wr_din0;
    input wire [2:0] wr_strb;
    // wr_strb = 000 -> store word
    // wr_strb = 001 -> store lower halfword
    // wr_strb = 010 -> nop
    // wr_strb = 011 -> store higher halfword
    // wr_strb = 100 -> store lowest byte
    // wr_strb = 101 -> store 2nd lowest byte
    // wr_strb = 110 -> store 3rd lowest byte
    // wr_strb = 111 -> store highest byte

    reg [31:0] mem [0:DEPTH-1];

    // initialize all registers to 0
    initial begin
        for (integer i = 0; i<DEPTH; i=i+1) begin
            mem[i] = {32{1'b0}};
        end
    end




    // write functionality. writes synchronously, on rising edge of clk.
    // all the write operations are programmed to be strictly little endian
    always @(posedge clk, rst) begin
       if (we0 && rst) begin
            case (wr_strb)
                 0: mem[wr_addr0][31:0] <= wr_din0[31:0];
                 1: mem[wr_addr0][15:0] <= wr_din0[15:0];
               /*2: NOP*/
                 3: mem[wr_addr0][31:16] <= wr_din0[15:0];
                 4: mem[wr_addr0][7:0] <= wr_din0[7:0];
                 5: mem[wr_addr0][15:8] <= wr_din0[7:0];
                 6: mem[wr_addr0][23:16] <= wr_din0[7:0];
                 7: mem[wr_addr0][31:24] <= wr_din0[7:0];
            endcase
        end

        `ifdef DEBUG_MEM
            printAll;
        `endif
    end

    // reset is async, works immediately. rst=0 means reset.
    always @(*) begin
        if (!rst) begin
            for (integer i = 0; i<DEPTH; i=i+1) begin
                mem[i] <= {32{1'b0}};
            end
        end
    end

    // read functionality. reads asynchronously.
    // currently rd_dout0 is a reg, but this could be changed to wire & some 'and' logic.
       assign rd_dout0 = mem[rd_addr0];

    


endmodule


