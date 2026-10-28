# Chapter 6 — Choosing the first increment

**Input:** the [brief](../requirements/brief.md), the [domain stories](../model/domain-stories/) and the [Big Picture board](../model/sketch/big-picture-contexts.json), the cut and map of [chapter 3](03-strategic-design.md), the records [ADR 2 to 11](../docs/adr/README.md), the [clarification log](../requirements/clarifications.md), the [report before this gate](../docs/reviews/pre-g6-context-cut.md)
**Tool:** the skill [`plan-scope`](../.claude/skills/plan-scope/SKILL.md); no board is changed in this chapter
**Result:** eighteen candidate scenarios with the contexts and boundaries each one touches and what each one needs, four options for the first increment, a recommendation, and the questions the scope decides. **Gate G6 was decided on 2026-10-26: option 3.** Nothing in this chapter is modelled in detail or built.

## Why a scope at all

The cut into four contexts was made for the whole picture the brief paints, because a cut made for the first release only would not survive the second. The detailed modelling is different. It models every command, event, rule and example of a context, and that costs a chapter per context. It also tests the cut: if a boundary does not hold when the inside is modelled, we go back to the cut ([G1](../docs/gates/g1-model-to-code.md), phase 5).

So there are two reasons to choose well. The scope is what we deliver. And it decides which boundaries are tested while a wrong cut is still cheap.

The choice of what the library needs first is a business decision, so it is the maintainer's, as the library. The skill prepares it.

## How the candidates were found

Each candidate is a business capability that a person in the brief relies on or asks for. The sources are the list of what people rely on (brief §4), the two stories of chapter 2, and the events on the Big Picture board. A candidate is split where its parts have different owners or open rules: the fine at return, the daily running amount and the payment at the desk are three; the morning lists and the notices are two.

For each candidate the table names the contexts it touches, the boundaries it crosses and what it needs. The contracts are those of the context map and the records: a fact travels as an event, an order goes through the owner's public API (ADR 4, ADR 5), a question comes from a front end through the module's public queries (ADR 8)[^adr10], and every event carries the envelope of ADR 11.

**Size.** **S**: one context, at most one boundary, no parked rule. **M**: two boundaries, or a parked rule, or a page that composes several modules. **L**: three or more boundaries, a boundary whose interface we do not know, or a path to or from an external payment system, or a refund. The sizes are a judgement, not a measurement.

## The candidates

