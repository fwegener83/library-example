# Chapter 6 — Choosing the first increment

**Input:** the [brief](../requirements/brief.md), the [domain stories](../model/domain-stories/) and the [Big Picture board](../model/sketch/big-picture-contexts.json), the cut and map of [chapter 3](03-strategic-design.md), the records [ADR 2 to 11](../docs/adr/README.md), the [clarification log](../requirements/clarifications.md), the [report before this gate](../docs/reviews/pre-g6-context-cut.md)
**Tool:** the skill [`plan-scope`](../.claude/skills/plan-scope/SKILL.md); no board is changed in this chapter
**Result:** fifteen candidate scenarios with the contexts and boundaries each one touches, three options for the first increment, a recommendation, and the questions the scope decides. **The decision is open: this is gate G6.** Nothing in this chapter is modelled in detail or built.

## Why a scope at all

The cut into four contexts was made for the whole picture the brief paints, because a cut made for the first release only would not survive the second. The detailed modelling is different. It models every command, event, rule and example of a context, and that costs a chapter per context. It also tests the cut: if a boundary does not hold when the inside is modelled, we go back to the cut ([G1](../docs/gates/g1-model-to-code.md), phase 5).

So there are two reasons to choose well. The scope is what we deliver. And it decides which boundaries are tested while a wrong cut is still cheap.

The choice of what the library needs first is a business decision, so it is the maintainer's, as the library. The skill prepares it.

## How the candidates were found

Each candidate is a business capability that a person in the brief relies on or asks for. The sources are the list of what people rely on (brief §4), the two stories of chapter 2, and the events on the Big Picture board. A candidate is split where its parts have different owners or open rules (for example the fine at return, the daily running amount and the payment at the desk).

For each candidate the table names the contexts it touches and the boundaries it crosses. The contracts are those of the context map and the records: a fact travels as an event, an order goes through the owner's public API (ADR 4, ADR 5), a question comes from a front end over REST (ADR 8, ADR 10). Size is **S**, **M** or **L**: S stays inside one context or crosses one boundary with no open rule; M crosses two or touches several parked rules; L crosses three or more boundaries, or depends on something we know too little about.

## The candidates

| # | Scenario | Source | Contexts | Boundaries crossed | Pulls in | Size |
|---|---|---|---|---|---|---|
| A | Register titles and copies (circulating or restricted, home branch); correct them | brief §3.1; Big Picture *Title Added*, *Copy Registered*; C-24, C-27, C-29 | catalogue | catalogue → lending (copy registered, corrected), ISBN service (ACL) | the ISBN lookup can be left to hand entry at first | S |
| B | Register a member and a card; grant researcher status; renew | brief §3.3; Big Picture *Member Registered*, *Researcher Status Granted*, *Card Renewed*; C-28, C-31 | membership | membership → lending (status with end dates) | contact details (C-31) | S |
| C | Check out and return a copy in time | brief §3.2; story `reserve-borrow-return`, sentences 3 to 6; *Book Checked Out*, *Book Returned* | lending (needs A, B) | catalogue → lending, membership → lending | 60-day loan (§3.2); restricted copies for researchers only (C-29); the overdue limit per branch (C-14) | M |
| D | Reserve a copy that is on the shelf, collect it, let it run out | brief §3.2; story sentences 1 to 3; *Book Reserved*, *Reservation Expired* | lending (needs A, B) | as C | five reservations per reader (§3.2); days a reservation is kept (C-12); collecting after a block (C-11); the overdue limit (C-14) | M |
| E1 | A late return: the fine is assessed | brief §3.4; story `overdue-book-fine-and-blocked-card`, sentences 3 to 5; *Late Fine Assessed*; C-03 | lending, fees (needs C) | lending → fees (ADR 9), catalogue → fees (replacement price) | €0.50 a day, capped at the price; loan identity and business time (ADR 11) | M |
| E2 | The running fine is counted every morning and blocks the card above €10 | brief §3.3, §3.4; C-03, C-18, C-19; ADR 5 | fees, membership, lending (needs E1) | fees → membership (order: place hold), membership → lending (blocked) | late and repeated events (ADR 11); the morning run | L |
| E3 | The reader pays at the desk; the card is unblocked | story sentences 7 to 9; *Payment Received*; C-22, C-26 | fees, membership (needs E2) | fees → membership (order: lift hold) | "received" means the amount owed falls at once (C-22) | M |
| E4 | CityPay confirms or rejects a payment | brief §3.4; *Payment Confirmed*, *Payment Cancelled*; C-02, C-22 | fees, CityPay | CityPay → fees (ACL) | the CityPay interface is not known; a rejection raises the amount owed again | L |
| F | A usage-fee copy is checked out and charged | brief §3.4; *Usage Fee Charged*; C-08, C-21, C-27 | catalogue, lending, fees (needs C, E1) | catalogue → fees (the mark), lending → fees | one tariff; the mark must be known before the checkout arrives (ADR 11) | M |
| G | A copy is lost, and found again | brief §3.4; *Book Declared Lost*, *Lost-Book Fee Charged*; C-04, C-20, C-30 | lending, catalogue, fees (needs C, E1) | lending → fees, catalogue → lending (withdrawn) | refund of the replacement price (C-30, by hand until CityPay is known) | L |
| H | A damaged copy is listed, withdrawn or released | brief §3.2 ("goes to Tom"); *Book Found Damaged*, *Copy Released*; C-06, C-25 | lending, catalogue (needs C) | lending → catalogue (the list, by the page), catalogue → lending | the release names the damage report (ADR 11) | M |
| I | A researcher's keeps; the status ends | brief §3.2, §3.3; *Book Kept for Researcher*; C-05, C-28, C-32 | lending, membership (needs B, D) | membership → lending | end dates travel as dates (C-28) | M |
| J | The morning lists and the notices (reservation ready, due soon) | brief §3.2, §3.5, §3.6; *Reservation-Ready Notice Sent*; C-31 | lending, membership, catalogue, mail gateway | none of the mappings; a staff page composes (ADR 8); the mail gateway has no mapping yet | contact details, titles; how a notice reaches an address (open, C-31) | L |
| K | Search the catalogue; the reader's account online | brief §3.5 ("see their own account"), §4; ADR 8 | catalogue, lending, fees (as questions) | questions over REST, composed by the page | availability per branch (finding F11 of the report) | M |
| L | The monthly report; waiving a fine | brief §3.4; C-16, C-23, C-26 | fees | CityPay → fees | who may waive (C-16) and what "paid" means (C-26) are open | M |

