module tb;
  parameter W = `TEST_WIDTH;
  reg [W-1:0] a;
  reg [W-1:0] b;
  reg [1:0] op;
  wire [W-1:0] y;
  reg [W-1:0] expected;
  integer ai;
  integer bi;
  integer oi;
  integer failures;

  alu #(.W(W)) dut(.a(a), .b(b), .op(op), .y(y));

  initial begin
    failures = 0;
    for (oi = 0; oi < 4; oi = oi + 1) begin
      for (ai = 0; ai < (1 << W); ai = ai + 1) begin
        for (bi = 0; bi < (1 << W); bi = bi + 1) begin
          a = ai; b = bi; op = oi; #1;
          case (op)
            0: expected = a + b;
            1: expected = a ^ b;
            2: expected = a & b;
            default: expected = a | b;
          endcase
          if (y !== expected) failures = failures + 1;
        end
      end
    end
    if (failures == 0) begin
      $display("PASS exhaustive width=%0d", W);
      $finish;
    end
    $display("FAIL exhaustive width=%0d failures=%0d", W, failures);
    $fatal(1);
  end
endmodule
