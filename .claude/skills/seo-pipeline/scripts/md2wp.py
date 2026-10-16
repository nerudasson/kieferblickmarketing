#!/usr/bin/env python3
"""Entwurf-Markdown (mit !-Direktiven) -> WordPress-Payload (Gutenberg-Blöcke + kb_-Meta)."""
import html, json, re, sys

def inline(s):
    s = html.escape(s, quote=False)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)

def p(t, cls=None):
    attr = f' {{"className":"{cls}"}}' if cls else ""
    c = f' class="{cls}"' if cls else ""
    return f"<!-- wp:paragraph{attr} -->\n<p{c}>{t}</p>\n<!-- /wp:paragraph -->"

def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{inline(t)}</h2>\n<!-- /wp:heading -->'

def ul(items, ordered=False, cls=None):
    tag = "ol" if ordered else "ul"
    attrs = {"ordered": True} if ordered else {}
    if cls: attrs["className"] = cls
    a = " " + json.dumps(attrs) if attrs else ""
    c = f' class="{cls}"' if cls else ""
    lis = "".join(f"<!-- wp:list-item --><li>{inline(i)}</li><!-- /wp:list-item -->" for i in items)
    return f"<!-- wp:list{a} -->\n<{tag}{c}>{lis}</{tag}>\n<!-- /wp:list -->"

def table(rows, cls=None):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    head, body = cells[0], cells[1:]
    th = "".join(f"<th>{inline(c)}</th>" for c in head)
    tr = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
    a = f' {{"className":"{cls}"}}' if cls else ""
    c = f" {cls}" if cls else ""
    return (f"<!-- wp:table{a} -->\n<figure class=\"wp-block-table{c}\"><table><thead><tr>{th}</tr></thead>"
            f"<tbody>{tr}</tbody></table></figure>\n<!-- /wp:table -->")

def details(summary, inner, cls):
    return (f'<!-- wp:details {{"className":"{cls}"}} -->\n<details class="wp-block-details {cls}">'
            f"<summary>{inline(summary)}</summary>{inner}</details>\n<!-- /wp:details -->")

def convert(body):
    lines = body.strip().splitlines()
    out, i = [], 0
    while i < len(lines):
        l = lines[i].rstrip()
        if not l:
            i += 1; continue
        if l.startswith("## "):
            out.append(h2(l[3:])); i += 1
        elif l.startswith("!merksatz "):
            out.append(p(inline(l[10:]), "kb-merksatz")); i += 1
        elif l.startswith("!hinweis "):
            out.append(p("<strong>Gut zu wissen:</strong> " + inline(l[9:]), "kb-hinweis")); i += 1
        elif l.startswith("!cta "):
            out.append(p(inline(l[5:]), "kb-cta")); i += 1
        elif l in ("!tabelle", "!vergleich"):
            j = i + 1; rows = []
            while j < len(lines) and lines[j].startswith("|"):
                rows.append(lines[j]); j += 1
            out.append(table(rows, "kb-vergleich" if l == "!vergleich" else None)); i = j
        elif l == "!schritte":
            j = i + 1; items = []
            while j < len(lines) and re.match(r"\d+\. ", lines[j]):
                items.append(re.sub(r"^\d+\. ", "", lines[j])); j += 1
            out.append(ul(items, True, "kb-schritte")); i = j
        elif l == "!quellen":
            j = i + 1; items = []
            while j < len(lines) and re.match(r"\d+\. ", lines[j]):
                items.append(re.sub(r"^\d+\. ", "", lines[j])); j += 1
            inner = ul(items, True).replace("<!-- wp:list -->", "<!-- wp:list {\"ordered\":true} -->")
            out.append(details("Quellen", inner, "kb-quellen")); i = j
        elif l.startswith("?? "):
            q = l[3:]; a = lines[i + 1][3:]
            out.append(details(q, p(inline(a)), "kb-faq")); i += 2
        elif re.match(r"- ", l):
            j = i; items = []
            while j < len(lines) and lines[j].startswith("- "):
                items.append(lines[j][2:]); j += 1
            out.append(ul(items)); i = j
        elif re.match(r"\d+\. ", l):
            j = i; items = []
            while j < len(lines) and re.match(r"\d+\. ", lines[j]):
                items.append(re.sub(r"^\d+\. ", "", lines[j])); j += 1
            out.append(ul(items, True)); i = j
        else:
            out.append(p(inline(l))); i += 1
    return "\n\n".join(out)

def frontmatter(txt):
    _, fm, body = txt.split("---\n", 2) if txt.startswith("---\n") else (None, "", txt)
    meta, key = {}, None
    for l in fm.splitlines():
        m = re.match(r"^(\w+): ?(\|)?(.*)$", l)
        if m and not l.startswith(" "):
            key = m.group(1); meta[key] = "" if m.group(2) else m.group(3).strip();
        elif key and l.startswith("  "):
            meta[key] += l.strip() + "\n"
    return {k: v.strip() for k, v in meta.items()}, body

if __name__ == "__main__":
    src, cat_id = sys.argv[1], int(sys.argv[2])
    meta, body = frontmatter(open(src, encoding="utf-8").read())
    payload = {
        "title": meta["title"], "slug": meta["slug"], "status": "draft",
        "excerpt": meta["meta_description"], "categories": [cat_id],
        "content": convert(body),
        "meta": {k: v for k, v in meta.items() if k.startswith("kb_")},
    }
    json.dump(payload, sys.stdout, ensure_ascii=False)
