# ADR-0003: Contexts talk through published events and own their data

**Status:** proposed · **Date:** 2026-10-23

## Context

The context map has ten mappings (chapter 3). They say who is upstream, who is downstream and what kind of translation is needed. We have to decide what they look like in code.

## Decision

1. **Facts travel as events.** What a context wants others to know is published as an event in its public API (open host service plus published language). Downstream modules react to events and keep the part they need in their own words.
2. **Orders go through the public API of the owner.** A module that needs another module to *do* something (not just to know something) gives an order through that module's public API (customer-supplier). It does not read the other module's data. An order is not a fact, so it cannot be an event; it is the one place where a call between modules is allowed (see ADR-0004 for the case of blocking a card).
3. **Each module owns its data.** No module reads or writes another module's data, whatever it is stored in, and modules refer to each other's things only by identifier. How the data is physically separated is decided at gate G2.
4. **Translation lives downstream.** Where the upstream is foreign (ISBN service, CityPay), the downstream module translates at the boundary (ADR-0005).
5. **A module never needs another module's answer to finish its own business decision.** Reactions to events must tolerate events that arrive twice or late. Whether delivery happens once or at least once, and when it happens in relation to the publisher's transaction, is a technical decision (gate G2).

| Mapping on the context map | In code |
|---|---|
| open host service + published language | public events (and, if needed, queries) in the publisher's API |
| customer-supplier | the supplier's public interface, shaped by what the customer asks for: events that carry the changes the customer needs (membership → lending), or an order the customer gives (fees → membership, if ADR-0004 is accepted) |
| anti-corruption layer | adapter class inside the downstream module |

## Alternatives we rejected

- **Shared database, shared tables.** Fast to build, and the end of every boundary: any module can read any other module's state and will.
- **Synchronous calls everywhere.** Simple to follow, but one module's failure becomes everybody's.

## Consequences

- A downstream module keeps its own copy of what it needs (for example lending keeps the member status). Copies can be late; the rules must say what happens then. That is a question for the modelling of each context.
- Published events are a contract. Changing one is a change to the upstream's API and is negotiated with its consumers.
- How events are delivered and kept is decided at gate G2. The rule that a reaction has to tolerate repeated and late events holds in any case.
