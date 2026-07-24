const fs = require('fs');
const path = require('path');
require('dotenv').config({ path: path.join(process.cwd(), '.env') });
const { createClient } = require('@supabase/supabase-js');

function arg(name) {
  const argv = process.argv.slice(2);
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith(`--${name}=`)) return a.split('=')[1];
    if (a === `--${name}`) return argv[i + 1];
  }
  return undefined;
}

function toCodeFromFilename(filename) {
  const base = path.basename(filename, path.extname(filename));
  const m = base.match(/^part(\d+)$/i);
  if (m) return `LTASW_RD_PART_${m[1]}`;
  return base
    .replace(/[^a-zA-Z0-9]+/g, '_')
    .replace(/^_+|_+$/g, '')
    .toUpperCase();
}

function parseFrontMatter(text) {
  if (!text.startsWith('---\n')) return {};
  const end = text.indexOf('\n---\n');
  if (end === -1) return {};
  const raw = text.slice(4, end + 1).trim();
  const lines = raw.split(/\r?\n/);
  const out = {};
  for (const line of lines) {
    const idx = line.indexOf(':');
    if (idx === -1) continue;
    const k = line.slice(0, idx).trim();
    let v = line.slice(idx + 1).trim();
    if ((v.startsWith('[') && v.endsWith(']')) || (v.startsWith('{') && v.endsWith('}'))) {
      try { out[k] = JSON.parse(v); } catch { out[k] = v; }
    } else {
      out[k] = v.replace(/^"|"$/g, '');
    }
  }
  return out;
}

