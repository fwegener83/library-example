---
name: design-context-contracts
description: Specify the contract on every boundary that the delivery scope crosses (phase 5, first the boundaries). Use when asked to "design the contracts", "specify the events between the contexts", "what does this edge carry", or once the flows across the contexts exist. Produces one contract per crossing (kind, owner, payload schema, behaviour when late or repeated, who may change it), the rule for changing events over time, and the findings that test the cut; it does not model the inside of a context.
---

# Design the contracts on the boundaries

The contexts are separate only if what crosses between them is stated.
The flows show where something crosses; this skill states what.

## Rules

- **One contract per crossing.** The crossing table of `model-flows` is
  the list. A crossing without a contract is not done; a contract without
  a crossing is not needed.
- **The owner decides.** The upstream side owns the shape; the
  downstream side translates it into its own words (see the mapping
  pattern on the edge). A downstream wish is a request, not an edit.
- **Kind follows what it is.** A fact that happened in the publisher is
  an event. An order to another context goes to a public command of the
  owner of the thing to change. A question for a screen is a query, not
  an event. Pick the kind from the meaning; the technology is chosen later.
- **Small and complete.** A payload carries what the consumer needs to
  act without asking back, and nothing that only the publisher's inside
  needs. Anything the consumer would have to ask back for is a finding.
- **Say what late and twice means.** Every contract states what the
  consumer does when the event arrives twice, late, out of order, or
  names something the consumer does not know yet. The architecture
  records set the common envelope; a contract adds only what is specific.
- **Evolution is part of the contract.** Fields are added, not changed
  or removed; the rule for anything else is written once, in an
  architecture record, and every contract points to it.
- **No hidden second contract.** Everything a consumer relies on is in
  the contract: the payload, its meaning, the business time of the fact.
- **Business before technology.** No transport, format or storage here.

## Inputs

- the crossing table and the flows from `model-flows`,
- the context map and mappings, the glossaries,
- the architecture records on events, orders and identifiers,
- the requirements log (every rule a payload field serves).

## Steps

1. **One row per crossing.** Kind, name, owner (publisher or callee),
   consumers, trigger (which fact or decision makes it happen).
2. **Payload.** Field by field: name, meaning in the owner's language,
   example from the sources, and which consumer rule needs it. Fields
   that no consumer rule needs are removed.
3. **Behaviour.** Per consumer: what it does on the event, what on a
   repeat, what on a late one, what on an unknown reference. Where a
   reaction can fail, say what the owner of the order sees.
4. **Record it in the model.** Payload schemas on the event or command
   nodes; the reason, the kind and the consumer reactions in the
   description of the node and of the mapping. The model is the source;
   the chapter shows a table made from it.
5. **Write the evolution rule** as an architecture record if none exists,
   and check each contract against it.
6. **Test the cut.** Per contract: can the consumer act with what it
   gets? Does a consumer need data of the owner at the moment of its own
   decision? Do two contexts both claim to own a field? Does a contract
   need two meanings of one word? Each yes is a finding; do not repair it
   in the contract. Hand it to the human with the contract as evidence.
7. **Hand over** the contract table, the findings, the open business
   questions as clarifications, and what is left to the inside of each
   context.

## What it does not do

It does not decide how events are delivered, stored or versioned on the
wire, and it does not model what happens inside a context.
