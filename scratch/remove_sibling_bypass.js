const fs = require('fs');
const file = 'apps/viewer/src/components/DataTableView.jsx';
let code = fs.readFileSync(file, 'utf8');

const oldIsRelated = `
  const isRelated = (item, type, context) => {
    if (!context || !context.item) return true;
    if (type === context.type) return true;
    return relatedIds.has(item.code);
  };
`;

const newIsRelated = `
  const isRelated = (item, type, context) => {
    if (!context || !context.item) return true;
    return relatedIds.has(item.code);
  };
`;

code = code.replace(oldIsRelated.trim(), newIsRelated.trim());

fs.writeFileSync(file, code);
