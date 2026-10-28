# Chapter 7 — storylines (step 2)

Written before any node exists. Each step names its context, its kind
(see → read-model slice; do → command slice; refused → command slice with
a rejection; by itself → command slice triggered by a policy or the
morning run) and its source. The nodes are created step by step from
this list (step 3).

## Decisions of shape, taken before the storylines

Each one has its reason here; the retrospective rates how it fitted.

1. **How `lending` learns of copies: a policy into a command of
   `lending`.** `lending` has its own *copy* with a life of its own (on
   the shelf, reserved, on loan, damaged, lost, retired) and rules that
   protect it. It is born when the catalogue registers a copy, so a
   policy turns *copy registered* into *take in copy*; corrections and
   withdrawals take the same path (ADR 4: `lending` keeps its own
   record). *Rejected:* a read model in `lending` on the catalogue's
   events. A read model cannot protect "one copy, one loan".
2. **How `lending` learns of readers: a read model on the membership
   events.** Nothing in `lending` changes the reader's card, status or
   block; `lending` only looks them up when it decides. The membership
   events carry the dates and the block as of the event (C-28, ADR 11),
   so the read model `reader-standing` projects them directly. *Rejected:*
   a policy and a *reader* aggregate in `lending` that would only copy
   the fields (an aggregate without a rule of its own).
