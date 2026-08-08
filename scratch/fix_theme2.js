const fs = require('fs');

const files = [
  'apps/viewer/src/components/ControlPanel.jsx',
  'apps/viewer/src/components/NodeDetailsPanel.jsx'
];

const replacements = [
  { find: /bg-\[\#1a1d21\]/g, replace: 'bg-white dark:bg-[#1a1d21]' },
  { find: /bg-\[\#1e2227\]/g, replace: 'bg-slate-50 dark:bg-[#1e2227]' },
  { find: /bg-\[\#2a2f36\]/g, replace: 'bg-slate-50 dark:bg-[#2a2f36]' },
  { find: /bg-\[\#23272e\]/g, replace: 'bg-slate-50 dark:bg-[#23272e]' },
  
  { find: /(?<!dark:)border-slate-800(?!\/)/g, replace: 'border-slate-200 dark:border-slate-800' },
  { find: /(?<!dark:)border-slate-700(?!\/)/g, replace: 'border-slate-200 dark:border-slate-700' },
  
  { find: /(?<!dark:|hover:)text-slate-500/g, replace: 'text-slate-600 dark:text-slate-500' },
  { find: /(?<!dark:|hover:)text-slate-400/g, replace: 'text-slate-500 dark:text-slate-400' },
  { find: /(?<!dark:|hover:)text-slate-300/g, replace: 'text-slate-700 dark:text-slate-300' },
  { find: /(?<!dark:|hover:)text-slate-200/g, replace: 'text-slate-800 dark:text-slate-200' },
  { find: /(?<!dark:|hover:)text-slate-100/g, replace: 'text-slate-900 dark:text-slate-100' },
  
  { find: /(?<!dark:|hover:)bg-slate-800(?!\/)/g, replace: 'bg-slate-100 dark:bg-slate-800' },
  { find: /(?<!dark:|hover:)bg-slate-700(?!\/)/g, replace: 'bg-slate-200 dark:bg-slate-700' },
  { find: /(?<!dark:|hover:)bg-slate-600(?!\/)/g, replace: 'bg-slate-300 dark:bg-slate-600' },
  
  { find: /(?<!dark:)hover:bg-slate-800(?!\/)/g, replace: 'hover:bg-slate-200 dark:hover:bg-slate-800' },
  { find: /(?<!dark:)hover:bg-slate-700(?!\/)/g, replace: 'hover:bg-slate-300 dark:hover:bg-slate-700' },
  { find: /(?<!dark:)hover:bg-slate-600(?!\/)/g, replace: 'hover:bg-slate-400 dark:hover:bg-slate-600' },
  
  { find: /(?<!dark:)hover:text-slate-200/g, replace: 'hover:text-slate-900 dark:hover:text-slate-200' },
  { find: /(?<!dark:)hover:text-slate-300/g, replace: 'hover:text-slate-800 dark:hover:text-slate-300' },
  { find: /(?<!dark:)hover:text-slate-400/g, replace: 'hover:text-slate-600 dark:hover:text-slate-400' },
  
  { find: /(?<!dark:)hover:border-slate-700(?!\/)/g, replace: 'hover:border-slate-300 dark:hover:border-slate-700' },
  { find: /(?<!dark:)hover:text-white/g, replace: 'hover:text-slate-900 dark:hover:text-white' },
];

for (const file of files) {
  let content = fs.readFileSync(file, 'utf8');
  for (const {find, replace} of replacements) {
    content = content.replace(find, replace);
  }
  fs.writeFileSync(file, content);
}
console.log('Done safer replacement!');
