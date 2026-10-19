export const meta = {
  name: 'artikel-batch',
  description: 'SEO-Artikel-Batch für ein Themencluster: Cluster-Plan, Einzelpläne, Belege und Beleg-Review einmal je Thema, dann je Artikel Schreiben, Review, Fix',
  whenToUse: 'Nach keyword-research (ein Thema) und pipeline.py prepare (Briefs liegen vor). args: {thema: "retainer", slugs: ["slug", ...]}. Legt keine WordPress-Entwürfe an.',
  phases: [
    { title: 'Cluster', detail: 'ein Cluster-Plan: Hauptartikel, Blickwinkel, Nebenkeywords, interne Links, Zusammenlegen' },
    { title: 'Plan', detail: 'article-planner je Artikel parallel' },
    { title: 'Belege', detail: 'ein evidence-researcher für das Thema inklusive Kostenrahmen, danach Beleg-Review' },
    { title: 'Schreiben', detail: 'je Artikel Skelett, article-writer, abschluss' },
    { title: 'Review', detail: 'je Artikel ein compliance-reviewer, nur wenn die Stichprobenregel es verlangt' },
    { title: 'Fix', detail: 'article-writer arbeitet daten/reviews/<slug>.md ab' },
  ],
}

const thema = args && args.thema
let slugs = (args && args.slugs) || []
if (!thema || !slugs.length) return { fehler: 'args.thema und args.slugs fehlen' }

const PY = 'python3 .claude/skills/seo-pipeline/scripts/'
const REVIEW = {
  type: 'object',
  properties: { uebersprungen: { type: 'boolean' }, ampel: { type: 'string', enum: ['gruen', 'gelb', 'rot'] }, wichtig: { type: 'number' } },
  required: ['uebersprungen'],
}

// Gemeinsame Stufen (Barriere ist hier richtig: Cluster-Plan, Belege und Beleg-Review brauchen alle Artikel des Themas)
phase('Cluster')
await agent(`CLUSTER-MODUS, Thema '${thema}' für ${slugs.join(', ')}. Lege daten/plaene/_cluster-${thema}.md an und lege Keywords mit gleicher Suchabsicht zusammen (Queue-Status zusammengelegt). Antwort höchstens 30 Wörter.`, { agentType: 'article-planner', label: `Cluster ${thema}`, phase: 'Cluster' })

// Zusammengelegte Artikel fallen weg
const aktiv = await agent(`Lies daten/artikel-queue.csv und gib die Slugs aus dieser Liste zurück, deren Status NICHT "zusammengelegt" ist: ${slugs.join(', ')}.`, { label: 'Aktive Slugs', phase: 'Cluster', effort: 'low', schema: { type: 'object', properties: { slugs: { type: 'array', items: { type: 'string' } } }, required: ['slugs'] } })
if (aktiv && aktiv.slugs && aktiv.slugs.length) slugs = aktiv.slugs
log(`Artikel im Cluster: ${slugs.join(', ')}`)

phase('Plan')
await parallel(slugs.map((s) => () => agent(`Erstelle den Artikelplan für den Slug "${s}" (Brief daten/briefs/${s}.md, Cluster-Plan daten/plaene/_cluster-${thema}.md) im Einzelplan-Modus. Danach plan-check ausführen und Fehler beheben. Antwort höchstens 30 Wörter.`, { agentType: 'article-planner', label: `Plan ${s}`, phase: 'Plan' })))

phase('Belege')
await agent(`Thema '${thema}' für die Pläne: ${slugs.join(', ')} (daten/plaene/). Ergänze daten/belege/${thema}.md nach deiner Agentendefinition, nur Fehlendes; Kostenrahmen-Aussagen vorab, wenn ein Artikel Intent Kosten/Vergleich hat; jede neue Aussage mit Formulierung. Antwort höchstens 40 Wörter.`, { agentType: 'evidence-researcher', label: `Belege ${thema}`, phase: 'Belege' })
await agent(`BELEG-MODUS, Thema '${thema}': prüfe daten/belege/${thema}.md und schreibe daten/reviews/_belege-${thema}.md. Antwort eine Zeile.`, { agentType: 'compliance-reviewer', label: `Beleg-Review ${thema}`, phase: 'Belege' })
await agent(`Setze die Korrekturen aus daten/reviews/_belege-${thema}.md in daten/belege/${thema}.md um (nur Aussagen und Formulierungen, kein neues Recherchieren, wenn nichts zu korrigieren ist, nichts ändern). Danach ${PY}belege_check.py validate daten/belege/${thema}.md. Antwort höchstens 20 Wörter.`, { agentType: 'evidence-researcher', label: `Beleg-Korrektur ${thema}`, phase: 'Belege' })

// Je Artikel eine Kette ohne Barrieren
const ergebnis = await pipeline(
  slugs,
  (s) => agent(`Lege das Skelett an (${PY}pipeline.py prepare --slug ${s} --no-brief), schreibe dann den Artikel für "${s}" nach deiner Agentendefinition. Beende mit ${PY}pipeline.py abschluss ${s}. Antwort höchstens 40 Wörter.`, { agentType: 'article-writer', label: `Schreiben ${s}`, phase: 'Schreiben' }).then(() => s),
  (s) => agent(`Führe ${PY}pipeline.py review ${s} aus. Steht dort "ohne Review", gib {uebersprungen: true} zurück, sonst prüfe den Artikel "${s}" im Artikel-Modus, schreibe daten/reviews/${s}.md und trage das Ergebnis mit ${PY}pipeline.py logreview ${s} <rot|gelb|gruen> <Zahl wichtiger Befunde> ein.`, { agentType: 'compliance-reviewer', label: `Review ${s}`, phase: 'Review', schema: REVIEW }).then((r) => ({ s, r })),
  async (x) => {
    if (!x || !x.r || x.r.uebersprungen || !(x.r.wichtig > 0 || x.r.ampel === 'rot')) return { slug: x && x.s, review: x && x.r, fix: false }
    await agent(`Fix-Modus für "${x.s}": arbeite daten/reviews/${x.s}.md ab (Schwere wichtig und ANNAHMEN, klein nur wenn mit einem Satz machbar), nur Edit-Patches. Dann ${PY}pipeline.py abschluss ${x.s}. Antwort höchstens 30 Wörter.`, { agentType: 'article-writer', label: `Fix ${x.s}`, phase: 'Fix' })
    return { slug: x.s, review: x.r, fix: true }
  }
)

const fertig = ergebnis.filter(Boolean)
const ausgefallen = slugs.filter((s) => !fertig.some((e) => e.slug === s))
if (ausgefallen.length) log(`Ausgefallen oder abgebrochen: ${ausgefallen.join(', ')}`)
return { thema, artikel: fertig, ausgefallen, naechster_schritt: 'pipeline.py gates, pipeline.py fragen, dann wp_publish.py nach Freigabe; nach Veröffentlichung pipeline.py live <slugs> und pipeline.py weiterlesen ' + thema }
