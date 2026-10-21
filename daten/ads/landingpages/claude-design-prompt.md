# Prompt für Claude Design: Anzeigen-Landingpages Kieferblick
Vorgehen: Zuerst den **Master-Prompt** einfügen (einmal je Projekt/Chat), danach je Seite den passenden **Seiten-Abschnitt** (A bis E). Wenn du eine bestehende Seite anpassen willst, hänge deren HTML oder Screenshot an und ergänze am Ende: „Übernimm Look und Feel der angehängten Seite, ersetze aber Struktur und Inhalt vollständig nach Vorgabe.“ Neu bauen: einfach ohne Anhang senden.

---

## MASTER-PROMPT

**Aufgabe.** Gestalte und liefere eine Landingpage für Google-Anzeigen der Zahnarztpraxis „Kieferblick · ZAHNBOUTIQUE“ (Mülheim an der Ruhr, reine Privatpraxis). Die Seite soll genau eine Handlung auslösen: den Termin-Button (oder den Anruf). Besucher kommen von einer Suchanzeige, sind kurz vor der Entscheidung und prüfen Vertrauen, Preis und Ablauf. Die Seite wird später als HTML in WordPress (Elementor/Plugin) eingebaut.

**Stil.** Nutze das Design „Wissen-Artikel“ dieses Projekts als Grundlage (gleiche Schriften, Farben, Karten, Buttons, dunkles Band). Falls nicht verfügbar: Hintergrund Creme #F4EFE4, Text #14302A, Marke Tannengrün #1F4A3F, Akzent Safran #E3A93F (nur Punkte, Linien, kleine Akzente), Fläche Sand #EBE2D3, Karte #FBF8F1, Salbei #B9CFC2; Überschriften Fraunces (400), Text DM Sans (400/500), selbst gehostet, keine Google-Fonts-Links. Ruhig, skandinavisch-reduziert, viel Weißraum, feine Linien, keine Schatten, keine Verläufe, kein Klinikblau, kein Neon, keine Emojis, keine Stockfoto-Posen, kein Pop-up. Heller und dunkler Modus wie im Artikel-Design.

**Aufbau (von oben nach unten, immer in dieser Reihenfolge, Blöcke ohne Inhalt weglassen):**
1. **Kopf:** Logo links, rechts Telefon (0208 30 99 88 0, antippbar) und ein Button. Keine Hauptnavigation, keine Links weg von der Seite außer Impressum/Datenschutz im Fuß.
2. **Hero:** kleine Zeile (Eyebrow), H1, ein Satz Unterzeile, **ein** Haupt-Button, darunter Fakten-Leiste (3 bis 4 Kurzfakten mit Safran-Punkt), rechts/darunter Video-Platzhalter (16:9, Beschriftung „[VIDEO: Alexander Andreev, ca. 90 Sekunden]“). Auf dem Handy ist der Button ohne Scrollen sichtbar.
3. **Vertrauensleiste:** Autorenkarte (Foto-Platzhalter „[FOTO ALEXANDER]“, „Alexander Andreev, Zahnarzt“, ein Satz) und Platz „[GOOGLE-BEWERTUNG: nur einsetzen, wenn echt und belegbar]“.
4. **Inhaltsblöcke** laut Seiten-Abschnitt (Karten, Schritte, Tabelle, Hinweiskasten).
5. **Zusagen** (3 Karten).
6. **FAQ** als `<details>`-Akkordeon (ohne JavaScript).
7. **Abschluss-Block:** dunkles Band mit Überschrift, Button, Telefon und Formular-Platzhalter.
8. **Fuß:** Adresse (Leineweberstr. 72, 45468 Mülheim an der Ruhr), Telefon, Impressum, Datenschutz, „Einwilligung ändern“.
Auf dem Handy zusätzlich eine **feste untere Leiste** mit zwei Buttons: [Haupt-CTA] | [Anrufen]. Nach jedem Beweisblock wiederholt sich der Haupt-Button (Textlink oder Button).

**Texte.** Verwende **nur** die Texte aus dem Seiten-Abschnitt. Erfinde keine Zahlen, Preise, Bewertungen, Fälle, Namen oder Zitate. Wo etwas fehlt, setze einen sichtbaren Platzhalter in eckigen Klammern. Sie-Form; die Praxis spricht „Wir“; Alexander Andreev in der dritten Person. Kurze Sätze, keine Ausrufezeichen. Nutzen vor Merkmal. **Verboten:** Garantie (stattdessen „Zusage“), Rabatt, Aktion, Dringlichkeit, Superlative („beste“, „führend“), „Luxus“, „unsichtbar“ (stattdessen „diskret“), Ergebnis- und Heilversprechen (z. B. „ohne Kieferknacken“, „schmerzfrei“), Vorher-nachher-Bilder, Namen von Wettbewerbern, Aussagen über Kasse oder Erstattung (nötigenfalls nur: „Wir sind eine reine Privatpraxis.“), die Bezeichnung „Kieferorthopäde“ oder „Fachzahnarzt“.

