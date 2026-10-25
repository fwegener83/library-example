# Plan: Library-Tutorial — von Anforderungen zu laufender Software

*Arbeitsdokument zur Abstimmung (deutsch). Das Tutorial selbst wird englisch.*
*Stand: 2026-10-25 · Status: Teil A (Kapitel 0–5) abgeschlossen; als Nächstes Gate G1 (vom Modell zum Code), Teil B danach*

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
| **G0** | nach Kapitel 0 | Review des Anforderungsdokuments — alles Weitere baut darauf auf | erledigt |
| **G1 — Vom Modell zum Code** | nach Kapitel 5 (Challenging the cut), **vor jeder Arbeit pro Bounded Context** | Wie der Agent pro Kontext vom Modell in DDD Studio zum Code kommt: Reihenfolge, Einheit eines Inkrements, Szenarien als Tests, fehlende Skills (§6) | offen |
| **G2 — Technik** | vor dem Projekt-Skelett | Versionen, Event-Store-Ansatz, UI-Technik, Datenbank (§7) | offen |
| **G3 — F2** | bevor `lending` im Detail modelliert wird | Woher `lending` weiß, ob ein Exemplar „restricted" ist (§11) | **entschieden** 2026-10-25 (Maintainer): der Katalog meldet es, `lending` prüft gegen die eigene Kopie. Im Modell seit Kapitel 3 so angelegt, vor der Freigabe; siehe §11 |
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
2. **Das Modell treibt die Umsetzung.** Das Modell in DDD Studio ist die
   einzige fachliche Quelle. Der Agent liest es und baut daraus den Code;
   die Szenarien werden zu Tests — *wie genau*, klärt Gate G1.
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
| Stack | Java, Spring Boot, Spring Modulith — Prämisse des Tutorials. Offen für G2: Versionen, Event-Store, Datenbank, UI-Technik (§7) |
| Schnitt | vier Kontexte `catalogue`, `lending`, `membership`, `fees`; kein Kontext für Benachrichtigungen (Kap. 3, geprüft in Kap. 5) |
| Git-Tags | keine (2026-10-25). Die Kapitel-Branches und Merge-Commits zeigen die Stände (§12) |
| Sprache | Englisch (Tutorial, Code, Modell); dieses Planungsdokument deutsch |
| Ort | eigenes Repo `fwegener83/library-example` |
| Deployment | eine Deployment-Einheit, Module = Bounded Contexts |
| Teams | gedanklich getrennte Teams pro BC, sichtbar über Verträge |
| Vorgehen pro Kontext | allein aus dem Modell in DDD Studio (Maintainer, 2026-10-25). Einzelheiten: G1 (§6) |
| UI | **kleine, minimale UI** — macht das Ergebnis greifbar (Technik: G2) |
| Format | Markdown-Kapitel im Repo; später Übernahme auf die DDD-Studio-Homepage |
| F1 Process Manager | vorerst **ohne**; ggf. später eigener Abschnitt (G5) |
| F4 Evolution | erst die Basis; danach als Erweiterung (G5) |

---

## 4. Domänenzuschnitt

### 4.1 Ergebnis (Kapitel 3–5)

Quelle der Wahrheit sind die Context Map in DDD Studio und der Export in
`model/esdm/`; begründet in Kapitel 3, geändert in Kapitel 4 (ADR 5) und
Kapitel 5 (ADR 9, C-20 bis C-25).

| Kontext | Subdomain | Team (fiktiv) | Tiefe (Vorschlag, G2) |
|---|---|---|---|
| `catalogue` | collection, supporting | Collection | CRUD |
| `lending` | circulation, **core** | Circulation | event-sourced |
| `membership` | member-services, supporting | Members | CRUD |
| `fees` | fines-and-payments, supporting | Finance | event-sourced |

Externe Systeme: *National ISBN Service*, *CityPay*, *City Mail Gateway*.

Context Map (upstream → downstream):

- `catalogue` → `lending`, `catalogue` → `fees`: **Open Host Service +
  Published Language** (Titel und Exemplare mit Art, Heimatzweigstelle,
  Nutzungsgebühr-Markierung; Abgang und Freigabe eines Exemplars)
