/**
 * Parses the raw master_tree.json into { nodes, links } for 3d-force-graph.
 * Calculates linkCount (degree) for node sizing.
 * Optimized with Map lookups (O(N) total complexity).
 */
export function parseKnowledgeTree(rawData) {
  const nodes = [];
  const links = [];
  const linksBySource = {};
  const linksByTarget = {};
  const nodeMap = new Map();
  
  const fieldHues = [200, 140, 30, 280, 0, 320, 60, 100, 250]; // Distinct hues for fields
  let fieldIndex = 0;
  
  const prereqLinksBySource = {};
  const prereqLinksByTarget = {};

  const processItems = (items, level, parentKeys) => {
    if (!items) return;
    
    items.forEach(item => {
      // Create node
      const node = {
        id: item.code,
        name: item.name,
        description: item.description,
        level: level,
        metadata: item.metadata ? (typeof item.metadata === 'string' ? JSON.parse(item.metadata) : item.metadata) : {},
        cs2023_ka: item.cs2023_ka_mapping || null,
        linkCount: 0
      };
      nodes.push(node);
      nodeMap.set(item.code, node);
      
      if (level === 'field') {
        node.hue = fieldHues[fieldIndex++ % fieldHues.length];
      }
      
      // Process Prerequisites (if available)
      if (item.prerequisite_concept_codes) {
        let prereqCodes = [];
        if (Array.isArray(item.prerequisite_concept_codes)) {
          prereqCodes = item.prerequisite_concept_codes;
        } else if (typeof item.prerequisite_concept_codes === 'string') {
          prereqCodes = item.prerequisite_concept_codes.split(',').map(code => code.trim());
        }
        prereqCodes = prereqCodes.filter(Boolean);
        prereqCodes.forEach(prereqCode => {
          if (!prereqLinksBySource[prereqCode]) prereqLinksBySource[prereqCode] = [];
          prereqLinksBySource[prereqCode].push(item.code);
          
          if (!prereqLinksByTarget[item.code]) prereqLinksByTarget[item.code] = [];
          prereqLinksByTarget[item.code].push(prereqCode);
        });
      }
      
      // Create links from parents
      if (parentKeys) {
        parentKeys.forEach(parentKey => {
          if (item[parentKey]) {
            let parentCodes = [];
            if (Array.isArray(item[parentKey])) {
               parentCodes = item[parentKey];
            } else if (typeof item[parentKey] === 'string') {
               parentCodes = item[parentKey].split(',').map(code => code.trim());
            }
            parentCodes.forEach(parentCode => {
              if (parentCode) {
                // Kế thừa màu từ cha - dùng Map O(1)
                const parentNode = nodeMap.get(parentCode);
                if (parentNode && node.hue === undefined) {
                  node.hue = parentNode.hue;
                }

                links.push({
                  source: parentCode,
                  target: item.code
                });
                
                // Build adjacency list for traversal later
                if (!linksBySource[parentCode]) {
                  linksBySource[parentCode] = [];
                }
                linksBySource[parentCode].push(item.code);
                
                // Build reverse adjacency list (children to parent)
                if (!linksByTarget[item.code]) {
                  linksByTarget[item.code] = [];
                }
                linksByTarget[item.code].push(parentCode);
              }
            });
          }
        });
      }
    });
  };

  // 1. Process all levels
  processItems(rawData.fields, 'field', null);
  processItems(rawData.subjects, 'subject', ['field_codes']);
  processItems(rawData.categories, 'category', ['subject_codes']);
  processItems(rawData.topics, 'topic', ['category_codes']);
  processItems(rawData.concepts, 'concept', ['topic_codes']);
  processItems(rawData.learning_objectives, 'learning_objective', ['concept_codes']);
  processItems(rawData.keywords, 'keyword', ['concept_codes']);
  
  // 2. Calculate linkCount for node sizing using Map O(1)
  links.forEach(link => {
    const sourceNode = nodeMap.get(link.source);
    const targetNode = nodeMap.get(link.target);
    
    if (sourceNode) sourceNode.linkCount = (sourceNode.linkCount || 0) + 1;
    if (targetNode) targetNode.linkCount = (targetNode.linkCount || 0) + 1;
  });

  return { 
    graphData: { nodes, links },
    linksBySource,
    linksByTarget,
    prereqLinksBySource,
    prereqLinksByTarget,
    nodeMap
  };
}
