# 5. No circle between modules: fees drives membership

Date: 2026-10-23

## Status

Proposed

## Context

Chapter 3 drew these relations, upstream to downstream: `catalogue` → `lending`, `catalogue` → `fees`, `membership` → `lending`, `lending` → `fees`, `fees` → `membership`. It said the circle `lending` → `fees` → `membership` → `lending` was harmless because every arrow is an event.

That was too optimistic. A module that reacts to an event has to know the event's type, so it depends on the publishing module's API. Seen as dependencies, three modules form a circle: `lending` uses `membership`, `membership` uses `fees`, `fees` uses `lending`. ADR 3 forbids that. A circle also means that none of the three can be built, tested or later separated without the other two.

We considered four ways out:

1. **Reverse one arrow: `fees` drives `membership`.** The rule that a card is blocked when the member owes more than €10 already sits in `fees` on the board (chapter 3), because the amounts are known there. `membership` offers a small API: block a card, lift a block. `fees` gives the order when the amount owed passes €10 or is back at €10 or less.
2. **Merge `fees` and `membership`** into one module. No circle, but two deciders and two vocabularies in one model, which chapter 3 rejected.
3. **Move the event types into a common module.** No circle in the build, but the common module is a shared kernel (rejected in chapter 3), and every change to an event touches all its users.
4. **Accept the circle** and exempt the three modules from the check. These are the modules that interact most (a loan ends, a fine arises, a card is blocked), so the check would stop protecting exactly where the boundaries are crossed most.

## Decision

We will take option 1. `fees` decides when a card has to be blocked or unblocked and gives the order; `membership` decides what a blocked card is (nothing new may be borrowed or reserved) and carries it out. The mapping between the two turns around: `membership` becomes the supplier, `fees` the customer.

An order states the wanted result (blocked or not blocked) and the time of the decision. `membership` ignores an order that is older than the last one it applied, so a late "lift" cannot undo a newer "block".

The allowed dependencies are then:

- `catalogue` and `membership` use no other module,
- `lending` uses `catalogue` and `membership`,
- `fees` uses `catalogue`, `membership` and `lending`.

## Consequences

- The build has no circle; the boundary check stays on everywhere.
- The context map in Studio, the glossary of `membership` (it says what a blocked card is, no longer why), the fees/membership row in chapter 3 and the exported model change with this decision.
- `membership` is upstream of two modules. It must keep its API small and stable.
- The block is the one call between modules the design needs. It is acceptable because it is an order and not a question, and `fees` does not need the answer to finish its own work: it gives the order after it has updated the amount owed (a charge, a payment, a waiver, or the daily running amount, C-03).
- Orders can be repeated and can arrive late; the rule on the time of the decision makes that harmless.
- `fees` remains a consumer of loan events. What is new is that it also gives orders to a module upstream of it.