- `membership` → `lending`: **Customer/Supplier**
- `membership` → `fees`: **Customer/Supplier** — `fees` setzt und hebt die
  Sperre „unpaid fees“ (C-19, ADR 5)
- `lending` → `fees`: **Customer/Supplier** (ADR 9)
- ISBN-Dienst → `catalogue`, CityPay → `fees`: **ACL**
- Mail-Gateway: noch ohne Mapping (Schnittstelle unbekannt)
- Verworfen: Partnership (erster Schnitt), Shared Kernel, ein gemeinsamer
  Kontext für `fees` und `membership`, ein Kontext für Benachrichtigungen

### 4.2 Ursprüngliche Hypothese (überholt)

Vor Kapitel 0 stand hier eine Hypothese mit fünf Kontexten. Was sich
geändert hat und wo:

- Kein Kontext `notification`: keine eigene Sprache, kein Aggregat
  (Kapitel 3). Die Hinweise an Leser hängen an `lending`.
- *patron* wird nicht verwendet; die Person heißt *reader* in `lending`
  und `fees`, *member* in `membership` (C-07).
- Die Beziehung zwischen `fees` und `membership` ist umgedreht:
  `membership` ist Supplier (C-19, ADR 5).
- `lending` → `fees` ist Customer/Supplier statt Open Host Service (ADR 9).
- `catalogue` beliefert auch `fees` (Preis, Nutzungsgebühr-Markierung).
- Die externen Systeme heißen wie im Brief: CityPay statt „Payment
  Provider“, National ISBN Service statt „Book Metadata Service“.

---

## 5. Ablauf

### Teil A — abgeschlossen

| # | Kapitel | Werkzeug | Ergebnis im Repo |
|---|---|---|---|
| 0 | **The brief** — Anforderungsdokument der Stadtbibliothek: Interviewnotizen, absichtlich lückenhaft, mit Synonymen und Widersprüchen | Text | `requirements/brief.md` |
| | **→ Gate G0** | | |
| 1 | **Big Picture Event Storming** — Exploration, Zeitleiste, Schlüsselereignisse, Hotspots, Akteure, externe Systeme | Sketch Board | `model/sketch/big-picture.json` |
| 2 | **Domain Stories** — zwei Kernprozesse; Sprachkonflikte sichtbar machen | Domain Stories | `model/domain-stories/…` |
| 3 | **Strategic design** — Klärungen, Subdomains, Bounded Contexts, Glossare, Context Map mit Mustern, Teamzuordnung; verworfene Partnership-Hypothese | Context Map, Glossar | `model/esdm/`, `model/sketch/big-picture-contexts.json`, `requirements/clarifications.md` |
| 4 | **Deployment decision** — Modulith, Modul = BC, Integrationsregeln als ADRs | ADRs | `docs/adr/…` |
| 5 | **Challenging the cut** — Schnitt und Context Map von einem frischen Agenten prüfen lassen (Skill `challenge-context-cut`), Befunde als Klärungen C-20 bis C-25 und ADR 9, Board und Glossare nachziehen | Skill, DDD Studio | `docs/reviews/…`, `requirements/clarifications.md`, `docs/adr/0009-…` |

### → Gate G1 (Vom Modell zum Code) — harter Halt

Alles ab hier hängt davon ab, *in welcher Reihenfolge* pro Bounded Context
Feinmodellierung und Umsetzung ineinandergreifen. Die folgende Gliederung
ist deshalb **vorläufig** und wird nach G1 neu geschnitten und nummeriert
(ab Kapitel 6).

### Teil B — vorläufig, nach G1 (und G2) neu zu planen

| # | Kapitel (Arbeitstitel) | Werkzeug |
|---|---|---|
| B1 | Kontextübergreifende Flows | Flow View |
| B2 | Feinmodellierung je Kontext (Aggregates, Invarianten, Slices, GWT) | Static View, Slices, Scenarios |
| B3 | Umsetzung je Kontext in der Reihenfolge aus Kapitel 4 (`catalogue` und `membership`, dann `lending`, dann `fees`); Szenarien als Tests | Code, Spring Modulith, DDD-Studio-MCP |
| B4 | Minimale UI | Code |

