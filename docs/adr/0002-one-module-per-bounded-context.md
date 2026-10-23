# ADR-0002: One module per bounded context, public API only

**Status:** proposed · **Date:** 2026-10-23

## Context

ADR-0001 puts four bounded contexts into one application. Inside one process, nothing stops code in `fees` from using a class of `lending`. The boundary from chapter 3 is a promise about language and ownership; without a rule it is only a drawing.

## Decision

- Each bounded context is **one module** with the context's name: `catalogue`, `lending`, `membership`, `fees`.
- A module has a **public API** (commands it accepts, queries it answers, events it publishes) and an **inside**. Only the public API may be used by other modules.
- The build fails when a module uses another module's inside, or when modules depend on each other in a circle (ADR-0004).
- Words inside a module are the words of its glossary. Two modules may use the same word for different things (*copy*), they never share the type.

## Alternatives we rejected

- **Shared domain classes** (a common `Reader`, a common `Copy`). It is the shared kernel from chapter 3, rejected there.
- **Agreement by convention only.** Boundaries that nobody checks do not survive the first deadline.

## Consequences

- The module tree mirrors the context map; a reader of the code sees the same four names as a reader of the tutorial.
- We need a check that runs with the tests. Which tool does it is part of gate G2; the plan proposes Spring Modulith's module verification.
- Code that would be convenient to share has to be published as part of an API or duplicated. That is the price of the boundary.
