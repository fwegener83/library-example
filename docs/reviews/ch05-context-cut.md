# Context cut challenge: after chapter 5

Input: snapshot of the repository after chapter 5 (no commit given; Studio
versions per the exports: `ch5-big-picture-after-challenge`,
`ch5-context-map-after-challenge`). Files read: `requirements/brief.md`,
`requirements/clarifications.md`, `model/esdm/**` (4 contexts, 4 subdomains,
3 external systems, 10 mappings), `model/sketch/big-picture-contexts.json`,
`model/domain-stories/overdue-book-fine-and-blocked-card.yaml`,
`model/domain-stories/reserve-borrow-return.yaml`,
`chapters/03-strategic-design.md`, `chapters/04-deployment-decision.md`,
`chapters/05-challenging-the-cut.md`, `docs/adr/0001` to `0008` and the ADR
index.
Run by: fresh agent, 2026-10-23

Scope: the state after the decisions C-20 to C-24 and the changes of
chapter 5. The findings of the chapter 4 report are not repeated; where a
fix was checked, this report says whether it holds. The open question on the
pattern between `lending` and `fees` is known and is not raised again.

## Canvas (short)

| Context | Purpose (business words) | Class. | Decides on its own | Receives | Sends | Own words |
|---|---|---|---|---|---|---|
| `catalogue` | Keep the register of titles and of the copies the library owns | supporting | a copy needs its title first; circulating or restricted; usage-fee copy (C-21); home branch (C-24); withdrawal (C-20) | ISBN service (ACL); Head of Collection | title added, copy registered (with mark and home branch), copy withdrawn | title, copy, circulating, restricted, usage-fee copy, home branch, withdrawn copy, replacement price |
| `lending` | Let readers reserve, borrow and return copies at the four branches | core | reservation limits, restricted for researchers, per-branch overdue limit, expiry of reservations, overdue, lost and damaged at the desk | catalogue events, membership status | loan events (checked out, became overdue, returned, declared lost); list for the Head of Collection | reader, copy (state now), loan, due date, overdue, reservation, branch, lost copy, damaged copy, morning list |
| `membership` | Register members, keep cards and researcher status valid | supporting | card validity and renewal, researcher status, a card with a hold is blocked | Membership Officer; place/lift hold orders from fees | status changes (blocked, unblocked, expired, researcher) | member, library card, researcher status, hold, blocked card, expired card, renewal |
| `fees` | Charge what readers owe, take payments, report to the city | supporting | late fines (running, assessed), lost-book fee, usage fee, arrears and the €10 hold (C-19), payment received/confirmed (C-22) | catalogue and lending events, CityPay (ACL) | place/lift hold orders; payments to CityPay; monthly report | reader, late fine, running fine, assessed fine, lost-book fee, usage fee, usage-fee tariff, payment, waiver, amount owed, arrears, monthly report |

Every field is filled from the sources; no context is empty of decisions.

## What holds

