---
status: "accepted"
date: 2026-10-23
decision-makers: the maintainer
consulted: none recorded
informed: none recorded
---

# 6. External systems and the clock sit inside the owning module

## Context and Problem Statement

Three external systems appear in the model (chapter 3): the national ISBN service, CityPay and the city mail gateway. The mail gateway's interface is not in the brief, and chapter 3 left it without a mapping; this record does not cover it. Time also acts on the system: reservations run out, loans become overdue, cards and researcher status expire. Today a librarian prints two lists every morning (brief §3.2); on the Big Picture the actor is a *clock*.

Where do the external systems and the daily, time-driven work sit?

## Decision Drivers

* The anti-corruption layers of the context map need a place.
* No module should see the types, codes or units of an external system (cents, 20-character references) except the one that owns the relationship.
* The daily checks (expired reservations, overdue loans, expiring cards, running fines) follow rules that belong to the contexts.

## Considered Options

* One integration module for all external systems
* One central job for all daily work
* One adapter and one schedule inside the module that owns the relationship or the rule

## Decision Outcome

Chosen option: "One adapter and one schedule inside the module that owns the relationship or the rule", because an integration module would end up knowing the vocabulary of every context, and a central job would have to reach into every module and know their rules.

We will reach every external system through one adapter inside the module that owns the relationship: the ISBN service from `catalogue`, CityPay from `fees`. The adapter is the anti-corruption layer of the context map. No other module sees the external system's types, codes or units (cents, 20-character references).

We will treat time-driven work as an order a module gives itself on a schedule. The daily checks (expired reservations, overdue loans, expiring cards, running fines) belong to the module that owns the rule.

### Consequences

* Good, because replacing CityPay or the ISBN service touches one adapter.
* Good, because tests can replace an adapter by a fake.
* Bad, because each module schedules its own work, so there are several schedules to watch instead of one.
* Neutral, because checks run per branch where the rule is per branch (the overdue limit). The time of day is a detail of each module.
* Neutral, because the mail gateway needs a record of its own once its interface is known.

## Pros and Cons of the Options

### One integration module for all external systems

* Bad, because it would end up knowing the vocabulary of every context.

### One central job for all daily work

* Good, because it is convenient to operate.
* Bad, because it has to reach into every module and know their rules.

### One adapter and one schedule inside the module that owns the relationship or the rule

* Good, because the adapter is the anti-corruption layer of the context map, and no other module sees the external system's types.
* Good, because the daily checks sit with the module that owns the rule.
* Bad, because there are several schedules to watch instead of one.
