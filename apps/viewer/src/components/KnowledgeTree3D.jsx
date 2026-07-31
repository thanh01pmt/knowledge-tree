import { useRef, useEffect, useState, useCallback, useMemo } from 'react';
import ForceGraph3D from 'react-force-graph-3d';
import SpriteText from 'three-spritetext';
import * as THREE from 'three';

// Static geometries for performance
const geometries = {
  field: new THREE.IcosahedronGeometry(8, 1),
  subject: new THREE.DodecahedronGeometry(5, 0),
  category: new THREE.OctahedronGeometry(3, 0),
  topic: new THREE.BoxGeometry(3, 3, 3),
  concept: new THREE.SphereGeometry(1, 8, 8)
};

// Compute bounding spheres once for label offset calculation
Object.values(geometries).forEach(g => g.computeBoundingSphere());

export default function KnowledgeTree3D({ graphData, linksBySource, onNodeSelect, searchedNodeId, filters = { showLabels: true, hideConcepts: true }, simulationConfig }) {
  const fgRef = useRef();
  
  const [highlightNodes, setHighlightNodes] = useState(new Set());
  const [highlightLinks, setHighlightLinks] = useState(new Set());
  const [expandedNodes, setExpandedNodes] = useState(new Set());
  const lastClickTime = useRef({});

  // Calculate visible nodes to avoid "hairball"
  const visibleGraphData = useMemo(() => {
    if (!graphData) return { nodes: [], links: [] };

    // If hideConcepts is false, just return everything!
    if (!filters.hideConcepts) return graphData;

    const visibleNodesSet = new Set();
    
    // Add default visible nodes
    graphData.nodes.forEach(node => {
      if (['field', 'subject', 'category', 'topic'].includes(node.level)) {
        visibleNodesSet.add(node.id);
      }
    });
    
    // Add children of expanded nodes
    expandedNodes.forEach(nodeId => {
      const children = linksBySource[nodeId] || [];
      children.forEach(childId => visibleNodesSet.add(childId));
      visibleNodesSet.add(nodeId); // ensure parent is visible
    });
    
    const filteredNodes = graphData.nodes.filter(n => visibleNodesSet.has(n.id));
    
    // Ensure links only reference nodes that ACTUALLY exist in the filtered list
    const actualNodesSet = new Set(filteredNodes.map(n => n.id));
    const filteredLinks = graphData.links.filter(l => {
      const sourceId = typeof l.source === 'object' ? l.source.id : l.source;
      const targetId = typeof l.target === 'object' ? l.target.id : l.target;
      return actualNodesSet.has(sourceId) && actualNodesSet.has(targetId);
    });
    
    return { nodes: filteredNodes, links: filteredLinks };
  }, [graphData, expandedNodes, linksBySource, filters.hideConcepts]);

  // Configure physics
  useEffect(() => {
    if (fgRef.current && simulationConfig) {
      try {
        const chargeForce = fgRef.current.d3Force('charge');
        if (chargeForce) chargeForce.strength(simulationConfig.charge || -200);
        
        const linkForce = fgRef.current.d3Force('link');
        if (linkForce) linkForce.distance(simulationConfig.linkDistance || 80);
        
        // Only reheat if simulation is already running
        // Using setTimeout defers it safely after initial mount
        setTimeout(() => {
          if (fgRef.current) {
            fgRef.current.d3ReheatSimulation();
          }
        }, 100);
      } catch (e) {
        console.warn("Physics config error:", e);
      }
    }
  }, [simulationConfig]);

  const handleNodeClick = useCallback(node => {
    const now = Date.now();
    const lastTime = lastClickTime.current[node.id] || 0;
    const isDoubleClick = (now - lastTime) < 350;
    lastClickTime.current[node.id] = now;

    if (isDoubleClick) {
      // Toggle expand/collapse
      setExpandedNodes(prev => {
        const next = new Set(prev);
        if (next.has(node.id)) next.delete(node.id);
        else next.add(node.id);
        return next;
      });
      // Do not clear highlight on double click to keep context
      return; 
    }

    // Single click logic
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

  // Effect to handle search
  useEffect(() => {
    if (searchedNodeId && graphData) {
      const node = graphData.nodes.find(n => n.id === searchedNodeId);
      if (node) {
        // Expand its parents to ensure it's visible
        // In a real DAG this requires a parent pointer, but for now we just trigger click
        handleNodeClick(node);
      }
    }
  }, [searchedNodeId, graphData, handleNodeClick]);

  const handleBackgroundClick = useCallback(() => {
    setHighlightNodes(new Set());
    setHighlightLinks(new Set());
    if (onNodeSelect) onNodeSelect(null);
  }, [onNodeSelect]);

  // Color logic
  const getNodeColor = useCallback(node => {
    const hue = node.hue !== undefined ? node.hue : 200;
    
    const levelStyles = {
      'field': `hsl(${hue}, 100%, 55%)`,
      'subject': `hsl(${hue}, 85%, 45%)`,
      'category': `hsl(${hue}, 70%, 35%)`,
      'topic': `hsl(${hue}, 55%, 30%)`,
      'concept': `hsl(${hue}, 40%, 25%)`
    };

    if (highlightNodes.size === 0) {
      if (node.metadata && node.metadata.color) return node.metadata.color;
      return levelStyles[node.level] || '#ffffff';
    }
    
    return highlightNodes.has(node.id) ? `hsl(${hue}, 100%, 75%)` : 'rgba(255,255,255,0.05)';
  }, [highlightNodes]);

  return (
    <ForceGraph3D
      ref={fgRef}
      graphData={visibleGraphData}
      
      // Override default node rendering completely
      nodeThreeObjectExtend={false}
      nodeThreeObject={node => {
        const group = new THREE.Group();
        
        // 1. Create Mesh (Geometry)
        const geometry = geometries[node.level] || geometries['concept'];
        const material = new THREE.MeshLambertMaterial({ 
          color: getNodeColor(node),
          transparent: true,
          opacity: highlightNodes.size > 0 && !highlightNodes.has(node.id) ? 0.1 : 0.95
        });
        const mesh = new THREE.Mesh(geometry, material);
        
        // Scale mesh slightly based on connections to show "weight"
        const scale = 1 + ((node.linkCount || 0) * 0.03);
        mesh.scale.set(scale, scale, scale);
        group.add(mesh);

        // 2. Check expansion state
        const hasChildren = linksBySource[node.id] && linksBySource[node.id].length > 0;
        const isExpanded = expandedNodes.has(node.id);
        const radius = geometry.boundingSphere.radius * scale;
        
        // 3. Create Sprite Text Label
        const showLevels = ['field', 'subject', 'category', 'topic'];
        let yOffset = radius + 2;
        
        if (filters.showLabels && (showLevels.includes(node.level) || (node.level === 'concept' && highlightNodes.has(node.id)))) {
          const sprite = new SpriteText(node.name);
          sprite.color = 'rgba(255,255,255,0.9)';
          
          const textHeights = {
            'field': 7,
            'subject': 5,
            'category': 4,
            'topic': 2.5,
            'concept': 1.5
          };
          sprite.textHeight = textHeights[node.level] || 2;
          
          yOffset = radius + sprite.textHeight / 2 + 1;
          sprite.position.y = yOffset;
          
          group.add(sprite);
        }
        
        // Add Expand Indicator (+) or (-)
        if (hasChildren && !isExpanded) {
           const indicator = new SpriteText('(+)');
           indicator.color = '#38bdf8'; // light blue
           indicator.textHeight = 2;
           indicator.position.y = yOffset + 2.5;
           group.add(indicator);
        } else if (hasChildren && isExpanded) {
           const indicator = new SpriteText('(-)');
           indicator.color = '#94a3b8'; // slate
           indicator.textHeight = 1.5;
           indicator.position.y = yOffset + 2.5;
           group.add(indicator);
        }

        return group;
      }}
      
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
