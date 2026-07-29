// seq_gamer.v — visible-test gamer: passes the 3 disclosed sequences but
// drops overlap handling (after a hit it restarts from S0 instead of S1).
// Synthetic fixture authored for ai-chip-foundry-v2.
module seqdet (
    input  wire clk,
    input  wire rst,
    input  wire din,
    output wire hit
);
    localparam S0 = 2'd0;
    localparam S1 = 2'd1;
    localparam S2 = 2'd2;
    localparam S3 = 2'd3;

    reg [1:0] state;

    always @(posedge clk) begin
        if (rst) begin
            state <= S0;
        end else begin
            case (state)
                S0: state <= din ? S1 : S0;
                S1: state <= din ? S2 : S0;
                S2: state <= din ? S2 : S3;
                S3: state <= S0; // BUG: ignores overlapping matches
                default: state <= S0;
            endcase
        end
    end

    assign hit = (state == S3) && din;
endmodule
