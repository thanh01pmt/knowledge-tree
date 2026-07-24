const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

function arg(name) {
  const argv = process.argv.slice(2);
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith(`--${name}=`)) return a.split('=')[1];
    if (a === `--${name}`) return argv[i + 1];
  }
  return undefined;
}

function normalizeDiacritics(str) {
  return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}

function stripEmoji(str) {
  return str.replace(/[\p{Extended_Pictographic}\p{Emoji}]/gu, '');
}

function toUpperSlug(text) {
  const noEmoji = stripEmoji(text || '');
  const noDia = normalizeDiacritics(noEmoji);
  const replaced = noDia
    .replace(/['"`]/g, '')
    .replace(/[^A-Za-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .replace(/-+/g, '-');
  return replaced.toUpperCase();
}

function parseFrontMatter(text) {
  const start = text.indexOf('---\n');
  if (start !== 0) return { fm: {}, body: text };
  const endIdx = text.indexOf('\n---\n', 4);
  if (endIdx === -1) return { fm: {}, body: text };
  const fmRaw = text.slice(4, endIdx + 1).trim();
  const body = text.slice(endIdx + 5);
  const lines = fmRaw.split(/\r?\n/);
  const fm = {};
  for (const line of lines) {
    const idx = line.indexOf(':');
    if (idx === -1) continue;
    const k = line.slice(0, idx).trim();
    let v = line.slice(idx + 1).trim();
    if ((v.startsWith('[') && v.endsWith(']')) || (v.startsWith('{') && v.endsWith('}'))) {
      try { fm[k] = JSON.parse(v); } catch { fm[k] = v; }
    } else {
      fm[k] = v.replace(/^"|"$/g, '');
    }
  }
  return { fm, body };
}

function findHeadings(body) {
  const lines = body.split(/\r?\n/);
  const headings = [];
  const regex = new RegExp(
    '^#\\s*(?:Chào\\s*)?Buổi(?:\\sHọc)?\\s*(?:' +
      '(?:' +
        '(?<unit>\\d+)\\.(?<mod>\\d+)(?:\\s*-\\s*(?<modEnd>\\d+))?' +
      ')' +
    ')\\s*:?\\s*(?<title>.*)$'
  );
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    const m = line.match(regex);
    if (m) {
      const unit = Number(m.groups.unit);
      const mod = Number(m.groups.mod);
      const modEnd = m.groups.modEnd ? Number(m.groups.modEnd) : null;
      const title = (m.groups.title || '').trim();
      headings.push({ index: i, unit, modStart: mod, modEnd, rawTitle: title, rawLine: lines[i] });
    }
  }
  return { lines, headings };
}

function sliceChunks(lines, headings) {
  const chunks = [];
  for (let i = 0; i < headings.length; i++) {
    const h = headings[i];
    const endIndex = i + 1 < headings.length ? headings[i + 1].index : lines.length;
    const chunkLines = lines.slice(h.index, endIndex);
    chunks.push({ heading: h, lines: chunkLines });
  }
  return chunks;
}

function rewriteFirstHeadingLine(lines, unit, mod) {
  if (!lines.length) return lines;
  const first = lines[0];
  const replaced = first.replace(/^(#\s*(?:Chào\s*)?Buổi(?:\sHọc)?\s*)(\d+\.)(\d+(?:\s*-\s*\d+)?)(\s*:?.*)$/,
    (match, p1, p2, _p3, p4) => `${p1}${unit}.${mod}${p4 || ''}`
  );
  const out = lines.slice();
  out[0] = replaced;
  return out;
}

function printFrontMatter(obj) {
  const lines = ['---'];
  for (const [k, v] of Object.entries(obj)) {
    if (Array.isArray(v)) {
      lines.push(`${k}: ${JSON.stringify(v)}`);
    } else if (v && typeof v === 'object') {
      lines.push(`${k}: ${JSON.stringify(v)}`);
    } else {
      lines.push(`${k}: ${String(v)}`);
    }
  }
  lines.push('---');
  return lines.join('\n') + '\n\n';
}

async function main() {
  const courseCode = arg('course-code') || 'LTASW';
  const sourceDirArg = arg('source-dir');
  const outDirArg = arg('out-dir');
  const dryRun = Boolean(arg('dry-run'));
  const overwrite = Boolean(arg('overwrite'));
  const upload = Boolean(arg('upload'));
  const creatorEmail = arg('creator-email');
  const creatorId = arg('creator-id');
  const classroomId = arg('classroom-id');
  const forceUpload = Boolean(arg('force'));

  const root = process.cwd();
  const defaultSource = path.join(root, '../../docs/examples/ltasw-reading-docs');
  const sourceDir = sourceDirArg ? (path.isAbsolute(sourceDirArg) ? sourceDirArg : path.join(root, sourceDirArg)) : defaultSource;
  const outDir = outDirArg ? (path.isAbsolute(outDirArg) ? outDirArg : path.join(root, outDirArg)) : path.join(sourceDir, 'lessons');

  if (!fs.existsSync(sourceDir)) {
    console.error(`Source directory not found: ${sourceDir}`);
    process.exit(1);
  }
  if (!fs.existsSync(outDir)) {
    if (dryRun) {
      console.log(`[dry-run] would create: ${outDir}`);
    } else {
      fs.mkdirSync(outDir, { recursive: true });
    }
  }

  const files = fs.readdirSync(sourceDir).filter(f => /^part\d+\.md$/i.test(f));
  if (files.length === 0) {
    console.log('No part*.md files found');
    return;
  }

  let generated = 0;
  const warnings = [];
  for (const file of files) {
    const full = path.join(sourceDir, file);
    const text = fs.readFileSync(full, 'utf8');
    const { fm, body } = parseFrontMatter(text);
    const { lines, headings } = findHeadings(body);
    if (headings.length === 0) {
      warnings.push({ file, reason: 'no headings matched' });
      continue;
    }
    const chunks = sliceChunks(lines, headings);
    for (const chunk of chunks) {
      const h = chunk.heading;
      const unit = h.unit;
      const startMod = h.modStart;
      const endMod = h.modEnd ?? h.modStart;
      const titleName = h.rawTitle || `Unit ${unit}.${startMod}`;
      for (let mod = startMod; mod <= endMod; mod++) {
        const lesson = mod;
        const upperName = toUpperSlug(titleName);
        const filename = `${courseCode}-U${unit}-M${mod}-L${lesson}-${upperName}.md`;
        const dest = path.join(outDir, filename);

        const rewritten = rewriteFirstHeadingLine(chunk.lines, unit, mod);
        const content = rewritten.join('\n');

        const fmOut = { ...fm, title: `${h.rawLine.replace(/^#\s*/, '').trim()}` };
        const finalText = printFrontMatter(fmOut) + content;

        if (dryRun) {
          console.log(`[dry-run] ${file} → ${filename}`);
        } else {
          if (fs.existsSync(dest) && !overwrite) {
          } else {
            fs.writeFileSync(dest, finalText, 'utf8');
          }
        }
        generated++;
      }
    }
  }

  console.log(`Generated lessons: ${generated}`);
  if (warnings.length > 0) {
    console.log('Warnings:');
    for (const w of warnings) console.log(`- ${w.file}: ${w.reason}`);
  }

  if (upload) {
    const importScript = path.join(__dirname, 'import-reading-resources.js');
    if (!fs.existsSync(importScript)) {
      console.error('import-reading-resources.js not found; cannot upload');
      process.exit(1);
    }
    const args = ['--folder', outDir];
    if (creatorEmail) { args.push('--creator-email', creatorEmail); }
    if (creatorId) { args.push('--creator-id', creatorId); }
    if (classroomId) { args.push('--classroom-id', classroomId); }
    if (forceUpload) { args.push('--force'); }
    const r = spawnSync('node', [importScript, ...args], { stdio: 'inherit' });
    if (r.error) {
      console.error(String(r.error && r.error.message || r.error));
      process.exit(1);
    }
    if (typeof r.status === 'number' && r.status !== 0) {
      process.exit(r.status);
    }
  }
}

main().catch(e => { console.error(String(e && e.message || e)); process.exit(1); });