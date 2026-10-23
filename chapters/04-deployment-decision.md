# Chapter 4 — Deployment decision

**Input:** [the brief](../requirements/brief.md), [chapter 3](03-strategic-design.md)
**Tool:** architecture decision records (ADRs) after Michael Nygard, plain Markdown
**Result:** eight proposed records in [`docs/adr/`](../docs/adr/README.md). None is accepted yet; the review of this chapter is the decision. ADR 5 needs a choice between options.

## Why decide now

Chapter 3 cut the library into four bounded contexts. A cut on paper costs nothing. It starts to cost when it meets the code: how many programs do we run, and what stops one context from reaching into another? These decisions are architectural, they are expensive to change later, and they follow from the context map. That is why they come here, before any context is modelled in detail.

We write each decision as an **architecture decision record** in the form Michael Nygard proposed in 2011: a title, a status, the *context* (the forces, including the alternatives that lost), the *decision* in plain sentences ("We will …"), and the *consequences*, good and bad. The first record ([ADR 1](../docs/adr/0001-record-architecture-decisions.md)) is the decision to keep such records at all. A short record that says *why* is worth more than a diagram that says only *what*.

What we do **not** decide here is technology: language version, framework, database, how events are stored, the user interface. That is a decision of its own (gate G2) and must not sneak in through the back door. The records say what a technology has to provide, not which one it is.

## The decisions (all proposed)

| ADR | Decision | Because |
|---|---|---|
| [1](../docs/adr/0001-record-architecture-decisions.md) | Record architecture decisions | Later chapters build on these decisions and need to know why. |
| [2](../docs/adr/0002-one-deployable-unit.md) | One application, a modular monolith | The IT contact asks for it ("One application to run, please, not a zoo of services"), the team is small, the contexts are coupled by the business flow. |
| [3](../docs/adr/0003-one-module-per-bounded-context.md) | One module per context; other modules may use only its public API | Inside one process the boundary exists only if something checks it. |
| [4](../docs/adr/0004-contexts-talk-through-published-events.md) | Facts travel as events, orders go through the owner's API, every module owns its data | This is what the mappings of chapter 3 look like in code. |
| [5](../docs/adr/0005-no-circle-between-modules.md) | No circle between modules; fees drives membership (**needs a choice**) | See below. |
| [6](../docs/adr/0006-adapters-and-clock-inside-the-module.md) | External systems and the daily checks sit inside the module that owns the rule | The anti-corruption layers of chapter 3 need a place; the clock must not know the rules. |
| [7](../docs/adr/0007-identifiers-across-contexts.md) | Identifiers are issued by the owning module; a member is not their card | A card expires, is renewed and can be blocked; the person stays the same. |
| [8](../docs/adr/0008-user-interfaces-outside-the-modules.md) | User interfaces sit outside the modules and only ask them | The reader's account page needs two contexts; neither should learn about the other. |

ADR 4 has a table that translates the patterns of the context map into code: an open host service with a published language becomes public events, customer-supplier becomes the supplier's interface (events or orders), an anti-corruption layer becomes an adapter inside the downstream module.

## A mistake from chapter 3

At the end of chapter 3 we wrote that the circle lending → fees → membership → lending was harmless because every arrow is a published event. Writing ADR 3 showed that this was wrong. A module that reacts to an event has to know the event's type, so it depends on the module that publishes it. As dependencies the three contexts form a circle, and a circle means that none of them can be built, tested or later pulled out without the other two. A boundary check that forbids circles, which is what ADR 3 asks for, would fail.

We found it here and not in chapter 3 because chapter 3 looked at the direction of the *messages* and not at who needs whose *types*. The check script of this repository now reads the context map and warns about a circle; it reports this one until the map is changed.

### Ways out

ADR 5 lists four. The recommended one is small and fits what we already drew: the rule "above €10 block the card" sits in `fees` on the board, because the amounts are known there. So `fees` should give the order, and `membership` should carry it out. `membership` then offers "block this card" and "lift the block", and no longer knows about fines. The arrow between the two on the context map turns around: `membership` becomes the supplier, `fees` the customer. Merging the two contexts or moving the event types into a shared module would remove the circle too, but they undo decisions of chapter 3 (different deciders, no shared kernel).

This changes the arrow on the context map, the glossary of `membership` (it no longer says *why* a card is blocked), the table row in chapter 3 and one mapping. One thing is already corrected, whatever the decision: the mapping's description no longer calls the circle harmless. The rest we have not done yet: **the maintainer decides first**, then the Studio model and chapter 3 are updated in this pull request.

## What we take with us

- The four modules and their allowed dependencies are known, once the records are accepted and ADR 5 is decided. The order is: `catalogue` and `membership` first, then `lending`, then `fees`.
- Deferred: a rule for changing published events (ADR 4 says only add, a record follows with the first event). Still open and deliberately not decided here: the mail gateway (its interface is not in the brief) and everything technical (gate G2).
- **Gate G1 (spec-driven development) comes next.** Before any context is modelled in detail, we have to agree how DDD Studio and the specification tool work together. Nothing in the next chapters starts before that.
