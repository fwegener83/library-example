---
status: "proposed"
date: 2026-10-26
decision-makers: the maintainer
consulted: none recorded
informed: none recorded
---

# 13. Gaps and repeats: streams that carry the state, a number for every published event, and orders that are remembered

## Context and Problem Statement

[ADR 11](0011-what-every-published-event-carries.md) says that a consumer applies the next number of a subject, ignores a repeat and holds back an event with a gap before it. [ADR 5](0005-no-circle-between-modules.md) says that `membership` ignores an order that is older than the last one it applied for the same hold. The independent review of chapter 7 (`docs/reviews/ch07-flows-and-contracts.md`, F1, F2, F5) played these rules through the flows and found three cases in which they fail, in the direction the chapter had called safe.

1. **A lost renewal hides a block.** The card events of a member are changes (a renewal carries the new end date, a hold carries whether the card is blocked). Number 3, a renewal, is lost; number 4, *hold placed*, arrives and is held back. For as long as the gap lasts `lending` lends to a reader whom `fees` has blocked. The renewal case, a refusal at the desk, is on the safe side; this one is not.
2. **An event that is ignored looks like a gap.** The number counts every event of a subject. A consumer that has no use for one of them (in scenario F, `fees` follows the copy for its usage-fee mark but not its withdrawal) sees a hole and holds everything after it back for good. The same happens when [ADR 12](0012-changing-published-events.md) publishes a replaced fact beside the old one, and ADR 11 does not say whether internal events of the same aggregate take a number.
3. **An order is forgotten when it is undone.** `membership` removes a hold when it is lifted and with it the time of the decision that ADR 5 compares. A repeated "place" of 06:00 that arrives after the "lift" of 07:30 finds no hold to compare with and places it again. `fees` believes the hold is lifted and sends nothing more until the next charge, so the reader stays blocked. Neither ADR 5 nor the chapter says what `fees` does when an order is refused.

What rules close these cases without a technology? The delivery is decided at gate G2.

## Decision Drivers

* The failure of a rule must go in the safe direction: a refusal at the desk is better than a loan to a blocked reader.
* A consumer must be able to ignore an event it does not need without stalling.
* The simplest rule that makes the case decidable; a second numbering is a cost on every context.
* The business rules do not change: the block above EUR 10 (C-19), the dates for card and status (C-28).

## Considered Options

1. State-carrying status events, a number for every published event, orders that remember the last decision
2. Keep ADR 11 and ADR 5 as they are and settle gaps at gate G2
3. Fail closed while there is a gap

## Decision Outcome

Recommended option: "State-carrying status events, a number for every published event, orders that remember the last decision", because it removes the three failures by rules that are local and cheap, and leaves the strict order for the streams where it is needed.

* **State-carrying events.** An event of a *status stream* (the events of `membership` about one member: member registered, researcher status granted, card renewed, hold placed, hold lifted) carries the whole status that `lending` needs: the end date of the card, the end date of researcher status, and whether the card is blocked. The consumer applies an event if its number is higher than the last it applied and ignores it otherwise. It does not hold anything back: a lost event costs nothing as long as a later one arrives. The same holds for `copy corrected`, which already carries all values. The events of a *delta stream* (a loan: checked out, returned, declared lost) keep the strict order of ADR 11, because each one adds something that no later one repeats.
* **A number for every published event of a subject, and none for internal events.** A consumer records the number of every published event it receives for a subject, whether it uses it or not, so that only a lost event leaves a gap. Internal events of the aggregate take no number. A fact published beside another (ADR 12) takes the next number and is received by every consumer of the subject.
* **Orders remember.** `membership` keeps, per member, party and reason, the time of the last decision it applied, also after the hold is lifted. An order with a decision time that is not later than that one is ignored (an equal time counts as already applied). A refused order (member not known yet) is retried by the caller later and shown on a list with its age; it is never dropped silently. The flag that `fees` keeps about its hold is a local belief and is corrected by the next decision, not trusted.

Not decided here: how long an event is held back, how a lost event is detected or requested again, and how events are delivered (gate G2).

### Consequences

* Good, because the case of a lost renewal no longer hides a block: the next event brings the whole status.
* Good, because a consumer may ignore events it does not need.
* Good, because a late repeated order cannot block a reader again.
* Bad, because the status events become larger and carry the same values several times. The Big Picture events *Card Blocked* and *Card Unblocked* are no longer separate in the model; they are two reasons for the same fact (they already are, in chapter 7).
* Bad, because the strict order stays for delta streams, and a lost event there still stops the later events of that subject until it arrives. The held-back list makes it visible; the loss itself is a matter for G2.
* Bad, because `membership` keeps one more small record per party and reason.
* Neutral, because ADR 11 stays accepted and valid for the rule of numbers, repeats and business time; this record adds how gaps are treated for two kinds of stream and what an order remembers. If the maintainer accepts it, ADR 11 and ADR 5 get a line pointing here.

## Pros and Cons of the Options

### State-carrying status events, a number for every published event, orders that remember the last decision

* Good, because each failure is closed by a local rule.
* Good, because it keeps ADR 11 and ADR 5 and extends them.
* Bad, because it asks the owner to say, for each stream, which kind it is.

### Keep ADR 11 and ADR 5 as they are and settle gaps at gate G2

* Good, because it decides nothing before the delivery is known.
* Bad, because the failures do not depend on the delivery: they are in the rules. The first one is a loan to a blocked reader.
* Bad, because chapters 8 and 9 model `lending` and `fees` on these rules.

### Fail closed while there is a gap

While a gap exists for a member, `lending` refuses new loans and reservations for that reader.

* Good, because it is simple and on the safe side.
* Bad, because the cause of a refusal at the desk is a message that is lost somewhere, and the staff cannot see or fix it. The held-back list becomes a list of daily operations.
* Bad, because it solves only the first case.
