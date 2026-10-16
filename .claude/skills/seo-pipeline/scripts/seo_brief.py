#!/usr/bin/env python3
"""SEO-Brief für einen Artikel über DataForSEO: verwandte Keywords, Autocomplete, Fragen der Suchenden, Top-Ergebnisse.

Aufruf: seo_brief.py "<keyword>" [--out daten/briefs/<slug>.json] [--location 2276]
Zugang: der Proxy der Umgebung setzt die Zugangsdaten für api.dataforseo.com (sonst DATAFORSEO_LOGIN/PASSWORD).
Gibt am Ende die Kosten in USD aus. Jeder Aufruf kostet Geld: nur gezielt nutzen.
"""
import argparse, json, os, subprocess, sys

BASE = 'https://api.dataforseo.com/v3/'

def call(path, payload):
    cmd = ['curl', '-s', '-m', '90', '-X', 'POST', BASE + path, '-H', 'Content-Type: application/json', '--data-binary', '@-']
    if os.environ.get('DATAFORSEO_LOGIN'):
        cmd[1:1] = ['-u', f"{os.environ['DATAFORSEO_LOGIN']}:{os.environ.get('DATAFORSEO_PASSWORD','')}"]
    r = subprocess.run(cmd, input=json.dumps(payload).encode(), capture_output=True)
    d = json.loads(r.stdout)
    t = (d.get('tasks') or [{}])[0]
    if t.get('status_code') != 20000:
        print('WARN', path, t.get('status_code'), t.get('status_message'), file=sys.stderr)
    return (t.get('result') or [{}])[0], float(d.get('cost') or 0)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('keyword'); ap.add_argument('--out'); ap.add_argument('--location', type=int, default=2276)
    a = ap.parse_args()
    loc = {'location_code': a.location, 'language_code': 'de'}
    cost, brief = 0.0, {'keyword': a.keyword, 'kosten_usd': {}}

    res, c = call('dataforseo_labs/google/related_keywords/live', [{'keyword': a.keyword, **loc, 'limit': 30, 'depth': 1}])
    cost += c; brief['kosten_usd']['related_keywords'] = c
    brief['verwandt'] = sorted([{'keyword': i['keyword_data']['keyword'], 'volumen': (i['keyword_data'].get('keyword_info') or {}).get('search_volume')}
                                for i in (res.get('items') or [])], key=lambda x: -(x['volumen'] or 0))

    res, c = call('serp/google/autocomplete/live/advanced', [{'keyword': a.keyword, **loc}])
    cost += c; brief['kosten_usd']['autocomplete'] = c
    brief['autocomplete'] = [i.get('suggestion') for i in (res.get('items') or [])]

    res, c = call('serp/google/organic/live/advanced', [{'keyword': a.keyword, **loc, 'depth': 10, 'people_also_ask_click_depth': 2}])
    cost += c; brief['kosten_usd']['serp'] = c
    items = res.get('items') or []
    brief['fragen'] = []
    for i in items:
        if i.get('type') == 'people_also_ask':
            for q in i.get('items') or []:
                if q.get('title'): brief['fragen'].append(q['title'])
    brief['top_ergebnisse'] = [{'rang': i.get('rank_group'), 'titel': i.get('title'), 'domain': i.get('domain'), 'url': i.get('url')}
                               for i in items if i.get('type') == 'organic'][:10]
    brief['fragen'] = list(dict.fromkeys(brief['fragen']))
    brief['kosten_usd']['gesamt'] = round(cost, 4)
    out = json.dumps(brief, ensure_ascii=False, indent=2)
    if a.out:
        open(a.out, 'w', encoding='utf-8').write(out)
    print(out)

if __name__ == '__main__':
    main()
