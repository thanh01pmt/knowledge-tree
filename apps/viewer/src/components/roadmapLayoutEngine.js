/**
 * Roadmap.sh Layout Engine - Algorithmic replication of roadmap.sh's exact positioning
 * 
 * Based on analysis of live API data from roadmap.sh/frontend
 * 
 * Key observations:
 * - 7 topic columns at fixed X positions
 * - Subtopics positioned relative to parent (direction depends on column)
 * - Vertical spines at specific X positions connecting topic groups
 * - Horizontal rules as section separators
 * - Section boxes encompassing topic groups
 * - Balsamiq style: yellow topics (#FDFF00), light yellow subtopics (#FFE599)
 * - Blue edges (#2B78E4), solid for required, dashed for alternatives
 */

// ============================================================================
// EXACT COLUMN POSITIONS (from live API analysis)
// ============================================================================

export const ROADMAP_TOPIC_COLUMNS = [
  { id: 'col-advanced', x: -652.1, label: 'Advanced Topics', subtopicDir: 'right', subtopicDx: 418 },
  { id: 'col-meta', x: -305.3, label: 'Meta Frameworks', subtopicDir: 'left', subtopicDx: -416 },
  { id: 'col-core', x: -237.0, label: 'Core Web', subtopicDir: 'right', subtopicDx: 323 },
  { id: 'col-graphql', x: -234.7, label: 'GraphQL', subtopicDir: 'down', subtopicDx: 0 },
  { id: 'col-bundlers', x: -233.7, label: 'Bundlers/Types', subtopicDir: 'left', subtopicDx: -416 },
  { id: 'col-react', x: -115.7, label: 'React', subtopicDir: 'down', subtopicDx: 0 },
  { id: 'col-tools', x: 159.5, label: 'Tools & Security', subtopicDir: 'down', subtopicDx: 0 },
  { id: 'col-pkg', x: 162.2, label: 'Package/CSS', subtopicDir: 'down', subtopicDx: 0 },
];

// Topic spacing within a column
export const TOPIC_SPACING = 110;
export const SUBTOPIC_SPACING = 53;

// ============================================================================
// SECTION DEFINITIONS (groupings of topics)
// ============================================================================

export const ROADMAP_SECTIONS = [
  {
    id: 'sec-basics',
    label: 'Learn the Basics',
    column: 'col-core',
    topics: ['Internet', 'HTML', 'CSS', 'JavaScript'],
    yStart: 50,
  },
  {
    id: 'sec-tools',
    label: 'Developer Tools',
    column: 'col-core',
    topics: ['Version Control', 'VCS Hosting', 'Package Managers', 'CSS Frameworks'],
    yStart: 380,
  },
  {
    id: 'sec-frameworks',
    label: 'Frameworks',
    column: 'col-core',
    topics: ['Learn a Framework', 'React', 'Vue.js', 'Svelte', 'Angular'],
    yStart: 730,
  },
  {
    id: 'sec-ai',
    label: 'AI in Development',
    column: 'col-core',
    topics: ['AI Assisted Coding', 'Prompting Techniques', 'Implementing AI', 'Agents', 'MCP', 'Skills'],
    yStart: 900,
  },
  {
    id: 'sec-advanced',
    label: 'Advanced Frontend',
    column: 'col-advanced',
    topics: [
      'Module Bundlers', 'Type Checkers', 'Linters & Formatters', 
      'Web Security', 'Web Components', 'GraphQL', 
      'SSR', 'SSG', 'PWAs', 'Mobile Apps', 'Desktop Apps', 
      'Accessibility', 'Testing', 'Performance', 'Deployment', 'Design Systems'
    ],
    yStart: 1480,
  },
];

// ============================================================================
// SUBTOPIC DEFINITIONS (which subtopics belong to which topic)
// ============================================================================

