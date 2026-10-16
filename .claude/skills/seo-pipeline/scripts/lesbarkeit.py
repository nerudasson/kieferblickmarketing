#!/usr/bin/env python3
"""Lesbarkeit eines Entwurfs: Flesch-Reading-Ease nach Amstad (deutsche Fassung) und Wiener Sachtextformel (WSTF 1). Ziel: Flesch >= 65, WSTF <= 6.

Aufruf: lesbarkeit.py daten/entwuerfe/<slug>.md [--max 6]
Liest nur den Fließtext (ohne Frontmatter, Tabellen, Quellen, Autorenbox).
"""
import re, sys, argparse

def silben(w):
    w = w.lower()
    w = re.sub(r'(ei|ie|au|eu|äu|ai|ey|oi|ui)', 'a', w)
    n = len(re.findall(r'[aeiouäöüy]+', w))
    return max(n, 1)

def text_only(src):
    src = re.sub(r'^---\n.*?\n---\n', '', src, flags=re.S)
    src = src.split('\n---\n')[0]
    src = re.sub(r'## Quellen.*', '', src, flags=re.S)
    src = re.sub(r'<!--.*?-->', '', src)
    src = re.sub(r'^\|.*$', '', src, flags=re.M)
    src = re.sub(r'\[FAKT FEHLT[^\]]*\]', '', src)
    src = re.sub(r'\[\d+(\]\[\d+)*\]', '', src)
    src = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', src)
    src = re.sub(r'[#>*_`]', '', src)
    src = re.sub(r'^\s*(\d+\.|-)\s+', '', src, flags=re.M)
    return src

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('md'); ap.add_argument('--max', type=float, default=6, help='maximaler WSTF'); ap.add_argument('--min-flesch', type=float, default=65)
    a = ap.parse_args()
    t = text_only(open(a.md, encoding='utf-8').read())
    sents = [s.strip() for s in re.split(r'(?<=[.!?:])\s+|\n+', t) if len(s.split()) >= 2]
    words = re.findall(r"[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß-]*", t)
    sy = [silben(w) for w in words]
    n = len(words)
    ms = 100 * sum(1 for s in sy if s >= 3) / n
    sl = n / len(sents)
    iw = 100 * sum(1 for w in words if len(w) > 6) / n
    es = 100 * sum(1 for s in sy if s == 1) / n
    wstf = 0.1935 * ms + 0.1672 * sl + 0.1297 * iw - 0.0327 * es - 0.875
    flesch = 180 - sl - 58.5 * (sum(sy) / n)
    print(f'Wörter {n}, Sätze {len(sents)}, Ø Satzlänge {sl:.1f}, Flesch (Amstad) {flesch:.0f} (Ziel >= {a.min_flesch:g}), WSTF {wstf:.1f} (Ziel <= {a.max:g})')
    lang = sorted(((len(s.split()), s) for s in sents), reverse=True)[:8]
    print('Längste Sätze:')
    for k, s in lang:
        if k > 18: print(f'  {k}: {s[:140]}')
    sys.exit(0 if wstf <= a.max and flesch >= a.min_flesch else 1)

if __name__ == '__main__':
    main()
