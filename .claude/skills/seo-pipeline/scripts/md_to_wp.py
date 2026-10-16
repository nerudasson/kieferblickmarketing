#!/usr/bin/env python3
"""Setzt einen Entwurf (daten/entwuerfe/<slug>.md) in WordPress-Blöcke der Kieferblick-Artikelvorlage um.

Aufruf:
  md_to_wp.py <entwurf.md> --json out.json     JSON für POST /wp-json/wp/v2/posts schreiben
  md_to_wp.py <entwurf.md> --post [--id N]     als Entwurf (status=draft) anlegen bzw. Beitrag N aktualisieren

Marker im Entwurf (HTML-Kommentar direkt vor dem Element): kb-merksatz, kb-hinweis, kb-schritte,
kb-vergleich, kb-faq, kb-cta, kb-quellen. Autorenbox und Schlusshinweis am Textende (nach '---')
liefert die Vorlage, sie werden nicht übernommen. Nie status=publish.
"""
import argparse, json, re, subprocess, sys, html

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', t)
    t = re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+|/[^)\s]*)\)', r'<a href="\2">\1</a>', t)
    return t

def parse_front(src):
    m = re.match(r'---\n(.*?)\n---\n(.*)', src, re.S)
    fm, body = m.groups()
    meta, key = {}, None
    for line in fm.splitlines():
        if re.match(r'^\s+- ', line) and key:
            meta.setdefault(key, []).append(line.strip()[2:].strip().strip('"'))
        elif ':' in line:
            key, v = line.split(':', 1)
            key, v = key.strip(), v.strip().strip('"')
            meta[key] = v if v else []
    return meta, body

def blk(name, attrs, inner):
    a = (' ' + json.dumps(attrs, ensure_ascii=False)) if attrs else ''
    return f'<!-- wp:{name}{a} -->\n{inner}\n<!-- /wp:{name} -->\n'

def para(t, cls=None):
    if cls:
        return blk('paragraph', {'className': cls}, f'<p class="{cls}">{inline(t)}</p>')
    return blk('paragraph', None, f'<p>{inline(t)}</p>')

def items(lines, ordered):
    return ''.join(f'<!-- wp:list-item --><li>{inline(re.sub(r"^(\d+\.|-|\*)\s+", "", l))}</li><!-- /wp:list-item -->' for l in lines)

def table(rows, cls):
    cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows if not re.match(r'^\s*\|?\s*-', r)]
    head, bodyr = cells[0], cells[1:]
    t = '<thead><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in head) + '</tr></thead><tbody>'
    t += ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in bodyr) + '</tbody>'
    attrs = {'className': cls} if cls else None
    return blk('table', attrs, f'<figure class="wp-block-table{" " + cls if cls else ""}"><table>{t}</table></figure>')

