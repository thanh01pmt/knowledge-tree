const fs = require('fs');

// 1. Update ChatSidebar.jsx to use /api/chat
const sidebarPath = 'apps/viewer/src/components/layout/ChatSidebar.jsx';
let sidebarCode = fs.readFileSync(sidebarPath, 'utf8');
sidebarCode = sidebarCode.replace("fetch('/.netlify/functions/chat'", "fetch('/api/chat'");
fs.writeFileSync(sidebarPath, sidebarCode);

// 2. Update vite.config.js to proxy /api/chat
const vitePath = 'apps/viewer/vite.config.js';
let viteCode = fs.readFileSync(vitePath, 'utf8');
viteCode = viteCode.replace("'/.netlify/functions': {", "'/api/chat': {");
fs.writeFileSync(vitePath, viteCode);

// 3. Update the edge function to ensure no process.env crash in Deno
const funcPath = 'apps/viewer/netlify/edge-functions/chat.js';
let funcCode = fs.readFileSync(funcPath, 'utf8');
funcCode = funcCode.replace("const apiKey = process.env.DEEPSEEK_API_KEY || Netlify?.env?.get('DEEPSEEK_API_KEY');", "const apiKey = Netlify.env.get('DEEPSEEK_API_KEY');");
fs.writeFileSync(funcPath, funcCode);