**Technik und Ausgabe.** Liefere (a) das Markup als **HTML-Fragment** (kein `<html>`/`<body>`, kein JavaScript außer, wenn zwingend, für nichts), (b) das CSS als **eine Datei `lp.css`** mit dem Präfix `.kb-lp-*` (Layout, Karten, Hero, Leisten) und den bestehenden Variablen des Artikel-Designs, (c) responsive von 360 px bis 1440 px, Mobil zuerst, (d) semantisches HTML, genau eine H1, H2 für Abschnitte, Kontrast mindestens 4,5:1, Buttons mindestens 48 px hoch, sichtbarer Fokus, Alt-Texte, (e) keine externen Bibliotheken, keine CDN-Links, keine Tracking-Skripte, (f) Platzhalter für Tally: `<div class="kb-lp-form" data-tally-produkt="…" data-hidden-fields="quelle,gruppe,gclid,seite,produkt"></div>`, (g) Buttons als `<a class="kb-lp-btn" href="#termin">` zum Formular-Anker `#termin`, Telefon als `tel:+49208309988​0`-Link ohne Leerzeichen, (h) Bilder als Platzhalter-Boxen mit Seitenverhältnis, nicht als Dateien. Zeige mir **Handy- und Desktop-Ansicht** und liste am Ende alle Platzhalter und alle Stellen, an denen ich Inhalt prüfen muss.

**Prüfe vor der Abgabe:** Steht jede Aussage der Anzeige auf der Seite? Gibt es nur einen Haupt-Button? Sind alle verbotenen Wörter draußen? Lädt nichts von außen?

---

