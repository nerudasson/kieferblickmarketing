# Artikelstruktur

Frontmatter: title, slug, keyword, cluster, intent, kategorie, autor (Alexander Andreev), meta_description (max. 155 Zeichen), status (entwurf).

1. Antwort in den ersten zwei Sätzen
2. Gliederung mit H2 passend zur Suchabsicht (Fragen als H2 wo sinnvoll)
3. Was dagegen spricht / Nachteile ehrlich
4. Kosten oder Ablauf konkret, wenn das Keyword danach fragt (nur Zahlen aus `kontext/angebot-und-preise.md`)
5. Wann ein Termin sinnvoll ist (ohne Druck, ohne Diagnose)
6. FAQ (3–5 Fragen, kurz)
7. Autorenbox: Alexander Andreev, Kieferblick · ZAHNBOUTIQUE, Mülheim an der Ruhr

Länge nach Intent: Info 800–1.200 Wörter, Kosten/Vergleich 1.200–1.800. Interne Links: 2–4 auf Artikel desselben Clusters, 1 auf die Leistungsseite.

## WordPress-Format (Vorlage: Beitrag „Beispielartikel“, ID 105)
- **Kategorie:** passend zum Thema (Aligner, Bleaching & Zahnreinigung, Veneers, Schnarchschiene, Funktionsschiene), IDs in `kontext/tech-stack.md`.
- **Hero-Bullets:** `meta.kb_kurz`, genau 3 Zeilen, je ein kurzer Satz mit Kernaussage, Quellenverweis `[n]` wo belegt. Keine Superlative, kein „ab“-Preis.
- **Infokästen:** `meta.kb_ursache`, `kb_behandlung`, `kb_dauer`, `kb_kosten`, `kb_ablauf`. Nur befüllen, was die Faktenlage trägt, sonst leer lassen. `kb_geprueft` bleibt leer (setzt Alexander).
- **Bausteine im Text** (Gutenberg-Blöcke mit CSS-Klasse): `kb-merksatz`, `kb-hinweis` („Gut zu wissen:“), `kb-schritte` (nummerierte Liste), `kb-vergleich` (Tabelle), `kb-faq` (details), `kb-cta` (ohne Preis- oder Dringlichkeitsaussage), `kb-quellen` (details „Quellen“, nummeriert, am Ende).
- **Quellen:** Zitate im Text als `[n]`. Vorzug: Leitlinien, systematische Übersichten, Verbraucherzentralen. Anbieterseiten und Vergleichsportale nicht als Beleg. Unsichere Fundstellen markieren.
- Lücken bleiben als `[FAKT FEHLT: …]` sichtbar, auch im WordPress-Entwurf.
