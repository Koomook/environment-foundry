# Task: unsigned 8-bit saturating adder

Implement a combinational Verilog module:

```verilog
module sat_add8(
  input  wire [7:0] a,
  input  wire [7:0] b,
  output wire [7:0] y
);
```

For every input pair, `y` must equal `min(a + b, 255)`. The module must contain
no clock, latch, delay, system task, or additional I/O. It must compile under
Icarus Verilog and synthesize under Yosys.