function extractTitle(text) {
  const lines = text.split(/\r?\n/);
  for (const l of lines) {
    const m = l.match(/^#\s+(.*)$/);
    if (m) return m[1].trim();
  }
  return null;
}

function extractDescription(text) {
  const body = text.replace(/^---[\s\S]*?---\n/, '');
  const paras = body.split(/\r?\n\r?\n/).map(s => s.trim()).filter(Boolean);
  for (const p of paras) {
    if (!p.startsWith('#')) return p.length > 220 ? p.slice(0, 220) : p;
  }
  return null;
}

async function main() {
  const creatorEmail = arg('creator-email');
  const creatorIdArg = arg('creator-id');
  const force = Boolean(arg('force'));
  const classroomId = arg('classroom-id');
  const folderArg = arg('folder');
  const root = process.cwd();
  const defaultFolder = path.join(root, '../../docs/examples/ltasw-reading-docs');
  const folder = folderArg ? path.isAbsolute(folderArg) ? folderArg : path.join(root, folderArg) : defaultFolder;

  const url = process.env.SUPABASE_URL || process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) {
    console.error('Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY');
    process.exit(1);
  }
  if (!creatorEmail && !creatorIdArg) {
    console.error('Missing required --creator-email or --creator-id');
    process.exit(1);
  }

  const supabase = createClient(url, key);

  const BUCKET_NAME = 'learning_resources';
  const buckets = await supabase.storage.listBuckets();
  if (buckets.error) {
    console.error('Failed to list storage buckets:', buckets.error.message);
    process.exit(1);
  }
  const exists = (buckets.data || []).some(b => b.name === BUCKET_NAME);
  if (!exists) {
    const created = await supabase.storage.createBucket(BUCKET_NAME, { public: false });
    if (created.error) {
      console.error('Failed to create storage bucket:', created.error.message);
      process.exit(1);
    }
  }

  let organizationCode;
  let creatorId;
  if (creatorIdArg) {
    const profById = await supabase.from('profiles').select('id,organization_code').eq('id', creatorIdArg).maybeSingle();
    if (profById.error || !profById.data) {
      console.error('Could not resolve creator profile by id');
      process.exit(1);
    }
    creatorId = profById.data.id;
    organizationCode = profById.data.organization_code;
  } else {
    const profRes = await supabase.rpc('get_profile_by_email', { p_email: creatorEmail });
    if (profRes.error || !Array.isArray(profRes.data) || profRes.data.length === 0) {
      console.error('Could not resolve creator profile by email');
      process.exit(1);
    }
    const creatorProfile = profRes.data[0];
    organizationCode = creatorProfile.organization_code;
    creatorId = creatorProfile.id;
  }
  if (!organizationCode) {
    console.error('Creator profile missing organization_code');
    process.exit(1);
  }

  const files = fs.readdirSync(folder).filter(f => f.toLowerCase().endsWith('.md'));
  let ok = 0;
  const errors = [];

  for (const file of files) {
    try {
      const full = path.join(folder, file);
      const content = fs.readFileSync(full, 'utf8');
      const fm = parseFrontMatter(content);
      const title = (fm.title && String(fm.title)) || extractTitle(content) || path.basename(file, '.md');
      const description = (fm.description && String(fm.description)) || extractDescription(content) || null;
      const learningObjectiveCodes = Array.isArray(fm.learningObjectiveCodes) ? fm.learningObjectiveCodes : [];
      const code = (fm.code && String(fm.code)) || toCodeFromFilename(file);
      const storagePath = `${organizationCode}/reading/${code}`;
      const stat = fs.statSync(full);
      const fileMetadata = { name: file, size: stat.size, mimeType: 'text/markdown' };

      const upload = await supabase.storage.from(BUCKET_NAME).upload(storagePath, content, { contentType: 'text/markdown', upsert: true });
      if (upload.error) {
        const msg = upload.error.message || '';
        const existsMsg = msg.toLowerCase().includes('already exists');
        if (force && existsMsg) {
          const upd = await supabase.storage.from(BUCKET_NAME).update(storagePath, content, { contentType: 'text/markdown' });
          if (upd.error) throw new Error(upd.error.message);
        } else if (!force && existsMsg) {
          // proceed without changing storage
        } else {
          throw new Error(upload.error.message);
        }
      }

      let resource;

      const existing = await supabase
        .from('learning_resources')
        .select('id')
        .eq('code', code)
        .eq('organization_code', organizationCode)
        .maybeSingle();

      const upsert = await supabase.rpc('upsert_resource_with_los', {
        p_id: null,
        p_code: code,
        p_title: title,
        p_description: description,
        p_resource_type: 'FILE',
        p_url: null,
        p_storage_path: storagePath,
        p_file_metadata: fileMetadata,
        p_organization_code: organizationCode,
        p_created_by: creatorId,
        p_lo_codes: learningObjectiveCodes
      }).select().single();
      if (upsert.error) {
        const msg = upsert.error.message || '';
        const missingFn = msg.includes('Could not find the function') || msg.includes('function') && msg.includes('not found');
        if (!missingFn) throw new Error(upsert.error.message);
        if (existing.data && !force) {
          resource = existing.data;
        } else if (existing.data && force) {
          const upd = await supabase
            .from('learning_resources')
            .update({
              title,
              description,
              url: null,
              storage_path: storagePath,
              file_metadata: fileMetadata,
              created_by: creatorId
            })
            .eq('id', existing.data.id)
            .select()
            .single();
          if (upd.error || !upd.data) throw new Error(upd.error ? upd.error.message : 'Update failed');
          resource = upd.data;
        } else {
          const ins = await supabase.from('learning_resources').insert({
            code,
            title,
            description,
          resource_type: 'FILE',
            url: null,
            storage_path: storagePath,
            file_metadata: fileMetadata,
            organization_code: organizationCode,
            created_by: creatorId
          }).select().single();
          if (ins.error || !ins.data) throw new Error(ins.error ? ins.error.message : 'Insert failed');
          resource = ins.data;
        }
      } else {
        resource = upsert.data;
      }

      if (classroomId) {
        const pin = await supabase.rpc('pin_resource_to_classroom', {
          p_classroom_id: classroomId,
          p_resource_id: resource.id,
          p_user_id: creatorId
        });
        if (pin.error) throw new Error(pin.error.message);
        console.log(`${code} imported and pinned`);
      } else {
        console.log(`${code} imported`);
      }
      ok++;
    } catch (e) {
      errors.push({ file, error: String(e && e.message || e) });
      console.error(`Error on ${file}: ${String(e && e.message || e)}`);
    }
  }

  console.log(`Imported: ${ok}, Failed: ${errors.length}`);
  if (errors.length > 0) {
    for (const item of errors) {
      console.log(`- ${item.file}: ${item.error}`);
    }
  }
}

main().catch(e => { console.error(String(e && e.message || e)); process.exit(1); });