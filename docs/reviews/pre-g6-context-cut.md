# Context cut challenge: pre-g6

Input: `origin/main` at `b911252` (branch `cut-review-before-g6`). Files read:
`requirements/brief.md`, `requirements/clarifications.md` (C-01 to C-27),
`model/esdm/**` (4 contexts, 4 subdomains, 3 external systems, 9 mappings),
`model/sketch/big-picture-contexts.json`, `model/sketch/big-picture.json`
(header only), `model/domain-stories/*.yaml`, `docs/adr/0001` to `0010`,
`chapters/03` to `05`, `docs/plan.md`, `docs/gates/g1-model-to-code.md`
(phase 5 abort criteria), `docs/tool-gaps.md`; then, after forming the
findings, `docs/reviews/ch03-baseline-context-cut.md`,
`ch04-context-cut.md`, `ch05-context-cut.md`.
Run by: fresh agent, 2026-10-25

Scope: can the cut carry the choice of the delivery scope (G6) and the
detailed modelling of each context (phase 5)? Special attention to
scenarios across lending, fees, membership and catalogue, one with late or
double events (ADR 4, ADR 5), and the F2/G3 case (restricted flag kept by
lending, `docs/plan.md` §11).

Verdict in one line: the cut holds. No finding is blocking. What is
missing is not a boundary but the **contract of the events that cross
it**: ADR 4 demands tolerance of late and double events, and only one of
the seven edges has the means to give it (F1, F2). Phase 5 will have to
settle these anyway; they are cheapest to settle before the scope is chosen.

## Canvas (short)

| Context | Purpose (business words) | Class. | Decides on its own | Receives | Sends |
|---|---|---|---|---|---|
| `catalogue` | Register titles and the copies the library owns | supporting | title before copy; circulating or restricted; usage-fee mark; home branch; withdraw, release (C-20, C-21, C-24, C-25) | ISBN service (ACL), Head of Collection | title added, copy registered, withdrawn, released |
| `lending` | Let readers reserve, borrow, return copies at four branches | core | reservation limits, restricted vs researcher, per-branch overdue limit, expiry of reservations, overdue, lost, damaged | catalogue events, membership status | loan events (checked out, became overdue, returned, declared lost), list for the Head of Collection |
| `membership` | Register members, keep cards and researcher status valid | supporting | card validity, researcher status, a card with a hold is blocked | Membership Officer, place/lift orders from fees | blocked, unblocked, expired, renewed, researcher granted/expired |
| `fees` | Charge what readers owe, take payments, hold the card when in arrears | supporting | late/running fine, lost-book and usage fee, arrears (C-19), received/confirmed (C-22) | catalogue and loan events, CityPay (ACL) | place/lift hold orders, payments to CityPay |

Words and Studio fields are filled from the sources. No field is empty;
every context has a decider, decisions and a language of its own.

## What holds

- **No dependency cycle.** Graph from the mappings and from who reacts to
  whose events: `catalogue` and `membership` depend on nothing; `lending`
  depends on `catalogue` and `membership`; `fees` depends on all three
  (ADR 5: "`fees` uses `catalogue`, `membership` and `lending`"). The
  business loop fees, hold, card, loan, fee runs through an order and an
  event, not through a dependency. The two human loops (lost or damaged
  copy to the Head of Collection and back through `catalogue`; payment
  taken at the desk) go through a page (ADR 8), not through a module.
- **A usable build order falls out of the graph.** `catalogue` and
  `membership`, then `lending`, then `fees` (chapter 4). Even the simplest
  story (`reserve-borrow-return`) needs three contexts (a registered copy,
  a member with a valid card, the loan); `fees` is a leaf that only the
  late path needs. See "Consequences for G6" below.
