# 5. Fees holds a card through membership, so the modules form no circle

Date: 2026-10-23

## Status

Accepted

## Context

**The business question.** The brief says "We block a card when someone owes more than €10 in fines … When they pay, we unblock." The rule links two contexts: the reason is money, which is the business of `fees`; the effect is on the card, which is the business of `membership`. Whoever owns the rule holds the policy, and the dependency between the two modules follows from it. The brief does not say whose rule it is, so we asked. C-19 decided that it belongs to the finance side: its purpose is that books come back and fees are paid.

**The technical problem.** Chapter 3 drew, upstream to downstream: `catalogue` → `lending`, `catalogue` → `fees`, `membership` → `lending`, `lending` → `fees`, `fees` → `membership`. It called the circle `lending` → `fees` → `membership` → `lending` harmless because every arrow is an event. That was wrong. A module that reacts to an event has to know the event's type, so it depends on the publishing module. As dependencies the three modules form a circle, which ADR 3 forbids: none of them could be built, tested or later separated without the other two. A circle in the *flow* is normal: fees lead to a block, a block stops loans, loans lead to fees. Only a circle in the *dependencies* is the problem.

**Order of the argument.** The first version of this record argued from the circle alone and picked the arrow that was easiest to turn. That lets the technical structure decide who owns a business rule. This version decides the owner first (C-19) and then checks that the result has no circle.

The options we considered:

1. **`fees` places a hold on the card.** `membership` owns the card and keeps a list of *holds*, each with the party that placed it. A card with at least one hold is blocked. `fees` places the hold "unpaid fees" when the amount owed passes €10 and lifts it when the amount owed is €10 or less again. Nobody lifts a hold placed by someone else.
2. **`fees` gives plain block and unblock orders.** This was the first version of this record. It was rejected because an unblock order cannot tell whose block it lifts. A payment would undo a block the Membership Officer set for another reason. And "fees blocks the card" puts fees in charge of something that is the business of membership.
3. **`membership` owns the rule; each module publishes its language as a separate artefact.** `fees` reports the amount owed, and `membership` holds the €10 threshold. The build has no circle as long as every module depends only on the published contracts of the others, never on the modules themselves. Rejected because C-19 gave the rule to the finance side, and because `membership` would have to understand amounts of money. It stays the fallback if a real circle ever appears that no business argument resolves.
4. **Merge `fees` and `membership`.** No circle, but two deciders and two vocabularies in one model, which chapter 3 rejected.
5. **One common module for all event types.** That is a shared kernel (rejected in chapter 3), and every change to an event touches all of its users.
6. **Accept the circle** and exempt the three modules from the check. They are the modules that interact most, so the check would stop protecting exactly where the boundaries are crossed most.

## Decision

We will take option 1.

- `membership` decides what a card is and when it may be used. It offers "place a hold" and "lift a hold". A hold carries its reason, the party that placed it and the time of the decision. A card with at least one hold is blocked: nothing new may be borrowed or reserved. `membership` publishes when a card becomes blocked or unblocked.
- `fees` decides when a reader is *in arrears* (amount owed above €10, C-01, C-03, C-18). It then places the hold "unpaid fees" and lifts it when the amount owed is €10 or less.
- Only the party that placed a hold may lift it. `membership` ignores a request that is older than the last one it applied for the same hold, so a late "lift" cannot undo a newer "place".
- The mapping turns around: `membership` is the supplier, `fees` the customer.

The allowed dependencies are then:

- `catalogue` and `membership` use no other module,
- `lending` uses `catalogue` and `membership`,
- `fees` uses `catalogue`, `membership` and `lending`.

## Consequences

- The build has no circle, and the boundary check stays on everywhere.
- `membership` knows nothing about money. "Amount owed" is gone from its glossary; "hold" is new. `fees` has the new word "arrears".
- In the first release there is one kind of hold, "unpaid fees". Other reasons are not in the brief (C-01). The concept costs one list on the card, and a second reason (say a manual one) can be added without touching `fees`.
- `lending` keeps asking only "is the card blocked?". It does not learn why.
- `membership` is upstream of two modules. It must keep its interface small and stable.
- This is the one call between modules the design needs. It is acceptable because `fees` does not need an answer to finish its own work: it places or lifts the hold after it has updated the amount owed (a charge, a payment, a waiver, or the daily running amount, C-03). Requests can be repeated and can arrive late; the rule on the time of the decision makes that harmless.
- On the Big Picture board the block and unblock policies already sit in the `fees` area. The events *Card Blocked* and *Card Unblocked* stay as they are; the hold is modelled when `membership` is modelled.
