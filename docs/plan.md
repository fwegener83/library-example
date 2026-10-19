# Plan: Library-Tutorial — von Anforderungen zu laufender Software

*Arbeitsdokument zur Abstimmung (deutsch). Das Tutorial selbst wird englisch.*
*Stand: 2026-10-19 · Status: Teil A freigegeben, Teil B hinter Gate G1*

---

## 0. Arbeitsweise: Gates

Viele Fragen klären wir erst, wenn wir an der Stelle stehen. Damit dabei
nichts auf Annahmen gebaut wird, gilt:

> **Ein Gate ist ein harter Halt.** Vor einem Gate höre ich auf, lege eine
> Entscheidungsvorlage vor (Optionen, Abwägung, Empfehlung) und arbeite
> erst weiter, wenn **die Freigabe ausdrücklich von dir** kommt. Kein
> Vorgriff, keine „vorläufige" Umsetzung hinter einem offenen Gate.

Erlaubt vor einem Gate ist nur die **Vorbereitung der Entscheidung**
(Recherche, Ausprobieren in einer Wegwerf-Umgebung, Vorlage schreiben) —
nichts, was ins Tutorial oder in den Code eingeht.

| Gate | Wann | Was geklärt wird | Status |
|---|---|---|---|
| **G0** | nach Kapitel 0 | Review des Anforderungsdokuments — alles Weitere baut darauf auf | offen |
| **G1 — SDD** | nach Kapitel 4a, **vor jeder Arbeit pro Bounded Context** | Zusammenspiel DDD Studio ↔ Spec Kit: Reihenfolge, Zuschnitt einer Spec, Rollen (§6) | offen |
| **G2 — Technik** | vor dem Projekt-Skelett | Versionen, Event-Store-Ansatz, UI-Technik, Datenbank (§7) | offen |
| **G3 — F2** | bevor `lending` im Detail modelliert wird | Woher `lending` weiß, ob ein Exemplar „restricted" ist (§11) | offen |
| **G4 — In-App-Beispiel** | bevor irgendetwas in `ddd-studio` geändert wird | Ersetzen des Library-Beispiels (§10) | offen |
| **G5 — Erweiterungen** | nach fertiger Basis | Process-Manager-Kapitel (F1), Evolutionskapitel (F4) | offen |

Daneben gibt es **weiche Reviews**: Jedes Kapitel kommt als eigener
Pull Request. Du reviewst, ich arbeite Änderungen ein; innerhalb von
Teil A darf ich parallel am nächsten Kapitel weiterarbeiten, sobald G0
durch ist.

---

## 1. Ziel und Kernbotschaft

Ein durchgängiges Tutorial, das zeigt, wie man aus einem unscharfen
Anforderungsdokument mit DDD zu einem belastbaren Domänenschnitt kommt und
von dort — Bounded Context für Bounded Context, als ob getrennte Teams
arbeiten — zu laufender Software.

**Drei Botschaften, an denen sich jedes Kapitel messen lassen muss:**

1. **Erst verstehen, dann schneiden, dann bauen.** Big Picture Event
   Storming und Domain Stories liefern die Kontextgrenzen.
2. **Das Modell treibt die Umsetzung.** Domänenmodell (DDD Studio) und
   Spec-Driven Development (Spec Kit) haben getrennte, klar benannte
   Zuständigkeiten — *wie genau*, klärt Gate G1.
3. **Grenzen sind anfangs Hypothesen.** Deshalb ein modularer Monolith mit
   *geprüften* Modulgrenzen.

**Zielgruppe:** Entwickler:innen und Architekt:innen mit Grundkenntnissen
in Java/Spring, die DDD „schon mal gehört" haben und sehen wollen, wie die
Teile zusammenpassen. Konzepte werden dort erklärt, wo sie gebraucht
werden.

---

## 2. Ausgangslage