Umsetzungstiefe im Code (Vorschlag): voll — `lending`, `fees` + ACL;
schlicht — `catalogue`, `membership` (CRUD); Hinweise an Leser als
schlichter Versand über das Mail-Gateway.

### Erweiterungen — nach G5

- **Process Manager** (F1): z. B. ein Mahnlauf über mehrere Kontexte,
  abgewogen gegen Policy-Choreographie.
- **Evolution** (F4): eine neue Anforderung (z. B. E-Books) verschiebt den
  Schnitt; Modell → Code ändern sich in dieser Reihenfolge.

---

## 6. Kernthema für G1: Vom Modell zum Code

*Nichts in diesem Abschnitt ist entschieden. Er sammelt die Frage, das
Material und die Vorbereitung für G1.*

### 6.1 Die Frage

Nach Kapitel 5 haben wir: Bounded Contexts, eine zweimal geprüfte Context
Map mit Beziehungen, Deployment-Entscheidungen als ADRs. Jetzt rückt erstmals **pro
Bounded Context** die Umsetzung in den Fokus. Das Modell in DDD Studio ist
dafür die einzige fachliche Quelle (Entscheidung des Maintainers, 2026-10-25).

> **Wie kommt der Agent pro Bounded Context vom Modell zum laufenden Code?**

Teilfragen:

- **Reihenfolge:** Erst ein Kontext vollständig fein modellieren und dann
  bauen, oder abwechselnd, Slice für Slice? Was kommt zuerst: die
  kontextübergreifenden Flows oder die Innensicht eines Kontexts?
- **Einheit:** Was ist ein Inkrement, das der Agent in einem Zug umsetzt —
  ein *Flow*, ein *Slice*, ein *Feature* mit GWT-Szenarien?
- **Kontextübergreifende Flows:** Wer modelliert einen Ablauf, der über
  mehrere Teams läuft, und wie hängen die Teile zusammen?
- **Modell lesen:** Liest der Agent das Modell über den MCP-Server oder über
  den ESDM-Export? Was gilt, wenn beides auseinanderläuft?
- **Szenarien → Tests:** von Hand mit Namenskonvention oder generiert? Wie
  wird geprüft, dass jedes Szenario einen Test hat?
- **Modell und Code im Gleichklang:** Wie fällt auf, wenn der Code vom
  Modell abweicht (Module == Kontexte, Ereignisse == Published Language)?
- **Wem gehört eine Regel?** DDD Studio hängt eine Policy an die Domain,
  nicht an einen Kontext, und nennt eine Regel mit laufender Summe einen
  Process Manager (`docs/tool-gaps.md`, 14 und 15). Wem eine Regel gehört
  (z. B. die €10-Regel, `fees`, C-19), muss bei der Feinmodellierung
  trotzdem sichtbar bleiben.
- **Skills:** Welche Arbeitsschritte wiederholen sich so, dass ein Skill
  lohnt? Kandidaten: Szenario → Test, Code gegen Modell prüfen, einen
  Kontext umsetzen.

### 6.2 Vorbereitung für G1 (erlaubt vor dem Gate)

1. **Entscheidungsvorlage** `docs/gates/g1-model-to-code.md` (nicht zu
   verwechseln mit `docs/decisions.md`, den Entscheidungsebenen): zwei bis
   drei Varianten, am konkreten Beispiel eines `lending`-Slices
   durchgespielt, Abwägung, Empfehlung, Skill-Kandidaten.
2. Dann: gemeinsame Runde, Entscheidung des Maintainers, Teil B neu planen.

---

## 7. Technik (Vorschlag — Entscheidung in G2)

- Java (aktuelles LTS), Spring Boot, Spring Modulith; Versionen in G2.
- Ein Modul pro BC als Top-Level-Package; öffentlich nur Modul-API und
  Integration Events; `ApplicationModules.verify()` im Test.
