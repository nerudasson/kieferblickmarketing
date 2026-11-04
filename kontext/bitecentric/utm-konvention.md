# UTM-Konvention BiteCentric (Quelle: Auftrag 04.11.2026)

Alles klein, mit Bindestrichen, ohne Umlaute, **keine Personen- oder Patientennamen**.

| Parameter | Erlaubte Werte |
|---|---|
| `utm_source` | linkedin · youtube · meta · buch · newsletter · website · partner-\<name\> · event-\<name\> |
| `utm_medium` | organic · flow · paid · qr · email · referral |
| `utm_campaign` | werkzeug-kap01 … werkzeug-kap11 · leseprobe · fall-analyse · intro · fall-einschaetzung · fallabend · kursanfrage |
| `utm_content` | post-JJJJ-MM-TT-\<thema\> · video-\<kurzname\> · anzeige-\<nr\> · kapNN |

Für Meta-Anzeigen: `utm_source=meta`, `utm_medium=paid`, `utm_content=anzeige-<nr>`.
- Aufruf „Aufzeichnung“ des Intro läuft unter `utm_campaign=intro` (Annahme, eigener Wert fehlt in der Konvention).
- Prüfung in `.claude/skills/meta-ads/scripts/anzeigen_check_meta.py`.
