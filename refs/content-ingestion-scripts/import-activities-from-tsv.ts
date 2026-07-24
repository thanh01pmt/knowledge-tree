#!/usr/bin/env tsx
import fs from 'fs';
import path from 'path';
import { createClient } from '@supabase/supabase-js';

type TsvRow = {
  code: string;
  name: string;
  overview: string;
  activityType: string;
  context?: string;
  scenario?: string;
  steps?: string;
  blooms?: string;
};

function parseTSV(filePath: string): TsvRow[] {
  const content = fs.readFileSync(filePath, 'utf-8');
  let lines = content.split(/\r?\n/).filter(l => l.trim().length > 0);
  if (lines.length && /^code\tname\t/i.test(lines[0])) {
    lines = lines.slice(1);
  }
  const rows: TsvRow[] = [];
  for (const line of lines) {
    const cols = line.split('\t');
    if (cols.length < 2) continue;
    const [code, name, overview, activityType, context, scenario, steps, blooms] = cols;
    if ((activityType || '').toLowerCase() === 'activitytype') continue;
    rows.push({ code: code?.trim() || '', name: name?.trim() || '', overview: overview?.trim() || '', activityType: (activityType || 'other').trim(), context: context?.trim(), scenario: scenario?.trim(), steps: steps?.trim(), blooms: blooms?.trim() });
  }
  return rows;
}

function combineDescription(row: TsvRow): string {
  const parts = [row.overview, row.scenario, row.steps].filter(Boolean);
  return parts.join('\n\n');
}

async function main() {
  const TSV_PATH = path.resolve(process.argv[2] || path.resolve(process.cwd(), 'docs/examples/classroom-activities/activities-vi.tsv'));
  const ORG_CODE = process.env.ORG_CODE || process.argv[3] || '';
  const DEFAULT_LOS = (process.env.DEFAULT_LOS || process.argv[4] || '').split(',').map(s => s.trim()).filter(Boolean);

  const SUPABASE_URL = process.env.SUPABASE_URL || process.env.NEXT_PUBLIC_SUPABASE_URL || '';
  const SUPABASE_SERVICE_ROLE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY || '';
  if (!SUPABASE_URL || !SUPABASE_SERVICE_ROLE_KEY) {
    console.error('Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in env.');
    process.exit(1);
  }

  if (!ORG_CODE) {
    console.error('Missing ORG_CODE (env ORG_CODE or argv[3]).');
    process.exit(1);
  }

  const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY);

  const rows = parseTSV(TSV_PATH);
  let success = 0, failed = 0;

  for (const row of rows) {
    const name = row.name || row.code;
    const description = combineDescription(row);
    const activityType = (row.activityType || 'OTHER').trim();
    const loCodes = DEFAULT_LOS; // For now, use global defaults; per-row LO can be added later

    const { data, error } = await supabase.rpc('upsert_master_activity_with_los', {
      p_id: null,
      p_name: name,
      p_description: description || null,
      p_activity_type: activityType,
      p_organization_code: ORG_CODE,
      p_lo_codes: loCodes,
      p_is_sample: true,
    }).select();

    if (error) {
      failed++;
      console.error(`Import failed for code=${row.code} name=${name}:`, error.message);
    } else {
      success++;
      console.log(`Imported: ${name} (${activityType})`);
    }
  }

  console.log(`Import finished: success=${success}, failed=${failed}`);
}

main().catch(e => { console.error(e); process.exit(1); });