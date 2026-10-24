---
status: "proposed"
date: 2026-10-23
decision-makers: the maintainer
consulted: none recorded
informed: none recorded
---

# 4. Contexts talk through published events and own their data

## Context and Problem Statement

The context map has ten mappings (chapter 3). They say who is upstream, who is downstream and what kind of translation is needed. We have to decide what they look like in code.

How do the modules exchange facts and orders, and who owns the data?

## Decision Drivers

* The ten mappings of the context map say who is upstream, who is downstream and what kind of translation is needed. The code has to show them.
* Any module that can read another module's state ends the boundary.
* One module's failure should not become everybody's.

## Considered Options

* A shared database with shared tables
* Synchronous calls between modules for everything
* Events for facts, orders through the owner's public API, each module owns its data

## Decision Outcome

Recommended option: "Events for facts, orders through the owner's public API, each module owns its data", because a shared database ends every boundary, and synchronous calls for everything make one module's failure everybody's.

We will connect the modules as follows.

1. **Facts travel as events.** What a context wants others to know is published as an event in its public API (open host service plus published language). Downstream modules react to events and keep the part they need, in their own words.
2. **Orders go through the public API of the owner.** A module that needs another module to *do* something, not just to know something, gives an order through that module's public API (customer-supplier). An order is not a fact, so it cannot be an event. It is the one kind of call from one module to another that we allow (ADR 5 has the case of a hold on a card). Questions (queries) in a module's public API are for the user interfaces (ADR 8); a module does not ask another module during its own work, it uses its own copy.
3. **Each module owns its data.** No module reads or writes another module's data, whatever it is stored in. Modules refer to each other's things only by identifiers that the owning module issues (ADR 7). How the data is physically separated is decided at gate G2.
4. **Translation lives downstream.** Where the upstream is foreign (ISBN service, CityPay), the downstream module translates at the boundary (ADR 6).
5. **A module never needs another module's answer to finish its own business decision.** Reactions to events must tolerate events that arrive twice or late. Whether delivery happens once or at least once, and when it happens in relation to the publisher's transaction, is a technical decision (gate G2).

| Mapping on the context map | In code |
|---|---|
| open host service + published language | public events in the publisher's API |
| customer-supplier | the supplier's public interface, shaped by what the customer asks for: events with the changes the customer needs (membership → lending), or an order the customer gives (if ADR 5 is accepted: fees gives orders to membership, which becomes the supplier) |
| anti-corruption layer | adapter inside the downstream module |

### Consequences

* Bad, because a downstream module keeps its own copy of what it needs (lending keeps the member status). Copies can be late; the rules of each context must say what happens then. That is a question for the modelling of each context.
* Bad, because published events are contracts. Changing one is a change to the upstream's API and is negotiated with its consumers. Events can still be in transit, late or repeated, when a new version is released, so an event should be changed only by adding to it. A record of its own follows when the first event is specified or gate G2 decides how events are kept.
* Neutral, because how events are delivered and kept is decided at gate G2. The rule that a reaction tolerates repeated and late events holds in any case.

## Pros and Cons of the Options

### A shared database with shared tables

* Good, because it is fast to build.
* Bad, because it ends every boundary: any module can read any other module's state, and will.

### Synchronous calls between modules for everything

* Good, because they are simple to follow.
* Bad, because one module's failure becomes everybody's.
* Bad, because every call couples the caller to the callee's availability.

### Events for facts, orders through the owner's public API, each module owns its data

* Good, because it is what the mappings of the context map look like in code (see the table).
* Good, because no module reads or writes another module's data.
* Bad, because copies can be late and published events are contracts (see Consequences).
