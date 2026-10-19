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
| Lending | Book Reserved, Book Kept for Researcher, Reservation Cancelled, Reservation Expired, Book Checked Out, Loan Became Overdue, Book Returned, Book Found Damaged, Book Declared Lost |
| Fees | Usage Fee Charged, Late Fine Assessed, Lost-Book Fee Charged, Fine Paid, Fine Waived |
| Notification | Reservation-Ready Notice Sent, Reservation-Expiring Reminder Sent, Due Reminder Sent |

Two things are worth noticing already:

- **Time is an actor.** *Reservation Expired* and *Loan Became Overdue* are not done by anybody. Today a librarian prints two lists each morning and works through them. On the board this is the actor **Clock (daily, per branch)**. Later it becomes a system actor and a daily sheet.
- **The same event is felt in two places.** *Book Declared Lost* is a lending fact and also starts a fee. *Book Found Damaged* ends a loan and also concerns the collection. Cards like these are where boundaries will be argued about.

### Actors and external systems

Actors: Reader/Patron/Member, Researcher, Branch Librarian, Membership Officer, Head of Collection, Treasury Liaison, Clock.

External systems, none of which we control: **National ISBN Service**, **CityPay**, **City Mail Gateway**. The brief describes how awkward each one is. We note that now, because it decides later how we talk to them.

### Policies and read models

Six rules were spoken aloud in the interviews and became policies on the board, for example "at most five reservations per ordinary reader" or "more than two overdue books at a branch: no more reservations there". Three read models appear: the morning lists, the reader's account page and the monthly fines report. Each of them is a promise to somebody, and that is a good reason to keep them on the board.

### Hotspots

Ten hotspots, each connected to the card it concerns:

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

Some hotspots are **questions for the business** (2, 3, 4, 5, 6). Others are **language problems** (1, 10), and these are the most valuable ones, because they will turn into the cut between contexts. The rest are **missing scope decisions** (7, 8, 9).

## What we take into chapter 2

- The **reservation → checkout → return** path is the core of the story. It is the first Domain Story.
- The **fine** path (overdue → fine → payment → block) crosses most themes. It is the second one.
- Hotspots 1 and 10 are carried into the glossary in chapter 3.

## Open for the business (not for us)

The hotspots about reservation duration, blocked cards and the new-release period stay open on purpose. In chapter 3 we will see that the *model* can leave such rules as configuration or a deferred decision without being wrong.

---

*The board lives in the DDD Studio workspace "Millbrook Library (tutorial)", board `big-picture`.*
