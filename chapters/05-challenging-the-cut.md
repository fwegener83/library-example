# Chapter 5 — Challenging the cut

**Input:** the [brief](../requirements/brief.md), the cut and map of [chapter 3](03-strategic-design.md), the records of [chapter 4](04-deployment-decision.md)
**Tool:** the skill [`challenge-context-cut`](../.claude/skills/challenge-context-cut/SKILL.md), run by a fresh agent; DDD Studio for the changes
**Result:** a tested way to challenge a context cut, a [report](../docs/reviews/ch04-context-cut.md) on the current cut, six new business decisions (C-20 to C-25), corrected glossaries, mappings and Big Picture board, and a [second report](../docs/reviews/ch05-context-cut.md) on our own answers. One new record, [ADR 9](../docs/adr/0009-lending-fees-customer-supplier.md): `lending` → `fees` becomes customer–supplier.

## Why challenge the cut

The cut into contexts is the decision that is most expensive to undo. Everything after gate G1 builds on it: the specifications, the detailed models, the code. Two mistakes in it were found late. Chapter 3 called a dependency circle harmless, and chapter 4 first moved a business rule without asking whose rule it was. DDD Studio draws the cut, but it does not argue with it.

So before we build on the cut, we let someone argue with it, and we do it in a way that can be repeated before every gate.

## The skill

The skill reads the cut through six lenses. Its rules come from established DDD practice and from our own mistakes:

1. **Canvas.** For each context, the fields of the *Bounded Context Canvas* (DDD Crew): purpose, classification, the decisions it makes, what it receives and sends, its words. A context that makes no decision of its own is suspect.
2. **Language.** A bounded context is the boundary within which the words have one meaning (Evans). The same word with another meaning in another context is a good sign; a word of one context inside another context's definitions is a leak.
3. **Owner of each rule.** For every rule that touches two contexts: who decides it, who may change it, where that is written. A rule split over two contexts is strong coupling across a long distance (Khononov, *Balancing Coupling in Software Design*).
4. **Dependencies.** Whoever reacts to an event depends on its publisher. Read as a build, the map must have no circle (the Acyclic Dependencies Principle). A circle in the business flow is normal; a circle in the dependencies is not.
5. **Scenarios.** Concrete cases through all contexts, with one about timing and one exception, and three likely changes: how many contexts does each one touch?
6. **Patterns and anti-patterns.** Is each mapping pattern real (a customer–supplier has a negotiation, an anti-corruption layer translates something)? Is there an entity service, a pass-through context, a god context, a context cut by technology?

Four working rules make the result usable. The challenge runs in a **fresh agent** that gets the files, not the reasoning of whoever drew the cut. Every finding **quotes its evidence**; without a quote it is not reported. **Business comes before technology**: "whose rule is it?" is asked before "which way do the dependencies point?". And the skill **proposes, it does not decide**: business questions go out as draft clarifications, architecture questions as proposed records (MADR, status `proposed`, with a recommended option), and the maintainer decides.

## Does it work? A test on chapter 3

The state at the end of chapter 3 contains the mistakes found later. If the skill is any good, it finds them there.

| Mistake, and who found it | Found by the skill? |
|---|---|
| The circle lending → fees → membership → lending, called harmless (found in chapter 4) | Yes, as blocking |
| Nobody asked whose rule the €10 block is (C-19, found by the maintainer) | Yes, as blocking, with the question almost word for word |
| "Amount owed" from `fees` in the glossary of `membership` | Yes, as evidence for the same finding |
| An unblock can lift a block placed by someone else (the first ADR 5) | Yes |

This is less than it looks. The skill was written by the agent that knew these mistakes, and its rules are the lessons of chapters 3 and 4. We replaced the examples from the library by examples from other domains, but the test can only show that the rules find what they were written for. The better evidence is what the run found besides them: that a lost copy never leaves the catalogue, that nobody owns the usage fee, that the open host services are justified by a count of consumers, and that a reader who pays at the desk stays blocked for a while. Nobody had noticed these in chapter 3 or 4. The [evaluation](../docs/reviews/README.md) lists both.

## The run on the current cut

The second run took the state after chapter 4. Its [report](../docs/reviews/ch04-context-cut.md) first says what holds: every context has a decider, decisions and words of its own; the dependencies form no circle; the €10 rule has one owner; both anti-corruption layers translate something real; none of the likely changes in the brief touches three contexts.

