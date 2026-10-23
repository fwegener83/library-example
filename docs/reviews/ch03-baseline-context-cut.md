# Context cut challenge: chapter 3 (6547c0c)

Input: snapshot of commit 6547c0c (end of chapter 3), files read:
`requirements/brief.md`, `requirements/clarifications.md`,
`model/esdm/**` (4 bounded contexts, 4 subdomains, 3 external systems,
10 mappings), `model/sketch/big-picture-contexts.json` (saved version
`ch3-context-cut-v3`), `model/domain-stories/*.yaml` (2 stories),
`chapters/03-strategic-design.md`; `chapters/01-big-picture.md` and
`chapters/02-domain-stories.md` searched for passages on block, clock and
loss. No `docs/adr/` in the input. Studio not consulted.
Run by: fresh agent, 2026-10-23

Quotes are exact; line wraps in the source are joined with a space. Board
edges are written as `"<source card>" --<label>--> "<target card>"`, card
texts and labels as in the snapshot JSON.

## What holds

- **The seam catalogue | lending** — passes language, decider and
  pace. "copy" has two definitions ("One physical book with its own
  barcode, registered under a title" vs "A physical book and what may be
  done with it right now: on the shelf, reserved or on loan"), two
  deciders (Head of Collection, Branch Librarian), and the brief draws the
  line itself: "What happens to a book after it leaves my desk is the
  branches' business, honestly. I don't need to know who has it." (brief
  §3.1). Keeping *availability* in lending and rejecting the partnership
  (chapter 3, "Rejected") keeps the arrow one-way.
- **Both anti-corruption layers** — pass §6: there is something foreign to
  translate. CityPay: "odd status codes, amounts in cents, references
  limited to 20 characters. We can't change any of that." (brief §3.4);
  ISBN service: "Half the time the author's name is formatted strangely
  ... We have no influence on that service whatsoever." (brief §3.1).
- **Membership as a context** — passes the canvas test on its own
  decisions (register, grant researcher status on a checked letter,
  renew, expire), its own decider (Membership Officer, brief §3.3), its
  own words (member, library card, researcher status, renewal) and its own
  pace (yearly / twelve months). See F1 for the block, which is the weak
  part of it.
- **No notifications context, reader account as a view** — passes the
  "cut by technology" test: "We cannot name a vocabulary of its own for
  them" and "That is a *view* across contexts, not a context." (chapter 3).
- **Lending keeps its own copy of member status** — scenario S1 runs with
  zero synchronous round trips; the parked lending rules (C-11, C-12,
  C-14) each touch only lending (change scenarios).
- **Fees takes the due date from lending** — the likely 28-day change
  (C-13: "If it comes, fines would start after 28 days for those,
  obviously", brief §3.4) does not touch fees at all.
- **One core** — "If we marked all four as core, the classification would
  tell us nothing." (chapter 3). Plausible from brief §2.
- **Rejected words are recorded with reasons** in every glossary (`avoid`
  entries citing C-07), so the language decisions are traceable.

## Findings

### F1 The block rule has two owners: membership "decides", fees holds the threshold and the decision
- Severity: blocking
- Lens: ownership
- Evidence:
  - `requirements/brief.md` §3.3 (Daniel Weber, Membership Services): "We block a card when someone owes more than €10 in fines."
  - `chapters/03-strategic-design.md`: "Whether a card is blocked is a decision of the membership office. Lending only uses what membership publishes."
  - `chapters/03-strategic-design.md`: "Both policies, block and unblock, are drawn in the `fees` area. The amounts are known there"
  - `model/sketch/big-picture-contexts.json`, area `fees`: policy "When a member owes more than €10, block the card" --then block--> "Card Blocked (owes more than €10)" (area `membership`)
  - `model/esdm/integration/fees-membership-customer-supplier.esdm.yaml`: "Fees tells it when the amount owed (fines, lost-book fees and usage fees, C-18) passes 10 euro or is back at 10 euro or less; membership decides what blocking means."
  - `model/esdm/membership/bounded-context.esdm.yaml`, *blocked card*: "because the member owes more than 10 euro in total: fines, lost-book fees and usage fees (C-01, C-18)."
  - `model/esdm/fees/bounded-context.esdm.yaml`, *amount owed*: "Above 10 euro it blocks the card (C-18)."
- Why it matters: the reason (amount owed) and the threshold (€10) sit in
  fees, the event and the stated decision in membership, and "what
  blocking means" ("no new loans, no new reservations") is enforced in
  lending. Membership is left to turn "passed 10 euro" into "Card
  Blocked" one-to-one, a pass-through for this rule. Changing the €10 (or
  what counts, as C-18 just did) touches the fees policy, the fees
  glossary, the membership glossary and the mapping text: two contexts for
  one number. The customer–supplier label also reads backwards: the
  customer (membership) has nothing to negotiate when the supplier already
  decides. Nobody in the sources says who may change the €10; C-01
  decided *automatic*, not *whose*.
