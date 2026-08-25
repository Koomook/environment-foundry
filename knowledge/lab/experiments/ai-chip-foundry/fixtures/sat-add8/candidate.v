module sat_add8(
  input  wire [7:0] a,
  input  wire [7:0] b,
  output wire [7:0] y
);
  // Intentionally buggy seed: overflow wraps instead of saturating.
  assign y = a + b;
endmodule
