// hidden_tb.v — exhaustive hidden behavioral grader for the sequential block.
// Replays ALL 2^14 = 16,384 input sequences of length 14, cycle-accurate,
// against an independent golden model (4-bit window == "1101").
`timescale 1ns/1ps
module hidden_tb;
    reg clk = 0;
    reg rst = 0;
    reg din = 0;
    wire hit;

    seqdet dut (.clk(clk), .rst(rst), .din(din), .hit(hit));
    always #5 clk = ~clk;

    integer seq;
    integer i;
    integer errors = 0;
    reg [13:0] bits;
    reg [2:0] prev;
    reg exp_hit;

    task do_reset;
        begin
            rst = 1; din = 0; prev = 3'b000;
            @(posedge clk); #1;
            rst = 0;
        end
    endtask

    task apply_bit(input reg b);
        begin
            din = b;
            #1; // settle Mealy output
            exp_hit = ({prev, b} == 4'b1101);
            if (hit !== exp_hit) begin
                errors = errors + 1;
                if (errors <= 10)
                    $display("MISMATCH seq=%0d bit=%0d prev=%b din=%b hit=%b expected=%b",
                             seq, i, prev, b, hit, exp_hit);
            end
            @(posedge clk); #1;
            prev = {prev[1:0], b};
        end
    endtask

    initial begin
        for (seq = 0; seq < 16384; seq = seq + 1) begin
            bits = seq[13:0];
            do_reset;
            for (i = 0; i < 14; i = i + 1) apply_bit(bits[i]);
        end
        if (errors == 0) begin
            $display("PASS: all 16384 sequences x 14 bits matched golden model (229376 cycle checks)");
        end else begin
            $display("FAIL: %0d cycle mismatches", errors);
            $fatal(1);
        end
        $finish;
    end
endmodule
