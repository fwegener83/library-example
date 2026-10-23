# Architecture decision records

One file per decision, in the format of Michael Nygard's "Documenting Architecture Decisions" (see [ADR 1](0001-record-architecture-decisions.md)): title, date, status, context, decision, consequences.

Status values: `Proposed`, `Accepted`, `Deprecated`, `Superseded by N`.

| ADR | Decision | Status |
|---|---|---|
| [1](0001-record-architecture-decisions.md) | Record architecture decisions | Proposed |
| [2](0002-one-deployable-unit.md) | One deployable unit: a modular monolith | Proposed |
| [3](0003-one-module-per-bounded-context.md) | One module per bounded context, public API only | Proposed |
| [4](0004-contexts-talk-through-published-events.md) | Contexts talk through published events and own their data | Proposed |
| [5](0005-no-circle-between-modules.md) | No circle between modules: fees drives membership | Proposed (needs a choice between options) |
| [6](0006-adapters-and-clock-inside-the-module.md) | External systems and the clock sit inside the owning module | Proposed |
| [7](0007-identifiers-across-contexts.md) | Identifiers across contexts are issued by the owner | Proposed |
| [8](0008-user-interfaces-outside-the-modules.md) | User interfaces sit outside the modules and use only public APIs | Proposed |

Technology (language version, framework, database, event store, user interface technology) is decided at gate G2 and is deliberately not part of these records.