What the brief puts out of the first release (§5) is not a candidate: e-books, inter-library loan, acquisitions, room bookings. A waiting line for books that are out (C-15) is a candidate that the brief does not ask for ("it would be nice"); it is left out of every option below and its question is answered in the last section.

Not every row is equal. A and B are prerequisites for everything else. C is the heart of lending. E1 to E3 are the only ones that cross the three boundaries that the records ADR 5, ADR 9 and ADR 11 are about.

## What needs what

```
A  B
 \ /
  C ── D ── I
  │
  E1 ── E2 ── E3 ── E4
  │
  F, G (they also need A) · H (needs C and A) · J, K, L (late)
```

The order is acyclic. A and B first, then C and D in `lending`, then E1 to E3 in `fees`, with `membership` receiving its orders. This is the build order that the [report before this gate](../docs/reviews/pre-g6-context-cut.md) found (`catalogue` and `membership`, then `lending`, then `fees`).

## Three options

### Option 1 — Lend and return

A, B, C, D. Three contexts, no fees.

* **Delivers:** a library that can register, lend, take back and reserve. Staff can use it at the desk, except for fines and blocking, which stay manual as today.
* **Tests of the cut:** the boundaries `catalogue` → `lending` and `membership` → `lending`. Not tested: `lending` → `fees`, the order `fees` → `membership` (ADR 5), the late *Returned* (ADR 11).
* **Costs:** two chapters of detailed modelling (`lending`, `catalogue` and `membership`). `fees` and the plan's chapter on it move to the second increment.
* **Leaves out:** everything with money, and with it the story of chapter 2, which has the card blocked because of a fine.

### Option 2 — Lend, return, fine and block (thin across all four contexts)

A, B, C, D, E1, E2, E3. All four contexts, `fees` only as far as the story of chapter 2.

