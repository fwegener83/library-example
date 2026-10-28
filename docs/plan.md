# Plan: Library-Tutorial — von Anforderungen zu laufender Software

*Arbeitsdokument zur Abstimmung (deutsch). Das Tutorial selbst wird englisch.*
*Stand: 2026-10-28 · Status: Teil A (Kapitel 0–5) abgeschlossen; Gate G1 entschieden (Phasenmodell, `docs/gates/g1-model-to-code.md`), am 2026-10-28 für Phase 5 geändert (§5, „Phase 5 im Detail“); ADR 10 (REST an den Außenkanten) am 2026-10-28 wieder geöffnet, entschieden wird in Phase 6 (G2); unabhängige Prüfung des Schnitts liegt vor (`docs/reviews/pre-g6-context-cut.md`); C-27 bis C-32 vom Agenten im Auftrag entschieden, ADR 11 (Event-Umschlag) angenommen (2026-10-26); Kapitel 6 (Liefer-Scope) angenommen, Gate G6 entschieden (Option 3); als Nächstes Kapitel 7 (den Scope modellieren)*

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
| **G1 — Vom Modell zum Code** | nach Kapitel 5 (Challenging the cut), **vor jeder Arbeit pro Bounded Context** | Das Phasenmodell 0–7 mit Skills, Rücksprüngen und starken Defaults (§6) | **entschieden** 2026-10-25 (Maintainer, im Gespräch: alle Empfehlungen angenommen); schriftliche Fassung `docs/gates/g1-model-to-code.md`; **geändert** 2026-10-28 (Maintainer): Phase 5 ohne Verträge und REST, Skills im Rückblick mit Probelauf |
| **G6 — Liefer-Scope** | nach G1, **vor der Feinmodellierung** (Phase 4, Kapitel 6) | Welche Szenarien jetzt fein modelliert und gebaut werden; fachliche Entscheidung | **entschieden** 2026-10-26 (Maintainer): Option 3 aus Kapitel 6 |
| **G2 — Technik** | nach der Feinmodellierung (Phase 6), vor dem Projekt-Skelett | Versionen, Event-Store-Ansatz, wie Frontends die Module erreichen (REST ja/nein, ADR 10 als Vorlage), Frontend-Technik, API-Spezifikation, Weiterentwicklung der Events, Zustellung (spät, doppelt), Datenbank, Tiefe pro Kontext, Deployment-Einheiten (Default: eine) (§7) | offen |
| **G3 — F2** | bevor `lending` im Detail modelliert wird | Woher `lending` weiß, ob ein Exemplar „restricted" ist (§11) | **entschieden** 2026-10-25 (Maintainer): der Katalog meldet es, `lending` prüft gegen die eigene Kopie. Im Modell seit Kapitel 3 so angelegt, vor der Freigabe; siehe §11 |
| **G4 — In-App-Beispiel** | bevor irgendetwas in `ddd-studio` geändert wird | Ersetzen des Library-Beispiels (§10) | offen |
| **G5 — Erweiterungen** | nach fertiger Basis | Process-Manager-Kapitel (F1), Evolutionskapitel (F4) | offen |

Die Gates sind nicht nach Zeit nummeriert: G6 kommt vor G2, G3 war vor G1
entschieden.

Daneben gibt es **weiche Reviews**: Jedes Kapitel kommt als eigener
Pull Request. Du reviewst, ich arbeite Änderungen ein; innerhalb von
Teil A darf ich parallel am nächsten Kapitel weiterarbeiten, sobald G0
durch ist.

**Rücksprünge sind Halte** (G1, §4 der Vorlage): Trägt eine Grenze in
Phase 5 oder 7 nicht, halte ich an und lege den Befund vor; zurück nach
Phase 2 geht es erst nach deiner Entscheidung. Eine Lücke im Modell, die
beim Bauen auffällt, schließe ich in Studio (kleine Schleife) und melde
sie im PR; eine fachliche Frage darin geht vorher als `C-nn` an dich.

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
   einzige fachliche Quelle. Es wird vor dem Code für den Liefer-Scope
   fertig modelliert und testet dabei den Schnitt; der Agent baut daraus
   den Code, die Szenarien werden zu Tests (G1).
3. **Grenzen sind anfangs Hypothesen.** Deshalb ein modularer Monolith mit
   *geprüften* Modulgrenzen; herausgelöst wird erst, wenn der Schnitt
   getragen hat.

