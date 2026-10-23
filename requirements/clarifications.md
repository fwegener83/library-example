# Clarifications

The brief (`brief.md`) stays as it was written. Whenever it is silent,
vague or contradicts itself and the answer matters for the model, the
question is logged here: where it came from, why it matters now, the
options, a recommendation, and the decision with who made it.

**How decisions are made in this tutorial.** In a real project these
questions go to the people in the brief (Helen Marsh, Daniel Weber, Grace
Lindqvist, …). Here, the tutorial's maintainer plays the library's side
and answers "on request". Every decision below is therefore marked as a
clarification, not as something the brief said. Anything that builds on
it cites the entry (`C-01`, …).

Status values: `proposed` (options and recommendation ready, no
decision yet), `decided`, `parked` (deliberately left for later, with the
moment it has to be decided).

---

## A. Questions that affect the domain cut (chapter 3)

### C-01 Who blocks and unblocks a card?

- **Source:** brief §3.3 ("We block a card when someone owes more than
  €10 in fines … When they pay, we unblock."); Big Picture events *Card
  Blocked*, *Card Unblocked*, policy "owes more than €10".
- **Why now:** decides whether membership has to know fine amounts, or
  only reacts to what fees reports.
- **Options:**
  1. Automatic: the card is blocked as soon as open fines exceed €10,
     and unblocked as soon as they are €10 or less again.
  2. The system flags it, the membership office decides.
  3. Manual, as today.
- **Sub-question:** unblock when *everything* is paid, or when the
  balance is back at €10 or less?
- **Recommendation:** option 1, unblock at €10 or less. The rule is
  mechanical, and the director wants fewer manual steps. Blocking for
  other reasons is not in the brief.
- **Status:** decided 2026-10-23 by the maintainer (acting for the library): recommendation accepted.

### C-02 How does a payment get to CityPay?

- **Source:** brief §3.4 (all payments through CityPay, its interface
  cannot be changed), §4 (paid at the desk, keyed into CityPay's portal
  by hand afterwards); chapter 2, finding "A payment is keyed in by hand".
- **Why now:** decides the boundary to CityPay and which side holds the
  truth about money.
- **Options:**
  1. The desk takes the payment, the new system passes it to CityPay
     through its interface; a fine counts as paid when CityPay confirms.
  2. Keep keying it in by hand; the new system only records the payment.
  3. Readers pay online through CityPay as well.
- **Recommendation:** option 1. Option 2 keeps two places to keep in
  step, which is the problem we found in chapter 2. Option 3 is not
  asked for (the director wants readers to *see* what they owe) and can
  come later on top of option 1.
- **Status:** decided 2026-10-23 by the maintainer (acting for the library): recommendation accepted.

### C-03 When is a late fine assessed, and does it count towards the block?

- **Source:** brief §3.4 (€0.50 per day per book from the day after the
  due date, capped at the replacement price), §3.3 (block above €10),
  §2 ("Fines … exist so that books come back"); hotspot "When exactly is
  a late fine assessed: on return or every day?".
- **Why now:** decides whether fees has to follow loans that are still
  out, and how the block (C-01) learns about them.
- **First proposal (rejected):** assess once, on return or loss, and
  count only assessed fines towards the block. Rejected by the
  maintainer: a reader who never brings a book back would never be
  blocked, which defeats the purpose of fines.
- **Options:**
  1. The fine is fixed once, on return or loss. While the book is out,
     the amount so far (days overdue × €0.50, capped at the price) is
     *running* and counts towards the €10 block. A daily check (the
     morning run) adds the running amounts to the fixed ones and blocks
     the card when the total is above €10.
  2. A fine is booked every day for every overdue book.
  3. Fines only on return, plus a separate block after a number of days
     overdue.
- **Recommendation:** option 1. It closes the gap and keeps one clear
  amount per book. Option 2 creates a booking per book per day for
  nothing. Option 3 needs a number the brief does not give and a second
  rule next to the €10 rule.
- **Consequences:** fees has to know the due date of every loan and
  learn when it ends (returned or lost); a running amount cannot be
  paid, only a fixed one. A blocked reader with a book still out gets
  unblocked only by returning it or reporting it lost and then paying.
  Below €10 nothing happens: one book triggers the block from day 21
  overdue (21 × €0.50 = €10.50).
- **Status:** decided 2026-10-23 by the maintainer (acting for the library): option 1, second round.

### C-04 Who declares a book lost, and what does it cost?

- **Source:** brief §3.4 (replacement price plus €5 handling fee);
  hotspot "Who declares a book lost, and when?".
- **Why now:** a lost book ends a loan, takes a copy out of the
  collection and creates a fee: three areas meet here.
- **Options:**
  1. The reader reports the loss, staff record it at the desk.
  2. Automatically after a number of days overdue.
  3. Both.
- **Sub-question:** is a late fine charged on top of the lost-book fee?
- **Recommendation:** option 1 for the first release. Option 2 needs a
  number the brief does not give. No late fine on top: the cap at the
  replacement price suggests the price is the most a book can cost in
  fines.
- **Status:** decided 2026-10-23 by the maintainer (acting for the library): recommendation accepted.

### C-05 What does an expired card or researcher status mean?

- **Source:** brief §3.3 (card valid for a year, researcher status for
  twelve months, expired members stay in the system); Big Picture events
  *Card Expired*, *Researcher Status Expired*.
- **Why now:** decides what lending has to know about a member: only
  "may borrow / may not", or more.
- **Options:**
  1. Expired card: like a blocked card (no new loans, no new
     reservations). Expired researcher status: the member is a normal
     reader again for new loans and reservations; what is already out
     stays out.
  2. Expired card: nothing changes until renewal is enforced at the desk.
- **Recommendation:** option 1. Both expiries are triggered by time
  (actor *Clock*), not by a person.
- **Status:** decided 2026-10-23 by the maintainer (acting for the library): recommendation accepted.

### C-06 What happens to a damaged book?

- **Source:** brief §3.2 ("Unless it's damaged, then it goes to Tom");
  hotspot "Damaged book 'goes to Tom' — what happens then?".
- **Why now:** it is a handover between lending and collection.
- **Options:**
  1. At check-in the copy is marked damaged and is not available; the
     collection decides to repair or withdraw it. The reader is not
     charged.
  2. As 1, and the reader is charged.
- **Recommendation:** option 1. The brief names no charge for damage.
- **Status:** decided 2026-10-23 by the maintainer (acting for the library): recommendation accepted.

### C-07 Which words do we use?

- **Source:** brief §3.1 ("items … instances — same thing"), §3.2
  ("readers … patrons … members. Whatever."); hotspots on "book" and on
  reader/patron/member.
- **Why now:** where the words change is a strong hint for a boundary.
- **Recommendation:**
  - **Title**: the catalogue entry (ISBN, title, author, price).
  - **Copy**: one physical book with its own barcode. *Item* and
    *instance* are not used.
  - **Book**: only in everyday speech, never in the model.
  - **Reader**: the person at the desk, in lending and fees.
  - **Member**: the same person as seen by the membership office.
  - *Patron* (LibTrack's word) is not used.
- **Status:** decided 2026-10-23 by the maintainer (acting for the library): recommendation accepted.

### C-17 Damaged copies: what is the library's own follow-up in the first release?

- **Source:** C-06 (decided: a damaged copy is marked and not lendable;
  "the collection decides to repair or withdraw it").
- **Why now:** the follow-up (repair, withdraw, back on the shelf) is a
  second crossing between lending and collection, in the opposite
  direction to registration. Modelled in full it turns the one-way
  relationship into a two-way one.
- **Options:**
  1. First release: lending marks the copy damaged and lists it for the
     Head of Collection. Repair and withdrawal happen outside the system
     and the copy is released by hand.
  2. First release: collection owns the copy's condition and lending
     reacts to it.
- **Recommendation:** option 1. The brief says nothing about repair or
  withdrawal. Option 2 is a later increment.
- **Status:** decided 2026-10-23 by the maintainer (acting for the library): recommendation accepted (option 1).

### C-18 Which amounts count towards the €10 block?

- **Source:** brief §3.3 ("when someone owes more than €10 in fines");
  C-01 and C-03 (decided: the total of assessed and running fines).
- **Why now:** the glossary of `fees` separates late fines, lost-book
  fees and usage fees. The brief says "fines" for the block and does not
  say whether the other two count.
- **Options:**
  1. Everything the reader owes (`amount owed`): late fines, lost-book
     fees and usage fees.
  2. Late fines only.
- **Recommendation:** option 1. A lost-book fee is the replacement price
  plus €5 and will usually be above €10 on its own; with option 2 a
  reader who lost a book would not be blocked, which is the gap C-03
  closed for late fines. The Big Picture policy and the glossaries of `membership` and `fees`
  use `amount owed`.
- **Status:** decided 2026-10-23 by the maintainer (acting for the library): recommendation accepted (option 1).

## A2. Questions that came up in chapter 4

### C-19 Whose rule is the €10 block?

- **Source:** brief §3.3 ("We block a card when someone owes more than
  €10 in fines … When they pay, we unblock."), §2 ("Fines … exist so
  that books come back"); C-01 (decided: automatic). The brief does not
  say who "we" is. Today the Membership Officer carries the block out by
  hand, which says who does the work, not whose rule it is.
- **Why now:** ADR 5. The rule links two contexts: the reason is money
  (`fees`), the effect is on the card (`membership`). Whoever owns the
  rule holds the policy, and the dependency between the two modules
  follows from that. Chapter 4 first argued from the dependency circle
  alone, which is the wrong order: the owner of the rule comes first,
  the technical structure follows.
- **Options:**
  1. **The rule belongs to the finance side.** `fees` decides when a
     reader is *in arrears* and places a hold "unpaid fees" on the card;
     it lifts the hold when the amount owed is €10 or less again.
     `membership` owns the card and its holds and knows nothing about
     money. A card with at least one hold is blocked; nobody lifts a
     hold placed by someone else.
  2. **The rule belongs to the membership office.** `fees` only reports
     the amount owed; `membership` holds the €10 threshold and decides.
     `membership` then has to understand amounts of money.
- **Recommendation:** option 1. The purpose of the rule is that books
  come back and fees are paid; that is the agenda of `fees`. The card
  stays the business of `membership`. The hold keeps the reasons apart:
  in the first release there is only one (C-01 found no other reason to
  block in the brief), but the rule "whoever placed a hold lifts it"
  means a second reason, say a manual one by the Membership Officer,
  cannot be undone by a payment.
- **Status:** decided 2026-10-23 by the maintainer (acting for the
  library): recommendation accepted (option 1).

## A3. Questions from challenging the cut (chapter 5)

Raised by the `challenge-context-cut` report on the state after chapter 4
(`docs/reviews/ch04-context-cut.md`). The maintainer accepted the
recommendations before reading the final wording; the entries say so.

### C-20 What happens to a lost copy in the collection?

- **Source:** C-04 ("a lost book ends a loan, takes a copy out of the
  collection and creates a fee: three areas meet here"); C-17 (damaged
  copies are released by hand); brief §3.1 ("we own eleven copies of it
  across the branches", "What happens to a book after it leaves my desk
  is the branches' business, honestly."). Report finding F1.
- **Why now:** the model ends the loan and charges the fee, but nothing
  takes the copy out of the collection. Letting `catalogue` react to a
  loss in `lending` would make the two depend on each other (ADR 3).
- **Options:**
  1. `lending` records the loss and lists the copy for the Head of
     Collection, as for damaged copies (C-17). The Head of Collection
     *withdraws* the copy in the catalogue; `catalogue` publishes that,
     and `lending` stops offering it.
  2. `lending` owns the end of a copy's circulation; the catalogue stays
     a register of what was acquired.
  3. `catalogue` reacts to the loss in `lending`.
- **Recommendation:** option 1. It is the same path as for damaged
  copies, the Head of Collection keeps the say over the collection, and
  the arrow stays catalogue → lending. Cost: one manual step per lost
  copy, and the catalogue counts the copy until it is withdrawn. Option 2
  leaves the catalogue counting copies the library no longer has.
  Option 3 creates a dependency circle.
- **Status:** decided 2026-10-23 by the maintainer (acting for the
  library): recommendation accepted (given in advance).

### C-21 Who decides which copies carry a usage fee, and how much?

- **Source:** brief §3.4 ("Some items in the special collection carry a
  usage fee — the archive insists on it. That's charged when the item is
  checked out"), §3.1 ("When we register a copy, we decide whether it
  circulates or not", "anything the archive lent us"); C-08. Report
  finding F2.
- **Why now:** `fees` charges the usage fee at checkout but no context
  owns the two facts it needs: *which* copies and *how much*. The brief
  says "items"; C-07 replaced the word by *copy*.
- **Options:**
  1. **Split by kind of fact.** The Head of Collection marks a copy as
     *usage-fee copy* when registering it, as with circulating and
     restricted; `catalogue` publishes the mark. The amount is a tariff in
     `fees`, set by the Treasury Liaison. Per copy, not per title.
  2. Everything in `catalogue`: the mark and the amount.
  3. Everything in `fees`: a list of copies with their amounts.
- **Recommendation:** option 1. Which copy belongs to the archive's
  special collection is known when it is registered, by the person who
  registers it. An amount of money is the business of `fees`; option 2
  would bring money into `catalogue`, option 3 would make `fees` keep a
  second list of copies in step with the catalogue. The mark is separate
  from *restricted*: the brief does not say that the two coincide. The
  amount is not in the brief; it is a setting.
- **Consequence:** `lending` no longer reports "checkout of a copy with
  a usage fee". It reports the checkout; `fees` knows from the catalogue
  whether that copy carries a fee.
- **Status:** decided 2026-10-23 by the maintainer (acting for the
  library): recommendation accepted (given in advance).

### C-22 When does a payment at the desk unblock the card?

- **Source:** brief §3.3 ("When they pay, we unblock."), §4 (payment
  taken at the desk); C-02 ("a fine counts as paid when CityPay
  confirms"); ADR 5. Report finding F5.
- **Why now:** with C-02 alone, a reader who has just paid at the desk
  stays blocked until CityPay confirms and the hold is lifted.
- **Options:**
  1. **Two steps.** A payment taken at the desk is *received* at once and
     lowers the amount owed; the hold is lifted if it is then €10 or
     less. CityPay's confirmation makes it *confirmed* for the accounts.
     If CityPay rejects it, the payment is cancelled, the amount owed
     rises again, and the €10 rule places the hold again.
  2. Only on confirmation (C-02 as it stands); the desk shows "payment
     pending".
- **Recommendation:** option 1. It is what the brief says ("When they
  pay, we unblock"), and the director wants fewer manual steps and
  fewer phone calls. A rejected transfer is rare and is handled by the
  rule that already exists. This **refines C-02**: for the accounts a
  payment counts when CityPay confirms; for the block it counts when it
  is received.
- **Status:** decided 2026-10-23 by the maintainer (acting for the
  library): recommendation accepted (given in advance).

### C-23 What does the monthly report cover?

- **Source:** brief §3.4 ("We need a monthly report: fines charged,
  paid, waived, outstanding."); C-18 (all charges count towards the
  block); C-16 (parked: who may waive). Report finding F3.
- **Why now:** the board feeds the report only with late fines, and the
  only payment event is called *Fine Paid*.
- **Options:**
  1. The report covers every charge (late fines, lost-book fees, usage
     fees), shown by kind: charged, paid, waived, outstanding.
  2. Late fines only, as the word "fines" reads.
- **Recommendation:** option 1, for the same reason as C-18: the brief
  says "fines" for everything a reader owes, and a report without
  lost-book fees would leave out most of the money. Every charge can be
  paid. Who may waive which charge stays parked in C-16.
- **Status:** decided 2026-10-23 by the maintainer (acting for the
  library): recommendation accepted (given in advance).

### C-24 Does a copy belong to a branch?

- **Source:** brief §3.1 ("we own eleven copies of it across the
  branches"), §3.2 ("You can only reserve a book that's on the shelf",
  "every branch keeps its own count"); C-14 (parked). Report finding F7.
- **Why now:** reservations and the overdue limit work per branch, but no
  context says where a copy belongs or who decides it.
- **Options:**
  1. Every copy has a **home branch**, set by the Head of Collection when
     registering it; `catalogue` publishes it. *Where the copy is now*
     (on the shelf at a branch, on loan) is the state of `lending`.
  2. Copies have no home; they stay wherever they were returned
     (`lending` only).
- **Recommendation:** option 1. The brief speaks of copies the library
  owns across its branches, which is a decision of the collection; the
  shelf a copy is on right now is the desk's business. What happens when
  a copy is returned at another branch is not in the brief; it is decided
  with C-14 when `lending` is modelled.
- **Status:** decided 2026-10-23 by the maintainer (acting for the
  library): recommendation accepted (given in advance); the return at
  another branch is parked with C-14.

---

## B. Answered by the brief (confirm only)

| ID | Question | What the brief says | Status |
|---|---|---|---|
| C-08 | What causes *Usage Fee Charged*? | Charged at checkout (§3.4): the checkout causes it. | decided 2026-10-23 (maintainer): as proposed |
| C-09 | What causes *Card Expired* and *Researcher Status Expired*? | Time: one year / twelve months (§3.3). Actor *Clock*. | decided 2026-10-23 (maintainer): as proposed |
| C-10 | Is *Reservation Cancelled* real? | Not in the brief (`src:inferred`). Proposal: keep it, the reader or staff cancel a reservation. Otherwise drop the event. | decided 2026-10-23 (maintainer): as proposed |

---

## C. Parked (decided later, when the model needs it)

| ID | Question | Source | Decide when |
|---|---|---|---|
| C-11 | Blocked card: collect a reservation made before the block? | brief §3.3, §6 | Modelling lending (rule, not a boundary) |
| C-12 | Reservation kept 3 or 5 days? | brief §3.2, §6 | Modelling lending (a setting) |
| C-13 | 28-day loans for new releases? | brief §3.4, §6 | Modelling lending (a setting) |
| C-14 | Overdue limit per branch: intended or habit? And where does a copy returned at another branch go (C-24)? | brief §3.2, §3.5 | Modelling lending (rule) |
| C-15 | Waiting line for books that are out? | brief §3.2 | Scope of the first release, before specs |
| C-16 | Who may waive a fine, and why? | brief §3.4 ("waived" in the report only) | Modelling fees |
