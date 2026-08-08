const fs = require('fs');
const file = 'apps/viewer/src/components/DataTableView.jsx';
let code = fs.readFileSync(file, 'utf8');

// We need to inject relatedIds useMemo before tabCounts
const relatedIdsLogic = `
  const relatedIds = useMemo(() => {
    const ids = new Set();
    if (!selectedContext || !selectedContext.item) return ids;
    const startCode = selectedContext.item.code;
    ids.add(startCode);

    if (linksBySource) {
      const queue = [startCode];
      while (queue.length > 0) {
        const curr = queue.shift();
        if (linksBySource[curr]) {
          linksBySource[curr].forEach(child => {
            if (!ids.has(child)) {
              ids.add(child);
              queue.push(child);
            }
          });
        }
      }
    }

    if (linksByTarget) {
      const queue = [startCode];
      const visited = new Set([startCode]);
      while (queue.length > 0) {
        const curr = queue.shift();
        if (linksByTarget[curr]) {
          linksByTarget[curr].forEach(parent => {
            if (!visited.has(parent)) {
              visited.add(parent);
              ids.add(parent);
              queue.push(parent);
            }
          });
        }
      }
    }
    return ids;
  }, [selectedContext, linksBySource, linksByTarget]);
`;

// Replace the old isRelated function
const newIsRelated = `
  const isRelated = (item, type, context) => {
    if (!context || !context.item) return true;
    if (type === context.type) return true;
    return relatedIds.has(item.code);
  };
`;

code = code.replace(
  /const isRelated = \([\s\S]*?return false;\n  };/,
  relatedIdsLogic + "\n" + newIsRelated.trim()
);

// We need to pass relatedIds to tabCounts dependencies
code = code.replace(
  "}, [rawTreeData, selectedContext, linksBySource, linksByTarget]);",
  "}, [rawTreeData, selectedContext, relatedIds]);"
);

// Also pass to displayedData
code = code.replace(
  "}, [rawTreeData, activeTab, searchTerm, selectedContext, linksBySource, linksByTarget]);",
  "}, [rawTreeData, activeTab, searchTerm, selectedContext, relatedIds]);"
);

fs.writeFileSync(file, code);
