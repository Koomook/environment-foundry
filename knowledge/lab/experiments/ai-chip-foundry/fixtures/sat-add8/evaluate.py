from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path


TESTBENCH = r"""
module tb;
  reg [7:0] a;
  reg [7:0] b;
  wire [7:0] y;
  integer i;
  integer j;
  integer expected;

  sat_add8 dut(.a(a), .b(b), .y(y));

  initial begin
    for (i = 0; i < 256; i = i + 1) begin
      for (j = 0; j < 256; j = j + 1) begin
        a = i[7:0];
        b = j[7:0];
        #1;
        expected = i + j;
        if (expected > 255)
          expected = 255;
        if (y !== expected[7:0]) begin
          $display("MISMATCH a=%0d b=%0d got=%0d expected=%0d", i, j, y, expected);
          $fatal(1);
        end
      end
    end
    $display("FUNCTIONAL_PASS cases=65536");
    $finish;
  end
endmodule
"""


def run(command: list[str], timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def version(command: list[str]) -> str:
    result = run(command, timeout=5)
    text = (result.stdout or result.stderr).splitlines()
    return text[0] if text else "unknown"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: evaluate.py <candidate.v>", file=sys.stderr)
        return 2

    candidate = Path(sys.argv[1]).resolve()
    if not candidate.is_file():
        print(json.dumps({"hard_failure": "candidate_not_found", "path": str(candidate)}))
        return 2

    started = time.monotonic()
    source = candidate.read_bytes()
    result: dict[str, object] = {
        "artifact_class": "interactive_environment",
        "candidate": str(candidate),
        "candidate_sha256": hashlib.sha256(source).hexdigest(),
        "tools": {
            "iverilog": version(["iverilog", "-V"]),
            "yosys": version(["yosys", "-V"]),
        },
        "functional": {"pass": False, "cases": 65_536},
        "synthesis": {"pass": False, "generic_cell_count": None},
        "hard_failure": None,
    }

    try:
        with tempfile.TemporaryDirectory(prefix="ai-chip-foundry-") as raw_tmp:
            tmp = Path(raw_tmp)
            tb = tmp / "tb.v"
            executable = tmp / "sim.out"
            tb.write_text(TESTBENCH)

            compile_result = run(
                ["iverilog", "-g2012", "-s", "tb", "-o", str(executable), str(candidate), str(tb)]
            )
            if compile_result.returncode != 0:
                result["hard_failure"] = "compile_failed"
                result["compile_stderr"] = compile_result.stderr[-4000:]
            else:
                simulation = run(["vvp", str(executable)])
                functional_pass = (
                    simulation.returncode == 0 and "FUNCTIONAL_PASS cases=65536" in simulation.stdout
                )
                result["functional"] = {
                    "pass": functional_pass,
                    "cases": 65_536,
                    "first_failure": next(
                        (line for line in simulation.stdout.splitlines() if line.startswith("MISMATCH")),
                        None,
                    ),
                }
                if not functional_pass:
                    result["hard_failure"] = "functional_mismatch"

            synth_script = (
                f"read_verilog {candidate}; "
                "synth -top sat_add8; "
                "stat"
            )
            synthesis = run(["yosys", "-p", synth_script])
            synth_text = synthesis.stdout + "\n" + synthesis.stderr
            cell_counts = re.findall(
                r"(?:Number of cells:\s*|^\s*)(\d+)\s+cells\s*$",
                synth_text,
                flags=re.MULTILINE,
            )
            result["synthesis"] = {
                "pass": synthesis.returncode == 0,
                "generic_cell_count": int(cell_counts[-1]) if cell_counts else None,
            }
            if synthesis.returncode != 0 and result["hard_failure"] is None:
                result["hard_failure"] = "synthesis_failed"
                result["synthesis_stderr"] = synthesis.stderr[-4000:]
    except subprocess.TimeoutExpired as exc:
        result["hard_failure"] = "timeout"
        result["timeout_command"] = exc.cmd

    result["elapsed_seconds"] = round(time.monotonic() - started, 4)
    result["accepted"] = bool(
        result["functional"]["pass"]  # type: ignore[index]
        and result["synthesis"]["pass"]  # type: ignore[index]
        and result["hard_failure"] is None
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
