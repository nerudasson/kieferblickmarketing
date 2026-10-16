# Artikelstruktur

Stil, Bausteine und Markdown-Konventionen stehen in `stil-und-format.md` (verbindlich). Diese Datei legt Gliederung und Länge fest.

Frontmatter: title, slug, keyword, cluster, intent, autor (Alexander Andreev), meta_description (max. 155 Zeichen), status (entwurf), kurz, ursache, behandlung, dauer, kosten, ablauf.

1. Kurzfassung (`kurz`, 3 Sätze) und Einstieg: Antwort in den ersten zwei Sätzen
2. Gliederung mit H2 passend zur Suchabsicht (Fragen als H2 wo sinnvoll, in Julias Worten)
3. Merksatz
4. Was dagegen spricht / Nachteile ehrlich (Liste)
5. Kosten oder Ablauf konkret, wenn das Keyword danach fragt (nur Zahlen aus `kontext/angebot-und-preise.md`), bei Kosten und Vergleich als Tabelle
6. Wann ein Termin sinnvoll ist (Liste, ohne Druck, ohne Diagnose)
7. FAQ (3–5 Fragen, Antwort höchstens 3 Sätze)
8. CTA (ein Satz)
9. Quellen (nummeriert)
10. Autorenbox: Alexander Andreev, Kieferblick · ZAHNBOUTIQUE, Mülheim an der Ruhr

Länge nach Intent (Wörter ohne Quellen): Info 600–1.000, Kosten/Vergleich 900–1.400. Kürzer und klarer schlägt länger. Interne Links: 2–4 auf Artikel desselben Clusters, 1 auf die Leistungsseite.

Hürden vor Prüfung durch den compliance-reviewer: `scripts/lesbarkeit.py` meldet OK (Flesch ≥ 60, Satz- und Absatzlänge, Formatmix).
