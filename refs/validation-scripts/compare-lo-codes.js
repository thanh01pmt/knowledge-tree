const fs = require('fs')

function readTSV(path) {
  const content = fs.readFileSync(path, 'utf8')
  const lines = content.split(/\r?\n/).filter(Boolean)
  const headers = lines[0].split('\t')
  const rows = lines.slice(1).map(line => {
    const cols = line.split('\t')
    const obj = {}
    headers.forEach((h, i) => (obj[h] = cols[i] || ''))
    return obj
  })
  return { headers, rows }
}

function extractLoCodesFromCurriculum(rows) {
  const set = new Set()
  rows.forEach((r, idx) => {
    const raw = r['activities_json'] || '[]'
    let arr = []
    try { arr = JSON.parse(raw) } catch { arr = [] }
    arr.forEach(a => {
      const codes = (a.lo_codes || '').split(',').map(s => s.trim()).filter(Boolean)
      codes.forEach(c => set.add(c))
    })
  })
  return set
}

function extractLoCodesFromLoTSV(rows) {
  const set = new Set()
  rows.forEach(r => {
    const c = r['code']?.trim()
    if (c) set.add(c)
  })
  return set
}

function main(curriculumPath, loPath) {
  const cur = readTSV(curriculumPath)
  const lo = readTSV(loPath)
  const used = extractLoCodesFromCurriculum(cur.rows)
  const available = extractLoCodesFromLoTSV(lo.rows)

  const missing = Array.from(used).filter(c => !available.has(c)).sort()
  const extra = Array.from(available).filter(c => !used.has(c)).sort()

  console.log(JSON.stringify({
    curriculumPath,
    loPath,
    counts: { used: used.size, available: available.size, missing: missing.length, extra: extra.length },
    missingPreview: missing.slice(0, 50),
  }, null, 2))
}

const [curriculumPath, loPath] = process.argv.slice(2)
if (!curriculumPath || !loPath) {
  console.error('Usage: node scripts/compare-lo-codes.js <curriculum.tsv> <learning-objectives.tsv>')
  process.exit(1)
}
main(curriculumPath, loPath)