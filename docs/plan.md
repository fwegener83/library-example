# Plan: Library-Tutorial — von Anforderungen zu laufender Software

*Arbeitsdokument zur Abstimmung (deutsch). Das Tutorial selbst wird englisch.*
*Stand: 2026-10-19 · Status: Entwurf, offen für die SDD-Runde (§6)*

---

## 1. Ziel und Kernbotschaft

Ein durchgängiges Tutorial, das zeigt, wie man aus einem unscharfen
Anforderungsdokument mit DDD zu einem belastbaren Domänenschnitt kommt und
von dort — Bounded Context für Bounded Context, als ob getrennte Teams
arbeiten — zu laufender Software.

**Drei Botschaften, an denen sich jedes Kapitel messen lassen muss:**

1. **Erst verstehen, dann schneiden, dann bauen.** Big Picture Event
   Storming und Domain Stories sind keine Folklore, sie liefern die
   Kontextgrenzen.
2. **Das Modell treibt die Umsetzung.** Domänenmodell (DDD Studio) und
   Spec-Driven Development (Spec Kit) haben getrennte, klar benannte
   Zuständigkeiten — es gibt keine zwei Wahrheiten über die Fachlichkeit.
3. **Grenzen sind anfangs Hypothesen.** Deshalb ein modularer Monolith mit
   *geprüften* Modulgrenzen — und ein Schlusskapitel, in dem eine neue
   Anforderung den Schnitt tatsächlich verschiebt.

**Zielgruppe:** Entwickler:innen und Architekt:innen mit Grundkenntnissen
in Java/Spring, die DDD „schon mal gehört" haben und sehen wollen, wie die
Teile zusammenpassen. Kein DDD-Grundlagenbuch — Konzepte werden dort
erklärt, wo sie gebraucht werden (wie im bestehenden In-App-Tutorial).

---

## 2. Ausgangslage (Befunde)

- **`fwegener83/library-example` ist leer** (kein Commit). Wir starten
  also auf der grünen Wiese.