## SEITE A · Aligner (Zone 1, Erstberatung)
**Slug/Ziel:** `/erstermin-aligner/` · Haupt-CTA **„Ersttermin online buchen“** (Anker `#termin`), zweiter CTA „Anrufen“ · Tally `produkt=aligner`.
**Eyebrow:** Aligner in Mülheim an der Ruhr · **H1:** Schön lächeln. Gut zubeißen. 
**Unterzeile (Standard, Gruppe „Behandler“):** Ein Arzt plant Ihre Behandlung und begleitet Sie bis zum Retainer. Wir planen Zähne, Kiefer und Biss zusammen.
*Alternative Unterzeilen als HTML-Kommentar darunter anlegen (später je Anzeigengruppe):* Erwachsene: „Aligner sind herausnehmbar und diskret. Wir erklären ehrlich, was Sie dafür tun müssen.“ · Kosten: „Festpreis schriftlich vorab. Der Preis im Plan bleibt gleich, Mehrkosten nur mit Ihrer Zustimmung.“ · Marke: „Welches System passt, entscheidet der Befund. Wir erklären den Weg ehrlich und ohne Druck.“ · Erfahrungen: „Fragen, die Sie jedem Anbieter stellen sollten: Wer plant? Wer ist danach zuständig? Wird der Biss geprüft?“
**Fakten-Leiste:** Ersttermin etwa 60 Minuten · Dauer meist 6 bis 12 Monate · Tragezeit etwa 22 Stunden · Reine Privatpraxis.
**Vertrauen:** „Alexander Andreev, Zahnarzt. Er plant Ihre Behandlung und begleitet Sie bis zum Retainer.“ [Qualifikationssatz: Alexander ergänzt]
**Block „Darum planen wir anders“ (3 Karten, jede: Merkmal, damit Nutzen):**
1. Biss-Check vor der Planung. Wir prüfen Zähne, Kiefergelenk und Kaumuskeln, damit ein schönes Lächeln nicht auf Kosten des Bisses geht.
2. Scan in der Praxis, ohne Abdruckmasse. Das geht in Minuten und ist die genaue Grundlage für Ihren Plan.
3. Die Halteschiene gehört zum Plan: zwei lose Retainer je Kiefer. So ist auch nach der Behandlung jemand für Sie zuständig.
**Block „Ihr Weg“ (3 Schritte):**
1. Ersttermin (etwa 60 Minuten): 3D-Scan, Foto- und Bissanalyse, Kiefergelenk-Check, Smile-Simulation am Bildschirm.
2. Ihr Plan: Sie nehmen ihn mit nach Hause und dürfen ihn jedem anderen Zahnarzt zeigen. Sie können auch gleich im Ersttermin starten. Beides ist in Ordnung.
3. Behandlung und Begleitung bis zum Retainer: regelmäßiger Schienenwechsel, Halbzeit-Check am Bildschirm, danach Kontrolle der Stellung.
**Hinweiskasten „Ehrlich vorab“:** Aligner trägt man etwa 22 Stunden am Tag und nimmt sie zum Essen heraus. Nicht jede Fehlstellung lässt sich mit Alignern behandeln. Das sagen wir Ihnen im Ersttermin offen.
**Tabelle „Fragen, die Sie jedem Anbieter stellen sollten“ (zwei Spalten: Frage | Bei uns, **keine** Wettbewerber-Spalte):** Wer plant meine Behandlung? | Alexander Andreev, persönlich · Wer ist danach für mich zuständig? | Dieselbe Person, auch nach der Behandlung · Wird mein Biss vor der Planung geprüft? | Ja · Scan oder Abdruck? | Scan in der Praxis · Gehört die Halteschiene zum Plan? | Ja · Darf ich den Plan prüfen lassen? | Ja
**Optionaler Block (Klasse `kb-lp-optional`, im Markup vorhanden, standardmäßig ausgeblendet; ich schalte ihn für einen Test ein):** „Ersttermin im Wert von 300 €, für Sie kostenlos“: 3D-Scan 64 € · Foto- und Bissanalyse 70 € · Kiefergelenk-Check 75 € · Ergebnis vorab mit Smile-Simulation und 10 Minuten mit Alexander Andreev 91 €. Dazu: Ihr Festpreis schriftlich.
**Zusagen (3 Karten):** Ein Mensch, der sich kümmert: ein fester Arzt und Ansprechpartner. · Ein Plan, der klar ist: Weg, Dauer und Kosten vorab, Mehrkosten nur mit Ihrer Zustimmung. · Ein Festpreis: Der Preis im Plan bleibt bis zum Abschluss gleich. [Ausnahmen: Alexander bestätigt]
**FAQ (6):** Wie lange dauert die Behandlung? Meist 6 bis 12 Monate, je nach Fall. · Wie lange muss ich die Schienen tragen? Etwa 22 Stunden am Tag. · Was kostet das? Den Endpreis nennen wir nach der Untersuchung, schriftlich und mit allem, was enthalten ist. Der Preis im Plan bleibt bis zum Abschluss gleich. · Darf ich den Plan prüfen lassen? Ja, auch bei einem anderen Zahnarzt. · Gehört der Retainer zum Plan? Ja, zwei lose Retainer je Kiefer. · Passen Aligner bei mir? Das klären wir im Ersttermin ehrlich; nicht jede Fehlstellung eignet sich.
**Abschluss-Band:** „Erst Klarheit. Dann entscheiden.“ + Button „Ersttermin online buchen“ + Telefon + Formular-Platzhalter (Vorname, Telefon oder E-Mail, Wunschzeit optional, Hinweis zur Verarbeitung von Gesundheitsangaben).
**Nicht aufnehmen:** Smile-Check, „Rückruf in 10 Minuten“, Plan-Preise, Bewertungszahlen, Vorher-nachher.
**Platzhalter, die ich später fülle:** Video, Foto, Qualifikationssatz, Google-Bewertung, Name des Aligner-Systems [nur für Marke-Gruppe].

---

