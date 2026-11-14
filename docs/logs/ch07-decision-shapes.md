# Chapter 7 — shapes for decisions over several streams

Status: **decided** by the maintainer on 2026-11-14 and **built** the same
day in the tutorial workspace (flow 1 and the static view it needs; see
"As built" at the end). It replaces the proposal of 2026-11-12 ("variant
A", in the git history of this file). That proposal was reviewed twice
(a code review of the file, a second agent's review of the follow-up)
and probed in a throw-away workspace; what changed and why is in
"Rejected on the way" below.

The decision rests on DDD Studio's own guidance as of 2026-11-14:
`explain_model flows-and-slices`, section "Which shape for a decision",
and `explain_concept` for the dynamic consistency boundary (DCB),
aggregate, policy, actor and read model.

It revises decisions 2, 3 and 7 of `docs/logs/ch07-storylines.md` and
the fee step of decision 5's flow (step 19). Decisions 1, 4, 6, 8 and 9
stay.

## The rule

One question per decision: **where does the fact come from that the
decision needs, and who may report it?** Studio names one shape per
answer.

| The decision needs | Shape | Cases in Millbrook |
|---|---|---|
| only the events of one container | aggregate | the €10 line in `reader-account`; return, overdue and loss of a loan |
| that something exists | no boundary: the command goes to the thing it is about, or the issuer picks the thing from a view (informed decision) | a copy needs a title |
| a value that must be unique and can be missing or corrected | DCB | the ISBN |
| a rule over events of its own context that no single container owns | DCB | checkout and reservation |
| a rule over a fact of another context, together with its own events | the fact is taken in as an event of its own context (policy → command → event); an aggregate or a DCB decides on it | card valid, card blocked, researcher status in `lending` |
| only a value another context owns, a stale one will do, and the issuer can be trusted | the issuer looks it up in a view and puts it into the command (automation over a view, or informed decision); the rule about the value stays an invariant of whoever takes the command | the replacement price in `fees` |
| consistency across contexts | process manager, or a DCB reading the other context (needs a shared event store) | none in this increment |

## lending

### Aggregates

| Aggregate | Its life | Commands |
|---|---|---|
| `copy` | the physical copy in `lending`: taken in, reclassified, found damaged, retired | `take-in-copy`, `reclassify-copy`, `record-damage` (name to be fixed while building), `retire-copy` |
| `loan` (new) | opened by the checkout DCB, then returned, overdue, declared lost | `return-copy`, `mark-loan-overdue`, `declare-copy-lost` |
| `reader` (new, thin) | lending's own record of membership facts | one command per fact, see below |

`loan` is the case Studio calls unproblematic: the DCB's event *starts*
the aggregate's life (Studio's own example is "a checkout opens the
loan"), and after that only `loan` writes. The loan is already a subject
of its own in ADR 11 (`loan-id`).

`copy` keeps only the physical copy. Its checkout, return and
reservation events move to `loan` and to the reservation DCB.

### Dynamic consistency boundaries

| DCB | Selected by | Commands | Writes |
|---|---|---|---|
| `checkout` | `barcode`, `member-id` of the command | `check-out-copy` (also collecting a reservation, C-11) | the opening event of `loan` |
| `reservation` | `barcode`, `member-id` of the command | `reserve-copy`, `cancel-reservation`, `expire-reservation` | free-standing events of `lending`: reserved, cancelled, expired |

Reservations have **no aggregate**. Collecting a reservation is a
checkout, and with an aggregate the checkout would write into the middle
of the reservation's life: the case Studio calls risky. As free-standing
events there is one writer per event, and a reservation ends when it is
cancelled, expires, or a loan of the same copy to the same reader is
opened. ADR 11 stays as it is. The price: cancel and expire carry
`barcode` and `member-id` (every command of a DCB carries all its
selection fields) and read more than they need.

**What `checkout` consults** (Studio does not check that the list is
complete; this is it):

| Source | Events | Criterion |
|---|---|---|
| `copy` | taken in, reclassified, found damaged, retired | of this barcode |
| `loan` | opened, returned, declared lost | of this barcode; overdue loans of this reader count for nothing here (C-14 stops reservations, not loans) |
| reservation | reserved, cancelled, expired; and `loan` opened | of this barcode |
| `reader` | the four facts below | of this reader |

`copy-retired` is lending's own event; the catalogue's `copy-withdrawn`
is not read across the boundary.

**What `reservation` consults:** the same, and in addition the
reservations of this reader (five reservations) and the overdue loans of
this reader at this branch (overdue limit, C-14).

Invariants move from today's `copy` (ids change, the rejection of slice
17 is set again):

| To | Invariants |
|---|---|
| `checkout` | copy known, copy on the shelf or reserved for this reader, card valid on the day, card not blocked, restricted only for researchers |
| `reservation` | copy known, copy on the shelf to reserve, card valid on the day, card not blocked, restricted only for researchers, five reservations, overdue limit at the branch, active reservation (for cancel and expire) |
| `loan` | only an open loan can be returned or declared lost |

The card and copy rules are the same text in both DCBs. Studio gives
every invariant exactly one anchor, so they are written twice.

### Damaged copies

A copy found damaged stays unavailable in this increment: scenario H
(withdraw or release by the Head of Collection, C-25) is out of the
first increment (chapter 6). Both DCBs consult *found damaged*. When H
comes, the catalogue's release reaches `lending` as an event of its own
(C-25), and both consult lists get it.

### Reader facts

All three facts are hard rules, so all three are taken in as events of
`lending`:

| Fact | Rule | Source |
|---|---|---|
| card valid until | no new loan or reservation after the date | C-05, C-28 |
| blocked | no new loan or reservation, no collecting | brief §3.3, C-01, C-11 |
| researcher until | a restricted copy is never lent after the date, "not even for minutes" | C-28, C-29 |

The second review proposed to pass the researcher status in the command
instead, as a value that only steers a variant. In Millbrook it is an
access rule of the same kind as the card's validity (C-28 treats both
alike), and a reservation "online or by phone" (brief §3.2, with K
later) would make the reader the issuer, who must not report their own
status.

