# Chapter 4 — Deployment decision

**Input:** [the brief](../requirements/brief.md), [chapter 3](03-strategic-design.md)
**Tool:** architecture decision records (ADRs), plain Markdown
**Result:** five proposed records in [`docs/adr/`](../docs/adr/README.md). None is accepted yet; the review of this chapter is the decision. ADR-0004 needs a choice between options.

## Why decide now

Chapter 3 cut the library into four bounded contexts. A cut on paper costs nothing. It starts to cost when it meets the code: how many programs do we run, and what stops one context from reaching into another? These decisions are architectural, they are expensive to change later, and they follow from the context map. That is why they come here, before any context is modelled in detail.

We write each decision as an **ADR**: status, context, decision, the alternatives we rejected, consequences. A short record that says *why* is worth more than a diagram that says only *what*.

What we do **not** decide here is technology: language version, framework, database, how events are stored, the user interface. That is a decision of its own (gate G2) and must not sneak in through the back door. The records say what a technology has to provide, not which one it is.

## The decisions (all proposed)

| ADR | Decision | Because |
|---|---|---|
| [0001](../docs/adr/0001-one-deployable-unit.md) | One application, a modular monolith | The IT contact asks for it ("One application to run, please, not a zoo of services"), the team is small, the contexts change together. |
| [0002](../docs/adr/0002-one-module-per-bounded-context.md) | One module per context, other modules may use only its public API | Inside one process the boundary exists only if something checks it. |
| [0003](../docs/adr/0003-contexts-talk-through-published-events.md) | Facts travel as events, orders go through the owner's API, every module owns its data | This is what the mappings of chapter 3 look like in code. |
| [0004](../docs/adr/0004-no-circle-between-modules.md) | No circle between modules; fees drives membership (**proposed**) | See below. |
| [0005](../docs/adr/0005-adapters-and-clock-inside-the-module.md) | External systems and the daily checks sit inside the module that owns the rule | The anti-corruption layers from chapter 3 need a place; the clock must not know the rules. |

ADR-0003 has a table that translates the patterns of the context map into code: an open host service with a published language becomes public events, customer-supplier becomes the supplier's API, an anti-corruption layer becomes an adapter inside the downstream module.

## A mistake from chapter 3

At the end of chapter 3 we wrote that the circle lending → fees → membership → lending was harmless because every arrow is a published event. Writing ADR-0002 showed that this was wrong. A module that reacts to an event has to know the event's type, so it depends on the module that publishes it. As dependencies the three contexts form a circle, and a circle means that none of them can be built, tested or later pulled out without the other two. A boundary check that forbids circles, which is what ADR-0002 asks for, would fail.

We found it here and not in chapter 3 because chapter 3 looked at the direction of the *messages* and not at who needs whose *types*. The check script of this repository now reads the context map and warns about a circle; it reports this one until the map is changed.

### Ways out

ADR-0004 lists four. The recommended one is small and fits what we already drew: the rule "above €10 block the card" sits in `fees` on the board, because the amounts are known there. So `fees` should give the order, and `membership` should carry it out. `membership` then offers "block this card" and "lift the block", and no longer knows about fines. The arrow between the two on the context map turns around: `membership` becomes the supplier, `fees` the customer. Merging the two contexts or moving the event types into a shared module would remove the circle too, but they undo decisions of chapter 3 (different deciders, no shared kernel).

This changes the arrow on the context map, the glossary of `membership` (it no longer says *why* a card is blocked), the table row in chapter 3 and one mapping. One thing is already corrected, whatever the decision: the mapping's description no longer calls the circle harmless. The rest we have not done yet: **the maintainer decides first**, then the Studio model and chapter 3 are updated in this pull request.

## What we take with us

- The four modules and their allowed dependencies are known, once the records are accepted and ADR-0004 is decided. The order is: `catalogue` and `membership` first, then `lending`, then `fees`.
- Still open and deliberately not decided here: the mail gateway (its interface is not in the brief), the reader's account view across contexts, and everything technical (gate G2).
- **Gate G1 (spec-driven development) comes next.** Before any context is modelled in detail, we have to agree how DDD Studio and the specification tool work together. Nothing in the next chapters starts before that.
