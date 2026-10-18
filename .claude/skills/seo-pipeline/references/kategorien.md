# WordPress-Kategorien für Wissensartikel

Die Adresse eines Artikels ist `/<kategorie-slug>/<artikel-slug>/` (Permalink-Struktur der Website). Jeder Artikel bekommt genau **eine** Hauptkategorie nach dem Produkt, zu dem er hinführt. Frontmatter-Feld `kategorie` (Slug).

| Kategorie (Slug) | Produkt / Thema | Typische Keywords |
|---|---|---|
| `aligner` | Aligner-Behandlung: Kosten, Ablauf, Erfahrungen, Risiken, Zähne begradigen/richten | aligner kosten, zähne begradigen, zähne richten lassen, aligner erfahrungen |
| `retainer` | Retainer, Haltephase, Rückfall (Retainer-Klub, PZR-Abo als Anschluss) | wie lange retainer tragen, retainer draht gelöst, zähne verschieben sich |
| `bleaching-zahnreinigung` | Bleaching und professionelle Zahnreinigung (PZR) | bleaching kosten, zähne aufhellen, pzr |
| `veneers` | Formkorrektur mit Veneers | veneers kosten, veneers haltbarkeit |
| `schnarchschiene` | Schiene für die Nacht bei Schnarchen | schnarchschiene kosten, schnarchen was tun |
| `funktionsschiene` | Knirschen, Funktionsschiene (Produkt geparkt, nur Vorrat) | zähneknirschen schiene |

Regeln:
- Mehrdeutig: die Kategorie wählen, die der CTA des Artikels bewirbt (z. B. „Zähne verschieben sich“ → `retainer`, weil es zu Retainer-Klub und Erstberatung führt).
- Fehlt eine passende Kategorie (neues Produkt), nicht raten: im Bericht melden, Alexander legt sie an oder gibt Freigabe.
- Nie `uncategorized`.
- Interne Links: Adresse aus `daten/linkplan.csv` (Spalte `url`).
