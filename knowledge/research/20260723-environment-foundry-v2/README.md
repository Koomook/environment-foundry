# Environment Foundry V2 — research brief

Date: 2026-07-23
Status: divergent research / evidence-backed / not canonical
Public-data boundary: only public benchmark code and synthetic benchmark data

## Executive answer

No inspected benchmark measures “running a real company” as one defensible
number. The strongest public artifacts measure different rungs:

1. correct tool/API use;
2. completion of a bounded workflow;
3. coordinated work across apps, state, time, or simulated coworkers;
4. policy and judgment under uncertainty;
5. longitudinal company outcomes such as retained revenue, trust, harm,
   survival, and changed future opportunity.

CRMArenaPro reaches levels 2 and parts of 4; TheAgentCompany and Gaia2 reach
level 3. None of the three observes a real company for long enough to validate
level 5. Therefore a benchmark portfolio and capability ladder are more valid
than a single “company-operation score.”

## Operational definitions

| Term | Minimum observable contract |
|---|---|
| Company operation | A bounded objective spanning at least two business objects or functions, with an authority/policy constraint and a state-changing action. |
| Decision | A time-stamped choice among at least two admissible actions, made from a frozen decision-time observation and uncertainty statement. |
| RL-ready | An agent can repeatedly observe, take typed actions, receive transitions and reward, terminate, and reset without test leakage. It does not mean RL is useful. |
| Simulator | Offline policy ranking predicts prospective live policy ranking and survives exploitation tests. Plausible synthetic state alone is insufficient. |

## Capability ladder

| Level | Unit | Must measure | Strongest inspected example | Missing proof |
|---|---|---|---|---|
| L1 Tool call | One call | arguments, authorization, tool result | τ-bench class | workflow outcome |
| L2 Bounded workflow | One defined job | multiple observations/actions, rule compliance, final state | CRMArenaPro | cross-functional consequences |
| L3 Cross-functional operation | Multi-app episode | app state, files/messages, dependencies, coordination | TheAgentCompany; Gaia2 | real institutional history |
| L4 Judgment under uncertainty | Decision episode | partial observation, policy, abstention, human/relationship trade-off | CRMArenaPro confidentiality; Gaia2 ambiguity/adaptability | calibrated human and real outcome |
| L5 Longitudinal company outcome | Linked episodes over time | delayed economic/trust/harm outcomes, policy changes, counterfactual limits | none inspected | almost everything |

The ladder is cumulative only as an **agent-surface evaluation** claim. It is
not the Foundry proof ladder. TheAgentCompany and Gaia2 have genuine mutable,
resettable simulated environments, so they deserve L3 surface credit. They do
not thereby pass Foundry validity, real-outcome closure, grader reliability,
prospective lift, or transfer gates. In short: `L3 simulated surface ≠ Gate 3
business evidence`.

## Three decoded upstream artifacts

### CRMArenaPro

- Downloaded public B2B JSON: 2,140 rows. B2C has another 2,140 rows.
- Real row keys: `idx`, `answer`, `task`, `persona`, `metadata`,
  `reward_metric`, `query`.
- The paper reports 4,280 unique queries; “interactive” files move hidden
  context into dialogue setup but do not add 4,280 new task identities.
- Upstream actions are `execute` (SOQL/SOSL) and `respond`.
- `ChatEnv.reset()` replaces the task and clears action history. It does not
  restore the shared Salesforce org. This is a logical reset, not a full state
  reset.
- Data/code license: CC BY-NC 4.0; it cannot be the commercial seed asset.
- Paper setting: Gemini 2.5 Pro reached 58.3% B2C single-turn “All” and 30.0%
  B2C multi-turn “All”; those are separate settings, not one leaderboard.

### TheAgentCompany

- Repository contains 175 task directories.
- Each task has a natural-language instruction and evaluator; the published
  task image adds `/utils/init.sh`, encrypted evaluator, workspace, and company
  service state.