- **Zwei Library-Modelle in DDD Studio:**
  - **Erster Schnitt (heute In-App):**
    `packages/core/src/examples/library-cataloging.ts`,
    `docs/examples/tutorial-library-example.md`. Kataloghälfte aus ESDMs
    „Your First Model", Ausleihhälfte dazuerfunden. BCs `cataloging` und
    `lending`, zwei gegenläufige Policies → **Partnership**.
  - **Zweiter Schnitt = Adaption von `ddd-by-examples/library`:**
    hinzugefügt in `0bc3c1be`, entfernt in `0e0797ff`, wiederherstellbar
    aus `0e0797ff^` (`packages/core/src/examples/library-lending.ts`,
    `docs/tutorial-library-lending.md`). BCs `catalogue` (supporting) und
    `lending` (core), **Customer/Supplier**, Verfügbarkeit in `lending`,
    eine Überquerung in eine Richtung, Aggregate `patron` mit vier
    Haltelimit-Regeln, Homonym `book`, Tagesblatt mit System-Akteur,
    12 Slices, 6 Invarianten.
- **`ddd-by-examples/library`** (MIT, © 2019 Jakub Pilimon) liefert die
  fachliche Vorlage: Geschäftsregeln im README, `docs/big-picture.md`,
  `docs/design-level.md`. Wir adaptieren Regeln und Begriffe mit
  Quellenangabe; Code übernehmen wir nicht.

**Konsequenz:** Das Tutorial baut auf dem zweiten Schnitt auf und erweitert
ihn. Der erste Schnitt erscheint in Kapitel 3 als naheliegende, verworfene
Hypothese („Verfügbarkeit gehört zum Katalog" → gegenläufige Policies →
Partnership).

---

## 3. Getroffene Entscheidungen

| Thema | Entscheidung |
|---|---|
| Domäne | Bibliothek auf Basis des zweiten Schnitts, erweitert |
| Stack | Java, Spring Boot, Spring Modulith (Details: G2) |
| Sprache | Englisch (Tutorial, Code, Modell); dieses Planungsdokument deutsch |
| Ort | eigenes Repo `fwegener83/library-example` |
| Deployment | eine Deployment-Einheit, Module = Bounded Contexts |
| Teams | gedanklich getrennte Teams pro BC, sichtbar über Verträge |
| UI | **kleine, minimale UI** — macht das Ergebnis greifbar (Technik: G2) |
| Format | Markdown-Kapitel im Repo; später Übernahme auf die DDD-Studio-Homepage |
| F1 Process Manager | vorerst **ohne**; ggf. später eigener Abschnitt (G5) |
| F4 Evolution | erst die Basis; danach als Erweiterung (G5) |

---

## 4. Domänenzuschnitt (Hypothese — wird im Tutorial *hergeleitet*)

Das Anforderungsdokument (Kap. 0) wird so geschrieben, dass dieser Schnitt
im Event Storming naheliegt, aber nicht offensichtlich ist.

| Kontext | Subdomain | Team (fiktiv) | Tiefe | Lehrzweck | Herkunft |
|---|---|---|---|---|---|
| `catalogue` | Supporting | Team Collection | CRUD | Datensätze + Exemplare; Homonym `book` | 2. Schnitt |
| `lending` | **Core** | Team Circulation | event-sourced | Patron-Regeln, Holds, Checkouts, Überfälligkeit, Tagesblatt | 2. Schnitt |
| `membership` | Supporting | Team Members | CRUD | Registrierung, Patron-Typ, Sperren | neu |
| `fees` | Supporting | Team Finance | event-sourced | Gebühren, Zahlung über ACL | neu |
| `notification` | Generic | Team Platform | dünn | reiner Event-Konsument | neu |
| *Payment Provider* | extern | — | Stub | **Anti-Corruption Layer** | neu |
| *Book Metadata Service* | extern | — | echter Aufruf + Stub im Test | ACL vs. Conformist | neu |

**Context-Map-Hypothese:**

