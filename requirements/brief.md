# Millbrook Public Library — Project Brief: A New Lending System

> **A note for readers of the tutorial.** This brief is the starting point
> of everything that follows. It was put together the way briefs usually
> are: from interviews, emails and a few meetings, by people who know the
> library well and software not at all. It has not been cleaned up. Words
> are used loosely, some statements contradict each other, and some of
> the most important rules are mentioned only in passing. That is
> deliberate. Finding those spots is the work of the next chapters.

---

## 1. Background

Millbrook Public Library runs four branches: **Central**, **Riverside**,
**Northgate** and **Old Town**. About 18,000 people hold a library card;
roughly 400 of them are registered as researchers, mostly staff and
students of the university and the city archive.

Lending is managed with *LibTrack*, a system bought in 2009. The vendor
ended support last year. The library board has approved the replacement
of LibTrack by a new system, to be built by the city's own small
development team.

The new system must cover what LibTrack does today and fix what the staff
complain about. It does not need to do everything at once.

## 2. What the director wants

From the kick-off meeting with **Helen Marsh, Library Director**:

- "One system for all four branches. Today every branch has its own
  little habits, and LibTrack lets them."
- "Readers should be able to see their own account online: what they
  have at home, what's waiting for them, what they owe."
- "Fewer phone calls. Staff spend an hour a day calling people about
  reservations and late books."
- "Researchers are important to us. The archive and the university fund
  part of our special collection, and they expect us to treat it
  carefully."
- "Fines are not a revenue stream. They exist so that books come back."

## 3. Interview notes

### 3.1 Catalogue and collection — Tom Okafor, Head of Collection (Central)

- "Everything starts with the catalogue. Before a single copy goes on a
  shelf, the title has to be in the catalogue: ISBN, title, author, and
  the price — we need the price because that's what we charge if a book
  is lost."
- "A title is one entry, however many copies we have. *The Hobbit* is in
  the catalogue once; we own eleven copies of it across the branches."
- "Every physical copy gets its own barcode when we register it. Some
  people here call them items, the old system calls them instances —
  same thing."
- "When we register a copy, we decide whether it circulates or not. Most
  copies circulate. Some are kept for reference only — signed first
  editions, the local history collection, anything the archive lent us.
  Those are restricted: only researchers may borrow them. We can have a
  circulating copy and a restricted copy of the same title."
- "We get the bibliographic details from the national ISBN service. Type
  in the ISBN, get the title and author back. Half the time the author's
  name is formatted strangely or the title has the subtitle glued on. We
  fix it by hand. We have no influence on that service whatsoever."
- "You can't register a copy of a book that isn't in the catalogue yet.
  People try that all the time when a donation comes in."
- "What happens to a book after it leaves my desk is the branches'
  business, honestly. I don't need to know who has it."

### 3.2 Lending desk — Priya Nair, Branch Librarian (Riverside)

- "Readers come in, take a book off the shelf, and check it out at the
  desk. A loan runs for 60 days, at most."
- "Or they reserve it first — online or by phone — and pick it up later.
  We put the book behind the desk with their name on it. Once a book is
  reserved, nobody else can reserve it or take it."
- "You can only reserve a book that's on the shelf. People constantly
  ask to get in line for a book that's out. LibTrack can't do it, and
  honestly, it would be nice."
- "A normal reader can have five reservations at the same time. Six is
  too many. Researchers have no limit."
- "A reservation is kept for three days. If they don't come, the book
  goes back on the shelf. Northgate keeps them for five days, I think —
  you'd have to ask them."
- "Researchers can ask us to keep a book for them until they come in,
  without any time limit. Normal readers can't."
- "Every morning, first thing, I print two lists: the reservations that
  ran out yesterday, and the loans that are now overdue. Then I work
  through them. The reservations go back on the shelf; for the overdue
  ones, we call people."
- "If someone has more than two overdue books from *our* branch, we
  don't take any more reservations from them here. Doesn't matter if
  they're a researcher. They can still reserve at Central, though —
  every branch keeps its own count. That's how it's always been."
