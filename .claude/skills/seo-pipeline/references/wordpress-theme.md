# Theme-Eigenheiten (Plugin kieferblick-setup, kb.css/kb.js) für `wp_publish.py`

Stand 19.10.2026, aus dem CSS/JS des Themes und dem Beispielartikel (Post 105) abgelesen.
- **Inhaltsleiste:** Das Theme erzeugt links eine eigene Leiste (`aside.kb-toc`) aus den H2 und vergibt die Überschrift-IDs selbst. Der Publisher setzt kein eigenes Inhaltsverzeichnis, keine Anker und keine Klasse `kb-toc` (sie ist sticky positioniert und würde den Text überlagern).
- **Eckige Klammern:** Alles in `[…]` im sichtbaren Text färbt das Theme gelb (Platzhalter-Markierung, `.kb mark`). Zitate werden deshalb als hochgestellte Ziffern `<sup>1</sup>` ausgegeben; der Publisher warnt bei verbleibenden Klammern.
- **Quellenbox:** `details.kb-quellen` ohne eigene H2 „Quellen“ davor, standardmäßig geöffnet (`showContent`), sonst wirkt sie leer.
- **FAQ, Tabellen, Merksatz, Hinweis, CTA:** Klassen `kb-faq`, `kb-vergleich`, `kb-merksatz`, `kb-hinweis`, `kb-cta` stehen im Theme-CSS; Tabellen werden mobil per JS in Karten umgebaut.
