module shifter (
	S,
	shift,
	B,
	H
);
	input [1:0] S;
	input [4:0] shift;
	input [31:0] B;
	output reg [31:0] H;
	parameter SLL = 2'b00;
	parameter SRL = 2'b10;
	parameter SRA = 2'b11;
	reg reg_IR;
	reg [31:0] reg_B;
	wire [31:0] reg_H;
	shift_right #(.data_length(32)) sr(
		.IR(reg_IR),
		.shift(shift),
		.B(reg_B),
		.H(reg_H)
	);
	always @(*) begin : instruction_select
		case (S)
			SLL: begin
				reg_IR = 1'b0;
				begin : sv2v_autoblock_1
					reg [31:0] _sv2v_strm_26DCB_inp;
					reg [31:0] _sv2v_strm_26DCB_out;
					integer _sv2v_strm_26DCB_idx;
					_sv2v_strm_26DCB_inp = {B};
					for (_sv2v_strm_26DCB_idx = 0; _sv2v_strm_26DCB_idx <= 31; _sv2v_strm_26DCB_idx = _sv2v_strm_26DCB_idx + 1)
						_sv2v_strm_26DCB_out[31 - _sv2v_strm_26DCB_idx-:1] = _sv2v_strm_26DCB_inp[_sv2v_strm_26DCB_idx+:1];
					reg_B = _sv2v_strm_26DCB_out << 0;
				end
				begin : sv2v_autoblock_2
					reg [31:0] _sv2v_strm_4B9FA_inp;
					reg [31:0] _sv2v_strm_4B9FA_out;
					integer _sv2v_strm_4B9FA_idx;
					_sv2v_strm_4B9FA_inp = {reg_H};
					for (_sv2v_strm_4B9FA_idx = 0; _sv2v_strm_4B9FA_idx <= 31; _sv2v_strm_4B9FA_idx = _sv2v_strm_4B9FA_idx + 1)
						_sv2v_strm_4B9FA_out[31 - _sv2v_strm_4B9FA_idx-:1] = _sv2v_strm_4B9FA_inp[_sv2v_strm_4B9FA_idx+:1];
					H = _sv2v_strm_4B9FA_out << 0;
				end
			end
			SRL: begin
				reg_IR = 1'b0;
				reg_B = B;
				H = reg_H;
			end
			SRA: begin
				reg_IR = B[31];
				reg_B = B;
				H = reg_H;
			end
		endcase
	end
endmodule