def convert(body):
    body = body.split('\n---\n')[0] if '\n---\n' in body else body
    lines = body.strip('\n').splitlines()
    out, i, marker, in_quellen = [], 0, None, False
    faq_open = False
    quellen = []
    while i < len(lines):
        l = lines[i]
        if not l.strip():
            i += 1; continue
        m = re.match(r'^<!--\s*(kb-[a-z]+)\s*-->$', l.strip())
        if m:
            marker = m.group(1); i += 1; continue
        if l.startswith('## '):
            title = l[3:].strip()
            if title.lower() == 'quellen':
                in_quellen = True; marker = 'kb-quellen'
            else:
                in_quellen = False
                out.append(blk('heading', None, f'<h2 class="wp-block-heading">{inline(title)}</h2>'))
                marker = None
            i += 1; continue
        if in_quellen:
            quellen.append(re.sub(r'^\[\d+\]\s*', '', l.strip())); i += 1; continue
        if l.startswith('>'):
            buf = []
            while i < len(lines) and lines[i].startswith('>'):
                buf.append(lines[i].lstrip('> ').strip()); i += 1
            txt = ' '.join(b for b in buf if b)
            if marker == 'kb-hinweis':
                out.append(para(txt, 'kb-hinweis'))
            else:
                out.append(para(txt, 'kb-merksatz'))
            marker = None; continue
        if l.lstrip().startswith('|'):
            buf = []
            while i < len(lines) and lines[i].lstrip().startswith('|'):
                buf.append(lines[i]); i += 1
            out.append(table(buf, 'kb-vergleich')); marker = None; continue
        if re.match(r'^\d+\.\s', l):
            buf = []
            while i < len(lines) and re.match(r'^\d+\.\s', lines[i]):
                buf.append(lines[i]); i += 1
            cls = ' class="kb-schritte"' if marker == 'kb-schritte' else ''
            attrs = {'ordered': True, **({'className': 'kb-schritte'} if marker == 'kb-schritte' else {})}
            out.append(blk('list', attrs, f'<ol{cls}>{items(buf, True)}</ol>')); marker = None; continue
        if re.match(r'^[-*]\s', l):
            buf = []
            while i < len(lines) and re.match(r'^[-*]\s', lines[i]):
                buf.append(lines[i]); i += 1
            out.append(blk('list', None, f'<ul class="wp-block-list">{items(buf, False)}</ul>')); marker = None; continue
        if marker == 'kb-faq' or re.match(r'^\*\*[^*]+\?\*\*$', l.strip()):
            q = l.strip().strip('*')
            a = []
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].startswith('**'):
                a.append(lines[i].strip()); i += 1
            ans = ' '.join(a)
            out.append(blk('details', {'className': 'kb-faq'},
                           f'<details class="wp-block-details kb-faq"><summary>{inline(q)}</summary>'
                           f'<!-- wp:paragraph --><p>{inline(ans)}</p><!-- /wp:paragraph --></details>'))
            marker = 'kb-faq'; continue
        if marker == 'kb-cta':
            out.append(para(l.strip(), 'kb-cta')); marker = None; i += 1; continue
        out.append(para(l.strip())); i += 1
    if quellen:
        li = ''.join(f'<!-- wp:list-item --><li>{inline(q)}</li><!-- /wp:list-item -->' for q in quellen)
        out.append(blk('details', {'className': 'kb-quellen'},
                       f'<details class="wp-block-details kb-quellen"><summary>Quellen</summary>'
                       f'<!-- wp:list {{"ordered":true}} --><ol>{li}</ol><!-- /wp:list --></details>'))
    return '\n'.join(out)

def build(path):
    meta, body = parse_front(open(path, encoding='utf-8').read())
    kurz = meta.get('kurz', [])
    payload = {
        'title': meta['title'], 'slug': meta['slug'], 'status': 'draft',
        'content': convert(body), 'excerpt': meta.get('meta_description', ''),
        'meta': {'kb_kurz': '\n'.join(kurz) if isinstance(kurz, list) else kurz,
                 'kb_ursache': meta.get('ursache', ''), 'kb_behandlung': meta.get('behandlung', ''),
                 'kb_dauer': meta.get('dauer', ''), 'kb_kosten': meta.get('kosten', '')},
    }
    return payload

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('md'); ap.add_argument('--json'); ap.add_argument('--post', action='store_true')
    ap.add_argument('--id', type=int)
    a = ap.parse_args()
    p = build(a.md)
    if a.json:
        json.dump(p, open(a.json, 'w', encoding='utf-8'), ensure_ascii=False)
    if a.post:
        url = 'https://kieferblick.de/wp-json/wp/v2/posts' + (f'/{a.id}' if a.id else '')
        r = subprocess.run(['curl', '-s', '-X', 'POST', url, '-H', 'Content-Type: application/json',
                            '--data-binary', '@-'], input=json.dumps(p, ensure_ascii=False).encode(), capture_output=True)
        d = json.loads(r.stdout)
        print(d.get('id'), d.get('status'), d.get('link'), d.get('message', ''))
        if d.get('status') == 'publish':
            sys.exit('FEHLER: Beitrag ist veröffentlicht, das darf nicht sein.')

if __name__ == '__main__':
    main()
