---
name: model-flows
description: Model the processes of the delivery scope across the bounded contexts (phase 5, first the boundaries). Use when asked to "model the flows", "draw the process across the contexts", "which scenario crosses which boundary", or after the delivery scope is decided and before the inside of any context is modelled. Produces one flow per scenario in the modelling tool, a table of the boundary crossings and the findings that test the cut; it does not design the contracts and does not model the inside of a context.
---

# Model the flows across the contexts

A flow is one example run of a scenario, left to right in time, like a
sequence diagram. It is the cheapest test of the cut: a process that
fits no boundary shows it here, before anything is built. This skill
draws the runs and collects the crossings. `design-context-contracts`
turns each crossing into a contract.

## Rules

- **Only the decided scope.** The scenarios come from the record of the
  scope decision. A scenario outside it gets no flow.
- **Sources, not memory.** Every step comes from a story, a board event
  or a rule of the requirements log. A step that is only inferred says so
  in its description.
- **Boundaries first.** A flow shows what crosses a boundary and who owns
  each side. Aggregates, commands, events and policies are real model
  elements, as many as the flows need. Invariants, scenarios and the
  commands that touch no boundary follow when the context is modelled in
  detail; the aggregate is then refined, not replaced.
- **Business before technology.** A flow names facts, orders and
  questions in the words of the contexts. It names no queue, table or
  endpoint.
- **A flow that goes back and forth is a finding.** Do not hide it by
  adding steps.
- **Report what the run showed, not that it ran.** A clean validation is
  not a good flow.

## Inputs

- the decision record of the scope, with the scenarios and what each one needs,
- the stories and board events in time order, the requirements log,
- the context map, glossaries and mappings, the architecture records
  (what a module may call, what an event carries),
- the modelling tool's own guide to flows and slices (read it first).

## Steps

1. **List the runs.** One flow per scenario of the scope, in build
   order. Add a second run where the same scenario has a different path
   across the boundaries (for example the late case); the exception
   path is where cuts break.
2. **Create the elements.** For every aggregate, command, event, policy
   and read model the run needs: the node under its owning context, with
   the fields the run needs. Name events as past-tense facts of the owner.
   Wire the references before grouping them into steps.
3. **Draw the steps.** One step per command or per reaction, in time
   order, with concrete example data from the sources. A reaction in
   another context is a policy or handler of the *consumer*; its owner is
   the consumer.
4. **Fill the crossing table** (one row per crossing, kept in the
   chapter): scenario, step, from context, to context, kind (fact, order,
   question), the name, who reacts, and whether the reaction may arrive
   late or twice.
5. **Test the cut.** Check the abort criteria of the phase model on every
   flow and write down the result per flow, also when nothing was found:
   an invariant that needs data of two contexts at the same moment; a
   policy without a clear owner; a flow that goes back and forth between
   two contexts; an aggregate that needs the state of another context to
   decide; a word that needs two meanings in one context.
6. **Stop on a finding.** A criterion that is hit is not repaired in the
   flow. Prepare the finding with the flow as evidence and hand it to the
   human; the cut is not changed on the side.
7. **Hand over.** The crossing table, the findings (or "none, and why we
   looked where we looked"), the open business questions as clarifications.

## What it does not do

It does not decide the kind or the schema of a contract, and it does not
describe the rules inside a context. Both come later.
