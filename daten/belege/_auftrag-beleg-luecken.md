# Auftrag: Beleg-Lücken aus dem Backlog schließen

Du schließt offene `[beleg]`-Zeilen in `daten/backlog.md` für ein Themenpaket. Die Zeilen siehst du mit `python3 .claude/skills/seo-pipeline/scripts/backlog.py list beleg`; deine Zeilen nennt der Prompt über Stichworte.

## Vorgehen je Lücke
1. Lies das betroffene Faktenblatt (`daten/belege/<thema>-web.md`, Quellen S.., Aussagen B..) und prüfe, ob die Lücke dort inzwischen gedeckt ist (dann nur schließen).
2. Suche gezielt: OpenAlex/PubMed (Tools des Agenten) für klinische Fragen; für Preise, Kasse, Steuer, Verbraucherinformation seriöse Drittquellen (Verbraucherzentrale, Krankenkassen, Bundeszahnärztekammer/KZBV, G-BA, BMF/Finanzverwaltung, Fachgesellschaften, zm-online). Keine Praxis-/Anbieterseiten, keine Foren, keine Ratgeber-Portale mit Werbecharakter.
3. Ergänze das Faktenblatt im vorhandenen Format (Quelle `S` nächste freie Nummer, Aussage `B` nächste freie Nummer, Spalte Formulierung vorsichtig, Einschränkung ehrlich). Euro-Beträge nur mit mindestens zwei unabhängigen Quellen oder klar als Einzelquelle gekennzeichnet in der Spalte Einschränkung (Artikel nutzen Einzelquellen-Beträge nicht). Keine Zahlen erfinden, keine Zahl aus dem Gedächtnis.
4. Danach `python3 .claude/skills/seo-pipeline/scripts/belege_check.py validate <thema>-web` (Fehler beheben).
5. Schließe die Backlog-Zeile mit `python3 .claude/skills/seo-pipeline/scripts/backlog.py schliessen "<Stichwort aus der Zeile>" "<Ergebnis mit Beleg-ID, z. B. B75/S36>" <status>`:
   - `belegt`: Beleg gefunden und im Faktenblatt eingetragen.
   - `offen`: ernsthaft recherchiert, kein belastbarer Beleg gefunden (ein Satz, wo gesucht wurde).
   - `alexander`: nur Praxiswissen von Alexander möglich (z. B. Dauer in der Praxis, Eingewöhnung, Praxispreis); zusätzlich `backlog.py add praxis <slug> "<konkrete Frage an Alexander>"`.

## Regeln
- Nur Faktenblatt und Backlog ändern, nie Artikel unter `daten/entwuerfe/`.
- Gleichartige Lücken in verschiedenen Zeilen mit einem Beleg abdecken und alle Zeilen schließen.
- Kein Heilversprechen, keine Rechtsberatung; Kasse/Steuer nur allgemein und mit Vorbehalt formulieren.
- Bericht höchstens 40 Wörter: Anzahl belegt / offen / alexander, neue Beleg-IDs.