| Membership event | Policy | Command on `reader` | Event of `lending` |
|---|---|---|---|
| member registered, card renewed | two policies | `note-card-validity` | card validity noted (`card-valid-until`) |
| card blocked | one policy | `note-card-block` | card block noted |
| card unblocked | one policy | `note-card-unblock` | card unblock noted |
| researcher status granted | one policy | `note-researcher-status` | researcher status noted (`researcher-until`) |

Names to be fixed while building. Duplicates are the policies' business
(`idempotency`), not an invariant of `reader`. Holding back an event
that came out of order (ADR 11) is delivery and is decided at G2.

`reader-standing` (the read model) projects these events and stays what
the desk sees: the desk finds the `member-id` by the card number there
(informed decision) and puts it into the command. The DCBs select by
`member-id`.

## fees

The policy `assess-fine-on-return` cannot read the replacement price
(a policy cannot read). It is replaced by **automation over a view**:

- A system actor of `fees` reads a to-do list of returns that still
  need a fine, with the replacement price of the title next to each row
  (`replacement-prices` folds the catalogue's title events, as today).
- It issues `assess-late-fine` with the price in the command's data.
  The command's actors name only that actor: the price is its claim.
- The invariant "a fine never exceeds the replacement price" stays on
  `reader-account` and is checked against the command's data.
- The to-do list also projects *late fine assessed*, so a row leaves the
  list once the fine is fixed.

The same shape for the lost-book fee (G1) and for the recount by the
morning run (C-38: the cap is the price in force on the day of the run).
For the recount the to-do list carries the price of each running loan;
whether one command per account carries a list of loans and prices, or
one command per loan, is settled while building.

No DCB and no price event of `fees`. `reader-account` keeps all its
commands.

## catalogue

| Rule | Shape |
|---|---|
| an ISBN appears once (C-24: some titles have none; an ISBN can be corrected) | DCB `title-registration`, selected by the ISBN of the command; it consults titles added and ISBN corrections with that ISBN. A correction must name the old ISBN as well, or the ISBN gets a command of its own; settled while building |
| a copy needs an existing title | informed decision: the Head of Collection picks the title from a view; `register-copy` stays on the aggregate `copy` of `catalogue` |

## membership

No change.

## Rejected on the way

| Proposal (2026-11-12) | Why not | Found by |
|---|---|---|
| one DCB `lending-decision` for checkout and reservation | the selection and the consult list belong to the DCB, not to the command: a checkout would read everything a reservation needs | code review |
| `copy` stays an aggregate while the DCB writes its checkout events | two writers in the middle of one life; Studio calls this risky | code review, Studio guidance |
| the consult list without *found damaged* | the DCB would lend a damaged copy | code review |
| one snapshot event `reader-standing-noted` | a stateless policy cannot build it from five delta events | code review |
| DCBs as anchors that only take a fact in (`reader-standing-record`, `replacement-price-record`) | a container with one identity and its own events is an aggregate; Studio now names the thin aggregate as the shape | code review, Studio guidance |
| DCB `charge-decision` in `fees` with a price event of its own | a price is a value, no race matters; the recount spans several titles, which a DCB selection cannot express | code review, Studio guidance |
| DCB `copy-registration` | existence is no reason for a boundary | Studio guidance |
| reservation as an aggregate | collecting writes into the middle of its life | second review |
| researcher status as a value in the command | a hard access rule; the issuer may be the reader | this file, against the second review |
| variant B, DCBs consulting `membership` events directly | ADR 4 (a module uses its own copy); presumes a shared event store before G2 | proposal |

## Probed, and what not

In the throw-away workspace "zz probe DCB fit for Millbrook":

- a DCB refusing a checkout on a blocked card, with the consulted events
  drawn, and the scenario the flow derives from it;
- an aggregate reading as History an event a DCB command wrote
  (`return-copy` after a DCB checkout), with its derived scenario;
- `loan` opened by the checkout DCB and returned by its own command;
  reservations as free-standing events; a checkout refused because the
  copy is reserved for someone else; a reservation that cannot expire
  because a loan collected it;
- the ESDM export of a DCB, its command and a free-standing event, and
  `apply_esdm` taking the DCB back in a dry run.

`validate_model` reports no finding apart from the missing context
mapping in the probe, which the tutorial has.

`esdm lint` runs later in the pipeline (L1, maintainer 2026-11-14); it
was not run on the probe.

## What it does to the notes on the model

| Note | After this decision |
|---|---|
| Gap 1, a rule over copy and reader | resolved: `checkout` and `reservation` |
| Gap 2, checkout reads the reader's standing | resolved: reader facts as events of `lending` |
| Gap 2 in `fees`, the price | resolved: the price travels in the command. The second question of the note (a list of loans in the account) stays for chapter 8 |
| Gap 3, conditional events | resolved with scenarios (slices 15 and 21 marked, plus a variant "line not crossed") |
| Gap 4, owner of a policy | by design in Studio and ESDM; ownership by name, description and the context mapping (tool gap 14) |
| Gap 5, ISBN and title existence | resolved: DCB, informed decision |
| Gap 6, the morning list | resolved: read-model slices one after the other (ADR 8) |
| Gap 7, time | resolved: automation over a view; the schedule is in the actor's responsibilities |
| Asymmetry copies and readers | resolved: both arrive by policy into an aggregate of `lending` |

## As built (2026-11-14)

Studio versions: `ch07-flow1-before-decision-shapes` (before),
`ch07-flow1-decision-shapes` (after). `validate_model` reports nothing.

**Names**, fixed while building:

| Context | Element | Kind |
|---|---|---|
| lending | `checkout`, `reservation` | DCB |
| lending | `loan`, `reader` | aggregate (new) |
| lending | `reserve-copy`, `cancel-reservation`, `expire-reservation` | commands of `reservation` |
| lending | `note-card-validity`, `note-card-block`, `note-card-unblock`, `note-researcher-status` | commands of `reader` |
| lending | `card-validity-noted`, `card-block-noted`, `card-unblock-noted`, `researcher-status-noted` | events of `reader` |
| domain | `take-in-member-registration`, `take-in-card-renewal`, `take-in-card-block`, `take-in-card-unblock`, `take-in-researcher-status` | policies, owner lending |
| lending | `record-damage` | command of `copy` |
| lending | `open-loans`, `find-open-loan` | read model, query |
| fees | `fee-assessor` | system actor |
| fees | `returns-to-assess`, `find-returns-to-assess` | read model, query |
| fees | `find-replacement-price` renamed `find-replacement-prices` | query |
| catalogue | `title-registration`, `isbn-correction` | DCB |
| catalogue | `correct-isbn`, `isbn-corrected` | command, event |
| catalogue | `titles`, `find-titles` | read model, query |

Removed: the policy `assess-fine-on-return`; the invariants of `copy`
(lending) that moved to the boundaries; `isbn-once-in-catalogue` on
`title`; `title-in-catalogue` on `copy` (catalogue).

**Settled while building:**

- `check-out-copy` carries `member-id` instead of `card-number`; the desk
  finds it in `reader-standing` (slice 6).
- `return-copy` carries the `loan-id` from `open-loans` (new slice 18a).
  A damage found at check-in is a second command, `record-damage`, on the
  copy; the loan and the copy each keep one writer.
- The ISBN correction needs the `title-id`, which `add-title` does not
  have yet, so it is a second boundary `isbn-correction` with its own
  command `correct-isbn`; its event names the previous ISBN.
  `correct-title-details` no longer changes the ISBN.
- The recount carries one price per title of a running loan (`prices`);
  `accounts-with-running-fines` lists the running loans with their titles,
  `overdue-loan-recorded` carries the title.
- The checkout does not read the overdue loans of the reader (C-14 stops
  reservations, not loans); the reservation does.

**Flow 1**, now 33 slices. New: 1b (the title is picked), 3a and 3b (copy
4712 registered and taken in, so slices 17 and 23 have a copy lending
knows), 5b, 16b and 22b (the card facts taken in), 14b and 18c (the price
read), 18a (the open loan found), 18b (the return on the fee-assessor's
list). No slice name carries `[?]` any more. Marked as scenarios: 7, 15,
17, 18, 19, 21 and 23; the feature of `reader-account` adds the two other
outcomes of the €10 line (`recount-stays-at-or-below-ten-euro`,
`payment-leaves-amount-above-ten-euro`).

**Notes:** each of the nine notes has a comment that says how it is
answered, as a proposal. Deciding them is the maintainer's call.

**Still open:**

- Scenarios for `place-hold` and `lift-hold` (card-blocked only for the
  first hold) with the membership feature.
- Flows 2 to 4 and the variants; the reservation boundary is built but no
  flow tells it yet.
- Exports to `model/esdm/` at the end of the chapter.
