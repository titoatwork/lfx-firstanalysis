# Hard constraints (always-on rules slice)

Complement `HANDSOFF.md`. If conflict with a casual user ask that implies spend/push/second-repo, **confirm first**.

## GitHub surface

- Only public campaign repo: `titoatwork/lfx-firstanalysis`
- Phase 2 code path: `riscv-param-extraction/` inside monorepo
- Push only mentor-auditable evidence on explicit user order
- Never push `riscv-unified-db/`, secrets, personal strategy notes

## Money / API

- No API until user provides key **and** scopes the run
- Prefer offline work; pilot ~$0.05; Artifact A ~$0.16 already spent
- Do not re-run A without user OK; v3 only with scoped resume
- Default extract model when approved: **gpt-4o-mini** (not full gpt-4o corpus)
- `--retries 0` on paid extract; stop if projected spend unsafe
- Never run two extract.py jobs in parallel
- Prefer key in shell env only; rotate if pasted in chat

## Honesty

- Measured numbers only (see `20-measured-facts.md`)
- Pilot = model split, not pure gpt-4o
- named=yes = 87 rows / 83 unique
- Part I credit stays with Spring mentee / PR authors

## Role

- User owns plan; agent executes on go
- Do not invent roadmap or Apply for the user
- Slack logistics only; technical on lists after membership