3. **Checkout and reservation are decided by the copy, which consults
   the reader's standing.** The rules belong to two things at once: the
   copy (on the shelf, not reserved for someone else) and the reader
   (card valid and not blocked, researcher for restricted copies, five
   reservations, overdue limit at the branch). The real boundary is the
   copy named in the command plus the reader named in it (a dynamic
   consistency boundary). Studio has none; its stand-in is an aggregate
   whose description says so. The copy is the stand-in because the strict
   rule is the copy's (one loan, one reservation); the reader's side is
   read from `reader-standing` and from `lending`'s own loans and
   reservations, which are as current as the events that fed them (ADR
   4). *Rejected:* the reader as the deciding aggregate with the copy
   following by event and a compensation when a copy was taken twice
   (as in ddd-by-examples/library). It needs compensation events for a
   case the desk cannot produce for a checkout (the copy is in the
   reader's hand) and that is rare for a reservation.
4. **The morning run is a system actor that reads a to-do list.** C-34:
   one run a day, not a timer per loan. In each context it sees a read
   model of what is due (loans due for overdue, reservations to expire,
   accounts with running fines) and issues one command per row. *Rejected:*
   a process manager per loan with a timer at the due date: correct, but
   thousands of instances for what the library does as one list.
5. **The €10 rule: decided in the reader's account in `fees`, carried
   to `membership` by stateless policies** (tool gap 15). The account
   publishes *reader fell into arrears* or *reader left arrears* when the
   amount owed crosses the line, after any change: a fine, a lost-book
   fee, a payment, the morning recount. The policy *hold card in
   arrears* turns it into *place hold* in `membership`, *lift hold when
   paid* into *lift hold*. Owner of both policies: `fees` (C-19; tool gap
   14, written in the description).
6. **`fees` learns of a loan when it becomes overdue**, not at checkout.
   The running fine starts the day after the due date, and *loan became
   overdue* carries what `fees` needs (loan, member, title, due date).
   *Returned* carries the due date and the day of return, so the late fine
   can be fixed even if *returned* arrives before *became overdue*
   (ADR 11). *Checked out* is not used by `fees` in this increment (usage
   fee, F, is out).
7. **The replacement price in `fees`: a read model `replacement-prices`**
   on the catalogue's title events. The reader's account reads it when it
   fixes a charge (C-38). Studio has no reference from an aggregate to a
   read model it consults; the description says it.
8. **Identifiers (ADR 7 left this to the modelling of `catalogue`):**
   a title gets an identifier from `catalogue` (`title-id`), the ISBN is
   an attribute (some local history has none); a copy is identified by
   its barcode, which the catalogue issues when it registers the copy. A
   member is identified by the member number (`member-id`); the card
   number is an attribute (ADR 7). A loan has a `loan-id`, issued by
   `lending` at checkout (ADR 11).
9. **What every published event carries (ADR 11):** the subject's
   identifier, the business time of the fact, and `sequence`, its place
   in order for that subject. Field names are the model's; ADR 11 left
   them open.

## Example figures (used in every flow)

| Who / what | Values |
|---|---|
| Maria Okoye | member M-1001, card 100234, registered 12 Jan 2026, card valid through 11 Jan 2027, phone 555-0142 |
| Jonas Berg | member M-1002, card 100235, registered 2 Feb 2026, valid through 1 Feb 2027, no phone |
| Dr Amira Haddad | member M-1003, card 100236, valid through 4 Mar 2027; researcher from 2 Mar 2026 through 1 Mar 2027 |
| *The Hobbit*, J. R. R. Tolkien | title T-0001, ISBN 978-0-261-10235-4, replacement price €14.90 |
| *Millbrook: A Local History* | title T-0002, no ISBN, replacement price €38.00 |
| Copies | 4711 and 4712 (*The Hobbit*, circulating, home Riverside); 4713 (*The Hobbit*, circulating, home Central); 5101 (*Millbrook*, restricted, home Old Town) |

Dates and amounts, checked: a checkout on 3 Aug 2026 is due 2 Oct 2026
(+60 days, C-13, C-34), overdue from 3 Oct; on 23 Oct it is 21 days
overdue, €10.50 (above €10, C-03); returned 24 Oct, 22 days, €11.00. A
reservation on Mon 7 Sep is kept through Thu 10 Sep and has run out on
Fri 11 Sep (C-12, C-34). A checkout on 1 Sep is due 31 Oct; declared lost
on 10 Nov (10 days overdue, running €5.00, dropped, C-04): lost-book fee
€14.90 + €5.00 = €19.90.

## Flow 1 — From the shelf to a blocked card and back

Scenarios A, B, C, E1, E2, E3 and half of J1. All four contexts.

| # | Context | Kind | Step | Source |
|---|---|---|---|---|
| 1 | catalogue | do | Head of Collection adds *The Hobbit*, €14.90 → *title added* | brief §3.1 |
| 2 | catalogue | do | Head of Collection registers copy 4711, circulating, home Riverside → *copy registered* | §3.1, C-24 |
| 3 | lending | by itself | policy *take in registered copy* → *take in copy* → *copy taken in* (on the shelf at Riverside) | ADR 4, decision 1 |
| 4 | fees | see | `replacement-prices` shows T-0001 at €14.90 (projects *title added*) | C-38, decision 7 |
| 5 | membership | do | Membership Officer registers Maria → *member registered* (card 100234 through 11 Jan 2027) | §3.3, C-28, C-31 |
| 6 | lending | see | `reader-standing` shows Maria: valid through 11 Jan 2027, not blocked | decision 2 |
| 7 | lending | do | Branch librarian checks out 4711 to card 100234 at Riverside, 3 Aug → *copy checked out*, loan L-0001 due 2 Oct | §3.2, C-13 |
| 8 | lending | see | the morning run sees `loans-due-for-overdue` on 3 Oct: L-0001 | C-34, decision 4 |
| 9 | lending | by itself | morning run → *mark loan overdue* → *loan became overdue* (overdue since 3 Oct) | C-34 |
| 10 | fees | by itself | policy *track overdue loan* → *record overdue loan* → *overdue loan recorded* | C-03, decision 6 |
| 11 | lending | see | Riverside's `overdue-loans` on 3 Oct: L-0001, copy 4711, M-1001, 1 day | §3.2, §4, J1 |
| 12 | membership | see | `member-contacts`: M-1001 Maria Okoye, 555-0142 | C-31, ADR 8 |
| 13 | catalogue | see | `copy-titles`: 4711 *The Hobbit*, Tolkien | ADR 8 |
| 14 | fees | see | the morning run sees `accounts-with-running-fines` on 23 Oct: M-1001 | C-03 |
| 15 | fees | by itself | morning run → *recount amount owed* → *amount owed recounted* (€10.50) and *reader fell into arrears* | C-03, C-18, decision 5 |
| 16 | membership | by itself | policy *hold card in arrears* → *place hold* "unpaid fees" by fees → *hold placed*, *card blocked* | C-19, ADR 5 |
| 17 | lending | refused | Maria wants 4712 on 23 Oct → refused: card blocked | §3.3, C-01 |
| 18 | lending | do | Maria returns 4711 on 24 Oct → *copy returned* | §3.2 |
| 19 | fees | by itself | policy *assess fine on return* → *assess late fine* → *late fine assessed* €11.00 (still in arrears) | §3.4, C-03 |
| 20 | fees | see | the librarian sees `amounts-owed`: M-1001 owes €11.00 | §3.4 |
| 21 | fees | do | Maria pays €5.00 at the desk → *payment received*, amount owed €6.00, and *reader left arrears* | C-22, C-35 |
| 22 | membership | by itself | policy *lift hold when paid* → *lift hold* → *hold lifted*, *card unblocked* | C-01, ADR 5 |
| 23 | lending | do | Maria checks out 4712 on 24 Oct → *copy checked out* | §3.3 ("we unblock") |

## Flow 2 — A reservation runs out

Scenario D and the other half of J1.

| # | Context | Kind | Step | Source |
|---|---|---|---|---|
| 1 | lending | do | Jonas reserves 4712 at Riverside on 7 Sep → *copy reserved*, kept through 10 Sep | §3.2, C-12, C-34 |
| 2 | lending | see | the morning run sees `reservations-to-expire` on 11 Sep: 4712 | C-34 |
| 3 | lending | by itself | morning run → *expire reservation* → *reservation expired*; the copy is available again | §3.2 |
| 4 | lending | see | Riverside's `expired-reservations` for 11 Sep: 4712, M-1002 | §3.2 ("ran out yesterday") |
| 5 | membership | see | `member-contacts`: M-1002 Jonas Berg, no phone number | C-31 |
| 6 | catalogue | see | `copy-titles`: 4712 *The Hobbit* | ADR 8 |

## Flow 3 — A copy is lost

Scenario G1.

| # | Context | Kind | Step | Source |
|---|---|---|---|---|
| 1 | lending | do | Jonas checks out 4713 at Central on 1 Sep → *copy checked out*, due 31 Oct | §3.2 |
| 2 | lending | do | Jonas reports 4713 lost at the desk on 10 Nov → *copy declared lost* | §3.4, C-04 |
| 3 | fees | by itself | policy *charge lost copy* → *charge lost-book fee* → *lost-book fee charged* €19.90 (running €5.00 dropped) and *reader fell into arrears* | C-04, C-18 |
| 4 | membership | by itself | *hold card in arrears* → *place hold* → *hold placed*, *card blocked* | C-19 |
| 5 | lending | see | the Head of Collection sees `copies-to-review`: 4713, lost on 10 Nov | C-20 |
| 6 | catalogue | do | Head of Collection withdraws 4713 → *copy withdrawn* | C-20 |
| 7 | lending | by itself | policy *retire withdrawn copy* → *retire copy* → *copy retired* | C-20 |

## Flow 4 — A restricted copy for a researcher

Scenarios A, B, C (C-29).

| # | Context | Kind | Step | Source |
|---|---|---|---|---|
| 1 | catalogue | do | Head of Collection registers copy 5101 of *Millbrook*, restricted, home Old Town → *copy registered* | §3.1 |
| 2 | lending | by itself | *take in registered copy* → *copy taken in* (restricted) | decision 1 |
| 3 | membership | do | Membership Officer grants researcher status to Amira on 2 Mar 2026 → *researcher status granted* (through 1 Mar 2027) | §3.3, C-28, C-37 |
| 4 | lending | see | `reader-standing`: Amira researcher through 1 Mar 2027 | decision 2 |
| 5 | lending | do | Amira checks out 5101 at Old Town on 5 Oct → *copy checked out* | C-29 |

## Variants (short flows, one rule each)

| Flow | Steps | Source |
|---|---|---|
| A restricted copy is refused to a reader who is not a researcher | Maria wants 5101 → refused: restricted for researchers | C-29 |
| Checkout refused: card expired | Jonas, card through 1 Feb 2027, wants 4712 on 2 Feb 2027 → refused | C-05, C-28 |
| A copy that `lending` does not know yet | checkout of 4714 before it is taken in → refused: copy not known | C-33 |
| A reservation is collected | Jonas reserves 4712 on 7 Sep, collects it on 9 Sep → *copy checked out* (reservation ends) | §3.2 |
| Collecting is refused while the card is blocked | → refused: card blocked; the reservation stays | C-11 |
| A reservation is cancelled | → *reservation cancelled* | C-10 |
| Reservation refused: five reservations | Maria has five, reserves a sixth → refused | §3.2 |
| Reservation refused: overdue limit at the branch | three loans from Riverside overdue → refused at Riverside | §3.2, C-14 |
| Reservation refused: copy not on the shelf | 4711 is on loan → refused | §3.2 |
| A damaged copy comes back | return with damage → *copy returned*, *copy found damaged*; listed for the Head of Collection | §3.2, C-06 |
| The Head of Collection corrects a copy | 4712 restricted → *copy corrected* → `lending` *reclassify copy* | C-27 |
| The Head of Collection corrects a title's price | *title details corrected* → `replacement-prices` | §3.1, C-38 |
| A card is renewed | *card renewed* → `reader-standing` | §3.3, C-36 |
| A payment above the amount owed is refused | → refused | C-35 |
| A hold is lifted by someone who did not place it | → refused | C-19, ADR 5 |
