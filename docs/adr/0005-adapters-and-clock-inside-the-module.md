# ADR-0005: External systems and the clock sit inside the owning module

**Status:** proposed · **Date:** 2026-10-23

## Context

Three external systems appear in the model (chapter 3): the national ISBN service, CityPay and the city mail gateway. Time also acts on the system: reservations run out, loans become overdue, cards and researcher status expire. Today a librarian prints two lists every morning (brief §3.2); on the Big Picture the actor is a *clock*.

## Decision

- **Every external system is reached through one adapter inside the module that owns the relationship**: the ISBN service from `catalogue`, CityPay from `fees`. The adapter is the anti-corruption layer from the context map; no other module sees the external system's types, codes or units (cents, 20-character references).
- **The mail gateway is not decided here.** Its interface is not in the brief and chapter 3 left it without a mapping. We decide when we know what it offers.
- **Time-driven work is a command the module sends itself on a schedule.** The daily checks (expired reservations, overdue loans, expiring cards, running fines) belong to the module that owns the rule. A scheduler outside the modules does not know their rules and must not be asked.

## Alternatives we rejected

- **One integration module for all external systems.** It would end up knowing the vocabulary of every context.
- **A central batch job for all daily work.** Convenient to operate, but it reaches into every module.

## Consequences

- Replacing CityPay or the ISBN service touches one adapter.
- Tests can replace an adapter by a fake.
- The daily checks run at the library's own time and per branch where the rule is per branch (the overdue limit). Which time zone and which hour is a detail for the module.