**Und das Tutorial ist der erste Durchlauf eines wiederverwendbaren
Workflows** (G1): Wer ein paar Dokumente mit Anforderungen hat, soll
später mit denselben Skills durch dieselben Phasen kommen.

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
| Vorgehen insgesamt | Phasenmodell 0–7 mit Skills, kleinem und großem Rücksprung (G1, Maintainer, 2026-10-25) |
| Scope | breit erschließen, eng bauen: Problem-Scope in Phase 0, Liefer-Scope nach dem Schnitt (G6) (Maintainer, 2026-10-25) |
| Modulith zuerst | starker Default: eine Einheit, bis der Schnitt getragen hat; Herauslösen später mit eigenem Skill (Maintainer, 2026-10-25) |
| Schnittstellen | zwischen Modulen Events und Aufträge (ADR 4). Wie Frontends die Module erreichen, entscheidet Phase 6 (G2); ADR 10 (REST) ist dafür die Vorlage. Am 2026-10-25 angenommen, am 2026-10-28 vom Maintainer wieder geöffnet: REST ist Technik und kein Vorgriff in Phase 3 oder 5 |
| Skills | im Repo unter `.claude/skills/`, generisch formuliert; ab Phase 5 **im Rückblick** geschrieben (aus dem Arbeitsprotokoll des Kapitels, nach dem Review des Maintainers) und mit einem **Probelauf** eines frischen Agenten getestet (Maintainer, 2026-10-28); Phasen 0–3 später herausgelöst und per frischem Durchlauf getestet (2026-10-25) |
| UI | **kleine, minimale UI** — macht das Ergebnis greifbar (Technik und Anbindung: G2) |
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

### Phasenmodell (G1)

Teil A war, ohne dass wir es so genannt haben, der Durchlauf der Phasen 0
bis 3. Ab hier folgt das Tutorial dem Phasenmodell aus G1
(`docs/gates/g1-model-to-code.md`); jede Phase bekommt ihren Skill beim
ersten echten Einsatz.

| Phase | Ziel | Skills | Im Tutorial |
|---|---|---|---|
| 0 Wissen sammeln | Quellen einordnen, Wissensdokument, Problem-Scope | `gather-knowledge` | Kap. 0 (dünn: der Brief ist schon ein Dokument) |
| 1 Domäne erschließen | genug verstehen, um zu schneiden | `prepare-event-storming`, `digitize-board`, `draw-domain-story`, `discovery-readiness` | Kap. 1, 2 |
| 2 Schneiden | Kontexte, Context Map, Glossare | `derive-contexts`, `challenge-context-cut` | Kap. 3, 5 |
| 3 Modulith-Regeln | eine Einheit, Integrationsregeln (ohne Technik der Frontends) | `set-modulith-rules` | Kap. 4 |
| 4 Liefer-Scope | was jetzt modelliert und gebaut wird | `plan-scope` | Kap. 6 → G6 |
| 5 Feinmodellieren = Schnitt testen | sauberes Modell in Studio für den Scope (ESDM, nicht draft), Flows wo sie tragen | `model-scope`, `challenge-context-cut` (Modus 2), `example-mapping` | Kap. 7–9 |
| 6 Technik | Technik, Anbindung der Frontends (REST?), API-Spezifikation, Event-Evolution, Tiefe, Deployment-Einheiten | `decide-technology` | Kap. 10 → G2 |
| 7 Bauen | Plan und Code aus dem Modell | `plan-implementation`, `implement-slice`, `check-model-code` | danach |
| später | Modul herauslösen | `extract-module` | offen |

Darüber `ddd-workflow` als Einstieg (welche Phase, welcher Halt, welcher
Skill als Nächstes). Rücksprünge: klein 7 → 5 (Lücke im Modell), groß
5/7 → 2 (Schnitt trägt nicht, Halt).

**Änderung vom 2026-10-28 (Maintainer).** Phase 5 enthält keinen eigenen
Schritt mehr für Verträge an den Kanten und nichts zu REST oder OpenAPI.
Die Skills `model-flows`, `design-context-contracts` und `model-context`
entfallen; an ihre Stelle tritt `model-scope`, der den ganzen Scope über
alle berührten Kontexte modelliert. Events, die eine Grenze überqueren,
werden darin ganz normal mit Payload modelliert: Sie sind Fachlichkeit,
und ohne sie ist das Modell nicht vollständig. Was Technik ist, geht nach
Phase 6: wie Frontends die Module erreichen (ADR 10 wieder geöffnet), eine
API-Spezifikation, wie Events weiterentwickelt werden (von ADR 4
angekündigt) und wie die Module mit späten oder doppelten Events umgehen.
Ab Phase 5 entsteht jeder Skill im Rückblick und wird mit einem Probelauf
getestet (Abschnitt „Wie ein Skill entsteht“).

### Teil B — nach G1

