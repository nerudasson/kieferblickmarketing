export const meta = {
  name: 'artikel-batch',
  description: 'SEO-Artikel-Batch für ein Themencluster (schlanke Kette): Cluster-Plan mit allen Einzelplänen, Belege + Beleg-Review einmal, dann je Artikel Schreiben (Schreibpaket) und Review mit Skript-Patch',
  whenToUse: 'Nach keyword-research (ein Thema) und pipeline.py prepare (Briefs liegen vor). args: {thema: "aligner", slugs: ["slug", ...]}. Legt keine WordPress-Entwürfe an. Läuft mit höchstens (CPUs - 2) Agenten gleichzeitig.',
  phases: [
    { title: 'Cluster', detail: 'ein Planer: Cluster-Plan, Zusammenlegen, alle Einzelpläne' },
    { title: 'Belege', detail: 'ein Researcher für das Thema, ein Beleg-Review, Korrektur nur bei wichtigen Befunden' },
    { title: 'Schreiben', detail: 'je Artikel Paket, Skelett, article-writer, abschluss' },
    { title: 'Review', detail: 'je Artikel ein compliance-reviewer: Befunde als Patches, Skript wendet an' },
    { title: 'Fix', detail: 'article-writer nur, wenn Patches offen blieben oder der Endstand nicht grün ist' },
  ],
}

const thema = args && args.thema
let slugs = (args && args.slugs) || []
if (!thema || !slugs.length) return { fehler: 'args.thema und args.slugs fehlen' }

const PY = 'python3 .claude/skills/seo-pipeline/scripts/'
const CLUSTER = {
  type: 'object',
  properties: { aktiv: { type: 'array', items: { type: 'string' } }, ohne_plan: { type: 'array', items: { type: 'string' } } },
  required: ['aktiv', 'ohne_plan'],
}
const BELEG = { type: 'object', properties: { wichtig: { type: 'number' } }, required: ['wichtig'] }
const REVIEW = {
  type: 'object',
  properties: {
    uebersprungen: { type: 'boolean' },
    ampel: { type: 'string', enum: ['gruen', 'gelb', 'rot'] },
    wichtig: { type: 'number' },
    offen: { type: 'number' },
    endstand: { type: 'string', enum: ['ok', 'pruefen'] },
  },
  required: ['uebersprungen'],
}

phase('Cluster')
const c = await agent(
  `CLUSTER-MODUS, Thema '${thema}' für ${slugs.join(', ')}. Lege daten/plaene/_cluster-${thema}.md an, lege Keywords mit gleicher Suchabsicht zusammen (Queue-Status zusammengelegt) und schreibe danach die Einzelpläne aller aktiven Artikel samt plan-check. Gib {aktiv: Slugs ohne zusammengelegte, ohne_plan: aktive Slugs, deren Plan fehlt oder den plan-check nicht besteht} zurück.`,
  { agentType: 'article-planner', label: `Cluster + Pläne ${thema}`, phase: 'Cluster', schema: CLUSTER }
)
if (c && c.aktiv && c.aktiv.length) slugs = c.aktiv
log(`Artikel im Cluster: ${slugs.join(', ')}`)
if (c && c.ohne_plan && c.ohne_plan.length) {
  log(`Einzelpläne nachholen: ${c.ohne_plan.join(', ')}`)
  await parallel(c.ohne_plan.map((s) => () => agent(`Erstelle im Einzelplan-Modus den Artikelplan für "${s}" (Brief daten/briefs/${s}.md, Cluster-Plan daten/plaene/_cluster-${thema}.md), danach plan-check. Antwort höchstens 30 Wörter.`, { agentType: 'article-planner', label: `Plan ${s}`, phase: 'Cluster' })))
}

phase('Belege')
await agent(`Thema '${thema}' für die Pläne: ${slugs.join(', ')} (daten/plaene/). Beginne mit den gemeinsamen Belegfragen im Cluster-Plan (Kostenrahmen zuerst). Ergänze daten/belege/${thema}.md nach deiner Agentendefinition, nur Fehlendes; jede neue Aussage mit Formulierung. Antwort höchstens 40 Wörter.`, { agentType: 'evidence-researcher', label: `Belege ${thema}`, phase: 'Belege' })
const br = await agent(`BELEG-MODUS, Thema '${thema}': prüfe daten/belege/${thema}.md und schreibe daten/reviews/_belege-${thema}.md. Gib {wichtig: Zahl der wichtigen Befunde} zurück.`, { agentType: 'compliance-reviewer', label: `Beleg-Review ${thema}`, phase: 'Belege', schema: BELEG })
if (br && br.wichtig > 0) {
  await agent(`Setze die Korrekturen aus daten/reviews/_belege-${thema}.md in daten/belege/${thema}.md um (nur Aussagen und Formulierungen, kein neues Recherchieren). Danach ${PY}belege_check.py validate daten/belege/${thema}.md. Antwort höchstens 20 Wörter.`, { agentType: 'evidence-researcher', label: `Beleg-Korrektur ${thema}`, phase: 'Belege' })
} else {
  log('Beleg-Review ohne wichtige Befunde: keine Korrektur nötig')
}

const ergebnis = await pipeline(
  slugs,
  (s) => agent(`Lege das Skelett an (${PY}pipeline.py prepare --slug ${s} --no-brief) und das Schreibpaket (${PY}pipeline.py paket ${s}). Schreibe dann den Artikel für "${s}" nach deiner Agentendefinition. Beende mit ${PY}pipeline.py abschluss ${s}. Antwort höchstens 40 Wörter.`, { agentType: 'article-writer', label: `Schreiben ${s}`, phase: 'Schreiben' }).then(() => s),
  (s) => agent(`Führe ${PY}pipeline.py review ${s} aus. Steht dort "ohne Review", gib {uebersprungen: true} zurück. Sonst prüfe den Artikel "${s}" im Artikel-Modus, schreibe daten/reviews/${s}.md mit PATCHES, führe ${PY}pipeline.py patch ${s} aus und trage das Ergebnis mit ${PY}pipeline.py logreview ${s} <rot|gelb|gruen> <Zahl wichtiger Befunde> ein. Gib {uebersprungen:false, ampel, wichtig, offen, endstand} zurück.`, { agentType: 'compliance-reviewer', label: `Review ${s}`, phase: 'Review', schema: REVIEW }).then((r) => ({ s, r })),
  async (x) => {
    const r = x && x.r
    if (!r || r.uebersprungen || (!(r.offen > 0) && r.endstand !== 'pruefen' && r.ampel !== 'rot')) return { slug: x && x.s, review: r, fix: false }
    await agent(`Fix-Modus für "${x.s}": In daten/reviews/${x.s}.md sind Befunde offen geblieben (Block OFFEN) oder der Endstand ist nicht grün (${PY}pipeline.py abschluss ${x.s} zeigt den Grund). Arbeite genau das ab, nur Edit-Patches, danach abschluss. Antwort höchstens 30 Wörter.`, { agentType: 'article-writer', label: `Fix ${x.s}`, phase: 'Fix' })
    return { slug: x.s, review: r, fix: true }
  }
)

const fertig = ergebnis.filter(Boolean)
const ausgefallen = slugs.filter((s) => !fertig.some((e) => e.slug === s))
if (ausgefallen.length) log(`Ausgefallen oder abgebrochen: ${ausgefallen.join(', ')}`)
return { thema, artikel: fertig, ausgefallen, naechster_schritt: 'pipeline.py gates, pipeline.py fragen, dann wp_publish.py nach Freigabe; nach Veröffentlichung pipeline.py live <slugs> und pipeline.py weiterlesen ' + thema }
