---
status: "accepted"
date: 2026-10-23
decision-makers: the maintainer
consulted: none recorded
informed: none recorded
---

# 5. Fees holds a card through membership, so the modules form no circle

## Context and Problem Statement

**The business question.** The brief says "We block a card when someone owes more than €10 in fines … When they pay, we unblock." The rule links two contexts: the reason is money, which is the business of `fees`; the effect is on the card, which is the business of `membership`. Whoever owns the rule holds the policy, and the dependency between the two modules follows from it. The brief does not say whose rule it is, so we asked. C-19 decided that it belongs to the finance side: its purpose is that books come back and fees are paid.

**The technical problem.** Chapter 3 drew, upstream to downstream: `catalogue` → `lending`, `catalogue` → `fees`, `membership` → `lending`, `lending` → `fees`, `fees` → `membership`. It called the circle `lending` → `fees` → `membership` → `lending` harmless because every arrow is an event. That was wrong. A module that reacts to an event has to know the event's type, so it depends on the publishing module. As dependencies the three modules form a circle, which ADR 3 forbids: none of them could be built, tested or later separated without the other two. A circle in the *flow* is normal: fees lead to a block, a block stops loans, loans lead to fees. Only a circle in the *dependencies* is the problem.

Who owns the €10 rule, and how do `fees` and `membership` depend on each other without a circle?

## Decision Drivers

* The owner of the business rule comes first, and the technical structure follows (C-19: the rule belongs to the finance side).
* ADR 3 forbids a circle between modules; none of the three could be built, tested or later separated without the other two.
* An order that lifts a block must not undo a block that someone else placed.
* `membership` is in charge of the card, `fees` of money. Two deciders and two vocabularies in one model were rejected in chapter 3, and so was a shared kernel.

## Considered Options

1. `fees` places a hold on the card
2. `fees` gives plain block and unblock orders
3. `membership` owns the rule; each module publishes its language as a separate artefact
4. Merge `fees` and `membership`
5. One common module for all event types
6. Accept the circle

## Decision Outcome

Chosen option: "`fees` places a hold on the card", because C-19 gave the rule to the finance side, and this option makes `fees` the owner of the rule while `membership` stays in charge of the card, with no circle between the modules.

We will take option 1.

* `membership` decides what a card is and when it may be used. It offers "place a hold" and "lift a hold". A hold carries its reason, the party that placed it and the time of the decision. A card with at least one hold is blocked: nothing new may be borrowed or reserved. `membership` publishes when a card becomes blocked or unblocked.
* `fees` decides when a reader is *in arrears* (amount owed above €10, C-01, C-03, C-18). It then places the hold "unpaid fees" and lifts it when the amount owed is €10 or less.
* Only the party that placed a hold may lift it. `membership` ignores a request that is older than the last one it applied for the same hold, so a late "lift" cannot undo a newer "place".
* The mapping turns around: `membership` is the supplier, `fees` the customer.

The allowed dependencies are then:

* `catalogue` and `membership` use no other module,
* `lending` uses `catalogue` and `membership`,
* `fees` uses `catalogue`, `membership` and `lending`.

### Consequences

* Good, because the build has no circle, and the boundary check stays on everywhere.
* Good, because `membership` knows nothing about money. "Amount owed" is gone from its glossary; "hold" is new. `fees` has the new word "arrears".
* Good, because `lending` keeps asking only "is the card blocked?". It does not learn why.
* Neutral, because in the first release there is one kind of hold, "unpaid fees". Other reasons are not in the brief (C-01). The concept costs one list on the card, and a second reason (say a manual one) can be added without touching `fees`.
* Bad, because `membership` is upstream of two modules. It must keep its interface small and stable.
* Neutral, because this is the one call between modules the design needs. It is acceptable because `fees` does not need an answer to finish its own work: it places or lifts the hold after it has updated the amount owed (a charge, a payment, a waiver, or the daily running amount, C-03). Requests can be repeated and can arrive late; the rule on the time of the decision makes that harmless.
* Neutral, because on the Big Picture board the block and unblock policies already sit in the `fees` area. The events *Card Blocked* and *Card Unblocked* stay as they are; the hold is modelled when `membership` is modelled.

### Confirmation

The check script of the repository reads the context map and warns about a circle (chapter 4); it reported the circle until the map was changed. The boundary check of ADR 3 fails the build on a circle between modules.

## Pros and Cons of the Options

### `fees` places a hold on the card

`membership` owns the card and keeps a list of *holds*, each with the party that placed it. A card with at least one hold is blocked. `fees` places the hold "unpaid fees" when the amount owed passes €10 and lifts it when the amount owed is €10 or less again. Nobody lifts a hold placed by someone else.

* Good, because the owner of the rule is the finance side (C-19), and the structure follows from that.
* Good, because only the party that placed a hold can lift it, so a payment cannot undo a block set for another reason.
* Good, because the modules form no circle.
* Bad, because `membership` is upstream of two modules and must keep its interface small and stable.

### `fees` gives plain block and unblock orders

This was the first version of this record.

* Bad, because an unblock order cannot tell whose block it lifts. A payment would undo a block the Membership Officer set for another reason.
* Bad, because "fees blocks the card" puts fees in charge of something that is the business of membership.

### `membership` owns the rule; each module publishes its language as a separate artefact

`fees` reports the amount owed, and `membership` holds the €10 threshold. The build has no circle as long as every module depends only on the published contracts of the others, never on the modules themselves.

* Bad, because C-19 gave the rule to the finance side.
* Bad, because `membership` would have to understand amounts of money.
* Neutral, because it stays the fallback if a real circle ever appears that no business argument resolves.

### Merge `fees` and `membership`

* Good, because there is no circle.
* Bad, because it puts two deciders and two vocabularies into one model, which chapter 3 rejected.

### One common module for all event types

* Bad, because it is a shared kernel (rejected in chapter 3).
* Bad, because every change to an event touches all of its users.

### Accept the circle

The three modules would be exempt from the check.

* Bad, because they are the modules that interact most, so the check would stop protecting exactly where the boundaries are crossed most.

## More Information

**Order of the argument.** The first version of this record argued from the circle alone and picked the arrow that was easiest to turn (option 2). That lets the technical structure decide who owns a business rule. This version decides the owner first (C-19) and then checks that the result has no circle.
