# Chapter 7 — proposal: decisions over several streams with a dynamic consistency boundary (variant A)

Status: **proposal, not decided, nothing built.** Written on 2026-11-12
after DDD Studio got the dynamic consistency boundary (DCB) as a model
element. It would change decisions 2, 3 and 7 of
`docs/logs/ch07-storylines.md`, so it waits for the maintainer.

Names of new elements below are proposals. Everything marked *probed* was
tried in a throw-away workspace ("zz probe DCB fit for Millbrook"), not in
the tutorial workspace; everything else follows from `explain_concept
dynamic-consistency-boundary` and `explain_model flows-and-slices` and is
not yet tried.

## The problem it answers

Flow 1 carries seven notes on places the model could not say what it
means. Three of them are one finding: a decision needs more than the
stream of its own aggregate.

| Note | Decision | What it needs besides its own aggregate |
|---|---|---|
| Gap 1 | checkout, reservation (`lending`) | the reader's other loans and reservations |
| Gap 2 | checkout, reservation (`lending`) | card valid until, researcher until, blocked (facts of `membership`) |
| Gap 2 in `fees` | late fine, lost-book fee | the replacement price (fact of `catalogue`) |
| Gap 5 | add title, register copy (`catalogue`) | all titles with the same ISBN; the title named in the command |

Until now the aggregate `copy` in `lending` stood in for the boundary and
its description said so (decision 3).

## The rule of variant A

1. **An aggregate keeps the life of its thing.** `copy`, `reader-account`,
   `title` stay aggregates, with the commands that need nothing but their
   own history.
2. **A decision that reads beyond one stream is a command of a DCB.** The
   DCB lists the events it reads (`consults`, each with a criterion) and
   holds the invariants of that decision. Its command writes the event of
   the aggregate it concerns (*probed*: a DCB command may publish an
   aggregate's event; an aggregate command may not publish a free-standing
   one).
3. **A DCB reads only events of its own context.** A fact of another
   context is first taken in as an event of the reading context, by a
   policy (ADR 4: a module uses its own copy). This is what makes it
   variant A.

Rule 3 is the difference to **variant B**, where the DCB consults the
other context's events directly. *Probed*: Studio accepts B and shows a
permanent hint, "That only works with a shared event store. If a slightly
stale view is enough, an event of its own in lending, fed by a policy, is
the decoupled form."

## What changes, per context

### lending

| Element | Kind | Change |
|---|---|---|
| `lending-decision` | DCB, new | identified by `barcode` and `member-id` of the command |
| `check-out-copy` | command | recreated under the DCB (a command cannot be moved); publishes `copy-checked-out` of the aggregate `copy` as before; carries `member-id` instead of only `card-number` |
| `reserve-copy` | command, new (flow 2) | under the DCB; publishes `copy-reserved` |
| `reader-standing-record` | DCB, new | identified by `member-id`; anchor of the command below |
| `note-reader-standing` | command, new | under `reader-standing-record` |
| `reader-standing-noted` | event, new, free-standing in `lending` | card valid until, researcher until, blocked, `sequence` |
| `note-reader-standing-from-membership` | policy, new | handles `member-registered`, `card-renewed`, `card-blocked`, `card-unblocked`, `researcher-status-granted`; emits `note-reader-standing` |
| `reader-standing` | read model | projects `reader-standing-noted` instead of the membership events; still what the desk sees |
| `copy` | aggregate | keeps `take-in-copy`, `return-copy`, `mark-loan-overdue`, `reclassify-copy`, `retire-copy` and its own invariants (`copy-on-loan`, `active-reservation`) |

`lending-decision` consults:

| Event | Criterion |
|---|---|
| `copy-taken-in`, `copy-reclassified`, `copy-retired` | of this barcode |
| `copy-checked-out`, `copy-returned`, `copy-declared-lost` | of this barcode, and of this reader |
| `copy-reserved`, `reservation-cancelled`, `reservation-expired` | of this barcode, and of this reader |
| `loan-became-overdue` | of this reader |
| `reader-standing-noted` | of this reader |