export const ROADMAP_SUBTOPICS = {
  'Internet': [
    'How does the internet work?',
    'What is HTTP?',
    'What is Domain Name?',
    'What is hosting?',
    'DNS and how it works?',
    'Browsers and how they work?',
  ],
  'Version Control': ['Git'],
  'VCS Hosting': ['GitHub'],
  'CSS Frameworks': ['Tailwind'],
  'AI Assisted Coding': ['Claude Code', 'Cursor', 'Copilot', 'Antigravity'],
  'Implementing AI': ['Gemini', 'OpenAI', 'Anthropic'],
  'Module Bundlers': ['Vite'],
  'Linters & Formatters': ['Biome'],
  'Learn the Basics': ['How LLMs work'],
  'Web Security': ['OWASP Risks'],
  'Mobile Apps': ['React Native'],
  'SSG': ['Astro'],
  'GraphQL': ['Apollo'],
  'Desktop Apps': ['Electron', 'Tauri', 'Flutter'],
  'Performance': ['Lighthouse', 'DevTools Usage', 'Service Workers', 'Cache-Control', 'Streamed Responses'],
  'Testing': ['Vitest'],
  'Web Components': ['HTML Templates'],
};

// ============================================================================
// COMPUTE LAYOUT - Generates exact positions matching roadmap.sh
// ============================================================================

