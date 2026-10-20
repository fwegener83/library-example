# Chapter 2 — Domain Stories

**Input:** [the brief](../requirements/brief.md), [chapter 1](01-big-picture.md)
**Tool:** DDD Studio, Domain Story boards
**Result:** two stories, each exported as YAML in [`model/domain-stories/`](../model/domain-stories/).

## Why a second look

The Big Picture shows *what happens*, all at once and in no particular order. A Domain Story shows *how one concrete case goes*: who does what, with which object, and who gets it next. Each sentence has an actor, an activity and a work object. Reading a story aloud is the test. If a domain expert says "no, that is not how we do it", the story is wrong, and that is useful to know.

We tell stories on purpose with **one happy path** each. Rules, limits and exceptions (five reservations, researchers, per-branch counts, expiry) stay out. They live on the Big Picture as policies and hotspots and will come back as scenarios in later chapters.

A caveat: in real Domain Storytelling the stories are told *by* the people who do the work. Ours are written from the brief, so they are our best reading and nothing more. Treat every sentence as a question to the business.

## Story 1: Reserve, borrow, return

*As-is, pure, fine-grained.* Board `Reserve, borrow, return`.

1. A **Reader** asks the **Branch Librarian** for a **Reservation** of a book on the shelf, by phone or online.
2. The Branch Librarian puts the **Book** aside, behind the desk, with the reader's name.
3. The Reader comes to the desk and collects the **Reserved book**.
4. The Branch Librarian checks out the **Book** and hands it to the Reader, for up to 60 days.
5. The Reader brings the **Book** back to the desk.
6. The Branch Librarian checks it in and puts it back on the **Shelf**.

It is *pure*: no software appears, only people and things. That is the right level to start with.

## Story 2: Overdue book, fine and blocked card

*As-is, digitalized, fine-grained.* Board `Overdue book, fine and blocked card`.

1. Every morning the **Branch Librarian** prints the **List of overdue loans** from **LibTrack**.
2. The Branch Librarian phones the **Reader** about the **Overdue book**.
3. The Reader brings the book back.
4. LibTrack calculates the **Late fine** (€0.50 per day, up to the price) and shows it to the Branch Librarian.
5. The **Membership Officer** blocks the **Library card**, because the reader owes more than €10.
6. The Reader pays the fine at the desk.
7. The Branch Librarian types the **Payment** into the web portal of **CityPay**, by hand.
8. The Membership Officer unblocks the card.

This one is *digitalized*, because the two systems are part of the problem. LibTrack and CityPay show up as actors.

## What the stories show that the Big Picture did not

- **Nobody triggers the block.** In sentence 5 the Membership Officer blocks the card, but the brief never says how they find out that someone owes more than €10. The Big Picture has the policy "when a member owes more than €10, block the card" and no actor behind it. The story makes the gap visible: *who notices, and when?*
- **Payment is entered twice.** The reader pays at the desk, then the librarian types the same payment into CityPay (sentences 6 and 7). This is today's pain, and the director's "fewer phone calls" and "fines exist so books come back" both sit around it. The new system will talk to CityPay itself, and we will see in chapter 3 why that boundary needs care.
- **The morning list is a person.** In sentence 1 a human prints and works through a list. The Big Picture called this *Clock*. A story shows it as a ritual that a system could take over.
- **"Book" is used for everything.** The Reader asks for a reservation of a *book*, the librarian puts a *book* aside, the same *book* is checked out and returned. The catalogue entry and the physical copy are the same word again, as in hotspot 10 of chapter 1. Even in a happy path we cannot tell which of the two is meant. This is the strongest language signal so far.
- **The block comes before the payment.** The card is blocked as soon as the fine is calculated, and unblocked only after the payment. Fine, payment and card status change together, and the two stories touch each other here.

## What we take into chapter 3

- The two stories give us our first idea of **where the seams are**: catalogue and copies, lending, fines and payment, membership. Chapter 3 compares them with the themes from the Big Picture and cuts.
- The glossary starts with three entries that clearly need a decision: *book* (title or copy), *reader / patron / member*, *item / copy / instance*.
- The block trigger and the double payment entry go on the list of questions for the business.

---

*The boards live in the DDD Studio workspace "Millbrook Library (tutorial)". Saved versions: `ch2-reserve-borrow-return` and `ch2-overdue-fine-blocked-card`.*
