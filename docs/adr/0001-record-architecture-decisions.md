# 1. Record architecture decisions

Date: 2026-10-23

## Status

Proposed

## Context

From chapter 4 on, the tutorial makes decisions that are expensive to change and that later chapters build on: how many programs run, how the contexts of chapter 3 meet in code, where external systems are reached. A later reader, or the maintainer in a year, needs to know not only what was decided but why, and what was given up for it. Chapter text explains, but it is written for learning, not for looking things up.

## Decision

We will keep architecture decision records in the format described by Michael Nygard in "Documenting Architecture Decisions" (2011): one short file per decision in `docs/adr/`, numbered and never reused, with the sections Title, Status, Context, Decision and Consequences.

- The **context** names the forces, including the alternatives we considered and why they lost.
- The **decision** is written in full sentences in active voice ("We will …").
- The **consequences** list everything that follows, the good and the bad.
- **Status** is `Proposed`, `Accepted`, `Deprecated` or `Superseded by N`. A record is accepted when the maintainer approves it. A replaced record stays and points to its successor.

Technology (language version, framework, database, event store, user interface technology) is decided at gate G2. Until then, records say what a technology must provide, never which one.

## Consequences

- Every decision of this kind has one place and one number that chapters, the model and code can point to.
- Writing a record takes time, so we write one only for decisions that are hard to reverse or that more than one module has to follow.
- Records are not rewritten when we change our mind; a new record supersedes the old one. The history stays readable.
- `scripts/check_repo.py` checks that each record has the five sections and is listed in the index.
