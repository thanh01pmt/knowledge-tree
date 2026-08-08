const fs = require('fs');

// 1. App.jsx
const appFile = 'apps/viewer/src/App.jsx';
let appCode = fs.readFileSync(appFile, 'utf8');

if (!appCode.includes('isConfigSidebarOpen')) {
  appCode = appCode.replace('const [searchMatchingIds, setSearchMatchingIds] = useState(new Set());', 'const [searchMatchingIds, setSearchMatchingIds] = useState(new Set());\n  const [isConfigSidebarOpen, setIsConfigSidebarOpen] = useState(true);');
  
  appCode = appCode.replace('<ControlPanel', '<ControlPanel \n            isOpen={isConfigSidebarOpen}\n            onToggle={() => setIsConfigSidebarOpen(!isConfigSidebarOpen)}');
  
  appCode = appCode.replace('<KnowledgeTree3D', '<KnowledgeTree3D \n              isConfigSidebarOpen={isConfigSidebarOpen}\n              onToggleConfigSidebar={() => setIsConfigSidebarOpen(!isConfigSidebarOpen)}');
  
  fs.writeFileSync(appFile, appCode);
}
console.log('App.jsx updated');