- Event Sourcing von Hand und lesbar: Aggregate als *Decider*
  (`decide`/`evolve`, sealed Interfaces + Records), schlanker
  JDBC-Event-Store in Postgres. Kein Axon (versteckt das Konzept).
- Policies als `@ApplicationModuleListener` im Downstream-Modul; Event
  Publication Registry = Outbox mit at-least-once. Achtung: DDD Studio
  hängt eine Policy an die Domain, nicht an einen Kontext, und nennt eine
  Regel mit laufender Summe einen Process Manager (`docs/tool-gaps.md`,
  14 und 15). Wem eine Regel gehört (z. B. die €10-Regel `fees`, C-19),
  muss bei der Feinmodellierung trotzdem sichtbar bleiben — siehe §6.1.
- System-Commands aus dem Tagesblatt per Scheduler.
- **Minimale UI** — Kandidaten für G2: serverseitig (Thymeleaf + htmx,
  bleibt im Spring-Monolithen, minimaler Aufwand) vs. kleine SPA.
  Vorschlag: serverseitig; Seiten etwa Katalogsuche, Leserkonto,
  Ausleihtheke, Tagesblatt.
- Tests: Decider-Unit-Tests aus Szenarien, Modulith-Scenario-Tests,
  Testcontainers, WireMock.

---

## 8. Repo-Struktur

```
library-example/
├── README.md
├── CLAUDE.md                    # Regeln für Claude Code (Session-übergreifend)
├── .claude/skills/              # Skills, z. B. close-chapter
├── requirements/
│   ├── brief.md                 # Kapitel 0
│   └── clarifications.md        # fachliche Klärungen C-nn
├── chapters/NN-*.md             # die Kapitel
├── model/
│   ├── esdm/                    # Context Map (export_esdm)
│   ├── domain-stories/          # export_domain_story
│   └── sketch/                  # Board-Snapshots (JSON)
├── scripts/check_repo.py        # maschinelle Prüfungen
├── docs/
│   ├── plan.md                  # dieses Dokument
│   ├── decisions.md             # wer was entscheidet (Ebenen)
│   ├── gates/                   # Entscheidungsvorlagen der Gates (ab G1)
│   ├── adr/                     # Architekturentscheidungen (MADR)
│   ├── reviews/                 # Berichte von challenge-context-cut
│   └── tool-gaps.md             # Lücken in DDD Studio
└── src/…                        # nach G2
```

Keine Git-Tags; die Kapitel-Branches zeigen die Stände (§12). Studio-Workspace
mit gleichnamigen Versionen; öffentlicher Read-only-Link pro Stand.

---

## 9. Meilensteine

| M | Inhalt | Gate davor |
|---|---|---|
| M1 | Kapitel 0: Anforderungsdokument | — |
| M2 | Kapitel 1–3 im Studio + Export + Texte | G0 |
| M3 | Kapitel 4: Deployment-ADRs | G0 |
| M3b | Kapitel 5: Schnitt prüfen (erledigt) | — |
| M4 | Vorbereitung G1: Entscheidungsvorlage Vom Modell zum Code | — (Vorbereitung) |
| — | **G1, G2** | |
| M5+ | Teil B, neu geplant | G1, G2 |
| — | **G4, G5** | |

---

## 10. Rückwirkungen auf DDD Studio (hinter G4)

- **In-App-Beispiel:** Vorschlag — ersten Schnitt durch den zweiten
  ersetzen (aus `0e0797ff^` wiederherstellen, an den heutigen
  Metamodell-Stand anpassen). Erweiterungen bleiben im Tutorial-Workspace;
  das In-App-Beispiel bleibt „der kurze Einstieg".
- **Werkzeuglücken sammeln, nicht nebenbei fixen** — erst in
  `docs/tool-gaps.md`, nach G4 als Issues im `ddd-studio`-Repo.
- **Homepage:** Beitrag + Link aufs Repo und die Read-only-Workspaces —
  später.

---

## 11. Register offener Punkte

