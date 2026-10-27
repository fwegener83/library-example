# Contracts across the boundaries

The contract of every event, order and question that crosses a boundary in the first increment (option 3 of [chapter 6](../chapters/06-choosing-the-first-increment.md)). Chapter 7 produced it from the flows in DDD Studio.

**Why a file next to the model.** The payload schemas are in the model and in the export under [`esdm/`](esdm/). The owner of a policy, who uses which field, and what a consumer does about a late event are not: Studio takes a description for every element, but neither the tools nor the export return it (tool gap 23). So this file holds them. `scripts/check_repo.py` compares it with the export: a policy, a published event, an order or a question that is in the model and not here fails the check.

**The rules for all events** are those of [ADR 11](../docs/adr/0011-what-every-published-event-carries.md): the subject, the business day (`occurred-on`) and the number in order (`sequence`) are in every published event; a repeat is ignored; a gap holds later events back; an event about a subject the consumer does not know yet is held back, except the event that introduces its own subject. How a contract changes is [ADR 12](../docs/adr/0012-changing-published-events.md) (proposed); how gaps and repeated orders are handled is [ADR 13](../docs/adr/0013-gaps-and-repeats.md) (proposed).

## Policies and their owners

A policy is owned by the context that reacts. It lives under the domain in Studio, so the model does not say whose it is.

| Policy | Owner | Handles (from) | Emits (to) |
|---|---|---|---|
| `shelve-registered-copy` | lending | copy registered (catalogue) | add copy to shelf (lending) |
| `follow-copy-correction` | lending | copy corrected (catalogue) | update copy details (lending) |
| `stop-lending-withdrawn-copy` | lending | copy withdrawn (catalogue) | remove copy from circulation (lending) |
| `follow-membership-status` | lending | member registered, researcher status granted, card renewed, hold placed, hold lifted (membership) | update reader status (lending) |
| `lend-collected-copy` | lending | reservation collected (lending) | check out copy (lending) |
| `track-loan-for-fees` | fees | copy checked out (lending) | track loan (fees) |
| `assess-fine-on-return` | fees | copy returned (lending) | assess late fine (fees) |
| `charge-lost-book-on-loss` | fees | copy declared lost (lending) | charge lost-book fee (fees) |
| `follow-title-prices` | fees | title added, title details corrected (catalogue) | record title price (fees) |
| `keep-unpaid-fees-hold-in-line` | fees | late fine assessed, lost-book fee charged, running fines counted, payment received (fees) | place hold, lift hold (membership) |

## Published events

Facts that other contexts react to (13). "Not promised" are fields that travel for the owner's own use or for a later scenario; a consumer must not rely on them (ADR 12).

| Event | Owner | Subject | Consumers use | Not promised | Late, twice, unknown |
|---|---|---|---|---|---|
| `copy-registered` | catalogue | the copy | lending: copy, title, kind, home branch | usage-fee mark (scenario F) | introduces its own subject; never held back for it |
| `copy-corrected` | catalogue | the copy | lending: kind, home branch (all values travel, so it replaces the earlier ones) | usage-fee mark | held back if the copy is not known yet |
| `copy-withdrawn` | catalogue | the copy | lending: the fact | reason | held back if the copy is not known yet |
| `title-added` | catalogue | the title | fees: replacement price | ISBN, title, author | introduces its own subject |
| `title-details-corrected` | catalogue | the title | fees: replacement price (the whole record travels) | ISBN, title, author | held back if the title is not known yet |
| `member-registered` | membership | the member | lending: end date of the card | | introduces its own subject |
| `researcher-status-granted` | membership | the member | lending: end date of the status | | applied strictly in order |
| `card-renewed` | membership | the member | lending: new end date of the card | | applied strictly in order |
| `hold-placed` | membership | the member | lending: whether the card is now blocked | reason | applied strictly in order |
| `hold-lifted` | membership | the member | lending: whether the card is now blocked | reason | applied strictly in order |
| `copy-checked-out` | lending | the loan | fees: loan, reader, title, due date | copy | introduces its own subject |
| `copy-returned` | lending | the loan | fees: loan, reader, day of return | copy | held back if the loan is not known yet; held back if the title price is not known yet |
| `copy-declared-lost` | lending | the loan | fees: loan, reader, day of the report | copy | held back if the loan or the title price is not known yet; a lost book is never charged as free |

## Orders

Requests from one context to the public command of the owner of the thing to change (ADR 5). Both carry the member, the reason, the party that placed the hold (`placed-by`) and the moment of the decision (`decided-at`).

| Order | Owner of the command | Caller | Rule |
|---|---|---|---|
| `place-hold` | membership | fees (reason "unpaid fees") | ignored if older than the last request applied for the same hold (ADR 5; see ADR 13 for what is remembered after a lift); refused for a member that is not known yet, with that reason |
| `lift-hold` | membership | fees | only the party that placed a hold lifts it (C-19); a request that finds no such hold changes nothing |

## Questions

Asked by a staff page and answered by one context from its own data (ADR 8, ADR 10). A list question returns only the rows it finds; the page shows an id without a row as "not known".

| Question | Answered by | Asked for | Parameters |
|---|---|---|---|
| `list-reservations-that-ran-out` | lending | the morning list | branch, day |
| `list-overdue-loans` | lending | the morning list | branch, day |
| `list-copies-for-head-of-collection` | lending | the Head of Collection | none |
| `get-contact-details` | membership | the morning list | list of members |
| `get-title-details` | catalogue | the morning list | list of titles |
| `get-amount-owed` | fees | the desk, when a payment is taken | member |

## Events that stay inside a context (16)

Internal to **lending**: `reader-status-updated`, `copy-added-to-shelf`, `copy-details-updated`, `copy-removed-from-circulation`, `copy-found-damaged`, `copy-reserved`, `reservation-cancelled`, `reservation-collected`, `reservation-expired`. Internal to **fees**: `loan-tracked`, `late-fine-assessed`, `lost-book-fee-charged`, `running-fines-counted`, `payment-received`, `title-price-recorded`. Internal to **membership**: `contact-details-recorded`.

The events of `fees` that the policy `keep-unpaid-fees-hold-in-line` handles are internal to `fees`; only the orders cross.
