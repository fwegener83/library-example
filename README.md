# Library Example — from a brief to running software

A tutorial that walks a single example, a public library, from an
unpolished requirements brief to a working application: Big Picture Event
Storming, Domain Stories, a context map, bounded contexts as modules of
one Spring Boot application, and then one context after the other,
modelled in detail and built from the model — with [DDD Studio](https://ddd-studio.dev).

**Status:** work in progress. Chapters 0 to 6 are done; gate G6 is decided (option 3). Gate G1 is
decided: the tutorial follows a [phase model](docs/gates/g1-model-to-code.md)
from a few documents with requirements to running software, with a skill
for each phase. ADR 10 (REST at the edges) is accepted. The independent review of the cut before gate G6 and its answers (C-27 to C-32, ADR 11) are done. Next is chapter 7, the flows and contracts across the boundaries.

| Chapter | Topic | Status |
|---|---|---|
| 0 | [The brief](requirements/brief.md) | done |
| 1 | [Big Picture Event Storming](chapters/01-big-picture.md) | done |
| 2 | [Domain Stories](chapters/02-domain-stories.md) | done |
| 3 | [Strategic design](chapters/03-strategic-design.md) | done |
| 4 | [Deployment decision](chapters/04-deployment-decision.md) | done |
| 5 | [Challenging the cut](chapters/05-challenging-the-cut.md) | done |
| 6 | [Choosing the first increment](chapters/06-choosing-the-first-increment.md) | done (gate G6 decided: option 3) |

How decisions are made, and by whom, is described in [`docs/decisions.md`](docs/decisions.md). The working plan (in German) is in [`docs/plan.md`](docs/plan.md).

## Credits

The domain is adapted from
[ddd-by-examples/library](https://github.com/ddd-by-examples/library)
(MIT License, © 2019 Jakub Pilimon).
