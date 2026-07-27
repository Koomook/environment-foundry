# Founder Capacity Interface

Status: active boundary

Environment Foundry may consume founder capacity constraints from the Founder
Companion. It may not consume the private reasons behind them.

## Allowed fields

```yaml
status: available | constrained | unavailable | hard-stop
effective_from: YYYY-MM-DD
effective_until: YYYY-MM-DD
weekly_company_hours: integer
travel_window: allowed | review-required | unavailable
consequential_decision_load: low | medium | high
review_date: YYYY-MM-DD
source_locator: opaque-local-reference
```

## Forbidden fields

- family identities or private preferences;
- health diagnosis, treatment, or narrative;
- private messages, recordings, or relationship history;
- reasons that could pressure an affected principal;
- inferred consent;
- raw life timeline or personal decision transcript.

The company may respond by narrowing scope, changing timing, or escalating a
founder decision. It may not optimize around a hard stop or ask an agent to
reverse-engineer the private reason.
