# Reviews

Reports of the `challenge-context-cut` skill
(`.claude/skills/challenge-context-cut/`). Each was written by a fresh
agent that got only the skill and a snapshot of the repo, not the
reasoning behind the model. A report proposes; the maintainer decides.
Draft clarification numbers in a report (`C-20`, …) are placeholders;
real numbers are given when a question goes into the log.

| Report | Input | Purpose |
|---|---|---|
| [ch03-baseline-context-cut.md](ch03-baseline-context-cut.md) | `6547c0c`, end of chapter 3 | Test of the skill: does it find the faults that were found later? |
| [ch04-context-cut.md](ch04-context-cut.md) | `9e404d9`, after chapter 4 | The real run on the current cut |
| [ch05-context-cut.md](ch05-context-cut.md) | chapter 5 branch, after the answers to the chapter 4 report | Did the answers hold, or did they bring new problems? |

## Test of the skill (2026-10-23)

The chapter 3 snapshot holds faults that were found only later, by
chapter 4 or by the maintainer. The skill was run on it to see whether
it would have found them.

| Fault, and who found it | Found by the skill? |
|---|---|
| Dependency circle lending → fees → membership → lending, called harmless (found in chapter 4) | Yes, blocking (F2) |
| Nobody asked whose rule the €10 block is (C-19, found by the maintainer) | Yes, blocking (F1), and asked as question 1 almost word for word |
| "Amount owed" from `fees` in the glossary of `membership` (found in the review of ADR 5) | Yes, as evidence in F1, not as a finding of its own |
| An unblock can lift a block placed by someone else (the first ADR 5) | Yes (F6, question 4) |

**Limits of the test.** The skill was written by the agent that knew
these faults. Examples from the library were replaced by examples from
other domains, but the rules themselves ("whose rule is it?", "read the
map as a build") are the lessons of chapters 3 and 4. The test shows
that the rules find what they were written for. It does not show that
they find unknown faults.

Better evidence is what the run on chapter 3 found besides these four:
a lost copy never leaves the catalogue (F5), nobody owns the usage fee
(F4), the open host services are justified by a count of consumers (F7),
and a reader who pays at the desk stays blocked for a while (F8). Nobody
had noticed them in chapter 3 or 4.

The run on the state after chapter 4 found seven points. Four are the
same as above and were still open; three are new, among them a mistake
of chapter 4: the Big Picture board still showed the plain block and
unblock orders that ADR 5 rejected (F3). The agent that drew the cut
checked the quoted evidence of all seven against the files; it is
correct. Chapter 5 answers the report.

(Corrected in chapter 5: an earlier version of this page said the seven
were "none of them known before", which the chapter 3 report
contradicts. Found by the independent review of chapter 5.)
