---
status: "proposed"
date: 2026-10-26
decision-makers: the maintainer
consulted: none recorded
informed: none recorded
---

# 12. A published contract changes by addition; anything else is a new fact beside the old one

## Context and Problem Statement

[ADR 4](0004-contexts-talk-through-published-events.md) says that a published event is "changed only by adding to it" and announces a record on how events change over time. [ADR 11](0011-what-every-published-event-carries.md) fixed the envelope and left the rest, saying that the versioning of events "is written when the first event is specified in chapter 7". Chapter 7 specified them: thirteen events that cross a boundary, two orders and six questions, each with a payload schema in the model.

The contracts will change. The usage fee (scenario F) adds a charge to the checkout; the release of a damaged copy (H) adds an event to the catalogue; the notices (J2) need an address; a new reader group may change what a restricted copy means. Each of these touches a contract that another module already relies on. What is a change that a consumer survives without being touched, and what must the owner do for every other change?

The technology decides how events are delivered and kept (gate G2). This record must hold whatever it chooses, so it speaks only of the contract.

## Decision Drivers

* A module is worth having only if one can change it without touching the others. A contract that can be changed freely makes every consumer a co-owner.
* ADR 9 says the supplier "tells the customer before it changes" an event. That needs a place where the consumers are listed. The model and its export hold the schemas but not the consumers (Studio does not return descriptions, tool gap 23), so the list is `model/contracts.md`, which `scripts/check_repo.py` compares with the export.
* There is one deployable unit (ADR 2). Publisher and consumer can be changed in one commit, but that is a convenience of the day, not a rule worth building the modules on.
* Whether events are stored, and for how long, is not known before G2. A rule that only works while no event is stored would have to be redone.
* Few rules. A rule the team has to look up for each change is not followed.

## Considered Options

1. Additions only; anything else is a new fact beside the old one
2. A version in every event, and the consumer converts old versions
3. Change publisher and consumers together; no compatibility
4. Additions only, and an incompatible change in one commit while there is one unit and nothing is stored

## Decision Outcome

Recommended option: "Additions only; anything else is a new fact beside the old one", because it needs no machinery, works for events that are stored and for those that are not, and keeps the consumers independent, which is the reason for the modules.

**Compatible changes**, which an owner makes without asking anyone:

* a new field in a published event, command or query result. Consumers ignore fields they do not know;
* a new published event for a situation that had none. Consumers ignore events they do not know;
* a new optional field in an order or a query parameter.

**All other changes** are not compatible. They are: removing, renaming or retyping a field; changing what a field means, its unit or its format; making an optional field required; splitting or merging events; changing the envelope of ADR 11; and adding a value to an enumeration, unless the contract names the safe default of every consumer that decides on it (see below). For these:

* the owner publishes a **new fact under a new name** (not a version suffix; a name that says what happened, as with any event) beside the old one, and keeps publishing both;
* the owner updates the contract in the model first (the event, the mapping, the contract table), naming each consumer that has to move, and tells them (ADR 9);
* when the last named consumer has moved and its change is released, the owner stops publishing the old fact and removes it from the model.

**Enumerations.** A consumer that decides on a value says in the contract what it does with a value it does not know, and it chooses the safe side: an unknown copy kind is not lendable. Adding a value is compatible if the contract names that default for every consumer that decides on the value; otherwise it is incompatible. A list that changes for business reasons (the four branches) is not made an enumeration of the contract: the events carry the branch as text, and the owner of the list is named when it first changes.

**Orders and questions** follow the same rules, with callers in place of consumers.

**Stored events.** If events are stored (gate G2), each stored event stays readable under these rules. Nothing here lets an owner rewrite stored events; how stored events are read after an incompatible change is decided with the storage.

**Where the contract lives.** The schema is in the model in DDD Studio and in its export. The owner, the consumers and the rules for late and repeated events are in `model/contracts.md`, checked against the export by `scripts/check_repo.py`. The check that the code still matches both belongs to the build phase (`check-model-code`).

Not decided here: the format and transport of events, how long both facts are published, and how stored events are migrated (gate G2).

### Consequences

* Good, because compatible changes are free and the common ones (a new field, a new event) are compatible.
* Good, because an incompatible change is visible in the model as a second fact with a named list of consumers, instead of a surprise in someone else's tests.
* Good, because every change starts in the model (the rule of this repo: Studio first).
* Bad, because during a transition two facts are published for one thing, and a consumer that listens to both must not count twice. The contract says which one a consumer follows; it follows one of them.
* Bad, because "the last consumer has moved" needs an up-to-date list of consumers. `model/contracts.md` holds it; the check finds a missing row, not a wrong one.
* Bad, because a field that is carried "for later" (the usage-fee mark and the reason of a hold travel today although no consumer uses them yet) costs a little in every event. The first driver of ADR 11 pays for it: a field added later is missing from every event already published.
* Neutral, because the cheaper rule of option 4 is the same rule with one exception that can be added later. The record recommends not to start with the exception: it works only while nothing is stored and only one unit exists, and it is the exception that gets used.

## Pros and Cons of the Options

### Additions only; anything else is a new fact beside the old one

* Good, because it needs no version handling in the consumers and no conversion code.
* Good, because the old fact keeps working until its consumers choose to move.
* Bad, because two facts exist for a time, and the owner carries the old one.

### A version in every event, and the consumer converts old versions

* Good, because a stored event of any age can be read by converting it.
* Good, because the event keeps its name.
* Bad, because every consumer carries conversion code for every version of every event it reads, forever, and each conversion is a place for a mistake.
* Bad, because it solves a problem (stored old events) that we do not know we have before gate G2.

### Change publisher and consumers together; no compatibility

* Good, because it is the cheapest rule while there is one unit, nothing is stored and every change is small.
* Bad, because it makes the modules co-owned in practice: a change in `lending` has to be released with `fees`, and the supplier no longer "tells the customer before" but changes the customer's code.
* Bad, because it fails at the first stored event, and the rule would have to be replaced with another then.

### Additions only, and an incompatible change in one commit while there is one unit and nothing is stored

* Good, because the common change costs nothing and the rare incompatible one costs a commit, not a transition.
* Good, because nothing in it has to be unlearned when a second unit or a stored event comes: the rule of option 1 then applies unchanged.
* Bad, because it makes "tells the customer before it changes" a review comment. It turns the supplier into the author of the customer's change.
* Bad, because the moment at which the exception ends (the first stored event, the second deployable) has to be noticed by someone; the check does not see it.
