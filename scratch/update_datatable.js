const fs = require('fs');
const file = 'apps/viewer/src/components/DataTableView.jsx';
let code = fs.readFileSync(file, 'utf8');

// Replace export default function DataTableView({ rawTreeData, theme }) {
// with export default function DataTableView({ rawTreeData, theme, linksBySource, linksByTarget }) {
code = code.replace(
  "export default function DataTableView({ rawTreeData, theme }) {",
  "export default function DataTableView({ rawTreeData, theme, linksBySource, linksByTarget }) {"
);

const newIsRelated = `
  const isRelated = (item, type, context) => {
    if (!context || !context.item) return true;
    
    // Same item
    if (item.code === context.item.code) return true;
    
    // If same type but not same item, return false (don't show siblings)
    if (type === context.type) return false;

    // We can use linksBySource to find all descendants, and linksByTarget to find all ancestors
    const isDescendant = (startCode, targetCode) => {
      if (!linksBySource) return false;
      const visited = new Set();
      const queue = [startCode];
      while (queue.length > 0) {
        const curr = queue.shift();
        if (curr === targetCode) return true;
        if (linksBySource[curr]) {
          linksBySource[curr].forEach(child => {
            if (!visited.has(child)) {
              visited.add(child);
              queue.push(child);
            }
          });
        }
      }
      return false;
    };

    const isAncestor = (startCode, targetCode) => {
      if (!linksByTarget) return false;
      const visited = new Set();
      const queue = [startCode];
      while (queue.length > 0) {
        const curr = queue.shift();
        if (curr === targetCode) return true;
        if (linksByTarget[curr]) {
          linksByTarget[curr].forEach(parent => {
            if (!visited.has(parent)) {
              visited.add(parent);
              queue.push(parent);
            }
          });
        }
      }
      return false;
    };

    // Check if the item is a descendant of the selected context
    if (isDescendant(context.item.code, item.code)) return true;
    
    // Check if the item is an ancestor of the selected context
    if (isAncestor(context.item.code, item.code)) return true;

    return false;
  };
`;

code = code.replace(
  /const isRelated = \([\s\S]*?return false;\n  };/,
  newIsRelated.trim()
);

// We need to add linksBySource, linksByTarget to dependency array of displayedData
code = code.replace(
  "}, [rawTreeData, activeTab, searchTerm, selectedContext]);",
  "}, [rawTreeData, activeTab, searchTerm, selectedContext, linksBySource, linksByTarget]);"
);

fs.writeFileSync(file, code);