| # | Scenario | Source | Contexts | Boundaries crossed | Pulls in | Needs | Size |
|---|---|---|---|---|---|---|---|
| A | Register titles (with the replacement price) and copies (circulating or restricted, home branch); correct them | brief §3.1; Big Picture *Title Added*, *Book Details Corrected*, *Copy Registered*; C-24, C-27, C-29 | catalogue | catalogue → lending (copy registered, corrected) | the usage-fee mark is recorded with the copy (C-21), but nothing charges it until F; the ISBN lookup (an anti-corruption layer) can wait, titles are keyed in | — | S |
| B | Register a member and a card; grant researcher status; renew; holds on a card (place, lift) and the blocked card | brief §3.3; *Member Registered*, *Researcher Status Granted*, *Card Renewed*, *Card Blocked*, *Card Unblocked*; story `overdue-book-fine-and-blocked-card`, sentences 6 and 9; ADR 5, C-28, C-31 | membership | membership → lending (status with end dates, blocked) | the only reason for a hold in the first release is "unpaid fees" (ADR 5), so the mechanism is built and the reason comes with E2; *Card Expired* and *Researcher Status Expired* only report an end that is a date (C-09, C-28) | — | S |
| C | Check out and return a copy in time; a damaged copy is marked and not available at check-in | brief §3.2 ("Unless it's damaged"); story `reserve-borrow-return`, sentences 3 to 6; *Book Checked Out*, *Book Returned*, *Book Found Damaged*; C-06 | lending | catalogue → lending, membership → lending | the loan of 60 days "at most" (§3.2); card validity and researcher status by date (C-28); restricted copies for researchers only (C-29); the envelope of ADR 11; returning at another branch (C-14, C-24) | A, B | M |
| D | Reserve a copy that is on the shelf, collect it, cancel it, let it run out | brief §3.2; story sentences 1 to 3; *Book Reserved*, *Reservation Cancelled*, *Reservation Expired*; C-10 | lending | as C | five reservations per reader (§3.2); days a reservation is kept (C-12); collecting after a block (C-11); the overdue limit per branch (C-14, brief §3.2: "more than two overdue books from our branch") | A, B | M |
| E1 | A late return: the fine is assessed | brief §3.4; story `overdue-book-fine-and-blocked-card`, sentences 3 to 5; *Late Fine Assessed*; C-03 | lending, fees | lending → fees (ADR 9; *Checked Out*, *Became Overdue*, *Returned*), catalogue → fees (replacement price) | €0.50 a day, capped at the price; loan identity and business time (ADR 11) | C | M |
| E2 | The running fine is counted every morning and blocks the card above €10 | brief §3.3, §3.4; C-03, C-18, C-19; ADR 5 | fees, membership, lending | lending → fees, fees → membership (order: place hold), membership → lending (blocked) | late and repeated events (ADR 11); the morning run; a reader who has lost a book and is blocked can only get out through G1 (C-03) | E1, B, G1 | L |
| E3 | The reader pays at the desk; the card is unblocked | story sentences 7 to 9; *Payment Received*; C-22 | fees, membership | fees → membership (order: lift hold) | "received" means the amount owed falls at once (C-22) | E2 | M |
| E4 | CityPay confirms or rejects a payment | brief §3.4; *Payment Confirmed by CityPay*, *Payment Cancelled*; C-02, C-22 | fees, CityPay | CityPay → fees (anti-corruption layer) | the CityPay interface is not known; a rejection raises the amount owed again | E3 | L |
| F | A usage-fee copy is checked out and charged | brief §3.4; *Usage Fee Charged*; C-08, C-21, C-27 | catalogue, lending, fees | catalogue → fees (the mark), lending → fees | one tariff; the mark must be known before the checkout arrives (ADR 11) | A, C, E1 | M |
| G1 | A copy is declared lost at the desk; the lost-book fee | brief §3.4; *Book Declared Lost*, *Lost-Book Fee Charged*; C-03, C-04, C-20 | lending, catalogue, fees | lending → fees, catalogue → lending (withdrawn) | no late fine on top of the lost-book fee (C-04); the Head of Collection withdraws the copy (C-20) | A, C, E1 | M |
| G2 | A lost copy comes back | brief §3.4 (no sentence about it); C-30 | lending, catalogue, fees | lending → fees, catalogue → lending | the replacement price is cancelled or refunded, by hand until CityPay is known (C-30) | G1, E3 | L |
| H | A damaged copy is withdrawn or released by the Head of Collection | brief §3.2 ("then it goes to Tom"); *Book Found Damaged*, *Copy Withdrawn*, *Copy Released*; C-06, C-25 | lending, catalogue | catalogue → lending | the release names the damage report (ADR 11) | A, C | M |
| I | A researcher's keeps; the status ends | brief §3.2, §3.3; *Book Kept for Researcher*; C-05, C-28, C-32 | lending, membership | membership → lending | end dates travel as dates (C-28); the member is told "through the normal notice" (C-32), which is J2 and can wait | B, D | M |
| J1 | The morning lists: reservations that ran out, loans that are overdue, with names, phone numbers and titles | brief §3.2, §4, §2 ("Staff spend an hour a day calling people"); *Loan Became Overdue*, *Reader Reminded by Phone*; C-31, finding F7 of the report | lending, membership, catalogue | questions from a front end, composed by a staff page (ADR 8); no event | contact details in membership (C-31, decided) | A, B, C, D | M |
| J2 | The notices by email: reservation ready, due soon, reservation expiring | brief §3.5, §3.6; *Reservation-Ready Notice Sent*, *Due Reminder Sent*, *Reservation-Expiring Reminder Sent* | lending, membership, mail gateway | the mail gateway has no mapping yet | how a notice from lending reaches an address kept in membership (open, C-31) | B, C, D | L |
| K | Search the catalogue; the reader's account online | brief §4, §2 ("see their own account online"), §3.5 ("see online what I have at home"); ADR 8 | catalogue, lending, fees | questions from a front end, composed by the page | availability per branch (finding F11 of the report) | A, B, C, D, E1 | M |
| L1 | The monthly report | brief §3.4; C-23, C-26 | fees | none | "paid" received or confirmed, "outstanding" with or without running fines (C-26); it reports every kind of charge that exists in the increment | E1 | M |
| L2 | Waive a fine | brief §3.4 ("waived" in the report); C-16 | fees | none | who may waive, and why (C-16, not answered) | E1 | M |

