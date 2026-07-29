// seq_gold.v — overlapping "1101" sequence detector (Mealy hit), GOLD reference.
// Synthetic fixture authored for ai-chip-foundry-v2. No third-party IP.
module seqdet (
    input  wire clk,
    input  wire rst,
    input  wire din,
    output wire hit
);
    localparam S0 = 2'd0; // nothing matched
    localparam S1 = 2'd1; // matched "1"
    localparam S2 = 2'd2; // matched "11"
    localparam S3 = 2'd3; // matched "110"

    reg [1:0] state;

    always @(posedge clk) begin
        if (rst) begin
            state <= S0;
        end else begin
            case (state)
                S0: state <= din ? S1 : S0;
                S1: state <= din ? S2 : S0;
                S2: state <= din ? S2 : S3;
                S3: state <= din ? S1 : S0; // overlap: suffix "1" is a prefix
                default: state <= S0;
            endcase
        end
    end

    assign hit = (state == S3) && din;
endmodule