## SEITE B · Bleaching (Intro-Offer)
**Slug/Ziel:** `/bleaching-zahnreinigung/` · Haupt-CTA **„Bleaching-Termin buchen“** · Tally `produkt=bleaching`.
**Eyebrow:** Bleaching und Zahnreinigung in Mülheim an der Ruhr · **H1:** Bleaching beim Zahnarzt: erst Reinigung, dann Bleaching.
**Unterzeile:** Vorher prüfen wir, ob Ihre Zähne bereit sind. Preise offen, Betrag auf Aligner voll angerechnet.
**Fakten-Leiste:** Befund und Beratung etwa 60 Minuten · Bleaching 1 bis 2 Termine · Bleaching in der Praxis oder zu Hause mit individueller Schiene · Reine Privatpraxis.
**Preisblock direkt unter dem Hero (3 Karten):** Professionelle Zahnreinigung **149 €** · Bleaching in der Praxis **399 €** · Bleaching für zu Hause **299 €** (mit individueller Schiene). Darunter: „Entscheiden Sie sich später für Aligner, rechnen wir den Betrag voll an. Ohne Frist.“
**Warum diese Reihenfolge (2 Sätze + Liste):** Wir bleachen erst, wenn Zähne und Zahnfleisch dafür bereit sind. Wir prüfen: Karies und Füllungen, entzündetes Zahnfleisch, freiliegende Zahnhälse, Art der Verfärbung.
**Ablauf (4 Schritte):** Befund und Beratung · Professionelle Zahnreinigung · Bleaching (Praxis oder zu Hause) · Kontrolle.
**Hinweiskasten „Ehrlich zuerst“:** Zähne können während und nach dem Bleaching empfindlich auf Kaltes reagieren; wir prüfen das vorab und sprechen es offen an. Die Farbe kann mit der Zeit nachlassen. Füllungen, Kronen und Veneers hellen nicht auf. Manchmal hilft schon die Zahnreinigung.
**Wer behandelt:** Bleaching mit wirksamer Konzentration darf nur ein Zahnarzt durchführen. [Alexander bestätigt: führt er selbst durch oder leitet er an]
**FAQ (5):** Schadet Bleaching meinen Zähnen? (Bei gesunden Zähnen und fachgerechter Durchführung greift es den Zahn nicht an; manche Zähne reagieren vorübergehend empfindlich; wir prüfen vorher.) · Wie lange hält das Ergebnis? (Von Mensch zu Mensch verschieden, abhängig von Ernährung, Rauchen und Pflege; wir besprechen eine Auffrischung.) · Brauche ich vorher eine Zahnreinigung? (Wir empfehlen sie als ersten Schritt.) · Praxis oder zu Hause? (Je nach Befund und Wunsch; zu Hause mit individueller Schiene.) · Was ist im Preis enthalten? (Wir erklären es vorab; Mehrkosten nur mit Ihrer Zustimmung.)
**Nicht aufnehmen:** Aligner-Ablauf („Ihr Lächeln am Bildschirm“), „kostenlos“, Fälle, Bewertungszahlen.

## SEITE C · Schnarchschiene
**Slug/Ziel:** `/erstermin-schnarchschiene/` · Haupt-CTA **„Termin online anfragen“** · Tally `produkt=schnarchschiene` · **Gesundheitswerbung: keine Wirkversprechen.**
**Eyebrow:** Schnarchschiene in Mülheim an der Ruhr · **H1:** Schnarchen ernst nehmen. Erst klären, dann behandeln.
**Unterzeile:** Wir klären zuerst die Ursache, dann, ob eine Schiene zu Ihnen passt.
**Fakten-Leiste:** Screening auf mögliche Schlafapnoe vorab · Individuell angefertigt · Paket mit Kontrollen · Reine Privatpraxis.
**Ablauf (4 Schritte):** 1 Gespräch und Screening (Schlaf, Tagesmüdigkeit, beobachtete Atempausen). 2 Bei Auffälligkeiten raten wir zuerst zur Abklärung in der Schlafmedizin. 3 Wenn eine Schiene passt: individuell angefertigt; vorher prüfen wir Zähne und Biss. 4 Wir begleiten die Eingewöhnung mit Kontrollen.
**Preisblock:** Schnarchschiene als Paket mit Kontrollen: **799 €**. Entscheiden Sie sich später für Aligner, rechnen wir den Betrag voll an. Ohne Frist. [Screening vorab: im Paket oder getrennt? Alexander bestätigt]
**Begriff:** „Protrusionsschiene“ (auch „Unterkieferprotrusionsschiene“) ist der Fachbegriff für eine individuell angefertigte Schiene für die Nacht. [Alexander prüft Wortlaut]
**FAQ (4):** Wie finde ich heraus, ob mein Schnarchen harmlos ist? (Im Ersttermin fragen wir nach Schlaf, Tagesmüdigkeit und beobachteten Atempausen; bei Auffälligkeiten verweisen wir in die Schlafmedizin.) · Was ist, wenn ich eine Schlafapnoe habe? (Dann kommt zuerst die schlafmedizinische Abklärung; ob eine Schiene Teil der Behandlung sein kann, entscheidet sich danach.) · Wie läuft die Eingewöhnung? (Wir begleiten sie mit Kontrollen.) · Lässt sich die Schiene mit einer Aligner-Behandlung kombinieren? (Das stimmen wir im Einzelfall ab.)
**Nicht aufnehmen:** Wirksamkeits- oder Erfolgsaussagen, „stoppt/beseitigt Schnarchen“, Dauerangaben zur Eingewöhnung, Aligner-Ablauf.

