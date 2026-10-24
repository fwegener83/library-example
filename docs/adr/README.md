# Architecture decision records

One file per decision, written with the full template of MADR, Markdown Architectural Decision Records (see [ADR 1](0001-record-architecture-decisions.md)): metadata, context and problem statement, decision drivers, considered options, decision outcome with consequences, pros and cons of the options.

Status values: `proposed`, `accepted`, `rejected`, `deprecated`, `superseded by ADR-N`. While a record is `proposed`, its decision outcome is a recommended option; once the maintainer has approved it, it is the chosen option.

| ADR | Decision | Status |
|---|---|---|
| [1](0001-record-architecture-decisions.md) | Record architecture decisions | accepted |
| [2](0002-one-deployable-unit.md) | One deployable unit: a modular monolith | accepted |
| [3](0003-one-module-per-bounded-context.md) | One module per bounded context, public API only | accepted |
| [4](0004-contexts-talk-through-published-events.md) | Contexts talk through published events and own their data | accepted |
| [5](0005-no-circle-between-modules.md) | Fees holds a card through membership, so the modules form no circle | accepted |
| [6](0006-adapters-and-clock-inside-the-module.md) | External systems and the clock sit inside the owning module | accepted |
| [7](0007-identifiers-across-contexts.md) | Identifiers across contexts are issued by the owner | accepted |
| [8](0008-user-interfaces-outside-the-modules.md) | User interfaces sit outside the modules and use only public APIs | accepted |

Technology (language version, framework, database, event store, user interface technology) is decided at gate G2 and is deliberately not part of these records.
