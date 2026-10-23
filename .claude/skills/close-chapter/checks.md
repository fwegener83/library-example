# Checks before a chapter goes to review

## Domain Stories

Read every story aloud, sentence by sentence.

- A sentence is **actor – activity – work object – (preposition) – actor**.
  One activity per sentence. The label on the second arrow is only the
  preposition ("to", "for", "in"), never a second verb.
- Work objects have plain names. No rules, numbers or amounts in a name
  ("late fine", not "late fine of 50 cents a day").
- The same thing has the same name in every sentence of a story. Different
  things do not share a name unless that is the finding.
- Places and times are not work objects.
- Pure stories contain no software and no "online".
- Happy path only. Exceptions and limits go into the findings.
- Each handover appears once and goes in the right direction.
- Every finding is derived from the story and the brief, not from memory.

Tool notes: in `edit_domain_story`, `to.label` is the second arrow;
replace a sentence with `remove` plus `sentences` using the same
`sequence`. Board description and settings cannot be changed after
creation, so get them right at creation.

## Big Picture (Sketch board)

- Events are past tense, each with a `src:` tag (brief section) or marked
  `src:inferred`. Wishes are tagged `to-be`.
- A **policy** is "whenever this event, then that command". A rule that
  guards a decision is an **invariant** (`rule:invariant`). The stock
  palette has no invariant card, so the policy card is borrowed.
- Actors, external systems, policies and read models are **connected** to
  their event with a labelled arrow. Position alone is not exported.
- Hotspots are tagged by type: `hotspot:question`, `hotspot:language`,
  `hotspot:scope`, and connected to the card they concern.
- Arrange with `arrange_sketch_board` (timeline, loose cards, no areas)
  only for material this chapter owns. It returns counts only, so look at
  the board afterwards.
- Hotspot and event numbers in the text match the board.

## Clarifications (`requirements/clarifications.md`)

- Every recommendation is tested against the director's goals (brief
  §2) and the purpose of the rule it touches. Ask: is there a reader
  who gets around the rule this way? (Caught too late in C-03: fines
  assessed only on return let a reader who keeps a book escape the
  block.)
- A rejected proposal stays in the entry, with the reason.
- Every decision says who made it and when, and that it is a
  clarification, not the brief.

## Strategic design (contexts, map, glossary)

- Each context has a stated reason: a language break, a different decider,
  or a different pace. "It is a team" or "it is a theme" is not enough.
- Each mapping has a description that says *why* this pattern, and the
  pattern fits the reason (an open host service for the consumer count
  alone is not a reason; a negotiation is customer-supplier).
- Every arrow that leaves an area on the board has a mapping, and every
  mapping has an arrow. Cards of one kind that react to the same events
  (block and unblock) sit in the same area, or the text says why not.
- Claims about "events only", "no call back" and similar in the prose
  match the mapping descriptions word for word.
- Whatever a rejected alternative is said to cause is spelled out
  correctly (partnership, shared kernel).

## Prose against board and brief (every chapter)

- Every quotation is copied word for word from the brief. Search for it;
  do not write it from memory. (The independent review found three
  altered quotes in chapter 3. A script check for this produced twelve
  false alarms on examples and was removed.)
- Every number or count in the text ("a third of", "five events") is
  counted on the board or in the export. No estimated numbers.
- If the text says "all X carry tag Y", count them in the snapshot.
- Do not refer to hotspots by number; refer to them by their question.
  Numbers drift between chapters.