## SEITE D · Veneers (Test; erst live, wenn Seite angepasst)
**Slug/Ziel:** `/veneers/` · Haupt-CTA **„Ersttermin online buchen“** · Tally `produkt=veneers` · **keine Preise, keine Vorher-nachher-Bilder.**
**Eyebrow:** Veneers in Mülheim an der Ruhr · **H1:** Veneers beim Zahnarzt: erst das Schonendere prüfen.
**Unterzeile:** Veneers verändern Form, Länge und Farbe. Wir prüfen zuerst, ob Schonenderes reicht.
**Fakten-Leiste:** Mock-up zum Probetragen · Biss-Check vor der Formkorrektur · Komposit oder Keramik · Reine Privatpraxis.
**Blöcke:** (1) „Zuerst der Biss, dann die Form“: Vor der Formkorrektur prüfen wir Zähne, Kiefergelenk und Kaumuskeln, weil ein ungünstiger Biss Veneers stark belasten kann. (2) „Sie sehen Ihr Lächeln, bevor etwas entschieden wird“: Smile-Simulation am Bildschirm; die Form lässt sich als Mock-up aus Kunststoff probetragen; wir passen an, bis sie zu Ihnen passt. (3) Tabelle „Material“ (Zeilen: Eingriff, passt bei): Komposit: Abtrag nach Befund; passt bei kleinen Korrekturen, Kanten, Lücken, zum Probieren. Keramik: Zahnschmelz wird meist abgetragen und lässt sich nicht rückgängig machen; passt bei größeren Veränderungen von Form und Farbe. [Haltbarkeitsangaben nur nach Bestätigung durch Alexander] (4) Hinweiskasten „Ehrlich“: Wir sagen, wann eine schonendere Lösung reicht. Wir sagen auch, wann Veneers nicht passen.
**Kosten:** keine Zahl. Satz: „Den Rahmen nennen wir nach der Untersuchung, schriftlich.“ [Alexander bestätigt]
**FAQ (4):** Muss Zahnschmelz abgetragen werden? (Bei Keramik meist ja, bei Komposit nach Befund.) · Was ist ein Mock-up? · Wie läuft es ab? [Termine/Dauer: Alexander] · Passen Veneers zu mir? (Das klären wir im Ersttermin ehrlich.)
**Nicht aufnehmen:** Non-Prep, „immer das Schonendste“, „natürlich, nicht überweiß“, Preise, Fälle.

## SEITE E · Professionelle Zahnreinigung
**Slug/Ziel:** neue schlanke Seite (z. B. `/professionelle-zahnreinigung/`) · Haupt-CTA **„Termin online buchen“** · Tally `produkt=pzr`.
**Eyebrow:** Zahnarztpraxis in Mülheim an der Ruhr · **H1:** Professionelle Zahnreinigung in Mülheim an der Ruhr.
**Unterzeile:** Festpreis 149 €. Auf eine spätere Aligner-Behandlung voll angerechnet.
**Fakten-Leiste:** Festpreis 149 € · Reine Privatpraxis · Zahnarztpraxis · [Dauer: Alexander bestätigt, Seite nennt 60 und 90 Minuten].
**Blöcke:** (1) „Was wir tun“: Beläge, Zahnstein und oberflächliche Verfärbungen entfernen, danach polieren. (2) „Ablauf“ in 3 Schritten: Befund · Reinigung · Politur und Pflegehinweise. (3) Preiskarte: Professionelle Zahnreinigung 149 €. „Entscheiden Sie sich später für Aligner, rechnen wir den Betrag voll an. Ohne Frist.“ (4) Hinweiskasten „Gut zu wissen“: Wir sind eine reine Privatpraxis. (5) „Danach“: Nach dem Aligner-Start gibt es das PZR-Abo mit zwei Zahnreinigungen im Jahr (Link zur Mitgliedschaft, kein Preis auf dieser Seite).
**FAQ (4):** Wie lange dauert die Reinigung? [Alexander] · Was kostet sie? (149 €, Festpreis.) · Wird der Betrag angerechnet? (Auf eine spätere Aligner-Behandlung voll, ohne Frist.) · Brauche ich die Reinigung vor einem Bleaching? (Wir empfehlen sie als ersten Schritt.)
**Nicht aufnehmen:** Aussagen zu Kasse und Zuschüssen, „gründlichste“, Ergebnisversprechen, Abo-Preis.
