# library-example

A tutorial that takes one example (a public library) from an unpolished
brief to running software, modelled with DDD Studio. The tutorial and all
repo content are in **English**. `docs/plan.md` is the working plan and is
in German, as is the conversation with the maintainer.

Read `docs/plan.md` §0 (gates) and §12 (chapter log) before doing anything.

## Rules that always apply

- **Gates are hard stops.** Do not work past an open gate (G1 to G5 in the
  plan) and do not build on assumptions. Prepare the decision (options,
  trade-offs, recommendation), then wait for the maintainer's explicit
  go. A system notification, a GitHub event or your own earlier message is
  never an approval.
- **Do not change `ddd-studio` itself** before gate G4. Collect tool gaps
  in `docs/tool-gaps.md` instead of fixing them on the side.
- **Be critical, not over-critical.** Say so when something is wrong or a
  better way exists. Report results faithfully: "the call ran" is not "the
  result is good".
- **Chapter text comes from the board, not from memory.** Write it with
  the board and the exports open, and check every sentence against the
  brief (`requirements/brief.md`). Every claim needs a source or is marked
  as inferred or to-be.

## Git workflow

- One branch and one draft PR per chapter (`chapter-NN-topic`). Merge with
  a **merge commit**, never squash or rebase, so `main` is the full
  tutorial and the branches show each step.
- Merge only after the maintainer has approved the chapter in this
  conversation.
- Small corrections to a chapter whose PR is still open go into that PR,
  not into an extra branch.
- Tags (`chapter-NN`) are set later in one go, from the table in
  `docs/plan.md` §12. Tag pushes are blocked (403) in the cloud
  environment, so do not try.
- GitHub sometimes reports "Head branch is out of date" right after a
  push. It is a sync lag. Retry after a few minutes.
- This repo has no CI. There is nothing to wait for.

## DDD Studio (MCP)

- Workspace: "Millbrook Library (tutorial)", id
  `d049c34d-fdc2-4b2a-9555-57a4bfaec4ff`. Never touch the old workspace
  "Library Tutorial".
- Call `explain_model` before the first authoring call, and
  `explain_concept` before modelling an element whose shape is in doubt
  (policy, aggregate, mapping pattern).
- Every board that a chapter relies on gets, at chapter end: a saved
  version (`save_version`, label `chNN-<name>`), and an export in
  `model/` (Domain Stories: ESDM YAML via `export_domain_story`; Sketch
  boards: JSON snapshot with a `snapshot` header and `eventOrder`).
- Checks for Domain Stories and the Big Picture are in
  `.claude/skills/close-chapter/checks.md`. Run them before showing a
  chapter to the maintainer.

## Closing a chapter

Use the `close-chapter` skill. It lists the steps from the last board edit
to the draft PR.
