---
name: plan-scope
description: Prepare the choice of the first increment (phase 4, the delivery scope) after the cut into contexts has been challenged. Use when asked to "plan the scope", "choose the first increment", "what do we model and build first", or at the gate between the cut and the detailed modelling. Produces candidate scenarios with the contexts and boundaries each one touches, the open rules it pulls in, options for the scope and a recommendation; it never decides the scope.
---

# Plan the delivery scope

Discovery covers the whole target picture; the cut was made for all of it.
Detailed modelling and building cover a part. Which part is a business
decision. This skill prepares it, so that the human chooses between
options and does not start from a blank page.

## Rules

- **Stop at the gate.** The scope is chosen by the human (the gate of the
  plan). Until then nothing is modelled in detail and nothing is built for
  a scenario that is not yet in scope.
- **Sources, not memory.** A scenario comes from a domain story, an event
  on the Big Picture board or a sentence of the brief. Each row quotes
  where. A scenario that is only inferred says so.
- **Boundaries decide the cost.** The size of a scenario is the number of
  contexts it touches, the boundaries it crosses and the rules still open,
  not the number of screens.
- **Test the cut, not only deliver.** The detailed modelling is also the
  test of the cut (phase 5). A scope that leaves out the hardest
  boundaries postpones the test; say so.
- **Business before technology.** Open rules that a scenario pulls in are
  asked as clarifications (decide them if the maintainer delegated them,
  otherwise ask), not assumed.
- **Say what is left out and why.** The increment is a cut through the
  scenarios; what stays outside is named, with the reason, so that nobody
  finds it missing later.

## Inputs

- the brief, the clarification log (decided and parked questions),
- the domain stories and the Big Picture board (events in time order),
- the context map, glossaries and mappings, the architecture records,
- the latest report of `challenge-context-cut` (its "consequences for the
  scope" are an input, not a decision).

## Steps

1. **Collect candidates.** One row per business capability that a person
   in the brief relies on or asks for (the "what people rely on" list, the
   stories, the Big Picture events). Split a row when its parts have
   different owners or different open rules.
2. **For each candidate:** the contexts it touches; each boundary it
   crosses, in which direction and with which kind of contract (fact,
   order, question); open rules from the log that it pulls in; what it
   needs from other candidates; and a size (S, M, L) with the reason.
3. **Order by need.** Which candidate cannot work without which other.
   This is a build order, and it must be acyclic.
4. **Form two to four options.** Each option is a set of candidates.
   Include one that is as small as is useful and one that is wide; do not
   include an option that skips a prerequisite. For each: what it
   delivers, what it tests of the cut, what it leaves out, what it costs
   in chapters and in open questions.
5. **Recommend one** and say what would change the recommendation. Name
   the strongest argument against it.
6. **List the open questions the scope decides** (for example a parked
   clarification marked "decide in the scope") and propose an answer to
   each.
7. **Write it up** as the chapter of the scope decision, with a box
   "Decisions in this chapter" that says the gate is open. Do not mark
   the chapter ready and do not go on to the detailed modelling.

## After the decision

Record who decided what and what was rejected (log of decisions, plan,
chapter). The accepted scope becomes the list of scenarios that the
detailed modelling covers; each later chapter says which of them it
models.