- `catalogue` → `lending`: **Customer/Supplier**, eine Überquerung in eine Richtung
- `membership` → `lending`: **Customer/Supplier**; *member* in membership,
  *patron* in lending (zweite Sprachlektion)
- `lending` → `fees`, `notification`: **Open Host Service + Published Language**
- `fees` → `membership`: **Customer/Supplier** (offene Gebühren sperren)
- `fees` → Payment Provider: **ACL**
- `catalogue` → Metadata Service: **ACL** (Alternative Conformist diskutiert)
- **Shared Kernel** diskutiert und verworfen; **Partnership** des ersten
  Schnitts als verworfene Hypothese

**Nicht jeder Kontext verdient dieselbe Tiefe:** `catalogue` und
`membership` bleiben CRUD, `notification` ein Listener.

---

## 5. Ablauf

### Teil A — freigegeben

| # | Kapitel | Werkzeug | Ergebnis im Repo |
|---|---|---|---|
| 0 | **The brief** — Anforderungsdokument der Stadtbibliothek: Interviewnotizen, absichtlich lückenhaft, mit Synonymen und Widersprüchen | Text | `requirements/brief.md` |
| | **→ Gate G0** | | |
| 1 | **Big Picture Event Storming** — Exploration, Zeitleiste, Schlüsselereignisse, Hotspots, Akteure, externe Systeme | Sketch Board | `model/sketch/…`, Screenshots |
| 2 | **Domain Stories** — 2–3 Kernprozesse; Sprachkonflikte klären | Domain Stories | `model/stories/…` |
| 3 | **Strategic design** — Subdomains, Bounded Contexts, Glossar, Context Map mit Mustern, Teamzuordnung; verworfene Partnership-Hypothese | Context Map, Glossar | `model/library.esdm.yaml` (strategisch) |
| 4a | **Deployment decision** — Modulith, Modul = BC, Integrationsregeln als ADRs | ADRs | `docs/adr/…` |

### → Gate G1 (SDD) — harter Halt

Alles ab hier hängt davon ab, *in welcher Reihenfolge* pro Bounded Context
Feinmodellierung und Spec-Driven Development ineinandergreifen. Die
folgende Gliederung ist deshalb **vorläufig** und wird nach G1 neu
geschnitten.

### Teil B — vorläufig, nach G1 (und G2/G3) neu zu planen

| # | Kapitel (Arbeitstitel) | Werkzeug |
|---|---|---|
| 4b | Constitution aus dem strategischen Design | Spec Kit |
| 5 | Kontextübergreifende Flows | Flow View |
| 6 | Feinmodellierung je Kontext (Aggregates, Invarianten, Slices, GWT) | Static View, Slices, Scenarios |
| 7 | Vom Modell zur Spec | Spec Kit + DDD-Studio-MCP |
| 8 | Umsetzung inkl. minimaler UI | Code, Spring Modulith |

Umsetzungstiefe im Code (Vorschlag): voll — `lending`, `fees` + ACL;
schlicht — `catalogue`, `membership` (CRUD), `notification` (Stub).

### Erweiterungen — nach G5

- **Process Manager** (F1): z. B. ein Mahnlauf über mehrere Kontexte,
  abgewogen gegen Policy-Choreographie.
- **Evolution** (F4): eine neue Anforderung (z. B. E-Books) verschiebt den
  Schnitt; Modell → Spec → Code ändern sich in dieser Reihenfolge.

---

## 6. Kernthema für G1: DDD und Spec-Driven Development

*Nichts in diesem Abschnitt ist entschieden. Er sammelt die Frage, das
Material und die Vorbereitung für G1.*

### 6.1 Die Frage

Nach Kapitel 4a haben wir: Bounded Contexts, eine Context Map mit
Beziehungen, eine Deployment-Entscheidung. Jetzt rückt erstmals **pro
Bounded Context** die Umsetzung in den Fokus.

