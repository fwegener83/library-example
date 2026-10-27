# Context cut challenge: ch07-flows-and-contracts (mode 2)

Input: repo `5f06028` (branch of chapter 7), Studio workspace "Millbrook Library (tutorial)", versions `ch07-flows-and-contracts` and `ch07-flows-and-contracts-v2` (177 elements each; `get_model_overview` reports `complete: true`, no violations).
Files read: `.claude/skills/challenge-context-cut/SKILL.md` and `heuristics.md`; `chapters/07-flows-and-contracts.md` and the plan scope in `chapters/06-choosing-the-first-increment.md`; `docs/adr/0002` to `0012`; `docs/gates/g1-model-to-code.md`; `requirements/brief.md`, `requirements/clarifications.md`; all of `model/esdm/` (events, commands, queries, read models, aggregates, 10 policies, 9 mappings, 4 glossaries); `model/sketch/` and `model/domain-stories/` (searched, not re-read in full); `.claude/skills/model-flows/SKILL.md`, `.claude/skills/design-context-contracts/SKILL.md`; `docs/reviews/pre-g6-context-cut.md` (F-titles and F9); `docs/tool-gaps.md`. In Studio, read only: `list_flows`, `list_slices` (all 51 slices with their example data), `get_model_overview`, `list_mappings`, `list_versions`, `get_node` on 8 nodes, `explain_model` (fields-and-validation). No create, patch or delete call was made.
Run by: fresh agent, 2026-10-26

