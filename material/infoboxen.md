# Infoboxen je Produktgruppe (feste Kopf-Box der Artikel)

Stand 19.10.2026. Diese Werte sind **konstant**: Sie gelten für jeden Artikel der Kategorie und werden nicht neu generiert. `skelett.py` schreibt sie ins Frontmatter, `wp_publish.py` überschreibt die Theme-Felder (`kb_ursache`, `kb_behandlung`, `kb_dauer`, `kb_kosten`, `kb_ablauf`) mit ihnen. Autoren-Agenten ändern die Felder nicht. Änderungen nur hier, dann `python3 .claude/skills/seo-pipeline/scripts/infoboxen.py anwenden <slugs>` und `wp_publish.py --update <id>`.

Quellen: Aligner aus dem geprüften Pillar-Artikel `aligner`. Veneers aus `material/fakten.md` (Alexanders Einschätzung), `kontext/angebot-und-preise.md` (Preisrahmen pro Fall, keine Zahlen im Artikel) und dem Faktenblatt `daten/belege/veneers-web.md` (B1, B6). Alexander gibt die Texte frei.

Format: `## <kategorie>` (Kategorie-Slug aus dem Frontmatter), darunter `- feld: Text` in einer Zeile.

## aligner
- ursache: Zähne stehen schief oder eng, weil im Kiefer der Platz fehlt oder Zähne gewandert sind.
- behandlung: Durchsichtige Schienen verschieben die Zähne in kleinen Schritten, danach halten Retainer die neue Stellung.
- dauer: Eine kleine Korrektur ist ab etwa 3 Monaten möglich, sonst meist 6 bis 12 Monate. Das hängt vom Einzelfall ab.
- kosten: Aligner-Behandlung ab ca. 3.900 € (kleine Korrektur, der Endpreis steht nach der Untersuchung fest).
- ablauf: Erstberatung, Untersuchung und 3D-Scan, Plan mit Kostenplan, Schienen im Wechsel, Halbzeit-Check, Retainer.

## veneers
- ursache: Veneers kommen in Frage, wenn Form und Farbe der Zähne verbessert werden sollen und die Fehlstellung nicht zu stark ist.
- behandlung: Dünne Schalen aus Keramik oder Komposit werden auf die Zahnvorderseite geklebt. Beim klassischen Veneer wird dafür Zahnschmelz abgetragen, das lässt sich nicht rückgängig machen.
- dauer: Die Behandlungsdauer ist kurz. Den Zeitplan legen wir nach der Untersuchung fest.
- kosten: Der Preis richtet sich nach dem Fall. Rahmen vorab im Smile-Check, Festpreis im Ersttermin.
- ablauf: Erstberatung und Untersuchung, virtuelle Planung mit Vorschau (Mock-up), Anpassung nach Ihren Wünschen, Einsetzen der Veneers, regelmäßige Kontrollen.

## Noch nicht hinterlegt
retainer, bleaching-zahnreinigung, schnarchschiene, funktionsschiene: bis dahin schreibt der Autor die Felder je Artikel (wie bisher).
