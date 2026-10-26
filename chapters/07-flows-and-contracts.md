# Chapter 7 — Flows and contracts across the boundaries

**Input:** the accepted scope of [chapter 6](06-choosing-the-first-increment.md) (option 3), the cut and map of [chapter 3](03-strategic-design.md), the records [ADR 2 to 11](../docs/adr/README.md), the [clarification log](../requirements/clarifications.md), the [brief](../requirements/brief.md)
**Tool:** the skills [`model-flows`](../.claude/skills/model-flows/SKILL.md) and [`design-context-contracts`](../.claude/skills/design-context-contracts/SKILL.md), both written for this chapter; DDD Studio, Static View and Flow View (Studio version `ch07-flows-and-contracts-v2`)
**Result:** ten flows with 51 steps across the four contexts, a contract for every boundary that the scope crosses (thirteen events, two orders, six questions), the test of the cut against the abort criteria of the phase model, and one proposed record on how contracts change over time ([ADR 12](../docs/adr/0012-changing-published-events.md)). **No abort criterion was hit.** Nothing is built.

## What this chapter is, and what it is not

Everything in this chapter is the **model in DDD Studio**. No code is written before chapter 12, after the technology gate (G2). The model is what the code will be built from; the code is a separate step.

Phase 5 of the [phase model](../docs/gates/g1-model-to-code.md) has two halves: the boundaries first, then the inside of each context. This chapter is the first half. In Studio that means real model elements, not sketches: for the nine scenarios of the scope, the aggregates, commands, events, policies, read models and queries that the processes need, and for every event, order and question that crosses a boundary, its payload schema, its owner and what its consumers do with it.

What waits for the second half (chapters 8 to 10): the invariants of each aggregate, the scenarios in Given/When/Then, the commands that touch no boundary, the REST API of each context, and the rules that are parked in the clarification log (C-11, C-12, C-13, C-14). The aggregates of this chapter are real, but they are refined there, not replaced. Which aggregate decides whether a checkout is allowed (`loan`, `copy` or `reader`) is one of the questions chapter 8 answers; what crosses the boundary does not depend on the answer.

## How the flows were drawn

For each scenario of option 3 there is a flow, in the order of the build (A and B first). A flow is one example run, with concrete data from the sources: a title *The Hobbit* at EUR 18.00, a loan due on 1 December, seven days late. A flow step is a command (who does what, in which aggregate, which fact results) or the reaction in another context (the policy, its command, the aggregate that changes). The policy always belongs to the context that reacts.

| Flow | Scenario of chapter 6 | Steps | Boundaries it crosses |
|---|---|---|---|
| A. Register a title and a copy, lending learns the copy | A | 4 | catalogue → lending, catalogue → fees |
| A2. Correct a copy and withdraw a copy | A (C-27), G1 | 4 | catalogue → lending |
| B. Register a member, grant researcher status, renew the card | B | 6 | membership → lending |
| C. Check out and return a copy, also a damaged one | C | 4 | none (inside `lending`) |
| D. Reserve a copy, collect it, cancel it or let it run out | D | 5 | none (inside `lending`) |
| E1. A late return: the fine is assessed | E1 | 4 | lending → fees |
| E2–E3. The running fine blocks the card, payment unblocks it | E2, E3 | 8 | lending → fees, fees → membership, membership → lending |
| E2b. The return reaches fees after the morning run and takes the hold back | E2 (late case) | 6 | the same |
| G1. A copy is declared lost at the desk | G1 | 6 | lending → fees, fees → membership, catalogue → lending |
| J1. The morning lists | J1 | 4 | questions to lending, membership, catalogue |

Two of the flows are about the exception. E2b is the case that ADR 11 was written for: a loan is 21 days overdue on the morning of 23 December, the morning run counts EUR 10.50 and fees orders the hold; the reader had in fact handed the copy back on 22 December (20 days, EUR 10.00), and the message arrives late. Fees counts to the business day of the return, finds EUR 10.00, which is not *more than* EUR 10, and orders the hold lifted. Lending applies "blocked" and then "free" in the order of their numbers and never sees the two the wrong way round.

