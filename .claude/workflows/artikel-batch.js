export const meta = {
  name: 'artikel-batch',
  description: 'SEO-Artikel-Batch: je Artikel eine Kette Plan, Belege (einmal je Thema), Schreiben, Review, Fix, ohne Stufen-Barrieren',
  whenToUse: 'Nach keyword-research und pipeline.py prepare (Briefs liegen vor). args: {slugs: ["slug", ...]}. Legt keine WordPress-Entwürfe an.',
  phases: [
    { title: 'Plan', detail: 'article-planner je Artikel' },
    { title: 'Belege', detail: 'evidence-researcher einmal je Thema, sobald alle Pläne des Themas da sind' },
    { title: 'Schreiben', detail: 'Skelett, article-writer, abschluss' },
    { title: 'Review', detail: 'je Artikel ein compliance-reviewer, nur wenn die Stichprobenregel es verlangt' },
    { title: 'Fix', detail: 'article-writer arbeitet daten/reviews/<slug>.md ab' },
  ],
}

const slugs = (args && args.slugs) || []
if (!slugs.length) return { fehler: 'args.slugs fehlt' }

const PY = 'python3 .claude/skills/seo-pipeline/scripts/'
const REVIEW = {
  type: 'object',
  properties: { uebersprungen: { type: 'boolean' }, ampel: { type: 'string', enum: ['gruen', 'gelb', 'rot'] }, wichtig: { type: 'number' } },
  required: ['uebersprungen'],
}

// Thema je Artikel und Tor je Thema: der Researcher startet, sobald der letzte Plan des Themas fertig ist.
const THEMA = await agent(
  `Lies daten/artikel-queue.csv und gib für diese Slugs ihr Feld "thema" zurück: ${slugs.join(', ')}. Keine weitere Arbeit.`,
  { label: 'Themen lesen', phase: 'Plan', effort: 'low', schema: { type: 'object', properties: { zuordnung: { type: 'object', additionalProperties: { type: 'string' } } }, required: ['zuordnung'] } }
)
const thema = (s) => (THEMA && THEMA.zuordnung && THEMA.zuordnung[s]) || 'unbekannt'
const tore = {}
for (const s of slugs) {
  const t = thema(s)
  if (!tore[t]) {
    let auf
    tore[t] = { offen: 0, slugs: [], fertig: new Promise((r) => { auf = r }), auf, gestartet: false }
  }
  tore[t].offen++
  tore[t].slugs.push(s)
}

const ergebnis = await pipeline(
  slugs,
  // Stufe 1: Plan
  (s) => agent(`Erstelle den Artikelplan für den Slug "${s}" (Brief daten/briefs/${s}.md) nach deiner Agentendefinition. Danach plan-check ausführen und Fehler beheben. Antwort höchstens 30 Wörter.`, { agentType: 'article-planner', label: `Plan ${s}`, phase: 'Plan' }).then(() => s),
  // Stufe 2: Belege einmal je Thema
  async (s) => {
    const t = thema(s)
    const tor = tore[t]
    tor.offen--
    if (tor.offen === 0 && !tor.gestartet) {
      tor.gestartet = true
      agent(`Thema '${t}' für die Pläne: ${tor.slugs.join(', ')} (daten/plaene/). Ergänze daten/belege/${t}.md nach deiner Agentendefinition, nur Fehlendes; Kostenrahmen-Aussagen vorab, wenn ein Artikel Intent Kosten/Vergleich hat. Antwort höchstens 40 Wörter.`, { agentType: 'evidence-researcher', label: `Belege ${t}`, phase: 'Belege' })
        .then(() => tor.auf(true), () => tor.auf(false))
    }
    await tor.fertig
    return s
  },
  // Stufe 3: Skelett, Schreiben, Endstand
  (s) => agent(`Lege das Skelett an (${PY}pipeline.py prepare --slug ${s} --no-brief), schreibe dann den Artikel für "${s}" nach deiner Agentendefinition. Beende mit ${PY}pipeline.py abschluss ${s}. Antwort höchstens 40 Wörter.`, { agentType: 'article-writer', label: `Schreiben ${s}`, phase: 'Schreiben' }).then(() => s),
  // Stufe 4: Review nur, wenn die Stichprobenregel es verlangt
  (s) => agent(`Führe ${PY}pipeline.py review ${s} aus. Steht dort "ohne Review", gib {uebersprungen: true} zurück, sonst prüfe den Artikel "${s}" nach deiner Agentendefinition, schreibe daten/reviews/${s}.md und trage das Ergebnis mit ${PY}pipeline.py logreview ${s} <rot|gelb|gruen> <Zahl wichtiger Befunde> ein.`, { agentType: 'compliance-reviewer', label: `Review ${s}`, phase: 'Review', schema: REVIEW }).then((r) => ({ s, r })),
  // Stufe 5: Fix nur bei wichtigen Befunden
  async (x) => {
    if (!x || !x.r || x.r.uebersprungen || !(x.r.wichtig > 0 || x.r.ampel === 'rot')) return { slug: x && x.s, review: x && x.r, fix: false }
    await agent(`Fix-Modus für "${x.s}": arbeite daten/reviews/${x.s}.md ab (Schwere wichtig und ANNAHMEN, klein nur wenn mit einem Satz machbar), nur Edit-Patches. Dann ${PY}pipeline.py abschluss ${x.s}. Antwort höchstens 30 Wörter.`, { agentType: 'article-writer', label: `Fix ${x.s}`, phase: 'Fix' })
    return { slug: x.s, review: x.r, fix: true }
  }
)

const fertig = ergebnis.filter(Boolean)
const ausgefallen = slugs.filter((s) => !fertig.some((e) => e.slug === s))
if (ausgefallen.length) log(`Ausgefallen oder abgebrochen: ${ausgefallen.join(', ')}`)
return { artikel: fertig, ausgefallen, naechster_schritt: 'pipeline.py gates, dann wp_publish.py nach Freigabe durch Alexander' }
