# 3. One module per bounded context, public API only

Date: 2026-10-23

## Status

Accepted

## Context

ADR 2 puts four bounded contexts into one application. Inside one process nothing stops code in `fees` from using a type of `lending`. The boundary from chapter 3 is a promise about language and ownership; without a rule it is only a drawing.

We considered shared domain types (one `Reader`, one `Copy` for everybody). That is the shared kernel chapter 3 rejected, because it ties teams together that decide independently. It would also force one meaning on words that mean different things in different contexts (*copy* in catalogue and lending). We also considered agreeing on boundaries by convention only; boundaries that nobody checks do not survive the first deadline.

## Decision

We will make each bounded context one module with the context's name: `catalogue`, `lending`, `membership`, `fees`.

- A module has a **public API** (orders it accepts, questions it answers, events it publishes) and an **inside**. Other modules may use only the public API.
- The build fails when a module uses another module's inside, or when modules depend on each other in a circle (ADR 5).
- The words inside a module are the words of its glossary. Two modules may use the same word for different things; they never share the type.

## Consequences

- The module tree mirrors the context map. A reader of the code sees the same four names as a reader of the tutorial.
- We need a check that runs with the tests. Which tool does it is decided at gate G2.
- Code that would be convenient to share has to be published as part of an API or duplicated. That is the price of the boundary.