- Alternatives:
  - (a) Fees owns the rule end to end and publishes a fact in its own
    words ("reader in arrears" / "back in good standing"); membership only
    shows it, and lending consumes it. Costs: the brief's "we block" moves
    from the membership office to finance (business decision); membership
    glossary loses the €10 wording; the arrow becomes fees → lending
    (see F2 for the cycle consequence).
  - (b) Membership owns the threshold and decides; fees publishes only the
    amount owed per reader whenever it changes. Costs: membership must
    understand *amount owed* (a fees quantity, a leak by §2) and receives
    every balance change; but the owner matches the brief's speaker, and
    customer–supplier becomes real.
  - (c) Keep as is, but state the owner explicitly in the glossaries and
    the mapping. Costs: the split stays; every threshold change still
    touches two contexts.
- Level and next step: business (draft **C-19**: "Who decides the €10
  limit and what counts towards it, and who may change it: membership
  office, treasury, or the director?"), then architecture (draft ADR on
  where the block policy lives).

### F2 The context map has a dependency cycle (and the board adds a second one)
- Severity: blocking
- Lens: dependencies
- Evidence:
  - `chapters/03-strategic-design.md`: "**The contexts form a circle, through events only.** lending → fees → membership → lending." and "this is workable. It is a deliberate decision, and it must hold when we choose the technology: no module may depend on another at build time in a circle."
  - `model/esdm/integration/fees-membership-customer-supplier.esdm.yaml`: "Note: the chain lending, fees, membership, lending runs in a circle through events only."
  - Mappings: `lending-fees-open-host-service` (host lending, consumer fees), `fees-membership-customer-supplier` (supplier fees, customer membership), `membership-lending-customer-supplier` (supplier membership, customer lending).
  - `model/sketch/big-picture-contexts.json`: actor "Clock (daily, per branch)" sits in area `lending`, with "Clock (daily, per branch)" --triggers--> "Card Expired" and --triggers--> "Researcher Status Expired" (both area `membership`), and --checks every morning--> "When a member owes more than €10, block the card" (area `fees`).
  - `requirements/brief.md` §3.6: "If parts need to go their own way later, fine"
- Why it matters: by heuristics §4 "only events" does not remove the
  dependency: lending reads membership's status events, membership reads
  fees' threshold events, fees reads lending's loan events. None of the
  three can be built, tested or separated without the other two, which
  is exactly what the chapter's own condition ("no module may depend on
  another at build time in a circle") forbids, so the map already breaks
  the rule it sets for chapter 4. It also blocks the brief's "go their own
  way later". On the board the Clock in lending causes membership's
  expiry events, which adds lending → membership next to membership →
  lending: a two-context cycle.
