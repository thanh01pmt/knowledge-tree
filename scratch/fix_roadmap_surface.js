const fs = require('fs');

// Update ActionRoadmapWeb.css
const cssFile = 'apps/viewer/src/components/ActionRoadmapWeb.css';
let css = fs.readFileSync(cssFile, 'utf8');

// Add --sidebar-bg to light mode
css = css.replace(/--surface: #ffffff;/, '--surface: #ffffff;\n  --sidebar-bg: #ffffff;');
// Change --surface back to #1e293b and add --sidebar-bg to dark mode
css = css.replace(/--surface: #1a1d21;/, '--surface: #1e293b;\n  --sidebar-bg: #1a1d21;');
// Update .sidebar to use --sidebar-bg
css = css.replace(/\.action-roadmap-scope \.sidebar \{\n(.*?)\n  background: var\(--surface\);/s, '.action-roadmap-scope .sidebar {\n$1\n  background: var(--sidebar-bg);');
// Update .mobile-nav to use --sidebar-bg
css = css.replace(/\.action-roadmap-scope \.mobile-nav \{\n(.*?)\n    background: var\(--surface\);/s, '.action-roadmap-scope .mobile-nav {\n$1\n    background: var(--sidebar-bg);');

fs.writeFileSync(cssFile, css);

// Update ActionRoadmapWeb.jsx
const jsxFile = 'apps/viewer/src/components/ActionRoadmapWeb.jsx';
let jsx = fs.readFileSync(jsxFile, 'utf8');

// Replace var(--surface) with var(--sidebar-bg) ONLY for the sidebar
// Look for className: 'sidebar' and replace the background style
jsx = jsx.replace(/className: 'sidebar',(.*?)background: 'var\(--surface\)'/s, "className: 'sidebar',$1background: 'var(--sidebar-bg)'");

fs.writeFileSync(jsxFile, jsx);
console.log('Fixed surface and sidebar backgrounds!');
