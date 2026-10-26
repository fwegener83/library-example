---
status: "proposed"
date: 2026-10-25
decision-makers: the maintainer
consulted: none recorded
informed: none recorded
---

# 11. Every published event names its subject, its business time and its place in order

## Context and Problem Statement

[ADR 4](0004-contexts-talk-through-published-events.md) says: "Reactions to events must tolerate events that arrive twice or late." It leaves to each context what to do about it ("the rules of each context must say what happens then") and announces a record of its own for the contract of events. This record covers the **envelope** every event carries, so that a context can apply its rules at all. It builds on ADR 4 and changes none of it. The versioning of events (adding fields, events in transit during a release) stays with the record that ADR 4 announces; it is written when the first event is specified in chapter 7.

So far only one direction has the means to be tolerant, and it does so for orders, not events: `membership` "ignores a request that is older than the last one it applied for the same hold" ([ADR 5](0005-no-circle-between-modules.md)), judged by the time of the decision that the order carries. The events themselves carry nothing that lets a consumer tell a repeat from a new fact, or an old fact from a new one.

The review before gate G6 (`docs/reviews/pre-g6-context-cut.md`, F1, F2, F3, F5) played the cases through:

* *Book Returned* reaches `fees` twice. Without a loan identity, `fees` can only compare copy, reader and due date, and a reader who returns a copy and borrows it again the same day has the same three values twice.
* *Book Returned* arrives after midnight, and the morning run (C-03) has already added a running day. The €10 line is 21 days (21 × €0.50 = €10.50), so one day decides the hold.
* *Card Blocked* and *Card Unblocked* arrive in reverse order. `lending` keeps "blocked" with no way to know it is wrong.
* The Head of Collection releases a damaged copy, it is damaged again, and the first release arrives late. `lending` cannot tell which damage the release answers.
* An event or an order names a copy that the receiver does not know yet.

The phase 5 flows (chapter 7) will specify every event that crosses a boundary. What must every one of them carry, and what does a consumer do with it?

## Decision Drivers

* Tolerance of repeated and late events is already a rule (ADR 4); it needs the information to be possible.
* A field added later is missing from every event already published or in transit, so every consumer would have to handle old and new events for good (ADR 4: an event is "changed only by adding to it"). Better to have the fields from the first event on.
* Business rules count in business time: the day a book came back, not the day the message arrived (C-03, C-28).
* One rule for all events is cheaper to model, build and check than one per context.
* The technology of delivery is decided at gate G2 and stays out of this record.

## Considered Options

1. One rule for every published event: subject identity, business time and order per subject
2. Identity by natural keys, no order
3. Leave it to each context in phase 5

## Decision Outcome

Recommended option: "One rule for every published event: subject identity, business time and order per subject", because it is the smallest rule that makes the cases above decidable, and it costs a few fields that are cheap now and expensive later.

Every event a module publishes carries:

* **the identity of its subject**, issued by the owner (ADR 7). The subject is the thing whose story the event tells: the member (also for everything about the card, its holds and the end dates, because the card number is only an attribute of the member, ADR 7), the copy, the title, and, new, **the loan**, issued by `lending` when a copy is checked out, and **the damage report**, issued by `lending` when it records a damaged copy;
* **the business time of the fact**: the date or moment it happened in the business ("returned on", "declared lost on", "decided at"), not the moment it was sent;
* **its place in order for its subject**: a number that grows by one with every event the publisher issues about that subject, without gaps, like the version of an aggregate. Publisher, subject and number together identify the event, so no separate event identifier is needed.

A consumer handles the place in order like this:

* a number it has already applied is a **repeat** and is ignored;
* the next number is applied;
* a number with a gap before it is **held back** until the missing events have arrived.

It never drops an event only because a later one came first. A later event is not a replacement for an earlier one unless it says so by carrying the whole state of what it changes.

Where two publishers are involved, there is no common order:

