# Evidence lab

This directory contains inspectable, rights-cleared, redacted artifacts for bounded environment work. It is not a raw operational archive.

Every experiment package should include:

- task contract and observation cutoff;
- typed actions, abstain/escalate behavior, transition, and termination;
- provenance and rights receipt;
- immutable baseline outputs;
- grader vector, hard failures, uncertainty, leakage and exploitation tests;
- temporal/entity holdout;
- outcome window and next decision;
- dataset/eval card distinguishing episode, replay, interactive environment, and validated simulator.

Synthetic fixtures must say synthetic. Live-ready validation must fail without a valid rights receipt.
