# Gate G1: from the model to code

**Status:** decided by the maintainer in the conversation of 2026-10-25.
The maintainer accepted every recommendation made in that conversation
("everything you recommended works for me"). This file is the written
record of that decision; it is reviewed in its pull request. Where the
conversation left a detail open, this file says so and names the moment
it is settled.

**Level:** way of working (`docs/decisions.md`).

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
5. **REST at the edges, events inside.** All front ends use the modules
   through REST APIs; between modules, facts travel as events and orders
   go through the owner's public API (ADR 4). API first: the OpenAPI
   specification of a module is written before its code.
6. **Phase 7 builds, it does not model.** A gap found while building is
   closed in Studio first (small loop to phase 5). A cut that does not
   hold is a stop (big loop to phase 2).
7. **Skills are built in this repo**, generic in their wording, each one
   while its phase runs in the tutorial. They are pulled out as a plugin
   later.

## 3. The phases

| Phase | Goal | Who does it | Skills | End (a human approves) |
|---|---|---|---|---|
| **0 Gather knowledge** | Bring in documents of any kind, rate them, merge them into one knowledge document; set the problem scope | The agent collects and rates, a human confirms | `gather-knowledge` | Knowledge document and problem scope confirmed |
| **1 Explore the domain** | Understand enough to see a cut | Big Picture: people. Domain Stories: the agent draws, a human checks | `prepare-event-storming`, `digitize-board`, `draw-domain-story`, `discovery-readiness` | "Enough to cut" |
| **2 Cut** | Subdomains, bounded contexts, context map, glossaries | The agent proposes, a fresh agent challenges | `derive-contexts`, `challenge-context-cut` | Cut accepted |
| **3 Rules of the modulith** | One unit, module = context, integration rules, REST at the edges | The agent, opinionated | `set-modulith-rules` | Rules accepted |
| **4 Delivery scope** | Which scenarios are modelled in detail and built now | A human decides, the agent prepares | `plan-scope` | Scope accepted |
| **5 Model in detail = test the cut** | A static model in Studio for the scope: contracts, aggregates, invariants, GWT scenarios; flows where they help | Agent and human | `model-flows`, `design-context-contracts`, `example-mapping`, `model-context`, `challenge-context-cut` (mode 2) | Model complete for the scope, **or** back to phase 2 |
| **6 Technology** | Versions, event store, database, front-end technology, depth per context, deployment units (default: one) | The agent, opinionated | `decide-technology` | Gate G2 |
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
events, orders through the owner, each module owns its data, REST at the
edges (ADR 2 to 9; REST at the edges was decided by the maintainer on 2026-10-25 and is recorded as ADR 10). The skill is opinionated
(§5).

### Phase 4: delivery scope

Phase 4 decides *what* is modelled in detail and built now; phase 5
does it. The agent prepares: the candidate scenarios from the stories
and the Big Picture, for each one the contexts and boundaries it
touches, and what it costs. The human picks the first increment. This is
a business decision and a stop of its own (gate G6 in the plan).

### Phase 5: model in detail, test the cut

The result is a **static model in Studio that covers the delivery
scope**: aggregates, commands, events, policies, read models, invariants,
GWT scenarios, and the contract on every boundary the scope crosses.

- **First the boundaries, then the inside.** The flows across contexts
  and the contracts on each boundary (`model-flows`,
  `design-context-contracts`): which scenario crosses which boundary, in
  which direction, with which kind of contract (fact → event, order →
  public command of the owner, question → query for the front end), the
  payload schema, and what the downstream does when an event comes late
  or twice (ADR 4). The rule for changing events that ADR 4 announced is
  written here.
- **Flows are optional.** A flow is like a sequence diagram: one example
  run. The static view is like a class diagram, and drawing a flow fills
  it. Flows help where a process crosses several boundaries; everything
  can also be modelled without them.
- **Example Mapping** (`example-mapping`) per story: cards for story,
  rules, examples and questions on a sketch board. Examples become GWT
  scenarios, questions become clarifications `C-nn`.
- **The inside of each context** (`model-context`), including its REST
  API, which follows from its commands, read models and the pages that
  need them.
- **The cut is under test the whole time.** `challenge-context-cut` gets
  a second mode for this phase (its own file already announces it).
  Abort criteria, each one a reason to go back to phase 2:
  - an invariant needs data from two contexts at the same moment,
  - a policy has no clear owner,
  - a flow goes back and forth between two contexts,
  - an aggregate needs the state of another context to decide,
  - a word needs two meanings inside one context.

### Phase 6: technology

The first time the question of deployment units is asked, with a strong
default: one unit, a fast and cheap prototype whose cut holds; splitting
comes later. Further: versions, event store, database, front-end
technology (REST is set; the front end is a separate client), depth per
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
interface. There is **no REST between modules** in one process.

