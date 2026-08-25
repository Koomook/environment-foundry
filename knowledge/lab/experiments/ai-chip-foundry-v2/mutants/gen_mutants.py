"""Generate 8 deterministic single-point mutants of rtl/seq_gold.v.

Each mutant is produced by an exact string replacement on the pristine gold
source; the script fails loudly if a replacement does not match exactly once.
Expected outcomes against the hidden exhaustive grader (iteration 2):

- 7 behavior-changing mutants MUST be killed (hidden grader is strong).
- seq_mut06 is an EQUIVALENT mutant (state-encoding swap, same behavior) and
  is EXPECTED TO SURVIVE — it calibrates the mutation score and, in
  iteration 3, exposes that quality metrics differ even for identical
  behavior.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GOLD = (ROOT.parent / "rtl" / "seq_gold.v").read_text()
OUT = ROOT / "generated"
OUT.mkdir(parents=True, exist_ok=True)

MUTATIONS = [
    {
        "name": "seq_mut01_no_overlap",
        "description": "S3 transition drops overlap (restart at S0 after hit)",
        "expected": "KILLED",
        "replacements": [
            ('S3: state <= din ? S1 : S0; // overlap: suffix "1" is a prefix',
             "S3: state <= S0; // MUT01"),
        ],
    },
    {
        "name": "seq_mut02_s2_reentry",
        "description": "S2 on din=1 falls back to S1 (breaks '11101')",
        "expected": "KILLED",
        "replacements": [
            ("S2: state <= din ? S2 : S3;",
             "S2: state <= din ? S1 : S3; // MUT02"),
        ],
    },
    {
        "name": "seq_mut03_pattern_1100",
        "description": "detects 1100 instead of 1101 (hit polarity flip)",
        "expected": "KILLED",
        "replacements": [
            ("assign hit = (state == S3) && din;",
             "assign hit = (state == S3) && !din; // MUT03"),
        ],
    },
    {
        "name": "seq_mut04_s1_wrong_zero",
        "description": "S1 on din=0 jumps to S2 instead of S0",
        "expected": "KILLED",
        "replacements": [
            ("S1: state <= din ? S2 : S0;",
             "S1: state <= din ? S2 : S2; // MUT04"),
        ],
    },
    {
        "name": "seq_mut05_registered_hit",
        "description": "hit registered by one cycle (timing shift, same pattern)",
        "expected": "KILLED",
        "replacements": [
            ("assign hit = (state == S3) && din;",
             "reg hit_r;\n    always @(posedge clk) hit_r <= (state == S3) && din;\n"
             "    assign hit = hit_r; // MUT05"),
        ],
    },
    {
        "name": "seq_mut06_equiv_encoding",
        "description": "EQUIVALENT: swaps S2/S3 encodings, behavior identical",
        "expected": "SURVIVES",
        "replacements": [
            ("localparam S2 = 2'd2; // matched \"11\"",
             "localparam S2 = 2'd3; // matched \"11\" (MUT06)"),
            ("localparam S3 = 2'd3; // matched \"110\"",
             "localparam S3 = 2'd2; // matched \"110\" (MUT06)"),
        ],
    },
    {
        "name": "seq_mut07_reset_to_s1",
        "description": "reset lands in S1 instead of S0 (reset semantics)",
        "expected": "KILLED",
        "replacements": [
            ("if (rst) begin\n            state <= S0;",
             "if (rst) begin\n            state <= S1; // MUT07"),
        ],
    },
    {
        "name": "seq_mut08_false_start",
        "description": "S0 advances on din=0 as well (false start)",
        "expected": "KILLED",
        "replacements": [
            ("S0: state <= din ? S1 : S0;",
             "S0: state <= din ? S1 : S1; // MUT08"),
        ],
    },
]

HEADER = "// {name}.v — generated mutant of rtl/seq_gold.v\n// mutation: {description}\n// expected vs hidden grader: {expected}\n\n"

manifest = []
for mut in MUTATIONS:
    text = GOLD
    for old, new in mut["replacements"]:
        count = text.count(old)
        if count != 1:
            raise SystemExit(
                f"FATAL: mutation {mut['name']} pattern matched {count} times (expected 1): {old!r}"
            )
        text = text.replace(old, new)
    path = OUT / f"{mut['name']}.v"
    path.write_text(HEADER.format(**mut) + text)
    manifest.append({k: mut[k] for k in ("name", "description", "expected")})

(OUT / "manifest.json").write_text(
    __import__("json").dumps({"mutants": manifest}, ensure_ascii=False, indent=2) + "\n"
)
print(f"generated {len(manifest)} mutants in {OUT}")
