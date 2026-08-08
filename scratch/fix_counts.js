const fs = require('fs');
const file = 'apps/viewer/src/components/DataTableView.jsx';
let code = fs.readFileSync(file, 'utf8');

// Inside the component, we should calculate the filtered count for each tab
const countsLogic = `
  const getFilteredCount = (tabId) => {
    if (!rawTreeData || !rawTreeData[tabId]) return 0;
    if (!selectedContext) return rawTreeData[tabId].length;
    return rawTreeData[tabId].filter(item => isRelated(item, tabId, selectedContext)).length;
  };
`;

code = code.replace(
  "const displayedData = useMemo(() => {",
  countsLogic + "\n  const displayedData = useMemo(() => {"
);

code = code.replace(
  "const count = rawTreeData && rawTreeData[tab.id] ? rawTreeData[tab.id].length : 0;",
  "const count = getFilteredCount(tab.id);"
);

fs.writeFileSync(file, code);
