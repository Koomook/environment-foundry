# Workstreams

Workstreams are the non-canonical coordination layer. Each bounded task owns one directory:

```text
NN-slug/
  brief.md
  status.md
  handoffs/YYYY-MM-DD-milestone.md
```

- `brief.md` is the stable scope and gate contract.
- `status.md` is the replaceable current view.
- `handoffs/` contains immutable milestone packets. Correct one with a superseding packet.
- A handoff may request claim promotion, but it is not canonical evidence by existence.

Only `06-memory-compiler` may promote claims to the wiki, and the founder retains final priority, external-action, and stop/continue authority.
