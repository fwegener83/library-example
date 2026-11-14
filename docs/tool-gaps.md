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
| 16 | Flows in the ESDM export | Flows and slices are not exported ("studio-internal"). A review that reads only the exports does not see the flows; the agent must read them through MCP (G1). | An export of flows, or a Studio-own export format next to ESDM. |
| 17 | Scenarios across contexts | A GWT feature is pinned to one aggregate or read model, and the example data of a flow is "purely narrative, never a test case". An acceptance test across contexts (G1: flows can become acceptance tests) has no place in the model. | A flow, or a feature on a flow, as an executable scenario across contexts. |
| 18 | REST contract | Commands, queries and read models carry payload schemas, but nothing turns them into an OpenAPI specification. Relevant only if gate G2 decides on REST (ADR 10, reopened 2026-10-28); the specification would then be written by hand from the model. | An OpenAPI export per bounded context. |
| 19 | `explain_model` flows-and-slices | Says "A flow is one story in one context, not the whole domain", but a flow has no context and each slice names its own (`bcId`); events of earlier slices flow into a read model "whatever context they come from". The text contradicts the API and discourages flows across contexts, which is what shows whether a cut holds. Found while planning phase 5; confirmed or corrected with the first flow in chapter 7. The maintainer has asked for the wording to be fixed (2026-10-28). | Say that a flow may cross contexts and that each slice carries its context. |
| 20 | DCB: `consults` and `identifiedBy` | Both belong to the DCB, not to its command. Two decisions with different selections (checkout and reservation) need two DCBs, and a command that needs less (cancel a reservation) still carries every selection field and reads everything. | Selection and consults per command, or commands of one DCB that may narrow them. |
| 21 | DCB: `identifiedBy` only from the command | No derived selection (card number → member, running loans → their titles). The value must be in the command; the issuer looks it up in a view first. | None needed now; the pattern is documented ("informed decision"). Recorded as a limit. |
| 22 | Invariants have one anchor | The same card and copy rules hold for checkout and reservation, so they are written twice, on two DCBs, with two ids. | A rule shared by several anchors, or a reference from one invariant to another. |
| 23 | Taking a fact in from another context | Each fact costs a policy, a command, an event and a thin aggregate as anchor, although the receiving context decides nothing about it (five membership events into `lending`). Studio names the shape and its price. | None needed: the cost is real and shows the coupling. Recorded as a limit. |
| 24 | `explain_model` code-sync | Says `apply_esdm` skips `dynamic-consistency-boundary` as a kind Studio does not model. A dry run on 2026-11-14 took a DCB back as an update. | Bring the text in line with the behaviour. |
| 25 | `apply_esdm` dry run | A file in which only an invariant's text was changed reported `identifiedBy` as changed as well (DCB `checkout`, probe, 2026-11-14). Cause not examined. | Report only the fields that differ. |
| 26 | `esdm lint` | Studio refers to the linter's findings ("esdm lint flags"), but no package by that name exists in npm or PyPI (checked again 2026-11-14). Question L1 in `docs/plan.md`. | Say where the linter is, or ship it. |
| 27 | Workspaces | A workspace cannot be deleted through MCP; the probe workspace of chapter 7 stays. | `delete_workspace`, or an archive. |
| 28 | `apply_esdm`, invariants | Applying a DCB file regenerated the ids of its invariants although the report named only `identifiedBy` and `description` as changed; a slice rejection that pointed to an invariant had to be set again (2026-11-14). | Keep invariant ids when name and rule are unchanged, or report `invariants` as changed. |
| 29 | `patch_node`, description | A node's description can only be changed through `apply_esdm` with the whole file. | A `description` field on `patch_node`. |
| 30 | `create_node`, field order | A payload given as a JSON Schema object came back in alphabetical order, although the tool says the order is kept. The list form keeps it. | Keep the order of `properties`, or say to use the list form. |

## State after the Studio update of 2026-11-14

Checked against `explain_model` and `explain_concept` on 2026-11-14 and in
a probe workspace (`docs/logs/ch07-decision-shapes.md`).

| # | State |
|---|---|
| 14 | **By design.** In ESDM and Studio a policy belongs to the domain because it joins contexts. The tutorial shows the owner by the policy's name and description and by the direction of the context mapping. Not a wish for Studio any more. |
| 15 | **Closed.** The policy guidance and "Which shape for a decision" describe a total held by one aggregate, an event at the line, and a stateless policy reacting to it. |
| 16 | Open. Flows are not ESDM. Scenarios a flow derives from marked slices are exported with their feature. |
| 17 | **Partly closed.** A marked slice yields a scenario; the Given of a DCB scenario may hold events of other contexts. A test that runs across several aggregates or contexts still has no place. |
| 19 | **Closed.** The text now says a flow may cross bounded contexts and each slice names its own. |
| 20–30 | New, see the table. 26: `esdm lint` runs later in the pipeline (maintainer, 2026-11-14). |
