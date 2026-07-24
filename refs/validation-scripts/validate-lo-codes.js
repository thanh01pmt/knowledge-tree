#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const CURR_PATH = path.resolve(process.argv[2] || '/Users/tonypham/MEGA/WebApp/WIP/qms-monorepo/docs/examples/ltasw-curriculum-ref.tsv');
const LO_PATH = path.resolve(process.argv[3] || '/Users/tonypham/MEGA/WebApp/WIP/qms-monorepo/docs/examples/knowledge-tree/learning-objectives-ltasw.tsv');

function readFile(p) {
  return fs.readFileSync(p, 'utf8');
}

function parseTSV(content) {
  const lines = content.split(/\r?\n/).filter(Boolean);
  const header = lines[0].split('\t');
  const rows = [];
  for (let i = 1; i < lines.length; i++) {
    const parts = lines[i].split('\t');
    // Handle potential tabs inside JSON by limiting split to header length-1 and joining rest
    if (parts.length > header.length) {
      const fixed = parts.slice(0, header.length - 1);
      fixed.push(parts.slice(header.length - 1).join('\t'));
      rows.push({ lineIndex: i + 1, data: fixed });
    } else {
      rows.push({ lineIndex: i + 1, data: parts });
    }
  }
  return { header, rows };
}

function getKnowledgeCodes(loTsv) {
  const { header, rows } = parseTSV(loTsv);
  const codeIdx = header.indexOf('code');
  const typeIdx = header.indexOf('lo_type');
  const codes = new Map();
  for (const r of rows) {
    const code = (r.data[codeIdx] || '').trim();
    if (!code) continue;
    const loType = (r.data[typeIdx] || '').trim();
    codes.set(code, { loType });
  }
  return codes;
}

function safeJSONParse(str) {
  try {
    return JSON.parse(str);
  } catch (e) {
    return null;
  }
}

function analyze(currTsv, codesMap) {
  const { header, rows } = parseTSV(currTsv);
  const idx = {
    unit: header.indexOf('unit_name'),
    module: header.indexOf('module_name'),
    lesson: header.indexOf('lesson_name'),
    activities: header.indexOf('activities_json'),
  };

  const missing = [];
  const emptyLo = [];
  const jsonErrors = [];
  const trailingEmptyTokens = [];
  const typeDistribution = new Map(); // activityType -> { UNIV, CONCEPTUAL, OTHER }
  const projectNoCIO = [];
  const labNoCIO = [];
  const quizOnlyULO = [];
  const unitEndNoULO = [];

  function addTypeCount(actType, loType) {
    const key = actType || 'UNKNOWN';
    const entry = typeDistribution.get(key) || { UNIV: 0, CONCEPTUAL_IMPL: 0, SPECIFIC_IMPL: 0, OTHER: 0, total: 0 };
    if (loType === 'UNIVERSAL') entry.UNIV++;
    else if (loType === 'CONCEPTUAL_IMPL') entry.CONCEPTUAL_IMPL++;
    else if (loType === 'SPECIFIC_IMPL') entry.SPECIFIC_IMPL++;
    else entry.OTHER++;
    entry.total++;
    typeDistribution.set(key, entry);
  }

  function isUnitEndLesson(lessonName) {
    // Detect pattern like "1.12:" or ends with ": Ôn tập"; simple numeric check for .12
    const m = /^\s*(\d+)\.(\d+)/.exec(lessonName || '');
    return m && m[2] === '12';
  }

  for (const r of rows) {
    const unit = r.data[idx.unit] || '';
    const module = r.data[idx.module] || '';
    const lesson = r.data[idx.lesson] || '';
    const actsStr = r.data[idx.activities] || '';
    const acts = safeJSONParse(actsStr);
    if (!acts) {
      jsonErrors.push({ line: r.lineIndex, unit, module, lesson });
      continue;
    }
    for (const a of acts) {
      const raw = (a.lo_codes || '').trim();
      const actType = a.type || '';
      if (!raw) {
        emptyLo.push({ line: r.lineIndex, unit, module, lesson, activity: a.name, type: actType });
        continue;
      }
      const tokens = raw.split(',').map(s => s.trim());
      for (const t of tokens) {
        if (!t) {
          trailingEmptyTokens.push({ line: r.lineIndex, unit, module, lesson, activity: a.name, type: actType });
          continue;
        }
        const meta = codesMap.get(t);
        if (!meta) {
          missing.push({ line: r.lineIndex, unit, module, lesson, activity: a.name, type: actType, code: t });
        } else {
          addTypeCount(actType, meta.loType || '');
        }
      }

      // Semantic heuristics
      const codeTypes = tokens.filter(Boolean).map(c => codesMap.get(c)?.loType).filter(Boolean);
      const hasCIO = tokens.some(c => /^CIO-/.test(c)) || codeTypes.includes('CONCEPTUAL_IMPL');
      const hasULO = tokens.some(c => /^ULO-/.test(c)) || codeTypes.includes('UNIVERSAL');
      if (actType === 'PROJECT' && !hasCIO) {
        projectNoCIO.push({ line: r.lineIndex, unit, module, lesson, activity: a.name });
      }
      if (actType === 'LAB' && !hasCIO) {
        labNoCIO.push({ line: r.lineIndex, unit, module, lesson, activity: a.name });
      }
      if (actType === 'FORMATIVE_QUIZ' && codeTypes.every(t => t === 'UNIVERSAL')) {
        quizOnlyULO.push({ line: r.lineIndex, unit, module, lesson, activity: a.name });
      }
      if (isUnitEndLesson(lesson) && (actType === 'LAB' || actType === 'DISCUSSION' || actType === 'PROJECT') && !hasULO) {
        unitEndNoULO.push({ line: r.lineIndex, unit, module, lesson, activity: a.name, type: actType });
      }
    }
  }

  return { missing, emptyLo, jsonErrors, trailingEmptyTokens, typeDistribution: Object.fromEntries(typeDistribution), projectNoCIO, labNoCIO, quizOnlyULO, unitEndNoULO };
}

