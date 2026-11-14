# Chapter 7 — working log

What was done, what failed and why, which decision fell and why. The
skill `model-scope` is written from this log after the maintainer's review
(`docs/plan.md`, "Wie ein Skill entsteht"). Column "fit" per step: *flow*
(in the flow), *static* (static only, as Studio intends), *bent*, *not
representable* (see plan, chapter 7, step 10).

## Step 1 — preparation

- 2026-10-28: Chapter 7 started first as Example Mapping on a sketch board;
  the maintainer stopped the board edits and then dropped Example Mapping
  as a chapter (plan PR #23). Lesson for the skill: the medium of a
  workshop technique (coloured cards) is not the technique; an agent
  working alone writes rules and examples where they are used.
- The open rules decided before the drop stay (C-11 to C-14, C-33 to
  C-38, clarification log A5).
- `explain_model` (overview) read. The ddd-studio MCP server disconnected
  twice while preparing; calls were retried after it came back.

## Step 3 — flow 1 (backbone), first pass

- 2026-10-28: Static view for `catalogue`, `membership` and part of `lending` was built
  **before** any flow. That broke the agreed way of working ("flow first":
  nodes per step, slice at once). The maintainer pointed it out. Lesson for the skill:
  build the storyline step by step, create only the nodes a step needs, then the slice;
  never a whole context ahead.
- Flow `1 · From the shelf to a blocked card and back`: 23 slices, all four contexts,
  `validate_model` without findings.
- Places Studio cannot express, marked with `[?]` in the slice name and a note on the static view:
  1. rule over many aggregates (five reservations, overdue limit): DCB missing;
  2. a decision that reads a read model (checkout reads `reader-standing`, fines read
     `replacement-prices`): no reference;
  3. conditional events (`publishes X, and Y if ...`);
  4. owner of a policy (tool gaps 14, 15);
  5. uniqueness/existence over several aggregates (ISBN, copy needs title);
  6. a page composed from three contexts (morning list);
  7. time (daily run as a system actor, one per context).
- Still open for this flow: backward check (step 5), GWT scenarios (step 4),
  maintainer's answers on the asymmetry policy/read model and on the daily run.

## Step 3a — DDD Studio gets the DCB; the shapes are decided

- 2026-11-05: Studio's new flow patterns read through MCP
  (`ddd-studio.dev` is not reachable from the session). Notes 3, 6, 7
  and the asymmetry turn out to be documented patterns; gaps 1, 2 and 5
  are one finding (a decision reads more than its own stream).
- 2026-11-12: Studio has the DCB. Probe workspace "zz probe DCB fit for
  Millbrook" built (throw-away; cannot be deleted through MCP). Proposal
  "variant A" written.
- 2026-11-12: code review of the proposal: 10 findings. Valid among
  them: one DCB for two decisions reads too much; `copy` and the DCB
  writing in the same life; *found damaged* missing from the consult
  list; a snapshot event a stateless policy cannot build; DCBs used as
  plain anchors.
- 2026-11-14: Studio updated again ("Which shape for a decision"). It
  settles most review findings. Probe extended: an aggregate reading as
  History an event a DCB wrote; `loan` opened by the DCB; reservations
  as free-standing events; ESDM export and `apply_esdm` dry run.
- 2026-11-14: a second agent reviewed the follow-up. Taken: `loan` as
  aggregate, reservations without one, automation over a view in `fees`,
  policy owner as "by design". Not taken: the researcher status as a
  value in the command (hard rule, C-28; the reader may be the issuer);
  `copy-withdrawn` in the consult list (the catalogue's event;
  `copy-retired` is lending's).
- 2026-11-14: **decided by the maintainer**: the shapes in
  `docs/logs/ch07-decision-shapes.md` (revises storylines decisions 2,
  3, 7). Release of a damaged copy stays out: scenario H is not in the
  first increment (chapter 6).
- Lessons for the skill: ask "where does the fact come from, and who may
  report it" before picking a shape; write the consult list of a DCB
  explicitly, because Studio does not check it; a probe in a throw-away
  workspace answers questions that reading the guidance leaves open.
- Still open: `esdm lint` (L1); the rebuild of flow 1.

