from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RTL = ROOT / "rtl"
TB = ROOT / "tb"
RESULTS = ROOT / "results"
CANDIDATES = [
    "syntax_broken",
    "visible_gamer",
    "correct_verbose",
    "correct_compact",
]


def run(cmd: list[str], cwd: Path) -> dict:
    process = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    return {
        "passed": process.returncode == 0,
        "returncode": process.returncode,
        "stdout_tail": process.stdout[-1200:],
        "stderr_tail": process.stderr[-1200:],
    }


def simulate(candidate: str, tb_name: str, width: int, work: Path) -> dict:
    output = work / f"{candidate}-{tb_name}-w{width}.out"
    compile_result = run(
        [
            "iverilog",
            "-g2012",
            f"-DTEST_WIDTH={width}",
            "-o",
            str(output),
            str(RTL / f"{candidate}.v"),
            str(TB / tb_name),
        ],
        work,
    )
    if not compile_result["passed"]:
        return {"compile": compile_result, "simulation": None, "passed": False}
    simulation = run(["vvp", str(output)], work)
    return {
        "compile": compile_result,
        "simulation": simulation,
        "passed": simulation["passed"],
    }


def synthesize(candidate: str, width: int, work: Path) -> dict:
    stat_path = work / f"{candidate}-w{width}-stat.json"
    script = (
        f"read_verilog -defer {RTL / f'{candidate}.v'}; "
        f"chparam -set W {width} alu; hierarchy -top alu; "
        "proc; flatten; opt; techmap; opt; abc -g simple; clean; "
        f"tee -o {stat_path} stat -json"
    )
    result = run(["yosys", "-q", "-p", script], work)
    if not result["passed"] or not stat_path.exists():
        return {"passed": False, "tool": result, "cell_count": None}
    stat = json.loads(stat_path.read_text())
    module = stat["modules"]["\\alu"]
    return {
        "passed": True,
        "tool": result,
        "cell_count": module["num_cells"],
        "cell_types": module["num_cells_by_type"],
    }


def write_result(number: int, payload: dict) -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    path = RESULTS / f"iteration-{number}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def main() -> None:
    missing = [tool for tool in ("iverilog", "vvp", "yosys") if not shutil.which(tool)]
    if missing:
        raise SystemExit(f"Missing required tools: {', '.join(missing)}")

    with tempfile.TemporaryDirectory(prefix="ef-chip-foundry-") as raw_work:
        work = Path(raw_work)

        iteration_1 = {
            "iteration": 1,
            "hypothesis": "A real compiler transition is enough to reject structurally invalid actions.",
            "artifact": "Icarus Verilog compile results",
            "metric": "compile pass/fail",
            "stop_rule": "Stop if the known syntax error compiles or valid candidates fail.",
            "results": {
                candidate: simulate(candidate, "visible_tb.v", 4, work)["compile"]
                for candidate in CANDIDATES
            },
            "next_hypothesis": "Compilation is necessary but cannot establish functional correctness.",
        }
        write_result(1, iteration_1)

        iteration_2_results = {
            candidate: simulate(candidate, "visible_tb.v", 4, work)
            for candidate in CANDIDATES
            if candidate != "syntax_broken"
        }
        iteration_2 = {
            "iteration": 2,
            "hypothesis": "A few visible examples will accept at least one behaviorally wrong candidate.",
            "artifact": "Visible smoke-test replay",
            "metric": "three visible examples passed",
            "stop_rule": "Stop if smoke tests already separate the gamer from correct implementations.",
            "results": iteration_2_results,
            "observed": "visible_gamer passes the disclosed examples by construction.",
            "next_hypothesis": "Hidden exhaustive behavior is required before optimizing design quality.",
        }
        write_result(2, iteration_2)

        iteration_3_results = {
            candidate: simulate(candidate, "exhaustive_tb.v", 4, work)
            for candidate in CANDIDATES
            if candidate != "syntax_broken"
        }
        iteration_3 = {
            "iteration": 3,
            "hypothesis": "Exhaustive tests on a bounded block reject visible-test gaming.",
            "artifact": "Hidden exhaustive functional replay",
            "metric": "all 1,024 width-4 input/op combinations passed",
            "stop_rule": "Stop if visible_gamer passes or either known-correct implementation fails.",
            "results": iteration_3_results,
            "next_hypothesis": "Once correctness is gated, synthesis can provide a reproducible but limited quality signal.",
        }
        write_result(3, iteration_3)

        iteration_4_results = {
            candidate: synthesize(candidate, 4, work)
            for candidate in ("correct_verbose", "correct_compact")
        }
        iteration_4 = {
            "iteration": 4,
            "hypothesis": "Generic synthesis can rank equivalent RTL candidates without a proprietary PDK.",
            "artifact": "Yosys generic mapped cell statistics",
            "metric": "generic cell count after a frozen synthesis recipe",
            "stop_rule": "Reject this as a decision metric if rankings are tied or unstable across replay.",
            "results": iteration_4_results,
            "limitations": "Cell count is an early area proxy, not PPA or silicon quality.",
            "next_hypothesis": "A useful environment contract should survive a held-out design parameter.",
        }
        write_result(4, iteration_4)

        iteration_5_results = {}
        for candidate in ("correct_verbose", "correct_compact"):
            functional = simulate(candidate, "exhaustive_tb.v", 5, work)
            synthesis = synthesize(candidate, 5, work) if functional["passed"] else None
            iteration_5_results[candidate] = {
                "held_out_width_functional": functional,
                "held_out_width_synthesis": synthesis,
            }
        iteration_5 = {
            "iteration": 5,
            "hypothesis": "The same observation-action-transition-grader contract transfers from width 4 to unseen width 5.",
            "artifact": "Held-out-width functional and synthesis replay",
            "metric": "all 4,096 width-5 combinations plus synthesis completion",
            "stop_rule": "Stop transfer claims if either known-correct parameterized design fails.",
            "results": iteration_5_results,
            "next_hypothesis": "The next material test is transfer to a different block family and correlation with RTL-to-GDS outcomes.",
        }
        write_result(5, iteration_5)

    summary = {
        "status": "OBSERVED",
        "capability": "deterministic local replay environment",
        "not_yet": [
            "validated simulator",
            "physical-design PPA correlation",
            "company-data utility",
            "held-out company transfer",
            "foundry economics",
        ],
        "iterations": [f"results/iteration-{number}.json" for number in range(1, 6)],
    }
    (RESULTS / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