| # | Kapitel (Arbeitstitel) | Phase | Neuer Skill | Werkzeug | Halt |
|---|---|---|---|---|---|
| — | **ADR 10: REST at the edges**: Nachtrag zu Kapitel 4, eigener PR; am 2026-10-25 angenommen, **am 2026-10-28 wieder geöffnet** (Entscheidung in G2). Im selben PR die Korrekturen an ADR 2–8 | 3 | — | ADR | erledigt (#17); wieder offen bis G2 |
| — | **Unabhängige Prüfung des Schnitts** vor G6: `challenge-context-cut` in frischem Agenten; Bericht nach `docs/reviews/` | 4 | `challenge-context-cut` | Skill | erledigt (#18) |
| 6 | **Choosing the first increment**: 18 Kandidaten, vier Optionen, Skill `plan-scope` | 4 | `plan-scope` | Repo, DDD Studio lesend | **G6 entschieden** 2026-10-26: Option 3 |
| — | **Plan für Phase 5** (dieser PR): Phase 5 ohne Verträge und REST, ADR 10 wieder offen, Skills im Rückblick, Detailplan | 5 | — | Plan | Freigabe durch dich |
| 7 | **Modelling the scope**: alle Szenarien von Option 3 als Flows, wo sie tragen, sonst direkt im Static View; Rückwärtsprüfung jedes Flows; Modell sauber (validiert, nichts draft, Export). Danach der **Rückblick** (was gut, was schlecht lief; Bedarf an DDD Studio) und, nach deinem Review, der Skill `model-scope` mit Probelauf | 5 | `model-scope` | Flows, Static View | Review; Rücksprung nach 2 möglich (Halt) |
| 8 | **Challenging the cut in the model**: `challenge-context-cut` Modus 2 in frischem Agenten gegen das Modell aus Kapitel 7 (Abbruchkriterien aus G1); danach Modus 2 im Skill aus dem Rückblick | 5 | `challenge-context-cut` (Modus 2) | Skill, DDD Studio lesend | du entscheidest über die Funde; Rücksprung nach 2 möglich |
| 9 | **Example Mapping**: je Regel des Modells Beispiele und Fragen auf einem Sketch Board, Beispiele als GWT-Features in Studio, Fragen als `C-nn`; Modell bleibt sauber. Danach Skill `example-mapping` mit Probelauf. **Ende von Phase 5:** du nimmst das Modell für den Scope ab | 5 | `example-mapping` | Sketch Board, Features | Abnahme Phase 5 |
| 10 | **Choosing the technology**: Versionen, Event Store, DB, Anbindung der Frontends (REST? ADR 10 als Vorlage), Frontend-Technik, API-Spezifikation, Event-Evolution und Zustellung, Tiefe pro Kontext, Deployment-Einheiten (Default: eine) | 6 | `decide-technology` | ADRs | **G2** |
| 11 ff. | **Building**: Implementierungsplan, Skelett, dann `catalogue` und `membership`, `lending`, `fees`, minimale UI | 7 | `plan-implementation`, `implement-slice`, `check-model-code` | Code, Spring Modulith, DDD-Studio-MCP | Review je Kontext; Rücksprünge |
| — | **Skills der Phasen 0–3 herauslösen** und mit frischem Durchlauf testen (neuer Wegwerf-Workspace, nur der Brief); `ddd-workflow`, `close-step` | 0–3 | `gather-knowledge` … `set-modulith-rules` | Skills | Review |

Umsetzungstiefe im Code (Vorschlag, entschieden in G2): voll — `lending`,
`fees` + ACL; schlicht — `catalogue`, `membership` (CRUD); Hinweise an
Leser als schlichter Versand über das Mail-Gateway.

### Wie ein Skill entsteht (ab Phase 5)

Entschieden vom Maintainer am 2026-10-28.

1. **Das Kapitel läuft ohne Skill**, mit einer kurzen Arbeitscheckliste in
   diesem Plan und einem **Arbeitsprotokoll**: was gemacht wurde, was
   nicht ging, welche Umwege es gab, welche Entscheidung warum fiel.
2. **Rückblick** am Kapitelende (`docs/reviews/chNN-…-retrospective.md`):
   was gut lief, was schlecht lief, was an DDD Studio fehlt
   (`docs/tool-gaps.md`).
3. **Dein Review** des Kapitels und des Rückblicks.
4. **Skill aus dem Protokoll**, generisch formuliert (keine
   Millbrook-Details), mit deinen Korrekturen.
5. **Probelauf:** ein frischer Agent bekommt nur den Skill und eine kleine
   Eingabe und arbeitet in einem neuen Wegwerf-Workspace (nie im
   Tutorial-Workspace, nie im alten „Library Tutorial“). Sein Ergebnis wird
   mit dem Kapitel verglichen; wo er abweicht oder hängen bleibt, wird der
   Skill angepasst. Der Befund steht im PR.

Schritte 4 und 5 laufen im selben PR wie das Kapitel, nach deinem Review.

### Phase 5 im Detail

**Eingabe:** der entschiedene Scope (G6, Option 3: A, B, C, D, E1, E2, E3,
G1, J1; Kapitel 6), das Klärungsprotokoll, ADR 2–9 und 11, die Context Map
mit Glossaren in Studio, die Domain Stories und das Big Picture.

**Ergebnis am Ende von Phase 5:** ein Modell in Studio, das jedes
Szenario des Scopes abdeckt; `validate_model` ohne Befund, kein Knoten im
Status draft, Export nach `model/esdm/`, GWT-Features für die Regeln; der
Schnitt ist gegen dieses Modell geprüft. Kein REST, keine OpenAPI, keine
Entscheidung zu Zustellung oder Versionierung.

#### Kapitel 7 — den Scope modellieren

**Arbeitsweise: Flow zuerst, wo er trägt; nie verbiegen.**

- *Was die MCP-Werkzeuge können:* Eine Slice gruppiert nur Knoten, die
  schon im Static View stehen; sie erzeugt keine (`explain_model`,
  flows-and-slices). In der Web-App entsteht der Static View laut dir beim Zeichnen
  des Flows mit, über MCP nicht. „Flow zuerst“ heißt für den Agenten
  deshalb: erst die Geschichte als Folge von Schritten aufschreiben (sehen
  → entscheiden → Command → Event oder Ablehnung → neue Sicht, dazwischen
  Automatik), dann Schritt für Schritt die Knoten anlegen, die der Schritt
  braucht, und sofort die Slice dazu. Das Protokoll hält fest, wo das von
  der Arbeit in der App abweicht. Das ist ein Kandidat für den Rückblick.
- *Was ein Flow nicht zeigen kann* (laut Studio): den Zustand, die Timer
  und das Ende eines Process Managers, Invarianten, Domain Services, die
  übrigen Ergebnisse eines Commands, mehrere Read Models auf einer Seite,
  Verzweigungen. Das wird direkt im Static View modelliert. Der Agent
  „denkt“ den Flow dabei mit, damit die Struktur dieselbe ist. Ein Process
  Manager steht im Flow nur als Auslöser der Slice, deren Command er
  auslöst; Zustand, Timer und Ende kommen danach im Static View dazu.
- *Nie verbiegen:* Ein Element bekommt die Art, die es fachlich ist
  (`explain_concept` vor jeder Art, deren Form offen ist), nicht die, die in
  eine Slice passt. Kein erfundenes Command oder Event als Brücke zwischen
  zwei Slices. Eine Alternative ist ein eigener Flow, eine Ablehnung ein
  Schritt mit Verweis auf eine Invariante.

**Schritte**

1. **Vorbereitung.** `explain_model` (Übersicht, static-view,
   flows-and-slices, features-and-scenarios, fields-and-validation);
   `explain_concept` für aggregate, policy, process-manager, read-model,
   event-handler, domain-service. Arbeitsprotokoll anlegen.
2. **Storylines schreiben**, vor jedem Knoten. Je Flow eine Liste der
   Schritte mit Quelle (Brief §, Satz der Story, `C-nn`), Kontext und Art
   des Schritts. Vorschlag für die Flows (endgültig in Schritt 2):
   - *A* Titel und Exemplar registrieren; Exemplar korrigieren (C-27).
     `catalogue`, Event an `lending` und den Ersatzpreis an `fees`.
   - *B* Mitglied registrieren, Karte ausstellen, Researcher-Status
     gewähren, Karte verlängern; Enddaten als Datum (C-28). `membership`,
     Events an `lending`.
   - *C* Ausleihen und rechtzeitig zurückgeben; Rückgabe mit Schaden
     (C-06); Ablehnungen als eigene kurze Flows: restricted ohne
     Researcher-Status (C-29), gesperrte Karte, abgelaufene Karte.
   - *D* Vormerken, abholen; stornieren; Vormerkung läuft ab (C-10,
     C-12); Ablehnung bei fünf Vormerkungen und beim Überziehungslimit der
     Zweigstelle (C-14).
   - *E1–E3* die Story aus Kapitel 2 über drei Kontexte: verspätete
     Rückgabe → Mahngebühr → laufende Summe am Morgen → über €10 Sperre
     (ADR 5) → Zahlung an der Theke → Entsperrung (C-03, C-18, C-19,
     C-22).
   - *G1* Exemplar als verloren gemeldet, Verlustgebühr ohne Mahngebühr
     obendrauf (C-04), Abgang durch die Leitung des Bestands (C-20).
   - *J1* die zwei Morgenlisten pro Zweigstelle, zusammengesetzt aus drei
     Kontexten (ADR 8, C-31): Read-Model-Slices nacheinander.
3. **Flow für Flow modellieren**, in der Reihenfolge C, D, E1–E3, G1, A, B,
   J1: zuerst `lending` (Kerndomäne, höchstes Risiko, G1), dann was es
   speist und was es auslöst. Je Schritt: Knoten anlegen oder
   wiederverwenden (Aggregat, Command, Event, Akteur, Read Model, Query,
   Policy, Process Manager), Referenzen setzen (publishes, actors,
   projections, handles/emits), dann die Slice mit `exampleData`.
   `draftReasons` jeder Antwort sofort lesen und beheben.
   Bekannte Stellen, an denen der Flow nicht reicht und der Static View
   übernimmt, jeweils mit `explain_concept` und Abwägung im Protokoll:
   - *Überfällig werden* einer Ausleihe und *Ablauf* einer Vormerkung: ein
     Process Manager mit Timer pro Ausleihe oder Vormerkung, oder ein
     täglicher Lauf eines System-Akteurs (Tagesblatt, ADR 6)?
   - *Die €10-Regel* (Tool-Gap 15): Entscheidung im Aggregat von `fees`,
     das ein Event veröffentlicht, das eine zustandslose Policy in „Sperre
     setzen“ in `membership` übersetzt (ADR 5); oder ein Process Manager
     mit laufender Summe. Wem die Regel gehört, steht in der Beschreibung
     der Policy (Tool-Gap 14).
   - *Invarianten* (fünf Vormerkungen, Überziehungslimit, restricted nur
     für Researcher, Karte gültig) am Aggregat; eine Ablehnung im Flow
     verweist nur darauf.
   - *Policies über Kontextgrenzen:* Zustellung „at-least-once“ mit
     Idempotenz beim Empfänger, weil ADR 4 späte und doppelte Kopien schon
     annimmt; der Mechanismus (`strategy`) bleibt offen für Phase 6.
   Fachliche Lücken: die geparkten C-11, C-12, C-14 und die Folgefrage aus
   G3 (eine Ausleihe für ein Exemplar, das `lending` noch nicht kennt)
   entscheidet der Agent im Auftrag, wo ein sinnvolles Verhalten existiert
   (`C-nn`, „decided by the agent (delegated)“), sonst fragt er.
4. **Rückwärtsprüfung jedes Flows** (aus dem Event Modeling: die
   Geschichte rückwärts lesen, ob jede Information erklärt ist). Von der
   letzten Slice zur ersten:
   - jedes Feld eines Read Models stammt aus einem Event, auf das es
     projiziert (oder die Regel der Projektion sagt, wie es berechnet wird);
   - jedes Feld eines Events stammt aus dem Command, dem Zustand des
     Aggregats oder einer benannten Quelle (Uhr, Kennung vom Owner,
     ADR 7, ADR 11);
   - jedes Feld eines Commands stammt aus dem, was der Akteur vorher
     gesehen hat (ein Read Model früher im Flow), aus dem auslösenden
     Event (Policy, Process Manager) oder ist eine benannte Eingabe des
     Akteurs (etwa die gescannte Kartennummer);
   - die `exampleData` bleiben über den Flow gleich (dieselbe
     Ausleihnummer, Beträge nachrechenbar: €0.50 × Tage, gedeckelt);
   - kein Feld ohne Quelle im Brief oder in einer Klärung.
   Funde werden im Modell behoben und im Protokoll gezählt. Der statische
   Teil der Prüfung wird ein Skript `scripts/check_model.py` auf dem
   Export (Felder von Read Models gegen projizierte Events, Events gegen
   Command und Zustand, Commands einer Policy gegen das behandelte Event).
   Die `exampleData` stehen nicht im Export (Tool-Gap 16); die prüft der
   Agent über MCP.
5. **Abbruchkriterien beobachten** (G1 §3, Phase 5): eine Invariante
   braucht Daten aus zwei Kontexten zugleich, eine Policy ohne klaren
   Owner, ein Flow pendelt zwischen zwei Kontexten, ein Aggregat braucht
   fremden Zustand, ein Begriff hat zwei Bedeutungen in einem Kontext.
   Trifft eins zu: **Halt**, Befund vorbereiten, nicht selbst nach Phase 2.
6. **Modell sauber machen:** `validate_model` ohne Befund, kein Knoten
   draft; `export_esdm` nach `model/esdm/`; `esdm lint` auf den Export, wenn
   das Werkzeug verfügbar ist (offen, siehe unten);
   `scripts/check_model.py`; `save_version` `ch07-model-scope`.
7. **Kapiteltext** `chapters/07-modelling-the-scope.md`, geschrieben mit
   Flows und Export offen, jeder Satz gegen den Brief geprüft; dann
   `close-chapter` mit unabhängigem Review.
8. **Rückblick** `docs/reviews/ch07-modelling-retrospective.md`: was im
   Flow gut ging, was nur im Static View ging, wo Studio oder MCP gebremst
   haben, wo der Agent unsicher war; daraus eine priorisierte Liste von
   Änderungswünschen an DDD Studio (neue Zeilen in `docs/tool-gaps.md`,
   Umsetzung erst nach G4). **Halt: dein Review.**
9. **Skill `model-scope`** aus dem Protokoll und deinem Review, dann der
   Probelauf (siehe oben; Eingabe für den frischen Agenten: ein
   Scope-Dokument mit einem einzigen Szenario, etwa D). Der Skill
   verlangt einen entschiedenen Scope als Eingabe; fehlt er, bricht er ab
   und verweist auf `plan-scope` oder fordert ein Dokument mit den
   Szenarien und der Entscheidung an. Die Rückwärtsprüfung ist Teil des
   Skills.

**Was Kapitel 7 nicht macht:** keine GWT-Features (Kapitel 9; ein Feature
ohne Szenarien hielte das Modell im Status draft), keine REST-Endpunkte,
keine OpenAPI, keine Verträge als eigenes Artefakt, keine Entscheidung zu
Zustellung, Reihenfolge oder Versionierung über die Annahmen von ADR 4 und
ADR 11 hinaus.

#### Kapitel 8 — den Schnitt im Modell prüfen

`challenge-context-cut` in einem frischen Agenten gegen das Modell aus
Kapitel 7, mit den Abbruchkriterien aus G1 als Auftrag (Modus 2 ist im
Skill angekündigt, aber noch nicht geschrieben; der erste Lauf bekommt den
Auftrag als Text, der Skill folgt im Rückblick). Bericht nach
`docs/reviews/`; du entscheidest über die Funde. Danach Modus 2 im Skill,
mit einem Probelauf: dieselbe Prüfung gegen eine Kopie des Modells mit
einem absichtlich eingebauten Fehler (etwa eine Invariante, die Daten aus
zwei Kontexten braucht). Findet der Agent ihn?

*Warum vor Example Mapping:* Die Abbruchkriterien betreffen die Struktur
(wer welche Daten hat, wem eine Regel gehört). Trägt eine Grenze nicht,
wäre das Example Mapping auf der falschen Struktur verschwendet. Ändert
Example Mapping die Struktur deutlich, läuft die Prüfung am Ende von
Phase 5 noch einmal kurz.

#### Kapitel 9 — Example Mapping

Je Regel des Modells (Invariante, Constraint, Regel einer Policy oder
eines Process Managers) ein Example Mapping auf einem Sketch Board: Karte
für die Geschichte (das Szenario des Scopes), Karten für die Regeln,
Beispiele je Regel, Fragen. Die Beispiele werden GWT-Szenarien in Studio
(Features am Aggregat oder Read Model, Ablehnungen mit `invariantId`),
die Fragen `C-nn`. Lücken, die sich zeigen, schließt die kleine Schleife
im Modell. Am Ende ist das Modell wieder sauber, jetzt mit Features.
Danach Skill `example-mapping` mit Probelauf.

*Kritische Anmerkung zur Reihenfolge:* Üblich ist Example Mapping
**vor** dem Feinmodell, um Regeln zu finden. Hier sind die Regeln schon
weitgehend geklärt (Brief, C-01 bis C-32), also dient Example Mapping
dazu, jede Regel mit Beispielen zu schärfen und Testfälle zu gewinnen
(Specification by Example). Der Skill sagt das: Bei dünner Regelbasis
kommt Example Mapping vor `model-scope`.

**Ende von Phase 5:** du nimmst das Modell für den Scope ab; danach
Kapitel 10 (Technik, G2).

**Offen für dich (blockiert nichts vor Schritt 6):** Wo liegt `esdm lint`?
Studio nennt es, ein Paket dafür habe ich weder in npm noch in PyPI
gefunden. Ohne das Werkzeug heißt „sauber gelintet“ in Kapitel 7:
`validate_model` ohne Befund, nichts draft, `scripts/check_model.py` grün.

### Erweiterungen — nach G5

- **Process Manager** (F1): z. B. ein Mahnlauf über mehrere Kontexte,
  abgewogen gegen Policy-Choreographie.
- **Evolution** (F4): eine neue Anforderung (z. B. E-Books) verschiebt den
  Schnitt; Modell → Code ändern sich in dieser Reihenfolge.
- **Herauslösen eines Moduls** (`extract-module`), wenn der Schnitt
  getragen hat.

---

## 6. Gate G1: Vom Modell zum Code — entschieden

*Entschieden vom Maintainer im Gespräch vom 2026-10-25 (alle Empfehlungen
angenommen). Schriftliche Fassung mit Begründung und verworfenen
Alternativen: `docs/gates/g1-model-to-code.md`.*

Die Frage war: Wie kommt der Agent pro Bounded Context vom Modell zum
laufenden Code? Sie ist im Gespräch größer geworden: Das Tutorial soll der
erste Durchlauf eines Workflows sein, der von ein paar Dokumenten mit
Anforderungen zu laufender Software führt. Die Antwort in Kürze:

1. **Acht Phasen** (0–7, §5), jede mit Ziel, Skills und einem Ende, das
   ein Mensch abnimmt; `ddd-workflow` als Einstieg.
2. **Breit erschließen, eng bauen.** Problem-Scope in Phase 0, Liefer-Scope
   nach dem Schnitt (G6).
3. **Das Modell testet den Schnitt.** Die Innensicht aller Kontexte im
   Scope entsteht in Phase 5 in Studio, vor jedem Code. Abbruchkriterien
   (Invariante über zwei Kontexte, Policy ohne Owner, Pendel-Flow,
   Aggregat braucht fremden Zustand, Begriff mit zwei Bedeutungen) führen
   zurück nach Phase 2.
4. **Phase 7 baut nur.** Lücken im Modell schließt die kleine Schleife in
   Studio; ein falscher Schnitt ist ein Halt.
5. **Modulith zuerst**, stark: „Verhandeln wie getrennte Teams, ändern wie
   ein Repo.“ Deployment-Einheiten werden erst in Phase 6 gefragt, mit dem
   Default „eine“.
6. ~~**REST an den Außenkanten, API first**~~ (am 2026-10-28 wieder
   geöffnet, Entscheidung in Phase 6); zwischen den Modulen Events und
   Aufträge (ADR 4).
7. **Skills im Repo**, generisch; ab Phase 5 im Rückblick mit Probelauf
   (2026-10-28); die Phasen 0–3 werden später herausgelöst und mit einem
   frischen Durchlauf getestet.

**Änderung vom 2026-10-28** (Maintainer): Phase 5 ohne eigenen
Vertragsschritt und ohne REST/OpenAPI, `model-scope` statt `model-flows`,
`design-context-contracts` und `model-context`; ADR 10 wieder offen. Im
G1-Dokument als Nachtrag festgehalten.

Offen und mit festem Zeitpunkt: die genaue Einheit eines Inkrements und
die Namenskonvention Szenario → Test (`plan-implementation`,
`check-model-code`, erstes Bau-Kapitel).

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
  steht bis dahin in der Beschreibung der Policy (G1, §8 der Vorlage).
- System-Commands aus dem Tagesblatt per Scheduler.
- **Anbindung der Frontends** (offen für G2; ADR 10 ist die Vorlage,
  am 2026-10-25 angenommen und am 2026-10-28 wieder geöffnet): Vorschlag
  REST, Endpunkte als Web-Adapter im Modul, OpenAPI-Spezifikation vor dem
  Code aus Commands, Queries und Read Models in Studio. Gegenoption:
  Thymeleaf + htmx (serverseitig, ohne REST). Zwischen den Modulen kein
  REST (ADR 4).
- **Weiterentwicklung der Events und Zustellung** (G2): wie ein Event
  geändert wird (von ADR 4 angekündigt), Mechanismus der Idempotenz beim
  Empfänger.
- **Minimale UI** (Technik in G2, z. B. eine kleine SPA als
  REST-Client); Seiten etwa Katalogsuche, Leserkonto, Ausleihtheke,
  Tagesblatt.
  Die UI setzt Seiten aus mehreren Modulen zusammen (ADR 8); ein Backend
  for Frontend bleibt der Ausweg.
- **Deployment-Einheiten:** Default eine (Phase 6, G2); Herauslösen erst,
  wenn der Schnitt getragen hat.
- Tests: Decider-Unit-Tests aus Szenarien, Modulith-Scenario-Tests,
  Akzeptanztests aus Flows, Prüfung gegen die OpenAPI-Spezifikation,
  Testcontainers, WireMock (die Prüfung gegen eine API-Spezifikation nur,
  wenn G2 sie beschließt).

---

## 8. Repo-Struktur

```
library-example/
├── README.md
├── CLAUDE.md                    # Regeln für Claude Code (Session-übergreifend)
├── .claude/skills/              # Skills des Workflows (G1), z. B. close-chapter
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
│   ├── gates/                   # Entscheidungen der Gates (ab G1)
│   ├── adr/                     # Architekturentscheidungen (MADR)
│   ├── reviews/                 # Berichte von challenge-context-cut
│   └── tool-gaps.md             # Lücken in DDD Studio
├── api/                         # API-Spezifikationen je Modul, falls G2 sie beschließt
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
| M4 | G1: Phasenmodell (erledigt) | — |
| M5 | ADR 10 (mit Korrekturen an Kapitel 4), unabhängige Prüfung des Schnitts, Kapitel 6: Liefer-Scope | G1 |
| — | **G6** | |
| M6 | Kapitel 7–9: Scope modelliert, Schnitt im Modell geprüft, Example Mapping; Skills `model-scope`, `challenge-context-cut` Modus 2, `example-mapping` | G6, Freigabe des Plans für Phase 5 |
| — | **G2** (Kapitel 10) | |
| M7 | Bauen, Kontext für Kontext | G2 |
| M8 | Skills der Phasen 0–3 herauslösen, frischer Durchlauf | nach dem ersten gebauten Kontext |
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
| G1-1 | Vom Modell zum Code: Reihenfolge, Einheit, Szenarien als Tests, Skills (§6) | G1 | **entschieden** 2026-10-25: Phasenmodell; Einheit und Testkonvention im ersten Bau-Kapitel |
| S1 | Liefer-Scope: welche Szenarien im ersten Inkrement | G6 | **entschieden** 2026-10-26: Option 3 (A, B, C, D, E1–E3, G1, J1), kein Go-live neben LibTrack, CityPay später, C-15 draußen |
| A1 | REST an den Außenkanten (ADR 10) | G2 | am 2026-10-25 angenommen (#17); **wieder offen** seit 2026-10-28 (Maintainer: Technik, kein Vorgriff); ADR 10 `proposed` als Vorlage |
| P5 | Detailplan Phase 5 (§5) | — | **zur Freigabe** (dieser PR) |
| L1 | Wo liegt `esdm lint`? | — | offen, Frage an den Maintainer; bis dahin `validate_model` und `scripts/check_model.py` |
| T1 | Java-, Spring-Boot-, Modulith-Versionen | G2 | offen |
| T2 | Event-Store-Ansatz (Vorschlag: von Hand, Decider) | G2 | offen |
| T3 | Anbindung und Technik der Frontends (Vorschlag REST, ADR 10; Gegenoption Thymeleaf + htmx) | G2 | offen |
| T5 | Weiterentwicklung der Events, Mechanismus der Idempotenz | G2 | offen |
| T4 | Deployment-Einheiten (Default: eine) | G2 | offen |
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
| 04 | Deployment decision | `chapter-04-deployment` (#8) | `9e404d9` | ADRs angenommen #9; MADR-Format #12 (`e065915`); Vorgehen allein aus dem Modell #15; ADR 10 samt Korrekturen an ADR 2–8: ADR 10 samt Korrekturen an ADR 2–8: #17 (`b911252`, 2026-10-25) | `ch4-context-map-circle-noted`, `ch4-context-map-holds` |
| 05 | Challenging the cut | `chapter-05-challenging-the-cut` (#11) | `71b79cd` | Konsistenzprüfung `consistency-after-ch05`; Vorgehen allein aus dem Modell #15 | `ch5-big-picture-after-challenge(-v2 … -v5)`, `ch5-context-map-after-challenge(-v2 … -v4)` |
| 06 | Choosing the first increment | `chapter-06-first-increment` (#19) | `9d4a438` | Verweis auf ADR 10 angepasst (`plan-phase-5-revision`) | — |

Außerhalb der Kapitel: Gate G1, Phasenmodell — `g1-phase-model`
(`docs/gates/g1-model-to-code.md`). Unabhängige Prüfung des Schnitts vor
G6 — `cut-review-before-g6` (#18): Bericht, C-27 bis C-32 (vom Agenten
entschieden, delegiert), ADR 11 `accepted` (2026-10-26), Glossare nachgezogen
(Studio-Version `pre-g6-glossaries-after-review`). Plan für Phase 5 —
`plan-phase-5-revision`: Phase 5 ohne Verträge und REST, ADR 10 wieder
offen, Skills im Rückblick mit Probelauf, Detailplan (2026-10-28).

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
- Stopp-Kriterien: eine fachliche Regel steht nicht in der Quelle **und**
  der Agent findet kein sinnvolles Verhalten (fachliche Fragen sind seit
  2026-10-25 an den Agenten delegiert, Einträge „decided by the agent
  (delegated)“, Maintainer kann im PR widersprechen); ein Gate; schwer umkehrbar *und* es gibt echte Alternativen; macht eine
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
