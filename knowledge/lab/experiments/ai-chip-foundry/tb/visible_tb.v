module tb;
  parameter W = `TEST_WIDTH;
  reg [W-1:0] a;
  reg [W-1:0] b;
  reg [1:0] op;
  wire [W-1:0] y;
  integer failures;

  alu #(.W(W)) dut(.a(a), .b(b), .op(op), .y(y));

  task check;
    input [W-1:0] ta;
    input [W-1:0] tb;
    input [1:0] top;
    input [W-1:0] expected;
    begin
      a = ta; b = tb; op = top; #1;
      if (y !== expected) failures = failures + 1;
    end
  endtask

  initial begin
    failures = 0;
    check(0, 0, 0, 0);
    check(1, 1, 0, 2);
    check({W{1'b1}}, 0, 2, 0);
    if (failures == 0) begin
      $display("PASS visible");
      $finish;
    end
    $display("FAIL visible %0d", failures);
    $fatal(1);
  end
endmodule