What the brief puts out of the first release (§5) is not a candidate: e-books, inter-library loan, acquisitions, room bookings. A waiting line for books that are out (C-15) is not a candidate either: the brief calls it "nice" (§3.2), not something people rely on (§4). Its question is at the end of this chapter.

The needs are acyclic: A and B have none, everything else needs candidates earlier in the table. The build order is that of the [report before this gate](../docs/reviews/pre-g6-context-cut.md): `catalogue` and `membership`, then `lending`, then `fees`. Only E2 and E3 use the hold of ADR 5; E1, E2, F and G1 cross the boundary of ADR 9; all of them depend on the envelope of ADR 11.

## Four options

An option is a set of candidates that contains everything its members need.

### Option 1 — Lend and return

A, B, C, D. Three contexts, no fees.

* **Delivers:** staff can register titles, copies and members, lend, take back and reserve. There is no blocking: the only reason for a hold in the first release is unpaid fees (ADR 5), which come with E2. A manual reason, as the Membership Officer carries it out today (story sentences 6 and 9), would be a second reason for a hold and a new business decision.
* **Tests of the cut:** the boundaries `catalogue` → `lending` and `membership` → `lending`, and in part the events from `catalogue` (F3 of the report). Not tested: `lending` → `fees`, the orders from `fees` to `membership` (ADR 5), a late *Returned* (ADR 11).
* **Costs:** `lending` and `catalogue` with `membership` are modelled, `fees` is not. The parked rules C-12 and C-14 are needed (D); C-11 (collecting after a block) does not arise because nothing blocks a card yet.
* **Leaves out:** everything with money. LibTrack calculates fines today (brief §4); with this option the new system does not, so a fine would be calculated elsewhere or by hand.
* **LibTrack:** cannot be retired. Fines, the lists, the search and the reader's account stay with it.

### Option 2 — Lend, return, fine and block

A, B, C, D, E1, E2, E3, G1. All four contexts, `fees` only as far as the story of chapter 2 and the way out for a lost book.

* **Delivers:** the story of chapter 2 from the late return (sentence 3) to the unblock (sentence 9): the reader returns late, is fined, is blocked above €10, pays at the desk, and is unblocked; a reader who has lost the book is charged the lost-book fee and can pay it (C-03, C-04); and the reservations of the other story.
* **Tests of the cut:** all four contexts and the three hardest boundaries: `lending` → `fees` (ADR 9), the hold that `fees` places on a card of `membership` (ADR 5), and late or repeated events (ADR 11).
* **Costs:** the three chapters of detailed modelling the plan has (`lending`, `fees`, `catalogue` with `membership`), with `fees` modelled thin: the late fine, the running amount, the €10 rule, payment received. The parked rules C-11 (a block exists from E2 on), C-12 and C-14.
* **A consequence you should know about:** CityPay is not connected (E4 is out). The desk takes the payment and the system records it as received (C-22), and somebody keys it into CityPay's portal by hand, as today. [C-02](../requirements/clarifications.md) decided the opposite for the finished system and rejected the manual keying as "two places to keep in step", and the mapping `citypay-fees-anti-corruption-layer` in the model says "the system passes each payment taken at the desk to CityPay". This option does not reverse C-02 and does not change the mapping; it postpones E4 and accepts the double entry until then. Until E4, a payment in `fees` is received and never confirmed, and C-26 (does "paid" mean received or confirmed) stays open. That is for the maintainer to confirm.
* **Leaves out:** E4, F, G2, H to L. In particular: a usage-fee copy is lent without a charge, so the desk charges it by hand (F); a copy marked damaged stays unavailable until somebody withdraws or releases it, which happens outside the system (H); a lost copy that comes back is handled by hand (G2).
* **LibTrack:** cannot be retired. The morning lists, the search, the reader's account, the report and CityPay still need it or a manual step.

