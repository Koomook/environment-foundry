"""ai-chip-foundry-v2: three iterations answering v1's open questions.

iter-1  Sequential transfer: does the contract hold for a block with state?
iter-2  Grader validation: mutation audit of the hidden exhaustive grader.
iter-3  Fidelity step-up: generic cell count vs Nangate45 liberty-mapped
        area/delay rankings (proxy reality gap, pre-P&R).

Usage: uv run python knowledge/lab/experiments/ai-chip-foundry-v2/run_v2.py
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RTL = ROOT / "rtl"
TB = ROOT / "tb"
MUT = ROOT / "mutants" / "generated"
RESULTS = ROOT / "results"
SYNTH = ROOT / "synth"
LIB_DIR = SYNTH / "lib"
LIB = LIB_DIR / "NangateOpenCellLibrary_typical.lib"
V1_RTL = ROOT.parent / "ai-chip-foundry" / "rtl"

LIB_URLS = [
    "https://raw.githubusercontent.com/The-OpenROAD-Project/OpenROAD-flow-scripts/master/flow/platforms/nangate45/lib/NangateOpenCellLibrary_typical.lib",
    "https://raw.githubusercontent.com/The-OpenROAD-Project/OpenROAD-flow-scripts/main/flow/platforms/nangate45/lib/NangateOpenCellLibrary_typical.lib",
]


def run(cmd: list[str], cwd: Path, timeout: int = 300) -> dict:
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, timeout=timeout)
    return {
        "passed": proc.returncode == 0,
        "returncode": proc.returncode,
        "stdout_tail": proc.stdout[-2000:],
        "stderr_tail": proc.stderr[-1200:],
        "_stdout_full": proc.stdout,
    }


def simulate(design: Path, tb: Path, work: Path, tag: str) -> dict:
    out = work / f"{tag}.out"
    comp = run(["iverilog", "-g2012", "-o", str(out), str(design), str(tb)], work)
    if not comp["passed"]:
        return {"compile_passed": False, "sim_passed": False, "compile_log": comp["stderr_tail"]}
    sim = run(["vvp", str(out)], work)
    return {
        "compile_passed": True,
        "sim_passed": sim["passed"],
        "sim_log": sim["stdout_tail"],
    }


def synthesize(design: Path, top: str, params: dict, work: Path, tag: str,
               liberty: Path | None = None) -> dict:
    stat_path = work / f"{tag}-stat.json"
    chparam = "".join(f"chparam -set {k} {v} {top}; " for k, v in params.items())
    steps = [
        f"read_verilog -defer {design}",
        chparam + f"hierarchy -top {top}",
        "proc; flatten; opt; techmap; opt",
    ]
    if liberty:
        steps = [f"read_liberty -lib {liberty}"] + steps
        steps.append(f"abc -liberty {liberty}")
        steps.append("clean")
        steps.append(f"tee -o {stat_path} stat -json -liberty {liberty}")
    else:
        steps.append("abc -g simple")
        steps.append("clean")
        steps.append(f"tee -o {stat_path} stat -json")
    script = "; ".join(s for s in steps if s)
    res = run(["yosys", "-p", script], work)
    if not res["passed"] or not stat_path.exists():
        return {"passed": False, "log": res["stderr_tail"] or res["stdout_tail"]}
    stat = json.loads(stat_path.read_text())
    module = stat["modules"][f"\\{top}"]
    # logic-depth proxy: longest topological path (unit cell delay)
    depth = None
    ltp = run(["yosys", "-q", "-p",
               (f"{'read_liberty -lib ' + str(liberty) + '; ' if liberty else ''}"
                f"read_verilog -defer {design}; {chparam}hierarchy -top {top}; "
                f"proc; flatten; opt; techmap; opt; "
                f"{'abc -liberty ' + str(liberty) if liberty else 'abc -g simple'}; clean; "
                f"tee -o {work / (tag + '-ltp.txt')} ltp")], work)
    ltp_txt = work / f"{tag}-ltp.txt"
    if ltp_txt.exists():
        nums = re.findall(r"length=(\d+)", ltp_txt.read_text())
        if nums:
            depth = float(nums[-1])
    return {
        "passed": True,
        "num_cells": module.get("num_cells"),
        "area": module.get("area"),
        "logic_depth": depth,
        "cell_types": module.get("num_cells_by_type"),
    }


def fetch_liberty() -> dict:
    LIB_DIR.mkdir(parents=True, exist_ok=True)
    if LIB.exists() and LIB.stat().st_size > 100_000:
        return {"fetched": True, "path": str(LIB), "cached": True}
    errors = []
    for url in LIB_URLS:
        try:
            with urllib.request.urlopen(url, timeout=60) as resp:
                data = resp.read()
            if len(data) < 100_000:
                errors.append(f"{url}: suspiciously small ({len(data)} bytes)")
                continue
            LIB.write_bytes(data)
            return {"fetched": True, "path": str(LIB), "cached": False, "url": url,
                    "bytes": len(data)}
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{url}: {exc}")
    return {"fetched": False, "errors": errors}


def write_result(number: int, payload: dict) -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / f"iteration-{number}.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def iteration_1(work: Path) -> dict:
    candidates = {
        "seq_gold": RTL / "seq_gold.v",
        "seq_gamer": RTL / "seq_gamer.v",
        "seq_alt_onehot": RTL / "seq_alt_onehot.v",
    }
    results = {}
    for name, path in candidates.items():
        visible = simulate(path, TB / "visible_tb.v", work, f"{name}-visible")
        entry = {"visible": {k: v for k, v in visible.items() if k != "sim_log"}}
        if visible["sim_passed"]:
            hidden = simulate(path, TB / "hidden_tb.v", work, f"{name}-hidden")
            entry["hidden"] = hidden
        results[name] = entry
    return {
        "iteration": 1,
        "hypothesis": "The v1 environment contract (compile -> visible -> hidden behavior "
                      "gate) transfers to a sequential block where internal state makes "
                      "exhaustive input testing insufficient.",
        "artifact": "Icarus replay of 3 disclosed sequences + hidden exhaustive replay "
                    "(16,384 sequences x 14 bits, cycle-accurate golden model)",
        "metric": "hidden exhaustive sequence pass/fail",
        "stop_rule": "Reject the transfer claim if seq_gold or seq_alt_onehot fails hidden "
                     "replay, or if seq_gamer passes it.",
        "results": results,
        "next_hypothesis": "The hidden grader itself must be validated before trusting its "
                           "verdicts: inject mutations of gold and require 100% kill of "
                           "behavior-changing mutants.",
    }


def iteration_2(work: Path) -> dict:
    gen = subprocess.run([sys.executable, str(ROOT / "mutants" / "gen_mutants.py")],
                         text=True, capture_output=True)
    if gen.returncode != 0:
        raise SystemExit(f"mutant generation failed: {gen.stderr}")
    manifest = json.loads((MUT / "manifest.json").read_text())["mutants"]
    results = {}
    killed = survived = 0
    for mut in manifest:
        path = MUT / f"{mut['name']}.v"
        hidden = simulate(path, TB / "hidden_tb.v", work, mut["name"])
        outcome = "SURVIVED" if hidden["sim_passed"] else "KILLED"
        if hidden["sim_passed"]:
            survived += 1
        else:
            killed += 1
        verdict = "OK" if outcome == ("SURVIVED" if mut["expected"] == "SURVIVES" else "KILLED") else "UNEXPECTED"
        results[mut["name"]] = {
            "mutation": mut["description"],
            "expected": mut["expected"],
            "observed": outcome,
            "verdict": verdict,
            "log": hidden.get("sim_log", "")[-300:],
        }
    behavior_changing = [m for m in manifest if m["expected"] == "KILLED"]
    score = sum(1 for m in behavior_changing
                if results[m["name"]]["observed"] == "KILLED") / len(behavior_changing)
    return {
        "iteration": 2,
        "hypothesis": "A grader is only trustworthy if audited: every behavior-changing "
                      "single-point mutation of gold must be rejected by the hidden grader.",
        "artifact": "8 deterministic single-point mutants of seq_gold.v through hidden "
                    "exhaustive replay",
        "metric": "mutation score (behavior-changing mutants killed / total)",
        "stop_rule": "If any behavior-changing mutant survives, the grader has a blind "
                     "spot; stop and lengthen sequences or add formal checks before "
                     "trusting quality rankings.",
        "results": results,
        "mutation_score_behavior_changing": score,
        "equivalent_mutants": [m["name"] for m in manifest if m["expected"] == "SURVIVES"],
        "next_hypothesis": "With a validated correctness gate, test whether the cheap "
                           "quality proxy (generic cell count) survives a fidelity "
                           "step-up to a real cell library.",
    }


def iteration_3(work: Path) -> dict:
    lib = fetch_liberty()
    if not lib["fetched"]:
        return {
            "iteration": 3,
            "status": "BLOCKED",
            "reason": "Nangate45 liberty download failed",
            "errors": lib["errors"],
        }
    designs = [
        ("alu_compact_w4", V1_RTL / "correct_compact.v", "alu", {"W": 4}),
        ("alu_verbose_w4", V1_RTL / "correct_verbose.v", "alu", {"W": 4}),
        ("seqdet_binary", RTL / "seq_gold.v", "seqdet", {}),
        ("seqdet_onehot", RTL / "seq_alt_onehot.v", "seqdet", {}),
        ("seqdet_equiv_enc", MUT / "seq_mut06_equiv_encoding.v", "seqdet", {}),
    ]
    table = {}
    for name, path, top, params in designs:
        generic = synthesize(path, top, params, work, f"{name}-gen")
        mapped = synthesize(path, top, params, work, f"{name}-map", liberty=LIB)
        table[name] = {"generic": {k: v for k, v in generic.items() if k != "cell_types"},
                       "nangate45": {k: v for k, v in mapped.items() if k != "cell_types"},
                       "generic_cell_types": generic.get("cell_types"),
                       "mapped_cell_types": mapped.get("cell_types")}

    def rank(metric: str, source: str) -> list:
        keyed = [(d[source].get(metric), n) for n, d in table.items()]
        return [n for v, n in sorted((x for x in keyed if x[0] is not None))]

    comparisons = {
        "alu_pair": {
            "generic_rank": sorted(["alu_compact_w4", "alu_verbose_w4"],
                                   key=lambda n: table[n]["generic"]["num_cells"] or 1e9),
            "mapped_area_rank": sorted(["alu_compact_w4", "alu_verbose_w4"],
                                       key=lambda n: table[n]["nangate45"]["area"] or 1e9),
        },
        "seqdet_styles_same_behavior": {
            n: {"generic_cells": table[n]["generic"]["num_cells"],
                "mapped_area": table[n]["nangate45"]["area"],
                "mapped_depth": table[n]["nangate45"]["logic_depth"]}
            for n in ("seqdet_binary", "seqdet_onehot")
        },
        "equivalent_pair_noise_floor": {
            n: {"generic_cells": table[n]["generic"]["num_cells"],
                "mapped_area": table[n]["nangate45"]["area"]}
            for n in ("seqdet_binary", "seqdet_equiv_enc")
        },
    }
    return {
        "iteration": 3,
        "hypothesis": "The generic cell-count proxy can mis-rank designs relative to a "
                      "real cell-library mapping; the proxy reality gap is observable "
                      "already at synthesis, before P&R.",
        "artifact": "Yosys generic vs Nangate45 liberty-mapped synthesis of 5 designs",
        "metric": "num_cells (generic) vs area and logic depth (Nangate45)",
        "stop_rule": "If all rankings agree exactly, record the proxy as adequate at "
                     "this scale and state the boundary explicitly.",
        "liberty": {k: v for k, v in lib.items() if k != "errors"},
        "results": table,
        "comparisons": comparisons,
        "limitations": "Liberty-mapped area/depth is still pre-P&R: no placement, "
                       "routing, parasitics, DRC, power, signoff, or silicon.",
        "next_hypothesis": "The remaining fidelity step is RTL-to-GDS (ORFS or "
                           "partner-side flow) with prospective correlation — "
                           "explicitly NOT YET.",
    }


def main() -> None:
    missing = [t for t in ("iverilog", "vvp", "yosys") if not shutil.which(t)]
    if missing:
        raise SystemExit(f"Missing required tools: {', '.join(missing)}")
    with tempfile.TemporaryDirectory(prefix="ef-chip-foundry-v2-") as raw:
        work = Path(raw)
        i1 = iteration_1(work)
        write_result(1, i1)
        i2 = iteration_2(work)
        write_result(2, i2)
        i3 = iteration_3(work)
        write_result(3, i3)
    summary = {
        "status": "OBSERVED" if i3.get("status") != "BLOCKED" else "PARTIAL",
        "capability": "sequential-block contract, mutation-audited grader, "
                      "liberty-mapped fidelity comparison",
        "not_yet": ["RTL-to-GDS correlation", "formal proofs", "commercial-node transfer",
                    "company-data utility", "silicon outcome"],
        "iterations": [f"results/iteration-{n}.json" for n in (1, 2, 3)],
        "headline": {
            "iter1_gamer_hidden_passed":
                i1["results"]["seq_gamer"].get("hidden", {}).get("sim_passed"),
            "iter2_mutation_score": i2.get("mutation_score_behavior_changing"),
            "iter3_status": i3.get("status", "OBSERVED"),
        },
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
