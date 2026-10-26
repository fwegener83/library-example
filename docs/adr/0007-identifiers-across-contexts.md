---
status: "accepted"
date: 2026-10-23
decision-makers: the maintainer
consulted: none recorded
informed: none recorded
---

# 7. Identifiers across contexts are issued by the owner

## Context and Problem Statement

ADR 4 lets modules refer to each other's things only by identifier. Three things cross the boundaries all the time: the person (member in `membership`, reader in `lending` and `fees`), the copy, and the title.

For the person, the brief offers the card number: "you get a card number, and you're a member" (§3.3). But a card is valid for a year, is renewed and can be blocked (§3.3), and the brief does not say whether the number stays when a card is replaced. A person who owes money must stay the same person when the card changes.

For copies and titles the brief names a barcode and an ISBN (§3.1). Whether those are stable enough to serve as identity (a replaced barcode label, two editions of one title) is not in the brief and is a question for the modelling of `catalogue`.

Who issues the identifiers that cross the boundaries, and what is the identity of a person?

## Decision Drivers

* ADR 4 lets modules refer to each other's things only by identifier.
* A person who owes money must stay the same person when the card changes.
* A card is valid for a year, is renewed and can be blocked (brief §3.3).
* The brief does not say whether the card number stays when a card is replaced, nor whether barcode and ISBN are stable enough to serve as identity (§3.1).

## Considered Options

* The owning module issues the identifier; every other module only stores it
* The card number is the identity of the person

## Decision Outcome

(Added with [ADR 11](0011-what-every-published-event-carries.md): `lending` also issues the identifier of a loan and of a damage report, and every published event names its subject by such an identifier.)

Chosen option: "The owning module issues the identifier; every other module only stores it", because a person must stay the same person when the card changes, and the card number belongs to a card that is renewed and can be blocked.

* **Member:** `membership` issues a member number at registration. The card number is an attribute of the card, not the identity of the person.
* **Copy and title:** `catalogue` issues their identifiers. Whether it uses the barcode and the ISBN for that, or its own numbers with barcode and ISBN as attributes, is decided when `catalogue` is modelled.

### Consequences

* Good, because no module has to look up or guess another module's identifiers.
* Neutral, because `lending` and `fees` speak of a *reader* but store the *member number*. The word changes at the boundary, the identifier does not.
* Neutral, because if the business wants the card number to be the member number, that is a decision of `membership` alone.

## Pros and Cons of the Options

### The owning module issues the identifier; every other module only stores it

* Good, because no module has to look up or guess another module's identifiers.
* Good, because the person stays the same when the card changes: the card number is an attribute of the card.
* Neutral, because for copies and titles it is open whether barcode and ISBN or own numbers are used; that is decided when `catalogue` is modelled.

### The card number is the identity of the person

The brief offers the card number: "you get a card number, and you're a member" (§3.3).

* Good, because the brief names it.
* Bad, because a card is valid for a year, is renewed and can be blocked, and the brief does not say whether the number stays when a card is replaced.
