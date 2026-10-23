# 6. External systems and the clock sit inside the owning module

Date: 2026-10-23

## Status

Accepted

## Context

Three external systems appear in the model (chapter 3): the national ISBN service, CityPay and the city mail gateway. The mail gateway's interface is not in the brief, and chapter 3 left it without a mapping; this record does not cover it. Time also acts on the system: reservations run out, loans become overdue, cards and researcher status expire. Today a librarian prints two lists every morning (brief §3.2); on the Big Picture the actor is a *clock*.

We considered one integration module for all external systems. It would end up knowing the vocabulary of every context. We also considered one central job for all daily work. It is convenient to operate, but it has to reach into every module and know their rules.

## Decision

We will reach every external system through one adapter inside the module that owns the relationship: the ISBN service from `catalogue`, CityPay from `fees`. The adapter is the anti-corruption layer of the context map. No other module sees the external system's types, codes or units (cents, 20-character references).

We will treat time-driven work as an order a module gives itself on a schedule. The daily checks (expired reservations, overdue loans, expiring cards, running fines) belong to the module that owns the rule.

## Consequences

- Replacing CityPay or the ISBN service touches one adapter.
- The mail gateway needs a record of its own once its interface is known.
- Tests can replace an adapter by a fake.
- Each module schedules its own work, so there are several schedules to watch instead of one.
- Checks run per branch where the rule is per branch (the overdue limit). The time of day is a detail of each module.
