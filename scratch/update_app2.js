const fs = require('fs');
const file = 'apps/viewer/src/App.jsx';
let code = fs.readFileSync(file, 'utf8');

code = code.replace(
  "<DataTableView rawTreeData={rawTreeData} theme={theme} />",
  "<DataTableView \n          rawTreeData={rawTreeData} \n          theme={theme} \n          linksBySource={linksBySource} \n          linksByTarget={linksByTarget} \n        />"
);

fs.writeFileSync(file, code);
