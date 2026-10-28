# Gate G1: from the model to code

**Status:** decided by the maintainer in the conversation of 2026-10-25.
The maintainer accepted every recommendation made in that conversation
("everything you recommended works for me"). This file is the written
record of that decision; it is reviewed in its pull request. Where the
conversation left a detail open, this file says so and names the moment
it is settled.

**Level:** way of working (`docs/decisions.md`).

**Amended by the maintainer on 2026-10-28.** Four changes, written into
the text below:

1. **Phase 5 has no step of its own for contracts on the boundaries, and
   nothing about REST or OpenAPI.** The skills `model-flows`,
   `design-context-contracts` and `model-context` are replaced by one
   skill, `model-scope`, that models the whole delivery scope across the
   contexts it touches. Events that cross a boundary are modelled like any
   other event, with their payload: they are business facts, and the model
   is not complete without them. What is technology moves to phase 6: how
   front ends reach the modules, an API specification, how events are
   changed over time (announced by ADR 4), and how modules deal with
   late or repeated events.
2. **REST at the edges is reopened.** ADR 10 (accepted 2026-10-25) is
   `proposed` again and is decided at gate G2 in phase 6. Deciding it in
   phase 3 anticipated the technology. Between modules nothing changes:
   facts travel as events and orders go through the owner (ADR 4).
3. **Skills are written in hindsight and tested.** From phase 5 on, a
   chapter runs without its skill, with a short working checklist and a
   log. After the maintainer's review the skill is written from the log
   and tested by a fresh agent in a throw-away workspace.

