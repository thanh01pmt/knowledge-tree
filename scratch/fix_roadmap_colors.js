const fs = require('fs');
const file = 'apps/viewer/src/components/ActionRoadmapWeb.jsx';
let content = fs.readFileSync(file, 'utf8');

const colorMap = {
  '#ffffff': 'var(--surface)',
  '#e6e6e6': 'var(--border)',
  '#18181b': 'var(--ink)',
  '#5c5c66': 'var(--ink-dim)',
  '#9a9aa5': 'var(--ink-faint)',
  '#0e7c6b': 'var(--accent)',
  '#e9f6f3': 'var(--accent-bg)',
  '#b4530c': 'var(--time)',
  '#fdf1e6': 'var(--time-bg)',
  '#4f46e5': 'var(--review)',
  '#eeedfd': 'var(--review-bg)',
  '#6b6b76': 'var(--assumed)',
  '#0f9d63': 'var(--verify)',
  '#eafaf1': 'var(--verify-bg)',
  '#9adcbd': 'var(--verify)',
  '#2b78e4': 'var(--review)', // mapping to review for feature tag
  '#e7f3ff': 'var(--review-bg)',
  '#d4d4d4': 'var(--border-strong)',
  '#f5f5f5': 'var(--border)',
  '#fff': 'var(--surface)'
};

for (const [hex, cssVar] of Object.entries(colorMap)) {
  const regex = new RegExp(`'${hex}'`, 'gi');
  content = content.replace(regex, `'${cssVar}'`);
  
  // Also handle cases like: border: '1px solid #e6e6e6'
  const regex2 = new RegExp(`${hex}`, 'gi');
  content = content.replace(regex2, `${cssVar}`);
}

fs.writeFileSync(file, content);
console.log('ActionRoadmapWeb.jsx updated!');