* **Delivers:** the two stories of chapter 2 as software: the reader reserves, borrows, returns late, is fined, is blocked at more than €10, pays at the desk, and is unblocked. The payment is entered at the desk and counts as received (C-22); CityPay is not connected.
* **Tests of the cut:** all four contexts and the three hardest boundaries: the customer–supplier between `lending` and `fees` (ADR 9), the hold that `fees` places on a card of `membership` (ADR 5) and late or repeated events (ADR 11).
* **Costs:** three chapters of detailed modelling as in the plan (`lending`, `fees`, `catalogue` and `membership`), and `fees` modelled thin: the late fine, the running amount, the €10 rule, payment received. Decisions needed from the parked list: C-11, C-12, C-14 (lending).
* **Leaves out:** E4 and F to L: CityPay, usage fees, lost and damaged copies, keeps, the lists and notices, the search and the reader's account page, the report and waiving.

### Option 3 — Everything the brief names that is clear

Option 2 plus F, G, H, I, K.

* **Delivers:** nearly the whole desk, including lost and damaged copies and the usage fee.
* **Tests of the cut:** everything in option 2, and `catalogue` → `fees`, the withdrawal and release paths.
* **Costs:** a rough estimate is twice the modelling of option 2 (not measured), and G needs a refund path whose interface (CityPay) we do not know. The tutorial grows by several chapters before the first line of code.
* **Leaves out:** J (lists, notices), E4, L.

## Recommendation: option 2

* **It tests the cut where the cut is most likely to be wrong.** The report before this gate found no blocking problem. Its main findings are about events that cross a boundary: the loan events to `fees` (F1), the membership events to `lending` (F2), the copy events from `catalogue` (F3, F5). Option 1 tests the last two only in part, and the loan events and the orders from `fees` to `membership` (ADR 5) not at all. A cut that fails there would then be found after `lending` has been built on it. [G1](../docs/gates/g1-model-to-code.md) asks for the opposite: the model tests the cut before the code.
* **It is the story of chapter 2.** Both stories of the tutorial run end to end. A reader of the tutorial sees a rule that crosses three contexts from the brief to the code.
* **It is thin on purpose.** CityPay (E4), the usage fee (F) and the lost copy (G) are the three parts with the most unknowns. They stay out, and so do the lists and notices (J), which depend on an unanswered question about the mail gateway. The first increment contains no part whose interface we do not know.
* **It fits the plan.** The plan already had a chapter for `fees`. Option 1 would remove it from the first increment; option 3 would add several.

**The strongest argument against it:** option 1 is smaller and delivers a library that works at the desk sooner. Fines and blocking are done by hand today; the library could live with that for a while. If the maintainer, as the library, cares more about a working desk soon than about testing the cut early, option 1 is the better choice. Then the second increment must come with the test of `fees` before more is built on `lending`.

**What would change the recommendation:** a business reason that the first release needs the lists and notices (J) more than the fines. The brief calls the lists a function "people rely on" (§4) and says staff spend an hour a day on calls (§2). If so, J joins option 2 and the open question about the mail gateway has to be answered first.

## Questions that the scope decides

* **C-15, the waiting line for books that are out.** The question is parked "for the scope of the first release". The brief lists it as wished for, not as relied on (§3.2). **Proposal:** not in the first increment; it is a new feature, it would change the rules for reservations (D), and it would reach `lending` only. If the maintainer takes it in, it becomes part of D.
* **Parked rules that the recommended scope pulls in:** C-11 (collecting after a block), C-12 (days a reservation is kept) and C-14 (the overdue limit per branch) are rules of `lending` and are decided when `lending` is modelled; they do not wait for the scope. The recommended scope leaves out C-13 (28-day loans), C-16 (waiving) and C-26 (the monthly report).

## What we take with us

* The decision is the maintainer's. **Gate G6 is open.** The chapters on the flows and contracts and on the detailed modelling do not start before it is closed.
* The skill `plan-scope` exists and was used here for the first time. It is generic; the next increment uses it again.
* After the decision the accepted candidates become the list of scenarios that the chapters 7 to 10 cover. Each of those chapters says which of them it models.

## Decisions in this chapter

* **Way of working:** gate G6 is **open**. Options and a recommendation are prepared above; the choice of the first increment is the maintainer's and is not yet made. Nothing recorded in this chapter is a decision.
* **Business:** none yet. C-15 is proposed for the scope decision; the parked C-11 to C-14 stay parked.
* **Architecture:** none.

---

*No board was changed in this chapter and no Studio version was saved for it. Sources: [`model/domain-stories/`](../model/domain-stories/), [`model/sketch/big-picture-contexts.json`](../model/sketch/big-picture-contexts.json), [`model/esdm/`](../model/esdm/), [`docs/reviews/pre-g6-context-cut.md`](../docs/reviews/pre-g6-context-cut.md).*
