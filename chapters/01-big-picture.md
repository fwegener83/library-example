# Chapter 1 — Big Picture Event Storming

**Input:** [the brief](../requirements/brief.md)
**Tool:** DDD Studio, Sketch Board `big-picture`
**Result:** a board with events, actors, external systems, policies, read models and hotspots. It is a sketch, not the model, so nothing on it is validated yet.

## What we do here, and what we do not

Big Picture Event Storming asks one question of the whole business: *what happens, in which order, and who or what makes it happen?* We collect **domain events** in past tense, put actors and external systems around them, note the rules we hear as **policies**, and mark every place where people disagree or do not know as a **hotspot**.

We deliberately do not decide anything yet: no aggregates, no boundaries, no technology. The sticky kinds are only borrowed from the Studio palette, so that later chapters can promote them into the real model.

## How the board was built

The brief has six voices and one rule of thumb: **every sentence with a verb in the past is a candidate event.** The sources are tagged on the cards (`src:brief-3.2` and so on), and the theme tags (`theme:collection`, `theme:membership`, `theme:lending`, `theme:fees`, `theme:notification`) show where the events seem to cluster. These themes are a first hint and not yet a boundary.

### The timeline

Read it left to right as the life of a book and of a member.

| Theme | Events |
|---|---|
| Collection | Title Added to Catalogue, Book Details Corrected, Copy Registered (circulating or restricted) |
| Membership | Member Registered (card issued), Researcher Status Granted, Researcher Status Expired, Card Blocked, Card Unblocked, Card Renewed, Card Expired |
| Lending | Book Reserved, Book Kept for Researcher, Reservation Cancelled, Reservation Expired, Book Checked Out, Loan Became Overdue, Reader Reminded by Phone (overdue), Book Returned, Book Found Damaged, Book Declared Lost |
| Fees | Usage Fee Charged, Late Fine Assessed, Lost-Book Fee Charged, Fine Paid, Fine Waived |
| Notification | Reservation-Ready Notice Sent, Reservation-Expiring Reminder Sent, Due Reminder Sent |

Not everything in this table is as-is. The three notices come from the reader survey (section 3.5 of the brief) and are **wishes**; they carry the tag `to-be`, and so does the reader account page below. *Reservation Cancelled* is not in the brief at all. We added it because a reservation that can expire probably can be cancelled, and the card is tagged `src:inferred`. Every other event has a `src:` tag that points into the brief.

Two things are worth noticing already:

- **Time is an actor.** *Reservation Expired* and *Loan Became Overdue* are not done by anybody. Today a librarian prints two lists each morning and works through them; for the overdue ones the staff phone the reader (*Reader Reminded by Phone*). On the board this is the actor **Clock (daily, per branch)**. Later it becomes a system actor and a daily sheet.
- **The same event is felt in two places.** *Book Declared Lost* is a lending fact and also starts a fee. *Book Found Damaged* ends a loan and also concerns the collection. Cards like these are where boundaries will be argued about.

### Reading the board

The board is arranged as a timeline. Events run from left to right. Hotspots sit **above** the event they concern, and actors, external systems, policies and read models hang **below** it. The order of the events is our reading of the brief, not a fact from it, so a domain expert may well move a card. The arrangement is done with the Studio's `arrange` function and moves cards only. It never changes their content.

Actors, external systems, policies and read models are not only placed under an event, they are **connected** to it, with a short label ("registers", "guards", "feeds", "reads"). Position is our reading, the connection is the fact, and only the connection survives in the export.

A JSON snapshot of the board at the end of this chapter is in [`model/sketch/big-picture.json`](../model/sketch/big-picture.json). It holds cards, tags and connections, plus the order of the events as `eventOrder`. It does not hold card positions.

### Actors and external systems

Actors: Reader/Patron/Member, Researcher, Branch Librarian, Membership Officer, Head of Collection, Treasury Liaison, Clock.

External systems, none of which we control: **National ISBN Service**, **CityPay**, **City Mail Gateway**. The brief describes how awkward each one is. We note that now, because it decides later how we talk to them.

### Rules, policies and read models

Six rules were spoken aloud in the interviews, and they are not all the same kind of thing. A **policy** in Event Storming reads "whenever *this event* happens, then *do that*". An **invariant** is a rule that must hold at the moment something is decided, such as "at most five reservations per ordinary reader". It does not react to anything. It says no.

Only one of the six is a policy: *when a member owes more than €10, block the card* (whenever a fine pushes the total over the limit, then block). The other five are invariants. They guard an event ("only a copy on the shelf can be reserved" guards *Book Reserved*) and are tagged `rule:invariant`. The Studio palette has no separate card for invariants, so we borrow the policy card and keep the tag.

> **Make the tool fit your method.** If you would rather see invariants as their own card, DDD Studio lets you define **custom kinds** for a workspace (a card kind with its own name, sections and a short description of what it is for). Define an "Invariant" kind, and the five rule cards can have their own look instead of a tag on a borrowed card. The same works for arrow kinds (for example "guards" and "feeds" instead of plain labels) and for areas. We kept the tag here to stay on the stock palette, but this is exactly the kind of adjustment the tool is meant for.
 In the model later, invariants end up on the aggregate that decides, and the one policy becomes a real policy.

Even the policy has a gap. In the brief a person blocks the card, and the policy has no actor that notices (chapter 2 comes back to this).

Three read models appear: the morning lists, the reader's account page and the monthly fines report. Each of them is a promise to somebody, and that is a good reason to keep them on the board.

### Hotspots

Ten hotspots, each connected to the card it concerns (card text shortened here):

1. *Reader / patron / member* and *item / copy / instance* are different words in different mouths.
2. Reservation kept for three or five days?
3. May a blocked card collect a reservation made before the block?
4. Shorter loan period for new releases, decided or not?
5. The overdue limit is counted per branch. Is that a rule or a habit?
6. Who declares a book lost, and when?
7. What happens to a damaged book after it "goes to Tom"?
8. Is a late fine assessed on return or every day?
9. A waiting line for books that are out: wanted, but not in the brief.
10. "Book" means the title in the catalogue and also the copy on the shelf.

The hotspots carry a tag with their type. Six are **questions for the business** (2, 3, 4, 5, 6, 8; `hotspot:question`; hotspot 8 counts here because the brief names both options). Two are **language problems** (1, 10, `hotspot:language`), and these are the most valuable ones, because they will turn into the cut between contexts. Two are **scope decisions** (7, 9, `hotspot:scope`): the brief says a damaged book "goes to Tom" and nothing about what happens next, and the waiting line is a wish (`to-be`) outside the stated scope.

## What we take into chapter 2

- The **reservation → checkout → return** path is the core of the story. It is the first Domain Story.
- The **fine** path (overdue → fine → payment → block) crosses most themes. It is the second one.
- Hotspots 1 and 10 are carried into the glossary in chapter 3.

## Open for the business (not for us)

The hotspots about reservation duration, blocked cards and the new-release period stay open on purpose. In chapter 3 we will see that the *model* can leave such rules as configuration or a deferred decision without being wrong.

## Decisions in this chapter

- **Business:** none. The open questions are collected as hotspots on the board; they are answered in [chapter 3](03-strategic-design.md).
- **Modelling, decided by the maintainer in the review:** the five rules that guard an event are drawn as invariants, only the €10 block rule as a policy. Recorded in this chapter and on the board (tags `rule:invariant`, `rule:policy`).

---

*The board lives in the DDD Studio workspace "Millbrook Library (tutorial)", board `big-picture`. Saved versions: `ch1-big-picture` (first draft) and `ch1-big-picture-v2` (after review).*
