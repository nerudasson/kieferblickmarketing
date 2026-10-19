#!/usr/bin/env python3
"""Musterprüfung auf wiederkehrende HWG-/Beleg-Fehler (deterministisch, vor dem Compliance-Reviewer).

  python3 hwg_check.py daten/entwuerfe/<slug>.md [--json]

HART  = muss behoben werden (Garantie, Beweisformeln, interne Persona, Entwarnung/Frist ohne Beleg, Werbesuperlative, Rabatt).
WEICH = prüfen und ersetzen, wenn die Quelle es nicht trägt (Absolutwörter, ungezitierte Vergleiche, "meist/oft" gehäuft).
Ausgenommen sind Frontmatter, Zusage-/CTA-/Praxis-Blöcke, Quellenbox und Kommentare. Zitierte Sätze ([B..], [S..], [n])
gelten bei WEICH-Mustern als belegt. Der Reviewer liest die Treffer, statt den ganzen Text nach diesen Mustern zu durchsuchen.
Die Ersatzformulierungen stammen aus den Befunden des Batches vom 19.10.2026.
"""
import json
import re
import sys
from pathlib import Path

# (Muster, Hinweis, braucht_Zitat_zur_Entschärfung)
HART = [
    (r"nachweislich|erwiesenermaßen|wissenschaftlich bewiesen|\bbewiesen\b|belegt sicher", "Beweisformel: „In Studien zu <Population> …; die Aussagekraft ist begrenzt.“"),
    (r"garantier|\bgarantie", "Statt Garantie „Zusage“; keine Ergebnisgarantie."),
    (r"\bJulia\b", "Interne Zielperson im Patiententext: „Sie“."),
    (r"kein drama|keine sorge|nicht schlimm|\bharmlos|kein notfall|müssen nicht sofort|nicht sofort handeln|können in ruhe abwarten|einfach abwarten", "Entwarnung/Dringlichkeit im Einzelfall nur mit Beleg: „Ob und wann, klärt die Untersuchung.“"),
    (r"\b(?:der|die|das|den|dem) beste[nrms]?\b|\bperfekt|\bluxus|\bschmerzfrei|\bohne risiko\b|\bnebenwirkungsfrei|\bunschlagbar|\bnummer 1\b", "Superlativ/Werbeversprechen: sachlich beschreiben."),
    (r"\brabatt|\baktion\b|nur noch heute|jetzt buchen|\bgratis-?angebot|\bschnäppchen", "Rabatt/Dringlichkeit ist ausgeschlossen."),
    (r"\bimmer\b.{0,40}(?:schmerz|erfolg|ergebnis|halt)|\bnie wieder\b|(?<!nicht )(?<!nicht\s)\bfür immer\b|\bdauerhaft(?:es)? ergebnis", "Absolutes Ergebnisversprechen."),
    (r"(?<!nicht )genau (?:steuern|vorhersag|planen|so aus)", "Ergebnisversprechen: „Wie das Ergebnis aussieht, lässt sich nicht genau vorhersagen.“"),
]
WEICH = [
    (r"\bimmer\b(?! (?:wieder|noch|mehr|häufiger|besser))(?<!für immer)|\bnie\b|\bstets\b|\bausnahmslos|\bin jedem fall|\bgrundsätzlich nicht", "Absolutwort: nur mit Beleg, sonst „meist/kann“ oder Ich-Aussage.", True),
    (r"\b(?:besser|günstiger|schneller|schonender|sicherer)\b (?:als|wirk\w*)\b|\b(?:ist|sind|wird|werden) (?:deutlich |meist |oft )?(?:besser|günstiger|schneller|schonender|sicherer)\b|\bbessere[nr]? (?:wahl|ergebnis\w*)|\bwer (?:vorher )?\w+ (?:fragt|prüft),? entscheidet sicherer", "Vergleich ohne Beleg: Quelle nennen oder als Ich-Einschätzung („Aus meiner Sicht …“).", True),
    (r"studien (?:zeigen|belegen)|forschung zeigt|wissenschaftlich", "Studienformel: Population und Einschränkung nennen.", True),
    (r"überschaubar|unproblematisch|gut verträglich|risikoarm", "Entwarnung: nur mit Beleg.", True),
    (r"\bkratzt\b.*schadet|schadet dem schmelz", "Risikoaussage ohne Beleg: „kann … belasten“.", True),
]
HAEUFIG = r"\b(?:meist|oft|häufig|selten|in der regel)\b"
MAX_HAEUFIG = 6


def haupttext(pfad):
    t = Path(pfad).read_text(encoding="utf-8")
    fm = re.match(r"^---\n.*?\n---\n", t, flags=re.S)
    zeilen = (t[fm.end():] if fm else t).split("\n")
    offset = t[: fm.end()].count("\n") if fm else 0
    out = []
    for i, z in enumerate(zeilen, start=offset + 1):
        if re.match(r"^##\s+Quellen\b", z):
            break
        s = z.strip()
        if not s or s.startswith(("<!--", "> Zusage", "> CTA", "> Praxis", "```")):
            continue
        out.append((i, z))
    return out


def pruefen(pfad):
    hart, weich = [], []
    zeilen = haupttext(pfad)
    for i, z in zeilen:
        zitiert = bool(re.search(r"\[(?:[SB]?\d+)\]", z))
        for muster, hinweis in HART:
            for m in re.finditer(muster, z, flags=re.I):
                hart.append((i, m.group(0), hinweis, z.strip()[:90]))
        if re.search(r"(?<![\d.,])100\s?(?:%|Prozent)|100 von 100", z) and not zitiert:
            hart.append((i, "100 %", "100 % nur mit Beleg und Studiengröße: „In einer kleinen Studie (n Veneers) …“", z.strip()[:90]))
        for muster, hinweis, braucht_zitat in WEICH:
            if braucht_zitat and zitiert:
                continue
            for m in re.finditer(muster, z, flags=re.I):
                weich.append((i, m.group(0), hinweis, z.strip()[:90]))
    text = "\n".join(z for _, z in zeilen)
    n_h = len(re.findall(HAEUFIG, text, flags=re.I))
    if n_h > MAX_HAEUFIG:
        weich.append((0, f"meist/oft/häufig ×{n_h}", f"Mengenwörter nur, wenn die Quelle sie trägt (höchstens {MAX_HAEUFIG}).", ""))
    return hart, weich


def bericht(pfad, ausfuehrlich=True):
    hart, weich = pruefen(pfad)
    zeilen = [f"HWG-Muster: {'OK' if not hart else 'PRÜFEN'} ({len(hart)} hart, {len(weich)} weich)"]
    for typ, liste in (("HART", hart), ("WEICH", weich if ausfuehrlich else [])):
        for i, w, h, z in liste:
            zeilen.append(f"  - {typ} Z.{i} „{w}“ – {h}" + (f"  | {z}" if z else ""))
    return not hart, zeilen


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    ok, zeilen = bericht(args[0])
    if "--json" in sys.argv:
        h, w = pruefen(args[0])
        print(json.dumps({"hart": h, "weich": w}, ensure_ascii=False))
    else:
        print("\n".join(zeilen))
    sys.exit(0 if ok else 1)
