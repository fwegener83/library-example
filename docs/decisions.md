# Who decides what

This tutorial builds software with an AI agent. The agent prepares, a human decides. To keep that visible, every decision in the repo has a level, a place where it is recorded, and a person who makes it.

## The levels

| Level | What is decided | Real project: who decides | Recorded in | Example |
|---|---|---|---|---|
| **Business** | What the rules of the business are, where the brief is silent or contradicts itself | The business: director, membership office, finance | [`requirements/clarifications.md`](../requirements/clarifications.md), entries `C-nn` | C-03: a late fine is fixed on return, but the running amount already counts towards the €10 block |
| **Strategy and architecture** | Where the boundaries run, how the parts are deployed and talk to each other | Architect or team | The context map in DDD Studio and [`docs/adr/`](adr/README.md) | ADR 5: how to avoid a circle between modules |
| **Way of working** | How we work on the next steps: tools, order, roles | Project lead | The gates in [`docs/plan.md`](plan.md) | G1: how a context goes from the model in DDD Studio to code |

In this tutorial the maintainer plays all the people on the right. The records say so wherever it matters.

## What the agent does with a decision

1. **Prepare.** Source in the brief, why it matters now, the options, a recommendation, the consequences.
2. **Stop.** The agent does not continue on a path that depends on the answer.
3. **Record.** After the answer: who decided, when, what was rejected and why. A rejected proposal stays in the record.
4. **Apply.** Everything that depends on the decision is changed, and cites the record (`C-03`, `ADR 5`).

In an architecture decision record the two steps are visible: while the status is `proposed`, the decision outcome is a *recommended* option; after the maintainer has approved it, it is the *chosen* option ([ADR 1](adr/0001-record-architecture-decisions.md)).

## When the agent must stop and ask

- The answer is **not in the source**: the brief is silent, vague or contradicts itself, the model depends on it, and the agent finds no sensible behaviour of its own (see below). (Business)
- The decision is **hard to reverse** and there are **real alternatives**. (Architecture)
- It decides **how we work** from here on, or it would touch something the tutorial has declared untouchable (a gate). (Way of working)
- A recommendation turns out to **undo an earlier decision** (for example the circle that undid a statement of chapter 3). The agent says so openly and does not change the earlier decision on its own.

**Business questions delegated (2026-10-25).** From the review before gate G6 on, the maintainer has handed business questions to the agent: where a sensible behaviour exists, the agent decides, records the options and the reason in the clarification log, marks the entry "decided by the agent (delegated by the maintainer)", and lists it in the pull request, where the maintainer can still overturn it. The agent asks only where it finds no sensible behaviour. **Widened on 2026-10-28:** the agent also decides where several options are sensible and none has a notable problem, and asks only when every option is bad. Gates and architecture decisions that are hard to reverse are not part of this delegation. In a real project this is the moment when the business trusts the team with the small rules and keeps the big ones; the tutorial shows it openly instead of pretending every rule came from an interview.

## When it is not a decision

Writing a sentence in the glossary, choosing a card colour, naming a field, correcting a document so that it says what was decided: these are the agent's work and the **review** of the chapter covers them. The agent lists what it decided this way in the pull request, so the maintainer can still object. A review checks work that has been done; a decision chooses between options that have not. If the agent presents every small choice as a question, the human stops deciding and starts nodding, and the real decisions disappear in the noise.

## Where to find them

Each chapter ends its text with the box **Decisions in this chapter**: which decisions were taken, by whom, where they are recorded, and which are still open. Chapters 1 and 2 collect questions and take none; the questions are answered in chapter 3.
