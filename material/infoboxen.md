# Infoboxen je Produktgruppe (feste Kopf-Box der Artikel)

Stand 19.10.2026. Diese Werte sind **konstant**: Sie gelten für jeden Artikel der Kategorie und werden nicht neu generiert. `skelett.py` schreibt sie ins Frontmatter, `wp_publish.py` überschreibt die Theme-Felder (`kb_ursache`, `kb_behandlung`, `kb_dauer`, `kb_kosten`, `kb_ablauf`) mit ihnen. Autoren-Agenten ändern die Felder nicht. Änderungen nur hier, dann `python3 .claude/skills/seo-pipeline/scripts/infoboxen.py anwenden <slugs>` und `wp_publish.py --update <id>`.

Quellen: Aligner aus dem geprüften Pillar-Artikel `aligner`. Veneers aus `material/fakten.md` (Alexanders Einschätzung), `kontext/angebot-und-preise.md` (Preisrahmen pro Fall, keine Zahlen im Artikel) und dem Faktenblatt `daten/belege/veneers-web.md` (B1, B6). Alexander gibt die Texte frei.

Format: `## <kategorie>` (Kategorie-Slug aus dem Frontmatter) oder `## <kategorie>/<cluster>`, wenn eine Kategorie mehrere Produkte trägt (Feld `cluster` im Frontmatter; der genauere Schlüssel gewinnt). Darunter `- feld: Text` in einer Zeile. **`offen`** heißt: dazu liegt noch kein belegter Praxisfakt vor, das Feld bleibt leer bzw. der Autor schreibt es ohne Zahl; sobald Alexander den Text liefert, hier eintragen.

Produktgruppen = WordPress-Kategorien: aligner, veneers, retainer, bleaching-zahnreinigung (Bleaching und PZR getrennt über `cluster`), schnarchschiene, funktionsschiene. Einstiegsangebote (Smile-Check, Erstberatung) und Bindungsangebote (Retainer-Klub, PZR-Abo, Kombi) haben keine eigene Box; sie stehen in Artikeln nicht mit Preis (Regel 16.10.2026).

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

## retainer
- ursache: Ohne Halt neigen Zähne dazu, in die alte Stellung zurückzuwandern.
- behandlung: Ein fester Retainer (dünner Draht, von innen an die Frontzähne geklebt) und ein loser Retainer (herausnehmbare Schiene) halten die neue Stellung. Wir empfehlen oft beides zusammen.
- dauer: Der feste Retainer wirkt unabhängig von der Tragedauer. Ein loser Retainer hält im Durchschnitt 4 bis 6 Monate und muss meist erneuert werden.
- kosten: Der Preis hängt davon ab, ob fest oder lose. Den Festpreis nennen wir im Ersttermin. Geht ein von uns eingesetzter fester Retainer kaputt, ersetzen wir ihn innerhalb von 2 Jahren kostenfrei (Zusage).
- ablauf: Einsetzen, eine Kontrolle danach, dann Prüfung bei den halbjährlichen Reinigungen.

## bleaching-zahnreinigung/bleaching
- ursache: Beläge auf der Oberfläche oder Verfärbungen im Zahninneren.
- behandlung: Aufhellung mit Gel, in der Praxis oder zu Hause mit einer individuell angefertigten Schiene.
- dauer: In der Praxis 1 bis 2 Sitzungen, zu Hause mehrere Anwendungen mit der Schiene.
- kosten: Bleaching bei Kieferblick: 399 € in der Praxis, 299 € zu Hause.
- ablauf: Vorprüfung von Zustand und Empfindlichkeit, Zahnreinigung, dann Bleaching in der Praxis oder mit der Schiene zu Hause.

## bleaching-zahnreinigung/pzr
- ursache: offen
- behandlung: offen
- dauer: offen
- kosten: Professionelle Zahnreinigung bei Kieferblick: 149 €.
- ablauf: offen

## schnarchschiene
- ursache: offen
- behandlung: Eine Schiene für die Nacht. Die Abklärung vorab entscheidet, welche Variante passt.
- dauer: offen
- kosten: Schnarchschiene bei Kieferblick: 799 € als Paket mit Kontrollen.
- ablauf: Screening vorab (auch auf Schlafapnoe), Abklärung der Variante, Schiene, Kontrollen.

## funktionsschiene
Produkt geparkt, nur Vorrat. Es gibt keinen freigegebenen Preis (Hypothese 700 bis 900 €) und keine Praxisfakten.
- ursache: offen
- behandlung: offen
- dauer: offen
- kosten: offen
- ablauf: offen
