import { useRef, useEffect, useState, useCallback } from 'react';
import ForceGraph3D from 'react-force-graph-3d';

export default function KnowledgeTree3D({ graphData, linksBySource, onNodeSelect }) {
  const fgRef = useRef();
  
  const [highlightNodes, setHighlightNodes] = useState(new Set());
  const [highlightLinks, setHighlightLinks] = useState(new Set());

  // Configure physics
  useEffect(() => {
    if (fgRef.current) {
      fgRef.current.d3Force('charge').strength(-150);
      fgRef.current.d3Force('link').distance(60);
    }
  }, []);

  const handleNodeClick = useCallback(node => {
    const newHighlightNodes = new Set();
    const newHighlightLinks = new Set();
    
    newHighlightNodes.add(node.id);

    // BFS to find all descendants
    const traverseChildren = (currentNodeId) => {
      const childrenIds = linksBySource[currentNodeId] || [];
      
      childrenIds.forEach(childId => {
        newHighlightLinks.add(`${currentNodeId}-${childId}`);
        if (!newHighlightNodes.has(childId)) {
          newHighlightNodes.add(childId);
          traverseChildren(childId);
        }
      });
    };

    traverseChildren(node.id);

    setHighlightNodes(newHighlightNodes);
    setHighlightLinks(newHighlightLinks);
    
    // Focus camera
    const distance = 250;
    const distRatio = 1 + distance/Math.hypot(node.x, node.y, node.z);
    fgRef.current.cameraPosition(
      { x: node.x * distRatio, y: node.y * distRatio, z: node.z * distRatio },
      node, // lookAt
      2000  // ms transition
    );

    if (onNodeSelect) {
      onNodeSelect(node);
    }
  }, [linksBySource, onNodeSelect]);

  const handleBackgroundClick = useCallback(() => {
    setHighlightNodes(new Set());
    setHighlightLinks(new Set());
    if (onNodeSelect) onNodeSelect(null);
  }, [onNodeSelect]);

  // Color logic
  const getNodeColor = node => {
    if (highlightNodes.size === 0) {
      // default colors based on metadata if available, else fallback
      if (node.metadata && node.metadata.color) return node.metadata.color;
      
      const levelColors = {
        'field': '#2980b9',
        'subject': '#27ae60',
        'category': '#f39c12',
        'topic': '#8e44ad',
        'concept': '#c0392b'
      };
      return levelColors[node.level] || '#ffffff';
    }
    
    return highlightNodes.has(node.id) ? '#ff0000' : 'rgba(255,255,255,0.05)';
  };

  return (
    <ForceGraph3D
      ref={fgRef}
      graphData={graphData}
      nodeVal={node => (node.linkCount || 0) * 1.2 + 3} 
      nodeLabel={node => `${node.name} (${node.level})`}
      nodeColor={getNodeColor}
      nodeOpacity={1}
      
      linkColor={link => {
        const sourceId = typeof link.source === 'object' ? link.source.id : link.source;
        const targetId = typeof link.target === 'object' ? link.target.id : link.target;
        const linkId = `${sourceId}-${targetId}`;
        
        if (highlightLinks.size === 0) return 'rgba(255,255,255,0.3)';
        return highlightLinks.has(linkId) ? '#ffaa00' : 'rgba(255,255,255, 0.01)';
      }}
      linkWidth={link => {
        const sourceId = typeof link.source === 'object' ? link.source.id : link.source;
        const targetId = typeof link.target === 'object' ? link.target.id : link.target;
        const linkId = `${sourceId}-${targetId}`;
        return highlightLinks.has(linkId) ? 2 : 0.5;
      }}
      
      linkDirectionalParticles={link => {
        const sourceId = typeof link.source === 'object' ? link.source.id : link.source;
        const targetId = typeof link.target === 'object' ? link.target.id : link.target;
        const linkId = `${sourceId}-${targetId}`;
        return highlightLinks.has(linkId) ? 4 : 0;
      }}
      linkDirectionalParticleWidth={2}
      
      onNodeClick={handleNodeClick}
      onBackgroundClick={handleBackgroundClick}
      
      backgroundColor="#0f172a" // Slate 900
    />
  );
}
