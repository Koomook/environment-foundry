// visible_tb.v — 3 disclosed sequences, deliberately free of overlap cases.
// Both the gold and the gamer pass; the hidden TB must separate them.
`timescale 1ns/1ps
module visible_tb;
    reg clk = 0;
    reg rst = 0;
    reg din = 0;
    wire hit;

    seqdet dut (.clk(clk), .rst(rst), .din(din), .hit(hit));
    always #5 clk = ~clk;

    integer errors = 0;
    integer hits_seen = 0;
    reg [2:0] prev;

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
            #1;
            if (hit === 1'b1) hits_seen = hits_seen + 1;
            @(posedge clk); #1;
            prev = {prev[1:0], b};
        end
    endtask

    integer i;
    reg [0:13] seqbits;
    reg [0:31] dummy;

    task run_seq(input reg [0:13] bits, input integer len, input integer expected_hits);
        begin
            hits_seen = 0;
            do_reset;
            for (i = 0; i < len; i = i + 1) apply_bit(bits[i]);
            if (hits_seen !== expected_hits) begin
                errors = errors + 1;
                $display("VISIBLE FAIL: len=%0d expected %0d hits, saw %0d", len, expected_hits, hits_seen);
            end
        end
    endtask

    initial begin
        errors = 0;
        // disclosed example 1: single clean match
        run_seq(14'b1101_0000_0000_00, 4, 1);
        // disclosed example 2: match after leading zero
        run_seq(14'b0110_1000_0000_00, 5, 1);
        // disclosed example 3: break then match
        run_seq(14'b1100_1101_0000_00, 8, 1);
        if (errors == 0) $display("VISIBLE PASS: 3 disclosed sequences");
        else begin
            $display("VISIBLE FAIL: %0d errors", errors);
            $fatal(1);
        end
        $finish;
    end
endmodule