- **No dependency circle.** From the mappings and the board's reactions:
  `catalogue` and `membership` depend on nothing; `lending` depends on
  `catalogue` (`catalogue-lending-*`) and `membership`
  (`membership-lending-customer-supplier`); `fees` depends on all three.
  The new lost-copy path (C-20) goes lending → list → *Head of Collection*
  → `catalogue` → `lending`. That is a loop in the business flow through a
  person and a page outside the modules (ADR 8: "The user interfaces may
  depend on every module; no module depends on a user interface"), not a
  loop in the dependencies. The claim in chapter 5, "The dependencies did
  not change", is correct.
- **The €10 rule still has one owner.** `membership` glossary: "Whoever
  placed a hold lifts it; nobody lifts another party's hold (C-19)". No
  money word in `membership`. C-22 changed *when* a payment counts, not who
  owns the rule; the policy stays in the `fees` area.
- **C-21 keeps money out of `catalogue`.** Catalogue glossary: "The amount
  is not known here; it is a tariff of fees (C-21)." `fees` uses the
  catalogue's word *usage-fee copy* as published language, which is the
  intended direction (downstream reads upstream's language).
- **C-24 keeps the two meanings of "where a copy is" apart.** Catalogue:
  "Where the copy is right now is not known here (C-24)"; lending: "A copy
  is on the shelf at one branch at a time; its home branch comes from the
  catalogue (C-24)."
- **Both anti-corruption layers translate something real** (cents,
  20-character references, odd status codes; oddly formatted titles), and
  the CityPay ACL now carries the two payment states of C-22.
- **Change scenarios stay narrow.** 28-day loans for new releases (C-13):
  `lending` sets the due date and `fees` already reads it from the loan
  event ("each with the copy, the reader and the due date"), so at most
  `catalogue` (if "new release" is a mark) and `lending`. Another threshold
  than €10: `fees` only. Readers paying online (C-02 option 3): `fees` and
  a page. A waiting line (C-15): `lending` only. None touches three
  contexts.

## Findings

### F1 The board does not apply C-18, C-22 and C-23: two charges and the rejected payment do not reach the arrears policy, and the usage fee does not reach the report
- Severity: should fix
- Lens: scenario
- Evidence:
  - `model/sketch/big-picture-contexts.json`, policy "When a reader is in arrears (amount owed above €10), place the hold 'unpaid fees' on the card", rule: "Amount owed = assessed fines + running fines of loans still out (days overdue × €0.50, capped at the book's price) + lost-book fees + usage fees, minus what is paid or waived. Checked every morning and whenever a charge is made." Its only incoming connections are from *Late Fine Assessed* ("whenever"), *Loan Became Overdue* ("whenever (running fine)") and *Clock (daily)* ("checks every morning"). *Usage Fee Charged* has no outgoing connection at all; *Lost-Book Fee Charged (price + €5)* only "feeds" the monthly report.
  - `requirements/clarifications.md`, C-22: "If CityPay rejects it, the payment is cancelled, the amount owed rises again, and the €10 rule places the hold again." The board has no event for a rejected or cancelled payment; the only trace is the note "a rejected payment is cancelled (C-02, C-22)". The `eventOrder` list ends with "Payment Received", "Payment Confirmed by CityPay", "Charge Waived".
  - `requirements/clarifications.md`, C-23: "The report covers every charge (late fines, lost-book fees, usage fees)". On the board the monthly report is fed by *Late Fine Assessed*, *Lost-Book Fee Charged*, *Payment Received*, *Payment Confirmed by CityPay* and *Charge Waived*, not by *Usage Fee Charged*.
  - `model/sketch/big-picture-contexts.json`, read model "Reader account: at home, waiting for me, what I owe" is fed only by *Book Reserved*, *Book Checked Out* and *Late Fine Assessed*; the brief §2 asks for "what they owe", which `fees` defines as the whole amount owed.
- Why it matters: played through, a reader who reports a copy lost at the desk is charged replacement price plus €5, usually above €10 on its own (C-18 says so), but on the board the hold is placed only by the next morning's check, so the reader can still borrow that day. A rejected CityPay payment has no event, so nobody models what re-places the hold. Code built from the board after G1 would inherit both gaps. This is the same kind of slip chapter 5 found ("ADR 5 changed the rule, and the context map and glossaries followed, but the board did not"), now for C-18, C-22 and C-23; the new check "a changed rule is looked for on the boards too" did not catch it.
- Alternatives: add the event *Payment Cancelled (rejected by CityPay)* in `fees` and connections from *Usage Fee Charged*, *Lost-Book Fee Charged* and the new event to the arrears policy, from *Usage Fee Charged* to the report and from the charges and payments to the reader account — costs a few cards; adding is possible, removing is a known tool gap. Or reword the policy trigger to "whenever the amount owed changes" and connect one generic card — costs precision on the board, but no rule is lost when a new charge appears.
- Level and next step: review. Consider making the check concrete: every event named in a clarification's consequence has a card, and every charge feeds the policies that count it.

### F2 After C-22, "paid" has two meanings inside `fees`, and "outstanding" is not the "amount owed"
- Severity: should fix
- Lens: language
- Evidence:
  - `model/esdm/fees/bounded-context.esdm.yaml`, *payment*: "Received when taken at the desk: it lowers the amount owed at once. Confirmed when CityPay confirms it". *amount owed*: "Everything charged to a reader and neither paid nor waived, plus running fines". Here "paid" has to mean *received*.
  - `requirements/clarifications.md`, C-22: "for the accounts a payment counts when CityPay confirms; for the block it counts when it is received."
  - `model/esdm/fees/bounded-context.esdm.yaml`, *monthly report*: "For every kind of charge (late fines, lost-book fees, usage fees): charged, paid, waived, outstanding (C-23)." The board feeds the report with both *Payment Received* and *Payment Confirmed by CityPay*, so the report's "paid" can be read either way.
  - *amount owed* includes running fines, which are "Not yet assessed" and, by C-03, cannot be paid ("a running amount cannot be paid, only a fixed one"). The report counts charges, so its "outstanding" either leaves running fines out (then it differs from the amount owed shown to the reader) or counts amounts that were never charged.
- Why it matters: one word with two meanings in one context (heuristics §2). The Treasury Liaison's report and the reader's "what I owe" will disagree whenever a desk payment is not yet confirmed or a book is still out, and nobody will be able to say which number is right. A rejected payment that was already in "paid" for a month would have to be taken back in a closed report.
- Alternatives: keep *received* and *confirmed* as the two words and never use bare "paid" in the glossary; define the report's "paid" as confirmed and its "outstanding" as charged minus confirmed minus waived, without running fines — costs a second figure for the reader page ("amount owed") next to the report's "outstanding". Or report "received", "confirmed" and "outstanding" separately — costs a report the brief does not name in those words.
- Level and next step: business, draft C-25 (below).

### F3 The catalogue mappings now say that lending takes *availability* from the catalogue, which chapter 3 rejected; chapter 3 still describes the old mappings
- Severity: should fix
- Lens: pattern
- Evidence:
  - `model/esdm/integration/catalogue-lending-open-host-service.esdm.yaml`: "Lending takes availability, restricted copies and the home branch; fees takes the price and the usage-fee mark."
  - `chapters/03-strategic-design.md`, Rejected: "We avoid it by letting lending own *availability*; the catalogue only knows what a copy is."
  - `model/esdm/lending/bounded-context.esdm.yaml`, *copy*: "A physical book and what may be done with it right now: on the shelf at a branch, reserved, on loan, lost or damaged."
  - `model/esdm/integration/catalogue-lending-published-language.esdm.yaml` lists what lending "listens to": "copy registered, with circulating or restricted, home branch and usage-fee mark", while C-21 says "`lending` no longer reports "checkout of a copy with a usage fee"" and nothing in the lending glossary uses the mark.
  - `chapters/03-strategic-design.md`, mapping table, still: "Fees follows loans (due date, returned, lost, usage fee)" and, for the catalogue, "Two consumers need the same thing … One general service is cheaper than two bespoke ones." Chapter 5 says the reason was corrected to "one stable format, not tailored to anyone"; the mapping file was, the chapter 3 table was not.
  - `model/esdm/integration/lending-fees-open-host-service.esdm.yaml` names "checked out, due date, returned, declared lost"; `lending-fees-published-language.esdm.yaml` names "checked out, became overdue, returned, declared lost". The board uses *Loan Became Overdue* for the running fine.
- Why it matters: "availability" in the catalogue's contract is exactly the word that, by chapter 3's own analysis, would turn catalogue–lending into a partnership. A reader of the map (or the code after G1) can take it literally. The stale chapter 3 table contradicts C-21. None of this changes the cut; it misleads.
- Alternatives: write "whether a copy may circulate at all (circulating, restricted, withdrawn)" instead of "availability"; say the mark is in the event for fees and lending ignores it; align the two lending → fees descriptions on one event list; add a line "changed in chapter 5" to the chapter 3 table — costs wording only.
- Level and next step: review.

### F4 The follow-up of a damaged copy now has two homes, and C-17 is revised without an entry
- Severity: should fix
- Lens: ownership
- Evidence:
  - `requirements/clarifications.md`, C-17 (decided): "Repair and withdrawal happen outside the system and the copy is released by hand." C-06: "the collection decides to repair or withdraw it."
  - `model/esdm/catalogue/bounded-context.esdm.yaml`, *withdrawn copy*: "A copy taken out of the collection by the Head of Collection, after it was lost or damaged beyond repair. Still recorded, no longer lendable (C-17, C-20)." Withdrawal of a damaged copy is now inside the system, citing C-17, which says the opposite.
  - `model/esdm/lending/bounded-context.esdm.yaml`, *damaged copy*: "Not lendable and listed for the Head of Collection; released by hand or withdrawn (C-06, C-17)."
  - `model/sketch/big-picture-contexts.json`: there is *Copy Withdrawn* with "Head of Collection | withdraws", but no event and no actor for releasing a repaired copy. *Book Found Damaged* only feeds "Copies for the Head of Collection: lost or damaged".
  - `chapters/03-strategic-design.md`: "Handling them inside the system would make the relationship between lending and catalogue two-way, which we deliberately avoid for now."
- Why it matters: one decision of one person (the Head of Collection: repair or withdraw, C-06) ends in two contexts. "Withdraw" is a catalogue event; "release" is a state change in lending with no named actor, so on the model anyone at the desk can make a damaged copy lendable again, and the Head of Collection's say over it (C-20's reason: "the Head of Collection keeps the say over the collection") holds for lost copies but not for damaged ones. The reason C-17 gave against option 2 (a two-way relationship) no longer applies: C-20 showed that the way back from lending to catalogue goes through a person and a page, and the catalogue → lending arrow already carries *Copy Withdrawn*.
- Alternatives: (a) keep release in `lending`, name it (*Damaged Copy Released*, actor Head of Collection) and amend C-17 to say withdrawal is in the catalogue — costs the Head of Collection acting in two contexts. (b) Take C-17 option 2 now: the catalogue publishes *Copy Back in Circulation* next to *Copy Withdrawn*, lending reacts to both; arrow stays catalogue → lending — costs one catalogue event and a catalogue word for "under repair". (c) Leave release outside the system as C-17 says and drop "released by hand" from lending — costs a manual workaround the model cannot show.
- Level and next step: business, draft C-26 (below).

### F5 The usage fee now depends on two event streams meeting in `fees`, and the mark cannot change after registration
- Severity: note
- Lens: dependencies
- Evidence:
  - `requirements/clarifications.md`, C-21: "`lending` no longer reports "checkout of a copy with a usage fee". It reports the checkout; `fees` knows from the catalogue whether that copy carries a fee."
  - `docs/adr/0004-contexts-talk-through-published-events.md`: "a module does not ask another module during its own work, it uses its own copy" and "Reactions to events must tolerate events that arrive twice or late."
  - `model/esdm/catalogue/bounded-context.esdm.yaml`, *usage-fee copy*: "Marked by the Head of Collection when the copy is registered". The catalogue publishes "title added; copy registered …; copy withdrawn" (`catalogue-lending-published-language`), no event for a changed mark.
  - `requirements/brief.md` §3.4: "Some items in the special collection carry a usage fee — the archive insists on it."
- Why it matters: before C-21 the checkout event carried the fact; now `fees` must already hold the catalogue's mark when the checkout arrives. A late or missing *Copy Registered* in `fees` gives a silent "no fee" rather than an error. And if the archive stops (or starts) insisting on a fee for a copy already registered, there is no way to say so; *Book Details Corrected* is about titles. No concrete failure in the sources yet, hence a note.
- Alternatives: a catalogue event *Usage-Fee Mark Changed* — costs one event, keeps C-21; `fees` treats a checkout of an unknown copy as an error to resolve, not as "no fee" — costs a rule in the modelling of `fees`.
- Level and next step: review; the question whether the mark can change goes with draft C-27 (below).

### F6 C-24 adds a second branch to the per-branch rules without saying which one counts
- Severity: note
- Lens: language
- Evidence:
  - `requirements/brief.md` §3.2: "If someone has more than two overdue books from *our* branch, we don't take any more reservations from them here."
  - `model/sketch/big-picture-contexts.json`, policy "More than 2 overdue books at a branch: no more reservations there", rule "Counted per branch, applies to researchers too."
  - `model/esdm/lending/bounded-context.esdm.yaml`, *branch*: "A copy is on the shelf at one branch at a time; its home branch comes from the catalogue (C-24)."
  - `requirements/clarifications.md`, C-24 parks only the return: "What happens when a copy is returned at another branch is not in the brief; it is decided with C-14". C-14: "Overdue limit per branch: intended or habit? And where does a copy returned at another branch go (C-24)?"
  - `requirements/brief.md` §3.1, the source C-24 relies on: "we own eleven copies of it across the branches"; and "What happens to a book after it leaves my desk is the branches' business, honestly."
- Why it matters: an overdue copy is on no shelf, so "from our branch" can now mean the branch where it was checked out or the copy's home branch, and the morning lists per branch have the same choice. Nothing on the board uses the home branch yet; the brief's evidence that it is the collection's decision is thin (the library owns copies "across the branches"; the Head of Collection disclaims what happens after his desk). If C-14 decides that copies stay where they are returned, the home branch has no consumer.
- Alternatives: add the question to C-14 ("which branch counts: checkout or home branch?") — costs nothing now; or define *loan branch* in lending now — costs a word that may turn out unused.
- Level and next step: business, extend parked C-14.

## Draft clarifications

- **C-25 (draft) What do "paid" and "outstanding" mean in the monthly report?** Source: brief §3.4 ("fines charged, paid, waived, outstanding"); C-22; C-03 (running amounts cannot be paid). Options: (1) paid = confirmed by CityPay, outstanding = charged minus confirmed minus waived, running fines not in the report; (2) report received and confirmed separately. Recommendation: (1), it follows C-22 ("for the accounts a payment counts when CityPay confirms").
- **C-26 (draft) Who releases a repaired copy, and in which context?** Source: C-06, C-17, C-20. Options (a) to (c) as in F4. Recommendation: (b), the same path as C-20, the Head of Collection keeps the say; amend C-17.
- **C-27 (draft) Can the usage-fee mark of a copy change after registration, and is there one tariff?** Source: brief §3.4 ("the archive insists on it"); C-21 ("The amount is not in the brief; it is a setting"). Options: mark fixed / changeable by the Head of Collection; one tariff / an amount per kind of copy.

## Questions for the maintainer

1. Damaged copies (F4, C-26): who may make a repaired copy lendable again, and is that recorded in the catalogue (like a withdrawal) or at the desk? C-17 says repair and withdrawal are outside the system; the glossaries now put withdrawal inside.
2. Monthly report (F2, C-25): does "paid" mean confirmed by CityPay, and does "outstanding" include running fines on books still out?
3. Usage fee (F5, C-27): can the archive's demand for a fee on a copy start or end after the copy is registered, and is it one amount for all such copies?
4. Per-branch overdue limit (F6, C-14): "more than two overdue books from our branch": the branch where the book was checked out, or the copy's home branch?
