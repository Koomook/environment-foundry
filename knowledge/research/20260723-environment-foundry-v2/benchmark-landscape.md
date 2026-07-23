# Benchmark landscape matrix — V2

Snapshot: 2026-07-23. Scores retain their own evaluation settings.

| Benchmark / owner | Ladder | Actual public artifact | Scale | State / action / grader / reset | License | Reported score and setting | Main limit |
|---|---:|---|---:|---|---|---|---|
| CRMArenaPro / Salesforce | L2 + partial L4 | Four JSON task files and two JSON object schemas; B2B row keys verified locally | 4,280 unique queries; 19 tasks + 3 confidentiality categories; 25 objects | Shared Salesforce org; SOQL/SOSL or respond; exact/F1 plus GPT-4o extraction/judge; logical reset only | CC BY-NC 4.0 | Gemini 2.5 Pro: 58.3% B2C single-turn All; 30.0% B2C multi-turn All, paper v2026 | synthetic CRM; no delayed outcome; non-commercial |
| TheAgentCompany / Princeton-led project | L3 | 175 task directories, Docker task images, simulated GitLab/Plane/OwnCloud/RocketChat, checkpoint evaluators | 175 tasks | Dockerized services and workspace; browser/shell/messages; weighted checkpoints; task init and backup restore | MIT code | TTE-MatrixAgent + DeepSeek-V3.2: 42.86% resolved, 52.4% score, verified row dated 2025-11-10 | simulated software company; one-task outcomes |
| Gaia2 / Meta | L3 + partial L4 | Parquet row with full JSON scenario; ARE code; app state, event DAG, oracle/checkers | 800 scenarios claimed across 10 universes; mini validation 160 | Dynamic apps/events; typed app actions; oracle and judge; JSON re-import reset | CC BY 4.0 data; MIT code | GPT-5.5 xhigh: 56.4% pass@1, self-reported, 2026-05-15, CLI split mix | synthetic scenarios; judge calibration; no economic outcome |
| WorkArena++ / ServiceNow | L2–L3 | Python task classes over a ServiceNow instance; BrowserGym integration; gated instance images | 33 compositional templates / 682 instances in paper setting | Browser actions; ServiceNow state; programmatic validators; instance reset tooling | Apache-2.0 code; instance terms separate | Record only with exact AgentLab/benchmark version; not yet locally decoded in V2 | access gate; knowledge-work UI, not longitudinal company |
| OSWorld / academic consortium | L2–L3 | VM configs, task JSON, screenshots, state graders | 369 real-computer tasks in original release | Mouse/keyboard; VM state; scripts/file/UI graders; VM snapshots | Apache-2.0 code; task assets vary | Do not compare across OSWorld and OSWorld-Verified | computer use, not organizational judgment |
| AndroidWorld / Google Research | L2 | Android emulator tasks and deterministic state checks | 116 tasks across 20 apps in original paper | UI actions; emulator state; programmatic reward; emulator reset | Apache-2.0 | Protocol-sensitive; record version and app snapshot | single-device workflows |
| τ-bench / Sierra + academia | L1–L2 | Tool schemas, database state, user simulator, policy rubric | retail + airline task sets | API tools and simulated user; DB state and policy; pass^k; environment reset | MIT code/data terms per repo | Useful lower rung, deliberately not headline here | customer-service tool use, narrow state |
| SWE-bench / Princeton | L2 | GitHub issue + repository commit + tests | 2,294 original; verified subsets differ | code edits; test verifier; repo checkout reset | MIT code; repository licenses vary | Never merge SWE-bench, Verified, Pro, Multilingual settings | verifiable engineering, not company operation |
| RE-Bench / METR | L3 judgment in R&D | Four long-horizon ML research environments, scoring scripts | 8-hour budget setting in paper | files/compute/code; continuous score; isolated task reset | repo-specific | Human-vs-agent curves depend on time budget | R&D economics, not cross-functional firm |
| PaperBench / OpenAI | L3 R&D replication | paper packages, rubric, Dockerized grading infrastructure | 20 ICML 2024 papers in initial release | full experiment reproduction; hierarchical rubric; isolated environment | repo/data terms per release | Setting includes paper set, time/compute, and grader version | research replication, not company operation |
| GDPval / OpenAI | L2 economic work product | task prompts, reference files, expert rubric/evaluation release | 1,320 tasks / 44 occupations in initial report | deliverable generation; expert pairwise grading; not generally interactive | release-specific | Pairwise win-rate setting, not an environment success rate | economically grounded output, limited transition/reset |
| SWE-Lancer / OpenAI | L2 decision + implementation | freelance issues, repositories, tests, manager choices | >1,400 tasks; $1M posted value in initial release | code/manager decision; tests or original manager choice | release-specific | Separate implementation and management settings | software labor only |

## Reading rule

A high score on a lower rung does not dominate a lower score on a higher rung.
Each reported number must include benchmark version, split, interaction mode,
harness, model, time/turn budget, grader, and date.

## Contamination and leakage ledger

- Public task prompts and gold answers are test assets, never SFT examples.
- TheAgentCompany task instructions and evaluators are public; leaderboard
  improvements require fresh or private holdouts to distinguish capability from
  task-specific adaptation.
- CRMArenaPro publishes answers and schema. Any training experiment must use a
  new generated training split and keep the public evaluation set untouched.
- Gaia2 public validation scenarios enable harness tuning. Final claims require
  an untouched test mechanism or new frozen scenarios.
- LLM judges add model/version drift and prompt exploitation risk even without
  classic train/test leakage.