It then found seven points, none of them blocking. Four had already come up in the run on chapter 3 and were still open (lost copy, usage fee, the open host services, payment at the desk); three were new, among them a mistake of chapter 4. The agent that drew the cut checked the quoted evidence of each; it is correct.

| Finding | What we did |
|---|---|
| A lost copy leaves the collection (C-04), but nothing in the model takes it out; letting `catalogue` react to `lending` would bring back a circle | Business question, **C-20** |
| No context owns which copies carry a usage fee, or how much it is | Business question, **C-21** |
| The Big Picture board still shows the plain block orders that ADR 5 rejected, the money threshold in `membership`, one central clock, and "Fine Paid" as the only payment | Board corrected, except one clock card and three old arrow labels, which notes now explain; the report question became **C-23** |
| `lending` → `fees` is called an open host service for consumers that do not exist | [ADR 9](../docs/adr/0009-lending-fees-customer-supplier.md): customer–supplier, see below |
| A reader who pays at the desk stays blocked until CityPay confirms | Business question, **C-22** |
| The catalogue's open host service is justified by the number of consumers alone, and a mapping claims a price that lending does not use | Wording corrected |
| No context says which branch a copy belongs to | Business question, **C-24** |

The third finding is a mistake of chapter 4. ADR 5 changed the rule, and the context map and glossaries followed, but the board did not. A new rule in the checks says that a changed rule is looked for on the boards as well.

## The decisions

The maintainer, playing the library, accepted the recommendations before reading the final wording; each entry in the [clarification log](../requirements/clarifications.md) says "given in advance".

- **C-20, lost copy.** `lending` ends the loan and lists the copy for the Head of Collection, as for damaged copies (C-17). The Head of Collection *withdraws* it in the catalogue, and the catalogue publishes that. The arrow stays catalogue → lending; the price is one manual step per lost copy.
- **C-21, usage fee.** Split by the kind of fact: the Head of Collection marks a *usage-fee copy* when registering it; the amount is a *usage-fee tariff* in `fees`. Money stays in `fees`, and `lending` only reports the checkout.
- **C-22, payment at the desk.** A payment is *received* at once and lowers the amount owed, so the hold can be lifted while the reader is still at the desk. It is *confirmed* when CityPay confirms. A rejected payment is cancelled, and the €10 rule places the hold again. This refines C-02.
- **C-23, monthly report.** Every kind of charge, shown by kind: charged, paid, waived, outstanding. Who may waive what stays parked (C-16).
- **C-24, home branch.** Every copy has a home branch, set by the Head of Collection; where the copy is right now is the business of `lending`. A return at another branch is decided with C-14.

## What changed in the model

- **Glossaries.** `catalogue`: *home branch*, *usage-fee copy* (with *special collection* as the word to avoid), *withdrawn copy*. `lending`: *lost copy*, *damaged copy*, and a copy is on the shelf at one branch. `fees`: *usage-fee tariff*, *monthly report*, and a *payment* is received, then confirmed; *item* is avoided.
- **Mappings.** The catalogue events carry the home branch and the usage-fee mark and announce a withdrawn copy. The loan events no longer report a usage fee. The CityPay translation knows received and confirmed. The catalogue's open host service is now justified by what it is: one format for titles and copies, offered to whoever needs it instead of being negotiated with each consumer; `lending` and `fees` take different parts of it.
- **Board.** The two policies now place and lift the hold "unpaid fees"; *Card Blocked* carries no amount; *Payment Received*, *Payment Confirmed by CityPay*, *Charge Waived* and *Copy Withdrawn* are there; lost and damaged copies feed a list that the Head of Collection reads. Notes say what was done by hand before (blocking, keying payments into CityPay) and that each daily check belongs to the module that owns its rule (ADR 6). The board still has one clock card in the `lending` area and the old arrow labels "then block", "then unblock" and "is keyed in by hand": an arrow can be neither edited nor removed, and removing a card leaves its arrows behind (tool gaps 12 and 13 in [`docs/tool-gaps.md`](../docs/tool-gaps.md)).

The dependencies did not change: `catalogue` and `membership` use no other module, `lending` uses those two, `fees` uses all three.

