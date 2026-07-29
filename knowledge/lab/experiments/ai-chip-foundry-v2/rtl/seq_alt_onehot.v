// seq_alt_onehot.v — behaviorally identical to seq_gold, one-hot encoding.
// Used in iteration 3: same behavior, different RTL style -> does the
// generic cell-count proxy rank it the same as liberty-mapped area/delay?
// Synthetic fixture authored for ai-chip-foundry-v2.
module seqdet (
    input  wire clk,
    input  wire rst,
    input  wire din,
    output wire hit
);
    reg [3:0] state; // state[0]=S0 ... state[3]=S3

    always @(posedge clk) begin
        if (rst) begin
            state <= 4'b0001;
        end else begin
            case (1'b1)
                state[0]: state <= din ? 4'b0010 : 4'b0001;
                state[1]: state <= din ? 4'b0100 : 4'b0001;
                state[2]: state <= din ? 4'b0100 : 4'b1000;
                state[3]: state <= din ? 4'b0010 : 4'b0001;
                default:  state <= 4'b0001;
            endcase
        end
    end

    assign hit = state[3] && din;
endmodule