### Option 3 — Option 2 and the morning lists

A, B, C, D, E1, E2, E3, G1, J1.

* **Delivers:** option 2, and the two lists of the morning, per branch, with names, phone numbers and titles. With them the story `overdue-book-fine-and-blocked-card` runs from its first sentence (the list) to the unblock, except for the telephone call and the keying into CityPay, which are done by people.
* **Tests of the cut:** option 2, and the case that no event covers: a staff page that composes `lending`, `membership` and `catalogue` through their public queries (ADR 8; finding F7 of the report).
* **Costs:** option 2, and a page with the public questions of three modules. The contact details of C-31 are decided, so there is no open interface.
* **Leaves out:** E4, F, G2, H, I, J2, K, L. The gaps named under option 2 (usage fee, damaged copy, lost copy that comes back) stay.
* **LibTrack:** cannot be retired. The search, the reader's account, the report and CityPay still need it or a manual step.

### Option 4 — The desk as far as it is clear

Option 3 and F, G2, H, I, K.

* **Delivers:** nearly everything a branch does at the desk, including lost and damaged copies, the usage fee, keeps and the search.
* **Tests of the cut:** everything in option 3, and the usage-fee mark on `catalogue` → `fees`, the paths of damaged copies and of a lost copy that comes back (F5, F6 of the report), and the ending of researcher status (F8).
* **Costs:** considerably more modelling than option 3 (not measured). G2 needs a refund, which is by hand until CityPay is known (C-30).
* **Leaves out:** E4, J2, L1, L2.
* **LibTrack:** could be retired for the desk only if the report, the notices and CityPay are handled by hand or kept alive.

## Recommendation: option 3

* **It tests the cut where it is most likely to be wrong.** The report found no blocking problem. Its main findings are about events that cross a boundary: the loan events to `fees` (F1), the membership events to `lending` (F2), the copy events from `catalogue` (F3, F5). Options 2 and 3 test the first two, and F3 in part. They do not test F5 (the release of a damaged copy, H) or F8 (the end of researcher status, I): only option 4 does. That is a gap we accept and name.
* **It adds the one boundary kind that nothing else tests.** The page that composes three modules (J1) is the case the cut says it can handle (ADR 8) and finding F7 doubted. It has no open interface, and the lists are what the brief says people rely on (§4) and what saves the hour of calls the director wants back (§2). The report called "the morning lists and notices" larger than they look (F7); with the contact details decided (C-31) and the notices split off (J2), J1 is sized M, but it is the part of option 3 where that warning applies.
* **It is the story of chapter 2.** Both stories of the tutorial are covered where they are about the system; the call and the keying remain with people.
* **It stays thin where the unknowns are.** CityPay (E4), the refund of a lost copy that comes back (G2) and the notices by email (J2) are left out; they are the parts whose interface or rule we do not know. The usage fee (F), the damaged copy (H) and keeps (I) are known but not needed for the story, and stay out.

**The strongest argument against it:** the report itself says that `fees` could come second without a change in the other three, "because it is a leaf of the graph", and that a scope without it is cheap if the loan events carry identity and business time from the first day. ADR 11, now accepted, guarantees that. So the case for including `fees` is not that it would be expensive to postpone, but that the test of ADR 5 and ADR 9 comes earlier and the story of chapter 2 is complete. If the maintainer, as the library, cares more about a working desk soon, option 1 is smaller and the test of `fees` then comes with the second increment; the loan events carry the envelope either way. If a smaller step with fines is wanted, option 2 is the one.

**What would change the recommendation:** a business reason that the first release needs the notices by email (J2) more than the fines; then the question of the mail gateway has to be answered first.