* Facts that change over time (the usage-fee mark, the end of a card, the restricted kind) are kept with their business time. A consumer judges a loan, a checkout or a fine by the state at the business time of that action. When a late fact arrives, it corrects what it already did: `fees` fixes the late fine to the day of a late *Returned* and lifts its hold if the €10 line was crossed only by the extra day (the placer lifts, ADR 5); it recalculates a usage fee when a correction of the mark turns up late.
* Business times of different publishers can be compared, because there is one application and one clock (ADR 2).
* Where business time is not enough, the event **names what it answers**. A release of a damaged copy carries the damage report it answers; `lending` makes a copy lendable only if that is its latest damage report. The Head of Collection's list in `lending` shows the damage report identifier, and the staff page that releases a copy passes it on (ADR 8). The same holds for any later event that answers a specific earlier one.

Two more rules:

* **An event that refers to a subject of another context that the consumer does not know yet** is held back and tried again later. Nothing is assumed: an unknown copy is not treated as circulating, and a checkout of a copy without a known usage-fee mark is not treated as free. The event that introduces its own subject (*Copy Registered*, *Checked Out*) is not held back for that reason. A held-back event is visible, as a list with its age, not silent.
* **An order or a desk action about a subject the module does not know** is refused with a clear reason ("copy not known yet"). Staff can try again.

Validity that the business states as a duration (a card valid for a year, researcher status for twelve months) travels as a **date** in the event that grants or renews it, and the consumer compares it with today (C-28). The event that reports the end is information, not the trigger of the rule.

Not decided here: the field names, the format of the identifiers, how the order number is produced, how long an event may be held back, and how events are delivered and stored (gate G2).

### Consequences

* Good, because each case of the review has an answer: a repeated *Returned* is a repeat by its number; the late fine counts to the day of the return and the extra running day is taken back; a late *Card Unblocked* is applied in its place, after the *Card Blocked* it follows; a release answers a named damage report; an unknown copy is never lent by default.
* Good, because it is one rule the phase 5 flows and the `check-model-code` step can check for every event.
* Bad, because every event gets three fields, and every consumer keeps, per subject, the last number it applied.
* Bad, because "hold back" needs a place to park events, and a missing event stops the later events about the same subject. How long to wait, and what happens when an event never comes, is decided with the delivery at gate G2; the held-back list makes it visible meanwhile.
* Bad, because a renewal reaches `lending` late as well. A researcher who renews on the last valid day and walks to the lending desk after midnight may be refused until the renewal arrives. The error is on the safe side (a refusal the desk can retry, no restricted copy lent by mistake), but it exists.
* Bad, because between publishers the rule cannot make everything exact: a checkout at 10:05 can reach `fees` before the correction of the mark made at 10:00. `fees` corrects the usage fee when the correction arrives; for a short time the amount owed is off.
* Neutral, because there are now two mechanisms with one purpose: orders (ADR 5) carry the time of the decision, events carry the number in order. An order is a request by a customer, an event is a fact of its publisher (ADR 4), so each keeps what fits it.
* Neutral, because when this record is accepted, ADR 7 gets a line pointing here: the loan and the damage report are identifiers issued by `lending`. The rule of ADR 7, "the owner issues it", stays.

## Pros and Cons of the Options

### One rule for every published event: subject identity, business time and order per subject

* Good, because it solves repeats, lateness and reordering in one place, in every context.
* Good, because it needs no extra identifier for an event: publisher, subject and number are enough.
* Bad, because it adds fields and a little state to every consumer, also where a context could have done with less.
* Bad, because strict order without gaps costs waiting when an event is lost.

### Identity by natural keys, no order

The consumer recognises a fact by the values it carries (copy, reader, due date).

* Good, because the events stay small.
* Bad, because natural keys are not unique (the same copy borrowed twice on one day) and cannot express order (blocked, then unblocked).

### Leave it to each context in phase 5

* Good, because each context takes only what it needs.
* Bad, because the same question is answered four times, possibly four ways, and the first event without the information is fixed for good once it has been published.
