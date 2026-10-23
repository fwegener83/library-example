# Heuristics for challenging a context cut

Each section is a lens with test questions and what counts as a finding.
Sources are named so that a finding can say where the test comes from.

## 1. Canvas: does each context have a reason to exist?

Use the fields of the **Bounded Context Canvas** (DDD Crew, Nick Tune):
name, purpose, strategic classification (core, supporting, generic),
domain roles, inbound and outbound communication, ubiquitous language,
business decisions, assumptions, open questions.

- Can the purpose be said in one sentence in the business's words?
- Which **decisions** does the context make on its own? A context that
  makes none, only stores or passes on, may not be a context at all.
- Does it have at least one of: a language of its own, a decider of its
  own (a person or role in the brief), a pace of its own (changes for
  different reasons or at a different rate)? "It is a team" or "it is a
  noun" is not a reason.

## 2. Language: where does the meaning change?

A bounded context is the boundary within which a model and its words
have one meaning (Evans, *Domain-Driven Design*, 2003, ch. 14).

- **Same word, different meaning across contexts** is expected and a
  good sign for the boundary. Check the glossaries say so (`avoid`
  entries, cross-references).
- **A word of context A inside a definition of context B** is a leak. B
  then has to understand A's concept, and A cannot change it alone.
  Typical leaks: a status of another context's object, another
  context's threshold, a quantity only another context can compute.
- **One word with two meanings inside one context** means the context
  is two models, or the word needs splitting.
- **Two words for one thing inside one context** blurs the language.
- Words in the brief that no glossary owns are a gap.

## 3. Ownership of rules: whose rule is it?

The owner of a business rule is the party that decides it and may
change it (threshold, exceptions, purpose). Who does the work today is
evidence, not proof.

For each rule that involves more than one context:

- Which context *decides*, and which only *executes* or *reacts*?
- Where is it written (brief, clarification)? If nowhere, the owner is
  an open business question, not an architecture choice.
- Is the rule **split**: the reason computed in one context, the
  threshold or the decision in another? That is strong *functional
  coupling* across a large distance (Khononov, *Balancing Coupling in
  Software Design*, 2024): every change to the rule touches both sides.
- Can one party undo the effect of another's decision (a "resume" order
  lifting a suspension set by a different party)? Then the effect needs to carry
  its owner.

## 4. Dependencies: read the map as a build, not as a flow

- A context that **reacts to an event or calls an API depends on the
  publisher's types.** "Only events" does not remove the dependency; it
  only makes it asynchronous.
- Draw the graph upstream → downstream from every mapping and every
  subscription. A cycle breaks the **Acyclic Dependencies Principle**
  (Robert C. Martin): none of the contexts in the cycle can be built,
  tested or separated without the others.
- A cycle in the *business flow* is normal (a booking earns loyalty
  points, the points change the price of the next booking). Only a cycle in the
  *dependencies* is a finding.
- Check direction against ownership (§3): the arrow should follow who
  owns the rule, not what is easiest to turn.

## 5. Scenarios: play it through

Pick concrete cases from the brief and the Domain Stories, and trace
them across all contexts.

- At least one **timing** case: two things at once, a message that
  arrives late or twice, a deadline that passes during a process.
- At least one **exception** the brief mentions.
- Count **boundary crossings** and **round trips** (A asks B, B asks A
  back). Many crossings or a question before every action ("may I?")
  suggests the boundary cuts through a decision.
- **Change scenarios:** name three changes the brief makes likely (a
  threshold, a new channel, a new kind of customer, a replaced external
  system). Count how many contexts each one touches. A likely change
  that touches three contexts is a finding.

## 6. Patterns and anti-patterns

Mapping patterns (Evans 2003; *DDD Reference* 2015) must be real:

- **Customer–supplier**: the customer's needs are negotiated and the
  supplier plans for them. Without anyone negotiating, it is a
  conformist relationship with a nicer name.
- **Open host service / published language**: worth it for several
  consumers or a stable public contract, not for the count of consumers
  alone.
- **Anti-corruption layer**: there is something foreign to translate.
- **Shared kernel / partnership**: if two contexts share types or must
  release together, name it; hidden, it is the worst of both.

Anti-patterns to look for:

- **Entity service**: one context per noun (a "book service"), with the
  behaviour spread over its callers.
- **Pass-through context**: receives and forwards, makes no decision
  (§1).
- **God context**: most words and most decisions in one place; the
  others are satellites.
- **Split rule**: §3.
- **Chatty boundary**: §5, many crossings for one business step.
- **Cut by technology or legacy**: a context for "notifications",
  "reports" or "the old system" with no business decision of its own.
- **Dependency cycle**: §4.
