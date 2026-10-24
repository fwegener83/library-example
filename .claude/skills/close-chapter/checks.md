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
- A claim that something is **new**, "not known before" or "found for
  the first time" is checked against the earlier reports in
  `docs/reviews/` and the logs. (Chapter 5 first said none of seven
  findings was known; the chapter 3 report already had four of them.)
- "Approved by the maintainer" names where: the conversation, a PR, a
  log entry. Scope words in the source ("before reading the final
  wording", "of the serious ones") are kept, not rounded up.

## Context map and architecture

- Read the map for **dependencies**, not only for message flow: whoever
  reacts to an event or calls an API depends on the publisher's types.
  The script warns about circles; a circle must be resolved in an ADR
  before the map is called done. (Chapter 3 called a circle harmless; it
  was found in chapter 4.)
- ADRs say what a technology must provide, never which one, while gate G2
  is open.
- A record that changes an earlier chapter says which chapter, and the
  chapter is corrected in the same pull request.
- A record or clarification that changes a rule is checked against the
  **boards** too: every card that states the old rule is updated or gets
  a hotspot pointing to the record, in the same pull request. (After
  ADR 5 the Big Picture still showed "block the card" orders and the
  money threshold in `membership`; found by `challenge-context-cut`.)
  Read the rule's own text for its triggers ("whenever a charge is
  made", "every kind of charge") and check that each one has an arrow
  on the board. (Chapter 5 renamed the policies but left lost-book and
  usage fees without an arrow to the hold; found by the second run.)

## Proposals and decisions (every chapter)

- Words match status: a heading "The decisions" over proposed records,
  or "known" for something that depends on an open decision, is an
  overclaim. Say "proposed" in the heading and in the summary line.
- A rule that sounds technology-neutral may still fix a technology
  ("after commit", "foreign keys", "same database"). Read each rule once
  as "which gate would own this word?".
- A claim that something can be changed or split later names what that
  costs (failure handling, retries), not only what stays.

## ADRs (`docs/adr/`, MADR format, checked by the script)

- Title `# N. <decision>`, a metadata block (`status`, `date`,
  `decision-makers`, `consulted`, `informed`), then Context and Problem
  Statement, Decision Drivers, Considered Options, Decision Outcome with
  Consequences, Pros and Cons of the Options. Confirmation and More
  Information only where there is something to say. ADR 1 fixes the list;
  the script reads the same list.
- Every considered option has a heading of the same name under Pros and
  Cons of the Options, with the reason it won or lost.
- Status is one of `proposed`, `accepted`, `rejected`, `deprecated`,
  `superseded by ADR-N`, and it is the same in the file and in the index.
  "Needs a choice" goes into the index and the chapter, not into the status.
- A `proposed` record says "Recommended option: …, because …" in its
  Decision Outcome, an `accepted` one says "Chosen option: …, because …".
  When the maintainer approves a record, status, index and that sentence
  change in the same commit.
- A statement in a record comes from the brief, a clarification, the
  chapter text or another record. Do not add arguments to fill a section;
  keep an empty section short and say so in the PR.
- A record that moves a business rule between contexts, or turns an
  arrow on the context map, first names whose rule it is and cites the
  clarification that decided it. The technical reason (a circle, a
  check) comes second. (The first ADR 5 argued from the circle alone and
  picked the arrow that was easiest to turn; C-19 came only in review.)
- Read each glossary for words of another context. If `membership`
  defines a word through an amount of money, money has leaked in.
  (The block definition used "amount owed" from `fees` until ADR 5.)
- Write a record only when there is something concrete to decide. A rule
  for things that do not exist yet (no event specified) is a line in an
  existing record, not a record of its own. (ADR 9 was written and
  withdrawn in chapter 4 for this reason.)
- When the record format or any other convention changes, search the
  whole repo for its name, its section names and its source (chapters,
  index, skills, checks, script), not only the files that come to mind.
  Fix the script and this list in the same commit.

## Decisions box (every chapter, checked for presence by the script)

- Every decision named in the box exists in the log it points to, with
  the same status (decided, proposed, parked). The box says who decided.
- Nothing is called decided in the box that is only proposed in the log.
- Choices that belong to review (wording, colours, field names) are not
  listed as decisions.