- **The G3 decision removes the round trip it was meant to remove.** With
  the flag in `lending`'s own copy, "only researchers may borrow a
  restricted copy" is decided in one context with no question to
  `catalogue` or `membership` (ADR 4, point 5: "A module never needs
  another module's answer to finish its own business decision"). Played
  through (S3), the invariant needs two foreign facts at the same moment
  (phase 5 abort criterion: "an invariant needs data from two contexts at
  the same moment"), and it passes only because both facts are local
  copies; that is the reason F2 and F3 matter.
- **The ownership of the €10 rule survives the timing test.** ADR 5:
  "`membership` ignores a request that is older than the last one it
  applied for the same hold, so a late "lift" cannot undo a newer "place"."
  In S2 the rejected payment, the late "lift" and the daily run all end in
  the right hold state. Only `membership`'s side is protected (F1, F2).
- **`lending` to `fees` is a real customer-supplier** (ADR 9): the due
  date and the loss shaped the events. A change to the due date (C-13,
  28 days) reaches `fees` without a change in `fees`.
- **Both anti-corruption layers translate something real** (cents, 20-
  character references, odd status codes; oddly formatted titles).
- **Single decision owners.** Arrears: `fees` (C-19). Usage-fee mark:
  `catalogue`, amount: `fees` (C-21). Home branch: `catalogue` (C-24).
  Withdraw and release: `catalogue` (C-20, C-25). No rule found with two
  deciders.
- **Change scenarios stay narrow.** €10 threshold or €0.50 rate: `fees`.
  Reservation period (C-12): `lending`. Waiting line (C-15): `lending`.
  28-day loans (C-13): `lending`, plus `catalogue` if "new release" is a
  mark. Online payment (C-02 option 3): `fees` and a page. The one likely
  change that reaches three parties is a second notification channel (F7).

## Status of the earlier findings

| Report | Finding | Now |
|---|---|---|
| ch03 | F1 block rule two owners, F2 cycle, F3 amounts, F6 manual block | closed (C-19, ADR 5, board corrected) |
| ch03 | F4 usage-fee owner, F5 lost copy, F7 open host services, F8 desk timing | closed (C-21, C-20, ADR 9, C-22). The residual timing of the three hops is in F2 |
| ch03 | F9 words with no glossary home | partly open: *damaged copy* and *special collection* are handled; *new release* has no owner (brief §3.4); a keep without time limit has no word in `lending` (F8) |
| ch04 | F1 to F7 | closed by C-20 to C-24 and ADR 9; verified in the exports (`catalogue-lending-open-host-service`: "Availability stays in lending"; *Payment Cancelled* card and edges exist) |
| ch05 | F1 board, F3 availability wording, F4 damaged copy home | closed (board edges, mapping wording, C-25) |
| ch05 | F2 "paid" two meanings | still open, parked as C-26 (modelling `fees`) |
| ch05 | F5 usage fee needs the mark before the checkout; mark cannot change | still open, parked as C-27. F3 below extends the same hole to `lending`'s flag |
| ch05 | F6 which branch counts | still open, parked in C-14 (modelling `lending`) |
| ch05 | F4, alternative (b) chosen | closed as to ownership; **new gap in how the release reaches `lending` (F5)** |

## Findings

### F1 The loan events have no loan identity and no business time, so double and late events cannot be tolerated
- Severity: should fix
- Lens: scenario (timing)
- Evidence:
  - `docs/adr/0004-contexts-talk-through-published-events.md`: "Reactions to events must tolerate events that arrive twice or late." and, in Consequences, "Copies can be late; the rules of each context must say what happens then. That is a question for the modelling of each context."
  - `model/esdm/integration/lending-fees-customer-supplier.esdm.yaml`: "checked out, became overdue, returned, declared lost, each with the copy, the reader and the due date".
  - `docs/adr/0007-identifiers-across-contexts.md`: "Three things cross the boundaries all the time: the person (member in `membership`, reader in `lending` and `fees`), the copy, and the title." No identifier for the loan.
  - `requirements/clarifications.md`, C-03: "days overdue × €0.50, capped at the price", "A daily check (the morning run) adds the running amounts to the fixed ones".
  - `model/sketch/big-picture-contexts.json`, policy "When an overdue book is returned, assess the late fine": "€0.50 per day from the day after the due date".
- Why it matters (S2): *Book Returned* reaches `fees` twice (at-least-once delivery is the stated default in `docs/plan.md` §7: "Event Publication Registry = Outbox mit at-least-once"). Without a loan identity `fees` can only deduplicate on copy, reader and due date. That key is not unique: a reader who returns a copy and borrows it again the same day gets the same due date (60 days from the same day). The second *Returned* then looks like a duplicate of the first, or the first like a duplicate of the second. Second case: *Returned* is delivered after midnight. The fine is "from the day after the due date" per day; if `fees` counts days with its own clock instead of the day of the return, the reader is charged one day more than the desk told him, and the daily run in `fees` has meanwhile added a running day for a book that is already back. The €10 line is 21 days (21 × 0.50 = 10.50), so a single extra day is exactly what flips the hold.
- Alternatives:
  - `lending` issues a loan identifier (extend ADR 7) and every loan event carries it and the business date of the fact (returned on, declared lost on) — costs two fields in the contract and one sentence in ADR 7; `fees` keeps one record per loan and applies each event at most once.
  - Key on copy, reader and due date as today — costs the same-day re-borrow ambiguity above and any future renewal.
  - Let `lending` send the number of days late — rejected: the rule (rate, cap) is `fees`'s, this would split it.
- Level and next step: architecture. Fold into the ADR on event evolution that `docs/plan.md` row 7 and ADR 4 already announce ("A record of its own follows when the first event is specified"): an event envelope with identity, business time and a monotonic order per aggregate. Proposed ADR 11 (status `proposed`, recommended: first alternative).

### F2 `membership` is protected against late orders, but `lending` is not protected against late membership events, and expiry is a message instead of a date
- Severity: should fix
- Lens: scenario (timing), dependencies
- Evidence:
  - `docs/adr/0005-no-circle-between-modules.md`: "`membership` ignores a request that is older than the last one it applied for the same hold". This protects the inbound order only.
  - `model/esdm/integration/membership-lending-customer-supplier.esdm.yaml`: "Membership decides status and publishes every change; lending keeps the part it needs and never calls back." No version, time or order is mentioned.
  - `model/sketch/big-picture-contexts.json`: edges "Clock (daily)" "triggers" *Card Expired* and "triggers" *Researcher Status Expired*; the clock's note: "Nobody 'does' expiry or overdue — time passes."
  - `requirements/brief.md` §3.3: "The card is valid for a year", "you're a researcher for twelve months".
  - `requirements/clarifications.md`, C-05: expired card "like a blocked card (no new loans, no new reservations)"; expired researcher status: "a normal reader again for new loans and reservations".
- Why it matters (S2, S3): *Card Blocked* then *Card Unblocked* (a payment minutes later) may arrive at `lending` in the reverse order; `lending`'s copy then says "blocked" until the next change, with no way to know. The same for *Card Expired* and *Card Renewed*. In the other direction the window is the point of the business rule: at midnight a researcher's status ends, the daily job in `membership` runs some time later, the event is delivered some time after that; until it arrives `lending` lends a restricted copy (signed first edition, "anything the archive lent us") to an ordinary reader, the case the director singled out ("they expect us to treat it carefully"). The facts are dates ("a year", "twelve months"); turning them into clock-fired events makes lateness part of the rule.
- Alternatives:
  - `membership` publishes the validity end (valid until) with *Granted*/*Renewed* and `lending` compares it with its own clock — costs: the exact last day ("twelve months": inclusive?) becomes a rule that both sides must read the same way; the expiry events remain for information only.
  - Keep the events and add a per-member sequence number or time of decision (as for holds) to everything `membership` publishes — costs one field; the window at midnight stays.
  - Accept the window and say so in `lending`'s rules — costs a business decision for the restricted copies only (question 2).
- Level and next step: architecture (same ADR as F1, envelope with order) and business for the tolerated window (draft C-28).

### F3 The G3 decision leaves open what `lending` does with a copy it does not know, and the flag cannot change; the same hole exists in `fees`
- Severity: should fix
- Lens: scenario, dependencies
- Evidence:
  - `docs/plan.md` §11, F2 decision: "wie mit einer Ausleihe umzugehen ist, deren Kopie `lending` noch nicht kennt, klärt die Feinmodellierung von `lending`."
  - `model/esdm/integration/catalogue-lending-published-language.esdm.yaml`: "title added; copy registered, with circulating or restricted, home branch; copy withdrawn; copy released after repair (C-20, C-24, C-25)". No event that changes the kind or the mark of a registered copy.
  - `requirements/clarifications.md`, C-27 (parked): "Fees must have the mark before the checkout arrives (C-21)." It asks about the usage-fee mark only.
  - `docs/reviews/ch05-context-cut.md`, F5: "A late or missing *Copy Registered* in `fees` gives a silent "no fee" rather than an error."
  - `requirements/brief.md` §3.1: "When we register a copy, we decide whether it circulates or not." Nothing says it is final; for titles the brief says "We fix it by hand" (*Book Details Corrected* exists; for copies there is none).
- Why it matters (S3): the invariant of the G3 case holds only for copies `lending` knows. For an unknown copy there are three answers: refuse, accept as circulating, accept and check later. "Accept as circulating" breaks the rule silently; "refuse" is safe but turns every late *Copy Registered* into a failed checkout at the desk. The decision is the same in `fees` (checkout of an unknown copy: charge nothing, or fail?) and the same in any later consumer, so it is a rule of the published language, not of `lending`. Second gap: if a copy was registered as circulating by mistake (a signed edition) nobody can correct it; the only way out is withdrawing the copy and registering a new one, which loses its history in `lending` and `fees`.
- Alternatives:
  - One rule for all consumers: an event about a copy the consumer does not know is held back and retried, a command about an unknown copy is refused, nothing defaults — costs a retry path per consumer and a visible "copy not yet known" error at the desk.
  - Add *Copy Reclassified* (kind, mark, home branch) to the published language — costs one event; decide with C-27 whether it exists at all.
  - Let the caller pass the kind in the command — the option G3 rejected; not recommended.
- Level and next step: business for "can the kind or mark change after registration" (extend parked C-27 to the restricted kind and the home branch), architecture for the "unknown copy" rule (ADR 11, same record as F1).

### F4 *Restricted* is defined by a rule of `lending` and `membership`, and nobody says who owns "researchers only"
- Severity: should fix
- Lens: language, ownership
- Evidence:
  - `model/esdm/catalogue/bounded-context.esdm.yaml`, *restricted*: "A copy only researchers may borrow: signed first editions, the local history collection, anything the archive lent."
  - `model/esdm/lending/bounded-context.esdm.yaml`: no term *restricted* or *circulating*; *researcher*: "A reader whom membership reports as a researcher: may borrow restricted copies and has no reservation limit."
  - `model/sketch/big-picture-contexts.json`, area `lending`, policy "Restricted copies: researchers only", rule: "Only researchers may borrow or reserve a restricted copy."
  - `requirements/brief.md` §3.1 (Tom Okafor, Head of Collection): "Those are restricted: only researchers may borrow them."
  - `model/esdm/integration/catalogue-lending-open-host-service.esdm.yaml`: "lending takes the copies, circulating or restricted, with their home branch".
- Why it matters: the catalogue's definition contains the rule that `lending` enforces and a word of `membership` (*researcher*); `lending` stores a flag whose word its own glossary does not define. Two places state one rule, three contexts' words meet in it (heuristics §2, a word of A inside a definition of B). The brief gives the decision to the Head of Collection ("we decide … restricted"), the enforcement to the desk. If the archive wants a second tier (say, university staff who are not researchers may use the local history collection), the change touches `catalogue` (a kind), `lending` (the rule) and `membership` (a status): three contexts for a likely change (heuristics §5).
- Alternatives:
  - `catalogue` publishes a neutral fact ("reference copy", "archive copy") and defines no consequence; `lending` owns the rule "researchers only" and says so in its glossary — costs a word for the class and one definition in `lending`; the Head of Collection no longer "decides who may borrow", only the class.
  - `catalogue` publishes the access rule itself ("borrowable by: researchers") and `lending` only enforces it — costs a rule vocabulary in `catalogue` that depends on `membership`'s statuses.
  - Leave as is and add *restricted* to the `lending` glossary pointing to the catalogue's definition — costs the duplicated rule.
- Level and next step: business (draft C-29: who decides who may borrow a restricted copy: the Head of Collection per copy, or the library's lending rules?). Recommendation: the first alternative.

### F5 *Copy Released* lifts a state that only `lending` holds, with no way to tell which damage it answers
- Severity: should fix
- Lens: ownership, scenario (timing)
- Evidence:
  - `requirements/clarifications.md`, C-25: "`lending` marks the copy damaged and lists it, as today. The Head of Collection decides: *withdraw* it in the catalogue … or *release* it after repair, also in the catalogue. `catalogue` publishes both; `lending` reacts."
  - `model/esdm/lending/bounded-context.esdm.yaml`, *damaged copy*: "Not lendable and listed for the Head of Collection, who withdraws it or, after repair, releases it in the catalogue (C-06, C-25)."
  - `model/esdm/catalogue/bounded-context.esdm.yaml`, *released copy*: "A damaged copy that the Head of Collection makes lendable again after repair (C-25)." The catalogue has no concept of "damaged".
  - `model/esdm/integration/catalogue-lending-published-language.esdm.yaml`: "copy released after repair" with no reference to anything else.
  - Heuristics §3: "Can one party undo the effect of another's decision … Then the effect needs to carry its owner." ADR 5 applied this to holds ("a late "lift" cannot undo a newer "place""); nothing equivalent exists for copies.
- Why it matters (S4): the damage is set by the librarian in `lending` (episode 1), the Head of Collection releases in `catalogue`, and the copy is damaged again (episode 2) before the *Released* of episode 1 is delivered or while a second *Released* is delivered twice. `lending` cannot tell the releases apart and makes a damaged copy lendable. `catalogue` cannot refuse a release of a copy that is not damaged, because it does not know the damage; it can publish *Released* for any copy, also a circulating one on the shelf, a withdrawn one (a released withdrawn copy would come back from the dead in `lending`) or a copy on loan. C-25 chose well on ownership (one place decides, the arrow stays catalogue to lending) but moved a state transition across the boundary: the cause of "damaged" lives in `lending`, the cure in `catalogue`.
- Alternatives:
  - Keep C-25 and give the release the order information of F2 plus a rule in `lending`: a release counts only if it is newer than the last damage report, and only for a damaged, not withdrawn, copy — costs the envelope of ADR 11 and two rules in `lending`; `catalogue` may still publish meaningless releases, harmlessly.
  - `lending` issues a damage report number, shown on the Head of Collection's list; the release names it — costs: the catalogue UI carries `lending`'s identifier (ADR 7 says the owner issues identifiers, which allows it) and a second page-level link between the two modules.
  - Release in `lending` after the Head of Collection's decision (C-25 option 2) — rejected in C-25 for good reason (two places decide).
- Level and next step: architecture (ADR 11), with a check of C-25 wording in phase 5 of `lending`. No new business question.

### F6 A lost copy that comes back has no owner in the sources
- Severity: should fix
- Lens: scenario (exception, timing)
- Evidence:
  - `model/esdm/lending/bounded-context.esdm.yaml`, *lost copy*: "A copy the reader reports lost at the desk. The loan ends and the copy is listed for the Head of Collection, who withdraws it in the catalogue (C-04, C-20)."
  - `model/esdm/fees/bounded-context.esdm.yaml`, *lost-book fee*: "The replacement price plus a handling fee, charged when a copy is declared lost (C-04)."
  - `requirements/clarifications.md`, C-04: "The reader reports the loss, staff record it at the desk."; C-03: "If the book is declared lost instead, the running amount ends without being fixed".
  - `requirements/brief.md` §3.4: "A lost book is charged at its replacement price, plus a €5 handling fee." No sentence about a book that turns up.
  - Grep over `requirements/`, `model/`, `docs/`, `chapters/` for "refund", "found again", "turns up": no hit.
- Why it matters (S4): a reader reports the loss on Monday at Central, pays the lost-book fee, finds the copy on Tuesday and hands it in at Riverside. Four contexts touch it, none decides. `lending`: the loan has ended, the copy is "lost"; is a check-in accepted, and is the copy back on the shelf or does the Head of Collection decide (it is listed, not yet withdrawn)? `catalogue`: *Copy Withdrawn* may already have been published, or may arrive after the copy is back on the desk (timing). `fees`: is the charge reversed, waived (C-16 is parked) or refunded to a payment that CityPay already confirmed? The reader's account shows "what I owe" (brief §2), which would be wrong either way. It is a normal case for a library, not an exotic one.
- Alternatives:
  - Not in the first release: a found copy is handled by hand outside the system (as repair in C-17 was) — costs a documented manual step and a known limit.
  - A *Lost Copy Found* path: `lending` ends the lost state, tells the Head of Collection; `fees` offers a waiver or refund — costs a refund path to CityPay that the cut does not have today (ACL has received/confirmed/rejected only).
- Level and next step: business, draft C-30 (what happens to a lost copy and its fee when the copy comes back?). Matters for G6 only if the lost-copy scenario is in the first increment.

### F7 Names, phone numbers, addresses and titles that the lists and notices need are held by no context that uses them
- Severity: should fix
- Lens: scenario, ownership
- Evidence:
  - `requirements/brief.md` §3.2: "Every morning, first thing, I print two lists … for the overdue ones, we call people."; §3.5: "Tell me when my reservation is ready."; §3.6: "Emails go out through the city's mail gateway."
  - `model/sketch/big-picture-contexts.json`, area `lending`: read model "Morning lists per branch: expired reservations, overdue loans"; events *Reservation-Ready Notice Sent*, *Due Reminder Sent* "sent through" *City Mail Gateway* ("Only way to send email.").
  - `docs/adr/0007-identifiers-across-contexts.md`: "`lending` and `fees` speak of a *reader* but store the *member number*."
  - `model/esdm/integration/membership-lending-customer-supplier.esdm.yaml`: lending must know "card valid, not blocked, researcher or not". `model/esdm/membership/bounded-context.esdm.yaml` has no term for contact data; the `lending` glossary has no term *title*.
  - `chapters/03-strategic-design.md`: "The mail gateway has no mapping yet." `docs/adr/0006`: "the mail gateway needs a record of its own once its interface is known."
- Why it matters (S5): the morning list is a core function of LibTrack (brief §4) and the director's "fewer phone calls" (§2). From its own data `lending` can print: member numbers, copy identifiers, due dates. The librarian needs a name and a number to call, a title to say which book. Notices need an address. The data lives in `membership` (who the person is) and `catalogue` (what the title is), and the published language gives `lending` neither. The cut does not forbid a solution (ADR 8 lets a page compose lists from several modules) but then "Morning lists" is not a read model of `lending` as the board shows it; it is a staff page that asks `lending` for the loans and `membership` and `catalogue` for the people and titles, once per row or in a batch. The change "a second channel" (SMS, letter) touches `lending` (the event), `membership` (the address) and the gateway adapter.
- Alternatives:
  - The staff page composes (ADR 8, ADR 10): `lending` returns member numbers and copy identifiers; `membership` and `catalogue` expose lookups by identifier in batch — costs two public queries and a rule that a list never needs more than one call per context.
  - `membership` publishes contact data to `lending` and `catalogue` publishes the title to `lending` — costs copies of personal data and of titles in `lending`, and a bigger contract for the whole life of the system.
  - A notification module — rejected in chapter 3 (no language of its own); still right, as long as the addresses live in `membership`.
- Level and next step: architecture (who composes), with a business question for the data (draft C-31: which contact data does the library hold and who maintains it?). To be answered when `lending`'s read models are specified; for G6 it decides whether "morning list" and "reservation-ready notice" are small or large scenarios.

### F8 What happens to a researcher's keeps and reservations when the status ends is not decided
- Severity: should fix
- Lens: ownership, scenario
- Evidence:
  - `requirements/brief.md` §3.2: "Researchers can ask us to keep a book for them until they come in, without any time limit. Normal readers can't." and "Researchers have no limit" (reservations).
  - `requirements/clarifications.md`, C-05: "Expired researcher status: the member is a normal reader again for new loans and reservations; what is already out stays out."
  - `model/sketch/big-picture-contexts.json`: event *Book Kept for Researcher (no time limit)*; `model/esdm/lending/bounded-context.esdm.yaml`, *reservation*: "until it is collected or runs out" (a keep never runs out).
- Why it matters (S3): a researcher with eight reservations and two keeps loses the status on the day after the letter expires. Does "already out" cover a reservation and a keep ("out" reads as loans)? If yes: the keep has no end date and the copy sits behind the desk forever, a former researcher's copy blocked for everyone (the very copy was perhaps restricted). If no: someone must cancel them, and then `lending` reacts to a `membership` event with a decision that is nobody's on paper. The reservation limit of five also shows the other side: eight reservations of an ordinary reader exist and nothing says they are tolerated until they end.
- Alternatives: a keep ends with the status (the reservation then runs out after the normal three days from that moment) — costs a rule in `lending` triggered by the late-prone event of F2; or the keep stays and shows on the morning list as "needs a decision" — costs a manual step; or the library accepts "stays out" for keeps — costs shelf space.
- Level and next step: business, draft C-32 (what happens to keeps and surplus reservations when researcher status ends?). Parked rules C-11 to C-14 are about `lending` as well; ask together.

### F9 `fees` uses words of `lending` and `catalogue` in its definitions that its own glossary does not define
- Severity: note
- Lens: language
- Evidence:
  - `model/esdm/fees/bounded-context.esdm.yaml`: *late fine*: "What a reader owes for a loan returned late: per day from the day after the due date, never more than the replacement price."; *assessed fine*: "fixed when the copy comes back"; *lost-book fee*: "charged when a copy is declared lost". The terms *loan*, *due date*, *copy* and *replacement price* are not entries of this glossary.
  - `model/esdm/lending/bounded-context.esdm.yaml`: *loan*, *due date*, *copy* (with its own meaning "what may be done with it right now"); `model/esdm/catalogue/bounded-context.esdm.yaml`: *replacement price*, *copy*.
- Why it matters: `fees` keeps its own record per loan (reader, copy, due date, price for the cap), which is a different thing from `lending`'s loan (a copy held by a reader), and a *copy* in `fees` is only an identifier with a price and a mark. Leaving the words undefined invites sharing `lending`'s type (forbidden by ADR 3, "Two modules may use the same word for different things; they never share the type"). It is cheap now and is exactly the kind of leak that appears as a shared class in phase 7.
- Alternatives: add *loan* (what is charged for), *due date* and *replacement price* as entries to the `fees` glossary, naming the other context as source — costs three entries; or name the `fees` concept differently (*charged loan*, *chargeable copy*) — costs a new word.
- Level and next step: review; do it when `fees` is modelled (chapter 9).

### F10 The board's *Reader account* read model is fed by events, which ADR 8 decided against
- Severity: note
- Lens: pattern
- Evidence:
  - `model/sketch/big-picture-contexts.json`: read model "Reader account: at home, waiting for me, what I owe" at top level; edges from *Book Reserved*, *Book Checked Out*, *Late Fine Assessed*, *Usage Fee Charged*, *Lost-Book Fee Charged*, *Payment Received*, each labelled "feeds".
  - `docs/adr/0008-user-interfaces-outside-the-modules.md`: "A user interface outside the modules … asks both modules through their public APIs"; the rejected option: "A separate view module. It listens to the events of `lending` and `fees` and keeps its own copy."
- Why it matters: read as a design, the card is the rejected view module with a copy of both streams. The board says "feeds"; the ADR says "asks". The risk is that the phase 5 model of the reader's page is built from the board. Combined with F1 and F2: a projection from two modules' events inherits their ordering problems; a page that asks does not.
- Alternatives: a note on the card ("composed by the page, ADR 8; not a projection") — costs wording on the board (edge labels cannot be edited, tool gap 13).
- Level and next step: review.

### F11 Finding a title that is on the shelf crosses `catalogue` and `lending` with no home
- Severity: note
- Lens: scenario
- Evidence:
  - `requirements/brief.md` §4: "Searching the catalogue."; §3.2: "You can only reserve a book that's on the shelf."
  - `model/esdm/catalogue/bounded-context.esdm.yaml`, *copy*: "Where the copy is right now is not known here (C-24)"; `model/esdm/lending/bounded-context.esdm.yaml`: no *title* term, the *reservation* is of "A copy on the shelf".
- Why it matters: the reader searches titles in `catalogue` and wants to see which can be reserved at Riverside, which is `lending`'s state. A search result is composed from two modules (ADR 8 allows it), and "filter by available at Riverside" cannot be done by either alone. Also unsaid: does a reader reserve a title (any copy on the shelf) or a copy? With a circulating and a restricted copy of one title (brief §3.1) it matters for the rule in F4. No concrete failure in the sources, a risk for the detailed modelling.
- Alternatives: `lending` exposes "available copies of these titles at this branch" as a public query that the search page calls after the catalogue search — costs a batch query in `lending` and a `title` reference in its API; or `lending` keeps a title identifier per copy (it receives it with *Copy Registered*) — costs one field.
- Level and next step: review (to be seen in the phase 5 model of `lending`).

## Scenarios played

| # | Case | Contexts | Crossings | Result |
|---|---|---|---|---|
| S1 | A researcher borrows a restricted usage-fee copy, returns it 25 days late, is blocked on day 21, pays at the desk, is unblocked (story `overdue-book-fine-and-blocked-card` extended; brief §3.1, §3.3, §3.4) | all four, plus CityPay | 11: copy registered to `lending` and `fees` (2), researcher/card to `lending` (1), checkout to `fees` (1), hold order (1), *Card Blocked* (1), *Returned* (1), payment to CityPay and confirmation (2), lift order (1), *Card Unblocked* (1) | holds; no module asks another during its own work; no cycle; order and double events open (F1, F2) |
| S2 | Timing: *Returned* arrives twice and after the next morning's run; the reader pays €10.50 at the desk; CityPay rejects a day later | `lending`, `fees`, `membership` | 6 plus CityPay | the hold logic holds (ADR 5); the amount owed does not, without loan identity and business time (F1); `lending`'s card state can end wrong (F2) |
| S3 | Timing and the G3 case: a researcher's status ends at midnight; at 00:05 she borrows a restricted copy that was registered a minute ago | `catalogue`, `membership`, `lending` | 2 in, 0 out | decided locally (good); correct only if both local copies are current (F2, F3); the keeps and reservations she leaves behind have no rule (F8) |
| S4 | Exceptions: a damaged copy is released and damaged again; a lost copy is found | `lending`, `catalogue`, `fees` | 2 to 3 | ownership clean (C-25), transitions and the found case open (F5, F6) |
| S5 | Priya's morning: the two lists for Riverside and the calls | `lending`, `membership`, `catalogue` | 0 in the cut; 2 to 3 by a page | not producible from `lending`'s data alone (F7) |
| S6 | Brief exception (§3.2, §3.5): a researcher with three overdue books at Riverside reserves at Central | `lending` | 0 | holds; which branch counts for a loan is still C-14 |

Change scenarios: (1) a second tier for restricted copies: `catalogue`,
`lending`, `membership` (F4); (2) a second notification channel: `lending`,
`membership`, the gateway adapter (F7); (3) 28-day loans (C-13): `lending`
(+ `catalogue`); (4) €10 threshold: `fees`. Only (1) and (2) reach three
parties, both through the same two seams: the meaning of *researcher* and
the contact data of a member.

## Consequences for G6 (delivery scope)

These are inputs for the scope decision; they decide nothing.

- The smallest sensible increment needs `catalogue`, `membership` and
  `lending` (S1 without the fee path, S6). `fees` can come in the second
  increment without a change in the three, because it is a leaf of the
  graph. A scope "lending without fees" is cheap only if the loan events
  carry identity and business time from the first day (F1): it is the part
  of the contract that cannot be added later without reading old events.
- Scenarios that are small in the cut: reserve, borrow, return in time,
  the per-branch limit (S6), blocking by arrears (S1).
- Scenarios that are larger than they look: the morning lists and notices
  (F7), anything with a researcher's status ending (F2, F8), lost and found
  (F6).
- Whichever scenarios are chosen, the event envelope (F1, F2, F3, F5) is
  one decision (proposed ADR 11) that every cross-context flow of phase 5
  needs; it is cheaper to take it before the flows are modelled.

## Draft clarifications and proposed ADR

Numbers are placeholders; C-26 and C-27 are taken, ADR 10 is the last.

- **C-28 (draft) How stale may `lending`'s view of a card be for restricted copies?** Source: F2, brief §3.1 ("they expect us to treat it carefully"). Options: (1) seconds are fine, say so; (2) `lending` checks validity dates itself for restricted copies. Recommendation: (1) if the dates travel (F2, first alternative), otherwise (2).
- **C-29 (draft) Who decides who may borrow a restricted copy?** Source: F4. Options: the Head of Collection per copy (class and consequence), or the lending rules (the Head of Collection only classifies). Recommendation: the second.
- **C-30 (draft) What happens when a lost copy comes back?** Source: F6. Options: by hand outside the system; a path in `lending` and `fees` with waiver or refund. Recommendation: by hand in the first release.
- **C-31 (draft) Which contact data does the library hold about a member, and who maintains it?** Source: F7. Recommendation: `membership` holds and maintains it.
- **C-32 (draft) What happens to a researcher's keeps and surplus reservations when the status ends?** Source: F8. Recommendation: a keep ends with the status; existing reservations run out normally.
- **Extend C-27** to the restricted kind and the home branch (F3).
- **ADR 11 (proposed) Event envelope: identity, business time, order, unknown subject.** Source: F1, F2, F3, F5. Options: (a) loan, damage and hold identity plus business time and a per-aggregate sequence in every published event; unknown subject is held back and retried; (b) identity by natural key, no sequence; (c) leave to each context in phase 5. Recommendation: (a). It is the record ADR 4 announces ("A record of its own follows when the first event is specified") and the "ADR zur Event-Evolution" of `docs/plan.md` row 7.

## Questions for the maintainer

1. (F4, C-29) Who owns "only researchers may borrow a restricted copy": the Head of Collection, who marks the copy, or the library's lending rules, with the Head of Collection only classifying?
2. (F2, F3, C-28, C-27) May a restricted copy be lent in the minutes between a researcher's status ending and `lending` hearing of it? And may the kind of a copy (restricted or not), its mark or its home branch be corrected after registration?
3. (F6, C-30) A reader reports a copy lost, pays the fee, and brings the copy back. What should happen to the fee and to the copy?
4. (F8, C-32) When researcher status ends: do the keeps without time limit and the reservations above five end, stay, or go to a person?
5. (F7, C-31) Which contact data does the library hold about a member (phone, email), and are the morning lists a staff page that may compose `lending` with `membership` and `catalogue`?
6. (F1, ADR 11) Do you accept, as a rule of every published event, a loan or episode identifier, the business date of the fact and a per-subject order, before the flows of phase 5 are modelled?
7. (G6) Is the first increment allowed to leave `fees` out, given that the loan events carry the identity and time from day one?
