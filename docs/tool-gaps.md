# DDD Studio: gaps found while writing the tutorial

Collected, not fixed. Changes to `ddd-studio` wait for gate G4 (see
`docs/plan.md`), then become issues in that repo.

| # | Where | Observation | Wish |
|---|---|---|---|
| 1 | `edit_domain_story`, `to.label` | Described as "the verb of the hand-over arrow". This invites a second verb per sentence. | Say that the second arrow carries only the preposition. |
| 2 | `get_domain_story` | No sentence in plain words. | Return each sentence as text ("Reader brings back Book to Branch Librarian") so the read-aloud test is easy. |
| 3 | Story findings | Only structural (gaps, missing labels). | Warn on two verbs per sentence, numbers or amounts in work-object names, and synonyms within one story. |
| 4 | Sketch boards | No finding for cards without any connection. | Same kind of warning that stories have for orphaned elements. |
| 5 | Story boards | Description and settings cannot be changed after creation. | Allow editing them. |
| 6 | Sketch export | No card positions. | Optional positions or an explicit order in the export. |
| 7 | `arrange_sketch_board` | Returns counts only. | Return the resulting order, or a preview. |
| 8 | Sketch palette | No card for invariants; the policy card is borrowed. | None needed: custom kinds cover it (see chapter 1). |