4. **Order and shape of phase 5** (recommended by the agent at the
   maintainer's request, approved with the plan): Example Mapping first,
   then the scope modelled as flows across the contexts, then the cut
   challenged against the finished model. The retrospective of the
   modelling rates how well each step fitted DDD Studio (in a flow, static
   as Studio intends, bent, not representable).

Rejected on 2026-10-28: Example Mapping after the model (rules would be
decided after the flows stand); one flow per context (it hides how the
contexts work together); keeping a separate contract step in phase 5
(contracts here are mostly technology: delivery, versions, API style);
keeping ADR 10 accepted and only moving the OpenAPI work (then REST would
still be decided before phase 6); writing skills before their first use
without a test.

## 1. The question

After chapter 5 we have bounded contexts, a context map challenged twice
and the integration rules of a modular monolith (ADR 2 to 9). The plan
asked: how does the agent get from the model in DDD Studio to running
code, context by context? In which order, in which increments, with which
skills?

While answering it, the question grew. The maintainer wants the tutorial
to be the first run of a **reusable workflow**: someone who has a few
documents with requirements is led, step by step and with skills, through
DDD Studio to running software. G1 therefore decides the whole phase
model, not only the last step.

## 2. The decision in short

1. **Eight phases** (0 to 7), each with a goal, an owner, skills and an
   explicit end. A human approves the end of each phase.
2. **Discover wide, build narrow.** The problem scope is set in phase 0
   and discovery covers the whole target picture. The delivery scope is
   set only after the cut (phase 4).
3. **The model tests the cut.** The inside of every context in scope is
   modelled in DDD Studio in phase 5, before any code. If a boundary does
   not hold, we go back to phase 2 there, where it is cheap.
4. **Modulith first, strongly.** One deployable unit, one module per
   context, until the cut has proved itself. Pulling a module out is a
   later step with a skill of its own.
5. **Events inside.** Between modules, facts travel as events and orders
   go through the owner's public API (ADR 4). How front ends reach the
   modules is technology and is decided in phase 6 (ADR 10 is the
   proposal; amended 2026-10-28).
6. **Phase 7 builds, it does not model.** A gap found while building is
   closed in Studio first (small loop to phase 5). A cut that does not
   hold is a stop (big loop to phase 2).
7. **Skills are built in this repo**, generic in their wording. From
   phase 5 on, each one is written after its chapter, from the log of
   that chapter, and tested by a fresh agent (amended 2026-10-28). They
   are pulled out as a plugin later.

## 3. The phases

| Phase | Goal | Who does it | Skills | End (a human approves) |
|---|---|---|---|---|
| **0 Gather knowledge** | Bring in documents of any kind, rate them, merge them into one knowledge document; set the problem scope | The agent collects and rates, a human confirms | `gather-knowledge` | Knowledge document and problem scope confirmed |
| **1 Explore the domain** | Understand enough to see a cut | Big Picture: people. Domain Stories: the agent draws, a human checks | `prepare-event-storming`, `digitize-board`, `draw-domain-story`, `discovery-readiness` | "Enough to cut" |
| **2 Cut** | Subdomains, bounded contexts, context map, glossaries | The agent proposes, a fresh agent challenges | `derive-contexts`, `challenge-context-cut` | Cut accepted |
| **3 Rules of the modulith** | One unit, module = context, integration rules | The agent, opinionated | `set-modulith-rules` | Rules accepted |
| **4 Delivery scope** | Which scenarios are modelled in detail and built now | A human decides, the agent prepares | `plan-scope` | Scope accepted |
| **5 Model in detail = test the cut** | A clean model in Studio for the scope (validated, nothing in draft, exported): aggregates, commands, events with payloads, policies, process managers, read models, invariants, GWT scenarios; flows across the contexts where they carry the story | Agent and human | `example-mapping`, `model-scope`, `challenge-context-cut` (mode 2) | Model complete for the scope, **or** back to phase 2 |
| **6 Technology** | Versions, event store, database, how front ends reach the modules, front-end technology, API specification, evolution of events, delivery of late or repeated events, depth per context, deployment units (default: one) | The agent, opinionated | `decide-technology` | Gate G2 |
| **7 Build** | Implementation plan and code from the model; no business modelling | The agent | `plan-implementation`, `implement-slice`, `check-model-code` | Scope runs, **or** a loop back |
| *later* | Pull a module out once the cut is stable | The agent; a human decides | `extract-module` | — |

Above the phases sits **`ddd-workflow`**, the entry point. It reads the
state of the repo and of Studio and says which phase we are in, which
stop is open, which loop is running and which skill comes next. It is
the framework the maintainer asked for; the phase skills are its steps.

Running across all phases: `challenge-context-cut` whenever the cut
changes, a closing skill per step (today `close-chapter`, generically
`close-step`: run the checks, save versions, export), and the decision
levels of `docs/decisions.md`.

### Phase 0: gather knowledge

Requirements, loose ideas, concepts and existing documents come in side
by side. The skill rates each source (what it is, how binding, how
recent, who wrote it), finds contradictions and synonyms between sources,
and writes one harmonised knowledge document that introduces phase 1. It
also writes down the **problem scope**: which part of the organisation
we look at, and what is explicitly outside. A human confirms both.

In the tutorial this phase is thin: our brief already is one merged
document. The chapter text says so instead of inventing source documents
after the fact.

### Phase 1: explore the domain

The goal is clear, the way is not: how much Event Storming and how many
Domain Stories are needed depends on the domain. Two rules:

- **Big Picture Event Storming is done by people.** Its value comes from
  people bringing *different* knowledge into one room. An agent storming
  from a document only mirrors the document. The agent prepares the
  session (opening questions and suspected hotspots from the knowledge
  document), transfers photos or notes of the session to a sketch board,
  and checks the board against the checklist. In the tutorial the agent
  drew the Big Picture from the brief (chapter 1); the framework says
  openly that this is a stand-in.
- **Domain Stories may be drawn by the agent** from interview notes or
  transcripts. A human does the read-aloud test.

"Enough to cut" is checked, not felt (`discovery-readiness`):

- the pivotal events are named,
- every hotspot is assigned or parked,
- language conflicts are named,
- every suspected boundary is crossed by at least one story.

Process-level Event Storming belongs to phase 5, not here (§6).

### Phase 2: cut

As in chapter 3 and 5: `derive-contexts` with the heuristics, then
`challenge-context-cut` in a fresh agent. Business questions go out as
clarifications `C-nn`.

### Phase 3: rules of the modulith

Phase 3 no longer asks how many deployment units there are. It sets the
rules of the one unit: module = context, public API only, facts as
events, orders through the owner, each module owns its data (ADR 2 to 9).
How front ends reach the modules is not a rule of the modulith but
technology; it was decided here as ADR 10 on 2026-10-25 and reopened for
phase 6 on 2026-10-28. The skill is opinionated (§5).

### Phase 4: delivery scope

Phase 4 decides *what* is modelled in detail and built now; phase 5
does it. The agent prepares: the candidate scenarios from the stories
and the Big Picture, for each one the contexts and boundaries it
touches, and what it costs. The human picks the first increment. This is
a business decision and a stop of its own (gate G6 in the plan).

### Phase 5: model in detail, test the cut

The result is a **clean model in Studio that covers the delivery scope**:
aggregates, commands, events with their payloads, policies, process
managers, read models, invariants and GWT scenarios. Clean means:
validated without findings, no element in draft, exported as ESDM.
(Amended 2026-10-28: no separate contracts, no REST API.)

- **Example Mapping first** (`example-mapping`): per scenario of the
  scope, cards for story, rules, examples and questions on a sketch
  board. Questions become clarifications `C-nn` before any structure
  exists; the examples become the example data of the flows and later
  the GWT scenarios. Where most rules are already clarified, it stays
  lean.
- **Model the scope, story by story** (`model-scope`). The scenarios of
  the scope are told as flows that run across all the contexts they
  touch, as the story happens in the business, not one flow per context;
  every step names its context, and every change of context is a
  boundary under test. An overview of the boundaries, derived from the
  flows, shows which mapping each step crosses and whether its pattern
  held. A flow is like a sequence diagram: one example
  run. The static view is like a class diagram, and the flow is built
  from it. What a flow cannot show (the state, timers and end of a
  process manager, invariants, domain services, other outcomes of a
  command) is modelled directly in the static view, with the flow in
  mind. Nothing is bent to fit a slice.
- **Read every flow backwards.** From the last step to the first: every
  field of a read model comes from an event, every field of an event from
  its command, the aggregate's state or a named source, every field of a
  command from what the actor saw, from the triggering event or from a
  named input. A field that appears from nowhere is a gap in the story.
- **The cut is under test the whole time.** `challenge-context-cut` gets
  a second mode for this phase (its own file already announces it); it
  runs on the finished model of `model-scope` (amended 2026-10-28).
  Abort criteria, each one a reason to go back to phase 2:
  - an invariant needs data from two contexts at the same moment,
  - a policy has no clear owner,
  - a flow goes back and forth between two contexts,
  - an aggregate needs the state of another context to decide,
  - a word needs two meanings inside one context.

### Phase 6: technology

The first time the question of deployment units is asked, with a strong
default: one unit, a fast and cheap prototype whose cut holds; splitting
comes later. Further: versions, event store, database, how front ends
reach the modules (ADR 10 proposes REST with an API specification
written before the code), front-end technology, how events are changed
over time, how a module deals with late or repeated events, depth per
context (CRUD or event-sourced). This is gate G2.

### Phase 7: build

A concrete implementation plan from the models of phase 5 and the
technology of phase 6, then code, slice by slice. No business modelling
happens here: the model in Studio stays the only source.

## 4. Loops

| Loop | When | What happens |
|---|---|---|
| **Small: 7 → 5** | Building shows a gap in the model: a missing scenario, a missing field, an unclear rule | The gap is closed in Studio (a business question goes out as `C-nn` first), then building goes on. Nothing is decided only in code. |
| **Big: 5 or 7 → 2** | A boundary does not hold (abort criteria in phase 5) | A stop. The agent prepares the finding, `challenge-context-cut` runs again, the maintainer decides. Everything that depends on the cut is redone from phase 2. |

Phase 5 does not have to be perfect. It has to be good enough to test
the cut. Because of the small loop, scenarios can still grow while
building, as long as they grow in the model first.

## 5. Strong defaults

**Modulith first.** Most trouble with a cut appears once teams have been
formed around it. A wrong cut inside one deployable unit costs a
refactoring in one commit; across services it costs a coordinated
migration. So the workflow builds one unit with checked module
boundaries, runs phases 5 to 7 against it, and lets the cut change while
that is still cheap. Exceptions the skill names, and which must come from
the sources, not from taste: teams that already exist and work
independently, scaling or isolation demanded by the business or by
regulation, a part that must be built in other technology.

**Negotiate like separate teams, change like one repo.** Contracts
between modules are as strict as between services: who supplies, who
consumes, who may change what, a fixed schema owned by the upstream, and
events changed only by adding to them (events can be in transit even in
a modulith: the event publication registry keeps them serialised). What
differs is the technology and the cost of a change: an event is a Java
record in the module's API, an order is a call on the owner's public
interface. There is **no REST between modules** in one process. In the
model, the payload of each event is the contract; how it evolves is
decided in phase 6.

**How front ends reach the modules** is decided in phase 6 (amended
2026-10-28). ADR 10 is the proposal: REST, endpoints inside each module
as its web adapter, the OpenAPI specification written before the code
from the commands, queries and read models in Studio. The front end
composes pages from several modules either way (ADR 8).

## 6. Rejected alternatives

| Alternative | Why rejected |
|---|---|
| Modelling the inside of a context only in phase 7, just before building it (the agent's first proposal) | A wrong cut is found later and costs more. The maintainer: find and challenge the cut in the model first. |
| One architecture skill for deployment and technology | The two run at different times with different inputs (phase 3 and 6). Two narrow skills trigger more reliably and are easier to check. |
| Deciding deployment units in phase 3 | The cut is still a hypothesis there. |
| Exploring only an MVP | The cut depends on the whole target picture; contexts that come next year would be missed. |
| Process-level Event Storming as a sketch board in phase 1 and as the source of flows | Two artefacts for one process drift apart. Studio flows are the source; a sketch board only as a throw-away for a tangled process. |
| The agent drawing the Big Picture | It mirrors the documents. The agent prepares, transfers and checks. |
| "No modelling in phase 7" without a small loop | Forces a big design up front. Building always finds gaps. |
| Thymeleaf and htmx for the front end (plan §7) | Rejected on 2026-10-25 in favour of REST (ADR 10). Since ADR 10 was reopened on 2026-10-28, it is the counter-option at G2 again. |
| Generating an API specification from the code | Then the code defines the contract, not the model. Stays the guidance for G2. |
| Skills straight into a plugin or into `ddd-studio` | `ddd-studio` is behind gate G4, and skills never used once are guesswork. |
| A step of its own for the contracts on the boundaries in phase 5 (`design-context-contracts`) | Rejected 2026-10-28: the payloads are modelled with the events anyway; the rest (delivery, versions, API style) is technology for phase 6. |
| Writing a skill before its phase runs | Rejected 2026-10-28: a skill written from experience is better; a fresh agent tests it. |

## 7. Skills

**Where:** `.claude/skills/` in this repo. The skill text names no
Millbrook detail; what is specific to a repo (paths of the clarification
log, ADRs, reviews, the Studio workspace) goes into one conventions file
that each skill reads. The general rules of `CLAUDE.md` (stops, decision
levels, evidence) belong to the framework as well.

**When:** `plan-scope` (phase 4) was written while its chapter ran. From
phase 5 on (amended 2026-10-28), a chapter runs with a short working
checklist and a log, the maintainer reviews it, and only then is the
skill written from the log and tested by a fresh agent with a small
input in a throw-away workspace. The skills for phases 0 to 3 are
pulled out of chapters 0 to 5, `checks.md` and the heuristics *after* the
first context is built, and tested like a regression: a fresh agent gets
only the brief in a new throw-away workspace. Does it reach a comparable
cut? Only that run shows whether the framework carries. The same test for
`set-modulith-rules`: does a fresh agent reach ADR 2 to 9 and 11?

| Skill | Phase | Status |
|---|---|---|
| `ddd-workflow` | all | written once the phase skills of 4 and 5 exist |
| `gather-knowledge` | 0 | extracted later |
| `prepare-event-storming`, `digitize-board`, `draw-domain-story`, `discovery-readiness` | 1 | extracted later |
| `derive-contexts` | 2 | extracted later |
| `challenge-context-cut` | 2, 5 | exists; mode 2 written after chapter 9 |
| `set-modulith-rules` | 3 | extracted later, tested against ADR 2 to 9 and 11 |
| `plan-scope` | 4 | chapter 6 |
| `example-mapping` | 5 | written after chapter 7 |
| `model-scope` | 5 | written after chapter 8 |
| `decide-technology` | 6 | gate G2 |
| `plan-implementation`, `implement-slice`, `check-model-code` | 7 | first build chapter |
| `extract-module` | later | after a stable cut |
| `close-step` | all | `close-chapter` made generic when the skills are extracted |

## 8. The sub-questions of the plan, answered

| Question (plan §6) | Answer |
|---|---|
| Order | All contexts in scope modelled (phase 5) before any is built (phase 7); in phase 5 Example Mapping, then the scope story by story across the contexts, the story that crosses the most boundaries first (amended 2026-10-28). Build order by dependencies (`catalogue` and `membership` first, chapter 4). |
| Unit of an increment | In phase 7: one slice with the GWT feature that specifies it. *Settled in detail by `plan-implementation` in the first build chapter.* |
| Flows across contexts | Modelled in phase 5 by `model-scope`, where a flow can carry the story; no separate contract step (amended 2026-10-28). |
| Reading the model: MCP or export | Studio is the source and is read through MCP; flows are only there, they are not in the ESDM export. The exports are the reviewable record and are refreshed at the end of each step; if they differ, Studio wins and the export is refreshed. |
| Scenarios → tests | Every GWT scenario becomes one test; flows can become acceptance tests across contexts, specified outside Studio (tool gap 17). *Naming and the check that every scenario has a test: `check-model-code`, first build chapter.* |
| Model and code in step | `check-model-code`: modules = contexts, events = published language, every scenario has a test, and, if G2 decides on one, the code matches the API specification. |
| Who owns a rule | Every policy that crosses a boundary names its owning context in its description until Studio has a field for it (tool gap 14). `challenge-context-cut` mode 2 checks it. |
| Skills | §7. |

## 9. What it means for the tutorial

| Phase | Chapter |
|---|---|
| 0 to 3 | Chapters 0 to 5, done. ADR 10 (REST at the edges) followed chapter 4 in a pull request of its own (accepted 2026-10-25, reopened 2026-10-28). |
| 4 Delivery scope | Chapter 6, gate G6 |
| 5 Model in detail | Chapter 7 (Example Mapping), chapter 8 (modelling the scope), chapter 9 (challenging the cut in the model) |
| 6 Technology | Chapter 10, gate G2 |
| 7 Build | After G2; `catalogue` and `membership` first |

The working plan (`docs/plan.md`, §5) has the chapters in detail.