> **Was passiert dann zuerst — und was ist die Einheit, die von DDD Studio
> an Spec Kit übergeht?**

Teilfragen:

- **Reihenfolge:** Erst Feinmodellierung in DDD Studio (Flows, Slices,
  Szenarien), dann Spec? Oder erst eine Spec (Nutzen, Scope), die die
  Feinmodellierung anstößt? Oder abwechselnd, Slice für Slice?
- **Einheit:** Ist ein *Flow* eine Spec? Ein *Slice*? Ein *Feature* mit
  GWT-Szenarien? Eine Nutzerfähigkeit innerhalb eines BC?
- **Kontextübergreifende Flows:** Wer spezifiziert einen Ablauf, der über
  mehrere Teams läuft — und wie hängen die Team-Specs zusammen?
- **Wahrheit:** Spec Kit versteht die Spec als „source of truth", DDD
  Studio das Modell. Wer ist wofür Master, ohne dass es doppelt geführt
  wird? (Risiko: „Key Entities" und `data-model.md` beschreiben die
  Fachlichkeit ein zweites Mal.)
- **Werkzeuge:** Reicht eine Constitution, oder braucht es ein eigenes
  Spec-Kit-Preset? Wie liest der Agent das Modell (MCP oder ESDM-Export)?
- **Szenarien → Tests:** von Hand mit Namenskonvention oder generiert?

### 6.2 Material aus der bisherigen Diskussion (nicht entschieden)

Ein Vorschlag lag schon auf dem Tisch und dient G1 als Ausgangspunkt:
*Modell = was die Domäne ist; Spec = warum, welches Inkrement, wie
gebaut.* Dazu: Constitution aus dem strategischen Design, Preset mit
„Domain model references" statt „Key Entities", Szenarien als zuerst
fehlschlagende Tests, CI-Prüfungen (jedes Szenario hat einen Test; Module
== BCs). Alternativen: *Spec-first* (Modell als Dekoration) und
*Model-only* (ohne Spec Kit). Alles davon steht in G1 zur Disposition.

### 6.3 Vorbereitung für G1 (erlaubt vor dem Gate)

1. **Spec Kit praktisch erkunden** — aktuelle Version in einer
   Wegwerf-Umgebung installieren und einmal durchspielen: Welche Befehle
   gibt es wirklich (die Benennung hat sich geändert, z. B. Skills
   `/speckit-…`, neu `/speckit-converge`), welche Dateien entstehen, wie
   sehen die Templates aus, was können Presets und Extensions?
2. **Entscheidungsvorlage** `docs/decisions/g1-sdd.md`: Fakten zu Spec
   Kit, zwei bis drei durchgespielte Varianten am konkreten Beispiel eines
   `lending`-Slices, Abwägung, Empfehlung.
3. Dann: gemeinsame Runde, Entscheidung von dir, Teil B neu planen.

---

## 7. Technik (Vorschlag — Entscheidung in G2)

- Java (aktuelles LTS), Spring Boot, Spring Modulith; Versionen in G2.
- Ein Modul pro BC als Top-Level-Package; öffentlich nur Modul-API und
  Integration Events; `ApplicationModules.verify()` im Test.
- Event Sourcing von Hand und lesbar: Aggregate als *Decider*
  (`decide`/`evolve`, sealed Interfaces + Records), schlanker
  JDBC-Event-Store in Postgres. Kein Axon (versteckt das Konzept).
- Policies als `@ApplicationModuleListener` im Downstream-Modul; Event
  Publication Registry = Outbox mit at-least-once.
- System-Commands aus dem Tagesblatt per Scheduler.
- **Minimale UI** — Kandidaten für G2: serverseitig (Thymeleaf + htmx,
  bleibt im Spring-Monolithen, minimaler Aufwand) vs. kleine SPA.
  Vorschlag: serverseitig; Seiten etwa Katalogsuche, Patron-Profil,
  Ausleihtheke, Tagesblatt.