**Not checked, or not checkable:** (1) The *descriptions* of events, policies, aggregates and slices. `get_node` returns none for any node I opened, and the ESDM export has a `description` only on the 9 mappings (see F4). I could not see whether Studio holds descriptions that the tools do not show. (2) The wiring of each slice (which member node is a step's command, event, policy) was read from `memberIds` only, not node by node. (3) Whether example data fits the payload schemas: spot-checked by eye on about 20 slices, not systematically (tool gap 21 says `validate_model` does not check it). (4) GWT features and notes: none exist, none were read.

## Summary

No abort criterion of the phase model is hit by any flow. I agree with the chapter on that, and I rebuilt the dependency graph independently: it is acyclic and every arrow has a mapping (see "What holds"). The cut survives the flows.

What does not hold is the chapter's statement about how well it was tested and recorded: **0 blocking, 12 should fix, 4 notes.** The 12 are in three groups. (a) The contract rules for order and gaps (ADR 11, ADR 12, ADR 5) fail in directions the chapter calls "safe": F1, F2, F3, F5. (b) The chapter says "the model is the source of the contracts" and "the test ran on every flow", and both are only partly true: F4, F9, F8, F12. (c) Details that contradict a clarification or a payload: F6, F7, F10, F11.

| Count | Severity |
|---|---|
| 0 | blocking |
| 12 | should fix (F1 to F12) |
| 4 | note (F13 to F16) |

### Checked numbers and claims of the chapter

| Claim in the chapter | Result |
|---|---|
| ten flows, 51 steps | `list_flows`: 10 flows; `list_slices`: 51 slices; per flow 4, 4, 6, 4, 5, 4, 8, 6, 4, 6, equal to the "Steps" column |
| 9 aggregates, 29 commands, 29 events, 10 policies, 6 read models, 6 queries, 6 actors | all equal to the file counts in `model/esdm/` (the 6 actors are 4 distinct names: `branch-librarian` and `clock` exist in two contexts) |
| 13 of the 29 events cross a boundary, 16 are internal | derived from the `handles` of the 10 policies: catalogue 5, membership 5, lending 3 are handled by a policy of another context = 13; fees 6, lending 9, membership 1 (`contact-details-recorded`) = 16. Correct. But the mark "Published to / Internal to" itself I could not find (F4) |
| 2 orders, 6 questions | `place-hold`, `lift-hold`; `get-title-details`, `get-amount-owed`, `list-copies-for-head-of-collection`, `list-overdue-loans`, `list-reservations-that-ran-out`, `get-contact-details`. Correct |
| "There are eleven" crossings | the table has 11 rows, but the rows group 2, 5, 3 and 6 contracts; the contracts are 13 + 2 + 6 = 21. The skill says "one contract per crossing" (F9) |
| 7 of 9 mappings used by the flows | correct: catalogue-lending (2 mappings), catalogue-fees (2), lending-fees, membership-lending, membership-fees. Unused: CityPay, ISBN service |
| "All ten policies have [an owner], written at the start of the description" | not verifiable (F4) |
| "The model in Studio is the source of the contracts" / "no second copy" | not borne out (F4) |
| EUR 0.50 per day from the day after the due date | E1: due 1 Dec, back 8 Dec, 7 days, 350 cents: correct. E2b: due 2 Dec, morning run 23 Dec = 21 days = 1050; back 22 Dec = 20 days = 1000: correct |
| lost-book fee = price + EUR 5 | G1: 1800 + 500 = 2300: correct |
| block only *above* EUR 10 | E2b: 10.00 lifts, 10.50 places: correct, and it is the best example in the chapter |
| loan 60 days | l-0001: 2 Nov + 60 days = 1 Jan 2027; l-0003: 3 Nov to 2 Jan; l-0004: 2 Oct to 1 Dec: correct |
| card valid one year "up to and including the day before" (C-28) | member registered: 2 Nov 2026 to 1 Nov 2027, researcher 9 Nov to 8 Nov 2027: correct. The renewal example is wrong (F11) |
| cap at the replacement price | no flow reaches the cap (F9) |

### Table "Flow x criterion"

Criteria: **C1** an invariant needs data of two contexts at the same moment; **C2** a policy without a clear owner; **C3** the flow goes back and forth between two contexts; **C4** an aggregate needs the state of another context to decide; **C5** a word needs two meanings inside one context. "no" = not hit. "(copy)" = not hit only because the decision is taken from a local copy of the other context's facts; the cut holds because of that copy, and the stale window is a cost. "*" = no policy has a visible owner in the model (F4); the owner can be derived from the `handles`/`emits` of the policy and is clear in every flow.

| Flow | C1 | C2 | C3 | C4 | C5 | Remark |
|---|---|---|---|---|---|---|
| A. Register title and copy | no | no* | no (catalogue to lending, to fees; one way) | no | no | fees keeps a copy of the price (`title-price`) |
| A2. Correct and withdraw a copy | no | no* | no | no | no | a correction to *restricted* while the copy is reserved is not settled (F15) |
| B. Member, researcher status, renewal | no | no* | no | no | no | renewal example date wrong (F11) |
| C. Check out and return, also damaged | no (copy) | no* | no | no (copy) | no (*branch*, 3 roles, as the chapter says) | checkout needs card end and status (membership), kind (catalogue), shelf state (lending): decided from `reader` and `copy`; the limits also need loans and reservations of lending (F15) |
| D. Reserve, collect, cancel, run out | no (copy) | no* | no | no (copy) | no (*branch*) | same as C; the collected copy is checked out by a policy inside lending |
| E1. A late return | no (copy) | no* | no | no (copy) | no | the cap combines the price (catalogue, local copy in fees) and the days (lending); **the cap is never reached by the example data** (F9) |
| E2-E3. Running fine blocks, payment unblocks | no (copy) | no* | no: lending to fees to membership to lending is three hops, no pair of contexts has traffic both ways | no (copy): fees decides arrears from its own account and from its own flag `hold-placed`, which membership does not feed | no | orders and gap rules: F1, F5 |
| E2b. Late return after the morning run | no (copy, and business time) | no* | no | no (copy) | no | wrong block for a few hours is the named cost; the hold-back of an event is the unnamed one (F1) |
| G1. A copy is declared lost | no (copy) | no* | no (lending to fees to membership; catalogue to lending is a separate hop, started by a person) | no (copy) | no | the loss is a fact of lending; the withdrawal is a person's decision in catalogue (C-20) |
| J1. The morning lists | no | no (no policy: questions) | no, but the reservation row lacks `title-id`, so the page must ask back (F6) | no | no | the question to fees is in no flow (F9) |

## What holds

- **The dependency graph is acyclic and matches the mappings.** Rebuilt from who handles whose event and who emits a command where: `lending` handles catalogue (3 events) and membership (5 events); `fees` handles catalogue (2 title events) and lending (3 events) and gives orders to `membership`; `catalogue` and `membership` handle nothing of another context. That is exactly ADR 5's list. Every arrow has a mapping (`catalogue-lending-*`, `catalogue-fees-*`, `membership-lending-customer-supplier`, `lending-fees-customer-supplier`, `membership-fees-customer-supplier`); the two mappings without traffic (CityPay, ISBN service) are the ones the chapter names. The business circle lending, fees, membership, lending exists in flow E2-E3, not in the dependencies (heuristics §4).
- **The high-frequency desk operations cross no boundary.** Flows C and D have zero crossings; the checkout is decided from the module's own `reader` and `copy`. A "may I?" question before an action does not occur anywhere. That is the strongest result of the chapter.
- **The EUR 10 rule has one owner, and the flows do not need a second.** `fees` decides, `membership` knows nothing of money, `lending` reads only `blocked` (ADR 5, C-19). E2b shows the late case working through the time of the decision (`decided-at` 06:00 and 07:30) and the number in order (2, then 3).
- **Change scenarios touch at most two contexts.** Threshold of EUR 10: `fees` only. 28-day loans (C-13): `lending`, plus `catalogue` if "new release" is a title attribute; `fees` follows the due date it receives. A new reader group for restricted copies (C-29): `lending` and `membership`. A second reason for a hold: `membership` and the new owner, `lending` untouched. A fifth branch: `catalogue` and `lending`, but it is costly under ADR 12 (F3).
- **The customer-supplier mappings are real.** lending to fees: the due date and the loss shaped the events (ADR 9); membership to lending: the end dates (C-28); membership to fees: the hold. Each has someone who needs something specific.
- **The earlier findings are visible in the model.** Loan identity and business time (pre-g6 F1) are in every event; end dates are dates (F2); unknown subjects are held back (F3); *restricted* is a rule of lending (F4, lending glossary); the list of the Head of Collection carries `damage-report-id` (F5); contact details live in `membership` and are asked for as a list (F7). The questions take lists, not one call per row.
- **Words that must differ do differ, and the glossaries say so**: *copy* (catalogue: a physical book; lending: what may be done with it now), *restricted* (catalogue: kept out of circulation; lending: who may borrow), *reader*/*member*. The payload names of the hold events (`blocked`) avoid carrying membership's *hold* semantics into lending.
- **ADR 12 does not contradict ADR 4 or ADR 9.** It is the record that ADR 4 announced ("changed only by adding to it"); it keeps ADR 9's "tells the customer before it changes". The conflict is with ADR 11 (F2) and inside ADR 12 (F3).
- The chapter says openly what the flows could not test (CityPay, ISBN, damage release, keeps, rules inside `lending`). I found nothing in that list that is wrong.

## Findings

### F1 A gap in the member's events holds back the *block* event, which is the unsafe direction
- Severity: should fix
- Lens: scenario
- Evidence:
  - `docs/adr/0011-what-every-published-event-carries.md`: "a number with a gap before it is **held back** until the missing events have arrived."
  - `chapters/07-flows-and-contracts.md`: "The card events are applied **strictly in order** for a member. Otherwise 'blocked' and 'free' could change places."; finding 1: "Both are on the safe side".
  - `model/esdm/membership/card-renewed.esdm.yaml` carries only `card-valid-until`; `hold-placed.esdm.yaml` only `blocked`. They are deltas, unlike `catalogue/copy-corrected.esdm.yaml`, which chapter 7 describes as "all three values travel, so the event replaces the earlier ones".
- Why it matters: member m-0003 has events 1 to 3 applied. Number 3 (a renewal) is delayed or lost; number 4 (`hold-placed`, `blocked: true`) arrives. Lending must hold number 4 back, so for as long as the gap lasts the desk lends to a reader whom `fees` has blocked. The renewal case in finding 1 is on the safe side (a refusal); this case is the opposite. ADR 11 leaves "how long to wait, and what happens when an event never comes" to G2, but it does not name the direction. The same gap rule holds back `copy-withdrawn` behind a lost `copy-corrected` (a withdrawn copy stays lendable).
- Alternatives: (a) make the membership events state-carrying (each carries `card-valid-until`, `researcher-until`, `blocked`), so lending applies the highest number it sees and needs no hold-back for this stream — costs: larger events, one rule less in lending, and the Big Picture events *Card Blocked*/*Card Unblocked* become one status fact; (b) keep strict order, but while a gap exists lending refuses new loans and reservations for that reader (fail closed) — costs: refusals at the desk during a gap, and the held-back list becomes a daily-operations list; (c) leave it for G2 and write the direction into ADR 11 as a known cost — costs: the decision is made without alternatives.
- Level and next step: architecture. Proposed ADR (amend ADR 11 or fold into ADR 12); recommend (a) for the member stream.

### F2 Gapless numbering per subject collides with "consumers ignore events they do not know" (ADR 12) and with internal events
- Severity: should fix
- Lens: dependencies
- Evidence:
  - ADR 11: "a number that grows by one with every event the publisher issues about that subject, without gaps, like the version of an aggregate."
  - ADR 12: "a new published event for a situation that had none. Consumers ignore events they do not know;" and "the owner publishes a **new fact under a new name** ... beside the old one, and keeps publishing both".
  - `model/esdm/membership/contact-details-recorded.esdm.yaml`: an event of aggregate `member`, with no `sequence`, in a flow (B, step 1) between `member-registered` (sequence 1) and `researcher-status-granted` (sequence 2). Chapter: "the other 16 are internal to a context".
  - `model/esdm/integration/catalogue-fees-published-language.esdm.yaml`: "The usage-fee mark of the copy (C-21) comes with scenario F".
- Why it matters: (1) If an event that a consumer ignores still takes a number, the consumer sees a gap and (by ADR 11) holds back every later event of that subject forever. This is not hypothetical: in scenario F `fees` would follow `copy-registered` and `copy-corrected` for the mark but has no use for `copy-withdrawn`; in scenario H `copy-released` is a new event on the same copy. (2) Whether an internal event of the same aggregate takes a number is not written. The example data (1, 2, 3 around `contact-details-recorded`) assumes it does not; "like the version of an aggregate" says it does. (3) Under ADR 12 a replaced fact "beside the old one" takes numbers on the same subject, and a consumer that follows only one of them sees gaps.
- Alternatives: (a) say that the number counts *published* events of a subject and that a consumer records the number of every published event it receives, handled or not — costs: every consumer must receive all published events of a subject it follows, so "ignore unknown events" is no longer free; (b) number per subject and per event family (copy lifecycle, copy condition), one family per consumer need — costs: more numbers to keep, a modelling rule; (c) drop gap detection where events are state-carrying (see F1 a) and keep only "apply if higher" — costs: only for streams whose events carry the whole state.
- Level and next step: architecture. Proposed ADR text for ADR 11/12 before ADR 12 is accepted; today there is no concrete failure, the first one is scenario F.

### F3 ADR 12 contradicts itself on enumerations, treats one real option as a straw man, and its first rule is expensive for a plausible change
- Severity: should fix
- Lens: pattern
- Evidence:
  - ADR 12, list of incompatible changes: "adding a value to an enumeration that a consumer decides on"; paragraph "Enumerations": "Adding a value is therefore compatible only where the contract names that safe default."
  - `model/esdm/catalogue/copy-registered.esdm.yaml` and `copy-corrected.esdm.yaml`: `home-branch` is an enum of the four branches; `model/esdm/lending/copy.esdm.yaml`: `home-branch: type: string`.
  - ADR 12, Consequences: "Neutral, because ... While both module and consumer are in the same commit and nothing is stored, nothing stops the team from changing both at once"; option 3 is rejected as "fails at the first stored event", while the same record says storage "is not known before G2".
  - ADR 12 driver 2: "That needs a place where the consumers are listed. The model has one: the descriptions of events and mappings, and the contract table of chapter 7." (see F4)
- Why it matters: (1) A consumer that decides on a value *and* has a named default is both "incompatible" and "compatible"; copy `kind` is exactly that case. (2) The brief opens with "four branches" and a fifth branch is a normal change. With the enumeration in `copy-registered` and `copy-corrected` the first rule makes it two new facts beside two old ones, for a change that touches only a list. (3) The Neutral bullet describes a fourth option, "additions by default, breaking changes in one commit while nothing is stored and all consumers are in the repo", and that is what option 3 competes with in practice. The three listed options are not the three real ones. (4) Nobody owns the list of branches: the lending glossary defines *branch* as "One of the four library sites", catalogue uses it without a definition.
- Alternatives: (a) keep the recommendation but fix the text: a value added to an enumeration is compatible iff the contract names the default; add "and every consumer that decides on it" to the contract table — costs: one paragraph; (b) add the fourth option (expand/contract only when needed: breaking change allowed in one commit while nothing is stored, else new fact) and decide between it and the first — costs: a longer ADR, a decision that depends on G2; (c) model `branch` as an open string whose list is owned by one context — costs: a business question about who owns the branches (draft C-nn).
- Level and next step: architecture (ADR 12 stays `proposed`; amend before the maintainer decides); the branch owner is business (draft C-nn, the agent may decide it, delegated).

### F4 "The model is the source of the contracts" is not borne out: the owner of each policy, the published/internal mark and the consumers are not in the model or the export
- Severity: should fix
- Lens: ownership
- Evidence:
  - `chapters/07-flows-and-contracts.md`: "The model in Studio is the source of the contracts. The tables above are made from it"; "The contract lives in the model in Studio; this repository has no second copy of it."; "All ten policies have one, written at the start of the description."; "A published event is marked in the description by its first words, 'Published to …' or 'Internal to …' (tool gap 19)."
  - `docs/adr/0012-changing-published-events.md`: "The model in DDD Studio is the source of the contract (schema, owner, consumers)."
  - `docs/tool-gaps.md` gap 19: "An event has no mark ... and no list of its consumers"; gap 14: "the model has no place for [the owner] except the description".
  - Studio `get_node` on policy `keep-unpaid-fees-hold-in-line` returns only `deliveryGuarantee`, `idempotency` and refs, no description; the same for the events `hold-placed`, `contact-details-recorded`, `copy-returned` and the aggregates I opened. In `model/esdm/` only the 9 files in `integration/` contain a `description`; none of the 10 policies and 29 events does. `explain_model` (fields-and-validation) says "description is text ... (both optional, on every kind)", so the field exists; I do not know whether it is empty or not shown by the tools.
- Why it matters: A reviewer who has the export and the MCP tools cannot find the owner of any policy, the Published/Internal mark, or who consumes a field. What I could do is derive the 13 published events from the `handles` of the policies; that works, but it is not what the chapter says. The columns "What the consumers use" and "Carried, not used yet" of the contract table exist only in the chapter, which is a snapshot, so in this repository the chapter *is* the second copy. The skill step 4 ("Record it in the model ... in the description of the node and of the mapping") and ADR 12 ("the owner updates the contract in the model first, naming each consumer") rest on this. If the descriptions exist, the export (the reviewable record, per `g1-model-to-code.md` §8) does not carry them; if they do not, the criterion C2 ("a policy has no clear owner") was answered from the derivation, not from the owner written in the model.
- Alternatives: (a) write owner and consumers into the descriptions (if the tool can) and check that the export carries them — costs: 39 descriptions, a check in `check_repo.py`; (b) keep an explicit contract file in the repo, generated or hand-kept, and say in the chapter and ADR 12 that it is the list of consumers — costs: a second copy that can drift; (c) accept the chapter table as the list of consumers and fix the wording ("source" becomes "derived from the model, completed in the chapter") — costs: ADR 12 must then say where "the last consumer has moved" is checked.
- Level and next step: way of working. Decide (a) or (b); correct the sentences in chapter 7 and ADR 12 whichever it is.

### F5 The order contract: membership forgets a lifted hold, so a repeated or late "place" can re-block; fees keeps a belief it is never told; a refusal has no consequence
- Severity: should fix
- Lens: ownership / scenario (repeat, late)
- Evidence:
  - `model/esdm/membership/member.esdm.yaml`: `holds` items (`reason`, `placed-by`, `decided-at`) exist only while the hold is on; `lift-hold` removes it.
  - `docs/adr/0005-no-circle-between-modules.md`: "`membership` ignores a request that is older than the last one it applied for the same hold, so a late 'lift' cannot undo a newer 'place'."
  - `model/esdm/policies/keep-unpaid-fees-hold-in-line.esdm.yaml`: `deliveryGuarantee: at-least-once`; `idempotency.owner: downstream`.
  - `model/esdm/fees/reader-account.esdm.yaml`: `hold-placed: boolean` (required); `fees` handles no membership event.
  - Chapter: "An order about a member that membership does not know is refused with the reason 'member not known yet'."; skill `design-context-contracts` step 3: "Where a reaction can fail, say what the owner of the order sees."
- Why it matters: (1) E2b: "place" at 06:00 applied, "lift" at 07:30 applied, the hold is gone. If the policy delivers "place 06:00" a second time (at-least-once), membership has no "last applied" to compare with and places the hold again. `fees` believes `hold-placed = false` and the amount is EUR 10.00, so it sends nothing more until a new charge: the reader stays blocked. ADR 5 covers the late "lift" only. (2) "Older than" does not say what happens with an equal `decided-at`. (3) `hold-placed` in `fees` is a local belief about a state that `membership` owns and that only an accepted order changes; the chapter lists lending's local copies as the cost of the cut (finding 1) but not this one. (4) For the refusal the chapter says what membership does, not what `fees` does (retry? list? drop the order?), so the owner of the order does not know what it sees.
- Alternatives: (a) membership keeps, per (placed-by, reason), the last applied `decided-at` even after the hold is lifted — costs: a few bytes per member, a field in `member`; (b) orders carry a number per (`fees`, reader) like events and membership applies "next number, ignore repeat" — costs: a second numbering to keep; (c) make the order idempotent by meaning ("the hold 'unpaid fees' is on/off as of t") and let the morning run re-send the state of every reader in arrears — costs: a daily order per blocked reader, but it also heals a lost order and removes the flag in `fees`.
- Level and next step: architecture. Amend ADR 5 or put it in ADR 12/ADR 11; decide with chapter 9 (`fees`) at the latest. For the refusal: a short rule in the order contract (business-safe default: `fees` retries and lists).

### F6 The question "which reservations ran out" returns no title, so the staff page cannot build the list without asking back
- Severity: should fix
- Lens: scenario
- Evidence:
  - `model/esdm/lending/list-reservations-that-ran-out.esdm.yaml` (and read model): result fields `reservation-id`, `member-id`, `copy-id`, `branch`, `ran-out-on`; no `title-id`. Slice "The staff page asks lending: which reservations ran out?": `{"branch": "riverside", "copy-id": "c-0004", "member-id": "m-0002", "ran-out-on": "2027-01-04", "reservation-id": "r-0003"}`.
  - `model/esdm/catalogue/get-title-details.esdm.yaml`: parameter `title-ids`.
  - `model/esdm/lending/bounded-context.esdm.yaml`, *morning list*: "the staff page adds names and phone numbers from membership and titles from the catalogue (C-31)." The overdue row does carry `title-id`.
- Why it matters: skill step 3 ("Can it act with what it gets, without asking back?"). The page has a `copy-id` and the catalogue answers only for titles. It must ask lending a second question (the `copy` aggregate has the `title-id`) or the catalogue a question that does not exist. The same two lines also show that the list questions return only the rows found: the example asks for `m-0002` and `m-0003` (and `t-0001`, `t-0002`) and gets one row each; what the page shows for an unknown id is not in the contract. `get-contact-details` also returns `postal-address`, which the lists do not need (C-31: "phone").
- Alternatives: (a) add `title-id` to the read model and the query result — costs: one field, the `reservation-expired` event or the read model must know the title; (b) a catalogue question by `copy-id` — costs: a new question and a catalogue answer about copies; (c) leave it and add a second lending question — costs: a round trip per list.
- Level and next step: review; fix in Studio (a), then say in the question contract what a list returns for an unknown id.

### F7 The chapter drops two events and cites C-28, which says the events stay
- Severity: should fix
- Lens: ownership (decision trail)
- Evidence:
  - `chapters/07-flows-and-contracts.md`: "*Card Expired* and *Researcher Status Expired* have no consumer and are not modelled (C-28)."; "No event is needed for a card to *expire*".
  - `requirements/clarifications.md` C-28, option 1: "The events stay, for information."; Consequence: "C-09 stays true: time causes the end; the event only reports it."
- Why it matters: the decision of C-28 is the dates; the sentence about the events was part of the same entry and is now reversed while citing it. Per `CLAUDE.md` an entry may be brought in line only "as long as the decision itself stays the same". Dropping the events is sensible (nobody consumes them, scenario I is out of scope), but C-32 (keeps become normal reservations "on the first day after the status ends") will need `lending` to act on a date without any event, and nobody has said so.
- Alternatives: (a) amend C-28 in the log ("the events are not modelled until a consumer needs them; lending compares dates; C-32 is applied by lending's own daily check"), marked decided by the agent (delegated) — costs: one entry; (b) model the two events as internal-to-membership information — costs: two events nobody reads.
- Level and next step: business, delegated. The agent can decide (a) and log it; no question to the maintainer is needed unless he wants the events.

### F8 More fields are carried without a consumer than the chapter admits, and the reason given for one of them does not fit
- Severity: should fix
- Lens: pattern
- Evidence:
  - Chapter finding 6: "The usage-fee mark travels in the copy events and the reason in the hold events."
  - Chapter table, column "Carried, not used yet": "card number" (member registered), "reason" (copy withdrawn), "copy" (three loan events), "ISBN, title, author (the catalogue's own page)" (title added, title details corrected).
  - `design-context-contracts/SKILL.md`: "Fields that no consumer rule needs are removed." ADR 12: "(the usage-fee mark and the reason of a hold travel today although no consumer uses them yet)".
  - `model/esdm/catalogue/title-details.esdm.yaml`: the read model for the catalogue's own page is fed inside `catalogue` by the same events; no other context uses the title events except `fees` for the price.
- Why it matters: `fees` receives the author and ISBN of every title; "the catalogue's own page" is not a consumer of an event that is published to another context. The card number is personal data that `lending` does not need. The reason given for keeping fields (a field added later is missing from old events, ADR 11 driver 2) is weakened by ADR 12 itself: under ADR 12 a new field is compatible and old consumers ignore it; the loss exists only for *stored* events, which G2 decides. The chapter names two exceptions where the table shows at least six.
- Alternatives: (a) apply the rule: remove the fields without a consumer, keep and name only the two with a reason (usage-fee mark, hold reason) — costs: later additions, which ADR 12 calls free; (b) keep all and list each with its reason in finding 6 and in the skill — costs: wider events, privacy for the card number; (c) publish a narrow price fact for `fees` and let the catalogue's page stay internal — costs: one more event.
- Level and next step: review (the agent can decide); say the same thing in the skill (F12).

### F9 The test of the cut is documented per criterion, not per flow, and two things the test should cover were not played
- Severity: should fix
- Lens: scenario
- Evidence:
  - Chapter: "The skills ask for the five abort criteria of the phase model on every flow, with the result written down also when nothing is found."; the table is "Criterion | Result" with no flow. `model-flows/SKILL.md` step 5: "write down the result per flow".
  - Brief §3.4: "The total for one book never exceeds its replacement price." Example data: the longest fine is 22 days = EUR 11.00 against a price of EUR 18.00; no slice reaches the cap. Chapter: "A fine is never counted without its cap".
  - Slices: none of the 51 has the node `get-amount-owed` (35ea02d5…) or the read model `amount-owed`; J1 asks lending, membership and catalogue only. Chapter row 11: "staff pages → lending, membership, catalogue, fees ... six queries".
  - Chapter: "There are eleven, and each one has exactly one kind ... and one owner of the reaction"; row 11 says "none". The skill (step 4) asks for columns scenario, step, late-or-twice; the chapter's table has none of them.
- Why it matters: the cap is the one rule where `fees` combines a fact of `catalogue` (price) with a fact of `lending` (days) in one number, which is the closest thing to criterion C1 in this increment; it is claimed but not played. One of the six contracts is not exercised by any flow ("a contract without a crossing is not needed", skill). "Eleven" is a count of groups; the number of contracts is 21.
- Alternatives: (a) add a flow slice pair E1b (a 40-day-late return of a EUR 6 paperback, fine capped at EUR 6.00; or use *The Hobbit* with 40 days: EUR 18.00 not 20.00) — costs: two slices; (b) add a step "the desk asks fees for the amount owed" to E2-E3 — costs: one slice; (c) replace the "Criterion | Result" table by the per-flow table of this report — costs: nothing.
- Level and next step: review.

### F10 Language: `member-id` throughout `lending` against its own "avoid member"; `fees` uses words it does not define
- Severity: should fix
- Lens: language
- Evidence:
  - `model/esdm/lending/bounded-context.esdm.yaml`, *reader*, avoid: "`member` — The membership office's word; here the person is a reader (C-07)." `model/esdm/lending/reader.esdm.yaml`: `identifiedBy: field: member-id`; `loan`, `reservation`, `overdue-loans`, `reservations-that-ran-out`: all `member-id`.
  - Chapter finding 7: "A word of one context therefore appears in the payloads of two others. It is the identifier, not a concept".
  - `model/esdm/fees/bounded-context.esdm.yaml`: *late fine*: "never more than the replacement price"; *arrears*: "holds the reader's card through membership". There is no entry for *replacement price*, *hold*, *card*, *loan*, *due date*. Aggregate `title-price` (command `record-title-price`) and the field `replacement-price-cents` name the same thing; `reader-account` has the field `hold-placed`, which is also the name of membership's event.
  - `docs/reviews/pre-g6-context-cut.md` F9 (same point, deferred "when `fees` is modelled (chapter 9)").
- Why it matters: the chapter justifies `member-id` in payloads, but the word is also in lending's own aggregates and queries, where the glossary says to avoid it. Without a glossary line the next reader of `lending` takes it as a lapse. In `fees` chapter 7 added the two concrete cases of F9 (*title price* beside *replacement price*, a flag named like a membership event).
- Alternatives: (a) add one line to each glossary: lending/fees "`member-id` is the identifier membership issues for the reader (ADR 7); the field keeps the name"; fees entries for *replacement price* (source: catalogue) and *hold* — costs: three to five entries; (b) rename to `reader-id` inside lending and fees and map at the boundary — costs: ADR 7 reading, about 20 fields, and the contracts of ADR 11 lose the single name.
- Level and next step: review (agent decides, recommend (a)).

### F11 The renewal example date follows no rule, and the rule is not decided
- Severity: should fix
- Lens: scenario
- Evidence:
  - Slice "Membership office renews the card": member m-0001, card valid until 2027-11-01 (registered 2 Nov 2026), renewal `occurred-on: 2027-10-20`, `card-valid-until: 2028-10-31`.
  - C-28: "A card granted on 25 October is valid up to and including 24 October of the next year". `model/esdm/membership/bounded-context.esdm.yaml`, *renewal*: "Making a card valid for another year."
- Why it matters: renewed from the old end the new date would be 2028-11-01, renewed from the renewal day 2028-10-19; 2028-10-31 is neither. The sources do not say whether an early renewal extends the old end or starts on the day; the member loses 12 days or gains 12 days, and `lending` compares the date literally.
- Alternatives: (a) from the old end if the card is still valid, from the day of renewal if it has expired — costs: no loss for early renewers; (b) always from the renewal day — costs: early renewal wastes days, simple rule; (c) always from the old end — costs: a long-expired card is renewed into the past.
- Level and next step: business, delegated; draft C-nn, the agent decides, recommend (a); fix the example in Studio.

### F12 The two new skills are generic, but they and the chapter disagree in five places and miss three things
- Severity: should fix
- Lens: pattern (skills)
- Evidence: `grep` of both skills for library words (`lending`, `fees`, `catalogue`, `membership`, `reader`, `copy`, `loan`, `ADR`, `C-nn`, EUR): no hit. Mode 2 of `challenge-context-cut` says "a loan or reservation" and "kept in the chapter" appears in `model-flows` step 4; both are generic enough.
  1. `model-flows` step 5 asks the result "per flow"; the chapter gives it per criterion (F9).
  2. `model-flows` step 4 asks for scenario, step, late-or-twice in the crossing table; the chapter's table has none of them.
  3. `design-context-contracts` rule: "Fields that no consumer rule needs are removed."; the chapter keeps at least six (F8) on the strength of a reason that is in ADR 12, not in the skill.
  4. The same skill states "Fields are added, not changed or removed" as a rule, which is the content of ADR 4/ADR 12 (the latter `proposed`); a generic skill should say "the rule of the architecture record".
  5. Step 4 "Record it in the model ... in the description of the node and of the mapping" cannot be checked (F4).
  - Missing: (i) a reviewable record of the flows: they are not exported (tool gap 16), the chapter table gives only names and counts, and the example data exist only in Studio; a reviewer without MCP cannot repeat this review; (ii) how a *question* crossing is drawn in a flow (J1 uses read-model slices) and what an *order* shows when it fails (F5); (iii) the check "does the consumer see every number of the subject it follows" for the ordering rule (F2). G1 §7 also asks for "one conventions file that each skill reads"; neither skill names one.
- Why it matters: the skills are what the next project would run; five of the places above would have produced a different chapter.
- Alternatives: change the skills to match what was learned (allow "carried for later, named with its reason in an architecture record"; add the extra columns and the per-flow table) — costs: two small edits; or change the chapter to match the skills — costs: F8, F9 work.
- Level and next step: way of working. Edit the skills when F8/F9 are decided.

### F13 The recommendation for J2 reverses part of C-31 without saying so, and the reason against option (b) is thin
- Severity: note
- Lens: ownership
- Evidence:
  - C-31, options: "2. Each context keeps what it needs." (not chosen); Decision: "contact details belong to the person, not to a loan."; mapping `membership-lending-customer-supplier`: "Contact details do not travel: staff pages ask membership (C-31)."
  - Chapter: "(a) Lending keeps the address. `membership` publishes its contact details as a fact, `lending` keeps a copy of phone and email"; "**Recommendation for J2: (a).** It is the option that keeps within the rules we have."; (b) is rejected because it is "a new kind of element that listens to events from outside, which ADR 8 does not provide for."
- Why it matters: (a) is option 2 of C-31 for one attribute, and the chapter writes the personal-data cost but not that it undoes a decided entry (`CLAUDE.md`: stop and ask when a choice would undo an earlier decision). ADR 8 is about user interfaces; ADR 3 lets an outside caller use "the public API", which includes published events, so the rejection of (b) needs an argument other than ADR 8. (c) is correctly ruled out by ADR 5. Nothing is built on this now.
- Alternatives: keep (a) with an explicit "supersedes part of C-31" for the maintainer at J2; or (b) with a one-line ADR on outside subscribers — costs: a new element kind.
- Level and next step: business and architecture, at J2; no action in this chapter except the sentence "keeps within the rules we have".

### F14 Example data contradicts itself across flows, hides an open rule, and mixes day and instant
- Severity: note
- Lens: scenario
- Evidence:
  - Same ids in different flows: `c-0001` is returned on 15 Dec (flow C) and withdrawn with reason `lost` on 20 Dec (A2) with no loss declared; `c-0002` is returned damaged on 16 Dec as `l-0002` (C) but reserved on 2 Nov and checked out as `l-0003` on 3 Nov (D); `r-0003` expires with `occurred-on: 2026-11-08` (D) and "ran-out-on": "2027-01-04" (J1).
  - Flow C: "Reader returns the copy at Riverside in time" for loan `l-0001` checked out at `central`: a return at another branch is an open question (C-14, parked).
  - Orders: `"decided-at": "2026-12-23T06:00:00Z"` against the date `occurred-on` for business days; the sources never give the library's time zone.
- Why it matters: each flow is one example run, so this harms no cut. But a reader of Studio sees one timeline, and the C-14 case is built into an example as if decided. A UTC instant against a local business day matters at the morning run.
- Alternatives: use distinct ids per flow; mark the C-14 step "inferred, C-14 parked"; state the time zone convention in ADR 11 or a clarification.
- Level and next step: review.

### F15 Smaller mismatches between text and model
- Severity: note
- Lens: language / pattern
- Evidence:
  - `catalogue-fees-published-language`: "The same catalogue events as for lending, in the same format"; `catalogue-fees-open-host-service`: "and whether a copy is a usage-fee copy ... Same service as for lending." The consumers share no event in this increment (lending: 3 copy events; `fees`: 2 title events). Heuristics §6: an open host service is "worth it for several consumers or a stable public contract, not for the count of consumers alone".
  - Chapter finding 1: "every command of `lending` that lends or reserves is decided from `reader` and `copy`"; the five-reservation limit and the overdue limit per branch (brief §3.2; C-14) also need `reservation` and `loan`. This is inside `lending` (not a boundary problem) but the sentence is wrong and the aggregate question is open.
  - C-27 option 1: "A copy that is out stays out"; nothing is said about a copy that is *reserved* when it is corrected to restricted by a normal reader's reservation (the C-32 rule exists for status ends only).
  - The Big Picture board (`model/sketch/big-picture-contexts.json`) still shows *Loan Became Overdue*, *Card Expired* and *Researcher Status Expired*; the chapter says no board was changed and records the divergence in finding 2 and in the decisions.
- Why it matters: small, but each is a stale or inexact statement of the kind step 5 of mode 2 looks for.
- Alternatives: correct the two mapping descriptions; fix the sentence in finding 1; draft C-nn for "copy corrected to restricted while reserved" (the agent may decide, delegated); a line in the chapter next to the board.
- Level and next step: review; business for the correction case (draft C-nn).

### F16 Rules stated as contract that are inferred or rest on a proposed record
- Severity: note
- Lens: ownership
- Evidence:
  - Chapter: "A return, or the morning run, for a loan whose title price fees does not know yet is held back or left out of the count and listed as waiting. A fine is never counted without its cap, and a lost book is never charged as free." Source: ADR 11 speaks of the usage-fee mark and of an unknown copy, not of the price.
  - Chapter: "Every unknown value of an enumeration is read on the safe side: an unknown copy kind is not lendable." Source: the "Enumerations" paragraph of ADR 12, which is `proposed`.
  - Chapter: "The two that ask for people and titles take a **list**, because a morning list has dozens of rows"; the brief gives no volume.
- Why it matters: `CLAUDE.md`: "Every claim needs a source or is marked as inferred". Leaving a loan out of the morning count means the card is not blocked when it should be (the direction of F1).
- Alternatives: mark the three as "inferred" in the chapter; for the first, decide whether a missing price should block the reader (fail closed) or not.
- Level and next step: review.

## Decisions: what is decided that is not, and what is asked that need not be

- **Decided by the agent but belongs to the maintainer, or reverses a decision:** (1) dropping *Card Expired* and *Researcher Status Expired* against C-28 (F7; low weight, the agent may log it); (2) the J2 recommendation (a) that reverses part of C-31 (F13; at J2). The removal of *Loan Became Overdue* follows `CLAUDE.md` (ADR 9's wording brought in line, decision unchanged, said so in the chapter); I would add the note to the board (F15). The envelope field names, `blocked`, the title on the checkout and `reader-account` are details and fit the "Decided by the agent" rule; the aggregate `reader-account` per reader holds all loans of a reader and may need a second look in chapter 9 (not judged here, out of scope).
- **Asked that the agent could decide:** finding 1 of the chapter ("The maintainer should be aware that it is the case") is already ADR 4's decision and consequence ("a downstream module keeps its own copy of what it needs ... Copies can be late"); it is not a new question. The renewal rule (F11), the copy corrected while reserved (F15) and the owner of the branch list (F3) are delegated business questions; the agent should decide and log them.
- **Rightly left to the maintainer:** ADR 12 (architecture, hard to reverse, real alternatives); but see F2 and F3 before he decides.

## Questions for the maintainer

1. **ADR 12.** Do you want it decided as written, or amended first for F2 (numbers and ignored events) and F3 (enumerations, the missing fourth option)? My advice: amend first; it is cheap now and the first failure is scenario F.
2. **Gaps in the member's stream (F1).** Should the membership events carry the whole status so that lending never needs to hold a block back (a), or should lending fail closed while a gap exists (b)? This is an architecture decision (proposed ADR).
3. **Orders (F5).** Should membership remember the last decision per hold after a lift (a), number orders (b), or should the morning run re-assert the state (c)? Architecture; needed before chapter 9.
4. **Where is the contract kept (F4)?** If Studio cannot hold the owner and the consumers in a form the export shows, is a contract file in the repo (a second copy) acceptable, or should the tool gap wait until G4 and the chapter table be the list? Way of working.
5. **Branches (F3).** Who decides that a branch opens or closes, and should the list be an enumeration in the events? Business; the agent may decide it (delegated); draft C-nn.
6. **Renewal (F11), copy corrected while reserved (F15), C-28 events (F7).** Three delegated business items; tell the agent only if you want an answer other than the recommendation in this report.
7. **J2 (F13).** Not now: when J2 comes, do you accept that (a) partly undoes C-31?
