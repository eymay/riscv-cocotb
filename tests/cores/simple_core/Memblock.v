// `define DEBUG_MEM
module Memblock (clk, rst, rd_addr0, wr_addr0, wr_din0, we0, rd_dout0 );
    parameter WIDTH=1, DEPTH=1;

    input wire clk, rst, we0;
    // read port 0
    input wire [$clog2(DEPTH)-1:0] rd_addr0;
    output [WIDTH-1:0] rd_dout0; /// TODO DONE: made wire
    // write port 0
    input wire [$clog2(DEPTH)-1:0] wr_addr0;
    input wire [WIDTH-1:0] wr_din0;

    reg [WIDTH-1:0] mem [0:DEPTH-1];

    // initialize all registers to 0
    initial begin
        for (integer i = 0; i<DEPTH; i=i+1) begin
            mem[i] = {WIDTH{1'b0}};
        end
    end


    // write functionality. writes synchronously, on rising edge of clk.
    always @(posedge clk, rst) begin
       if (we0 && rst) begin
            mem[wr_addr0] = wr_din0;
        end

        `ifdef DEBUG_MEM
            printAll;
        `endif
    end

    // reset is async, works immediately. rst=0 means reset.
    always @(*) begin
        if (!rst) begin
            for (integer i = 0; i<DEPTH; i=i+1) begin
                mem[i] <= {WIDTH{1'b0}};
            end
        end
    end

    // read functionality. reads asynchronously.
    // currently rd_dout0 is a reg, but this could be changed to wire & some 'and' logic.
       assign rd_dout0 = mem[rd_addr0];



endmodule