- Tests: Decider-Unit-Tests aus Szenarien, Modulith-Scenario-Tests,
  Testcontainers, WireMock.

---

## 8. Repo-Struktur

```
library-example/
├── README.md
├── requirements/brief.md        # Kapitel 0
├── model/                       # ESDM-Exporte, Stories, Sketch-Exporte
├── docs/
│   ├── plan.md                  # dieses Dokument
│   ├── decisions/               # Entscheidungsvorlagen der Gates
│   ├── tutorial/NN-*.md         # die Kapitel
│   └── adr/
├── .specify/ · specs/           # Spec Kit — Struktur nach G1
└── src/…                        # nach G2
```

Git-Tags pro Kapitel; Studio-Workspace mit gleichnamigen Versionen;
öffentlicher Read-only-Link pro Stand.

---

## 9. Meilensteine

| M | Inhalt | Gate davor |
|---|---|---|
| M1 | Kapitel 0: Anforderungsdokument | — |
| M2 | Kapitel 1–3 im Studio + Export + Texte | G0 |
| M3 | Kapitel 4a: Deployment-ADRs | G0 |
| M4 | Vorbereitung G1: Spec Kit erkunden, Entscheidungsvorlage | — (Vorbereitung) |
| — | **G1, G2** | |
| M5+ | Teil B, neu geplant | G1, G2, G3 |
| — | **G4, G5** | |

---

## 10. Rückwirkungen auf DDD Studio (hinter G4)

- **In-App-Beispiel:** Vorschlag — ersten Schnitt durch den zweiten
  ersetzen (aus `0e0797ff^` wiederherstellen, an den heutigen
  Metamodell-Stand anpassen). Erweiterungen bleiben im Tutorial-Workspace;
  das In-App-Beispiel bleibt „der kurze Einstieg".
- **Werkzeuglücken sammeln, nicht nebenbei fixen** — als Issues im
  `ddd-studio`-Repo.
- **Homepage:** Beitrag + Link aufs Repo und die Read-only-Workspaces —
  später.

---

## 11. Register offener Punkte

| ID | Frage | Gate | Stand |
|---|---|---|---|
| S1–S6 + Reihenfolge | Zusammenspiel DDD Studio ↔ Spec Kit (§6) | G1 | offen |
| T1 | Java-, Spring-Boot-, Modulith-Versionen | G2 | offen |
| T2 | Event-Store-Ansatz (Vorschlag: von Hand, Decider) | G2 | offen |
| T3 | UI-Technik (Vorschlag: Thymeleaf + htmx) | G2 | offen |
| F1 | Process Manager | G5 | vorerst ohne |
| F2 | Woher kennt `lending` den Exemplartyp? (siehe unten) | G3 | offen |
| F3 | UI | — | **entschieden:** minimale UI |
| F4 | Evolutionskapitel | G5 | nach der Basis |
| F5 | Format | — | **entschieden:** Markdown im Repo |
| E1 | In-App-Beispiel ersetzen | G4 | offen |

**F2 in einfachen Worten.** Nur Researcher dürfen ein *restricted*
Exemplar vormerken. Ob ein Exemplar restricted ist, weiß ursprünglich der
**Katalog**. Die Regel wird aber in `lending` geprüft. Im zweiten Schnitt
hat man das gelöst, indem der **Aufrufer** den Typ im Vormerk-Command
mitschickt — die UI sagt also „das ist restricted", und `lending` glaubt
es. Alternative: Der Katalog schickt den Typ ohnehin mit, wenn er ein neues
Exemplar meldet (das ist die eine Überquerung). `lending` merkt ihn sich in
seinem eigenen `book` und prüft dann gegen die eigene Kopie der Tatsache —
niemand von außen kann sie verfälschen. Die Frage für G3: Übernehmen wir
die Alternative, und was bedeutet das für die Szenarien?
