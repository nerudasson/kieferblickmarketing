#!/usr/bin/env python3
"""Legt einen geprüften Meta-Kampagnenentwurf PAUSIERT im Werbekonto an (Marketing API, nur Standardbibliothek).

  meta_push.py <kampagne.json>               Trockenlauf (Standard): zeigt die Objekte, kein Netzwerk, kein Token nötig
  meta_push.py <kampagne.json> --anwenden    legt Kampagne, Anzeigengruppen, Creatives, Anzeigen an (alles PAUSED)

Sperren (alle müssen offen sein, sonst Abbruch vor dem ersten Aufruf):
  1. anzeigen_check_meta.py ohne HART-Treffer
  2. config/meta.json: freigabestufe >= 2, ads.nur_pausiert true, ads.schreibzugriff true
  3. Umgebungsvariablen (Namen in config/meta.json): META_ADS_ACCESS_TOKEN, META_AD_ACCOUNT_ID, META_PAGE_ID, META_PIXEL_ID
  4. Zielgruppen-IDs für „kunden“ (und alle genannten custom_audiences) in config/meta.json
Der Agent aktiviert nie etwas: _sende() lässt nur POST auf campaigns/adsets/adimages/adcreatives/ads zu, nur mit status PAUSED,
und kein POST auf bestehende Objekte (keine Änderungen, keine Aktivierung). Keine Schlüssel in Dateien oder Ausgaben.
Stand: gegen kein echtes Konto getestet (nur gegen einen lokalen Testserver). Bei Fehlern des ersten Laufs Payload anpassen.
"""
import base64
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HIER = Path(__file__).resolve().parent
sys.path.insert(0, str(HIER))
import anzeigen_check_meta as check  # noqa: E402

ROOT = Path(__file__).resolve().parents[4]
CONFIG = Path(os.environ.get("META_CONFIG") or ROOT / "config/meta.json")  # META_CONFIG nur für Tests
PROTOKOLL = Path(os.environ.get("META_PROTOKOLL") or ROOT / "daten/meta/protokoll.md")
ERLAUBT = ("campaigns", "adsets", "adimages", "adcreatives", "ads")
NAMENSPRAEFIX = "[bc-agent] "


def basis_url():
    b = os.environ.get("META_GRAPH_BASE", "https://graph.facebook.com")
    if b != "https://graph.facebook.com" and not b.startswith("http://127.0.0.1"):
        sys.exit("META_GRAPH_BASE darf nur https://graph.facebook.com oder ein lokaler Testserver sein.")
    return b


def cents(eur):
    return int(round(float(eur) * 100))


