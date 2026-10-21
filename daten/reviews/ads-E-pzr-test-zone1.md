AMPEL: gelb
BEFUNDE:
- [gelb, wichtig] Beschreibung "Mit dem PZR-Abo haben Sie zwei Zahnreinigungen im Jahr zu festen Terminen." – Das PZR-Abo startet laut angebot-und-preise.md erst im Abschlusstermin (Bindung nach dem Ja) und ist für PZR-Suchende nicht buchbar. Auf der Landingpage (Bleaching und Zahnreinigung) steht es vermutlich nicht, Preis nur auf /mitgliedschaft/. "Festen Terminen" steht in keiner Faktenquelle. Anzeige verspricht mehr, als die Seite hält. Vorschlag: Bezug zu Aligner-Patienten herstellen, Terminzusage streichen.
- [gelb, wichtig] Überschrift "PZR-Abo: zwei Reinigungen" (beide Gruppen) – ohne Preis und ohne Bezug klingt es wie ein Angebot für jeden Suchenden; gleiche Passungslücke wie oben. Zulässigkeit (Prophylaxe-Mitgliedschaft, GOZ 1040) ist laut recht.md geklärt, kein Rechtsbefund.
- [gelb, wichtig] Überschrift "Mit Befund beim Zahnarzt" (beide Gruppen) – In fakten.md steht kein Befund bei der PZR; der Befund gehört zur Erstberatung. Behandlungsaussage ohne Praxis-Eintrag. Auch "Zahnarzt vor Ort" lässt offen, wer reinigt. Vorschlag: neutral "Zahnarztpraxis".
- [gelb, klein] Beschreibung "Zahnreinigung für 149 €. Entscheiden Sie sich später für Aligner, rechnen wir sie voll an." – Preis 149 € und "voll, ohne Frist" stimmen mit angebot-und-preise.md (Intro-Offers) überein. Wortlaut der Seite ist "den Betrag voll an"; "sie" bleibt unklar. Ersatz gleich lang, an die Seite angeglichen.
- [gelb, klein] Überschrift "Voll angerechnet, ohne Frist" – korrekt, aber allein ohne Bezug (angerechnet worauf?). Kürzere Ersatzform nennt den Plan; "ohne Frist" steht weiter in der Beschreibung der Seite. Nur sinnvoll, wenn Alexander "ohne Frist" in der Überschrift nicht braucht.
- [gelb, klein] Überschrift "Bis in die Zwischenräume" (beide Gruppen) – Qualitätsversprechen ohne Beleg in fakten.md, Ergebnisklang. Vorschlag: Tätigkeit statt Ergebnis.
- [gelb, klein] Überschrift "Beläge und Zahnstein entfernt" – Partizip klingt wie zugesichertes Ergebnis. Vorschlag: Tätigkeit im Infinitiv.
- [gelb, klein] Beschreibung "Wir entfernen Beläge, Zahnstein und Verfärbungen und polieren danach. Zahnarzt vor Ort." (Gruppe 1) und "…und polieren danach." (Gruppe 2) – "Verfärbungen" kann als Aufhellung gelesen werden (Bleaching ist ein eigenes Angebot, fakten.md). "Zähne werden poliert" ist als Vorgang ok, kein Befund.
- [gelb, klein] Negativliste – Lücken: "pulver", "versicherung", "zusatzversicherung", "hausbesuch" fehlen (Suchende nach Erstattung oder Hausmitteln, passen nicht zu 149 € Privatleistung). Konflikte mit den Keywords gibt es nicht. "kasse" bleibt sinnvoll; "günstig" ebenfalls, weil der Festpreis nicht über den Preis wirbt.
PATCHES:
- ALT: "Zahnreinigung für 149 €. Entscheiden Sie sich später für Aligner, rechnen wir sie voll an.",
  NEU: "Zahnreinigung für 149 €. Wählen Sie später Aligner, rechnen wir den Betrag voll an.",
  (Zeile kommt in beiden Gruppen vor; in beiden ersetzen)
- ALT: "Mit dem PZR-Abo haben Sie zwei Zahnreinigungen im Jahr zu festen Terminen.",
  NEU: "Nach dem Aligner-Start gibt es das PZR-Abo mit zwei Zahnreinigungen im Jahr.",
- ALT: "PZR-Abo: zwei Reinigungen",
  NEU: "PZR-Abo für Aligner-Patienten",
  (beide Gruppen)
- ALT: "Mit Befund beim Zahnarzt",
  NEU: "Zahnarztpraxis in Mülheim",
  (beide Gruppen; in Gruppe 2 steht Mülheim schon in anderen Überschriften, dann alternativ "Zahnarztpraxis, Privat")
- ALT: "Voll angerechnet, ohne Frist",
  NEU: "Auf Aligner voll angerechnet",
  (beide Gruppen)
- ALT: "Bis in die Zwischenräume",
  NEU: "Auch an den Zwischenräumen",
  (beide Gruppen)
- ALT: "Beläge und Zahnstein entfernt",
  NEU: "Beläge und Zahnstein entfernen",
- ALT: "Wir entfernen Beläge, Zahnstein und Verfärbungen und polieren danach. Zahnarzt vor Ort.",
  NEU: "Wir entfernen Beläge, Zahnstein und oberflächliche Verfärbungen und polieren die Zähne.",
- ALT: "Wir entfernen Beläge, Zahnstein und Verfärbungen und polieren danach.",
  NEU: "Wir entfernen Beläge, Zahnstein und oberflächliche Verfärbungen. Danach polieren wir.",
OFFEN (kein Patch möglich):
- Negativliste ergänzen um "pulver", "versicherung", "zusatzversicherung", "hausbesuch" (Listeneinträge, keine einzeilige Ersetzung).
- Passung Landingpage: Die Seite /bleaching-zahnreinigung/ muss "149 €" und "voll angerechnet, ohne Frist" im Wortlaut tragen und PZR-Abo erwähnen (oder die Abo-Zeilen bleiben bei obigem Ersatz). Im Skriptlauf nicht prüfbar; vor Livegang gegenlesen.
ANNAHMEN (nicht blockierend):
- Preis 149 € und "voll angerechnet, ohne Frist" in Anzeigen: als freigegeben angenommen, weil es dem Website-Wortlaut und den Intro-Offers entspricht (Alexander bestätigt mit dem Wortlaut).
- PZR-Abo ohne Preis in der Anzeige: konservativ als Aligner-Folgeangebot erwähnt; wer es streichen will, ersetzt die Beschreibung durch "Reine Privatpraxis in Mülheim an der Ruhr. Termin online buchen."
- "Termin online buchen": Annahme, dass die Seite eine Online-Buchung hat.
- Eigene PZR-Seite statt Bleaching-Seite bleibt Entscheidung von Alexander vor Livegang (laut Strategie Voraussetzung für E).
