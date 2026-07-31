import { useRef, useEffect, useState, useCallback, useMemo } from 'react';
import ForceGraph3D from 'react-force-graph-3d';
import SpriteText from 'three-spritetext';
import * as THREE from 'three';

// Static geometries for performance (normalized to ~radius 1)
const shapeGeometries = {
  sphere: new THREE.SphereGeometry(1, 16, 16),
  box: new THREE.BoxGeometry(1.5, 1.5, 1.5),
  tetrahedron: new THREE.TetrahedronGeometry(1.2, 0),
  cylinder: new THREE.CylinderGeometry(0.8, 0.8, 2, 16),
  dodecahedron: new THREE.DodecahedronGeometry(1.2, 0)
};

// Compute bounding spheres once for label offset calculation
Object.values(shapeGeometries).forEach(g => g.computeBoundingSphere());

export default function KnowledgeTree3D({ graphData, linksBySource, onNodeSelect, searchedNodeId, filters = { showLabels: true, hideConcepts: true }, visualConfig, levelConfig }) {
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
    if (fgRef.current && visualConfig) {
      try {
        const chargeForce = fgRef.current.d3Force('charge');
        if (chargeForce) chargeForce.strength(visualConfig.charge || -200);
        
        const linkForce = fgRef.current.d3Force('link');
        if (linkForce) linkForce.distance(visualConfig.linkDistance || 80);
        
        const centerForce = fgRef.current.d3Force('center');
        if (centerForce && visualConfig.centerGravity !== undefined) {
           centerForce.strength(visualConfig.centerGravity);
        }
        
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
  }, [visualConfig]);

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
    let hue = node.hue !== undefined ? node.hue : 200;
    
    // Coloring strategy
    if (visualConfig && visualConfig.coloringStrategy === 'connections') {
       // node.linkCount is calculated in dataParser
       const maxLinks = 15;
       const ratio = Math.min((node.linkCount || 0) / maxLinks, 1);
       // Cold to hot (blue 240 -> red 0)
       hue = 240 - (ratio * 240);
    }
    
    const levelStyles = {
      'field': `hsl(${hue}, 100%, 55%)`,
      'subject': `hsl(${hue}, 85%, 45%)`,
      'category': `hsl(${hue}, 70%, 35%)`,
      'topic': `hsl(${hue}, 55%, 30%)`,
      'concept': `hsl(${hue}, 40%, 25%)`
    };

    if (highlightNodes.size === 0) {
      if (node.metadata && node.metadata.color && (!visualConfig || visualConfig.coloringStrategy === 'hierarchy')) return node.metadata.color;
      return levelStyles[node.level] || '#ffffff';
    }
    
    return highlightNodes.has(node.id) ? `hsl(${hue}, 100%, 75%)` : 'rgba(255,255,255,0.05)';
  }, [highlightNodes, visualConfig]);

  return (
    <ForceGraph3D
      ref={fgRef}
      graphData={visibleGraphData}
      
      // Override default node rendering completely
      nodeThreeObjectExtend={false}
      nodeThreeObject={node => {
        const group = new THREE.Group();
        const config = levelConfig ? levelConfig[node.level] || levelConfig['concept'] : null;
        
        // 1. Create Mesh (Geometry) if not text-only
        const isTextOnly = config && config.shape === 'none';
        
        const baseRadius = { field: 8, subject: 5, category: 3, topic: 3, concept: 1 }[node.level] || 1;
        const sizeMultiplier = visualConfig ? visualConfig.nodeSizeMultiplier : 1.0;
        const scale = baseRadius * (1 + ((node.linkCount || 0) * 0.03)) * sizeMultiplier;
        
        let radius = baseRadius * scale; // approximate radius for label offset
        
        if (!isTextOnly) {
          const shapeKey = config ? config.shape : 'sphere';
          const geometry = shapeGeometries[shapeKey] || shapeGeometries['sphere'];
          
          const nodeOpacity = config ? config.opacity : 1.0;
          const isFaded = highlightNodes.size > 0 && !highlightNodes.has(node.id);
          
          const material = new THREE.MeshLambertMaterial({ 
            color: getNodeColor(node),
            transparent: nodeOpacity < 1.0 || isFaded,
            opacity: isFaded ? (nodeOpacity * 0.1) : nodeOpacity
          });
          const mesh = new THREE.Mesh(geometry, material);
          
          mesh.scale.set(scale, scale, scale);
          group.add(mesh);
          
          if (geometry.boundingSphere) {
             radius = geometry.boundingSphere.radius * scale;
          }
        } else {
          radius = 1; // minimal offset if no shape
        }

        // 2. Check expansion state
        const hasChildren = linksBySource[node.id] && linksBySource[node.id].length > 0;
        const isExpanded = expandedNodes.has(node.id);
        
        // 3. Create Sprite Text Label
        const showLevels = ['field', 'subject', 'category', 'topic'];
        let yOffset = radius + 2;
        
        // Label logic
        const isSelected = highlightNodes.has(node.id);
        const hasHighlight = highlightNodes.size > 0;
        const showUnselected = visualConfig ? visualConfig.showUnselectedLabels : false;
        
        // If text-only, always show label because there's no node mesh!
        const shouldShowLabel = isTextOnly || (filters.showLabels && (
           (showLevels.includes(node.level) || node.level === 'concept') &&
           (!hasHighlight || isSelected || showUnselected)
        ));
        
        if (shouldShowLabel) {
          const sprite = new SpriteText(node.name);
          
          // Apply Text Config
          const defaultColor = config ? config.textColor : 'rgba(255,255,255,0.9)';
          sprite.color = hasHighlight && !isSelected ? 'rgba(255,255,255,0.3)' : defaultColor;
          sprite.fontWeight = config && config.textWeight === 'bold' ? 'bold' : 'normal';
          
          const textHeights = { 'field': 7, 'subject': 5, 'category': 4, 'topic': 2.5, 'concept': 1.5 };
          sprite.textHeight = config ? config.textHeight : (textHeights[node.level] || 2);
          
          // If text-only, center the text on the node coordinates instead of floating above
          if (isTextOnly) {
             yOffset = 0;
          } else {
             yOffset = radius + sprite.textHeight / 2 + 1;
          }
          
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
        
        const opacity = visualConfig ? visualConfig.linkOpacity : 0.3;
        
        if (highlightLinks.size === 0) return `rgba(255,255,255,${opacity})`;
        return highlightLinks.has(linkId) ? '#ffaa00' : 'rgba(255,255,255, 0.01)';
      }}
      linkWidth={link => {
        const sourceId = typeof link.source === 'object' ? link.source.id : link.source;
        const targetId = typeof link.target === 'object' ? link.target.id : link.target;
        const linkId = `${sourceId}-${targetId}`;
        
        const width = visualConfig ? visualConfig.linkWidth : 0.5;
        return highlightLinks.has(linkId) ? width * 3 : width;
      }}
      
      linkDirectionalParticles={link => {
        if (visualConfig && !visualConfig.showParticles) return 0;
        const sourceId = typeof link.source === 'object' ? link.source.id : link.source;
        const targetId = typeof link.target === 'object' ? link.target.id : link.target;
        const linkId = `${sourceId}-${targetId}`;
        return highlightLinks.has(linkId) ? 4 : 1;
      }}
      linkDirectionalParticleWidth={2}
      
      onNodeClick={handleNodeClick}
      onBackgroundClick={handleBackgroundClick}
      
      backgroundColor="#0f172a" // Slate 900
    />
  );
}
