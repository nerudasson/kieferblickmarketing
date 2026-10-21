# Weg über die Google Ads API (geplant, Entscheidung Alexander 21.10.2026)
Alexander stellt die API später bereit. Dann legt der Agent Kampagnen direkt im Konto an, **pausiert** (= Entwurf), und Alexander gibt sie dort frei, indem er sie aktiviert. Bis dahin gilt der Weg über CSV und Google Ads Editor (SKILL.md, Schritt 5). Die Kampagnendatei (`daten/ads/kampagnen/<kampagne>.json`) bleibt in beiden Fällen die einzige Quelle.

## Was „Entwurf“ bedeutet
Search-Kampagnen haben über die API keinen eigenen Entwurfsstatus. Entwurf = Kampagne, Anzeigengruppen und Anzeigen im Status **PAUSED**. Pausierte Objekte schalten nicht und kosten nichts. Aktivieren ist die Freigabe und liegt allein bei Alexander. Der Agent setzt nie ENABLED.

## Was Alexander bereitstellt
Developer Token (Zugriffsebene klären: Test-/Basic-Zugriff), OAuth-Zugang (Client-ID, Client-Secret, Refresh-Token), Kunden-ID und bei Verwaltungskonto die Verwaltungs-ID. Nie im Chat oder im Repo. Als Umgebungsvariablen oder Network secrets der Cloud-Umgebung: `GOOGLE_ADS_DEVELOPER_TOKEN`, `GOOGLE_ADS_CLIENT_ID`, `GOOGLE_ADS_CLIENT_SECRET`, `GOOGLE_ADS_REFRESH_TOKEN`, `GOOGLE_ADS_CUSTOMER_ID`, `GOOGLE_ADS_LOGIN_CUSTOMER_ID` (optional). Die Netzwerkfreigabe der Umgebung muss `googleads.googleapis.com` und `oauth2.googleapis.com` erlauben (Umgebung bearbeiten, Allowed domains). Eine neue Sitzung übernimmt die Werte.

## Ablauf des Anlegens (Skript `anzeigen_push.py`, noch nicht gebaut)
1. Prüfung wie im Export (`anzeigen_check.py`), bei HART-Treffer Abbruch.
2. **Trockenlauf ist Standard:** zeigt, welche Objekte angelegt oder geändert würden. Angelegt wird nur mit `--anwenden`.
3. Reihenfolge: Tagesbudget → Kampagne (PAUSED, nur Suche, Suchpartner und Display aus, Sprache, Standorte „Präsenz“, Gebotsstrategie „Klicks maximieren“ mit Obergrenze) → Negativbegriffe → Anzeigengruppen (PAUSED) → Keywords (Exact/Phrase) → responsive Suchanzeige (PAUSED, Überschrift 1 fest auf Position 1) → Erweiterungen.
4. Jedes angelegte Objekt bekommt das Label `kb-agent`. Idempotenz: eine Kampagne gleichen Namens wird nicht doppelt angelegt; geändert werden nur Objekte mit Label `kb-agent`, die noch PAUSED sind.
5. Protokoll nach `daten/ads/api-log.md` (Datum, Objekt, Ergebnis).

## Leitplanken
- Nie ENABLED setzen, nie Budget über den Deckel (`config/budget.json`), nie Gebote über `references/obergrenzen.json`, kein gemeinsames Budget, höchstens ein Lauf mit begrenzter Objektzahl.
- **Laufende Objekte** (aktivierte Kampagnen, Gruppen, Anzeigen) fasst der Agent nicht an, mit **einer Ausnahme (Entscheidung Alexander 21.10.2026): Negativbegriffe darf er später direkt eintragen.** Gebote, Budgets, Pausierungen, Texte und Keywords gehen weiter als Vorschlag in `daten/ads/vorschlaege/`; neue Texte und Keywords stellt der Agent pausiert neben die laufenden (Label `kb-agent`), Alexander tauscht sie aus.
- **Regeln für direkt eingetragene Negativbegriffe (Annahmen, vor dem Bau bestätigen):**
  1. Nur **hinzufügen**, nie entfernen oder ändern. Match-Typ Exact oder Phrase, nie Broad.
  2. Nur auf Grundlage des Suchbegriff-Berichts: offensichtlich Unpassendes (Kasse, Kinder, Jugendliche, DIY, Tier, Gerät, Ausbildung, Stellen, Gratis-Angebote) oder ein Begriff mit mindestens 15 Klicks ohne Anfrage und klarer Unpassung. Alles Unklare geht als Vorschlag.
  3. **Konfliktprüfung vorab:** Ein Negativbegriff darf in keinem eigenen Keyword der Kampagne vorkommen und keinen Themabegriff einer Gruppe blockieren (Skript, Vorbild: `anzeigen_check.py`). Kein einzelnes Wort wie „kosten“ oder „zahnarzt“.
  4. Höchstens 10 neue Negativbegriffe je Woche und Kampagne.
  5. Jeder Eintrag ins Protokoll `daten/ads/api-log.md` mit Suchbegriff, Zahlen, Begründung und Rückgängig-Hinweis (Negativbegriffe tragen kein Label). Die Wochenübersicht nennt sie Alexander.
  6. Trockenlauf bleibt Standard, angewendet wird nur mit `--anwenden`.

## Einführung (Reihenfolge)
Zuerst nur lesen (Berichte für `ads-optimizing`), dann Trockenlauf gegen das echte Konto, dann die erste Kampagne pausiert anlegen und gemeinsam im Konto ansehen. Direktes Eintragen von Negativbegriffen erst, wenn Alexander es nach den ersten Wochen mit Vorschlägen ausdrücklich einschaltet (`config/budget.json`). Bibliothek (offizielles Python-Paket oder REST) wird beim Bau entschieden.