## The pattern between lending and fees

`lending` → `fees` was drawn as an open host service with a published language. Chapter 3 gave as reason that "Reminders and the reader account will need the same events". Since then, reminders stayed inside `lending` and the account page asks the modules instead of listening (ADR 8). `fees` is the only consumer, and its needs shaped the events (due date for the running fine, the loss). That is what chapter 3 itself calls customer–supplier.

Because it revises a pattern approved in chapter 3, it was prepared as [ADR 9](../docs/adr/0009-lending-fees-customer-supplier.md) with two options: customer–supplier, or keeping the open host service with a stable contract as its reason. The maintainer followed the recommendation: **customer–supplier**, because a pattern should describe the relationship we have, not one we might have later. In the model the two mappings (open host service and published language) became one customer–supplier mapping. The dependencies did not change, and the loan events stay events (ADR 4).

## A second run on our own answers

Answers to a report can bring new problems, so the skill ran once more on the result. It found no new circle, no money in `catalogue` and no rule with two owners, and it confirmed that the path of a lost copy runs through a person and a list, not through a dependency. It found six points in our own work:

| Finding | What we did |
|---|---|
| The board did not apply our own rules: lost-book and usage fees did not trigger the hold, a payment rejected by CityPay had no event, the usage fee did not reach the report | Board corrected: *Payment Cancelled (rejected by CityPay)*, and arrows from every charge to the hold policy, the report and the reader account |
| "Paid" has two meanings in `fees` since C-22, and the report's "outstanding" is not the amount owed | *Amount owed* now says "no payment received"; what the report counts is parked as **C-26** (modelling `fees`) |
| A catalogue mapping said lending takes *availability* from the catalogue, which chapter 3 rejected; chapter 3's table still had the old reasons | Mappings and the table in chapter 3 corrected |
| After C-20, a damaged copy has two places that decide about it, and C-17 no longer fits | **C-25**: the Head of Collection withdraws *or releases* a damaged copy in the catalogue; *Copy Released (after repair)* is on the board. It amends C-17, so it went to the maintainer, who followed the recommendation |
| The usage fee depends on two streams of events meeting in `fees` in the right order | Parked with the open question on the mark as **C-27** (modelling `catalogue` and `fees`) |
| C-24 brings a second branch to the per-branch overdue limit | Added to the parked C-14 |

The first finding is the same kind of slip as in chapter 4, although we had just added a check for it. The check said "look for the old rule on the board"; it did not say "follow the rule's own triggers". It says so now.

## What we take with us

- The cut has now been challenged twice by a reader who did not draw it. What it found is fixed, decided or parked with the moment it has to be decided.
- The skill runs again whenever the cut changes and before every gate that builds on it (`CLAUDE.md`, `close-chapter`).
- Still parked: C-11 to C-16, C-26, C-27, the mail gateway.
- **Gate G1 (spec-driven development) comes next.** Nothing per context starts before it.

## Decisions in this chapter

- **Business**, decided by the maintainer playing the library: C-20 to C-24, recommendations accepted in advance. Recorded in the [clarification log](../requirements/clarifications.md); C-22 refines C-02, the return at another branch is parked with C-14. C-25 (damaged copies, amends C-17) decided 2026-10-24, recommendation accepted. **Parked:** C-26, C-27, and an addition to C-14.
- **Architecture:** [ADR 9](../docs/adr/0009-lending-fees-customer-supplier.md) accepted by the maintainer (2026-10-24): `lending` → `fees` is customer–supplier.
- **Way of working**, approved by the maintainer in the conversation that led to this chapter (the skill was merged with PR #10): the cut is challenged by a fresh agent with the `challenge-context-cut` skill before every gate that builds on it and whenever it changes; its reports go to [`docs/reviews/`](../docs/reviews/README.md). New checks: a changed rule is looked for on the boards, including its own triggers; a claim that something is new is checked against earlier reports; an approval names where it was given.

---

*The boards live in the DDD Studio workspace "Millbrook Library (tutorial)". Saved versions: `ch5-big-picture-after-challenge` to `-v4` (Big Picture), `ch5-context-map-after-challenge` to `-v4` (model). Exports: [`model/sketch/big-picture-contexts.json`](../model/sketch/big-picture-contexts.json), [`model/esdm/`](../model/esdm/).*
