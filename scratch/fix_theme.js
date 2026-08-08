const fs = require('fs');

const files = [
  'apps/viewer/src/components/ControlPanel.jsx',
  'apps/viewer/src/components/NodeDetailsPanel.jsx'
];

const replacements = [
  ['bg-\\[#1a1d21\\]', 'bg-white dark:bg-[#1a1d21]'],
  ['bg-\\[#1e2227\\]', 'bg-slate-50 dark:bg-[#1e2227]'],
  ['bg-\\[#2a2f36\\]', 'bg-slate-50 dark:bg-[#2a2f36]'],
  ['bg-\\[#23272e\\]', 'bg-slate-50 dark:bg-[#23272e]'],
  ['border-slate-800', 'border-slate-200 dark:border-slate-800'],
  ['border-slate-700', 'border-slate-200 dark:border-slate-700'],
  ['text-slate-400', 'text-slate-500 dark:text-slate-400'],
  ['text-slate-300', 'text-slate-700 dark:text-slate-300'],
  ['text-slate-200', 'text-slate-800 dark:text-slate-200'],
  ['text-slate-100', 'text-slate-900 dark:text-slate-100'],
  ['bg-slate-800', 'bg-slate-100 dark:bg-slate-800'],
  ['bg-slate-700', 'bg-slate-200 dark:bg-slate-700'],
  ['bg-slate-600', 'bg-slate-300 dark:bg-slate-600'],
  ['hover:bg-slate-800', 'hover:bg-slate-100 dark:hover:bg-slate-800'],
  ['hover:bg-slate-700', 'hover:bg-slate-200 dark:hover:bg-slate-700'],
  ['hover:bg-slate-600', 'hover:bg-slate-300 dark:hover:bg-slate-600'],
  ['hover:text-slate-200', 'hover:text-slate-900 dark:hover:text-slate-200'],
  ['hover:text-slate-300', 'hover:text-slate-800 dark:hover:text-slate-300'],
  ['hover:text-slate-400', 'hover:text-slate-600 dark:hover:text-slate-400'],
  ['hover:border-slate-700', 'hover:border-slate-300 dark:hover:border-slate-700'],
  ['text-slate-500', 'text-slate-500 dark:text-slate-400'], // text-slate-500 goes to 500 in light, 400 in dark
  ['text-slate-600', 'text-slate-400 dark:text-slate-500'],
];

for (const file of files) {
  let content = fs.readFileSync(file, 'utf8');
  for (const [find, replace] of replacements) {
    const regex = new RegExp(find, 'g');
    content = content.replace(regex, replace);
  }
  fs.writeFileSync(file, content);
}
console.log('Done!');
