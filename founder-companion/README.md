# Founder Companion

This is the founder's decision system inside the Environment Foundry Codex
project. It exists to answer a harder question than “How do we grow the
company?”:

> If I live this way for years, will I and the people I love be glad that I
> chose it?

The Companion remembers what one human cannot hold in working memory at once:
important transitions, good and bad decisions, recurring fears, sources of
energy, family constraints, mentors, books, ambitions, and the outcomes that
later revealed whether a decision was wise.

## Start here

1. Read [`constitution.md`](constitution.md).
2. Use [`runtime-protocol.md`](runtime-protocol.md) when the founder asks what
   to do in a live difficult moment.
3. Use [`decision-protocol.md`](decision-protocol.md) for a consequential
   decision.
4. Record a new decision from
   [`decisions/_template.md`](decisions/_template.md).
5. Use [`scenarios/_template.md`](scenarios/_template.md) for a multi-year
   thought experiment.
6. Run [`reviews/weekly-review.md`](reviews/weekly-review.md) to update the
   system from outcomes.
7. Use [`system-map.md`](system-map.md) to decide which plane and artifact a
   new fact belongs to.
8. Use [`flow-protocol.md`](flow-protocol.md) when the immediate problem is
   neither a major life decision nor a company strategy question, but the
   inability to be fully present in work, family, play, or recovery.

## Two planes

### Tracked operating plane

This directory contains reusable, public-safe rules and templates. It must not
contain raw family conversations, detailed health records, private messages,
audio, or intimate life history.

### Local private plane

The actual life timeline and personal evidence live under:

```text
../private-plane/payload/founder-companion/
```

That directory is ignored by Git. Its contents are available locally to an
authorized Codex session but are not company knowledge and must never be
promoted automatically.

The evidence-audited typed Constitution also lives there. Its current state,
not the slogans in this tracked directory, decides whether an article is a
candidate, an L2 trial, or an active L3 law.

The practical health workbook is also private. Its stable locator is
`private-plane/payload/founder-companion/health/README.md`; the actual workbook
must never be copied into Git or a website build.

## Current build sequence

1. Recover the founder's life timeline and ten pivotal decisions.
2. Extract candidate principles and a counterexample for each.
3. Simulate three plausible lives rather than one optimized company plan.
4. Discuss affected family scenarios with the affected people; do not simulate
   their consent.
5. Freeze a small constitution and test it on live decisions for 90 days.
6. Promote only principles that repeatedly improve decisions without hidden
   family, health, or trust debt.