| ID | Frage | Gate | Stand |
|---|---|---|---|
| G1-1 | Vom Modell zum Code: Reihenfolge, Einheit, Szenarien als Tests, Skills (§6) | G1 | offen |
| T1 | Java-, Spring-Boot-, Modulith-Versionen | G2 | offen |
| T2 | Event-Store-Ansatz (Vorschlag: von Hand, Decider) | G2 | offen |
| T3 | UI-Technik (Vorschlag: Thymeleaf + htmx) | G2 | offen |
| F1 | Process Manager | G5 | vorerst ohne |
| F2 | Woher kennt `lending` den Exemplartyp? (siehe unten) | G3 | **entschieden** 2026-10-25: aus den Ereignissen des Katalogs |
| F3 | UI | — | **entschieden:** minimale UI |
| F4 | Evolutionskapitel | G5 | nach der Basis |
| F5 | Format | — | **entschieden:** Markdown im Repo |
| E1 | In-App-Beispiel ersetzen | G4 | offen |

**F2 in einfachen Worten.** Nur Researcher dürfen ein *restricted*
Exemplar (*copy*) ausleihen. Ob eine Kopie restricted ist, entscheidet der
**Katalog** beim Registrieren. Die Regel wird aber in `lending` geprüft. Im
zweiten Schnitt schickte der **Aufrufer** die Art im Command mit — die UI
sagt „das ist restricted“, und `lending` glaubt es.

**Entscheidung (G3, 2026-10-25, Maintainer):** Der Katalog meldet die Art
mit, wenn er eine Kopie registriert (Published Language
`catalogue-lending`). `lending` merkt sie sich in seiner eigenen Sicht auf
die Kopie und prüft gegen diese Kopie der Tatsache; niemand von außen kann
sie verfälschen. Verworfen: die Art im Command des Aufrufers. So stand es
schon seit Kapitel 3 im Modell („lending the copies and their flag“), bevor
das Gate entschieden war; die Konsistenzprüfung nach Kapitel 5 hat das
gefunden, der Maintainer hat es nachträglich bestätigt. Folge für die
Szenarien: Ein Given „copy registered as restricted“ steht vor jedem
Szenario, das die Regel prüft; wie mit einer Ausleihe umzugehen ist, deren
Kopie `lending` noch nicht kennt, klärt die Feinmodellierung von `lending`.

---

## 12. Kapitelstand

Jedes Kapitel ist ein eigener Branch mit einem PR, gemergt als
**Merge-Commit** (kein Squash). Git-Tags setzen wir nicht (entschieden
2026-10-25): Die Branches und Merge-Commits zeigen die Stände der Kapitel.
Korrekturen nach dem Merge laufen über eigene PRs und stehen in der
Spalte „Danach“.