def plan_bauen(k, cfg, env):
    """Baut die Objekte (ohne IDs der noch nicht angelegten Eltern). Rückgabe: dict."""
    ads = cfg["ads"]
    ids = ads.get("zielgruppen_ids", {})
    kunden = ids.get("kunden", "")

    def aud(namen):
        out = []
        for n in namen:
            out.append({"id": ids.get(n) or f"<zielgruppen_ids.{n}>"})
        return out

    zg = k.get("zielgruppe", {})
    gruppen = k["anzeigengruppen"]
    je_gruppe = k["tagesbudget_eur"] / len(gruppen)
    p = {
        "kampagne": {
            "name": NAMENSPRAEFIX + k["kampagne"],
            "objective": "OUTCOME_LEADS",
            "status": "PAUSED",
            "special_ad_categories": [],
            "is_adset_budget_sharing_enabled": False,
        },
        "gruppen": [],
        "manuell_nachzutragen": [],
    }
    if zg.get("berufe_oder_interessen"):
        p["manuell_nachzutragen"].append(
            "Detailtargeting (Berufe/Interessen: " + ", ".join(zg["berufe_oder_interessen"]) + ") in Meta ergänzen: IDs liefert nur die Targeting-Suche.")
    for g in gruppen:
        targeting = {
            "geo_locations": {"countries": k["laender"]},
            "age_min": zg.get("alter_min", 25),
            "age_max": zg.get("alter_max", 65),
            "publisher_platforms": ["facebook", "instagram"],
            "targeting_automation": {"advantage_audience": 0},
            "excluded_custom_audiences": [{"id": kunden or "<zielgruppen_ids.kunden>"}],
        }
        if zg.get("custom_audiences"):
            targeting["custom_audiences"] = aud(zg["custom_audiences"])
        satz = {
            "name": NAMENSPRAEFIX + g["name"],
            "daily_budget": cents(je_gruppe),
            "billing_event": "IMPRESSIONS",
            "optimization_goal": "OFFSITE_CONVERSIONS",
            "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
            "promoted_object": {"pixel_id": env.get("pixel_id") or "<META_PIXEL_ID>", "custom_event_type": "LEAD"},
            "targeting": targeting,
            "status": "PAUSED",
        }
        anzeigen = []
        for a in g["anzeigen"]:
            cta = {"type": a.get("cta_button", "LEARN_MORE"), "value": {"link": a["link"]}}
            if a.get("format") == "video":
                if not a.get("video_id"):
                    p["manuell_nachzutragen"].append(f"Anzeige {a['nr']}: Video im Werbekonto hochladen und video_id eintragen (kein Video-Upload im Skript).")
                spec = {"video_data": {"video_id": a.get("video_id") or "<video_id>", "message": a["primaerer_text"],
                                       "title": a.get("titel", ""), "link_description": a.get("beschreibung", ""),
                                       "call_to_action": cta}}
            else:
                spec = {"link_data": {"message": a["primaerer_text"], "link": a["link"], "name": a.get("titel", ""),
                                      "description": a.get("beschreibung", ""), "image_hash": "<aus adimages>",
                                      "call_to_action": cta}}
            anzeigen.append({
                "nr": a["nr"],
                "bild_datei": a.get("bild_datei"),
                "creative": {"name": f"{NAMENSPRAEFIX}anzeige-{int(a['nr']):03d}", "object_story_spec": {"page_id": env.get("seite") or "<META_PAGE_ID>", **spec}},
                "anzeige": {"name": f"{NAMENSPRAEFIX}anzeige-{int(a['nr']):03d}", "status": "PAUSED"},
            })
            if a.get("format") != "video" and not a.get("bild_datei"):
                p["manuell_nachzutragen"].append(f"Anzeige {a['nr']}: bild_datei fehlt (Bild aus Fall-Dossier, kein Upload möglich).")
        p["gruppen"].append({"satz": satz, "anzeigen": anzeigen})
    return p


