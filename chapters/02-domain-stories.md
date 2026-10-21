# Chapter 2 — Domain Stories

**Input:** [the brief](../requirements/brief.md), [chapter 1](01-big-picture.md)
**Tool:** DDD Studio, Domain Story boards
**Result:** two stories, each exported as YAML in [`model/domain-stories/`](../model/domain-stories/).

## Why a second look

The Big Picture shows *what happens*, all at once and in no particular order. A Domain Story shows *how one concrete case goes*: who does what, with which object, and who gets it next.

A sentence has the shape **actor – activity – work object – (preposition) – actor**. "Branch Librarian checks out Book to Reader" is one sentence. Reading a story aloud is the test: if a sentence sounds odd, or a domain expert says "no, that is not how we do it", the story is wrong, and that is useful to know. One sentence carries one activity, and work objects have plain names ("late fine", not "late fine of 50 cents per day"), because every rule in a name hides a second question.

We tell each story on purpose as **one happy path**. Rules, limits and exceptions (five reservations, researchers, per-branch counts, expiry, the 60 days, the €10) stay out. They live on the Big Picture as policies and hotspots and will come back as scenarios in later chapters.

A caveat: in real Domain Storytelling the stories are told *by* the people who do the work. Ours are written from the brief, so they are our best reading and nothing more. Every sentence is a question to the business.

## Story 1: Reserve, borrow, return

*As-is, pure, fine-grained.* Board `Reserve, borrow, return`.

1. The **Reader** phones in a **Reservation** to the **Branch Librarian**.
2. The Branch Librarian puts aside the **Book** behind the desk for the Reader.
3. The Branch Librarian checks out the **Book** to the Reader.
4. The Reader brings back the **Book** to the Branch Librarian.
5. The Branch Librarian checks in the **Book**.
6. The Branch Librarian puts the **Book** back on the shelf.

It is *pure*: no software appears, only people and things. We tell only the phone route here. Readers can also reserve on LibTrack's old web page, and that is a different story with a different actor.

Sentences 3 to 5 are deliberately small. "Checking out" and "checking in" are the verbs the staff use, and they will turn into events and commands later.

## Story 2: Overdue book, fine and blocked card

*As-is, digitalized, fine-grained.* Board `Overdue book, fine and blocked card`.

1. Every morning the **Branch Librarian** prints the **List of overdue loans** from **LibTrack**.
2. The Branch Librarian makes a **Reminder call** to the **Reader**.
3. The Reader brings back the **Overdue book** to the Branch Librarian.
4. The Branch Librarian checks in the **Overdue book** in LibTrack.
5. LibTrack calculates the **Late fine**.
6. The **Membership Officer** blocks the **Library card** of the Reader.
7. The Reader pays the **Fine** at the desk to the Branch Librarian.
8. The Branch Librarian types in the **Payment** by hand into the web portal of **CityPay**.
9. The Membership Officer unblocks the **Library card** of the Reader.

This one is *digitalized*, because the two systems are part of the problem. LibTrack and CityPay show up as actors.

## What the stories show that the Big Picture did not

- **Nobody triggers the block, and nobody triggers the unblock.** The brief says a card is blocked above €10 and unblocked after payment. It never says how the Membership Officer finds out in either case. Sentences 6 and 9 are therefore our guess at the order, not something we heard. On the Big Picture the policy "when a member owes more than €10, block the card" has no actor behind it. The story makes that gap visible. *Who notices, and when?*
- **A payment is keyed in by hand.** The reader pays at the desk, and afterwards the librarian types the payment into CityPay's portal (sentences 7 and 8). The brief does not say whether LibTrack learns about the payment too. If it does not, someone has to keep two places in step. That is a question for the business, and it matters for the boundary around CityPay in chapter 3.
- **The morning list is the clock, done by a person.** In sentence 1 a human prints and works through a list. On the Big Picture this was the actor *Clock*. The story shows it as a daily ritual that a system could take over.
- **"Book" is used for everything.** In both stories the Reader's request, the thing behind the desk and the thing on the shelf are all "the book". The catalogue entry and the physical copy are one word again, as in hotspot 10 of chapter 1. The brief's own rule, "only a copy on the shelf can be reserved", only makes sense if we can tell them apart. This is the strongest language signal so far.
- **How does the reader learn that the book is ready?** The brief does not say. The survey asks for exactly this ("Tell me when my reservation is ready") and the director wants fewer phone calls, which suggests there is no systematic notice today. Story 1 therefore has no such sentence. We did not invent one. On the Big Picture the notices are wishes from the survey, so they belong to a later to-be view and not to these as-is stories.
- **The fine is assessed on return, but only in our story.** Whether a late fine is assessed on return or every day is hotspot 8. Story 2 puts the calculation after the return (sentence 5) because the brief mentions the fine after the book comes back. Take that as a placeholder, not as an answer.

## What we take into chapter 3

- The two stories give us a first idea of **where the seams are**: catalogue and copies, lending, fines and payment, membership. Chapter 3 compares them with the themes from the Big Picture and cuts.
- The glossary starts with three entries that clearly need a decision: *book* (title or copy), *reader / patron / member*, *item / copy / instance*.
- Three questions go to the business: who triggers a block and an unblock, what happens to a payment on the way from the desk to CityPay and back, and when the late fine is assessed.

---

*The boards live in the DDD Studio workspace "Millbrook Library (tutorial)". Saved versions: `ch2-reserve-borrow-return-v2` and `ch2-overdue-fine-blocked-card-v2`.*
