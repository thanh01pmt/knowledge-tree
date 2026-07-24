const fs = require('fs')
const path = require('path')

const CANONICAL_TYPES = new Set([
  'CASE_STUDY',
  'COLLABORATION',
  'ENGAGE',
  'FORMATIVE_QUIZ',
  'GUIDED_INQUIRY',
  'LECTURE',
  'OTHER',
  'PORTFOLIO_SUB',
  'PRACTICE_DRILL',
  'PRESENTATION',
  'PROJECT_TASK',
  'READING',
  'SELF_ASSESSMENT',
  'SIMULATION',
  'SUMMATIVE_EXAM',
  'VIDEO',
  'DOC',
  'CODING_TASK',
  'LAB',
  'PROJECT',
  'REFERENCE_LINK',
  'DISCUSSION'
])

const SYNONYMS = {
  QUIZ: 'FORMATIVE_QUIZ',
  MCQ: 'FORMATIVE_QUIZ',
  CODING_EXERCISE: 'CODING_TASK',
  CODE_TASK: 'CODING_TASK',
  PRACTICE: 'PRACTICE_DRILL',
  GROUP_WORK: 'COLLABORATION',
  TALK: 'LECTURE',
  SLIDES: 'LECTURE',
  ARTICLE: 'READING',
  LINK: 'REFERENCE_LINK',
  DISCUSS: 'DISCUSSION',
  PRESENT: 'PRESENTATION',
  PROJECT_ASSIGNMENT: 'PROJECT_TASK'
}

function normalizeType(raw) {
  const base = raw.trim().toUpperCase().replace(/\s+/g, '_')
  if (CANONICAL_TYPES.has(base)) return { normalized: base, changed: base !== raw, unknown: false }
  const syn = SYNONYMS[base]
  if (syn && CANONICAL_TYPES.has(syn)) return { normalized: syn, changed: true, unknown: false }
  return { normalized: base, changed: false, unknown: !CANONICAL_TYPES.has(base) }
}

function processFile(inputPath, outputPath) {
  const content = fs.readFileSync(inputPath, 'utf8')
  const lines = content.split(/\r?\n/)
  if (lines.length < 2) throw new Error('Empty TSV')
  const headers = lines[0].split('\t')
  const idx = {
    activities: headers.indexOf('activities_json')
  }
  if (idx.activities === -1) throw new Error('Missing activities_json column')

  const conversions = {}
  const unknowns = {}

  const out = [lines[0]]
  for (let i = 1; i < lines.length; i++) {
    const line = lines[i]
    if (!line.trim()) continue
    const cols = line.split('\t')
    const rawJson = cols[idx.activities]
    let arr
    try {
      arr = JSON.parse(rawJson || '[]')
    } catch {
      out.push(line)
      continue
    }
    const updated = arr.map(a => {
      const res = normalizeType(a.type || '')
      if (res.changed) conversions[`${a.type}→${res.normalized}`] = (conversions[`${a.type}→${res.normalized}`] || 0) + 1
      if (res.unknown) unknowns[res.normalized] = (unknowns[res.normalized] || 0) + 1
      return { name: a.name, type: res.normalized, lo_codes: a.lo_codes }
    })
    cols[idx.activities] = JSON.stringify(updated)
    out.push(cols.join('\t'))
  }

  const finalOut = out.join('\n')
  const target = outputPath || path.join(path.dirname(inputPath), path.basename(inputPath, path.extname(inputPath)) + '.normalized.tsv')
  fs.writeFileSync(target, finalOut, 'utf8')

  const convKeys = Object.keys(conversions)
  const unkKeys = Object.keys(unknowns)
  const report = {
    outputPath: target,
    conversions: convKeys.map(k => ({ rule: k, count: conversions[k] })),
    unknownTypes: unkKeys.map(k => ({ type: k, count: unknowns[k] }))
  }
  console.log(JSON.stringify(report, null, 2))
}

const argv = process.argv.slice(2)
if (argv.length < 1) {
  console.error('Usage: node scripts/normalize-curriculum-tsv.js <input.tsv> [output.tsv]')
  process.exit(1)
}
processFile(argv[0], argv[1])