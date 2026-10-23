# Chapter 4 — Deployment decision

**Input:** [the brief](../requirements/brief.md), [chapter 3](03-strategic-design.md)
**Tool:** architecture decision records (ADRs) after Michael Nygard, plain Markdown
**Result:** eight records in [`docs/adr/`](../docs/adr/README.md). All eight are accepted: ADR 5 after a second round, the others in the review of this chapter. One new business decision (C-19) and a turned arrow on the context map.

## Why decide now

Chapter 3 cut the library into four bounded contexts. A cut on paper costs nothing. It starts to cost when it meets the code: how many programs do we run, and what stops one context from reaching into another? These decisions are architectural, they are expensive to change later, and they follow from the context map. That is why they come here, before any context is modelled in detail.

We write each decision as an **architecture decision record** in the form Michael Nygard proposed in 2011: a title, a status, the *context* (the forces, including the alternatives that lost), the *decision* in plain sentences ("We will …"), and the *consequences*, good and bad. The first record ([ADR 1](../docs/adr/0001-record-architecture-decisions.md)) is the decision to keep such records at all. A short record that says *why* is worth more than a diagram that says only *what*.

What we do **not** decide here is technology: language version, framework, database, how events are stored, the user interface. That is a decision of its own (gate G2) and must not sneak in through the back door. The records say what a technology has to provide, not which one it is.

## The decisions

| ADR | Decision | Because |
|---|---|---|
| [1](../docs/adr/0001-record-architecture-decisions.md) | Record architecture decisions | Later chapters build on these decisions and need to know why. |
| [2](../docs/adr/0002-one-deployable-unit.md) | One application, a modular monolith | The IT contact asks for it ("One application to run, please, not a zoo of services"), the team is small, the contexts are coupled by the business flow. |
| [3](../docs/adr/0003-one-module-per-bounded-context.md) | One module per context; other modules may use only its public API | Inside one process the boundary exists only if something checks it. |
| [4](../docs/adr/0004-contexts-talk-through-published-events.md) | Facts travel as events, orders go through the owner's API, every module owns its data | This is what the mappings of chapter 3 look like in code. |
| [5](../docs/adr/0005-no-circle-between-modules.md) | Fees holds a card through membership, so the modules form no circle | The €10 rule belongs to fees (C-19); see below. |
| [6](../docs/adr/0006-adapters-and-clock-inside-the-module.md) | External systems and the daily checks sit inside the module that owns the rule | The anti-corruption layers of chapter 3 need a place; the clock must not know the rules. |
| [7](../docs/adr/0007-identifiers-across-contexts.md) | Identifiers are issued by the owning module; a member is not their card | A card expires, is renewed and can be blocked; the person stays the same. |
| [8](../docs/adr/0008-user-interfaces-outside-the-modules.md) | User interfaces sit outside the modules and only ask them | The reader's account page needs two contexts; neither should learn about the other. |

ADR 4 has a table that translates the patterns of the context map into code: an open host service with a published language becomes public events, customer-supplier becomes the supplier's interface (events or orders), an anti-corruption layer becomes an adapter inside the downstream module.

## A mistake from chapter 3

At the end of chapter 3 we wrote that the circle lending → fees → membership → lending was harmless because every arrow is a published event. Writing ADR 3 showed that this was wrong. A module that reacts to an event has to know the event's type, so it depends on the module that publishes it. As dependencies the three contexts form a circle, and a circle means that none of them can be built, tested or later pulled out without the other two. A boundary check that forbids circles, which is what ADR 3 asks for, would fail.

We found it here and not in chapter 3 because chapter 3 looked at the direction of the *messages* and not at who needs whose *types*. The check script of this repository now reads the context map and warns about a circle; it reported this one until the map was changed (see below).

### Ways out, and a second mistake

The first version of ADR 5 looked for the arrow that was easiest to turn. The rule "above €10 block the card" was already drawn in the `fees` area, so `fees` would give block and unblock orders and `membership` would carry them out. The circle would be gone.

The review with the maintainer found two problems. First, the argument ran the wrong way round: a technical constraint (no circle) decided who owns a business rule. In DDD the owner comes first, and the structure follows. Second, an "unblock" order cannot tell whose block it lifts. The brief knows no other reason to block (C-01), but as soon as there is one, say a block by hand from the Membership Officer, a payment would undo it, and `fees` would be in charge of the card, which is the business of `membership`.

So we went back to the business question: **whose rule is the €10 block?** The brief says "we block", not who "we" is. Today the Membership Officer does it by hand, but that says who does the work, not whose rule it is. The question went into the clarification log as C-19. The decision: the rule belongs to the finance side, because its purpose is that books come back and fees are paid.

From that the design follows:

- `membership` owns the card and keeps a list of **holds**. Each hold has a reason and the party that placed it. A card with at least one hold is blocked, and only the party that placed a hold lifts it.
- `fees` decides when a reader is **in arrears** (amount owed above €10). It then places the hold "unpaid fees" and lifts it at €10 or less.
- `membership` no longer knows anything about money. "Amount owed" left its glossary, and "hold" came in.
- The arrow between the two turns around: `membership` is the supplier, `fees` the customer. The circle is gone, and this time for a business reason.

ADR 5 keeps the rejected options with their reasons: plain block orders, `membership` owning the rule with each module's language as a separate artefact (the fallback if a circle ever appears that no business argument resolves), merging the two contexts, a shared module for all events, and living with the circle.

The context map in Studio, both glossaries, the mapping and chapter 3 are updated. The check script no longer reports a circle.

> **Challenging the cut.** Both mistakes were found late, so before anything is built on the cut we added a skill that challenges it: [`challenge-context-cut`](../.claude/skills/challenge-context-cut/SKILL.md). A fresh agent, which knows only the files, reads the contexts, glossaries and the map through six lenses (purpose, language, owner of each rule, dependencies, scenarios, patterns) and reports findings with evidence and alternatives. It changes nothing; the maintainer decides. Run on the state at the end of chapter 3, it found the circle, the missing owner of the €10 rule, the money word in `membership` and the unblock that lifts someone else's block. Run on the state after this chapter, it found seven open points, among them a board that still shows the rejected block orders. The [reports and the limits of this test](../docs/reviews/README.md) are in `docs/reviews/`.

## What we take with us

- The four modules and their allowed dependencies are known. The order is: `catalogue` and `membership` first, then `lending`, then `fees`.
- Deferred: a rule for changing published events (ADR 4 says only add, a record follows with the first event). Still open and deliberately not decided here: the mail gateway (its interface is not in the brief) and everything technical (gate G2).
- **Gate G1 (spec-driven development) comes next.** Before any context is modelled in detail, we have to agree how DDD Studio and the specification tool work together. Nothing in the next chapters starts before that.

## Decisions in this chapter

- **Business**, decided by the maintainer playing the library: C-19, the €10 rule belongs to the finance side. Recorded in the [clarification log](../requirements/clarifications.md), with the rejected option.
- **Architecture:** [ADR 5](../docs/adr/0005-no-circle-between-modules.md) accepted by the maintainer: fees places a hold, membership owns the card, the arrow turns around. Its first version (plain block orders, argued from the circle alone) was rejected and is kept in the record. ADRs 1 to 4 and 6 to 8 accepted by the maintainer in the review of this chapter (2026-10-23).
- **Way of working:** a decision that moves a business rule between contexts starts with the business question (whose rule is it?), not with the technical structure. Gate G1 is next. It is a decision of the maintainer, prepared by the agent, and nothing per context starts before it.
