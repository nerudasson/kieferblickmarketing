---
name: seo-pipeline
description: Erzeugt SEO-Wissensartikel in Menge aus daten/artikel-queue.csv – Entwurf, Compliance-Prüfung, WordPress-Entwurf. Nutzen, wenn Alexander Artikel erstellen, einen Batch starten oder den Stand der Warteschlange sehen will.
---
# seo-pipeline

Ziel: Warteschlange abarbeiten. Der Agent legt nur **Entwürfe** an, Alexander veröffentlicht in WordPress.

## Ablauf (pro Batch, z. B. 10 Keywords)
Deterministische Stufen übernimmt `scripts/pipeline.py`, die Agenten bekommen eine Arbeitsliste. `pipeline.py prepare` führt immer die nächste mögliche Stufe aus und nennt, welcher Agent als Nächstes dran ist. `pipeline.py status` zeigt je Artikel die nächste Stufe.
1. **Auswahl und Brief:** `pipeline.py prepare --n 10` nimmt die nächsten offenen Zeilen der Queue (Kategorie und Thema aus `references/themen.json`) und holt je Keyword den SEO-Brief (`seo_brief.py`, DataForSEO: Volumen, Nebenkeywords, Fragen, Verwandte Suchen, Wettbewerber; ca. 0,02–0,03 USD je Brief, `--dry-run` zeigt die Abrufe; bei mehr als 20 am Stück vorher die Summe nennen).
2. **Artikelplan (automatisch, ohne Freigabe):** `article-planner` je Artikel parallel. Er bildet aus Nebenkeywords, Fragen und Verwandten Suchen **Cluster** (= Abschnitte), legt je Abschnitt Argument, **Element** (Tabelle, Liste, Schritte, Fließtext), Belegfrage, Ziel-Länge und Bausteine fest → `daten/plaene/<slug>.md`. Prüfung: `skelett.py plan-check <slug>`.
3. **Belege (bedarfsgetrieben):** `evidence-researcher` je Thema mit den Belegfragen der Pläne: je Frage **ein starker Beleg**, vorhandene Belege werden wiederverwendet (`daten/belege/<thema>.md`, Frontmatter `abgedeckt`). Danach `pipeline.py prepare` erneut.
4. **Skelett:** `prepare` legt es aus dem Plan an (`skelett.py`): Abschnitte mit Element-Hinweis, Zusage und CTA nach Kategorie, Weiterlesen, Quellen-Platzhalter. Praxis-Block pflicht oder optional laut Queue.
5. **Schreiben:** `article-writer` je Skelett parallel, nach Plan und Belegen, im Stil von `references/regeln.md`. Er prüft sich mit `lesbarkeit.py` und `belege_check.py check` (Zitate `[B19]`) und ruft `finalize` auf (nummeriert, baut die Quellenbox mit 4–6 Quellen; Länge nahe `ziel_woerter`).
6. **Hürden:** `pipeline.py gates` über alle Entwürfe. Nicht OK → höchstens 2 Rückläufe an den Writer, danach `warteschlange.py set <slug> blockiert`.
7. **Review nach Stichprobenregel:** `pipeline.py review` nennt die Entwürfe, die der `compliance-reviewer` prüfen muss (die ersten 3 je Thema immer, danach jeder fünfte, dazu Kosten/Vergleich, Kasse/Recht, Praxis-Block, viele Zitate; Rückfallregel bei Rot oder ≥ 3 **wichtigen** Befunden im Schnitt der letzten 5 (Schwere „wichtig“ vs. „klein“ vergibt der Reviewer)). Mehrere Entwürfe in **einem** Aufruf. Ergebnis mit `pipeline.py logreview <slug> <rot|gelb|gruen> <n>` eintragen. Rot → Writer, max. 2 Runden. Gelb/grün → `warteschlange.py set <slug> geprueft`.
8. **Fragen an Alexander:** `pipeline.py fragen` bündelt offene `[FAKT FEHLT]` je Thema (Antwort 1–3 Sätze je Zeile in `material/fakten.md`, Abschnitt „Persönliche Einschätzung“, Format `- <slug>: …`). Artikel mit `praxis: optional` brauchen das nicht.
9. **WordPress-Entwurf:** `wp_publish.py <entwurf> --dry-run` zeigt das HTML, ohne `--dry-run` legt es den Entwurf an (Kategorie, Yoast, Theme-Felder, `status=draft`). Verweigert bei `[FAKT FEHLT]`, ausstehenden Prüfungen oder unbekannter Kategorie. Danach `warteschlange.py set <slug> wp_entwurf`.
10. **Bericht an Alexander:** Anzahl je Ampel, Lesbarkeit, Länge gegen Ziel, offene Fragen je Thema, was in WordPress wartet.

## Regeln
- Nie `status=publish`. Veröffentlichen gibt nur Alexander frei.
- Doppelungen: `warteschlange.py check` meldet Keywords, die zu nah beieinander liegen (gleicher Cluster und gleicher Wortstamm) – zusammenlegen statt zwei Artikel.
- Skalierung: Batchgröße steigern erst, wenn die letzten 10 Entwürfe ohne rot durchliefen.
- Ergebnisse (Indexierung, Rankings) später in `experiment-log.md`.

## Testfälle
Siehe `tests/faelle.md`.