The model now holds 9 aggregates, 29 commands, 29 events, 10 policies, 6 read models, 6 queries and 6 actors. Of the 29 events, 13 cross a boundary; the other 16 are internal to a context and exist because the aggregate that handles a command has to record what happened (for example that lending took over a change of a member's card).

## The crossings

A crossing is where a step of a flow leaves one context for another. There are eleven, and each one has exactly one kind (fact, order or question) and one owner of the reaction.

| # | From → to | Kind | What | Reaction, and whose it is |
|---|---|---|---|---|
| 1 | catalogue → lending | fact | copy registered | `shelve-registered-copy`, lending |
| 2 | catalogue → lending | fact | copy corrected | `follow-copy-correction`, lending |
| 3 | catalogue → lending | fact | copy withdrawn | `stop-lending-withdrawn-copy`, lending |
| 4 | catalogue → fees | fact | title added, title details corrected | `follow-title-prices`, fees |
| 5 | membership → lending | fact | member registered, researcher status granted, card renewed, hold placed, hold lifted | `follow-membership-status`, lending |
| 6 | lending → fees | fact | copy checked out | `track-loan-for-fees`, fees |
| 7 | lending → fees | fact | copy returned | `assess-fine-on-return`, fees |
| 8 | lending → fees | fact | copy declared lost | `charge-lost-book-on-loss`, fees |
| 9 | fees → membership | order | place the hold "unpaid fees" | `keep-unpaid-fees-hold-in-line`, fees (C-19) |
| 10 | fees → membership | order | lift the hold | the same policy |
| 11 | staff pages → lending, membership, catalogue, fees | question | six queries | none: a page composes the answers (ADR 8, ADR 10) |

Two mappings of the context map carry no traffic in this increment: CityPay → fees (E4) and the national ISBN service → catalogue (titles are keyed in, A). They are not tested.

## The contracts

Every published event carries the envelope of [ADR 11](../docs/adr/0011-what-every-published-event-carries.md): the identity of its subject, the business day (`occurred-on`) and its place in order for the subject (`sequence`). The names of the fields are an agent's decision of this chapter (see the box at the end). An order carries `decided-at`, the moment of the decision, as ADR 5 asks.

The contract of an event is its schema, its owner, who uses what, and what the consumer does when it arrives twice, late, out of order or about something it does not know yet. The first three are in the table; the last is the same rule for all events, with the exceptions below it.

| Event | Owner | Subject | What the consumers use | Carried, not used yet |
|---|---|---|---|---|
| copy registered | catalogue | the copy | lending: copy, title, kind, home branch | usage-fee mark (scenario F) |
| copy corrected | catalogue | the copy | lending: kind, home branch (all three values travel, so the event replaces the earlier ones) | usage-fee mark |
| copy withdrawn | catalogue | the copy | lending: the fact | reason (lists of the Head of Collection) |
| title added | catalogue | the title | fees: title, replacement price | ISBN, title, author (the catalogue's own page) |
| title details corrected | catalogue | the title | fees: replacement price (the whole record travels) | as above |
| member registered | membership | the member | lending: end date of the card | card number |
| researcher status granted | membership | the member | lending: end date of the status | |
| card renewed | membership | the member | lending: new end date of the card | |
| hold placed | membership | the member | lending: whether the card is now blocked | reason |
| hold lifted | membership | the member | lending: whether the card is now blocked | reason |
| copy checked out | lending | the loan | fees: loan, reader, title, due date | copy |
| copy returned | lending | the loan | fees: loan, reader, day of return | copy |
| copy declared lost | lending | the loan | fees: loan, reader, day of the report | copy |

The two orders carry the member, the reason, the party that placed the hold and the time of the decision. The owner is `membership`; `fees` is the only caller in this increment. An order about a member that membership does not know is refused with the reason "member not known yet".

The six questions are asked by a staff page and answered by one module each: the reservations that ran out and the overdue loans of a branch on a day (lending), the copies that wait for the Head of Collection (lending), contact details of a list of members (membership), details of a list of titles (catalogue) and the amount a reader owes (fees). The two that ask for people and titles take a **list**, because a morning list has dozens of rows and a call per row would be a call per reader.

**For every event, the same rule** (ADR 11): a number already applied is a repeat and is ignored; the next number is applied; a gap holds the later events back until the missing ones arrive, and the held-back events are visible as a list with their age. Business rules count in business time: fees counts the late days to the day of the return, not to the day the message arrived.

**Exceptions and additions that belong to one contract:**

* A correction or a withdrawal of a copy that lending does not know yet is held back, as is a return that arrives before its checkout (ADR 11).
* A return, or the morning run, for a loan whose title price fees does not know yet is held back or left out of the count and listed as waiting. A fine is never counted without its cap, and a lost book is never charged as free.
* The card events are applied **strictly in order** for a member. Otherwise "blocked" and "free" could change places.
* Dates, not durations: the end of a card and of researcher status travel as dates, and lending compares them with the day (C-28). No event is needed for a card to *expire*; this is why the events of the Big Picture *Card Expired* and *Researcher Status Expired* have no consumer and are not in the model.
* Every unknown value of an enumeration is read on the safe side: an unknown copy kind is not lendable.

## What the test of the cut showed

The skills ask for the five abort criteria of the phase model on every flow, with the result written down also when nothing is found.

| Criterion | Result |
|---|---|
| An invariant needs data from two contexts at the same moment | Not hit, but it is the main thing the test showed (finding 1). |
| A policy has no clear owner | Not hit. All ten policies have one, written at the start of the description. |
| A flow goes back and forth between two contexts | Not hit (finding 3). Between no two contexts does traffic run in both directions. |
| An aggregate needs the state of another context to decide | Not hit, with the same remark as the first criterion. |
| A word needs two meanings inside one context | Not hit. One word, *branch*, has several roles in `lending` (finding 5). |

**The cut holds. Seven findings, none of which is a stop.**

1. **Lending decides from local copies, and that is the cost of this cut.** A checkout needs the end date of the card and the researcher status (membership), the kind of the copy (catalogue) and the shelf state (lending itself). Read as an invariant, that is data of three contexts at the same moment. The answer in ADR 4 and ADR 11 is that `lending` keeps what it needs as facts of its own and never asks back. The flows show that this works: every command of `lending` that lends or reserves is decided from `reader` and `copy`, which are kept up to date by two policies. The price is a window of staleness. A reader who has just renewed may be refused until the renewal arrives; a copy that was corrected a minute ago is lent under its old kind until then. Both are on the safe side and ADR 11 already names the renewal case. **The cut holds only if this reading of ADR 4 is accepted.** The maintainer should be aware that it is the case.
2. **An event that nobody needs was removed.** The context map (ADR 9, mapping `lending-fees`) and the Big Picture name *Loan Became Overdue*. In the flows nothing consumes it: `fees` counts from the due date it holds, and the morning list of overdue loans is a comparison of the due date with the day. The wording of ADR 9 and of the mapping is corrected; the decision of ADR 9 (customer–supplier) is unchanged.
3. **Three hops, no circle.** A payment at the desk is a fact of `fees`, which orders `membership` to lift the hold, which publishes a fact that `lending` applies. The flow touches three contexts and returns to the one it started from, but the dependencies are `fees → lending`, `fees → membership` and `lending → membership`, which is acyclic, as ADR 5 wants. Delivery costs time: in the moment between the payment and the arrival of the fact the desk of `lending` still sees the card as blocked. With one deployable unit this may be a matter of milliseconds, but the contract does not rely on it; the technology is decided at G2.
4. **A fee that crosses ten euros by one day.** The case E2b above is what ADR 11 did for the first time on a real flow. It works because the hold order carries the time of the decision and the policy is stateless: the aggregate in `fees` decides, the policy turns the decision into an order (tool gap 15 describes this pattern).
5. **The word *branch* has several roles in `lending`:** the home branch from the catalogue, the branch where a copy stands now, the branch where it was checked out and the branch where it was returned. C-14 (which branch counts for the overdue limit) is exactly the question which of them is meant. The model keeps them apart by field name today (`home-branch`, `current-branch`, `branch`); chapter 8 names the roles properly when it decides C-14.
6. **Some fields are carried that no consumer uses yet.** The usage-fee mark travels in the copy events and the reason in the hold events. By the rule "a field that no consumer needs is removed" they would be gone. They stay, because the first driver of ADR 11 says that a field added later is missing from every event already published. This is an exception with a reason, and ADR 12 says so.
7. **Identifiers keep the name of the owner.** The aggregates are called `reader` and `reader-account` (the words of `lending` and `fees`, C-07), but the identifier is `member-id`, as membership issues it (ADR 7). A word of one context therefore appears in the payloads of two others. It is the identifier, not a concept, and it is kept so that a reader of two contracts sees at once that they speak of the same thing.

**What the flows could not test**, and nobody should believe they did: the anti-corruption layers to CityPay and to the ISBN service (E4 and the lookup are left out); the release of a damaged copy, which ADR 11 wants to name the damage report that it answers (H is left out; `lending` already issues the damage report and lists it); keeps and the end of researcher status (I); the rules inside `lending`, among them the five reservations, the overdue limit per branch and the restricted copy for a researcher on the day, which are rules of an aggregate and are tested in chapter 8.

## How a contract changes: ADR 12 (proposed)

ADR 4 says that a published event is "changed only by adding to it" and announced a record on the rest. [ADR 12](../docs/adr/0012-changing-published-events.md) writes it and is **proposed**, for the maintainer to decide. The recommendation: adding a field or a new event is free for the owner; everything else (a removed, renamed or retyped field, a changed meaning, a new value in an enumeration that a consumer decides on) is a **new fact under a new name, published beside the old one**, with the consumers named in the model, until the last has moved. The alternatives are a version in every event with conversion in the consumer, and changing publisher and consumers together without compatibility; the record says why the first is more than we know we need before G2 and why the second turns the modules into co-owned code.

## The open point of C-31

C-31 left one question for this chapter: how a notice from `lending` reaches an email address that `membership` keeps. No contract of this increment needs it: the notices by email (J2) are left out, and the morning lists ask `membership` for the phone number by a question. So the question stays open for J2. The options and a recommendation, for the day J2 comes into scope:

* **(a) Lending keeps the address.** `membership` publishes its contact details as a fact, `lending` keeps a copy of phone and email and sends the notice through the mail gateway (which gets its own mapping). It fits ADR 4 (each context keeps the facts it needs) and adds no new dependency, because `lending` already follows `membership`. Cost: personal data in two contexts, and a change of an address has to reach both.
* **(b) A notice adapter outside the modules** listens to the facts of `lending` and asks `membership` for the address. One copy of the data. Cost: a new kind of element that listens to events from outside, which ADR 8 does not provide for.
* **(c) Membership sends.** It would have to listen to `lending`, which closes a circle with the existing arrow. ADR 5 rules this out.

**Recommendation for J2: (a).** It is the option that keeps within the rules we have.

## What we take with us

* **The cut survived the first test with the inside of the contexts.** Seven of the nine mappings were used by the flows; two were not, and the chapter says which.
* The skills `model-flows` and `design-context-contracts` exist and were used for real. The second mode of `challenge-context-cut` (flows and contracts) was added and is used for the review of this chapter.
* The model in Studio is the source of the contracts. The tables above are made from it, and the export in [`model/esdm/`](../model/esdm/) holds the events, commands, queries and policies as files. The flows are in Studio only, because ESDM does not export them (tool gap 16).
* Chapter 8 starts with `lending` and takes the questions that this chapter left: which aggregate decides a checkout, the roles of the branch, and C-11 to C-14.

## Decisions in this chapter

* **Business — decided by the agent (delegated by the maintainer), one entry:** C-33. A late fine is charged also for a damaged copy; the damage costs the reader nothing (C-06). Recorded in the [clarification log](../requirements/clarifications.md), where the maintainer can overturn it.
* **Architecture — one proposal, for the maintainer to decide:** [ADR 12](../docs/adr/0012-changing-published-events.md), how a contract changes. Status `proposed`; the recommended option is "additions only; anything else is a new fact beside the old one". Until it is decided, ADR 4 ("changed only by adding to it") stands.
* **Open for the maintainer, later:** the recommendation for C-31 (the address of a notice) is made for J2 and not for this increment.
* **Way of working:** the skills `model-flows` and `design-context-contracts` are used from now on; mode 2 of `challenge-context-cut` is part of phase 5. The contract lives in the model in Studio; this repository has no second copy of it.
* **Decided by the agent, listed so that the maintainer can object** (detail of the model, not decisions between options):
  * The envelope fields are `<subject>-id`, `occurred-on` (the business day, a date) and `sequence`; an order carries `decided-at` (a moment). Money is whole cents.
  * *Card Blocked* and *Card Unblocked* of the Big Picture are the events *hold placed* and *hold lifted*, each with the field `blocked` for the state after the change. The reason is why the card is blocked; lending needs only the state.
  * *Loan Became Overdue* is not an event (finding 2). *Card Expired* and *Researcher Status Expired* have no consumer and are not modelled (C-28).
  * The checkout names the title, so that `fees` needs no copy events in this increment.
  * `fees` keeps one aggregate per reader (`reader-account`), because the EUR 10 rule adds up all charges of a reader (C-19). `lending` keeps a `reader` and a `copy` of its own.
  * *Reservation collected* is an event of this model, inferred; the checkout of a collected reservation follows from it in a policy of `lending`.
  * Flow E2b was added for the late case; the questions for people and titles take lists.
  * A published event is marked in the description by its first words, "Published to …" or "Internal to …" (tool gap 19).

---

*Boards: no Domain Story or sketch board was changed. Studio versions: `ch07-flows-and-contracts` and `ch07-flows-and-contracts-v2` (workspace "Millbrook Library (tutorial)"). Sources: [`model/esdm/`](../model/esdm/), [`docs/adr/`](../docs/adr/README.md), [`requirements/clarifications.md`](../requirements/clarifications.md), [`docs/tool-gaps.md`](../docs/tool-gaps.md).*
