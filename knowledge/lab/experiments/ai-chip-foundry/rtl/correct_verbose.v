module alu #(parameter W = 4) (
  input  wire [W-1:0] a,
  input  wire [W-1:0] b,
  input  wire [1:0] op,
  output reg  [W-1:0] y
);
  integer i;
  reg carry;
  reg [W-1:0] sum;

  always @* begin
    sum = {W{1'b0}};
    carry = 1'b0;
    for (i = 0; i < W; i = i + 1) begin
      sum[i] = a[i] ^ b[i] ^ carry;
      carry = (a[i] & b[i]) | (a[i] & carry) | (b[i] & carry);
    end
    case (op)
      2'b00: y = sum;
      2'b01: y = a ^ b;
      2'b10: y = a & b;
      default: y = a | b;
    endcase
  end
endmodule
