---
status: "accepted"
date: 2026-10-23
decision-makers: the maintainer
consulted: none recorded
informed: none recorded
---

# 2. One deployable unit

## Context and Problem Statement

The city's development team is small, and its IT contact asks for it in so many words: "One application to run, please, not a zoo of services. If parts need to go their own way later, fine — but not on day one." (brief §3.6). The library needs a staff screen at the desk and a page for readers (§3.6); mail goes through the city's gateway only, payments through CityPay.

Chapter 3 gave us four bounded contexts with different owners and different pace. They are coupled by the business flow: a loan ending triggers a fine, a fine can block a card, a blocked card stops loans.

How many programs do we build and run for the four contexts?

## Decision Drivers

* The IT contact asks for one application (brief §3.6), and the development team is small.
* The contexts are coupled by the business flow.
* The cut from chapter 3 should not exist only in documents.
* Independent scaling and release are not asked for by the brief, for about 18,000 card holders and four branches (our assessment).

## Considered Options

* One service per context
* A monolith without internal boundaries
* One application with one release cycle, a modular monolith

## Decision Outcome

Chosen option: "One application with one release cycle, a modular monolith", because the IT contact asks for one application, the contexts are coupled by the business flow, and the benefits of separate services are in our assessment not needed.

We will build and deploy one application with one release cycle, a modular monolith. The four contexts are modules inside it (ADR 3), not services.

### Consequences

* Good, because there is one build, one release, one place to look when something fails.
* Bad, because the contexts can be pulled apart later only if the boundaries hold; ADR 3 and ADR 4 are there to make them hold. Splitting out a module then means replacing in-process calls by messages and adding failure handling and retries. The model itself stays.
* Bad, because all modules share one runtime. A module that misbehaves (memory, a slow job) affects the others.
* Neutral, because the technology of the application stays open (gate G2).

## Pros and Cons of the Options

### One service per context

* Good, because independent scaling and release are possible. In our assessment they are not needed for about 18,000 card holders and four branches; the brief does not ask for them.
* Bad, because it means four deployments, four pipelines and network calls between contexts that are coupled by the business flow, for a team that asked for one application.

### A monolith without internal boundaries

* Good, because it is cheapest on day one.
* Bad, because the cut from chapter 3 would exist only in documents and erode with the first shortcut.

### One application with one release cycle, a modular monolith

* Good, because it is what the IT contact asks for, and the team is small.
* Good, because the contexts stay modules (ADR 3) and the cut does not exist only in documents.
* Bad, because all modules share one runtime and splitting out a module later has a cost (see Consequences).