export function computeRoadmapLayout() {
  const nodes = [];
  const edges = [];
  let nodeId = 0;
  
  // ID generator
  const genId = (prefix = 'node') => `${prefix}-${nodeId++}`;
  
  // Track topic nodes by label for edge creation
  const topicNodes = new Map();
  const subtopicNodes = new Map();
  
  // ---- TITLE NODE ----
  nodes.push({
    id: genId('title'),
    type: 'title',
    position: { x: -200, y: -100.6 },
    data: {
      label: 'Front-end',
      style: { fontSize: 28, fontWeight: 'bold', color: '#000000', textAlign: 'center' },
    },
  });
  
  // ---- LEGEND NODE ----
  nodes.push({
    id: genId('legend'),
    type: 'legend',
    position: { x: -654.9, y: -292.1 },
    data: {
      legends: [
        { id: 'leg-1', color: '#874efe', label: 'Personal Recommendation' },
        { id: 'leg-2', color: '#4f7a28', label: 'Alternative Option' },
        { id: 'leg-3', color: '#929292', label: 'Order not strict on roadmap' },
      ],
    },
  });
  
  // ---- BUTTON NODES ----
  const buttonData = [
    { label: 'Visit Beginner Friendly Version', x: -654.9, y: -153.7, href: '/frontend?r=frontend-beginner' },
    { label: 'Beginner Project Ideas', x: -631.9, y: 280.3, href: 'https://roadmap.sh/frontend/projects?difficulty=beginner' },
    { label: 'Intermediate Project Ideas', x: -277.5, y: 597.3, href: 'https://roadmap.sh/frontend/projects?difficulty=intermediate' },
    { label: 'Advanced Project Ideas', x: -314.5, y: 1942.7, href: 'https://roadmap.sh/frontend/projects?difficulty=advanced' },
    { label: 'roadmap.sh', x: 57.7, y: -204.2, href: 'https://roadmap.sh' },
    { label: 'Prompt Engineering', x: -652.1, y: 1061.7, href: 'https://roadmap.sh/prompt-engineering' },
    { label: 'AI Agents Roadmap', x: -652.1, y: 1154.7, href: 'https://roadmap.sh/ai-agents' },
    { label: 'Nodejs', x: -504.7, y: 3511.0, href: 'https://roadmap.sh/nodejs' },
    { label: 'Fullstack', x: -380.7, y: 3511.0, href: 'https://roadmap.sh/full-stack' },
    { label: 'Backend', x: -256.7, y: 3511.0, href: 'https://roadmap.sh/backend' },
    { label: 'Design System', x: -132.7, y: 3511.0, href: 'https://roadmap.sh/design-system' },
    { label: 'TypeScript', x: -233.7, y: 2589.8, href: 'https://roadmap.sh/typescript' },
  ];
  
  buttonData.forEach(btn => {
    nodes.push({
      id: genId('btn'),
      type: 'button',
      position: { x: btn.x, y: btn.y },
      data: {
        label: btn.label,
        href: btn.href,
        style: { backgroundColor: '#2B78E4', color: '#FFFFFF', fontSize: 17 },
      },
    });
  });
  
  // ---- PARAGRAPH NODES ----
  const paragraphData = [
    { label: 'HTML, CSS and JavaScript are the backbone of web development', x: -648.4, y: 170.3, style: { fontSize: 17, color: '#000000', textAlign: 'left', backgroundColor: '#ffffff' } },
    { label: 'At this point, you should be able to build modern vanilla JS', x: -295.5, y: 515.3, style: { fontSize: 17, color: '#000000', textAlign: 'left', backgroundColor: '#ffffff' } },
    { label: 'At this point you should have the expertise of an intermedia', x: -332.5, y: 1831.0, style: { fontSize: 17, color: '#000000', textAlign: 'left', backgroundColor: '#ffffff' } },
    { label: 'Continue Learning with following relevant tracks', x: -517.5, y: 3462.4, style: { fontSize: 17, color: '#000000', textAlign: 'center', backgroundColor: '#ffffff' } },
    { label: 'Find the detailed version of this roadmap along with other s', x: 44.5, y: -286.2, style: { fontSize: 17, color: '#000000', textAlign: 'left', backgroundColor: '#ffffff' } },
  ];
  
  paragraphData.forEach(p => {
    nodes.push({
      id: genId('para'),
      type: 'paragraph',
      position: { x: p.x, y: p.y },
      data: { label: p.label, style: p.style },
    });
  });
  
  // ---- SECTION BOXES ----
  const sectionData = [
    { label: '', x: -305.3, y: 2369.0, width: 182, height: 94, backgroundColor: '#ffffff', borderColor: '#000000' },
    { label: 'Frameworks', x: -305.3, y: 2240.4, width: 182, height: 114, backgroundColor: '#ffffff', borderColor: '#000000' },
    { label: 'React Ecosystem', x: -115.7, y: 2184.6, width: 197, height: 278, backgroundColor: '#ffffff', borderColor: '#000000' },
  ];
  
  sectionData.forEach(s => {
    nodes.push({
      id: genId('sec'),
      type: 'section',
      position: { x: s.x, y: s.y },
      data: { 
        label: s.label, 
        style: { 
          width: s.width, 
          height: s.height, 
          backgroundColor: s.backgroundColor, 
          borderColor: s.borderColor 
        } 
      },
    });
  });
  
  // ---- TOPIC NODES ----
  // Build topics for each column with proper Y positions
  const columnTopics = new Map();
  
  ROADMAP_TOPIC_COLUMNS.forEach(col => {
    const section = ROADMAP_SECTIONS.find(s => s.column === col.id);
    let y = section ? section.yStart : 50;
    
    // Get topics for this column
    let topics = [];
    if (section) {
      topics = section.topics;
    } else {
      // Fallback: topics that belong to this column
      switch(col.id) {
        case 'col-advanced':
          topics = ['Auth Strategies', 'Testing', 'Deployment', 'Design Systems', 'Performance', 'Web Components'];
          break;
        case 'col-meta':
          topics = ['Vue.js', 'SvelteKit'];
          break;
        case 'col-graphql':
          topics = ['GraphQL'];
          break;
        case 'col-bundlers':
          topics = ['Module Bundlers', 'Type Checkers', 'Desktop Apps'];
          break;
        case 'col-react':
          topics = ['React'];
          break;
        case 'col-tools':
          topics = ['Learn the Basics', 'Linters & Formatters', 'Web Security', 'SSR', 'SSG', 'Accessibility', 'PWAs', 'Mobile Apps'];
          break;
        case 'col-pkg':
          topics = ['Package Managers', 'CSS Frameworks'];
          break;
      }
    }
    
    const columnNodes = [];
    topics.forEach((topicLabel, idx) => {
      const isRecommendation = ['React', 'Vue.js', 'SvelteKit', 'Tailwind', 'Vite', 'Biome'].includes(topicLabel);
      const isAlternative = ['Angular'].includes(topicLabel);
      
      const node = {
        id: genId('topic'),
        type: 'topic',
        position: { x: col.x, y: y },
        data: {
          label: topicLabel,
          style: {
            fontSize: isRecommendation || isAlternative ? 14 : 16,
            fontWeight: 'bold',
            color: '#000000',
            backgroundColor: '#FDFF00',
          },
          legend: isRecommendation ? { color: '#874efe', label: '★' } : 
                  isAlternative ? { color: '#4f7a28', label: 'alt' } : null,
        },
      };
      
      nodes.push(node);
      topicNodes.set(topicLabel, node);
      columnNodes.push({ label: topicLabel, node, y });
      y += TOPIC_SPACING;
    });
    
    columnTopics.set(col.id, columnNodes);
  });
  
  // ---- VERTICAL SPINES ----
  // These connect topics within a column visually
  const spineData = [
    { x: -124.7, y: -209.6, height: 109 },
    { x: -124.7, y: 3294.6, height: 169 },
    { x: -136.7, y: 3577.4, height: 85 },
    { x: -410.4, y: 531.3, height: 257 },
    { x: -478.4, y: 2431.4, height: 105 },
    { x: -603.1, y: 2409.5, height: 89 },
    { x: 210.9, y: 375.5, height: 88 },
    { x: 333.5, y: 377.5, height: 85 },
  ];
  
  spineData.forEach(s => {
    nodes.push({
      id: genId('spine'),
      type: 'vertical',
      position: { x: s.x, y: s.y },
      data: {
        style: {
          height: s.height,
          stroke: '#2B78E4',
          strokeWidth: 3.5,
          strokeDasharray: '0.8 8',
          strokeLinecap: 'round',
        },
      },
    });
  });
  
  // ---- HORIZONTAL RULES ----
  const horizontalData = [
    { x: -483.8, y: 1867.2, width: 408, stroke: '#2B78E4', strokeDasharray: '0' },
    { x: -398.0, y: 753.6, width: 161, stroke: '#2B78E4', strokeDasharray: '0.8 8' },
    { x: -41.7, y: 562.2, width: 214, stroke: '#2B78E4', strokeDasharray: '0' },
  ];
  
  horizontalData.forEach(h => {
    nodes.push({
      id: genId('horiz'),
      type: 'horizontal',
      position: { x: h.x, y: h.y },
      data: {
        style: {
          width: h.width,
          stroke: h.stroke,
          strokeWidth: 3.5,
          strokeDasharray: h.strokeDasharray,
        },
      },
    });
  });
  
  // ---- SUBTOPIC NODES ----
  Object.entries(ROADMAP_SUBTOPICS).forEach(([parentLabel, subtopics]) => {
    const parentNode = topicNodes.get(parentLabel);
    if (!parentNode) return;
    
    const parentX = parentNode.position.x;
    const parentY = parentNode.position.y;
    
    // Determine subtopic column based on parent column
    const parentCol = ROADMAP_TOPIC_COLUMNS.find(c => Math.abs(c.x - parentX) < 5);
    const subtopicDx = parentCol?.subtopicDx || 320;
    const subtopicDir = parentCol?.subtopicDir || 'right';
    
    let subY = parentY + SUBTOPIC_SPACING;
    
    subtopics.forEach((subLabel, idx) => {
      let subX = parentX;
      if (subtopicDir === 'right') {
        subX = parentX + subtopicDx;
      } else if (subtopicDir === 'left') {
        subX = parentX + subtopicDx; // subtopicDx is negative for left
      } else if (subtopicDir === 'down') {
        subX = parentX;
      }
      
      const node = {
        id: genId('sub'),
        type: 'topic', // Same component, different style
        position: { x: subX, y: subY },
        data: {
          label: subLabel,
          style: {
            fontSize: 14,
            fontWeight: 'normal',
            color: '#000000',
            backgroundColor: '#FFE599',
          },
        },
      };
      
      nodes.push(node);
      subtopicNodes.set(`${parentLabel}::${subLabel}`, node);
      
      // Edge from parent to subtopic
      const edgeStyle = ['Vitest', 'HTML Templates', 'Apollo', 'Electron', 'Tauri', 'Flutter'].includes(subLabel) 
        ? 'dashed' 
        : 'solid';
      
      edges.push({
        id: genId('edge'),
        source: parentNode.id,
        target: node.id,
        type: 'bezier',
        data: { edgeStyle },
        style: { stroke: '#2B78E4', strokeWidth: 3.5 },
      });
      
      subY += SUBTOPIC_SPACING;
    });
  });
  
  // ---- TOPIC-TO-TOPIC EDGES (vertical spines connections) ----
  // Connect topics within a column
  columnTopics.forEach((colNodes, colId) => {
    for (let i = 0; i < colNodes.length - 1; i++) {
      const source = colNodes[i].node;
      const target = colNodes[i + 1].node;
      
      edges.push({
        id: genId('edge'),
        source: source.id,
        target: target.id,
        type: 'bezier',
        data: { edgeStyle: 'solid' },
        style: { stroke: '#2B78E4', strokeWidth: 3.5 },
      });
    }
  });
  
  // Cross-column edges (like Version Control -> Git, VCS Hosting -> GitHub)
  // These are already handled in subtopics
  
  return { nodes, edges };
}

