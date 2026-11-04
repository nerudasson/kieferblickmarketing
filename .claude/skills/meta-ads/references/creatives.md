# Creatives (Quelle: Auftrag 04.11.2026)

**Grundlage sind echte Fälle aus Fall-Dossiers.** Keine generischen KI-Bilder von Menschen oder Zähnen, keine Stock-Posen. `bild_quelle` ist `fall-dossier`, `eigene-aufnahme` (Alexander, Team, Praxis) oder `dokument` (Buchcover, Zertifikat).

| Typ | Inhalt | Pflichtfelder | Aufruf (Beispiel) |
|---|---|---|---|
| `fall-in-bildern` | ein Fall in 3–5 Bildern/Szenen, ruhig kommentiert | fall_dossier | kalt: Leseprobe; mit konkretem Fall: Fall-Einschätzung |
| `gruendergeschichte` | Alexanders erster schwieriger Fall: was er damals nicht wusste | fall_dossier | kalt: Leseprobe oder Werkzeug |
| `entscheidung-am-fall` | eine Entscheidung aus dem Buch, am Fall gezeigt | fall_dossier | kalt: Werkzeug zum Kapitel (`werkzeug-kapNN`) |
| `teilnehmerstimme` | Stimme eines Teilnehmers, **erst ab der ersten Startgruppe** | einwilligung_vorhanden | warm: Intro |
| `qualifikation` | Zertifikat, Fortbildungspunkte | beleg | warm: Intro |

## Regeln für jedes Creative
- Kollegensprache, Sie-Form, ruhig, fallbasiert. Kein Hype, keine Dringlichkeit, keine Ergebnis- oder Umsatzversprechen, nie andeuten, dass bisherige Behandlungen falsch waren („Fehlerfall“ ist ein Falltyp, kein Vorwurf).
- Patientinnen und Patienten nur anonymisiert, nie erkennbar, nie mit Namen. Vorher-nachher nur, wenn die Einwilligung dokumentiert ist, ohne Ergebnisversprechen.
- Keine Wettbewerbernamen im Text; die Abgrenzung heißt „systemneutral“.
- Fall-Dossiers: im Repo nur Kennung und anonymisierte Kurzbeschreibung. **Lücke:** Ablageort und Format der Dossiers sind nicht bekannt.
- Testen: Varianten unterscheiden sich in **einem** Punkt (Typ, Einstieg oder Aufruf), sonst lässt sich das Ergebnis nicht zuordnen. Jede Variante bekommt eine eigene `anzeige-<nr>`.
- Bildvarianten legt der Agent als Beschreibung (Szene, Bildausschnitt, Text-Einblendung) in der Kampagnendatei an. Fertige Bilddateien liefert Alexander aus den Dossiers.
