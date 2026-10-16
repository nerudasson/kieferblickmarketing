# Schreibstil für Patienten-Artikel

Leitbild: Alexander erklärt es einer Patientin auf dem Behandlungsstuhl. Ruhig, freundlich, konkret. Ein Fünftklässler soll es verstehen. Ziel: Flesch-Reading-Ease (Amstad, deutsch) mindestens 65 und Wiener Sachtextformel (WSTF) höchstens 6 (Skript `lesbarkeit.py` misst beides).

## Regeln
- Antwort zuerst, dann der Grund. Ein bis zwei Sätze, dann erst Details.
- Ein Satz, ein Gedanke. Richtwert 8 bis 14 Wörter, nie über 20. Keine Schachtelsätze, kein Passiv, wo „wir“ oder „Sie“ geht.
- Alltagswörter. Ein Fachwort höchstens einmal, sofort erklärt: „Retainer (die Haltespange nach der Behandlung)“. Danach bleibt das Fachwort stehen, damit man es googeln kann.
- Bilder aus dem Alltag statt Fachsprache („Zähne sind wie ein Zaun in weichem Boden“). Höchstens ein Bild pro Abschnitt, es muss stimmen.
- Konkret statt abstrakt: Zahlen, Beispiele, „nachts, etwa 8 Stunden“ statt „regelmäßig“.
- Sie-Form. Ich-Form von Alexander nur bei seiner Haltung („Ich empfehle …“).
- Absätze 2 bis 4 Sätze. Zwischenüberschrift alle 100 bis 150 Wörter, am besten als Frage, wie Patienten sie stellen.
- Abwechslung: Fließtext, Aufzählung, Schritte, Tabelle, Merksatz. Kein Block aus Text länger als ein Bildschirm.

## Aus der Copywriting-Schule übernehmen (Jim Edwards und andere), ohne Druck
- Überschriften, die neugierig machen, weil sie eine echte Frage der Leserin stellen.
- Klarer Nutzen für die Leserin in ihren Worten, nicht in unseren.
- Kurze Aufzählungen mit je einem konkreten Vorteil oder Fakt.
- Ein klarer nächster Schritt am Ende, freundlich und freiwillig.

## Nicht tun
- Kein Druck, keine Dringlichkeit, keine Angst („Sonst …“), keine Übertreibung, keine Superlative, kein Ausrufezeichen.
- Keine rhetorischen Tricks, keine Clickbait-Überschriften, keine Versprechen.
- Nachteile ehrlich nennen.
- Nicht belehren. Auf Augenhöhe: „Das kennen viele.“

## SEO im Text (ohne Stopfen)
- Hauptkeyword in Titel, erster Absatz, einer Zwischenüberschrift, Meta-Beschreibung.
- Verwandte Keywords und Autocomplete-Begriffe aus dem SEO-Brief (`daten/briefs/<slug>.json`) dort einbauen, wo sie natürlich passen: als Zwischenüberschrift, im FAQ oder in einem Satz.
- Jede relevante Frage der Suchenden („Ähnliche Fragen“) bekommt einen eigenen Abschnitt oder FAQ-Eintrag mit Kurzantwort in 1 bis 2 Sätzen am Anfang.
- Fragen, die nichts mit dem Thema zu tun haben (z. B. Zahnspangenfarbe), weglassen.
- Schreibe für die Leserin zuerst, für Google danach.
