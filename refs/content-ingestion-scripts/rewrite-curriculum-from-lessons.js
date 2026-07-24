const fs = require('fs');
const path = require('path');

function arg(name) {
  const argv = process.argv.slice(2);
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith(`--${name}=`)) return a.split('=')[1];
    if (a === `--${name}`) return argv[i + 1];
  }
  return undefined;
}

function pad2(n) {
  return String(n).padStart(2, '0');
}

function parseXYFromText(text) {
  if (!text) return null;
  const m = String(text).match(/(\d+)\.(\d+)/);
  if (!m) return null;
  return { unit: Number(m[1]), mod: Number(m[2]) };
}

function parseLessonTitle(text) {
  const m = String(text || '').match(/^(\d+)\.(\d+)\s*:\s*(.*)$/);
  if (!m) return null;
  return { unit: Number(m[1]), mod: Number(m[2]), title: m[3].trim() };
}

function splitModuleTitle(moduleName) {
  const m = String(moduleName || '').match(/^Module\s*(\d+)\.(\d+)\s*:\s*(.*)$/i);
  if (!m) return null;
  return { unit: Number(m[1]), mod: Number(m[2]), title: m[3].trim() };
}

function rebuildRow(row, headers) {
  const idx = (name) => headers.indexOf(name);
  const courseCode = row[idx('course_code')];
  const unitName = row[idx('unit_name')];
  const moduleName = row[idx('module_name')];
  const lessonName = row[idx('lesson_name')];

  let u = null, m = null, lessonTitle = null, moduleTitle = null;

  const fromLesson = parseLessonTitle(lessonName);
  if (fromLesson) {
    u = fromLesson.unit; m = fromLesson.mod; lessonTitle = fromLesson.title;
  } else {
    const fromModule = splitModuleTitle(moduleName);
    if (fromModule) { u = fromModule.unit; m = fromModule.mod; moduleTitle = fromModule.title; }
  }
  if (u == null || m == null) {
    const fromAny = parseXYFromText(moduleName) || parseXYFromText(lessonName) || parseXYFromText(unitName);
    if (fromAny) { u = fromAny.unit; m = fromAny.mod; }
  }
  if (u == null || m == null) return row; // cannot infer

  const newUnitCode = `${courseCode}_U${pad2(u)}`;
  const newModuleCode = `${newUnitCode}_M${pad2(m)}`;
  const newLessonCode = `${newModuleCode}_L${pad2(m)}`;

  const ensuredLessonTitle = lessonTitle || moduleTitle || (lessonName ? String(lessonName).replace(/^(\d+)\.(\d+)\s*:\s*/, '') : String(moduleName).replace(/^Module\s*\d+\.\d+\s*:\s*/i, ''));
  const newLessonName = `${u}.${m}: ${ensuredLessonTitle}`.trim();
  const ensuredModuleTitle = moduleTitle || (moduleName ? String(moduleName).replace(/^Module\s*\d+\.\d+\s*:\s*/i, '') : ensuredLessonTitle);
  const newModuleName = `Module ${u}.${m}: ${ensuredModuleTitle}`.trim();

  row[idx('unit_code')] = newUnitCode;
  row[idx('module_code')] = newModuleCode;
  row[idx('lesson_code')] = newLessonCode;
  row[idx('module_name')] = newModuleName;
  row[idx('lesson_name')] = newLessonName;
  return row;
}

function parseTSV(text) {
  const lines = text.split(/\r?\n/);
  const rows = lines.filter(l => l.length > 0).map(l => l.split(/\t/));
  const headers = rows[0];
  const body = rows.slice(1);
  return { headers, body };
}

function printTSV(headers, body) {
  const lines = [headers.join('\t')];
  for (const r of body) lines.push(r.join('\t'));
  return lines.join('\n') + '\n';
}

function ensureHeaders(headers) {
  const required = ['course_code', 'unit_name', 'module_name', 'unit_code', 'module_code', 'lesson_code', 'lesson_name'];
  for (const k of required) {
    if (!headers.includes(k)) {
      throw new Error(`Missing column: ${k}`);
    }
  }
}

async function main() {
  const fileArg = arg('file');
  const inPlace = Boolean(arg('in-place'));
  if (!fileArg) {
    console.error('Usage: node scripts/rewrite-curriculum-from-lessons.js --file <tsv> [--in-place]');
    process.exit(1);
  }
  const filePath = path.isAbsolute(fileArg) ? fileArg : path.join(process.cwd(), fileArg);
  if (!fs.existsSync(filePath)) {
    console.error(`File not found: ${filePath}`);
    process.exit(1);
  }
  const text = fs.readFileSync(filePath, 'utf8');
  const { headers, body } = parseTSV(text);
  ensureHeaders(headers);

  const out = [];
  let changed = 0;
  for (const row of body) {
    const before = row.slice();
    const after = rebuildRow(row, headers);
    if (after !== before) changed++;
    out.push(after);
  }

  const printed = printTSV(headers, out);
  if (inPlace) {
    fs.writeFileSync(filePath, printed, 'utf8');
    console.log(`Updated TSV in-place: ${filePath}`);
  } else {
    const outPath = filePath.replace(/\.tsv$/i, '.rewritten.tsv');
    fs.writeFileSync(outPath, printed, 'utf8');
    console.log(`Wrote TSV: ${outPath}`);
  }
  console.log(`Rows processed: ${body.length}, rows changed: ${changed}`);
}

main().catch(e => { console.error(String(e && e.message || e)); process.exit(1); });