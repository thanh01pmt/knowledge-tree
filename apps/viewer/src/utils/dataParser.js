/**
 * Parses the raw master_tree.json into { nodes, links } for 3d-force-graph.
 * Calculates linkCount (degree) for node sizing.
 */
export function parseKnowledgeTree(rawData) {
  const nodes = [];
  const links = [];
  const linksBySource = {};
  const linksByTarget = {};
  
  const fieldHues = [200, 140, 30, 280, 0, 320, 60, 100, 250]; // Distinct hues for fields
  let fieldIndex = 0;
  
  const processItems = (items, level, parentKeys) => {
    if (!items) return;
    
    items.forEach(item => {
      // Create node
      const node = {
        id: item.code,
        name: item.name,
        description: item.description,
        level: level,
        metadata: item.metadata ? JSON.parse(item.metadata) : {},
        linkCount: 0 // Will calculate later
      };
      nodes.push(node);
      
      if (level === 'field') {
        node.hue = fieldHues[fieldIndex++ % fieldHues.length];
      }
      
      // Create links from parents
      if (parentKeys) {
        parentKeys.forEach(parentKey => {
          if (item[parentKey]) {
            // parentKey might be a comma-separated string like "CSN, MET"
            const parentCodes = item[parentKey].split(',').map(code => code.trim());
            parentCodes.forEach(parentCode => {
              if (parentCode) {
                // Kế thừa màu từ cha
                const parentNode = nodes.find(n => n.id === parentCode);
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
  
  // 2. Calculate linkCount for node sizing
  links.forEach(link => {
    const sourceNode = nodes.find(n => n.id === link.source);
    const targetNode = nodes.find(n => n.id === link.target);
    
    if (sourceNode) sourceNode.linkCount = (sourceNode.linkCount || 0) + 1;
    if (targetNode) targetNode.linkCount = (targetNode.linkCount || 0) + 1;
  });

  return { 
    graphData: { nodes, links },
    linksBySource,
    linksByTarget
  };
}