- "When a book comes back, I check it in and it's available again.
  Unless it's damaged, then it goes to Tom."
- "We call them readers. The system calls them patrons. The membership
  office calls them members. Whatever."

### 3.3 Membership office — Daniel Weber, Membership Services

- "To get a library card, you come in with your ID and proof of address.
  We register you, you get a card number, and you're a member. The card
  is valid for a year and has to be renewed."
- "Researcher status is something you apply for. You bring a letter from
  the university or the archive, we check it, and you're a researcher
  for twelve months. Then you need a new letter."
- "We block a card when someone owes more than €10 in fines. Blocked
  means: no new loans, no new reservations. When they pay, we unblock."
- "What nobody ever decided: if your card is blocked, can you still
  collect a book you reserved before the block? Every branch does it
  differently."
- "When a card expires, the member is still in the system. We don't
  delete anyone just because they forgot to renew."

### 3.4 Finance — Grace Lindqvist, Treasury Liaison (City of Millbrook)

- "Late returns cost €0.50 per day per book, starting the day after the
  book was due. The total for one book never exceeds its replacement
  price."
- "A lost book is charged at its replacement price, plus a €5 handling
  fee."
- "Some items in the special collection carry a usage fee — the archive
  insists on it. That's charged when the item is checked out, not when
  it's returned."
- "All payments go through *CityPay*, the city's payment platform. Every
  department has to use it. Its interface is what it is: odd status
  codes, amounts in cents, references limited to 20 characters. We can't
  change any of that."
- "There's been talk of a shorter loan period for new releases — 28 days
  instead of 60. Nothing decided. If it comes, fines would start after
  28 days for those, obviously."
- "We need a monthly report: fines charged, paid, waived, outstanding."

### 3.5 A reader's view — from the user survey (selected answers)

- "I'd like to see online what I have at home and when it's due."
- "Tell me when my reservation is ready. And tell me before it runs
  out — I've lost reservations because I didn't know."
- "A reminder before a book is due would be nice. I only find out I'm
  late when the fine arrives."
- "Why can I reserve at Central but not at Riverside? Nobody could
  explain it to me." *(a researcher)*

### 3.6 IT — Marcus Chen, City Development Team

- "We're a small team. One application to run, please, not a zoo of
  services. If parts need to go their own way later, fine — but not on
  day one."
- "Emails go out through the city's mail gateway. Nobody at the library
  gets to send email from anywhere else."
- "Data protection: we may not keep forever who borrowed what. Once a
  loan is closed and nothing is owed, the link between a person and a
  book has to go after a while. Legal is still working out how long."
- "The staff need a simple screen at the desk. Readers need a simple
  page for their account. Nobody needs anything fancy."

## 4. What LibTrack does that people rely on

Collected in a workshop with staff from all four branches:

- Checking books out and in at the desk.
- Reservations, entered by staff or by readers on the old web page.
- The two morning lists — expired reservations and overdue loans — per
  branch.
- Fines: LibTrack calculates them; payment is taken at the desk and
  entered by hand into CityPay's web portal afterwards.
- Membership records, card renewal, blocking.
- Searching the catalogue.

## 5. Out of scope for the first release

- E-books and other digital media.
- Borrowing from other libraries (inter-library loan).
- Buying new books (acquisitions) and the budget process.
- Room bookings and events.

## 6. Open questions collected so far

- How long are reservations kept — three days, five days, or something
  that depends on the branch?
- Can a member with a blocked card collect a reservation made before the
  block?
- Shorter loan periods for new releases: yes or no?
- How long may the connection between a person and a returned book be
  kept?

*This list is certainly not complete.*

---

*The business rules for catalogue, reservations, checkouts, the daily
lists and the overdue limit are adapted from
[ddd-by-examples/library](https://github.com/ddd-by-examples/library)
(MIT License, © 2019 Jakub Pilimon). Names, people, branches and all
other details are invented for this tutorial.*
