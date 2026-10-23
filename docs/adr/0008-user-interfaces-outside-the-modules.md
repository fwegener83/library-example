# 8. User interfaces sit outside the modules and use only public APIs

Date: 2026-10-23

## Status

Proposed

## Context

The brief asks for "a simple screen at the desk" for staff and "a simple page" for readers (§3.6). The reader's page shows "what they have at home, what's waiting for them, what they owe" (§2). That page needs data from two contexts: loans and reservations from `lending`, the amount owed from `fees`. Chapter 3 decided not to make it a context of its own and left open where it lives; this record decides it.

We considered three places for such a page:

1. A **read model inside one of the modules** (for example `lending` also keeps the amounts owed). It gives one module knowledge that belongs to another.
2. A **separate view module** that listens to the events of `lending` and `fees` and keeps its own copy. It works, but adds a fifth module that has no vocabulary of its own and has to follow every change of two others.
3. A **user interface outside the modules** that asks both modules through their public APIs and puts the answers on one page.

## Decision

We will keep the user interfaces outside the four modules. A page may use the public API of any module (ADR 3) and may put the answers of several modules on one page. The user interfaces may depend on every module; no module depends on a user interface. It contains no business rules: a page never decides whether a reservation is allowed, it asks the module that decides.

The technology of the user interface is decided at gate G2. Depending on that choice, "asking a module" may be a call inside the application or a request from a browser; the rule is the same.

## Consequences

- The reader's account page asks `lending` and `fees` and shows both answers. Neither module learns about the other.
- The modules need public questions (queries) for what the pages show, not only orders and events. Each such question is part of a module's API and is shaped by what the page needs.
- If the reader's page becomes slow or complex (many questions per page), option 2 is still open: a view module can be added later without changing the four modules.
- Staff and reader pages are separate users of the same APIs. What a reader may see of their own data is a question for each module.
