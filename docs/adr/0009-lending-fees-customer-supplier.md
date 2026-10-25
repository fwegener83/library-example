---
status: "accepted"
date: 2026-10-24
decision-makers: the maintainer
consulted: none recorded
informed: none recorded
---

# 9. Lending supplies fees as customer and supplier, not as an open host

## Context and Problem Statement

Chapter 3 drew `lending` → `fees` as an open host service with a published language. Its reason, in the wording chapter 3 had then: "Fees follows loans (due date, returned, lost, usage fee) without lending knowing that fees exist. Reminders and the reader account will need the same events, so lending publishes them once for everyone." The same table says: "Where the consumer's needs are negotiated one to one, as between membership and lending, *customer-supplier* fits better."

Since then the other consumers have not come. Chapter 3 cut no context for notifications; the reminders all concern `lending` ("What we did not cut"). And the reader's account page asks the modules instead of listening to their events (ADR 8). `fees` is the only consumer of the loan events, and its needs shaped them: the due date for the running fine (C-03), the loss (C-04). The usage fee is no longer part of them (C-21). The challenge of the cut found this (`docs/reviews/ch04-context-cut.md`, F4); chapter 5 prepared it, and the maintainer followed the recommendation (2026-10-24).

Which pattern describes the relationship between `lending` and `fees`?

## Decision Drivers

* A pattern describes the relationship we have, not one we might have later.
* An open host service is worth it for several consumers or a stable public contract, not for the count of consumers alone (`challenge-context-cut`, heuristics §6).
* Where the consumer's needs are negotiated one to one, customer–supplier fits better (chapter 3).
* The dependencies must not change: `fees` uses `lending`, never the other way round (ADR 3, ADR 5).

## Considered Options

1. Customer–supplier
2. Open host service with a published language, justified by a stable contract
3. Conformist

## Decision Outcome

Chosen option: "Customer–supplier", because `fees` is the only consumer and its needs shaped the loan events, which is what chapter 3 itself calls customer–supplier.

* `lending` is the supplier, `fees` the customer. `lending` plans its loan events for what `fees` needs (checked out, became overdue, returned, declared lost, each with its due date) and tells `fees` before it changes them.
* The facts still travel as events in the public API of `lending` (ADR 4 allows events with the changes the customer needs, as between `membership` and `lending`). `lending` knows `fees` as its customer, but it does not depend on `fees` in code (ADR 3, ADR 5) and does not know what `fees` does with the events.
* In the model, the two mappings `lending-fees-open-host-service` and `lending-fees-published-language` become one customer–supplier mapping, so the context map has nine mappings instead of the ten that ADR 4 counts. The table in chapter 3 changes.
* If a second consumer of the loan events appears, the pattern is looked at again.

### Consequences

* Good, because the map says what is true: one consumer, negotiated needs.
* Good, because `lending` knows who it plans for when a loan event changes (for example, if 28-day loans come, C-13).
* Neutral, because nothing changes in the dependencies or in the code that ADR 4 describes: the loan events stay events.
* Bad, because a pattern approved in chapter 3 changes, and chapter 3 and the model have to follow.

## Pros and Cons of the Options

### Customer–supplier

* Good, because it matches the relationship: `fees` is the only consumer and its needs shaped the events.
* Good, because it matches the rule of chapter 3 for one-to-one negotiated needs.
* Bad, because the mapping, its description and the table in chapter 3 change.

### Open host service with a published language, justified by a stable contract

* Good, because it changes only words.
* Good, because a second consumer would find a general format ready.
* Bad, because it keeps a pattern for consumers that do not exist and gives it a new reason after the old one fell away.

### Conformist

`fees` takes the loan events as `lending` publishes them, and nobody negotiates.

* Good, because it asks nothing of `lending`.
* Bad, because there is a negotiation: the needs of `fees` shaped the events (the due date for the running fine, C-03; the loss, C-04), and `lending` has to tell `fees` before it changes them. Without that, a change in `lending` would break the fines silently. "Without anyone negotiating, it is a conformist relationship with a nicer name" (`challenge-context-cut`, heuristics §6); here someone negotiates.
