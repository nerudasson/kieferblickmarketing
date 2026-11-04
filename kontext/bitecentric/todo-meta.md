# To-do für Alexander: Meta-Anzeigen-Agent und Konkurrenz-Monitor (Stand 04.11.2026)

Reihenfolge einhalten; jeder Block baut auf dem vorigen auf. Schlüssel nie in Chat, Repository oder Dateien, nur als Umgebungsvariablen der Cloud-Umgebung. Alle Freigabe-Schalter in `config/meta.json` stehen bis zu deinem OK auf false.

## A. Konten und Grundlagen (ohne Kosten)
1. **Meta-Entwicklerkonto und Meta-App** anlegen (developers.facebook.com/apps). App-ID notieren. Produkt „Marketing API“ hinzufügen (Zugriffsstufe Limited Access kommt automatisch, für das eigene Konto ohne App Review). Für den Ads-MCP den Use Case „Create & manage ads with ads MCP server“ hinzufügen.
2. **Identitäts- und Standortbestätigung für die Ad Library API** (Ausweis, laut Metas Radlibrary-Paket 1–2 Tage) und die Nutzungsbedingungen für öffentliche Informationen akzeptieren. Länder: Deutschland, Österreich, Vereinigtes Königreich. Die offizielle Zugangsseite war bei meiner Recherche nicht lesbar: bitte die Schritte dort selbst prüfen und mir Abweichungen melden.
3. **BiteCentric-Werbekonto, Facebook-Seite und Pixel** anlegen oder zuordnen. Im Pixel das Ereignis „Lead“ für die Anmeldung zu Leseprobe/Werkzeug einrichten. Notieren: Werbekonto-ID, Seiten-ID, Pixel-ID.
4. **Benutzerdefinierte Zielgruppen** im Werbekonto anlegen: Kunden (zum Ausschließen), Intro angemeldet, Intro besucht, Leseprobe-Leads, Webseitenbesucher. Die IDs trägst du (oder ich nach deiner Ansage) unter `ads.zielgruppen_ids` in `config/meta.json` ein; es sind keine Geheimnisse. Kundenlisten enthalten personenbezogene Daten von Zahnärzten: nur gehasht und mit Rechtsgrundlage hochladen.
5. **Meta-Budget festlegen:** `ads.kampagnen_eur` (kalt, warm, heiss) und `ads.monatsbudget_eur` in `config/meta.json`. Der Auftrag nennt keinen Wert; solange er 0 ist, besteht keine Kampagnendatei die Prüfung.
6. **Webadresse bestätigen** (Annahme `bitecentric.de`, Eintrag `ads.erlaubte_domains`). Zielseiten für Leseprobe, Werkzeug, Fall-Analyse, Fall-Einschätzung, Intro und Kursanfrage mit HubSpot-Formular, Pixel und versteckten Feldern für `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`.
7. **HubSpot prüfen:** Das Portal meldet „Onboarding nicht abgeschlossen“. Prüfen, ob Workflows existieren, die aus `bc_funnel_status` die Lebenszyklusphase setzen (Intro besucht → MQL, Vorgespräch geführt → SQL, Gewonnen → Customer). Ohne sie sind MQL, SQL und Customer in der Auswertung leer.
8. **Verhältnis zu Scheu klären** (Gesamtkonzept 14, Punkt 14), bevor Anzeigen laufen.

## B. Schlüssel und Umgebung
9. **Netzwerkfreigabe** der Cloud-Umgebung: `graph.facebook.com` erlauben (Umgebung bearbeiten, Allowed domains). Für den Ads-MCP zusätzlich `mcp.facebook.com`. Eine neue Sitzung übernimmt die Werte.
10. **Ad-Library-Token:** langlebigen User-Token (ca. 60 Tage) aus der Meta-App erzeugen und als `META_ADLIB_ACCESS_TOKEN` in der Umgebung hinterlegen. Ablauf alle 60 Tage im Kalender vermerken (Fehler 190 im Lauf bedeutet abgelaufen).
11. **Ads-Token (erst für Stufe 2 nötig):** `META_ADS_ACCESS_TOKEN` (User- oder System-User-Token mit Employee-Rolle, Scopes `ads_read`, `ads_management`, beim MCP zusätzlich `ads_mcp_management`), dazu `META_AD_ACCOUNT_ID`, `META_PAGE_ID`, `META_PIXEL_ID`.
12. **Schutz bei Meta:** im Werbekonto unter „Ads MCP Rules“ (falls für dich verfügbar) Statusänderungen und Budgeterhöhungen durch den Agenten verbieten. Das ist ein zweites Schloss neben `.claude/settings.json`.
13. **Ads-MCP verbinden** (Claude Code): `claude mcp add --transport http --client-id <META_APP_ID> meta-ads https://mcp.facebook.com/ads`, Anmeldung im Browser, Servername `meta-ads` beibehalten (die Sperren in den Einstellungen verwenden ihn).

## C. Trockenlauf und Freigaben (Konkurrenz-Monitor)
14. Trockenlauf ansehen: `python3 -I .claude/skills/meta-wettbewerb/scripts/adlib.py snapshot --dry-run` und `… seiten --dry-run`. Sag mir „OK“, wenn Plan und Obergrenzen (26 bzw. 28 Abfragen, höchstens 150) passen.
15. Schalter `adlib.echtlauf_freigegeben` auf true setzen (oder mir sagen).
16. Erster Echtlauf `seiten`: **Seiten-IDs bestätigen** (`daten/meta/wettbewerb/seiten-vorschlag.md`), ich trage sie ein.
17. Erster Echtlauf `snapshot` und `report` gemeinsam ansehen. Dabei klärt sich: UK-Abdeckung für alle Anzeigen, Struktur der UK-Reichweite, Trefferqualität der Suchbegriffe.
18. **Wochenlauf einplanen:** erst jetzt und nach deinem OK. Ich lege die geplante Aufgabe an (Prompt in `.claude/skills/meta-wettbewerb/references/wochenlauf-prompt.md`). Hinweis: Der Lauf schreibt auf den Arbeitsbranch; nach einem Merge den Branch im Prompt anpassen lassen.

## D. Anzeigen (Stufe 2)
19. **Fall-Dossiers:** Ablageort und Format festlegen (im Repository nur Kennung und anonymisierte Kurzbeschreibung), erste Bild- und Videodateien liefern.
20. Schalter `ads.lesezugriff_freigegeben` auf true, sobald der Ads-MCP verbunden ist (Auswertung der Ausgaben).
21. **Erste Kampagne:** ich entwerfe sie (Kalt, Fall-Clip → Leseprobe), Prüfung und Review laufen, Trockenlauf von `meta_push.py` ansehen. Erst danach `ads.schreibzugriff` auf true; das Anlegen ist **nicht gegen ein echtes Konto getestet**, rechne mit Nachbesserungen im ersten Lauf.
22. Im Werbekonto die pausierten Objekte prüfen, Detailtargeting und ggf. Video/Bild ergänzen, selbst aktivieren.

## E. Offene Fragen (Wettbewerbsdokument; Gesamtkonzept 14)
AT und CH in der Werbebibliothek prüfen (CH ist über die API nicht abbildbar) · ob Align in DACH gezielt Zahnärzte über Meta anwirbt · welche Labore als Partner zuerst angesprochen werden.
