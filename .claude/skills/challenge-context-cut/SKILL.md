---
name: challenge-context-cut
description: Challenge the cut into bounded contexts and the context map before anything is built on it. Use at the end of strategic design, before a gate or chapter that builds on the cut, after a context is added, merged or split, after a mapping is turned, or when asked to "challenge", "stress-test" or "review the domain cut / context cut / context map". Produces findings with evidence and alternatives; it never changes the model.
---

# Challenge the context cut

The cut is the decision that is most expensive to undo later. DDD Studio
draws it, but it does not argue with it. This skill does.

The heuristics are in `heuristics.md` in this folder. Read it first.

## Rules

- **Independent.** Run the challenge in a fresh agent that gets only file
  paths and this skill, not the reasoning of whoever drew the cut. The
  author defends the cut without noticing. In chapters 3 and 4 the
  fresh reviews found more than the author.
- **Evidence or silence.** Every finding quotes the file and the passage
  it is based on. A finding without a quote is not reported. "Could be
  a problem some day" is a note, not a finding.
- **Business before technology.** When a rule crosses a boundary, the
  question "whose rule is it?" comes before "which way do the
  dependencies point?". Do not let the cheapest technical fix decide who
  owns a rule.
- **Propose, do not decide.** The skill changes nothing in Studio or in
  the repo except its own report. Every serious finding comes with at
  least one alternative and what that alternative costs. Questions of
  business go out as draft clarifications (`C-nn`), questions of
  architecture as proposed ADRs (status `proposed`, with a recommended
  option). The maintainer decides
  (`docs/decisions.md`).
- **Say what holds.** A report that finds only faults is not believed.
  Name the parts of the cut that survive the tests and why.

## Inputs

Read the current state, from Studio or from the exports, whichever is
newer (exports are what a review can quote):

- the brief `requirements/brief.md` and the clarification log
  `requirements/clarifications.md`,
- contexts, subdomains, glossaries and mappings: `model/esdm/` (or Studio:
  `get_model_overview`, `list_mappings`, `get_node`),
- the Big Picture board with its areas: `model/sketch/`,
- the Domain Stories: `model/domain-stories/`,
- the chapter that drew the cut and any ADRs in `docs/adr/`.

## Steps

1. **Canvas.** For each context write a short Bounded Context Canvas
   (heuristics §1): purpose, classification, the decisions it makes,
   what it receives and sends, its words. Leave a field empty rather
   than invent it. A context whose purpose and decisions stay empty is
   already a finding.
2. **Language** (heuristics §2). Compare the glossaries with each other
   and with the brief. Look for words of one context inside another
   context's definitions, one word with two meanings in one context, and
   two words for one thing.
3. **Ownership of rules** (heuristics §3). List every policy, invariant
   and threshold that involves more than one context. For each: who
   decides, who may change it, where the source says so. A rule split
   over two contexts, or owned by nobody in the sources, is a finding.
4. **Dependencies** (heuristics §4). Build the dependency graph from the
   mappings *and* from who reacts to whose events. Report every cycle,
   even when every arrow is "only an event".
5. **Scenarios** (heuristics §5). Play three to five concrete cases
   through all contexts, at least one with timing (two things happen at
   once, or late) and one exception from the brief. Count boundary
   crossings and round trips. Then name three changes the brief makes
   likely and count how many contexts each one touches.
6. **Patterns and anti-patterns** (heuristics §6). Check that each
   mapping pattern is real (a customer–supplier has a negotiation, an
   anti-corruption layer translates something) and look for the
   anti-patterns.
7. **Alternatives.** For each serious finding, sketch at least one other
   cut (move the rule, turn the arrow, merge, split) and what it costs.
8. **Report** (format below). Save it as
   `docs/reviews/<label>-context-cut.md` and give the maintainer the
   list of questions.

## Report format

```markdown
# Context cut challenge: <label>

Input: <commit or Studio version>, <files read>
Run by: <fresh agent | author>, <date>

## What holds
- <part of the cut> — <which test it passed>

## Findings
### F1 <one-line claim>
- Severity: blocking | should fix | note
- Lens: language | ownership | dependencies | scenario | pattern
- Evidence: `<file>`: "<quote>"
- Why it matters: <consequence, concretely>
- Alternatives: <option> — costs <…>; <option> — costs <…>
- Level and next step: business (draft C-nn) | architecture (proposed ADR) | review

## Questions for the maintainer
1. <question that only the business or the maintainer can answer>
```

Severity: **blocking** means later work would build on it and become
wrong (a cycle, a rule with two owners). **Should fix** means the cut
holds but a word or mapping is misleading. **Note** means a risk without
a concrete failure yet.

## Not in scope (yet)

- Sharpening the language *inside* one context while modelling it, and
  the cut of aggregates (invariants, consistency boundaries). Both come
  after gate G1, once contexts are modelled in detail. Add them here as
  a second mode then, not as guesswork now.
