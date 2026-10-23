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
- **Status:** proposed

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
- **Status:** proposed

### C-03 When is a late fine assessed?

- **Source:** brief §3.4 (€0.50 per day per book from the day after the
  due date, capped at the replacement price); hotspot "When exactly is a
  late fine assessed: on return or every day?".
- **Why now:** decides whether fees has to follow every overdue loan day
  by day, and whether a reader with a book still out can be blocked
  (C-01).
- **Options:**
  1. Once, when the book comes back (or is declared lost). While it is
     out, the reader's account shows the amount so far, for information.
  2. Daily: the fine grows every day and counts towards the €10 block
     at once.
- **Recommendation:** option 1. It gives one clear amount that can be
  paid or waived. The overdue limit per branch already deals with books
  that are still out. Trade-off: someone who never returns a book is
  never blocked by fines; C-04 covers that case.
- **Status:** proposed

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
- **Status:** proposed

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
- **Status:** proposed

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
- **Status:** proposed

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
- **Status:** proposed

---

## B. Answered by the brief (confirm only)

| ID | Question | What the brief says | Status |
|---|---|---|---|
| C-08 | What causes *Usage Fee Charged*? | Charged at checkout (§3.4): the checkout causes it. | proposed |
| C-09 | What causes *Card Expired* and *Researcher Status Expired*? | Time: one year / twelve months (§3.3). Actor *Clock*. | proposed |
| C-10 | Is *Reservation Cancelled* real? | Not in the brief (`src:inferred`). Proposal: keep it, the reader or staff cancel a reservation. Otherwise drop the event. | proposed |

---

## C. Parked (decided later, when the model needs it)

| ID | Question | Source | Decide when |
|---|---|---|---|
| C-11 | Blocked card: collect a reservation made before the block? | brief §3.3, §6 | Modelling lending (rule, not a boundary) |
| C-12 | Reservation kept 3 or 5 days? | brief §3.2, §6 | Modelling lending (a setting) |
| C-13 | 28-day loans for new releases? | brief §3.4, §6 | Modelling lending (a setting) |
| C-14 | Overdue limit per branch: intended or habit? | brief §3.2, §3.5 | Modelling lending (rule) |
| C-15 | Waiting line for books that are out? | brief §3.2 | Scope of the first release, before specs |
| C-16 | Who may waive a fine, and why? | brief §3.4 ("waived" in the report only) | Modelling fees |
