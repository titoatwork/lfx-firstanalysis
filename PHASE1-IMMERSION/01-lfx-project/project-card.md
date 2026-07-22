# LFX Project — AI-assisted extraction of architectural parameters (Part II)

- URL: https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66
- ID: 22296947-cecb-4a8f-8bcb-4f34710e9f66
- Mentors: Allen Baum, Ajit Dingankar
- Repo: https://github.com/riscv/riscv-unified-db
- Apply through: 2026-08-05 (plan submit Jul 31–Aug 2)
- Term: ~Sep 15–Nov 15, >=30 h/wk
- Seats: ~1 paid (RVI first mentee)

## Official Part II objectives (map everything here)

1. LLM extract priv+unpriv; gold (a) Manual chapter YAML (b) Drive keyword_matches (c) UDB YAML — improve recall
2. Extend classification scheme
3. AI agents/skills, reproducible workflows
4. Export → UDB YAML
5. Reviewed PR + merge follow-up

## Mentors focus
- Baum: precision, spec/cert, reviewable artifacts, justification/provenance
- Dingankar: AI-for-V&V, metrics, baselines, ablations

## Spring Part I (context)
- Mentee: @ishaan-arora-1
- Parallel: @ankit-cybertron
- Plans: issues #1747, #1751
- PRs: #1765–#1832 (local branches lfx-*)
- Public metrics (remeasured): adjusted recall 72.9%, class acc 88.4%, WARL ~50%
