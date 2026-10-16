# Recherche für Artikel (PubMed und OpenAlex)

Der Writer füllt Faktenlücken zuerst selbst, bevor er `[FAKT FEHLT]` setzt. Reihenfolge:

1. **Eigene Quellen:** `material/fakten.md`, `kontext/angebot-und-preise.md`. Was Alexander oder die Praxis betrifft (Erfahrung, Zahlen aus der Praxis, Haltung, Preise, Abläufe), recherchiert man nicht: fehlt es dort, bleibt `[FAKT FEHLT]`.
2. **Medizinische Aussagen** (Ursachen, Häufigkeiten, Zeiträume, Wirksamkeit, Risiken) recherchierst du:
   - PubMed: `python3 .claude/skills/seo-pipeline/scripts/pubmed.py suche "<englische Anfrage>" --typ leitlinie|review|studie --ab 2015 --n 8`, danach `pubmed.py abstract <PMID>`.
   - OpenAlex (Zitationen, Leitlinien, Abdeckung prüfen): die Tools `search_works`, `get_work`, `resolve_references` des OpenAlex-Connectors. Direkte Aufrufe von api.openalex.org gehen nicht (Ratenlimit ohne Schlüssel).
   - Anfragen auf Englisch, mit Fachbegriffen (z. B. „orthodontic retention relapse timing“, „retainer failure prevalence“).
3. **Rangfolge der Quellen:** Leitlinie (BOS, DGKFO, NICE, S3) > Cochrane/systematische Übersicht > Metaanalyse > randomisierte Studie > Kohortenstudie > Expertenmeinung. Gesetze und Verbraucherzentrale für Kasse/Kosten. Keine Blogs, keine Praxis- oder Herstellerseiten als Beleg für Medizin.
4. **Verarbeitung:** Nur was im Abstract oder Volltext steht. Zahl, Population und Einschränkung (Spange vs. Aligner, Unterkiefer, Alter) mitnehmen. Passt die Quelle nicht auf Aligner oder auf Erwachsene, steht das in einem kurzen Satz. Nie aus dem Gedächtnis zitieren. Findet sich nichts Brauchbares: `[FAKT FEHLT]`, ehrlich.
5. **Zahlen gegenprüfen:** Abstract-Zahlen und Zahlen aus bestehenden Entwürfen vergleichen. Weichen sie ab (z. B. andere Analyse, Ausschluss von Studien mit hohem Risiko), die Fassung nehmen, die du belegen kannst, und im Bericht melden.
6. **Weniger Quellen:** Eine starke Quelle (z. B. eine Leitlinie) darf mehrere Aussagen tragen und ohne DOI/PMID mit URL zitiert werden. Pro Artikel höchstens **6** Quellen, bevorzugt 3–5. Pro Aussage die eine stärkste Quelle, nicht drei. Zweitbelege nur, wenn sie der Hauptquelle widersprechen. Im Text höchstens **eine** Quellenklammer pro Absatz, und nur an Zahlen und starken Aussagen. Quellenangaben stehen in der Quellenbox mit DOI oder PMID.
7. **Bericht an den Aufrufer:** Welche Lücken du gefüllt hast (mit PMID/DOI), welche offen bleiben und warum, und Auffälligkeiten (abweichende Zahlen, widersprüchliche Quellen).

## Praxiserfahrung aus dem Test (16.10.2026)
- **PubMed-Suche:** kurze, breite Anfragen mit 2–4 Stichwörtern, ohne `--typ`; lange Mehrbegriff-Anfragen und `--typ review` liefern oft „Keine Treffer“. Dann erst mit `--typ` eingrenzen. `abstract <PMID>` funktioniert zuverlässig.
- **OpenAlex:** `search_works` (semantisch) findet Treffer, die PubMed übersieht; `resolve_references` bestätigt PMIDs/DOIs. Die Tools erst mit ToolSearch laden („select:…“). Nur Abstracts, kein Volltext.
- **Volltext:** über Europe PMC per curl (`https://www.ebi.ac.uk/europepmc/webservices/rest/<PMCID>/fullTextXML`), wenn der Abstract für eine Zahl nicht reicht.
- **Leitlinien** (BOS, DGKFO, NICE) gezielt suchen; PubMed/OpenAlex finden sie schlecht.
- **Hauptanalyse zitieren:** Zahlen aus der im Abstract hervorgehobenen Hauptanalyse, nicht aus Nebenanalysen. Zeitangaben so wie im Paper (nicht rundend umetikettieren).
- **Messgröße nicht verwechseln:** „Failure“ eines Retainers (Ablösen, Bruch, Verlust) ist nicht „Rückfall der Zähne“. Beides getrennt formulieren.
- **Schwache Evidenz in einem Satz sagen** (z. B. „sehr unsichere Datenlage“), Details bleiben in der Quellenbox.
- **Anzeichen und Patientenwahrnehmung:** dazu gibt es kaum Studien. Das ist Praxiswissen von Alexander: `[FAKT FEHLT]`, nicht erfinden.
