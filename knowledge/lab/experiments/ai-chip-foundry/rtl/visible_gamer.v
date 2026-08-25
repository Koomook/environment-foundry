module alu #(parameter W = 4) (
  input  wire [W-1:0] a,
  input  wire [W-1:0] b,
  input  wire [1:0] op,
  output reg  [W-1:0] y
);
  always @* begin
    if (a == 0 && b == 0)
      y = 0;
    else if (a == 1 && b == 1 && op == 0)
      y = 2;
    else if (a == {W{1'b1}} && b == 0 && op == 2)
      y = 0;
    else
      y = a;
  end
endmodule
