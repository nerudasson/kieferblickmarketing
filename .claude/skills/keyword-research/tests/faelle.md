# Testfälle keyword-research
1. **Dry-run:** `--dry-run` mit 5 Seeds. Erwartung: kein Netzwerkzugriff, Ausgabe der geplanten Anfrage, keine Kosten.
2. **Fehlende Zugangsdaten:** ohne Variablen und ohne `--dry-run`. Erwartung: klare Fehlermeldung, kein Absturz mit Stacktrace.
3. **Queue mit Marke:** CSV mit „invisalign kosten“ und „aligner kosten“. Erwartung: beide in der Queue, erstes mit `notiz=marke`, Intent „kosten“.
4. **Wiederholter Lauf:** Queue hat bereits eine Zeile mit `status=geprueft`. Erwartung: Status bleibt, keine Duplikate.
