---
name: close-chapter
description: Finish a tutorial chapter in library-example. Use when a chapter's modelling and text are done and need to be checked, exported, committed and put up as a draft PR. Also use when asked to "close", "wrap up" or "finish" a chapter.
---

# Close a chapter

Work through these in order. Stop and report if a step fails. Do not merge.

0. **Run the script**: `python3 scripts/check_repo.py`. Fix every FAIL. Keep
   the WARN lines for the audit.
1. **Check the boards** against `checks.md` in this folder (Domain Story
   and Big Picture checks). Fix what fails on the board, not only in the
   text.
2. **Re-read the brief** (`requirements/brief.md`) next to the chapter.
   Every statement must trace to a section, or be marked `inferred` /
   `to-be`.
3. **Save versions** of every board used: `save_version` with label
   `chNN-<board>`; use `-v2`, `-v3` when a board is reworked.
4. **Export** into `model/`:
   - Domain Stories: `export_domain_story` → `model/domain-stories/<slug>.yaml`
   - Sketch boards: `get_sketch_board` → `model/sketch/<board>.json`,
     with a `snapshot` header (chapter, workspace, board, savedVersion,
     note) and `eventOrder` for timeline boards. Positions are not in the
     export, so say so in the note.
   - Context map and later: `export_esdm` → `model/library.esdm.yaml`
5. **Chapter file** `chapters/NN-<topic>.md`: input, tool, result at the
   top; findings and "what we take into the next chapter" at the bottom;
   saved version names in the footer.
6. **README**: update the chapter table.
7. **Plan**: add the chapter to the table in `docs/plan.md` §12 with the
   merge commit once it exists.
8. **Independent review.** Ask for a review that did not write the
   chapter (for example `/code-review` or a fresh agent that gets only the
   files). Fix findings before presenting. If the chapter adds, merges
   or splits a context, turns a mapping or changes a glossary, the
   review includes the `challenge-context-cut` skill in a fresh agent;
   its report goes to `docs/reviews/`.
9. **Retrospective.** List what was found in steps 0 to 8 or by the
   maintainer. For each finding, decide which rule or check would have
   caught it earlier, and add it to `CLAUDE.md`, `checks.md` or
   `scripts/check_repo.py`. Remove rules that did not help.
10. **Commit** on `chapter-NN-topic`, push, open a **draft** PR with a
   short summary and a **Rules audit** section (checks run, results, fixes,
   open warnings, rules added or changed). Tell the maintainer what to review and what is still
   open. Wait for their approval before marking ready and merging with a
   merge commit.