function main() {
  const currTsv = readFile(CURR_PATH);
  const loTsv = readFile(LO_PATH);
  const codesMap = getKnowledgeCodes(loTsv);
  const report = analyze(currTsv, codesMap);

  const summary = {
    files: { curriculum: CURR_PATH, knowledge: LO_PATH },
    counts: {
      totalMissingCodes: report.missing.length,
      activitiesWithoutLoCodes: report.emptyLo.length,
      jsonErrors: report.jsonErrors.length,
      trailingEmptyTokens: report.trailingEmptyTokens.length,
      projectWithoutCIO: report.projectNoCIO.length,
      labWithoutCIO: report.labNoCIO.length,
      unitEndWithoutULO: report.unitEndNoULO.length,
      quizOnlyULO: report.quizOnlyULO.length,
    },
  };

  console.log('=== LO Codes Validation Summary ===');
  console.log(JSON.stringify(summary, null, 2));
  console.log('\n=== Activity Type → LO Type Distribution ===');
  for (const [type, dist] of Object.entries(report.typeDistribution)) {
    console.log(`${type}: UNIV=${dist.UNIV}, CIO=${dist.CONCEPTUAL_IMPL}, SIO=${dist.SPECIFIC_IMPL}, OTHER=${dist.OTHER}, total=${dist.total}`);
  }

  function preview(items, title, limit = 10) {
    if (!items.length) return;
    console.log(`\n--- ${title} (top ${Math.min(limit, items.length)}) ---`);
    for (const it of items.slice(0, limit)) {
      console.log(`[line ${it.line}] ${it.unit} | ${it.module} | ${it.lesson} | ${it.activity}${it.code ? ' | ' + it.code : ''}`);
    }
  }

  preview(report.missing, 'Missing LO codes');
  preview(report.emptyLo, 'Activities with empty lo_codes');
  preview(report.jsonErrors, 'JSON parse errors');
  preview(report.trailingEmptyTokens, 'Trailing empty tokens in lo_codes');
  preview(report.projectNoCIO, 'PROJECT activities without CIO');
  preview(report.labNoCIO, 'LAB activities without CIO');
  preview(report.unitEndNoULO, 'Unit-end activities without ULO');
  preview(report.quizOnlyULO, 'Formative quizzes using only ULO');

  // Exit code reflects presence of hard issues (missing codes or JSON errors)
  const hardIssues = report.missing.length + report.jsonErrors.length;
  process.exit(hardIssues ? 1 : 0);
}

main();