- **Es gab zwei Library-Modelle in DDD Studio:**
  - **Erster Schnitt (heute In-App):**
    `packages/core/src/examples/library-cataloging.ts`,
    `docs/examples/tutorial-library-example.md`. Kataloghälfte aus ESDMs
    „Your First Model", Ausleihhälfte dazuerfunden. BCs `cataloging`
    (Gate `available-copies-non-negative`) und `lending` (`loan`). Zwei
    gegenläufige Policies → **Partnership**. Offener Punkt: „max. 5 Loans
    pro Mitglied" ist nicht garantierbar.
  - **Zweiter Schnitt = `ddd-by-examples/library`:** hinzugefügt in
    `0bc3c1be` („add the library, cut a second way"), entfernt in
    `0e0797ff` („retire the second library cut"). Wiederherstellbar aus
    `0e0797ff^`: `packages/core/src/examples/library-lending.ts` (~1070
    Zeilen) und `docs/tutorial-library-lending.md`.
    - BCs `catalogue` (supporting) und `lending` (core), **Customer/Supplier**.
    - **Verfügbarkeit liegt in `lending`.** Genau eine Policy überquert die
      Grenze, nur in eine Richtung (`on-instance-added-make-book-available`).
    - Aggregate `patron` mit vier Haltelimit-Regeln (u. a.
      `regular-patrons-hold-at-most-five`). **Das löst den offenen Punkt
      des ersten Schnitts.**
    - Homonym `book` (Katalogdatensatz vs. Exemplar) als
      Ubiquitous-Language-Lektion.
    - System-Akteur + Read Model `daily-sheet` treiben `expire-hold` und
      `register-overdue-checkout`.
    - 12 Slices, 6 Invarianten, GWT-Szenarien inkl. Idempotenz.
- **`ddd-by-examples/library` (MIT) liefert die fachliche Vorlage.** Das
  sind die Geschäftsregeln im README, `docs/big-picture.md` (Big Picture
  Event Storming) und `docs/design-level.md`. Das passt direkt zu den
  Kapiteln 1 und 6. Code übernehmen wir nicht: Unser Code folgt unserem
  Modell. Texte und Regeln verwenden wir mit Quellenangabe.
- **DDD Studio deckt die Kette gut ab:** Sketch Board (Event-Storming-
  Zettel inkl. Hotspot, Areas), Domain Stories, Context Map mit Mustern
  und Teamzuordnung, Glossar, Static View, Flow View, GWT-Szenarien,
  ESDM-Export, Versionen, MCP-Server für Agenten. Die Überführung
  Sketch → Modell ist agentisch (per MCP), nicht per Klick.

**Konsequenz:** Das Tutorial baut auf dem **zweiten Schnitt** auf und
erweitert ihn. Der erste Schnitt bekommt eine Rolle als **erste,
naheliegende Hypothese**: Nach dem Event Storming liegt „Verfügbarkeit
gehört zum Katalog" nahe. Kapitel 3 skizziert das und verwirft es an der
Context Map, denn gegenläufige Policies ergeben eine Partnership. Der
Grund ist die Frage „Wen geht es etwas an, dass ein Buch ausgeliehen
ist?". Damit wird beides verwertet, und die stärkste Lektion des Repos
(*eine Grenze an anderer Stelle ändert alles*) steht mitten im Tutorial
statt in einem Vergleichsbeispiel. Das In-App-Beispiel ersetzen wir am
Ende durch den Tutorial-Stand (§10).

---

## 3. Getroffene Entscheidungen

| Thema | Entscheidung |
|---|---|
| Domäne | Bibliothek (Stadtbibliothek), erweitert um weitere Kontexte |
| Stack | Java, Spring Boot, Spring Modulith |
| Sprache | Englisch (Tutorial, Code, Modell) |
| Ort | eigenes Repo `fwegener83/library-example` |
| Deployment | eine Deployment-Einheit, Module = Bounded Contexts |
| Teams | gedanklich getrennte Teams pro BC, sichtbar über Verträge |
| Homepage | später: Beitrag/Einbindung auf ddd-studio.dev |

---

## 4. Domänenzuschnitt (Zielbild — wird im Tutorial *hergeleitet*)

Das Anforderungsdokument (Kap. 0) wird so geschrieben, dass dieser Schnitt
im Event Storming *naheliegt*, aber nicht offensichtlich ist. Er ist
Hypothese, kein Spoiler.

Kern ist der zweite Schnitt (`catalogue` + `lending`). Erweitert wird nur
dort, wo eine neue Lektion entsteht.

| Kontext | Subdomain | Team (fiktiv) | Modellierungstiefe | Lehrzweck | Herkunft |
|---|---|---|---|---|---|
| `catalogue` | Supporting | Team Collection | **CRUD** (wie in der Referenz) | Bibliographische Datensätze + Exemplare; das Homonym `book` | 2. Schnitt |
| `lending` | **Core** | Team Circulation | event-sourced | Patron-Regeln, Holds, Checkouts, Überfälligkeit, Tagesblatt | 2. Schnitt |
| `membership` | Supporting | Team Members | CRUD | Registrierung, Patron-Typ (regular/researcher), Sperren. Löst die Metamodell-Krücke `register-patron` in `lending` auf | neu |
| `fees` | Supporting | Team Finance | event-sourced | Gebühren für Überfälligkeit, Zahlung über ACL | neu |
| `notification` | Generic | Team Platform | dünn | reiner Event-Konsument (Hold bereit, Hold verfallen, überfällig) | neu |
| *Payment Provider* | extern | — | Stub | **Anti-Corruption Layer** | neu |
| *Book Metadata Service* (z. B. Open Library) | extern | — | echter Aufruf + Stub im Test | ACL vs. Conformist bewusst abgewogen | neu |

**Context-Map-Hypothese:**

- `catalogue` → `lending`: **Customer/Supplier**, eine Überquerung in eine
  Richtung (aus dem 2. Schnitt)
- `membership` → `lending`: **Customer/Supplier**. Lending hält ein eigenes
  `patron`-Modell, gespeist aus `patron-registered`. Das ist die zweite
  Ubiquitous-Language-Lektion: *member* in membership, *patron* in lending.
- `lending` → `fees`, `notification`: **Open Host Service + Published
  Language** (Lending veröffentlicht Integration Events, Downstreams
  passen sich an)
- `fees` → `membership`: **Customer/Supplier** (offene Gebühren über
  Schwelle sperren das Mitglied, und die Sperre fließt zurück zu
  `lending`)
- `fees` → Payment Provider: **ACL**
- `catalogue` → Metadata Service: **ACL** (Alternative Conformist wird
  diskutiert)
- **Shared Kernel** wird diskutiert und **verworfen** (z. B. für `Isbn`),
  mit Begründung.
- Die **Partnership** des ersten Schnitts erscheint als verworfene
  Hypothese (Kap. 3).

**Lektion „nicht jeder Kontext verdient dieselbe Tiefe":** `catalogue`
und `membership` bleiben CRUD, `notification` bleibt ein Listener. Event
Sourcing gibt es nur dort, wo Historie und Invarianten zählen. Die
Referenz begründet das für den Katalog genauso: Das Event Storming fand
dort keine komplexe Regel. Das passt gut zu ihr.

**Process Manager nicht erzwingen.** Der zweite Schnitt löst Hold-Ablauf
und Überfälligkeit ohne Process Manager: Ein Tagesblatt (Read Model)
treibt System-Commands, das ist das To-do-List-Muster. Das ist eine
eigene, wertvolle Form. Ein Process Manager wäre erst gerechtfertigt,
wenn ein Ablauf über mehrere Kontexte Zustand und Kompensation braucht.
Ein Kandidat dafür: *Mahnlauf* (überfällig → Gebühr → Benachrichtigung →
nach Frist Sperre → bei Zahlung Entsperrung). Siehe offene Frage F1.

---

## 5. Kapitelstruktur

Jedes Kapitel hat dasselbe Raster: **Ziel · Input · Vorgehen · Werkzeug ·
Ergebnis im Repo · Git-Tag**. Jeder Stand ist reproduzierbar
(`git checkout chapter-NN`) und im Studio als Version gespeichert.

| # | Kapitel | Werkzeug | Ergebnis im Repo |
|---|---|---|---|
| 0 | **The brief** — Anforderungsdokument der Stadtbibliothek, absichtlich lückenhaft, mit Synonymen und Widersprüchen | Text | `requirements/brief.md` |
| 1 | **Big Picture Event Storming** — chaotische Exploration, Zeitleiste, Schlüsselereignisse, Hotspots, Akteure, externe Systeme | Sketch Board | `model/sketch/big-picture.*`, Fotostrecke im Kapitel |
| 2 | **Domain Stories** — 2–3 Kernprozesse (Ausleihe, Rückgabe mit Verspätung, Vormerkung); Sprachkonflikte klären | Domain Stories | `model/stories/*.esdm.yaml` |
| 3 | **Strategic design** — Subdomains, Bounded Contexts, Glossar, Context Map mit Mustern, Teamzuordnung; die naheliegende erste Hypothese (Verfügbarkeit im Katalog → Partnership) wird skizziert und verworfen | Context Map, Glossar | `model/library.esdm.yaml` (strategisch), verworfene Variante als Studio-Version |
| 4 | **Architecture decisions** — Modulith, Modul = BC, Integrationsregeln, ES nur wo nötig; daraus die **Constitution** | ADRs, Spec Kit | `docs/adr/*`, `.specify/memory/constitution.md`, Projekt-Skelett mit leeren Modulen + Modulith-Verify-Test |
| 5 | **Cross-context flows** — die Lebensgeschichte eines Buchs über alle Kontexte: Ausleihe → Überfälligkeit → Gebühr → Benachrichtigung → Sperre | Flow View | Flow im Modell, Integration Events als Published Language |
| 6 | **Going deep, team by team** — je BC: Aggregates, Invarianten, Commands/Events, Read Models, GWT-Szenarien. Die Regeln landen dort, wo das ablehnbare Command ankommt (`patron`); Denkfalle „Boolean statt Zähler" aus dem ersten Schnitt | Static View, Slices, Scenarios | vollständiges taktisches Modell |
| 7 | **From model to spec** — Specs pro Team/Fähigkeit aus dem Modell ableiten | Spec Kit + DDD-Studio-MCP | `specs/NNN-*/` |
| 8 | **Implementation** — Slice für Slice, Szenarien als Tests zuerst, Verträge zwischen Modulen testen | Code, Spring Modulith | `src/…`, Tests |
| 9 | **Evolution** — eine neue Anforderung stellt den Schnitt infrage; Modell → Spec → Code ändern sich in dieser Reihenfolge | alle | Diff über alle Ebenen |

**Umsetzungstiefe im Code:**
- **Voll:** `lending` (event-sourced) und `fees` mit Payment-ACL.
- **Bewusst schlicht:** `catalogue` und `membership` als CRUD,
  `notification` als Log- bzw. Mail-Stub.
- **Modelliert** werden alle Kontexte.

---

## 6. Kernthema: DDD und Spec-Driven Development zusammenbringen

*Das ist der Abschnitt für die Extra-Runde. Er enthält meinen Vorschlag,
die verworfenen Alternativen und die offenen Fragen.*

### 6.1 Das Grundproblem

Spec Kit versteht die Spec als „source of truth" — *„code serves
specifications"*. DDD Studio versteht das Modell als Quelle der
Fachlichkeit. Werden beide naiv kombiniert, beschreiben `spec.md`
(„Key Entities", Acceptance Scenarios) und `data-model.md` dieselbe
Fachlichkeit ein zweites Mal — in Prosa, pro Feature, ohne
Kontextgrenzen. Das driftet garantiert auseinander.

### 6.2 Vorschlag: Zuständigkeit nach Frage trennen

| Frage | Zuhause | Artefakt |
|---|---|---|
| **Was ist die Domäne?** Sprache, Grenzen, Aggregates, Invarianten, Events, Policies, Verhalten an Beispielen | **DDD Studio** | `model/*.esdm.yaml` (ESDM-Export, versioniert im Repo) |
| **Warum, für wen, welches Inkrement?** Nutzen, Scope, Priorität, nicht-funktionale Anforderungen, UI/API-Verhalten | **Spec Kit** `spec.md` | `specs/NNN-*/spec.md` |
| **Wie bauen wir es?** Technik, Module, Persistenz, Schnittstellen | **Spec Kit** `plan.md` | `plan.md`, `contracts/`, `research.md` |
| **In welchen Schritten?** | **Spec Kit** `tasks.md` | `tasks.md` |
| **Welche Regeln gelten immer?** Architekturregeln aus dem strategischen Design | **Constitution** | `.specify/memory/constitution.md` |

**Eine Regel, die das Tutorial wiederholt einhämmert:**
> *Fachliche Fragen werden nie in der Spec beantwortet, sondern im Modell —
> die Spec verweist darauf.*

### 6.3 Der Kreislauf

```
 Event Storming / Domain Stories
             │
             ▼
  DDD Studio: strategisches Modell ──► Constitution (Architekturregeln)
             │
             ▼
  DDD Studio: Flow, Slices, Szenarien ──► ESDM-Export im Repo
             │                                 │
             ▼                                 ▼
  /speckit-specify  (liest Modell per MCP bzw. Export, verweist auf Slices/Szenarien)
             │
   Klärung findet Fachlücke? ──ja──► zurück ins Modell, erst dann weiter
             │ nein
             ▼
  /speckit-plan  (Modul = BC, Aggregate = Decider, Policy = Modul-Listener, ACL …)
             ▼
  /speckit-tasks (Szenarien zuerst als fehlschlagende Tests)
             ▼
  /speckit-implement
             ▼
  CI: esdm lint · jedes Szenario hat einen Test · Module == BCs · Events im Code == Events im Modell
```

### 6.4 Konkrete Bausteine

1. **Constitution aus dem strategischen Design.** Beispiele für Artikel:
   Module entsprechen Bounded Contexts; kein Zugriff auf Interna fremder
   Module; Integration nur über veröffentlichte Events oder eine explizite
   Modul-API; externe Systeme nur hinter einer ACL; jedes GWT-Szenario
   wird zuerst als fehlschlagender Test umgesetzt; Event Sourcing nur in
   Kontexten, die das Modell als event-sourced führt; die Spec definiert
   keine Fachbegriffe neu.
2. **Spec-Kit-Preset „DDD Studio"** (Spec Kit unterstützt Presets und
   projektlokale Template-Overrides): Die Spec-Vorlage ersetzt „Key
   Entities" durch **„Domain model references"** (BC, Slices, Szenarien
   per qualifiziertem Namen), ergänzt **„Integration contracts"** (welche
   Events konsumiert/veröffentlicht) und **„Team boundary"**. Die
   Plan-Vorlage bekommt ein Mapping-Raster Modell → Code. *Startet im
   Tutorial-Repo; später ggf. als wiederverwendbares Preset für DDD-Studio-
   Nutzer — das wäre ein starkes Homepage-Argument.*
3. **Agent liest das Modell per MCP.** Claude Code mit DDD-Studio-MCP und
   Spec Kit: `/speckit-specify` bekommt „Slice X im Flow Y" statt eines
   Prosatexts; der Agent holt Slices und Szenarien selbst. Das ist die
   eindrücklichste Demo im Tutorial.
4. **Szenarien → Tests.** Jedes ESDM-Szenario wird ein JUnit-Test mit
   identischem Namen (Given = Events, When = Command, Then = Events /
   Rejection). Für Aggregate reine Unit-Tests auf Decider-Ebene; für
   modulübergreifende Abläufe die Scenario-Test-API von Spring Modulith.
   Ein kleines Prüfskript in CI stellt sicher, dass kein Szenario ohne
   Test bleibt.
5. **Verträge zwischen Teams.** Integration Events sind Published
   Language: im Modell definiert, im Upstream-Modul als öffentlicher Typ,
   in beiden Specs unter `contracts/` referenziert, mit einem
   Vertragstest im Downstream-Modul.

### 6.5 Erwogene Alternativen

| Variante | Bewertung |
|---|---|
| **A — Spec-first:** Spec Kit pur, Modell wird nachträglich gezeichnet | Verworfen. Domänenwissen entsteht in Prosa pro Feature, Grenzen fallen nie auf; das Modell wird Dekoration. |
| **B — Model-only:** kein Spec Kit, Agent implementiert direkt aus dem Modell | Möglich und schlank, verliert aber Nutzen, Scope, NFRs, Plan und Tasks — und das SDD-Thema, das du herausstellen willst. |
| **C — Geschichtet (Vorschlag):** Modell für Fachlichkeit, Spec Kit für Inkrement und Umsetzung | Empfohlen. Klare Zuständigkeit, Rückkopplung explizit, prüfbar in CI. |

### 6.6 Offene Fragen für die SDD-Runde

- **S1 — Zuschnitt einer Spec:** eine Spec pro Slice, pro
  Nutzerfähigkeit (mehrere Slices, z. B. „Borrow a book") oder pro BC-
  Inkrement? *Mein Vorschlag:* pro Nutzerfähigkeit **innerhalb eines BC**;
  modulübergreifende Fähigkeiten werden in Team-Specs geschnitten, die
  über einen Vertrag verbunden sind. Das macht die Teamgrenze sichtbar.
- **S2 — Wer ist Master des Modells?** Studio als Master, Export bei jeder
  Modelländerung ins Repo committen (Review sieht den Modell-Diff) — oder
  Repo-Datei als Master, Import ins Studio? *Vorschlag:* Studio = Master,
  Export im Repo = überprüfbarer Snapshot.
- **S3 — Szenarien → Tests:** im Tutorial 1:1 von Hand (mit
  Namenskonvention + Coverage-Check) oder ein Generator? *Vorschlag:* von
  Hand; ein Generator wäre ein eigenes DDD-Studio-Feature (→ §10).
- **S4 — Preset oder nur Constitution?** Reicht eine gute Constitution,
  oder lohnt das eigene Preset schon im Tutorial? *Vorschlag:* Preset —
  sonst erzeugt Spec Kit die doppelten „Key Entities".
- **S5 — Spec Kit-Version:** Die Befehle haben sich verändert
  (`/speckit.x` → Skills `/speckit-x`, neu z. B. `/speckit-converge`,
  Extensions). Wir pinnen beim Aufsetzen eine Version und prüfen die
  Befehle dann genau.
- **S6 — Rückkopplung sichtbar machen:** Soll das Tutorial mindestens
  einmal bewusst zeigen, wie `/speckit-specify` eine Fachlücke aufdeckt,
  die zurück ins Modell geht? *Vorschlag:* ja, in Kapitel 7 inszeniert.

---

## 7. Technische Architektur (Vorschlag)

- **Java** (aktuelles LTS), **Spring Boot**, **Spring Modulith** — Versionen
  beim Aufsetzen festlegen.
- **Ein Modul pro BC** als Top-Level-Package; Interna in Unterpackages,
  öffentliche Typen nur Modul-API und Integration Events.
- **Event Sourcing von Hand, minimal und lesbar:** Aggregate als
  *Decider* (sealed Interfaces + Records: `decide(command, state) →
  events`, `evolve(state, event) → state`), ein schlanker JDBC-Event-Store
  in Postgres. Kein Axon: würde das Konzept verstecken, und sein
  Programmiermodell bildet ESDM nicht 1:1 ab. Der Decider bildet GWT
  dagegen direkt ab.
- **Policies** = `@ApplicationModuleListener` im *Downstream*-Modul;
  Spring Modulith's **Event Publication Registry** = Outbox mit
  at-least-once — exakt die Semantik, die das Modell für Policies
  deklariert (`deliveryGuarantee: at-least-once`, Idempotenz downstream).
- **System-Commands aus dem Tagesblatt** (`expire-hold`,
  `register-overdue-checkout`) über einen Scheduler. Der Process Manager
  für den Mahnlauf wird nur gebaut, falls F1 = ja.
- **Read Models** als JDBC-Projektionen; **API** REST + OpenAPI. UI
  vorerst nicht (→ F3).
- **Tests:** Decider-Unit-Tests aus Szenarien, Modulith-Scenario-Tests,
  `ApplicationModules.verify()`, Testcontainers für Postgres, WireMock für
  externe Systeme.
- **Doku-Abgleich:** Spring Modulith generiert Moduldiagramme — im
  Tutorial direkt neben die Context Map gestellt („stimmt der Code mit dem
  Modell überein?").

---

## 8. Repo-Struktur

```
library-example/
├── README.md                    # Einstieg, Kapitelübersicht, Quickstart
├── requirements/brief.md        # Kapitel 0
├── model/                       # ESDM-Exporte, Stories, Sketch-Exporte
├── docs/
│   ├── tutorial/00-…09-*.md     # die Kapitel
│   └── adr/
├── .specify/                    # Spec Kit: Constitution, Templates/Preset
├── specs/NNN-<bc>-<capability>/ # spec.md, plan.md, contracts/, tasks.md
├── src/main/java/…/{catalogue,lending,membership,fees,notification}/
└── src/test/java/…
```

Git-Tags `chapter-00` … `chapter-09`; Studio-Workspace mit gleichnamigen
Versionen; öffentlicher Read-only-Link pro Stand.

---

## 9. Meilensteine

| M | Inhalt | Abhängigkeit |
|---|---|---|
| M0 | Plan + SDD-Runde abgeschlossen | — |
| M1 | Kapitel 0: Anforderungsdokument | M0 |
| M2 | Kapitel 1–3 im Studio + Export + Texte | M1 |
| M3 | Kapitel 4: ADRs, Constitution, Preset, Projekt-Skelett, CI | M2 |
| M4 | Kapitel 5–6: Flow + taktisches Modell (alle BCs) | M2 |
| M5 | Kapitel 7–8 für `catalogue` + `lending` | M3, M4 |
| M6 | `fees` + ACL, `membership`, `notification` (+ Process Manager, falls F1) | M5 |
| M7 | Kapitel 9: Evolution | M6 |
| M8 | In-App-Beispiel abgleichen/ersetzen, Homepage-Beitrag | M7 |

Jeder Meilenstein endet mit einem Review durch dich, bevor der nächste
beginnt.

---

## 10. Rückwirkungen auf DDD Studio

- **In-App-Beispiel:** Der erste Schnitt wird durch den zweiten ersetzt.
  Er lässt sich aus `0e0797ff^` wiederherstellen und muss an den
  heutigen Metamodell-Stand angepasst werden. Die Erweiterungen
  (membership, fees, notification, externe Systeme) stellen wir dort
  **nicht** ein. Das In-App-Beispiel bleibt „der kurze Einstieg"
  (Begründung aus `0e0797ff`). Den vollen Tutorial-Stand gibt es als
  öffentlichen Read-only-Workspace.
  Ob catalogue + lending im Tutorial artefaktgleich mit dem
  In-App-Beispiel sind, prüfen wir am Ende von Kapitel 6.
  Das deutsche Dokument `docs/examples/tutorial-library-example.md` wird
  dann ersetzt.
- **Werkzeuglücken sammeln, nicht nebenbei fixen.** Während des Tutorials
  fallen sicher Lücken auf (Kandidaten: Szenario → Test-Export, Spec-Kit-
  Preset als Produktbestandteil, Sketch → Modell-Überführung). Wir
  notieren sie als Issues im ddd-studio-Repo und entscheiden getrennt.
- **Homepage:** Beitrag + Link aufs Repo und die Read-only-Workspaces —
  später.

---

## 11. Weitere offene Fragen

- **F1 — Process Manager für den Mahnlauf?** Holds und Überfälligkeit
  brauchen keinen. Der Mahnlauf über `lending`, `fees`, `notification`
  und `membership` wäre ein ehrlicher Kandidat. *Vorschlag:* nur
  modellieren und gegen die Policy-Choreographie abwägen; bauen erst,
  wenn die Abwägung für ihn ausgeht.
- **F2 — Abweichungen des zweiten Schnitts übernehmen?**
  `register-patron` in `lending` war eine Metamodell-Krücke und wird
  durch `membership` ersetzt. `place-on-hold` trägt den `instance-type`.
  *Vorschlag:* den Typ als Daten aus dem `catalogue`-Event in das
  lending-eigene `book` übernehmen, statt ihn vom Aufrufer mitzugeben.
  Das ist sauberer, sobald es ohnehin eine Überquerung gibt.
- **F3 — UI oder nur API?** *Vorschlag:* nur API (plus HTTP-Beispieldatei);
  eine UI lenkt vom Thema ab.
- **F4 — Evolutionsszenario für Kapitel 9:** *E-Books* (digitale
  Exemplare kennen keine Knappheit → stellt das zentrale Gate infrage →
  Modell-Umbau) oder *Herauslösen von `notification`* (zeigt, dass der
  Modulith den Split billig macht). *Vorschlag:* E-Books — es zeigt, wie
  eine Anforderung zuerst das Modell ändert, dann Spec, dann Code.
- **F5 — Tutorial-Format:** reine Markdown-Kapitel im Repo, ergänzt um
  Screenshots/GIFs aus dem Studio. Die klickbaren In-App-Tutorials
  (`tutorials/*.yaml`) höchstens für einzelne Kapitel.
