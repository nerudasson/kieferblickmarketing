---
name: seo-pipeline
description: Erzeugt SEO-Wissensartikel in Menge aus daten/artikel-queue.csv – Entwurf, Compliance-Prüfung, WordPress-Entwurf. Nutzen, wenn Alexander Artikel erstellen, einen Batch starten oder den Stand der Warteschlange sehen will.
---
# seo-pipeline

Ziel: Warteschlange abarbeiten. Der Agent legt nur **Entwürfe** an, Alexander veröffentlicht in WordPress.

## Gesamtablauf von A bis Z (Überblick)
| Stufe | Wer | Ergebnis |
|---|---|---|
| 0 Keyword-Auswahl | Skill `keyword-research` (`waehle_keywords.py`) | Queue-Zeilen mit Kategorie, Thema, Praxis-Flag |
| 1 Brief | `seo_brief.py` (DataForSEO) | Nebenkeywords, Fragen, Verwandte Suchen, Wettbewerber-Struktur, Ziel-Länge |
| 2 Plan | Agent `article-planner` | Cluster → Abschnitte, Element und **Wortbudget je Abschnitt**, Keyword-Zuordnung, Lücken-Abschnitt, Tabellen/FAQ mindestens auf Wettbewerbsniveau, Kostenrahmen-Belegfrage bei Intent Kosten; Summe erreicht die SEO-Ziel-Länge des Briefs (`plan-check` prüft hart) |
| 3 Belege | Agent `evidence-researcher` (nur Fehlendes) | `daten/belege/<thema>.md` |
| 4 Skelett | `skelett.py` | Vorlage mit Zusage, CTA, Links |
| 5 Schreiben | Agent `article-writer` (nutzt Spalte „Formulierung“) | Artikel, ein Korrekturdurchgang gegen harte Fehler, `abschluss` |
| 6 Hürden | `pipeline.py check/gates` | harte Fehler vs. weiche Hinweise |
| 7 Review | je Artikel ein `compliance-reviewer` parallel (Stichprobenregel), Befunde in `daten/reviews/<slug>.md`, danach eine Fix-Runde nur für „wichtige“ Befunde | Ampel, Annahmen |
| 8 WordPress | `wp_publish.py` | Entwurf (nie veröffentlicht), Beitragsbild, `kb_geprueft` = Datum, Link-Prüfung (Inhaltsleiste und Überschrift-IDs baut das Theme selbst) |

Leitlinien dieses Aufbaus (alle in `references/regeln.md`): Agenten fragen im Batch nie nach, sondern treffen die konservativste Annahme und vermerken sie; Belegpflicht nur für Zahlen, Wirksamkeit, Risiken, Kasse/Recht, Preise; Preise im Artikel nur Intro-Offers und „ab“-Preis; Zitate als `[B..]`, Quellenbox 5–6 (max. 8); Länge aus Wettbewerber-Median (Brief) → Plan (Budget je Abschnitt und Element) → Writer füllt jedes Budget; fehlende Belege werden zu Orientierung, nicht zu Kürzung.
Zugänge in der Cloud-Umgebung: DataForSEO, WordPress und PubMed laufen über den Proxy bzw. frei; OpenAlex über den Connector. Es ist kein API-Schlüssel im Repo.
Neuer Chat: Branch `claude/magical-wright-r306g3` bzw. nach Merge den Standard-Branch nutzen; Einstieg `pipeline.py status`.

## Effizienz-Regeln (seit 19.10.2026, aus dem Batch mit 10 Artikeln)
- **Pro Artikel eine Kette, keine Stufen-Barrieren:** Plan → Belege (einmal je Thema) → Skelett → Schreiben → `abschluss` → Review → Fix → `abschluss`. Jeder Artikel geht weiter, sobald seine eigene Stufe fertig ist. Empfohlen: Workflow `artikel-batch` (`.claude/workflows/artikel-batch.js`, `args: {slugs: [...]}`); startet viele Agenten, daher nur auf ausdrücklichen Wunsch von Alexander.
- **Fehler vorab vermeiden:** Beleg-Tabelle mit Spalte „Formulierung“ (fertiger, korrekt begrenzter Satz), `hwg_check.py` (in `pipeline.py check/gates/abschluss` und `wp_publish.py` enthalten), Abschnitt „Typische Befunde“ in `regeln.md`.
- **Review gezielt und parallel:** je Artikel ein `compliance-reviewer`, Eingabe `pipeline.py check <slug>` (Skript-Treffer + ABGLEICH), Ausgabe `daten/reviews/<slug>.md`; der Autor liest sie im Fix-Modus selbst. Keine Weitergabe von Hand.
- **Endstand:** Nach jedem Schreiben oder Fix `pipeline.py abschluss <slug>` (check, finalize, check); danach nicht mehr editieren. `gates` und `wp_publish.py` prüfen den Stand ohnehin erneut.
- **Kurze Berichte:** Agenten antworten mit höchstens 40 Wörtern; Lücken, Fragen an Alexander, Nebenartikel und Regelkonflikte gehen mit `backlog.py add …` nach `daten/backlog.md`. Nebenartikel speisen die nächste Keyword-Auswahl.
- **Themenwahl:** `waehle_keywords.py` begrenzt auf 3 neue Artikel je Thema (`--max-pro-thema`), damit nicht mehrere Varianten desselben Themas parallel entstehen. Vorab `pipeline.py fragen`: Praxisfragen an Alexander (nicht blockierend). Pro Thema ein Kostenrahmen-Beleg, bevor Kostenartikel geschrieben werden.
- **Nichts wegwerfen:** Bestehende Entwürfe, Pläne und WordPress-Entwürfe erst löschen, wenn der Ersatz fertig und besser ist (Belege bleiben immer).
- **Review-Log:** nicht leeren; ein leeres Log erzwang bisher die Vollprüfung (Standardwert 99, jetzt 0).