def sende(pfad, daten, token):
    """Einziger Schreibweg. Lässt nur das Anlegen neuer Objekte zu, nur pausiert."""
    teile = pfad.strip("/").split("/")
    if len(teile) != 2 or not teile[0].startswith("act_") or teile[1] not in ERLAUBT:
        sys.exit(f"Interner Schutz: Pfad „{pfad}“ nicht erlaubt (nur POST act_<id>/{'|'.join(ERLAUBT)}).")
    if teile[1] in ("campaigns", "adsets", "ads") and daten.get("status") != "PAUSED":
        sys.exit("Interner Schutz: Anlegen ohne status=PAUSED verweigert.")
    if "status" in daten and daten["status"] != "PAUSED":
        sys.exit("Interner Schutz: nur status=PAUSED erlaubt.")
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    version = cfg.get("graph_version", "v26.0")
    body = {k: (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)) for k, v in daten.items()}
    body["access_token"] = token
    req = urllib.request.Request(f"{basis_url()}/{version}/{pfad}", data=urllib.parse.urlencode(body).encode(), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        try:
            fehler = json.load(e).get("error", {})
        except Exception:
            fehler = {"message": f"HTTP {e.code} ohne JSON (Proxy/Netzwerkfreigabe für graph.facebook.com prüfen)"}
        msg = str(fehler.get("message", fehler)).replace(token, "***")
        sys.exit(f"Meta-API-Fehler bei {teile[1]}: {msg} (Code {fehler.get('code')}). Es wurde nichts aktiviert.")


def lese(pfad, params, token):
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    q = dict(params, access_token=token)
    req = urllib.request.Request(f"{basis_url()}/{cfg.get('graph_version', 'v26.0')}/{pfad}?{urllib.parse.urlencode(q)}")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Lesefehler: HTTP {e.code} (Token, Konto-ID, Netzwerkfreigabe prüfen).")


def protokoll(zeilen):
    kopf = ("# Änderungsprotokoll Meta-Werbekonto (BiteCentric)\n\n"
            "Jede Änderung im Werbekonto mit Datum, Begründung und erwarteter Wirkung. Neue Objekte entstehen nur pausiert.\n\n"
            "| Datum | Objekt | Kennung | Änderung | Begründung | Erwartete Wirkung |\n|---|---|---|---|---|---|\n")
    if not PROTOKOLL.exists() or not PROTOKOLL.read_text(encoding="utf-8").strip():
        PROTOKOLL.parent.mkdir(parents=True, exist_ok=True)
        PROTOKOLL.write_text(kopf, encoding="utf-8")
    with PROTOKOLL.open("a", encoding="utf-8") as f:
        for z in zeilen:
            f.write("| " + " | ".join(str(x).replace("|", "/").replace("\n", " ") for x in z) + " |\n")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    anwenden = "--anwenden" in sys.argv
    if len(args) != 1:
        sys.exit(__doc__)
    k = check.lade_json(args[0])
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))

    hart, weich = check.pruefen(k)
    for z in weich:
        print("WEICH ", z)
    if hart:
        for z in hart:
            print("HART  ", z)
        sys.exit(f"Abbruch: {len(hart)} HART-Treffer in der Prüfung. Nichts angelegt.")

    if cfg.get("freigabestufe", 1) < 2 or not cfg["ads"].get("nur_pausiert", False):
        sys.exit("Abbruch: Freigabestufe < 2 oder nur_pausiert nicht true in config/meta.json.")

    ev = cfg["umgebungsvariablen"]
    env = {"token": os.environ.get(ev["ads_token"], ""), "konto": os.environ.get(ev["werbekonto_id"], ""),
           "seite": os.environ.get(ev["seiten_id"], ""), "pixel": os.environ.get(ev["pixel_id"], "")}
    env["pixel_id"] = env["pixel"]
    plan = plan_bauen(k, cfg, env)

    print(f"\nPlan: 1 Kampagne, {len(plan['gruppen'])} Anzeigengruppe(n), {sum(len(g['anzeigen']) for g in plan['gruppen'])} Anzeige(n). Alles PAUSED.")
    if not anwenden:
        print(json.dumps(plan, ensure_ascii=False, indent=1))
        for m in plan["manuell_nachzutragen"]:
            print("MANUELL", m)
        print("\nTROCKENLAUF: nichts angelegt, kein Netzwerkzugriff. Zum Anlegen: --anwenden (nach Freigabe in config/meta.json).")
        return

    # --anwenden: alle Sperren
    if not cfg["ads"].get("schreibzugriff"):
        sys.exit("Abbruch: ads.schreibzugriff ist false in config/meta.json (Alexander schaltet es nach Token und Trockenlauf frei).")
    fehlend = [name for name, wert in (("ads_token", env["token"]), ("werbekonto_id", env["konto"]), ("seiten_id", env["seite"]), ("pixel_id", env["pixel"])) if not wert]
    if fehlend:
        sys.exit("Abbruch: Umgebungsvariable(n) fehlen: " + ", ".join(ev[n] for n in fehlend) + ". Schlüssel nur als Umgebungsvariablen setzen.")
    ids = cfg["ads"].get("zielgruppen_ids", {})
    gebraucht = ["kunden"] + list(k.get("zielgruppe", {}).get("custom_audiences", []))
    ohne = [n for n in gebraucht if not ids.get(n)]
    if ohne:
        sys.exit("Abbruch: Zielgruppen-ID fehlt in config/meta.json (ads.zielgruppen_ids): " + ", ".join(ohne))

    # Vorab: kein Platzhalter darf an die API gehen (Video ohne video_id, Bild ohne Datei, fehlende IDs)
    offen = []
    for g in plan["gruppen"]:
        for a in g["anzeigen"]:
            vd = a["creative"]["object_story_spec"].get("video_data")
            if vd is not None and "<" in str(vd.get("video_id")):
                offen.append(f"Anzeige {a['nr']}: video_id fehlt")
            if vd is None and not (a.get("bild_datei") and (ROOT / a["bild_datei"]).is_file()):
                offen.append(f"Anzeige {a['nr']}: bild_datei fehlt oder existiert nicht")
    if re.search(r"<(?!aus adimages>)[^>]*>", json.dumps({"k": plan["kampagne"], "g": [x["satz"] for x in plan["gruppen"]]})):
        offen.append("Platzhalter in Kampagne/Anzeigengruppe (z. B. Pixel- oder Zielgruppen-ID)")
    if offen:
        sys.exit("Abbruch vor dem ersten Aufruf: " + "; ".join(offen))

    konto = "act_" + re.sub(r"^act_", "", env["konto"])
    vorhanden = lese(f"{konto}/campaigns", {"fields": "name", "limit": 200}, env["token"]).get("data", [])
    if any(c.get("name") == plan["kampagne"]["name"] for c in vorhanden):
        sys.exit(f"Abbruch: Kampagne „{plan['kampagne']['name']}“ existiert schon. Nichts doppelt angelegt.")

    heute = datetime.date.today().isoformat()
    log = []
    kam = sende(f"{konto}/campaigns", plan["kampagne"], env["token"])
    log.append((heute, "Kampagne (PAUSED)", kam["id"], f"angelegt: {plan['kampagne']['name']}", k["begruendung"], k["erwartete_wirkung"]))
    print("Kampagne", kam["id"])
    try:
        for g in plan["gruppen"]:
            satz = dict(g["satz"], campaign_id=kam["id"])
            s = sende(f"{konto}/adsets", satz, env["token"])
            log.append((heute, "Anzeigengruppe (PAUSED)", s["id"], f"angelegt: {g['satz']['name']}", k["begruendung"], k["erwartete_wirkung"]))
            print("Anzeigengruppe", s["id"])
            for a in g["anzeigen"]:
                creative = a["creative"]
                if a.get("bild_datei"):
                    daten = base64.b64encode((ROOT / a["bild_datei"]).read_bytes()).decode()
                    img = sende(f"{konto}/adimages", {"bytes": daten}, env["token"])
                    h = next(iter(img["images"].values()))["hash"]
                    creative["object_story_spec"]["link_data"]["image_hash"] = h
                c = sende(f"{konto}/adcreatives", creative, env["token"])
                ad = sende(f"{konto}/ads", {"name": a["anzeige"]["name"], "adset_id": s["id"], "creative": {"creative_id": c["id"]}, "status": "PAUSED"}, env["token"])
                log.append((heute, "Anzeige (PAUSED)", ad["id"], f"angelegt: {a['anzeige']['name']}", k["begruendung"], k["erwartete_wirkung"]))
                print("Anzeige", ad["id"])
    finally:
        protokoll(log)
    for m in plan["manuell_nachzutragen"]:
        print("MANUELL", m)
    print("\nFertig. Alles PAUSED, nichts aktiviert. Alexander prüft im Werbekonto und schaltet frei. Protokoll: daten/meta/protokoll.md")


if __name__ == "__main__":
    main()
