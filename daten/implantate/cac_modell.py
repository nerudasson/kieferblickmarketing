#!/usr/bin/env python3
"""CAC-Modell Implantat-Lead-Generation. Liest annahmen.json, gibt Markdown-Tabellen aus.
Aufruf: python3 daten/implantate/cac_modell.py [--budget 7000]"""
import argparse, json, os

def rechne(s):
    r = {"cpc": s["cpc"]}
    r["klicks_pro_lead"] = 1 / s["klick_zu_lead"]
    r["kosten_lead"] = s["cpc"] * r["klicks_pro_lead"]
    r["kosten_termin"] = r["kosten_lead"] / s["lead_zu_termin"]
    r["kosten_erschienen"] = r["kosten_termin"] / s["termin_erschienen"]
    r["cac_auftrag"] = r["kosten_erschienen"] / s["erschienen_zu_auftrag"]
    r["klicks_pro_auftrag"] = r["cac_auftrag"] / s["cpc"]
    return r

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--budget", type=float); a = ap.parse_args()
    A = json.load(open(os.path.join(os.path.dirname(__file__), "annahmen.json"), encoding="utf-8"))
    budget = a.budget or A["monatsbudget_test_eur"]
    print("| Szenario | CPC | Klicks je Lead | € je Lead | € je Termin | € je erschienenem Termin | Klicks je Auftrag | CAC je Auftrag |")
    print("|---|---|---|---|---|---|---|---|")
    erg = {}
    for name, s in A["szenarien"].items():
        r = rechne(s); erg[name] = r
        print(f"| {name} | {r['cpc']:.2f} € | {r['klicks_pro_lead']:.0f} | {r['kosten_lead']:.0f} € | {r['kosten_termin']:.0f} € | {r['kosten_erschienen']:.0f} € | {r['klicks_pro_auftrag']:.0f} | **{r['cac_auftrag']:.0f} €** |")
    print(f"\nCAC in Prozent vom Fallumsatz:\n")
    print("| Szenario | " + " | ".join(f"{k} ({v} €)" for k, v in A["fallumsatz_eur"].items()) + " |")
    print("|---|" + "---|" * len(A["fallumsatz_eur"]))
    for name, r in erg.items():
        print(f"| {name} | " + " | ".join(f"{r['cac_auftrag']/v*100:.0f} %" for v in A["fallumsatz_eur"].values()) + " |")
    print(f"\nMengengerüst bei {budget:.0f} € Klickbudget pro Monat:\n")
    print("| Szenario | Klicks | Leads | Termine | erschienen | Aufträge |")
    print("|---|---|---|---|---|---|")
    for name, s in A["szenarien"].items():
        k = budget / s["cpc"]; l = k * s["klick_zu_lead"]; t = l * s["lead_zu_termin"]; e = t * s["termin_erschienen"]; au = e * s["erschienen_zu_auftrag"]
        print(f"| {name} | {k:.0f} | {l:.0f} | {t:.0f} | {e:.0f} | {au:.1f} |")
    lo_l, hi_l = A["lead_gen_preise_eur"]["pro_qualifiziertem_lead"]; lo_t, hi_t = A["lead_gen_preise_eur"]["pro_erschienenem_termin"]
    print(f"\nMarge je Einheit, wenn die Praxis pro Lead ({lo_l}–{hi_l} €) oder pro erschienenem Termin ({lo_t}–{hi_t} €) zahlt:\n")
    print("| Szenario | Kosten je Lead | Marge je Lead | Kosten je erschienenem Termin | Marge je Termin |")
    print("|---|---|---|---|---|")
    for name, r in erg.items():
        print(f"| {name} | {r['kosten_lead']:.0f} € | {lo_l-r['kosten_lead']:.0f} bis {hi_l-r['kosten_lead']:.0f} € | {r['kosten_erschienen']:.0f} € | {lo_t-r['kosten_erschienen']:.0f} bis {hi_t-r['kosten_erschienen']:.0f} € |")

if __name__ == "__main__":
    main()