## Questions that the scope decides

*(Decided on 2026-10-26, see the last section. The text below is the proposal the maintainer accepted.)*

* **Does the first increment go live beside LibTrack, or does it stay a complete piece of software until further increments make a cut-over possible?** No option replaces LibTrack: the brief says the new system "must cover what LibTrack does today" (§1). Parallel running means double entry for everything the new system does. **Proposal:** for the tutorial, no go-live; each increment is complete as software and the cut-over is a later decision, as in the plan. This is for the maintainer to confirm, because it decides whether the double entry of option 2 ever happens in practice.
* **Option 2 and CityPay (see above):** confirm that postponing E4 is acceptable.
* **C-15, the waiting line for books that are out.** The question is parked "for the scope of the first release". **Proposal:** not in the first increment. It is a new feature that would change the rules for reservations (D); it reaches `lending` only. It is not decided here because it is part of the scope, which is the gate's decision. If the maintainer takes it in, it becomes part of D.
* **Parked rules that the options pull in:** C-12 (days a reservation is kept) and C-14 (the overdue limit per branch, the return at another branch) are rules of `lending` and come with every option; C-11 (collecting after a block) from option 2 on. They are decided when `lending` is modelled and do not wait for the scope. C-13 (28-day loans) is a setting. C-16 (waiving) and C-26 (the report) belong to L2 and L1, which no option contains.

## What we take with us

* **Gate G6 is closed** (2026-10-26). The chapters on the flows and contracts and on the detailed modelling can start.
* The skill `plan-scope` exists and was used here for the first time. A fresh agent reviewed this chapter and found errors in the first version (among them a wrong statement about how fines are handled today); the skill now asks for a column of needs, a check that each option contains what its members need, and a line on the system being replaced.
* The accepted candidates are the list of scenarios that chapter 7 models in DDD Studio, across the contexts they touch.

## Decisions in this chapter

* **Way of working, gate G6 — decided by the maintainer on 2026-10-26.** The maintainer accepted the chapter as written, with its recommendation and its proposals, after reading it in the pull request. So:
  * **The first increment is option 3:** A, B, C, D, E1, E2, E3, G1 and J1. Candidates in these terms: titles and copies; members, cards, holds; check out and return, with a damaged copy marked at check-in; reservations; the late fine, the running fine with the block above €10, the payment at the desk and the unblock; declaring a copy lost with the lost-book fee; the morning lists.
  * **Rejected:** option 1 (without fines and blocking), option 2 (without the morning lists), option 4 (the whole desk as far as it is clear). Reasons are in the chapter.
  * **Left out of the first increment:** E4 (CityPay), F (usage fee), G2 (a lost copy comes back), H (withdraw or release a damaged copy), I (keeps, end of researcher status), J2 (notices by email), K (search, the reader's account), L1 (monthly report), L2 (waiving). The gaps this leaves are named under each option.
  * **LibTrack:** the first increment does not go live beside LibTrack. Each increment is complete as software; the cut-over is a later decision.
  * **CityPay:** postponing E4 is accepted; until it is built, a payment in `fees` means "received" only, and C-26 stays open. C-02 is not reversed.
  * **C-15** (the waiting line for books that are out): not in the first increment (recorded in the [clarification log](../requirements/clarifications.md)).
* **Business:** C-15 as above. The parked C-11, C-12 and C-14 are decided when `lending` is modelled (chapter 7).
* **Architecture:** none.

[^adr10]: When this chapter was written, ADR 10 had settled that a front end asks over REST. The maintainer reopened ADR 10 on 2026-10-28; how a front end reaches a module is decided at gate G2. The candidates and options of this chapter do not depend on it.

---

*No board was changed in this chapter and no Studio version was saved for it. Sources: [`model/domain-stories/`](../model/domain-stories/), [`model/sketch/big-picture-contexts.json`](../model/sketch/big-picture-contexts.json), [`model/esdm/`](../model/esdm/), [`docs/reviews/pre-g6-context-cut.md`](../docs/reviews/pre-g6-context-cut.md).*
