const fs = require('fs');

const file = 'apps/viewer/src/components/ControlPanel.jsx';
let code = fs.readFileSync(file, 'utf8');

// Update props
code = code.replace('onOpenDashboard', 'onOpenDashboard,\n  isOpen = true,\n  onToggle');

// Remove isCollapsed state
code = code.replace(/const \[isCollapsed, setIsCollapsed\] = useState\(false\);\n/, '');

// Replace isCollapsed logic with returning null when !isOpen
code = code.replace(/if \(isCollapsed\) \{.*?\n    \);\n  \}/s, 'if (!isOpen) return null;');

// Update close button onClick
code = code.replace(/onClick=\{.*?setIsCollapsed\(true\).*?\}/s, 'onClick={onToggle}');

fs.writeFileSync(file, code);
console.log('ControlPanel.jsx updated');
