Out of draft, and sorry for the gap: the work landed on 2026-08-03 and I left the PR marked draft, so it never came back to you.

All seven inline comments from the 2026-08-01 review are addressed:

- YAML is loaded with `ruamel` into a dict rather than pattern-matched. That is the one you said would change all the logic, and it did.
- Scope is everything under `spec`. There is now a single `spec_root = root / "spec"`, and `param_dir` derives from it, so the separate scan roots and the duplicated path constants are both gone rather than being referenced more consistently.
- The file filter is `spec_root.rglob("?*.?*")`, the "files with a dot" pattern you suggested.
- No `.yml` handling, since there are none.
- `.layout` templates are scanned, which the earlier version missed. A typo in one should be reported against the file you can edit, not against the generated copy that says not to edit it.
- The test file lost the repetition and the per-case structure with it.

73 checks green, 14 skipped, 0 failures. The seven review threads still marked unresolved are all flagged outdated, since the code moved past them. Happy to resolve them one by one if you would rather see that explicitly than take my word for it.
