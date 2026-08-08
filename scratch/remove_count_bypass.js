const fs = require('fs');
const file = 'apps/viewer/src/components/DataTableView.jsx';
let code = fs.readFileSync(file, 'utf8');

const bypassLogic = `
      // If it's the active context type, don't filter siblings for count
      if (tab.id === selectedContext.type) {
        counts[tab.id] = rawTreeData[tab.id].length;
        return;
      }
`;

code = code.replace(bypassLogic, "");

fs.writeFileSync(file, code);