Invariants that move from `copy` to `lending-decision`: `copy-known`,
`copy-on-shelf-to-check-out`, `copy-on-shelf-to-reserve`,
`card-valid-on-the-day`, `card-not-blocked`,
`restricted-only-for-researchers`, `five-reservations`,
`overdue-limit-at-branch`. Their ids change, so the rejection of slice 17
is set again.

`reader-standing-record` has one rule, taken from ADR 11: a fact is
applied in its place in order for its member; a repeat is ignored, a fact
with a gap before it is held back. Decision 2 rejected a reader aggregate
in `lending` as "an aggregate without a rule of its own"; with ADR 11 the
taking-in has a rule, and it is the same rule for every fact taken in from
another context.

Why `member-id` in the command: the DCB selects by values of the command,
and the events of `lending` carry `member-id`. The desk already has it
from `find-reader-standing` (slice 6).

### fees

| Element | Kind | Change |
|---|---|---|
| `charge-decision` | DCB, new | identified by `member-id` and `title-id` of the command |
| `assess-late-fine` | command | recreated under the DCB; publishes `late-fine-assessed` (and the arrears events) of `reader-account` |
| `charge-lost-book-fee` | command, new (flow 3) | under the DCB |
| `replacement-price-record` | DCB, new | identified by `title-id` |
| `note-replacement-price` / `replacement-price-noted` | command / free-standing event, new | fed by a policy on `title-added` and `title-details-corrected` |
| `replacement-prices` | read model | projects `replacement-price-noted` |
| `reader-account` | aggregate | keeps `record-overdue-loan`, `recount-amount-owed`, `receive-payment` |

`charge-decision` consults the events of `reader-account` for this member
and `replacement-price-noted` for this title. To check while building:
whether `recount-amount-owed` also caps at the replacement price (C-38);
if so it moves too.

This is the weakest case for a DCB. The price is a reference value, no
race matters, and a late price is corrected under ADR 11 anyway. The
reason to do it all the same: the cap is a business rule (C-38) that rests
on a fact outside the account, and the DCB is the only element that can
say so.

### catalogue

| Element | Kind | Change |
|---|---|---|
| `title-registration` | DCB, new | identified by `isbn`; consults `title-added` and `title-details-corrected` with the same ISBN; invariant "an ISBN appears once"; a title without ISBN (T-0002) is not checked, said in the criterion |
| `add-title` | command | recreated under the DCB; publishes `title-added` of `title`. `correct-title-details` moves too if it can change the ISBN |
| `copy-registration` | DCB, new | identified by `title-id`; consults `title-added`; invariant "a copy needs an existing title" |
| `register-copy` | command | recreated under the DCB; publishes `copy-registered` of `copy` |

No taking-in is needed here: all events are the catalogue's own.

### membership

No change.

## What changes in flow 1

Today 23 slices. With variant A about 27:

| Where | New or changed slice |
|---|---|
| after 1 | new, `fees`, by itself: policy → `note-replacement-price` → `replacement-price-noted` (step 4, the read-model slice, stays and now shows this event) |
| 1, 2 | anchor becomes the DCB; step 2 gets `consulted` → *title added* of step 1 |
| after 5 | new, `lending`, by itself: policy → `note-reader-standing` → `reader-standing-noted` (valid through 11 Jan 2027, not blocked) |
| 7, 23 | anchor becomes `lending-decision`; `consulted` → *copy taken in* and the latest *reader standing noted* |
| after 16 | new, `lending`, by itself: the block is noted |
| 17 | anchor `lending-decision`, rejection `card-not-blocked`, `consulted` → the noted block (*probed*: this shape validates, and marked as a scenario it yields a Given/When/Then with the consulted events as Given) |
| 19 | anchor `charge-decision`; `consulted` → *overdue loan recorded* and *replacement price noted* |
| after 22 | new, `lending`, by itself: the unblock is noted |

