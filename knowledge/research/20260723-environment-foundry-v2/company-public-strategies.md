# Public company strategies — primary-source ledger

Snapshot: 2026-07-23. “Public evidence” below is not a claim about a
company's private training stack.

| Company | Public evidence | What it supports | What remains inference |
|---|---|---|---|
| OpenAI | PaperBench publishes 20 paper-replication environments and 8,316 rubric nodes; the Agent Post-Training / Frontier Evals / Environments role explicitly joins data, environments, graders, training and feedback loops; OpenAI's 2026 SWE-Bench Pro investigation used agents plus human review and estimated about 30% broken tasks. | Environment and grader construction are treated as a first-class post-training and eval loop; benchmark validity itself is audited. | Which private company-operation environments train production models, and their mixture weights, are not public. |
| Anthropic | Bloom generates behavioral evaluations and explicitly warns that public evals can become contaminated; the Economic Index uses privacy-preserving production telemetry to estimate autonomy, complexity and success; system cards disclose internal and external suites. | Anthropic separates controlled capability evals from privacy-preserving post-deployment measurement and studies contamination. | No public source reviewed here shows a reusable company-operation RL environment or its training recipe. |
| Google / DeepMind | Gemini technical reports publish broad agent/eval results; Genie 3 exposes a world-model research prototype while naming limited action space and multi-agent interaction as open limitations. | Google evaluates across interactive surfaces and researches learned dynamic worlds. | A business-process environment-to-post-training pipeline is not publicly specified. |
| Microsoft | SentinelBench evaluates long-running monitoring agents while external state changes; AgenticRAG evaluates agentic retrieval workflows. | Microsoft is moving from static QA toward temporal, externally changing task settings. | No reviewed public artifact establishes longitudinal company outcomes or a general company RL stack. |
| NVIDIA | NeMo Gym defines an environment as dataset + agent harness + verifier + per-task state, supports JSONL rollout collection and SFT/DPO/RL, and publishes a multi-step Workplace Assistant GRPO tutorial. | This is the clearest public infrastructure analogue for an evaluate → collect rollout → train loop. | “Battle-tested in Nemotron training” does not reveal every private environment, curriculum or reward. |
| Salesforce | CRMArena/Pro publishes synthetic Salesforce data, 4,280 queries, CRM tools and graders; the official repository is research-only and the dataset is CC BY-NC 4.0. | Salesforce publicly tests professional CRM query and dialogue behavior in a realistic product surface. | The inspected `execute` path is read-only and reset does not restore the org, so calling the public artifact a full mutable digital twin would overstate it. |
| Sierra | τ-bench publishes tool-agent-user tasks, policies, database state and `pass^k`; τ² and τ-knowledge extend conversation and policy/knowledge composition. | Sierra openly uses executable policy-and-state benchmarks for customer-service agents. | These artifacts do not demonstrate cross-functional or longitudinal firm outcomes. |
| Palantir | AIP Evals publishes test suites, exact/custom/LLM judges, repeated runs, traces and model/prompt grid search over production functions connected to the Ontology. | Palantir publicly emphasizes versioned production-function evaluation, variance, debugging and cost/performance selection. | Public docs reviewed here do not show weight updates, RL rollouts or a reusable open benchmark dataset. |

## Why this matters

There are at least four distinguishable products:

1. benchmark authoring;
2. mutable environment and verifier infrastructure;
3. post-training rollout supply;
4. production outcome monitoring.

The public evidence does not support treating those as one market. Environment
Foundry's strongest possible wedge is the join between 2 and 4: rights-valid,
replayable decision episodes whose offline grader is later checked against a
prospective outcome. That join is also the least proven part of the thesis.

## Primary sources

- OpenAI: <https://openai.com/index/paperbench/>,
  <https://openai.com/careers/agent-post-training-frontier-evals-and-environments-research/>,
  <https://openai.com/index/separating-signal-from-noise-in-software-engineering-evaluations/>
- Anthropic: <https://www.anthropic.com/research/bloom>,
  <https://www.anthropic.com/research/measuring-agent-autonomy>,
  <https://www.anthropic.com/research/economic-index-june-2026-report>
- Google DeepMind: <https://deepmind.google/models/gemini/>,
  <https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/>
- Microsoft: <https://www.microsoft.com/en-us/research/project/sentinelbench/>,
  <https://www.microsoft.com/en-us/research/project/agentic-rag/>
- NVIDIA: <https://docs.nvidia.com/nemo/gym/about/concepts/environments>,
  <https://docs.nvidia.com/nemo/gym/latest/training-tutorials/nemo-rl-grpo/>
- Salesforce: <https://github.com/SalesforceAIResearch/CRMArena>,
  <https://www.salesforce.com/blog/crmarena-pro/>
- Sierra: <https://github.com/sierra-research/tau-bench>,
  <https://sierra.ai/blog/tau-knowledge>
- Palantir: <https://www.palantir.com/docs/foundry/aip-evals/overview>,
  <https://www.palantir.com/docs/foundry/aip-evals/experiments>