- The inspected tasks use files, RocketChat, OwnCloud, GitLab/Plane, and
  deterministic weighted checkpoints.
- Code license: MIT. Service images, backups, and embedded content still need
  dependency-level review.
- Current website on 2026-07-23: the latest **verified** entry visible in the
  shipped JavaScript was TTE-MatrixAgent + DeepSeek-V3.2, 42.86% resolved and
  52.4% score, dated 2025-11-10. A newer IRIS+GPT-5.4 row dated 2026-06-25 was
  marked unchecked, so it is not used as the verified headline.

### Gaia2

- Public dataset is Parquet with columns `id`, `scenario_id`, `split`, `data`,
  `category`.
- Gaia2 mini validation has 160 rows. Each `data` cell is a full JSON scenario
  with app state and scheduled events. The first decoded scenario had 14
  scheduled events.
- The code can re-import scenario JSON and app state, so reset semantics are
  materially stronger than CRMArenaPro.
- Dataset license: CC BY 4.0; code license: MIT.
- Official leaderboard code dated 2026-05-15 reports GPT-5.5 (xhigh) at 56.4%
  pass@1 across the CLI split mix. The leaderboard states that scores are
  self-reported. It must not be compared directly to CRMArenaPro percentages.

All three adapters decoded three episodes each against
`normalized-episode-v2.schema.json` with zero validation failures.

## What the local baseline means

The implemented baseline refuses policy-sensitive rows and abstains elsewhere.
On the first ten CRMArenaPro B2B rows it scored `0.0` under a deterministic
local exact-set approximation. This is an intentional negative control. It is
not a CRMArenaPro result because it did not connect to Salesforce, use their
LLM answer extractor, or run the official protocol.

## Facts, unknowns, and next falsification

### Known from artifacts

- Public benchmarks now contain multi-app state, simulated colleagues,
  temporal events, privacy policies, and deterministic or oracle graders.
- “Enterprise benchmark” does not imply real enterprise trajectories.
- Reset, grader, and license semantics differ enough that scores cannot be
  collapsed without losing meaning.

### Still unknown

- Whether rights-valid Korean or Japanese operating context creates lift over
  a generic model plus private retrieval and harness.
- Whether a buyer wants training data, an eval, an interactive environment, or
  a managed outcome-closure service.
- Whether offline ranking predicts prospective business outcomes.

### Next falsification

Freeze one low-risk decision task before action, capture 20 rights-valid shadow
episodes, and compare four arms: human-only, generic model, retrieval/harness,
and environment-trained or environment-rehearsed policy. Close a real delayed
outcome and test held-out operator transfer. If the environment arm does not
improve outcome-adjusted performance or reduce intervention, stop calling the
asset training-value evidence.

## Primary sources

- CRMArenaPro: <https://arxiv.org/abs/2505.18878>,
  <https://github.com/SalesforceAIResearch/CRMArena>,
  <https://huggingface.co/datasets/Salesforce/CRMArenaPro>
- TheAgentCompany: <https://arxiv.org/abs/2412.14161>,
  <https://github.com/TheAgentCompany/TheAgentCompany>,
  <https://the-agent-company.com/#/leaderboard>
- Gaia2/ARE: <https://arxiv.org/abs/2509.17158>,
  <https://github.com/facebookresearch/meta-agents-research-environments>,
  <https://huggingface.co/datasets/meta-agents-research-environments/gaia2>,
  <https://huggingface.co/spaces/meta-agents-research-environments/leaderboard>

## V2 deliverables in this folder

- `benchmark-landscape.md` — benchmark matrix and leakage ledger
- `learning-guide-ko.md` — high-school → founder → ML engineer guide
- `company-public-strategies.md` — primary-source company strategy ledger
- `training-experiment.md` — executed Qwen experiment and spend gate
- `business-paths-and-30-day-wedge.md` — two business paths and kill gates
- `reproducibility-manifest.json` — pinned upstream source receipts
