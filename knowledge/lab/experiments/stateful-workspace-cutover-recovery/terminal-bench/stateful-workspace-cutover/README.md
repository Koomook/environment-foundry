# Stateful workspace cutover

## Difficulty

The task combines stateful debugging, SQLite semantic comparison, active-work
safety, credential handling, revision compare-and-swap, atomic file operations,
idempotency, and recovery ordering. A superficially healthy fix can still use
the wrong database, leak the token, mutate the source, overwrite a populated
head, or switch authority before pull-back verification.

## Solution

The reference implementation treats the existing database as immutable local
authority, recovers it without touching remote state, and gates cutover on an
inactive source plus exact remote preconditions. It exports and verifies before
enrollment, stores only a token digest, commits one revision with CAS semantics,
pulls into a fresh cache, verifies the logical database hash, and only then
switches authority. Repetition is a no-op.

## Verification

The package uses Harbor's separate-verifier container mode and declares only
`/app/workspace_runtime.py` as the transferred artifact. Hidden randomized fixtures check semantic hashing,
active recovery, precondition failures, partial export, conflicting identity,
stale CAS, corrupt pull-back, secret redaction, source immutability, operation
ordering, and idempotency. Reward is binary. In the verifier image, submitted
Python runs as UID 10001 through a narrow worker; `/tests` and `/logs/verifier`
remain root-only. A committed adversarial probe confirmed that the candidate
could neither read hidden tests nor write reward output.

## Relevant experience and provenance

Environment Foundry reconstructed the task from an audited stateful recovery
pattern and authored a clean synthetic implementation. The originating private
task and its data are not included. The package is an internal evaluation
artifact and has not been proposed or accepted upstream.

See the [experiment card](../../README.md) for rights, evidence, and RLVR
boundaries.
