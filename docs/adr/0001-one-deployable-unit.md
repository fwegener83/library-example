# ADR-0001: One deployable unit

**Status:** proposed · **Date:** 2026-10-23

## Context

The city's development team is small, and its IT contact asks for it in so many words: "One application to run, please, not a zoo of services. If parts need to go their own way later, fine — but not on day one." (brief §3.6). The library needs a staff screen at the desk and a page for readers (§3.6), mail goes through the city's gateway only, payments through CityPay.

Chapter 3 gave us four bounded contexts with different owners and different pace, but they are coupled by the business flow: a loan ending triggers a fine, a fine can block a card, a blocked card stops loans.

## Decision

We build and deploy **one application** with one release cycle: a modular monolith. The four contexts are modules inside it (ADR-0002), not services.

## Alternatives we rejected

- **One service per context.** Four deployments, four pipelines and network calls between contexts that change together, for a team that asked for one application. The benefit (independent scaling and release) is not needed: about 18,000 members, four branches.
- **A monolith without internal boundaries.** Cheapest on day one, but the cut from chapter 3 would exist only in the documents and erode with the first shortcut.

## Consequences

- One build, one release, one place to look at when something fails.
- The contexts can still be pulled apart later, but only if the boundaries hold. That is what ADR-0002 and ADR-0003 are for. Splitting out a module then means replacing in-process calls by messages and adding failure handling and retries. The model itself stays.
- The choice of technology for the application stays open (gate G2).
