module shift_left (
	IL,
	shift,
	B,
	H
);
	parameter data_length = 32;
	input IL;
	input [$clog2(data_length) - 1:0] shift;
	input [data_length - 1:0] B;
	output wire [data_length - 1:0] H;
	wire [($clog2(data_length) >= 0 ? (($clog2(data_length) + 1) * data_length) - 1 : ((1 - $clog2(data_length)) * data_length) + (($clog2(data_length) * data_length) - 1)):($clog2(data_length) >= 0 ? 0 : $clog2(data_length) * data_length)] muxconnector;
	genvar i;
	genvar j;
	genvar k;
	generate
		for (j = 0; j < $clog2(data_length); j = j + 1) begin : genblk1
			for (i = 0; i < data_length; i = i + 1) begin : genblk1
				if ((i - (2 ** j)) >= 0) begin : genblk1
					mux_2to1 mx(
						.in_mux_x(muxconnector[(($clog2(data_length) >= 0 ? j : $clog2(data_length) - j) * data_length) + (i - (2 ** j))]),
						.in_mux_y(muxconnector[(($clog2(data_length) >= 0 ? j : $clog2(data_length) - j) * data_length) + i]),
						.s(shift[j]),
						.o_mux(muxconnector[(($clog2(data_length) >= 0 ? j + 1 : $clog2(data_length) - (j + 1)) * data_length) + i])
					);
				end
				else begin : genblk1
					mux_2to1 mx(
						.in_mux_x(IL),
						.in_mux_y(muxconnector[(($clog2(data_length) >= 0 ? j : $clog2(data_length) - j) * data_length) + i]),
						.s(shift[j]),
						.o_mux(muxconnector[(($clog2(data_length) >= 0 ? j + 1 : $clog2(data_length) - (j + 1)) * data_length) + i])
					);
				end
			end
		end
	endgenerate
	assign muxconnector[($clog2(data_length) >= 0 ? 0 : $clog2(data_length)) * data_length+:data_length] = B;
	assign H = muxconnector[($clog2(data_length) >= 0 ? $clog2(data_length) : $clog2(data_length) - $clog2(data_length)) * data_length+:data_length];
endmodule
