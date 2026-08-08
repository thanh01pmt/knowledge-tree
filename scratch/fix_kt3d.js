const fs = require('fs');
const file = 'apps/viewer/src/components/KnowledgeTree3D.jsx';
let content = fs.readFileSync(file, 'utf8');

const replacements = [
  { find: /bg-\[\#252930\]/g, replace: 'bg-slate-100 dark:bg-[#252930]' },
  { find: /bg-\[\#2a2f36\]/g, replace: 'bg-slate-50 dark:bg-[#2a2f36]' },
  { find: /(?<!dark:)border-slate-800(?!\/)/g, replace: 'border-slate-200 dark:border-slate-800' },
  { find: /(?<!dark:|hover:)text-slate-300/g, replace: 'text-slate-700 dark:text-slate-300' },
  { find: /(?<!dark:)hover:bg-slate-800(?!\/)/g, replace: 'hover:bg-slate-200 dark:hover:bg-slate-800' },
  { find: /(?<!dark:)hover:text-white/g, replace: 'hover:text-slate-900 dark:hover:text-white' },
];

for (const {find, replace} of replacements) {
  content = content.replace(find, replace);
}
fs.writeFileSync(file, content);
console.log('KnowledgeTree3D fixed');