// ============================================================================
// EXPORT FOR DIRECT API DATA USAGE
// ============================================================================

export function parseFrontendData(frontendData) {
  if (!frontendData?.nodes || !frontendData?.edges) {
    return computeRoadmapLayout();
  }
  
  const nodes = frontendData.nodes.map((apiNode, idx) => {
    const pos = apiNode.position || { x: 0, y: 0 };
    const measured = apiNode.measured || { width: 200, height: 50 };
    const nodeData = apiNode.data || {};
    
    let type = apiNode.type;
    if (type === 'subtopic') type = 'topic'; // Same component
    
    return {
      id: apiNode.id,
      type: type === 'vertical' ? 'vertical' : 
            type === 'horizontal' ? 'horizontal' :
            type === 'section' ? 'section' :
            type === 'paragraph' ? 'paragraph' :
            type === 'title' ? 'title' :
            type === 'button' ? 'button' :
            type === 'legend' ? 'legend' : 'topic',
      position: { x: pos.x, y: pos.y },
      data: {
        label: nodeData.label || '',
        style: nodeData.style || {},
        legend: nodeData.legend,
        progress: nodeData.progress,
        resources: nodeData.resources,
        description: nodeData.description,
        href: nodeData.href,
        color: nodeData.color,
        backgroundColor: nodeData.backgroundColor,
        borderColor: nodeData.borderColor,
        legends: nodeData.legends,
      },
      style: {
        width: Math.max(measured.width || 180, 180),
        height: Math.max(measured.height || 50, 50),
      },
      draggable: apiNode.draggable !== false,
      selectable: apiNode.selectable !== false,
      deletable: apiNode.deletable !== false,
    };
  });
  
  const edges = frontendData.edges.map((apiEdge, idx) => {
    const edgeData = apiEdge.data || {};
    const edgeStyle = edgeData.edgeStyle || 'solid';
    
    return {
      id: apiEdge.id || `edge-${apiEdge.source}-${apiEdge.target}`,
      source: apiEdge.source,
      target: apiEdge.target,
      type: 'bezier',
      data: { edgeStyle },
      style: {
        stroke: '#2B78E4',
        strokeWidth: 3.5,
      },
    };
  });
  
  return { nodes, edges };
}

export default { computeRoadmapLayout, parseFrontendData, ROADMAP_TOPIC_COLUMNS, ROADMAP_SECTIONS, ROADMAP_SUBTOPICS };