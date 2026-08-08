const fs = require('fs');
const file = 'apps/viewer/src/App.jsx';
let code = fs.readFileSync(file, 'utf8');

if (!code.includes("import DataTableView")) {
  code = code.replace("import ProjectGraphViewer from './components/ProjectGraphViewer';", "import ProjectGraphViewer from './components/ProjectGraphViewer';\nimport DataTableView from './components/DataTableView';");
}

code = code.replace(
  "} else if (viewMode === 'roadmap') {",
  "} else if (viewMode === 'table') {\n        return <DataTableView rawTreeData={rawTreeData} theme={theme} />;\n      } else if (viewMode === 'roadmap') {" // wait, it's ternary in the code
);

code = code.replace(
  "      ) : viewMode === 'roadmap' ? (",
  "      ) : viewMode === 'table' ? (\n        <DataTableView rawTreeData={rawTreeData} theme={theme} />\n      ) : viewMode === 'roadmap' ? ("
);

fs.writeFileSync(file, code);
