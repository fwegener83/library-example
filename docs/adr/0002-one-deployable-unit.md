# 2. One deployable unit

Date: 2026-10-23

## Status

Proposed

## Context

The city's development team is small, and its IT contact asks for it in so many words: "One application to run, please, not a zoo of services. If parts need to go their own way later, fine — but not on day one." (brief §3.6). The library needs a staff screen at the desk and a page for readers (§3.6); mail goes through the city's gateway only, payments through CityPay.

Chapter 3 gave us four bounded contexts with different owners and different pace. They are coupled by the business flow: a loan ending triggers a fine, a fine can block a card, a blocked card stops loans.

We considered one service per context. It would mean four deployments, four pipelines and network calls between contexts that are coupled by the business flow, for a team that asked for one application. Its benefits, independent scaling and release, are in our assessment not needed for about 18,000 card holders and four branches; the brief does not ask for them.

We also considered a monolith without internal boundaries. It is cheapest on day one, but the cut from chapter 3 would exist only in documents and erode with the first shortcut.

## Decision

We will build and deploy one application with one release cycle, a modular monolith. The four contexts are modules inside it (ADR 3), not services.

## Consequences

- One build, one release, one place to look when something fails.
- The contexts can be pulled apart later only if the boundaries hold; ADR 3 and ADR 4 are there to make them hold. Splitting out a module then means replacing in-process calls by messages and adding failure handling and retries. The model itself stays.
- All modules share one runtime. A module that misbehaves (memory, a slow job) affects the others.
- The technology of the application stays open (gate G2).
