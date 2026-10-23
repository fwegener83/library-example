# ADR-0004: No circle between modules: fees drives membership

**Status:** proposed — **needs the maintainer's decision** · **Date:** 2026-10-23

## Context

Chapter 3 drew these relations (upstream → downstream): `catalogue` → `lending`, `catalogue` → `fees`, `membership` → `lending`, `lending` → `fees`, `fees` → `membership`. We said that the circle `lending` → `fees` → `membership` → `lending` was harmless because every arrow is an event.

That was too optimistic. A downstream module that reacts to an event has to know the event's type, so it depends on the upstream module's public API. Seen as dependencies the three modules form a circle: `lending` uses `membership`, `membership` uses `fees`, `fees` uses `lending`. ADR-0002 forbids exactly that. A circle also means that none of the three can be built, tested or later separated without the other two.

## Options

1. **Reverse one arrow: `fees` drives `membership`.** The rule "above €10 the card is blocked" already sits in `fees` on the board (chapter 3). `membership` offers a small API: block a card, lift a block. `fees` calls it when the amount owed passes €10 or falls back to €10 or less. `membership` no longer knows about fees; it only executes. The mapping `fees` → `membership` turns into `membership` → `fees` (customer-supplier, fees is the customer).
2. **Merge `fees` and `membership`** into one module. No circle, but two deciders and two vocabularies in one model (chapter 3 rejected it).
3. **Move the shared event types into a common module.** No circle in the build, but the common module is a shared kernel (rejected in chapter 3), and every change to an event would touch all its users.
4. **Accept the circle** and exempt these three modules from the boundary check. These are the three modules that change together most often (a loan ends, a fine arises, a card is blocked), so the check would stop protecting exactly where boundaries are crossed most.

## Decision (proposed)

Option 1. The block rule is a decision about money, so it belongs in `fees`. Membership decides what a blocked card is (nothing new may be borrowed or reserved) and carries it out. The dependency order becomes `catalogue` and `membership` first, then `lending`, then `fees`:

- `lending` uses `catalogue` and `membership`
- `fees` uses `catalogue`, `membership` and `lending`
- `membership` uses nobody, `catalogue` uses nobody

## Consequences

- The build has no circle and the boundary check can stay on everywhere.
- The glossary of `membership` stops explaining why a card is blocked (it says only what a blocked card is); `fees` carries the reason. The mapping on the context map and the glossary change with this decision.
- `membership` is now upstream of two modules. It must keep its API small and stable.
- A block is an order from `fees` to `membership`, not a fact. It is the one call between modules that the design needs, and it is acceptable for three reasons: it is an order and not a question, `fees` does not need the answer to finish its own work, and it is given after `fees` has recorded the charge. Orders can be repeated and can arrive late. So an order states the wanted result (blocked or not blocked) with the time of the decision, and `membership` ignores an order that is older than the last one it applied. A late "lift" must not undo a newer "block".
- Fees is still a downstream consumer of loan events, as in the plan's idea of policies as listeners in the downstream module. What is new is that it also gives orders to a module upstream of it.

## If you decide differently

Option 2 changes chapter 3 (one context fewer). Option 3 gives up the decision against a shared kernel, option 4 gives up the boundary check where it is needed most.