**REST at the edges, API first.** Every front end uses the modules
through REST. The endpoints sit inside each module as its web adapter
(as ADR 6 does for the adapters to external systems); the front end composes pages from
several modules (ADR 8). A backend for frontend stays the way out if a
page needs too many calls. The OpenAPI specification of a module is
written before its code, derived from its commands, queries and read
models in Studio, and the code is tested against it. Here a second
artefact is worth its cost: the consumer is a front end in other
technology and needs a language-neutral contract. Between modules the
payload schemas in Studio are the contract; AsyncAPI or OpenAPI for them
only when a module is pulled out.

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
| Thymeleaf and htmx for the front end (plan §7) | The maintainer wants REST for every front end (conversation of 2026-10-25; ADR 10). |
| Generating the OpenAPI specification from the code | Then the code defines the contract, not the model. |
| Skills straight into a plugin or into `ddd-studio` | `ddd-studio` is behind gate G4, and skills never used once are guesswork. |

## 7. Skills

**Where:** `.claude/skills/` in this repo. The skill text names no
Millbrook detail; what is specific to a repo (paths of the clarification
log, ADRs, reviews, the Studio workspace) goes into one conventions file
that each skill reads. The general rules of `CLAUDE.md` (stops, decision
levels, evidence) belong to the framework as well.

**When:** each skill from phase 4 on is written while its phase runs in
the tutorial and is used there for real. The skills for phases 0 to 3 are
pulled out of chapters 0 to 5, `checks.md` and the heuristics *after* the
first context is built, and tested like a regression: a fresh agent gets
only the brief in a new throw-away workspace. Does it reach a comparable
cut? Only that run shows whether the framework carries. The same test for
`set-modulith-rules`: does a fresh agent reach ADR 2 to 10?

| Skill | Phase | Status |
|---|---|---|
| `ddd-workflow` | all | written once the phase skills of 4 and 5 exist |
| `gather-knowledge` | 0 | extracted later |
| `prepare-event-storming`, `digitize-board`, `draw-domain-story`, `discovery-readiness` | 1 | extracted later |
| `derive-contexts` | 2 | extracted later |
| `challenge-context-cut` | 2, 5 | exists; mode 2 added in phase 5 |
| `set-modulith-rules` | 3 | extracted later, tested against ADR 2 to 10 |
| `plan-scope` | 4 | chapter 6 |
| `model-flows`, `design-context-contracts` | 5 | chapter 7 |
| `example-mapping`, `model-context` | 5 | chapter 8 |
| `decide-technology` | 6 | gate G2 |
| `plan-implementation`, `implement-slice`, `check-model-code` | 7 | first build chapter |
| `extract-module` | later | after a stable cut |
| `close-step` | all | `close-chapter` made generic when the skills are extracted |

## 8. The sub-questions of the plan, answered

| Question (plan §6) | Answer |
|---|---|
| Order | Boundaries before inside; all contexts in scope modelled (phase 5) before any is built (phase 7). Modelling order by risk (`lending` first), build order by dependencies (`catalogue` and `membership` first, chapter 4). |
| Unit of an increment | In phase 7: one slice with the GWT feature that specifies it. *Settled in detail by `plan-implementation` in the first build chapter.* |
| Flows across contexts | Modelled first in phase 5, together with the contract on each boundary. |
| Reading the model: MCP or export | Studio is the source and is read through MCP; flows are only there, they are not in the ESDM export. The exports are the reviewable record and are refreshed at the end of each step; if they differ, Studio wins and the export is refreshed. |
| Scenarios → tests | Every GWT scenario becomes one test; flows can become acceptance tests across contexts, specified outside Studio (tool gap 17). *Naming and the check that every scenario has a test: `check-model-code`, first build chapter.* |
| Model and code in step | `check-model-code`: modules = contexts, events = published language, every scenario has a test, the code matches the OpenAPI specification. |
| Who owns a rule | Every policy that crosses a boundary names its owning context in its description until Studio has a field for it (tool gap 14). `challenge-context-cut` mode 2 checks it. |
| Skills | §7. |

## 9. What it means for the tutorial

| Phase | Chapter |
|---|---|
| 0 to 3 | Chapters 0 to 5, done. ADR 10 (REST at the edges) follows chapter 4 in a pull request of its own (accepted 2026-10-25). |
| 4 Delivery scope | Chapter 6, gate G6 |
| 5 Model in detail | Chapter 7 (boundaries and flows), then the inside of the contexts, `lending` first |
| 6 Technology | After phase 5, gate G2 |
| 7 Build | After G2; `catalogue` and `membership` first |

The working plan (`docs/plan.md`, §5) has the chapters in detail.
