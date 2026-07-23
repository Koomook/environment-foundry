# Environment Foundry V2 benchmark and training handoff

- Workstream ID: EF-02
- Date: 2026-07-23
- Supersedes: none
- Current gate: artifact-informed workflow audit; bounded live task not selected
- Graph edge affected: external benchmark evidence → environment contract → falsifiable experiment design
- Artifact paths: `knowledge/research/20260723-environment-foundry-v2/`, `knowledge/lab/schemas/normalized-episode-v2.schema.json`, `src/environment_foundry_v2/`, `tests/test_v2_loaders.py`
- Verification command/observation: `uv run pytest`; `uv run python scripts/validate_company_os.py`; three decoded rows each from pinned CRMArenaPro, TheAgentCompany, and Gaia2 artifacts
- Verification result: 8 tests passed; 11 canonical pages and 6 workstreams valid; 9/9 decoded samples schema-valid
- Observations: public artifacts now reach mutable multi-app simulated work and policy-sensitive CRM tasks, but none inspected closes a longitudinal real-company outcome; a 12-step local Qwen LoRA run restored valid/safe serialization but left held-out decision accuracy at zero
- Decisions: retain a capability ladder instead of one company-operation score; keep simulator validity and Foundry proof gates separate; use SFT before RLVR at the current data scale
- Hypotheses: rights-valid Korean/Japanese decision episodes may add value only if they beat generic model + retrieval/harness on prospective held-out outcomes
- Atomic claims requested for promotion: none; this is divergent research and implementation evidence
- Contradictions/failures/missing evidence: no buyer-written specification, no rights-valid live episode set, no grader reliability study, no prospective outcome lift, no held-out operator transfer
- Privacy and rights attestation: only public benchmark artifacts and the public synthetic Ralphthon release dataset were used; upstream data remains outside Git; no credentials or private participant data were added
- Next falsifiable gate: freeze one low-risk decision task and collect at least 20 rights-valid shadow episodes with human, generic-model, retrieval/harness, and environment-policy arms
- Owner: EF-02 owner
- Stop rule: stop or redirect if the simple baseline ties, ranking is unstable, outcomes cannot be closed, or fewer than 20 defensible episodes are available
