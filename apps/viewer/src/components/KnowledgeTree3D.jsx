import { useRef, useEffect, useState, useCallback, useMemo } from 'react';
import ForceGraph3D from 'react-force-graph-3d';
import SpriteText from 'three-spritetext';
import * as THREE from 'three';
import { Maximize, Plus, Minus, Play, Pause, Network, Search, Camera, Hand, Rotate3d } from 'lucide-react';

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
  const [isPlaying, setIsPlaying] = useState(true);
  const [isPanMode, setIsPanMode] = useState(false);
  const [dimensions, setDimensions] = useState({ width: window.innerWidth, height: window.innerHeight });
  const containerRef = useRef();
  const lastClickTime = useRef({});
  
  // Update dimensions when container resizes (e.g. sidebar toggles)
  useEffect(() => {
    if (!containerRef.current) return;
    const observer = new ResizeObserver(entries => {
      if (entries && entries.length > 0) {
        const { width, height } = entries[0].contentRect;
        // Avoid setting 0 which causes errors in Three.js
        if (width > 0 && height > 0) {
          setDimensions({ width, height });
        }
      }
    });
    observer.observe(containerRef.current);
    return () => observer.disconnect();
  }, []);
  
  // Trackpad Pan Handling (Intercept wheel event)
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const handleWheel = (e) => {
      // Nếu là pinch-to-zoom (ctrlKey = true) trên trackpad, bỏ qua để OrbitControls tự lo zoom
      if (e.ctrlKey) return;

      // Nếu là thao tác trượt 2 ngón tay (scroll), chặn lại để thực hiện lệnh Pan
      e.preventDefault();
      e.stopPropagation();

      if (!fgRef.current || !fgRef.current.camera() || !fgRef.current.controls()) return;

      const camera = fgRef.current.camera();
      const controls = fgRef.current.controls();
      
      const distance = camera.position.distanceTo(controls.target);
      // Điều chỉnh tốc độ pan tỉ lệ với khoảng cách camera
      let multiplier = 0.0015;
      if (e.deltaMode === 1) multiplier = 0.05; // Scroll by lines
      
      const panSpeed = distance * multiplier;

      const panX = e.deltaX * panSpeed;
      // Scroll down (positive deltaY) moves camera down -> scene moves UP -> pan down.
      // Vì vậy ta giữ nguyên dấu hoặc đảo dấu tùy cảm giác. Thông thường vuốt lên = cuộn xuống = deltaY > 0 -> scene di chuyển lên -> camera di chuyển xuống -> panY = -deltaY
      const panY = -e.deltaY * panSpeed;

      const right = new THREE.Vector3().setFromMatrixColumn(camera.matrix, 0);
      const up = new THREE.Vector3().setFromMatrixColumn(camera.matrix, 1);

      right.multiplyScalar(panX);
      up.multiplyScalar(panY);

      const panVector = new THREE.Vector3().addVectors(right, up);

      camera.position.add(panVector);
      controls.target.add(panVector);
      
      controls.update();
    };

    container.addEventListener('wheel', handleWheel, { passive: false, capture: true });
    return () => container.removeEventListener('wheel', handleWheel, { capture: true });
  }, []);
  
  // Áp dụng mouse controls khi chuyển chế độ
  useEffect(() => {
    // Cần một độ trễ nhỏ để đảm bảo ForceGraph đã khởi tạo controls
    const timeoutId = setTimeout(() => {
      if (fgRef.current && fgRef.current.controls()) {
        const controls = fgRef.current.controls();
        if (isPanMode) {
          controls.mouseButtons.LEFT = THREE.MOUSE.PAN;
          controls.mouseButtons.RIGHT = THREE.MOUSE.ROTATE;
        } else {
          controls.mouseButtons.LEFT = THREE.MOUSE.ROTATE;
          controls.mouseButtons.RIGHT = THREE.MOUSE.PAN;
        }
      }
    }, 100);
    return () => clearTimeout(timeoutId);
  }, [isPanMode]);

  // Canvas Actions
  const handleZoomIn = useCallback(() => {
    if (!fgRef.current) return;
    const pos = fgRef.current.cameraPosition();
    fgRef.current.cameraPosition({ x: pos.x * 0.8, y: pos.y * 0.8, z: pos.z * 0.8 }, null, 300);
  }, []);

  const handleZoomOut = useCallback(() => {
    if (!fgRef.current) return;
    const pos = fgRef.current.cameraPosition();
    fgRef.current.cameraPosition({ x: pos.x * 1.2, y: pos.y * 1.2, z: pos.z * 1.2 }, null, 300);
  }, []);

  const handleZoomFit = useCallback(() => {
    if (!fgRef.current) return;
    fgRef.current.zoomToFit(400);
  }, []);

  const handleTogglePlay = useCallback(() => {
    if (!fgRef.current) return;
    if (isPlaying) {
      fgRef.current.pauseAnimation();
    } else {
      fgRef.current.resumeAnimation();
    }
    setIsPlaying(!isPlaying);
  }, [isPlaying]);

  const handleReheat = useCallback(() => {
    if (!fgRef.current) return;
    fgRef.current.d3ReheatSimulation();
  }, []);

  const handleScreenshot = useCallback(() => {
    if (!fgRef.current) return;
    const canvas = fgRef.current.renderer().domElement;
    const dataUrl = canvas.toDataURL('image/png');
    const link = document.createElement('a');
    link.download = 'knowledge-tree-snapshot.png';
    link.href = dataUrl;
    link.click();
  }, []);

  const handleSearchClick = () => {
    document.dispatchEvent(new CustomEvent('focus-search'));
  };

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
    <div className="relative w-full h-full overflow-hidden" ref={containerRef}>
      <ForceGraph3D
        ref={fgRef}
        width={dimensions.width}
        height={dimensions.height}
        controlType="orbit"
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
      {/* Canvas Toolbars */}
      <div className="absolute top-4 left-4 flex flex-col gap-3 z-10 pointer-events-none">
        
        {/* Zoom Controls */}
        <div className="flex flex-col bg-[#2a2f36]/80 backdrop-blur-md border border-slate-700/50 rounded-lg overflow-hidden shadow-xl pointer-events-auto">
          <button onClick={handleZoomFit} className="p-2 text-slate-400 hover:text-white hover:bg-slate-700 transition-colors border-b border-slate-700/50 flex items-center justify-center" title="Fit to screen">
            <Maximize className="w-4 h-4" strokeWidth={2} />
          </button>
          <button onClick={handleZoomIn} className="p-2 text-slate-400 hover:text-white hover:bg-slate-700 transition-colors border-b border-slate-700/50 flex items-center justify-center" title="Zoom In">
            <Plus className="w-4 h-4" strokeWidth={2} />
          </button>
          <button onClick={handleZoomOut} className="p-2 text-slate-400 hover:text-white hover:bg-slate-700 transition-colors flex items-center justify-center" title="Zoom Out">
            <Minus className="w-4 h-4" strokeWidth={2} />
          </button>
        </div>

        {/* Action Controls */}
        <div className="flex flex-col bg-[#2a2f36]/80 backdrop-blur-md border border-slate-700/50 rounded-lg overflow-hidden shadow-xl pointer-events-auto">
          <button onClick={() => setIsPanMode(!isPanMode)} className={`p-2 transition-colors border-b border-slate-700/50 flex items-center justify-center ${isPanMode ? 'text-blue-400 bg-slate-700' : 'text-slate-400 hover:text-white hover:bg-slate-700'}`} title={isPanMode ? "Switch to Rotate (3D Orbit) Mode" : "Switch to Pan Mode"}>
            {isPanMode ? <Hand className="w-4 h-4" strokeWidth={2} /> : <Rotate3d className="w-4 h-4" strokeWidth={2} />}
          </button>
          <button onClick={handleTogglePlay} className="p-2 text-slate-400 hover:text-white hover:bg-slate-700 transition-colors border-b border-slate-700/50 flex items-center justify-center" title={isPlaying ? "Pause Simulation" : "Play Simulation"}>
            {isPlaying ? <Pause className="w-4 h-4" fill="currentColor" strokeWidth={0} /> : <Play className="w-4 h-4" fill="currentColor" strokeWidth={0} />}
          </button>
          <button onClick={handleReheat} className="p-2 text-slate-400 hover:text-white hover:bg-slate-700 transition-colors border-b border-slate-700/50 flex items-center justify-center" title="Reheat Simulation">
            <Network className="w-4 h-4" strokeWidth={2} />
          </button>
          <button onClick={handleSearchClick} className="p-2 text-slate-400 hover:text-white hover:bg-slate-700 transition-colors border-b border-slate-700/50 flex items-center justify-center" title="Search Node">
            <Search className="w-4 h-4" strokeWidth={2} />
          </button>
          <button onClick={handleScreenshot} className="p-2 text-slate-400 hover:text-white hover:bg-slate-700 transition-colors flex items-center justify-center" title="Take Screenshot">
            <Camera className="w-4 h-4" strokeWidth={2} />
          </button>
        </div>

      </div>
    </div>
  );
}
