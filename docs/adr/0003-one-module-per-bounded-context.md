---
status: "accepted"
date: 2026-10-23
decision-makers: the maintainer
consulted: none recorded
informed: none recorded
---

# 3. One module per bounded context, public API only

## Context and Problem Statement

ADR 2 puts four bounded contexts into one application. Inside one process nothing stops code in `fees` from using a type of `lending`. The boundary from chapter 3 is a promise about language and ownership; without a rule it is only a drawing.

What stops one context from reaching into another inside one application?

## Decision Drivers

* Inside one process nothing stops code in `fees` from using a type of `lending`.
* The boundary from chapter 3 is a promise about language and ownership. Without a rule it is only a drawing.
* Words that mean different things in different contexts (*copy* in catalogue and lending) must keep their own meaning.
* Boundaries that nobody checks do not survive the first deadline.

## Considered Options

* Shared domain types
* Boundaries by convention only
* One module per bounded context, public API only

## Decision Outcome

Chosen option: "One module per bounded context, public API only", because a boundary that the build checks holds where a shared type or an agreement does not.

We will make each bounded context one module with the context's name: `catalogue`, `lending`, `membership`, `fees`.

* A module has a **public API** (orders it accepts, questions it answers, events it publishes) and an **inside**. Other modules may use only the public API.
* The build fails when a module uses another module's inside, or when modules depend on each other in a circle (ADR 5).
* The words inside a module are the words of its glossary. Two modules may use the same word for different things; they never share the type.

### Consequences

* Good, because the module tree mirrors the context map. A reader of the code sees the same four names as a reader of the tutorial.
* Bad, because we need a check that runs with the tests. Which tool does it is decided at gate G2.
* Bad, because code that would be convenient to share has to be published as part of an API or duplicated. That is the price of the boundary.

### Confirmation

The build fails when a module uses another module's inside, or when modules depend on each other in a circle. The check runs with the tests; which tool does it is decided at gate G2.

## Pros and Cons of the Options

### Shared domain types

One `Reader`, one `Copy` for everybody.

* Bad, because it is the shared kernel chapter 3 rejected: it ties teams together that decide independently.
* Bad, because it would force one meaning on words that mean different things in different contexts (*copy* in catalogue and lending).

### Boundaries by convention only

* Bad, because boundaries that nobody checks do not survive the first deadline.

### One module per bounded context, public API only

* Good, because the boundary from chapter 3 becomes a rule that the build checks.
* Good, because each module keeps the words of its own glossary.
* Bad, because shared code has to be published as part of an API or duplicated.
