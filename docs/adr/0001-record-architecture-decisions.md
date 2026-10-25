---
status: "accepted"
date: 2026-10-23
decision-makers: the maintainer
consulted: none recorded
informed: none recorded
---

# 1. Record architecture decisions

## Context and Problem Statement

From chapter 4 on, the tutorial makes decisions that are expensive to change and that later chapters build on: how many programs run, how the contexts of chapter 3 meet in code, where external systems are reached. A later reader, or the maintainer in a year, needs to know not only what was decided but why, and what was given up for it. Chapter text explains, but it is written for learning, not for looking things up.

Which form do we give these records, so that preparing a decision and deciding it stay two visible steps?

## Decision Drivers

* The decisions are expensive to change, and later chapters build on them.
* A later reader needs to know what was decided, why, and what was given up for it.
* The tutorial separates preparation from decision ([`docs/decisions.md`](../decisions.md)): the agent prepares the options, a recommendation and the consequences; a human decides. Afterwards the record says who decided, when, and what was rejected and why. A rejected proposal stays in the record.
* Chapter text is written for learning, not for looking things up.

## Considered Options

* MADR, full template
* Chapter text only

## Decision Outcome

Chosen option: "MADR, full template", because it has a place for each step of the way of working in `docs/decisions.md`: the options and the recommendation are prepared, the maintainer decides, and the options that lost stay in the record with their reasons.

* **One file per decision** in `docs/adr/`, numbered and never reused, written with the full template of MADR (Markdown Architectural Decision Records, version 4.0.0, <https://adr.github.io/madr/>).
* **Sections.** The metadata (`status`, `date`, `decision-makers`, `consulted`, `informed`), then *Context and Problem Statement*, *Decision Drivers*, *Considered Options*, *Decision Outcome* with *Consequences*, and *Pros and Cons of the Options*. *Confirmation* and *More Information* are added only where there is something to say.
* **Recommendation and decision.** While a record has the status `proposed`, the *Decision Outcome* reads `Recommended option: "…", because …`. After the maintainer has approved it, the status is `accepted` and the same place reads `Chosen option: "…", because …`. Only the maintainer changes the status.
* **Status** is `proposed`, `accepted`, `rejected`, `deprecated` or `superseded by ADR-N`. A replaced record stays and points to its successor.
* **Decision-makers** are named in the metadata. In this tutorial the maintainer plays all the people who decide (`docs/decisions.md`).
* **The options** that were considered are listed under *Considered Options*. Each one has a heading under *Pros and Cons of the Options* that says why it won or lost.

### Consequences

* Good, because every decision of this kind has one place and one number that chapters, the model and code can point to.
* Good, because a reader sees at once whether a record is a recommendation or a decision.
* Bad, because writing a record takes time. We write one only for decisions that are hard to reverse or that more than one module has to follow.
* Neutral, because records are not rewritten when we change our mind; a new record supersedes the old one. The history stays readable.

### Confirmation

`scripts/check_repo.py` checks that each record has the metadata and the sections named above, that its status matches the index in `docs/adr/README.md`, that the wording of the *Decision Outcome* matches the status, and that each considered option has a heading under *Pros and Cons of the Options*.

## Pros and Cons of the Options

### MADR, full template

* Good, because it has sections for the options, the recommendation or choice, and the pros and cons of each option, which is what the way of working in `docs/decisions.md` records.
* Good, because the metadata names who decided and when.
* Bad, because writing a record takes time.

### Chapter text only

* Good, because the chapter explains the decision where it is learned.
* Bad, because chapter text is written for learning, not for looking things up, and it gives a decision no number of its own.

## More Information

The tutorial is written for Java, Spring Boot and Spring Modulith (`docs/plan.md` §3); that is a premise of the tutorial, not a record. Versions, the event store, the database and the user interface technology are decided at gate G2. Until then, records say what a technology must provide, never which one. (Corrected 2026-10-25: this paragraph first listed the framework as open too, which contradicted the plan.)