- Alternatives (A → B = A depends on B):
  - (a) Turn fees → membership: membership publishes an inbound contract
    ("block / unblock for arrears") and fees conforms to it. Graph:
    lending → membership, fees → membership, fees → lending: acyclic.
    Costs: fees must speak membership's language (conformist), and fits
    F1 (a) only if fees is the decider.
  - (b) Turn lending → fees: lending calls fees through fees' API on
    checkout, return and loss. Acyclic as well. Costs: lending knows fees
    exists, which the chapter rejected ("without lending knowing that
    fees exist").
  - (c) Move the eligibility decision into lending (it consumes amount
    owed from fees and validity from membership). Costs: lending learns
    the €10 rule; still a lending ↔ fees cycle unless (b). Rejected in the
    chapter ("Blocking inside lending"); only worth reopening if F1 lands
    there.
  - For the Clock: one time trigger per context, or a Clock actor outside
    any area. Costs: nearly none on the board.
- Level and next step: architecture (draft ADR "Break the
  lending → fees → membership → lending cycle"), after C-19, because the
  arrow should follow the owner of the block (§4), not the cheapest turn.

### F3 Block and unblock use different amounts, and fees' own policies use membership's word
- Severity: should fix
- Lens: language
- Evidence:
  - `model/sketch/big-picture-contexts.json`, area `fees`: policy "When a member's fines are back at €10 or less, unblock the card", rule "Triggered by a payment or a waiver. Replaces the membership office unblocking by hand."
  - same area: policy "When a member owes more than €10, block the card", rule "Amount owed = assessed fines + running fines of loans still out ... + lost-book fees + usage fees, minus what is paid or waived."
  - `requirements/clarifications.md` C-18: "The Big Picture policy and the glossaries of `membership` and `fees` use `amount owed`."
  - `model/esdm/fees/bounded-context.esdm.yaml`, *reader*: avoid "member", "The membership office's word for the same person (C-07)."
  - fees events "Fine Paid", "Fine Waived" vs *payment*: "Money received for fines and fees"; *usage fee*: "A fee some special-collection items carry" (C-07 drops *item*); *assessed fine*: "The late fine fixed when the book comes back" (C-07: *book* only in everyday speech).
- Why it matters: read literally, a reader with an unpaid lost-book fee
  of €25 and no fines would be unblocked by the unblock policy and
  re-blocked by the block policy; C-18 says the policies use *amount
  owed*, but only one does. Inside fees the person is a *member* on both
  policy cards, although fees' glossary forbids the word, and paying a
  lost-book fee produces an event called "Fine Paid".
- Alternatives: reword the unblock policy to "amount owed back at €10 or
  less" and both policies to "reader" — costs one board edit; rename
  "Fine Paid" / "Fine Waived" to "Payment Confirmed" / "Charge Waived" (or
  define *fine* as the umbrella word) — costs a glossary decision.
- Level and next step: review.

### F4 Nobody owns which copies carry a usage fee, and lending has to publish it anyway
- Severity: should fix
- Lens: ownership
- Evidence:
  - `requirements/brief.md` §3.4: "Some items in the special collection carry a usage fee — the archive insists on it. That's charged when the item is checked out, not when it's returned."
  - `model/esdm/catalogue/bounded-context.esdm.yaml`: terms title, copy, circulating, restricted, replacement price; no usage fee.
  - `model/esdm/integration/catalogue-fees-published-language.esdm.yaml`: "fees reads only the price."
  - `model/esdm/integration/lending-fees-open-host-service.esdm.yaml`: "Fees follows loans without lending knowing about fees: due date, returned, declared lost, checkout of an item with a usage fee (C-03, C-04, C-08)."
  - `model/sketch/big-picture-contexts.json`, area `fees`: "When an item with a usage fee is checked out, charge the fee".
- Why it matters: the fact "this copy carries a usage fee, of this amount"
  has no home. Lending is supposed to publish "checkout of an item with a
  usage fee", which needs that fact and contradicts "without lending
  knowing about fees". Change scenario: the archive lends a new item with
  a fee: catalogue (register it), lending (event content), fees (amount)
  = three contexts for one likely change.
- Alternatives: (a) catalogue owns *usage fee* as a property of a copy,
  set at registration next to the restricted flag, and publishes it on the
  existing catalogue → fees language; lending publishes a plain checkout
  — costs a wider catalogue → fees contract and fees reacting to every
  checkout; no new arrow. (b) fees keeps its own list of fee-bearing
  copies — costs a second registration step by finance for collection
  data.
- Level and next step: business (draft **C-20**: "Who decides which copies
  carry a usage fee and how much: the Head of Collection with the archive,
  or finance?").

### F5 A lost or withdrawn copy never reaches the catalogue
- Severity: should fix
- Lens: scenario
- Evidence:
  - `requirements/clarifications.md` C-04: "a lost book ends a loan, takes a copy out of the collection and creates a fee: three areas meet here."
  - C-06: "the collection decides to repair or withdraw it." C-17 option 1: "Repair and withdrawal happen outside the system and the copy is released by hand."
  - `requirements/brief.md` §3.1: "we own eleven copies of it across the branches."
  - `chapters/03-strategic-design.md`: "Handling them inside the system would make the relationship between lending and catalogue two-way, which we deliberately avoid for now."
  - `model/esdm/integration/`: no mapping from lending to catalogue.
- Why it matters: in scenario S3 (lost book) the loan ends in lending and
  the fee lands in fees, but "takes a copy out of the collection" has no
  owner and no path; the catalogue keeps counting the copy. The same holds
  for a withdrawn damaged copy. "Released by hand" (C-17) does not say in
  which context or by whom.
- Alternatives: (a) Head of Collection records "copy withdrawn" in the
  catalogue, working from lending's loss/damage list; lending reacts —
  keeps the arrow catalogue → lending, costs a manual step. (b) catalogue
  subscribes to "Book Declared Lost" — costs the two-way relationship the
  chapter avoided (a cycle). (c) define catalogue *copy* as "registered",
  not "owned", and let lending answer "how many do we own" — costs a
  glossary change and a cross-context view for the collection.
- Level and next step: business (draft **C-21**: "Must the catalogue show
  that a copy is lost or withdrawn, and who records it?").

### F6 The board keeps the manual block next to the automatic one, so one party can undo the other's block
- Severity: should fix
- Lens: ownership
- Evidence:
  - `chapters/03-strategic-design.md`: "the connections from the Membership Officer to *Card Blocked* and *Card Unblocked* still show how it is done today, by hand. The new policies show how it should be done. We keep both on purpose."
  - `model/sketch/big-picture-contexts.json`: "Membership Officer" --blocks--> "Card Blocked (owes more than €10)", --unblocks--> "Card Unblocked"; neither edge is marked as-is.
  - `requirements/clarifications.md` C-01: "Blocking for other reasons is not in the brief."
  - same board: "Fine Paid" --is keyed in by hand--> "CityPay", while C-02 decided "the new system passes it to CityPay through its interface".
- Why it matters (heuristics §3, "Can one party undo the effect of
  another's decision"): if the officer blocks by hand, the next payment or
  waiver triggers the automatic unblock and lifts it; if the officer
  unblocks by hand while the amount owed is above €10, the next morning
  check blocks again. The block does not carry its owner, and a reader of
  the board cannot tell which edges are to-be. The CityPay edge contradicts
  a decided clarification in the same way.
- Alternatives: (a) mark the manual edges as as-is (or remove them) so
  that only the policies act in the to-be — costs nothing on the board,
  but leaves no way for staff to make an exception (C-16 waiver is open).
  (b) keep a manual block as a second reason: the block carries its
  reason, and only the same owner lifts it — costs block reasons in
  membership's model and a business answer.
- Level and next step: business (draft **C-22**: "May staff block or
  unblock a card by hand in the new system, and for what reasons?").

### F7 Open host services are justified by the count of consumers, and the extra consumers are not contexts
- Severity: should fix
- Lens: pattern
- Evidence:
  - `model/esdm/integration/catalogue-lending-open-host-service.esdm.yaml`: "Two contexts need title and copy data ... One general service instead of two bespoke integrations."
  - `model/esdm/integration/lending-fees-open-host-service.esdm.yaml`: "Other consumers (reader account, reminders) need the same events."
  - `chapters/03-strategic-design.md`: reminders, "We cannot name a vocabulary of its own for them"; reader account, "That is a *view* across contexts, not a context."
  - `requirements/brief.md` §3.6: "One application to run, please, not a zoo of services."
- Why it matters: heuristics §6 say an open host service is worth it "for
  several consumers or a stable public contract, not for the count of
  consumers alone". Catalogue's argument is the count (two), fees reads
  one field ("fees reads only the price"), and lending → fees has one
  consuming context; the other two consumers were explicitly not cut as
  contexts. The label promises a general, versioned service that nobody
  plans to build for one small team.
- Alternatives: published language only (the agreed event format) —
  costs adding a host service later if a public contract appears; or keep
  open host service and name the stable contract it protects — costs
  writing that reason down.
- Level and next step: review (or a short draft ADR on mapping patterns
  if the maintainer wants the reason recorded).

### F8 After payment at the desk, the unblock reaches the desk only after CityPay and two hops
- Severity: note
- Lens: scenario
- Evidence:
  - `requirements/brief.md` §3.3: "When they pay, we unblock."
  - `requirements/clarifications.md` C-02: "a fine counts as paid when CityPay confirms."
  - `model/sketch/big-picture-contexts.json`: "Branch Librarian (lending desk)" --takes payment--> "Fine Paid" (area `fees`).
  - `model/esdm/integration/membership-lending-customer-supplier.esdm.yaml`: "lending keeps the part it needs and never calls back."
- Why it matters: scenario S2 (timing): the reader pays at the desk and
  wants to borrow on the spot. Path: desk → fees → CityPay → fees →
  membership → lending's copy of the status. CityPay's confirmation time is
  unknown; until all hops land the desk still says "blocked". No failure
  yet, but the desk moment is where staff will notice.
- Alternatives: none needed now; when modelling lending, decide whether
  the desk may see a "payment pending" state.
- Level and next step: business (draft **C-23**: "Must a reader who has
  just paid be able to borrow in the same visit?").

### F9 Brief words with no glossary home
- Severity: note
- Lens: language
- Evidence:
  - board, area `lending`: "Book Kept for Researcher (no time limit)"; `lending` *reservation*: "until it is collected or runs out" (a researcher hold does not run out).
  - board, area `lending`: "Book Found Damaged"; no *damaged* term in `lending` or `catalogue`.
  - `requirements/brief.md` §3.4: "a shorter loan period for new releases"; no context owns *new release* (C-13 change would touch catalogue and lending).
  - `requirements/brief.md` §3.1, §3.4: "special collection"; used in `fees` *usage fee*, defined nowhere.
- Why it matters: words in the brief that no glossary owns are gaps
  (heuristics §2); *hold* vs *reservation* may be one word with two
  meanings inside lending.
- Alternatives: add the terms when each context is modelled — costs
  nothing now.
- Level and next step: review.

## Questions for the maintainer

1. (C-19) Who decides the €10 limit and what counts towards it, and who may change it: the membership office, the treasury, or the director?
2. (C-20) Who decides which copies carry a usage fee and how much: the Head of Collection together with the archive, or finance?
3. (C-21) Must the catalogue show that a copy is lost or withdrawn, and who records it?
4. (C-22) May staff block or unblock a card by hand in the new system, and if so for what reasons, and may an automatic unblock lift a manual block?
5. (C-23) Must a reader who has just paid at the desk be able to borrow in the same visit?
6. (architecture, after 1) Which arrow should be turned to break the lending → fees → membership → lending cycle (F2), and should the Clock leave the lending area?

---

## Appendix: working notes

### Canvases (heuristics §1)

| Context | Purpose | Class. | Decisions it makes | Receives | Sends | Own words |
|---|---|---|---|---|---|---|
| catalogue | Keep titles and registered copies | supporting | copy circulating or restricted; title before copy | ISBN data (ACL) | title added, copy registered (+flag), price | title, copy, circulating, restricted, replacement price |
| lending | Reserve, lend, take back copies at the branches | core | reservation allowed (5 limit, per-branch overdue limit, restricted, on shelf); due date; overdue; expiry; lost recorded | catalogue copies, member status | loan events, reservation events | reader, copy (state), loan, due date, overdue, reservation, researcher, branch, morning list |
| membership | Register people, cards and researcher status | supporting | register, grant researcher status, renew, expire; block: see F1 | "passed / back under 10 euro" from fees | member status changes | member, library card, researcher status, blocked card, expired card, renewal |
| fees | Charge, collect and report money owed | supporting | late fine, lost-book fee, usage fee, amount owed, €10 crossing (F1); waiver owner open (C-16) | loan events, price, CityPay confirmations (ACL) | threshold crossings, monthly report | reader, late/running/assessed fine, lost-book fee, usage fee, payment, waiver, amount owed |

Empty on purpose: assumptions and open questions per context beyond the
parked C-11 to C-16; no decision field is empty.

### Scenarios (heuristics §5)

- **S1 Reserve, borrow, return on time** (story `reserve-borrow-return`): lending decides locally from its copies of catalogue and membership data; lending → fees on checkout (usage fee policy) and return. 2 async crossings, 0 round trips. Holds.
- **S2 Overdue to day 21, pay, borrow again** (timing; story `overdue-book-fine-and-blocked-card`): Clock → fees running amount €10.50 → membership Card Blocked → lending. Return → Late Fine Assessed → pay at desk → CityPay → fees → membership → lending. 7 crossings, 0 synchronous round trips; see F2, F8.
- **S3 Book declared lost** (exception, C-04): lending → fees (price + €5, running fine stops), catalogue price via catalogue → fees, fees → membership (block stays) → lending. Copy leaving the collection has no path (F5).
- **S4 Researcher status expires with a restricted copy out** (C-05): membership → lending; loan stays. 1 crossing. Holds.

Change scenarios: €10 threshold or what counts — 2 contexts (F1); 28-day
new releases — lending + catalogue for the marker, fees untouched (F9);
new usage-fee item — 3 contexts (F4); online payment (C-02 option 3) —
fees only; reservation days / overdue limit per branch — lending only.
