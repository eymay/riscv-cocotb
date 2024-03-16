
module shift_right_placeholder (
    input IR, input [4:0] shift, input [31:0] B,
    output [31:0] H
);

always @(*) begin
    if (IR==1'b0) H <= B >> shift;
    else H <= B >>> shift;
end

endmodule