The `[?]` marks of slices 2, 4, 6, 7, 17 and 19 go.

## What it does to the notes

| Note | After variant A |
|---|---|
| Gap 1 | resolved: the rule over copy and reader is the DCB's |
| Gap 2 (`lending`) | resolved: the DCB consults `reader-standing-noted`; the flow draws the arrow |
| Gap 2 (`fees`) | resolved for the price. The second question in that note (a list of loans in the account's state) stays for the challenge in chapter 8 |
| Gap 5 | resolved, both halves |
| Asymmetry copies/readers | resolved: both arrive by policy into an event of `lending` |
| Gap 3, conditional events | not touched by this; closed with scenarios (slices 15 and 21 marked as scenarios, plus a variant "line not crossed") |
| Gap 6, morning list; Gap 7, morning run | not touched by this; both are the documented patterns (read-model slices one after the other; automation over a view) |
| Gap 4, owner of a policy | not touched; tool gaps 14 and 15 stay |

## Decisions of the storylines it revises

| Decision | Today | With variant A |
|---|---|---|
| 2 | readers reach `lending` only as a read model on membership events | readers reach `lending` by a policy into an event of `lending`; the read model projects that event |
| 3 | the aggregate `copy` stands in for the DCB | a DCB decides; `copy` keeps its own life |
| 7 | `replacement-prices` is a read model on catalogue events, read by the account | the price is taken in as an event of `fees`; a DCB consults it |

Decisions 1, 4, 5, 6, 8 and 9 stay.

## Why A and not B

| | A: own event by policy | B: consult the other context's events |
|---|---|---|
| ADR 4 ("uses its own copy") | follows it | the model reads another module's stream |
| Gate G2 (technology) | says nothing about storage | presumes a shared event store (Studio's hint) |
| What the model claims | "as current as the events that fed it", as decision 3 says | a transactional decision over membership's events |
| Copies and readers | one shape for both | two shapes stay |
| New elements | 2 record DCBs, 2 commands, 2 events, 2 policies | none |
| Flow 1 | about 27 slices | 23 slices |
| Studio | no hint | a permanent hint on two DCBs |

Recommendation: A. B is less work and reads shorter, but it states
something the architecture decided against, and it settles a storage
question before G2.

## Costs and risks

- Commands cannot be moved in Studio: `check-out-copy`, `assess-late-fine`,
  `add-title`, `register-copy` are deleted and recreated; slices 1, 2, 7,
  17, 19, 23 and the policy `assess-fine-on-return` are rewired. No GWT
  feature exists yet, so nothing else breaks.
- Four DCBs that decide and two that only record is a lot for one
  increment. Studio's own warning applies: "Do not use a DCB to avoid
  choosing a boundary." The two in `catalogue` and the one in `fees` are
  the candidates to drop if the chapter gets too heavy; the notes for them
  would then stay open with a reason.
- A record DCB with a single ordering rule is close to "an aggregate
  without a rule". If the maintainer prefers, the anchor can be a small
  aggregate (`reader-standing-record` identified by `member-id`); the
  flow and the events are the same.
- Not probed: the whole of flow 1 in the new shape, the DCBs in `fees` and
  `catalogue`, and an aggregate slice (`return-copy`) whose history
  includes an event written by a DCB command.

## Open in DDD Studio (for `docs/tool-gaps.md` once decided)

- Tool gaps 14 and 15 (owner of a policy; decision in the aggregate with a
  stateless policy across the boundary) are unchanged.
- Tool gap 19: `explain_model flows-and-slices` still says "A flow is one
  story in one context, not the whole domain".
- New: a fact taken in from another context needs an anchor (aggregate or
  DCB) although the receiving context decides nothing about it.
- The probe workspace cannot be deleted through MCP.
