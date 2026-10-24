---
status: "proposed"
date: 2026-10-23
decision-makers: the maintainer
consulted: none recorded
informed: none recorded
---

# 8. User interfaces sit outside the modules and use only public APIs

## Context and Problem Statement

The brief asks for "a simple screen at the desk" for staff and "a simple page" for readers (§3.6). The reader's page shows "what they have at home, what's waiting for them, what they owe" (§2). That page needs data from two contexts: loans and reservations from `lending`, the amount owed from `fees`. Chapter 3 decided not to make it a context of its own and left open where it lives; this record decides it.

Where does a page live that needs the answers of several modules?

## Decision Drivers

* The reader's page needs data from two contexts: `lending` and `fees`.
* Chapter 3 decided not to make the page a context of its own.
* One module should not get knowledge that belongs to another.
* A page should not need a module of its own that has no vocabulary and follows every change of two others.

## Considered Options

1. A read model inside one of the modules
2. A separate view module
3. A user interface outside the modules

## Decision Outcome

Recommended option: "A user interface outside the modules", because it asks both modules through their public APIs and puts the answers on one page, without giving one module the knowledge of another and without a fifth module.

We will keep the user interfaces outside the four modules. A page may use the public API of any module (ADR 3) and may put the answers of several modules on one page. The user interfaces may depend on every module; no module depends on a user interface. It contains no business rules: a page never decides whether a reservation is allowed, it asks the module that decides.

The technology of the user interface is decided at gate G2. Depending on that choice, "asking a module" may be a call inside the application or a request from a browser; the rule is the same.

### Consequences

* Good, because the reader's account page asks `lending` and `fees` and shows both answers. Neither module learns about the other.
* Bad, because the modules need public questions (queries) for what the pages show, not only orders and events. Each such question is part of a module's API and is shaped by what the page needs.
* Neutral, because if the reader's page becomes slow or complex (many questions per page), option 2 is still open: a view module can be added later without changing the four modules.
* Neutral, because staff and reader pages are separate users of the same APIs. What a reader may see of their own data is a question for each module.

## Pros and Cons of the Options

### A read model inside one of the modules

For example `lending` also keeps the amounts owed.

* Bad, because it gives one module knowledge that belongs to another.

### A separate view module

It listens to the events of `lending` and `fees` and keeps its own copy.

* Good, because it works.
* Bad, because it adds a fifth module that has no vocabulary of its own and has to follow every change of two others.

### A user interface outside the modules

It asks both modules through their public APIs and puts the answers on one page.

* Good, because neither module learns about the other.
* Bad, because the modules need public questions for what the pages show.
