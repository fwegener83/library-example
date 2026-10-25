---
status: "proposed"
date: 2026-10-25
decision-makers: the maintainer
consulted: none recorded
informed: none recorded
---

# 10. Front ends use the modules through REST; between modules there is no REST

## Context and Problem Statement

[ADR 8](0008-user-interfaces-outside-the-modules.md) keeps the user interfaces outside the four modules and lets a page use the public API of any module. It leaves open how a page asks: "Depending on that choice, 'asking a module' may be a call inside the application or a request from a browser; the rule is the same." [ADR 4](0004-contexts-talk-through-published-events.md) fixes how modules talk to each other (events and orders) but says nothing about the way in from outside.

The brief asks for a screen at the desk for staff and a page for readers (§3.6). The plan first assumed Thymeleaf and htmx, that is pages rendered on the server. On 2026-10-25 the maintainer asked for REST for every front end instead; [the phase model of gate G1](../gates/g1-model-to-code.md) builds on it (principle 5, "REST at the edges, events inside"). This record writes the decision down with its reasons and what it rules out.

How do the front ends reach the modules, and does REST have a place between the modules?

## Decision Drivers

* The staff screen and the reader's page are two front ends for the same modules. A further client is not in the brief, but if one comes, it needs the same contract.
* A front end in other technology needs a contract that does not depend on Java.
* The model in DDD Studio holds commands, queries and read models per context. The contract towards the front end should come from it, not from the code (G1).
* Inside one process, a call over HTTP between modules costs availability and gains nothing (ADR 2, ADR 4).
* The user interface contains no business rules (ADR 8), whatever the technology.

## Considered Options

1. REST at the edges: every front end uses the modules through REST, and the modules do not use REST between them
2. Server-rendered pages (Thymeleaf and htmx) that call the modules inside the application
3. REST between the modules as well

## Decision Outcome

Recommended option: "REST at the edges: every front end uses the modules through REST, and the modules do not use REST between them", because it gives every front end the same language-neutral contract, derived from the model, and keeps the modules free of HTTP between each other.

* **Endpoints sit inside each module** as its web adapter, in the same way as the adapters to external systems (ADR 6). The commands, queries and read models of the module become its REST resources. The module's public API (ADR 3) stays what other modules use; REST is how the world outside the application uses it.
* **API first.** The OpenAPI specification of a module is written before its code, derived from the commands, queries and read models in DDD Studio, and the code is tested against it. The code does not generate the contract.
* **The front end composes.** A page may put the answers of several modules on one page (ADR 8) by calling several APIs. If a page needs too many calls, a backend for frontend is the way out; it is not a fifth module with business rules.
* **Between modules, nothing changes.** Facts travel as events and orders go through the owner's public API (ADR 4). Payload schemas in the model are the contract there. AsyncAPI or OpenAPI for them are worth their cost only when a module is pulled out of the application.
* **Not decided here:** the technology of the front end (gate G2; it is a separate client, but which one is open), authentication and authorisation, the style of the API versions, and the format of errors. Each is decided when the first API is modelled or at G2.

### Consequences

* Good, because the staff screen, the reader's page and any later client use one contract that does not depend on the language of the backend.
* Good, because the contract comes from the model, so a gap in the model shows up before code exists.
* Good, because ADR 8 gets its answer: asking a module from a page is a request over REST.
* Bad, because a second artefact, the OpenAPI specification, has to be kept in line with the model. We accept it here because the consumer is a front end in other technology.
* Bad, because a separate front end is more work than server-rendered pages: its own build, its own tests, calls over the network. For two small screens, option 2 would be cheaper on day one.
* Neutral, because the reader's page may need several calls. A backend for frontend stays open if that becomes slow or complex.
* Neutral, because what a reader may see of their own data and what staff may do is a question for each module and for G2.

## Pros and Cons of the Options

### REST at the edges: every front end uses the modules through REST, and the modules do not use REST between them

* Good, because every front end has the same contract, written before the code.
* Good, because it keeps the rules of ADR 4 intact: inside the application, events and orders.
* Bad, because the contract is one more artefact and the front end a separate piece of software.

### Server-rendered pages (Thymeleaf and htmx) that call the modules inside the application

* Good, because it is the cheapest for two small screens: one build, no separate client, no contract to write.
* Good, because the pages call the modules in the same process.
* Bad, because the contract with the front end is then the Java interfaces and the templates. A second client, such as an app, would need REST anyway.
* Bad, because the maintainer asked for REST for every front end (2026-10-25), and the tutorial is meant to show an API-first way of working.

### REST between the modules as well

* Good, because one style is used everywhere.
* Bad, because inside one process a call over HTTP gives nothing and adds failure modes, which ADR 4 wants to avoid.
* Bad, because it makes pulling modules apart look easier than it is: the failure handling would still be missing (ADR 2).
