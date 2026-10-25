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
| 9 | `edit_sketch_board` | An existing card cannot be moved into an area. The only way is `arrange_sketch_board` with a full timeline, which moves every card named. | Allow moving a card into an area, or an `arrange` mode that only sets the area. |
| 10 | `export_esdm` | Returns the files only in the response, nothing is written to disk. Copying 22 files by hand invites mistakes. | Write to a path, or return a zip as an attachment. |
| 11 | `get_sketch_board` with `tags` | An area that matches the filter is returned without the cards inside it when the cards do not match. | Return the cards of a matching area. |
| 12 | `edit_sketch_board`, `remove` | Removing a card leaves its connections on the board as dangling edges (three after chapter 5). | Remove a card's connections with it. |
| 13 | `edit_sketch_board`, connections | A connection's label cannot be changed and a connection cannot be removed; a new one in the same direction is skipped. | Allow updating and removing connections by id. |
| 14 | Policy (`create_node`) | A policy is created under the domain, not under a bounded context ("Policies bind an event from one context to a command in another"). The tutorial decides an owner for such rules (the €10 rule belongs to `fees`, C-19, ADR 5); the model has no place for it except the description. | A field for the context that owns the rule, separate from where the event and the command live. |
| 15 | Policy vs. process manager | `explain_concept` calls a rule that needs a running total a process manager. The €10 rule needs the amount owed. It only fits as a policy if `fees` decides inside an aggregate and publishes an event ("reader in arrears") that the policy turns into "place hold". | Say this pattern (decision in the aggregate, stateless policy across the boundary) in the policy guidance, not only the two extremes. |
