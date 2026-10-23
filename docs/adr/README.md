# Architecture decision records

One file per decision, in the format of Michael Nygard's "Documenting Architecture Decisions" (see [ADR 1](0001-record-architecture-decisions.md)): title, date, status, context, decision, consequences.

Status values: `Proposed`, `Accepted`, `Deprecated`, `Superseded by N`.

| ADR | Decision | Status |
|---|---|---|
| [1](0001-record-architecture-decisions.md) | Record architecture decisions | Accepted |
| [2](0002-one-deployable-unit.md) | One deployable unit: a modular monolith | Accepted |
| [3](0003-one-module-per-bounded-context.md) | One module per bounded context, public API only | Accepted |
| [4](0004-contexts-talk-through-published-events.md) | Contexts talk through published events and own their data | Accepted |
| [5](0005-no-circle-between-modules.md) | Fees holds a card through membership, so the modules form no circle | Accepted |
| [6](0006-adapters-and-clock-inside-the-module.md) | External systems and the clock sit inside the owning module | Accepted |
| [7](0007-identifiers-across-contexts.md) | Identifiers across contexts are issued by the owner | Accepted |
| [8](0008-user-interfaces-outside-the-modules.md) | User interfaces sit outside the modules and use only public APIs | Accepted |

Technology (language version, framework, database, event store, user interface technology) is decided at gate G2 and is deliberately not part of these records.