## Ablauf (pro Batch, z. B. 10 Keywords)
Deterministische Stufen übernimmt `scripts/pipeline.py`, die Agenten bekommen eine Arbeitsliste. `pipeline.py prepare` führt immer die nächste mögliche Stufe aus und nennt, welcher Agent als Nächstes dran ist. `pipeline.py status` zeigt je Artikel die nächste Stufe.
1. **Auswahl und Brief:** Zuerst Queue füllen (`keyword-research`: `waehle_keywords.py --top 10`). Dann `pipeline.py prepare --n 10` nimmt die nächsten offenen Zeilen der Queue (Kategorie und Thema aus `references/themen.json`) und holt je Keyword den SEO-Brief (`seo_brief.py`, DataForSEO: Volumen, Nebenkeywords, Fragen, Verwandte Suchen, Wettbewerber; ca. 0,02–0,03 USD je Brief, `--dry-run` zeigt die Abrufe; bei mehr als 20 am Stück vorher die Summe nennen).
2. **Artikelplan (automatisch, ohne Freigabe):** `article-planner` je Artikel parallel. Er bildet aus Nebenkeywords, Fragen und Verwandten Suchen **Cluster** (= Abschnitte), legt je Abschnitt Argument, **Element** (Tabelle, Liste, Schritte, Fließtext), Belegfrage, Ziel-Länge und Bausteine fest → `daten/plaene/<slug>.md`. Prüfung: `skelett.py plan-check <slug>`.
3. **Belege (bedarfsgetrieben):** `evidence-researcher` je Thema mit den Belegfragen der Pläne: je Frage **ein starker Beleg**, vorhandene Belege werden wiederverwendet (`daten/belege/<thema>.md`, Frontmatter `abgedeckt`). Danach `pipeline.py prepare` erneut.
4. **Skelett:** `prepare` legt es aus dem Plan an (`skelett.py`): Abschnitte mit Element-Hinweis, Zusage und CTA nach Kategorie, Weiterlesen, Quellen-Platzhalter. Praxis-Block pflicht oder optional laut Queue.
5. **Schreiben:** `article-writer` je Skelett parallel, nach Plan und Belegen, im Stil von `references/regeln.md`. Er prüft sich mit `lesbarkeit.py` und `belege_check.py check` (Zitate `[B19]`) und ruft `finalize` auf (nummeriert, baut die Quellenbox mit 4–6 Quellen; Länge nahe `ziel_woerter`).
6. **Hürden:** `pipeline.py gates` über alle Entwürfe. Nicht OK → höchstens 2 Rückläufe an den Writer, danach `warteschlange.py set <slug> blockiert`.
7. **Review nach Stichprobenregel:** `pipeline.py review` nennt die Entwürfe, die der `compliance-reviewer` prüfen muss (die ersten 3 je Thema immer, danach jeder fünfte, dazu Kosten/Vergleich, Kasse/Recht, Praxis-Block, viele Zitate; Rückfallregel bei Rot oder ≥ 3 **wichtigen** Befunden im Schnitt der letzten 5 (Schwere „wichtig“ vs. „klein“ vergibt der Reviewer)). Mehrere Entwürfe in **einem** Aufruf. Ergebnis mit `pipeline.py logreview <slug> <rot|gelb|gruen> <n>` eintragen. Rot → Writer, max. 2 Runden. Gelb: **eine Fix-Runde** durch den Writer (SendMessage an denselben Writer, nur Edit-Patches; Befunde werden ersetzt, nicht gestrichen, das Wortbudget bleibt) für die Befunde der Schwere „wichtig“ und die Annahmen-Vorschläge des Reviewers, danach `pipeline.py check`; „klein“ nur, wenn mit einem Satz machbar. Danach `warteschlange.py set <slug> geprueft`. Kein erneuter Review.
8. **Fragen an Alexander:** `pipeline.py fragen` bündelt offene `[FAKT FEHLT]` und die Praxisfragen aus den Plänen je Thema (Antwort 1–3 Sätze je Zeile in `material/fakten.md`, Abschnitt „Persönliche Einschätzung“, Format `- <slug>: …`). Artikel mit `praxis: optional` brauchen das nicht.
9. **WordPress-Entwurf:** `wp_publish.py <entwurf> --dry-run` zeigt das HTML, ohne `--dry-run` legt es den Entwurf an (Kategorie, Yoast, Theme-Felder, `status=draft`). Verweigert bei `[FAKT FEHLT]`, ausstehenden Prüfungen oder unbekannter Kategorie. Danach `warteschlange.py set <slug> wp_entwurf`.
10. **Bericht an Alexander:** Anzahl je Ampel, Lesbarkeit, Länge gegen Ziel, offene Fragen je Thema, was in WordPress wartet, Hinweis zum Bild-Alt-Text (Phrase), solange Bilder nicht im Beitrag stehen.

## Regeln
- Nie `status=publish`. Veröffentlichen gibt nur Alexander frei.
- Doppelungen: `warteschlange.py check` meldet Keywords, die zu nah beieinander liegen (gleicher Cluster und gleicher Wortstamm) – zusammenlegen statt zwei Artikel.
- Skalierung: Batchgröße steigern erst, wenn die letzten 10 Entwürfe ohne rot durchliefen.
- Ergebnisse (Indexierung, Rankings) später in `experiment-log.md`.

## Testfälle
Siehe `tests/faelle.md`.
