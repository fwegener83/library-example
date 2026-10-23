# 7. Identifiers across contexts are issued by the owner

Date: 2026-10-23

## Status

Proposed

## Context

ADR 4 lets modules refer to each other's things only by identifier. Three things cross the boundaries all the time: the person (member in `membership`, reader in `lending` and `fees`), the copy, and the title.

For the person, the brief offers the card number: "you get a card number, and you're a member" (§3.3). But a card is valid for a year, is renewed and can be blocked (§3.3), and the brief does not say whether the number stays when a card is replaced. A person who owes money must stay the same person when the card changes.

For copies and titles the brief names a barcode and an ISBN (§3.1). Whether those are stable enough to serve as identity (a replaced barcode label, two editions of one title) is not in the brief and is a question for the modelling of `catalogue`.

## Decision

We will let the owning module issue the identifier of its things; every other module only stores it and never invents one.

- **Member:** `membership` issues a member number at registration. The card number is an attribute of the card, not the identity of the person.
- **Copy and title:** `catalogue` issues their identifiers. Whether it uses the barcode and the ISBN for that, or its own numbers with barcode and ISBN as attributes, is decided when `catalogue` is modelled.

## Consequences

- No module has to look up or guess another module's identifiers.
- `lending` and `fees` speak of a *reader* but store the *member number*. The word changes at the boundary, the identifier does not.
- If the business wants the card number to be the member number, that is a decision of `membership` alone.
