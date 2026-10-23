# Architecture decision records

One file per decision, numbered. Format: status, context, decision, alternatives we rejected, consequences. A decision stays in the list when it is replaced; the new record says which one it replaces.

Status values: `proposed` (written, waiting for the maintainer), `accepted`, `superseded by ADR-nnnn`.

| ADR | Decision | Status |
|---|---|---|
| [0001](0001-one-deployable-unit.md) | One deployable unit: a modular monolith | proposed |
| [0002](0002-one-module-per-bounded-context.md) | One module per bounded context, public API only | proposed |
| [0003](0003-contexts-talk-through-published-events.md) | Contexts talk through published events and own their data | proposed |
| [0004](0004-no-circle-between-modules.md) | No circle between modules: fees drives membership | proposed |
| [0005](0005-adapters-and-clock-inside-the-module.md) | External systems and the clock sit inside the owning module | proposed |

Technology (language version, framework, database, event store, user interface) is decided at gate G2 and is deliberately not part of these records.
