# Context cut challenge: after chapter 4 (9e404d9)

Input: snapshot of commit 9e404d9 (after chapter 4). Files read:
`requirements/brief.md`, `requirements/clarifications.md`, `model/esdm/**`
(4 bounded contexts, 4 subdomains, 3 external systems, 10 mappings),
`model/sketch/big-picture-contexts.json` (saved version
`ch3-context-cut-v3`), `model/domain-stories/*.yaml` (2 stories),
`chapters/03-strategic-design.md`, `chapters/04-deployment-decision.md`,
`docs/adr/0002` to `0008`. No Studio calls; the exports are the input.
Run by: fresh agent, 2026-10-23

## What holds

- **Each of the four contexts has a reason to exist** (canvas, §1). Each
  has a decider of its own named in the brief (Head of Collection, Branch
  Librarian, Membership Officer, Treasury Liaison), decisions of its own
  (register a copy as circulating or restricted; reserve, check out,
  limits; register, grant researcher status, holds; assess, charge,
  arrears) and a vocabulary of its own. None is a pass-through, an entity
  service or a context cut by technology. Lending has the most cards, but
  the other three make real decisions, so it is not a god context.
- **The dependency graph is acyclic** (§4). From the mappings and from
  who reacts to whose events: catalogue → lending, catalogue → fees,
  membership → lending, membership → fees (fees gives orders to
  membership's API), lending → fees. No context reacts to fees, and
  membership reacts to nobody. The cycle that chapter 3 had is gone, and
  ADR 5 removed it in the right order: owner first (C-19), structure
  second (`docs/adr/0005-no-circle-between-modules.md`: "This version
  decides the owner first (C-19) and then checks that the result has no
  circle.").
- **The €10 rule has one owner** (§3). Reason, threshold and decision all
  sit in `fees`; membership only keeps holds. The hold carries the party
  that placed it, which passes the "can one party undo another's
  decision?" test (`model/esdm/membership/bounded-context.esdm.yaml`:
  "Whoever placed a hold lifts it; nobody lifts another party's hold
  (C-19)."). A late "lift" is handled too (ADR 5: "a late "lift" cannot
  undo a newer "place"").
- **Likely changes stay local** (§5). Threshold or counting rule of the
  block (C-18): fees only. Reservation period (C-12), per-branch overdue
  limit (C-14), waiting line (C-15): lending only. 28-day loans (C-13):
  lending, plus catalogue if "new release" is a property of a title;
  fees is not touched as long as the loan events carry the due date
  (`lending-fees-published-language`: "with due date and copy"). Readers
  paying online (C-02 option 3): fees and a user interface. None touches
  three contexts.
- **Both anti-corruption layers are real** (§6): there is something
  foreign to translate ("odd status codes, amounts in cents, references
  limited to 20 characters"; "Titles and authors come back oddly
  formatted").
- **membership → lending is a real customer–supplier** (§6): lending's
  needs are stated and negotiated ("Lending says what it must know about
  a member: card valid, not blocked, researcher or not").
- **Same word, different meaning is recorded** (§2). *copy* differs
  between catalogue ("One physical book with its own barcode") and lending
  ("what may be done with it right now"); *reader* and *member* are the
  same person in different contexts, and every glossary lists the
  `avoid` words with C-07.
- **No context for notifications, and no context for the reader account.**
  Both would be contexts without a language or a decision of their own;
  ADR 8 puts the account page outside the modules.

## Findings

### F1 The end of a copy's life has no owner, and the obvious fix would bring back a cycle
- Severity: should fix
- Lens: ownership, dependencies
- Evidence:
  - `requirements/clarifications.md` (C-04): "a lost book ends a loan, takes a copy out of the collection and creates a fee: three areas meet here."
  - `requirements/clarifications.md` (C-17): "Repair and withdrawal happen outside the system and the copy is released by hand."
  - `chapters/03-strategic-design.md`: "Handling them inside the system would make the relationship between lending and catalogue two-way, which we deliberately avoid for now."
  - `model/esdm/catalogue/bounded-context.esdm.yaml` (copy): "One physical book with its own barcode, registered under a title. Circulating or restricted." There is no state for lost or withdrawn, and no mapping from lending to catalogue.
  - `model/sketch/big-picture-contexts.json`: *Book Declared Lost* is tagged `theme:lending,theme:fees` and has edges only to fees; *Book Found Damaged* is tagged `theme:lending,theme:collection`.
  - `requirements/brief.md` (§3.1): "we own eleven copies of it across the branches."
- Why it matters: C-04 says a lost copy leaves the collection, but the
  model has two of the three areas only. The collection's own record
  would still count a lost copy as owned. The damaged case was decided
  (C-17, "released by hand", but in which context, by whom?); the lost
  case was not. Whoever models `catalogue` first (ADR 5: "`catalogue` and
  `membership` first") will meet the question. The natural answer
  ("catalogue reacts to *Book Declared Lost*") makes catalogue depend on
  lending while lending depends on catalogue: a cycle that ADR 3 forbids.
- Alternatives:
  - Lending owns the end of a copy's circulation (lost, withdrawn after
    damage); catalogue stays a register of what was acquired. Costs: the
    Head of Collection's question "how many copies do we still have?" is
    answered by lending or by a page that asks both (ADR 8), not by the
    catalogue.
  - The Head of Collection takes the copy out of the catalogue by hand,
    as for damage (C-17); catalogue publishes "copy withdrawn" and lending
    reacts. The arrow stays catalogue → lending. Costs: a manual step per
    lost copy and a gap between the desk recording the loss and the
    catalogue knowing it.
  - Catalogue reacts to lending's loss event. Costs: a cycle between
    catalogue and lending, which ADR 3 and ADR 5 forbid; it would have to
    be named as a partnership, which chapter 3 rejected.
- Level and next step: business (draft C-20: "When a copy is lost, does
  the collection's record have to know, and who takes the copy out of
  the collection?"), then review of the mapping.

### F2 Nobody owns which copies carry a usage fee, or how much it is
- Severity: should fix
- Lens: ownership, language
- Evidence:
  - `requirements/brief.md` (§3.4): "Some items in the special collection carry a usage fee — the archive insists on it. That's charged when the item is checked out, not when it's returned."
  - `model/esdm/fees/bounded-context.esdm.yaml` (usage fee): "A fee some special-collection items carry, charged at checkout (C-08)."
  - `model/esdm/integration/catalogue-fees-published-language.esdm.yaml`: "fees reads only the price."
  - `model/esdm/integration/catalogue-lending-published-language.esdm.yaml`: "copy registered with its circulating or restricted flag"
  - `model/esdm/integration/lending-fees-open-host-service.esdm.yaml`: "checkout of an item with a usage fee"
  - `model/sketch/big-picture-contexts.json` (fees policy): "When an item with a usage fee is checked out, charge the fee"
  - `model/esdm/catalogue/bounded-context.esdm.yaml` (replacement price): "The price recorded on a title"
- Why it matters: the policy in `fees` needs two inputs, "does this copy
  carry a usage fee?" and "how much?". No glossary owns the word, no
  published language carries it, and the brief names the archive as the
  party that insists on it. Fees reads only a *title*-level price, but a
  usage fee belongs to some *copies* ("We can have a circulating copy and
  a restricted copy of the same title"). Also, *item* is a word C-07
  dropped ("*Item* and *instance* are not used."), and "special
  collection" is in no glossary; it is not clear that it equals
  *restricted*. Catalogue's events are specified first (ADR 5 order), so
  the gap would surface as a later change to a published contract.
- Alternatives:
  - Catalogue owns it: the Head of Collection sets the usage fee when a
    copy is registered, like the circulating/restricted flag; catalogue
    publishes it and fees keeps it per copy. Costs: catalogue's language
    gains a money word per copy; fees keeps copy-level data, not only the
    title price.
  - Fees owns a tariff (which copies, what amount), set by the Treasury
    Liaison on the archive's instruction. Costs: fees must know copy
    identities from the catalogue and keep its list in step with new
    registrations.
  - Lending carries the flag in the checkout event. Costs: lending would
    hold a money rule it does not decide; not recommended.
- Level and next step: business (draft C-21: "Who decides which copies
  carry a usage fee and how much? Per copy or per title? Is the special
  collection the same as the restricted copies?").

### F3 The Big Picture board still shows the rejected design and the old words
- Severity: should fix
- Lens: language, ownership
- Evidence:
  - `model/sketch/big-picture-contexts.json`, membership area: event "Card Blocked (owes more than €10)"; against `docs/adr/0005-no-circle-between-modules.md`: "`membership` knows nothing about money."
  - Same board, fees area: policies "When a member owes more than €10, block the card" (edge "then block" to *Card Blocked*) and "When a member's fines are back at €10 or less, unblock the card" (edge "then unblock"). ADR 5 rejected exactly this: "**`fees` gives plain block and unblock orders.** … It was rejected because an unblock order cannot tell whose block it lifts." Fees' glossary avoids *member* ("The membership office's word for the same person (C-07).") and counts the *amount owed*, not fines (C-18).
  - `requirements/clarifications.md` (C-18): "The Big Picture policy and the glossaries of `membership` and `fees` use `amount owed`." Since chapter 4 the membership glossary no longer has it (`chapters/04-deployment-decision.md`: ""Amount owed" left its glossary"), and the unblock policy says "fines".
  - Same board: actor "Clock (daily, per branch)" sits in the lending area and has edges "checks every morning" to the fees block policy and "triggers" to *Card Expired* and *Researcher Status Expired* in membership. `docs/adr/0006-adapters-and-clock-inside-the-module.md`: "The daily checks (expired reservations, overdue loans, expiring cards, running fines) belong to the module that owns the rule." The €10 rule is not per branch.
  - Same board: event "Fine Paid" is the only payment event, and the "Monthly fines report: charged, paid, waived, outstanding" is fed by *Late Fine Assessed*, *Fine Paid* and *Fine Waived* only, while fees' glossary defines payment as "Money received for fines and fees".
- Why it matters: the project rule is that chapter text comes from the
  board. Anyone who models `fees` or `membership` from this board reads
  block/unblock orders, a money threshold in membership and a central
  clock in lending: the three things ADR 5 and ADR 6 decided against.
  ADR 5 defers only the hold itself ("the hold is modelled when
  `membership` is modelled"), not the policy wording. The "Fine Paid"
  name and the report feed also leave open whether lost-book and usage
  fees are paid, waived and reported like fines.
- Alternatives:
  - Update the board now: policies "When a reader is in arrears, place
    the hold 'unpaid fees'" / "… lift it", *Card Blocked* without the
    amount, one clock per context, a payment event that covers all
    charges. Costs: one board edit, a saved version and a new snapshot.
  - Leave the board and add a hotspot "superseded by C-19 / ADR 5 /
    ADR 6" on the affected cards. Costs: almost nothing now, but board
    and context map disagree until membership and fees are modelled.
- Level and next step: review (board edit). The report scope is
  business (draft C-23, see questions).

### F4 lending → fees is called an open host service for consumers the model sends elsewhere
- Severity: should fix
- Lens: pattern
- Evidence:
  - `model/esdm/integration/lending-fees-open-host-service.esdm.yaml`: "Other consumers (reader account, reminders) need the same events."
  - `chapters/03-strategic-design.md`: "Reminders and the reader account will need the same events, so lending publishes them once for everyone."
  - `chapters/03-strategic-design.md` (what we did not cut): reminders "all concern lending" and get no context of their own.
  - `docs/adr/0008-user-interfaces-outside-the-modules.md`: "The reader's account page asks `lending` and `fees` and shows both answers." (questions, not events; the separate view module that listens to events was option 2 and not taken).
  - `requirements/clarifications.md` (C-03): "fees has to know the due date of every loan and learn when it ends (returned or lost)".
- Why it matters: after chapter 3 and ADR 8 the only context that
  consumes lending's loan events is fees, and fees' needs shaped those
  events (due date for the running fine, loss, usage-fee checkout).
  That is the description of a customer–supplier, which chapter 3 itself
  gives: "Where the consumer's needs are negotiated one to one, as between
  membership and lending, *customer-supplier* fits better." The label
  matters for what lending promises: as an open host it publishes what it
  thinks is general; as a supplier it plans for fees, for example when a
  due date changes (C-13) or a loss is recorded.
- Alternatives:
  - Rename to customer–supplier (lending supplier, fees customer).
    Costs: the mapping, the chapter 3 table and the ADR 4 table change;
    nothing in the dependencies changes.
  - Keep open host service + published language, but justify it by the
    stable public contract that ADR 4 asks for, not by consumers that do
    not exist. Costs: wording only; the heuristic that count alone does
    not justify an open host is then honestly met.
- Level and next step: review. It revises a pattern approved in chapter
  3, so the maintainer decides.

### F5 A reader who pays at the desk may still be blocked at the desk
- Severity: note
- Lens: scenario (timing)
- Evidence:
  - `requirements/brief.md` (§3.3): "When they pay, we unblock."
  - `requirements/clarifications.md` (C-02): "the new system passes it to CityPay through its interface; a fine counts as paid when CityPay confirms."
  - `docs/adr/0005-no-circle-between-modules.md`: "`fees` … lifts it when the amount owed is €10 or less."
  - `docs/adr/0004-contexts-talk-through-published-events.md`: "Copies can be late; the rules of each context must say what happens then."
  - `model/sketch/big-picture-contexts.json`: "Branch Librarian (lending desk) --takes payment--> Fine Paid".
- Why it matters: played through, the reader pays at the desk, fees passes
  the payment to CityPay, waits for its confirmation, lifts the hold in
  membership, membership publishes the unblock and lending updates its
  copy of the member status: four crossings plus a round trip to a
  system we cannot change. The cut is not wrong (each step is owned by
  the right context), but until all four have happened, the reader who
  has just paid cannot borrow. The brief expects the unblock on payment;
  C-02 ties it to the confirmation. Nobody has said which wins.
- Alternatives:
  - Lift the hold when the desk receives the money ("received, not yet
    confirmed"), and place it again if CityPay rejects. Costs: a second
    payment state in fees and a re-block path.
  - Lift only on confirmation (as decided). Costs: the desk must be able
    to show "payment pending" and the reader waits.
  - Let staff lift the hold by hand. Costs: contradicts "nobody lifts
    another party's hold"; not recommended.
- Level and next step: business (draft C-22).

### F6 The catalogue's open host service is justified by the number of consumers
- Severity: note
- Lens: pattern
- Evidence:
  - `model/esdm/integration/catalogue-lending-open-host-service.esdm.yaml`: "Two contexts need title and copy data (lending for availability and restricted copies, fees for the price). One general service instead of two bespoke integrations."
  - `model/esdm/integration/catalogue-fees-published-language.esdm.yaml`: "Same catalogue events and price field that lending uses; fees reads only the price."
  - `model/esdm/lending/bounded-context.esdm.yaml`: no term for a price.
- Why it matters: the two consumers need different things (a flag versus a
  price), and lending is not shown to use the price at all, so "the price
  field that lending uses" has no source. The pattern itself is
  defensible (catalogue is a stable upstream for two modules), but the
  reason given is the count, which the heuristic does not accept on its
  own. If F2 is decided for the catalogue, fees' needs grow (price and
  usage fee), which makes the "general service" argument stronger.
- Alternatives: keep the pattern and give the stable-contract reason
  (costs wording); or two customer–supplier relationships (costs two
  negotiated interfaces for one small upstream; not recommended).
- Level and next step: review.

### F7 Where a copy belongs is in no context's language
- Severity: note
- Lens: language
- Evidence:
  - `requirements/brief.md` (§3.1): "we own eleven copies of it across the branches."
  - `requirements/brief.md` (§3.2): "You can only reserve a book that's on the shelf." and "every branch keeps its own count."
  - `model/esdm/lending/bounded-context.esdm.yaml`: branch "One of the four library sites"; copy "on the shelf, reserved or on loan".
  - `model/esdm/catalogue/bounded-context.esdm.yaml`: copy has no branch.
- Why it matters: reservations happen at a branch and "on the shelf" means
  a particular shelf, but no glossary says which branch a copy belongs to
  or who decides it (the collection at registration, or the branches).
  If the collection decides, catalogue publishes it (direction holds); if
  copies move with returns, lending owns it. Not a failure yet; it
  becomes one when the reservation rules are modelled.
- Alternatives: home branch as a catalogue attribute (costs a field in
  catalogue's events); current location as lending state (costs nothing
  at the boundary, but the Head of Collection loses the view).
- Level and next step: business (draft C-24), with the parked C-14.

## Questions for the maintainer

1. (F1, draft C-20) When a copy is declared lost, does the collection's
   own record have to know, and who takes the copy out of the collection:
   the system, or the Head of Collection by hand as for damaged copies?
2. (F2, draft C-21) Who decides which copies carry a usage fee and how
   much it is: the Head of Collection at registration, or the Treasury
   Liaison on the archive's instruction? Per copy or per title? Is the
   "special collection" the same as the restricted copies?
3. (F5, draft C-22) A reader pays at the desk: is the card usable again at
   once, or only when CityPay has confirmed the payment?
4. (F3, draft C-23) Does the monthly report ("fines charged, paid,
   waived, outstanding") include lost-book fees and usage fees, and can
   those be paid and waived like fines?
5. (F7, draft C-24) Does each copy belong to one branch, and who decides
   that: the collection or the branches? Does a copy returned at another
   branch move there?
6. (F4) Do you want lending → fees renamed to customer–supplier, or kept
   as an open host service with a different reason?

## Appendix: canvases and scenario counts

**Canvases** (fields left empty when the sources say nothing).

| Context | Purpose | Class | Decisions | Receives | Sends | Own words |
|---|---|---|---|---|---|---|
| catalogue | Know what the library owns: titles and their copies | supporting | title may be added; copy circulating or restricted; replacement price | ISBN details (ACL) | title and copy events | title, copy, circulating, restricted, replacement price |
| lending | Decide what may be done with a copy right now | core | reserve, check out, return, overdue, limits, lost (recorded at the desk) | catalogue events, member status | loan events | reader, copy, loan, due date, overdue, reservation, researcher, branch, morning list |
| membership | Decide who is a member and whether a card may be used | supporting | registration, researcher status, renewal, expiry, holds | place/lift hold orders | status and block events | member, library card, researcher status, hold, blocked card, expired card, renewal |
| fees | Decide what a reader owes and whether they are in arrears | supporting | assess, charge, arrears; waiver (who decides: C-16, parked) | loan events, price, CityPay confirmation (ACL) | hold orders | reader, late/running/assessed fine, lost-book fee, usage fee, payment, waiver, amount owed, arrears |

**Scenarios played** (boundary crossings at run time; no context asks
another during its own work in any of them, so no round trips between
modules).

| Case | Contexts | Crossings | Result |
|---|---|---|---|
| Reserve, collect, borrow, return in time (story `reserve-borrow-return`) | lending, fees | 2 (checkout, return events to fees) | holds |
| Overdue, running fine passes €10 on day 21, return, pay, unblock (story `overdue-book-fine-and-blocked-card`, timing) | lending, fees, membership, CityPay | 5 plus a CityPay round trip | holds; desk timing open (F5) |
| Researcher with 3 overdue at Riverside reserves at Central (exception, brief §3.5) | lending | 0 | holds |
| Copy declared lost while a running fine counts | lending, fees, (catalogue?) | 1, plus an unowned one to catalogue | F1 |
| Checkout of a special-collection copy with a usage fee | catalogue, lending, fees | 2, input unowned | F2 |

**Change scenarios**: block threshold (fees only), reservation period
(lending only), 28-day loans (lending, perhaps catalogue), waiting line
(lending only), online payment (fees and a user interface). None touches
three contexts.
