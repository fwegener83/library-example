---
status: "proposed"
date: 2026-10-25
decision-makers: the maintainer
consulted: none recorded
informed: none recorded
---

# 11. Every published event names its subject, its business time and its place in order

## Context and Problem Statement

[ADR 4](0004-contexts-talk-through-published-events.md) says: "Reactions to events must tolerate events that arrive twice or late." It announces a record of its own for the contract of events: "A record of its own follows when the first event is specified or gate G2 decides how events are kept." So far only one direction has the means to be tolerant: `membership` "ignores a request that is older than the last one it applied for the same hold" ([ADR 5](0005-no-circle-between-modules.md)). The events themselves carry nothing that would let a consumer tell a repeat from a new fact, or an old fact from a new one.

The review before gate G6 (`docs/reviews/pre-g6-context-cut.md`, F1, F2, F3, F5) played the cases through:

* *Book Returned* reaches `fees` twice. Without a loan identity, `fees` can only compare copy, reader and due date, and a reader who returns a copy and borrows it again the same day has the same three values twice.
* *Book Returned* arrives after midnight. If `fees` counts the days with its own clock, the reader pays one day more than the desk said. The €10 line is 21 days (21 × €0.50 = €10.50), so one day decides the hold.
* *Card Blocked* and *Card Unblocked* arrive in reverse order. `lending` keeps "blocked" with no way to know it is wrong.
* The Head of Collection releases a damaged copy, it is damaged again, and the first release arrives late. `lending` cannot tell which damage the release answers.
* An event or an order names a copy that the receiver does not know yet.

The phase 5 flows (chapter 7) will specify every event that crosses a boundary. What must every one of them carry, and what does a consumer do with it?

## Decision Drivers

* Tolerance of repeated and late events is already a rule (ADR 4); it needs the information to be possible.
* What is missing from an event on the first day cannot be added later without reading old events again (ADR 4: an event is "changed only by adding to it").
* Business rules count in business time: the day a book came back, not the day the message arrived (C-03, C-28).
* One rule for all events is cheaper to model, build and check than one per context.
* The technology of delivery is decided at gate G2 and stays out of this record.

## Considered Options

1. One rule for every published event: subject identity, business time and order per subject
2. Identity by natural keys, no order
3. Leave it to each context in phase 5

## Decision Outcome

Recommended option: "One rule for every published event: subject identity, business time and order per subject", because it is the smallest rule that makes every case above decidable, and it costs a few fields that are cheap now and expensive later.

Every event a module publishes carries:

* **an event identifier**, unique, so a consumer can recognise a repeat and apply each event at most once;
* **the identity of its subject**, issued by the owner (ADR 7): the member, the copy, the title, and, new, **the loan**, issued by `lending` when a copy is checked out; a damage report and a hold are subjects with an identity of their own where they can recur;
* **the business time of the fact**: the date or moment it happened in the business ("returned on", "declared lost on", "decided at"), not the moment it was sent;
* **its place in order for its subject**: a number that grows with each event about the same subject from the same publisher. A consumer ignores an event that is older than the last one it applied for that subject, as ADR 5 does for holds.

And every consumer follows two rules:

* **An event about a subject the consumer does not know yet** is held back and tried again later. Nothing is assumed: an unknown copy is not treated as circulating, and a checkout of a copy without a known usage-fee mark is not treated as free.
* **An order or a desk action about a subject the module does not know** is refused with a clear reason ("copy not known yet"). Staff can try again.

Validity that the business states as a duration (a card valid for a year, researcher status for twelve months) travels as a **date** in the event that grants or renews it, and the consumer compares it with today (C-28). The event that reports the end is information, not the trigger of the rule.

Not decided here: the field names, the format of the identifiers, how the order number is produced, and how events are delivered and stored (gate G2).

### Consequences

* Good, because each case of the review has an answer: a repeated *Returned* is recognised by its identifier; the late fine counts to the day of the return; a late *Card Unblocked* is not overtaken by an older *Card Blocked*; a release that is older than the latest damage report does not make the copy lendable; an unknown copy is never lent by default.
* Good, because it is one rule the phase 5 flows and the `check-model-code` step can check for every event.
* Bad, because every event gets four fields, and every consumer keeps, per subject, the last order number it applied.
* Bad, because "hold back and try again" needs a place to park events. How long, and what happens when a subject never appears, is decided with the delivery at gate G2.
* Neutral, because ADR 7 gains one identifier (the loan) that it did not list; the rule of ADR 7, "the owner issues it", stays.

## Pros and Cons of the Options

### One rule for every published event: subject identity, business time and order per subject

* Good, because it solves repeats, lateness and reordering in one place, in every context.
* Good, because it matches what ADR 5 already does for holds.
* Bad, because it adds fields and a little state to every consumer, also where a context could have done with less.

### Identity by natural keys, no order

The consumer recognises a fact by the values it carries (copy, reader, due date).

* Good, because the events stay small.
* Bad, because natural keys are not unique (the same copy borrowed twice on one day) and cannot express order (blocked, then unblocked).

### Leave it to each context in phase 5

* Good, because each context takes only what it needs.
* Bad, because the same question is answered four times, possibly four ways, and the first event without the information is fixed for good once it has been published.