| Kapitel | Thema | Branch / PR | Merge-Commit (`main`) | Danach | Studio-Versionen |
|---|---|---|---|---|---|
| 00 | The brief | `chapter-00-brief` (#1) | `a0eb886` (Squash, vor der Regel) | — | — |
| 01 | Big Picture Event Storming | `chapter-01-big-picture` (#2) | `8ac11b4` | Korrekturen #4 | `ch1-big-picture-v2` |
| 02 | Domain Stories | `chapter-02-domain-stories` (#3) | `d40021b` | — | `ch2-reserve-borrow-return-v2`, `ch2-overdue-fine-blocked-card-v2` |
| 03 | Strategic design | `chapter-03-strategic-design` (#6) | `6547c0c` | — | `ch3-before-clarifications`, `ch3-context-cut-v3`, `ch3-context-map-v3` |
| 04 | Deployment decision | `chapter-04-deployment` (#8) | `9e404d9` | ADRs angenommen #9; MADR-Format #12 (`e065915`); Vorgehen allein aus dem Modell #15 | `ch4-context-map-circle-noted`, `ch4-context-map-holds` |
| 05 | Challenging the cut | `chapter-05-challenging-the-cut` (#11) | `71b79cd` | Konsistenzprüfung `consistency-after-ch05`; Vorgehen allein aus dem Modell #15 | `ch5-big-picture-after-challenge(-v2 … -v5)`, `ch5-context-map-after-challenge(-v2 … -v4)` |

## 13. Regeln für die Arbeit mit Claude Code

Die Arbeitsregeln stehen in `CLAUDE.md` (immer geladen) und im Skill
`.claude/skills/close-chapter/` (Ablauf zum Abschluss eines Kapitels,
Prüfliste für Domain Stories und Big Picture). Wer die Regeln ändern will,
ändert diese Dateien, nicht nur dieses Gespräch.

## 14. Selbstverbesserndes Vorgehen

Ziel: Du musst nicht daran denken, ob die Regeln greifen. Dafür gibt es
drei Mechanismen, alle im Repo:

1. **Skript** `scripts/check_repo.py` prüft, was sich maschinell prüfen
   lässt: Links, README und Kapitelstand, Snapshot-Header und
   `eventOrder`, verwaiste Karten, fehlende `src:`-, `hotspot:`- und
   `rule:`-Tags, Zahlen in Work-Object-Namen. Fehler brechen den
   Kapitelabschluss ab, Warnungen kommen in die Rules-Audit.
2. **Rules-Audit** in jedem Kapitel-PR: welche Prüfungen liefen, was kam
   heraus, was wurde behoben, was bleibt offen. Ein PR ohne Audit ist nicht
   „ready".
3. **Retrospektive** am Kapitelende: Jeder Fund (von mir, vom Review, von
   dir) führt zu einer Frage — welche Regel oder welche Prüfung hätte ihn
   früher gefunden? Sie kommt im selben PR in `CLAUDE.md`, `checks.md`
   oder ins Skript. Regeln, die nicht geholfen haben, fliegen raus.

Grenze: Ob ein Satz gut klingt oder ein Schnitt fachlich stimmt, prüft kein
Skript. Dafür bleiben die Prüfliste und der unabhängige Review. Ob die
Regeln wirken, zeigt sich an jeder Rules-Audit: Fehlt sie oder ist sie
oberflächlich, ist das ein Fehler von mir. Regeln, die nur bremsen, ohne
Fehler zu finden, werden gestrichen.

---

## 15. Entscheidungsebenen (Human in the Loop)

Das Tutorial zeigt auch, wo ein Agent aufhören und einen Menschen fragen
muss. Beschrieben in `docs/decisions.md`; in Kürze:

| Ebene | Entscheidet (im echten Projekt) | Festgehalten in |
|---|---|---|
| Fachlich | Fachbereich | `requirements/clarifications.md` (`C-nn`) |
| Strategie und Architektur | Architekt/Team | Context Map in Studio, `docs/adr/` |
| Vorgehen | Projektleitung | Gates in diesem Plan |

- Der Agent bereitet vor (Quelle, Optionen, Empfehlung, Folgen), stoppt,
  hält nach der Antwort fest, **wer wann entschieden hat und was verworfen
  wurde**, und zieht alles nach, was davon abhängt.
- Stopp-Kriterien: eine fachliche Regel steht nicht in der Quelle; ein
  Gate; schwer umkehrbar *und* es gibt echte Alternativen; macht eine
  frühere Entscheidung rückgängig (dann offen sagen, nicht selbst ändern).
- Alles andere entscheidet der Agent selbst, wenn es eine vernünftige
  Lösung gibt, und meldet es im PR („vom Agenten entschieden“). Dazu
  gehören Korrekturen, die ein Dokument mit dem entschiedenen Stand in
  Einklang bringen, auch im Wortlaut einer Klärung oder eines ADR, solange
  sich die Entscheidung nicht ändert. Der Maintainer will ein schlüssiges
  Tutorial, nicht jede Kleinigkeit steuern (2026-10-25).
- Ein Review prüft geleistete Arbeit, eine Entscheidung wählt zwischen
  Optionen. Nicht jede Kleinigkeit ist eine Entscheidung, sonst nickt der
  Mensch nur noch ab.
- Jedes Kapitel (ab 1) endet mit dem Kasten „Decisions in this chapter“;
  `scripts/check_repo.py` prüft, dass er da ist.
