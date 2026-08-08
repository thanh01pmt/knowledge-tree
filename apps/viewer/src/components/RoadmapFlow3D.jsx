import { useRef, useEffect, useState, useCallback, useMemo } from 'react';
import ForceGraph3D from 'react-force-graph-3d';
import SpriteText from 'three-spritetext';
import * as THREE from 'three';
import { Maximize, Plus, Minus, Play, Pause, Network, Search, Camera, Hand, Rotate3d, HelpCircle, X } from 'lucide-react';

const shapeGeometries = {
  sphere: new THREE.SphereGeometry(1, 16, 16),
  box: new THREE.BoxGeometry(1.5, 1.5, 1.5),
  tetrahedron: new THREE.TetrahedronGeometry(1.2, 0),
  cylinder: new THREE.CylinderGeometry(0.8, 0.8, 2, 16),
  dodecahedron: new THREE.DodecahedronGeometry(1.2, 0)
};

Object.values(shapeGeometries).forEach(g => g.computeBoundingSphere());

let glowTextureCache = null;
function getGlowTexture() {
  if (glowTextureCache) return glowTextureCache;
  const canvas = document.createElement('canvas');
  canvas.width = 64;
  canvas.height = 64;
  const context = canvas.getContext('2d');
  const gradient = context.createRadialGradient(32, 32, 0, 32, 32, 32);
  gradient.addColorStop(0, 'rgba(255, 255, 255, 1)');
  gradient.addColorStop(0.3, 'rgba(255, 255, 255, 0.8)');
  gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');
  context.fillStyle = gradient;
  context.fillRect(0, 0, 64, 64);
  glowTextureCache = new THREE.CanvasTexture(canvas);
  return glowTextureCache;
}

const ROADMAP_LEVEL_CONFIG = {
  field: { textHeight: 15, textColor: '#f6fa00', textWeight: 'bold', shape: 'dodecahedron', opacity: 1.0, baseSize: 3.5 },
  subject: { textHeight: 12, textColor: '#8cba36', textWeight: 'normal', shape: 'box', opacity: 0.9, baseSize: 3.0 },
  category: { textHeight: 7, textColor: '#cccccc', textWeight: 'normal', shape: 'box', opacity: 0.8, baseSize: 2.5 },
  topic: { textHeight: 5, textColor: '#aaaaaa', textWeight: 'normal', shape: 'tetrahedron', opacity: 0.7, baseSize: 2.0 },
  concept: { textHeight: 3, textColor: '#44bbff', textWeight: 'normal', shape: 'sphere', opacity: 0.6, baseSize: 1.5 },
  learning_objective: { textHeight: 2, textColor: '#ff44aa', textWeight: 'normal', shape: 'sphere', opacity: 0.4, baseSize: 1.0 },
  // Roadmap-specific levels
  gate: { textHeight: 5, textColor: '#f6fa00', textWeight: 'bold', shape: 'cylinder', opacity: 1.0, baseSize: 2.5 },
  phase: { textHeight: 4, textColor: '#44bbff', textWeight: 'normal', shape: 'box', opacity: 0.8, baseSize: 2.2 },
  feature: { textHeight: 3, textColor: '#8cba36', textWeight: 'normal', shape: 'tetrahedron', opacity: 0.8, baseSize: 1.8 },
};

const LEVEL_ORDER = ['field', 'subject', 'category', 'topic', 'concept', 'learning_objective', 'gate', 'phase', 'feature'];

export default function RoadmapFlow3D({ 
  roadmap,
  onNodeSelect,
  selectedNodeId,
  visualConfig = {},
  levelConfig = {},
}) {
  const fgRef = useRef();
  const [highlightNodes, setHighlightNodes] = useState(new Set());
  const [highlightLinks, setHighlightLinks] = useState(new Set());
  const [expandedNodes, setExpandedNodes] = useState(new Set());
  const [isPlaying, setIsPlaying] = useState(true);
  const [isPanMode, setIsPanMode] = useState(false);
  const [hoveredNode, setHoveredNode] = useState(null);
  const [focusedNodeId, setFocusedNodeId] = useState(null);
  const [isTransforming, setIsTransforming] = useState(false);
  const [dimensions, setDimensions] = useState({ width: window.innerWidth, height: window.innerHeight });
  const containerRef = useRef();
  const lastClickTime = useRef({});
  const [searchTerm, setSearchTerm] = useState('');

  // Merge configs
  const mergedLevelConfig = useMemo(() => ({ ...ROADMAP_LEVEL_CONFIG, ...levelConfig }), [levelConfig]);
  const mergedVisualConfig = useMemo(() => ({
    charge: -120,
    linkDistance: 30,
    centerGravity: 0.3,
    ...visualConfig
  }), [visualConfig]);

  // Build unified graph data from roadmap
  const graphData = useMemo(() => {
    if (!roadmap) return { nodes: [], links: [] };
    
    const nodes = [];
    const links = [];
    const nodeMap = new Map();
    
    // 1. Add knowledge concepts from topo_order
    (roadmap.topo_order || []).forEach((conceptCode, idx) => {
      const concept = roadmap.roadmap_graph?.nodes?.find(n => n.id === `LO-${conceptCode}`);
      if (!concept) return;
      
      // Determine level based on position in topo order
      const level = idx < 3 ? 'concept' : idx < 6 ? 'topic' : 'learning_objective';
      
      const node = {
        id: `concept-${conceptCode}`,
        name: concept.label,
        level,
        type: 'concept',
        originalCode: conceptCode,
        description: `Knowledge: ${concept.label}`,
        // Position hint for initial layout
        fx: (idx % 5) * 50,
        fy: Math.floor(idx / 5) * 50,
        fz: 0,
      };
      nodes.push(node);
      nodeMap.set(`concept-${conceptCode}`, node);
    });
    
    // 2. Add prerequisite edges between concepts
    (roadmap.roadmap_graph?.edges || []).forEach(edge => {
      const sourceId = `concept-${edge.from.replace('LO-', '')}`;
      const targetId = `concept-${edge.to.replace('LO-', '')}`;
      if (nodeMap.has(sourceId) && nodeMap.has(targetId)) {
        links.push({
          source: sourceId,
          target: targetId,
          type: 'prerequisite',
          label: edge.kind,
        });
      }
    });
    
    // 3. Add phases and gates as connected nodes
    let prevPhaseNodeId = null;
    
    (roadmap.waterfall_phases || []).forEach((phase, phaseIdx) => {
      const phaseNodeId = `phase-${phase.phase_num}`;
      const gateNodeId = `gate-${phase.phase_num}`;
      
      // Phase node
      const phaseNode = {
        id: phaseNodeId,
        name: phase.title,
        level: 'phase',
        type: 'phase',
        phaseNum: phase.phase_num,
        description: `Phase ${phase.phase_num}: ${phase.engineering_action}`,
        timeframe: phase.timeframe,
        prereq: phase.required_prereq_knowledge,
        concepts: phase.matching_concept_codes,
      };
      nodes.push(phaseNode);
      nodeMap.set(phaseNodeId, phaseNode);
      
      // Gate node
      const gate = roadmap.waterfall_gates?.[phaseIdx];
      const gateNode = {
        id: gateNodeId,
        name: gate?.checkpoint || `Gate ${phase.phase_num}`,
        level: 'gate',
        type: 'gate',
        phaseNum: phase.phase_num,
        description: `Gate ${phase.phase_num}: ${gate?.checkpoint}`,
        status: gate?.status,
        remediation: gate?.remediation_sprint?.sprint_title,
      };
      nodes.push(gateNode);
      nodeMap.set(gateNodeId, gateNode);
      
      // Link: Previous gate → Current phase
      if (prevPhaseNodeId) {
        links.push({
          source: prevPhaseNodeId,
          target: phaseNodeId,
          type: 'sequence',
          label: '→',
        });
      }
      
      // Link: Phase → Gate (within same phase)
      links.push({
        source: phaseNodeId,
        target: gateNodeId,
        type: 'phase_to_gate',
        label: 'passes',
      });
      
      // Link: Gate → Next phase (will be created in next iteration)
      prevPhaseNodeId = gateNodeId;
      
      // 4. Connect phase to its required concepts
      (phase.matching_concept_codes || []).forEach(conceptCode => {
        const conceptId = `concept-${conceptCode}`;
        if (nodeMap.has(conceptId)) {
          links.push({
            source: conceptId,
            target: phaseNodeId,
            type: 'concept_to_phase',
            label: 'enables',
          });
        }
      });
      
      // 5. Add features as child nodes of phase
      (phase.concepts || []).forEach((concept, cIdx) => {
        const featureNodeId = `feature-${phase.phase_num}-${cIdx}`;
        const featureNode = {
          id: featureNodeId,
          name: concept.name,
          level: 'feature',
          type: 'feature',
          phaseNum: phase.phase_num,
          conceptCode: concept.concept_code,
          description: `Feature: ${concept.name} (${concept.estimated_hours}h)`,
          estimatedHours: concept.estimated_hours,
          learningObjectives: concept.learning_objectives,
        };
        nodes.push(featureNode);
        nodeMap.set(featureNodeId, featureNode);
        
        // Link: Phase → Feature
        links.push({
          source: phaseNodeId,
          target: featureNodeId,
          type: 'phase_to_feature',
          label: 'contains',
        });
        
        // Link: Feature → Related concept
        if (nodeMap.has(`concept-${concept.concept_code}`)) {
          links.push({
            source: featureNodeId,
            target: `concept-${concept.concept_code}`,
            type: 'feature_to_concept',
            label: 'implements',
          });
        }
      });
    });
    
    return { nodes, links };
  }, [roadmap]);

  // Filter nodes by search
  const filteredGraphData = useMemo(() => {
    if (!searchTerm) return graphData;
    
    const term = searchTerm.toLowerCase();
    const matchingNodes = new Set();
    
    graphData.nodes.forEach(node => {
      if (node.name.toLowerCase().includes(term) || 
          node.description?.toLowerCase().includes(term) ||
          node.type?.toLowerCase().includes(term)) {
        matchingNodes.add(node.id);
      }
    });
    
    // Include connected nodes for context
    const contextNodes = new Set(matchingNodes);
    graphData.links.forEach(link => {
      const sourceId = typeof link.source === 'object' ? link.source.id : link.source;
      const targetId = typeof link.target === 'object' ? link.target.id : link.target;
      if (matchingNodes.has(sourceId)) contextNodes.add(targetId);
      if (matchingNodes.has(targetId)) contextNodes.add(sourceId);
    });
    
    const filteredNodes = graphData.nodes.filter(n => contextNodes.has(n.id));
    const actualNodesSet = new Set(filteredNodes.map(n => n.id));
    const filteredLinks = graphData.links.filter(l => {
      const sourceId = typeof l.source === 'object' ? l.source.id : l.source;
      const targetId = typeof l.target === 'object' ? l.target.id : l.target;
      return actualNodesSet.has(sourceId) && actualNodesSet.has(targetId);
    });
    
    return { nodes: filteredNodes, links: filteredLinks };
  }, [graphData, searchTerm]);

  // Canvas actions
  const handleZoomIn = useCallback(() => {
    if (!fgRef.current) return;
    setIsTransforming(true);
    const pos = fgRef.current.cameraPosition();
    fgRef.current.cameraPosition({ x: pos.x * 0.8, y: pos.y * 0.8, z: pos.z * 0.8 }, null, 300);
    setTimeout(() => setIsTransforming(false), 350);
  }, []);

  const handleZoomOut = useCallback(() => {
    if (!fgRef.current) return;
    setIsTransforming(true);
    const pos = fgRef.current.cameraPosition();
    fgRef.current.cameraPosition({ x: pos.x * 1.2, y: pos.y * 1.2, z: pos.z * 1.2 }, null, 300);
    setTimeout(() => setIsTransforming(false), 350);
  }, []);

  const handleZoomFit = useCallback(() => {
    if (!fgRef.current) return;
    setIsTransforming(true);
    fgRef.current.zoomToFit(400);
    setTimeout(() => setIsTransforming(false), 450);
  }, []);

  const handleTogglePlay = useCallback(() => {
    if (!fgRef.current) return;
    if (isPlaying) fgRef.current.pauseAnimation();
    else fgRef.current.resumeAnimation();
    setIsPlaying(!isPlaying);
  }, [isPlaying]);

  const handleReheat = useCallback(() => {
    if (!fgRef.current) return;
    fgRef.current.d3ReheatSimulation();
  }, []);

  // Node rendering
  const nodeThreeObject = useCallback((node) => {
    const config = mergedLevelConfig[node.level] || mergedLevelConfig.concept;
    const geometry = shapeGeometries[config.shape];
    const material = new THREE.MeshStandardMaterial({
      color: config.textColor,
      transparent: true,
      opacity: config.opacity,
      metalness: 0.3,
      roughness: 0.7,
      emissive: config.textColor,
      emissiveIntensity: 0.1,
    });
    
    const mesh = new THREE.Mesh(geometry, material);
    const scale = config.baseSize * (mergedVisualConfig.nodeSizeMultiplier || 1);
    mesh.scale.set(scale, scale, scale);
    
    // Add label
    const label = new SpriteText(node.name);
    label.color = config.textColor;
    label.textHeight = config.textHeight;
    label.fontFace = 'Inter, sans-serif';
    label.fontWeight = config.textWeight;
    label.material.depthWrite = false;
    label.material.transparent = true;
    label.centered = true;
    label.position.y = scale + 1.5;
    mesh.add(label);
    
    // Type indicator
    const typeLabel = new SpriteText(node.type.toUpperCase());
    typeLabel.color = '#888';
    typeLabel.textHeight = 2;
    typeLabel.fontFace = 'Inter, sans-serif';
    typeLabel.fontWeight = 'normal';
    typeLabel.material.depthWrite = false;
    typeLabel.material.transparent = true;
    typeLabel.centered = true;
    typeLabel.position.y = scale + 3;
    mesh.add(typeLabel);
    
    // Hover glow
    mesh.onPointerOver = () => {
      material.emissiveIntensity = 0.5;
      setHoveredNode(node);
    };
    mesh.onPointerOut = () => {
      material.emissiveIntensity = 0.1;
      setHoveredNode(null);
    };
    
    // Click to select
    mesh.onClick = () => {
      const now = Date.now();
      const last = lastClickTime.current[node.id] || 0;
      if (now - last < 300) {
        // Double click - focus
        setFocusedNodeId(node.id);
      } else {
        // Single click - select
        onNodeSelect?.(node);
      }
      lastClickTime.current[node.id] = now;
    };
    
    return mesh;
  }, [mergedLevelConfig, mergedVisualConfig, onNodeSelect]);

  // Link rendering
  const linkThreeObject = useCallback((link) => {
    const sourceObj = typeof link.source === 'object' ? link.source : null;
    const targetObj = typeof link.target === 'object' ? link.target : null;
    if (!sourceObj || !targetObj) return null;
    
    const sourceNode = sourceObj.__threeObj;
    const targetNode = targetObj.__threeObj;
    if (!sourceNode || !targetNode) return null;
    
    const sourcePos = new THREE.Vector3();
    const targetPos = new THREE.Vector3();
    sourceNode.getWorldPosition(sourcePos);
    targetNode.getWorldPosition(targetPos);
    
    const midPos = new THREE.Vector3().addVectors(sourcePos, targetPos).multiplyScalar(0.5);
    const distance = sourcePos.distanceTo(targetPos);
    
    // Color by type
    const typeColors = {
      prerequisite: '#44bbff',
      phase_to_gate: '#f6fa00',
      sequence: '#8cba36',
      concept_to_phase: '#ff44aa',
      phase_to_feature: '#8cba36',
      feature_to_concept: '#cccccc',
    };
    const color = typeColors[link.type] || '#888';
    const width = link.type === 'prerequisite' ? 0.03 : link.type === 'sequence' ? 0.04 : 0.02;
    const dash = ['phase_to_gate', 'sequence'].includes(link.type) ? [0.5, 0.5] : [0, 0];
    
    const material = new THREE.LineDashedMaterial({
      color,
      linewidth: 2,
      dashSize: dash[0] || 0,
      gapSize: dash[1] || 0,
      transparent: true,
      opacity: 0.7,
      depthWrite: false,
    });
    
    const points = [
      sourcePos.clone(),
      midPos.clone().add(new THREE.Vector3(0, distance * 0.1, 0)),
      targetPos.clone(),
    ];
    
    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const line = new THREE.Line(geometry, material);
    line.computeLineDistances();
    
    return line;
  }, []);

  // Link direction particles
  const linkDirectionalParticles = useCallback((link) => {
    if (!mergedVisualConfig.showParticles) return 0;
    return link.type === 'prerequisite' ? 2 : 1;
  }, [mergedVisualConfig.showParticles]);

  // Handle container resize
  useEffect(() => {
    if (!containerRef.current) return;
    const observer = new ResizeObserver(entries => {
      if (entries?.[0]?.contentRect) {
        const { width, height } = entries[0].contentRect;
        if (width > 0 && height > 0) setDimensions({ width, height });
      }
    });
    observer.observe(containerRef.current);
    return () => observer.disconnect();
  }, []);

  // Trackpad pan handling
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;
    const handleWheel = (e) => {
      if (e.ctrlKey) return;
      e.preventDefault();
      e.stopPropagation();
      if (!fgRef.current?.camera() || !fgRef.current?.controls()) return;
      const camera = fgRef.current.camera();
      const controls = fgRef.current.controls();
      const distance = camera.position.distanceTo(controls.target);
      const multiplier = e.deltaMode === 1 ? 0.05 : 0.0015;
      const panSpeed = distance * multiplier;
      const right = new THREE.Vector3().setFromMatrixColumn(camera.matrix, 0);
      const up = new THREE.Vector3().setFromMatrixColumn(camera.matrix, 1);
      right.multiplyScalar(e.deltaX * panSpeed);
      up.multiplyScalar(-e.deltaY * panSpeed);
      const panVector = new THREE.Vector3().addVectors(right, up);
      camera.position.add(panVector);
      controls.target.add(panVector);
      controls.update();
    };
    container.addEventListener('wheel', handleWheel, { passive: false, capture: true });
    return () => container.removeEventListener('wheel', handleWheel, { capture: true });
  }, []);

  // Mouse mode
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (fgRef.current?.controls()) {
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

  // Highlight selected node
  useEffect(() => {
    if (fgRef.current && selectedNodeId) {
      fgRef.current.emit('nodeClick', graphData.nodes.find(n => n.id === selectedNodeId));
    }
  }, [selectedNodeId, graphData.nodes]);

  if (!roadmap) {
    return (
      <div className="roadmap-flow-3d loading" style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#0f172a', color: '#e2e8f0' }}>
        <div className="spinner" style={{ width: 48, height: 48, border: '4px solid #1e293b', borderTopColor: '#44bbff', borderRadius: '50%', animation: 'spin 1s linear infinite' }}></div>
      </div>
    );
  }

  return (
    <div className="roadmap-flow-3d" ref={containerRef} style={{ width: '100%', height: '100%', background: '#0f172a' }}>
      <ForceGraph3D
        ref={fgRef}
        graphData={filteredGraphData}
        nodeThreeObject={nodeThreeObject}
        linkThreeObject={linkThreeObject}
        linkDirectionalParticles={linkDirectionalParticles}
        nodeId="id"
        nodeVal="level"
        linkSource="source"
        linkTarget="target"
        linkColor="type"
        nodeLabel="name"
        onNodeClick={onNodeSelect}
        onNodeHover={setHoveredNode}
        onEngineStop={() => setIsPlaying(false)}
        d3AlphaDecay={0.02}
        d3VelocityDecay={0.4}
        cooldownTime={15000}
        warmupTicks={100}
        enableNodeDrag={true}
        enableNavigationControls={false}
        backgroundColor="#0f172a"
        showNavInfo={false}
      />
      
      {/* Controls Overlay */}
      <div className="controls-overlay">
        <div className="toolbar-left">
          <div className="search-box">
            <Search className="search-icon" size={16} />
            <input
              type="text"
              placeholder="Search concepts, phases, gates..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-input"
            />
          </div>
          <div className="node-type-filter">
            <span className="filter-label">Show:</span>
            <button className={`filter-btn ${!visualConfig.maxLevel ? 'active' : ''}`} onClick={() => setVisualConfig(v => ({...v, maxLevel: undefined}))}>All</button>
            <button className={`filter-btn ${visualConfig.maxLevel === 'concept' ? 'active' : ''}`} onClick={() => setVisualConfig(v => ({...v, maxLevel: 'concept'}))}>Concepts</button>
            <button className={`filter-btn ${visualConfig.maxLevel === 'phase' ? 'active' : ''}`} onClick={() => setVisualConfig(v => ({...v, maxLevel: 'phase'}))}>Phases</button>
            <button className={`filter-btn ${visualConfig.maxLevel === 'gate' ? 'active' : ''}`} onClick={() => setVisualConfig(v => ({...v, maxLevel: 'gate'}))}>Gates</button>
          </div>
        </div>
        
        <div className="toolbar-center">
          <div className="legend">
            <span className="legend-item"><span className="legend-dot concept"></span>Concepts</span>
            <span className="legend-item"><span className="legend-dot phase"></span>Phases</span>
            <span className="legend-item"><span className="legend-dot gate"></span>Gates</span>
            <span className="legend-item"><span className="legend-dot feature"></span>Features</span>
          </div>
        </div>
        
        <div className="toolbar-right">
          <button className="icon-btn" onClick={handleZoomIn} title="Zoom In"><Plus size={18} /></button>
          <button className="icon-btn" onClick={handleZoomOut} title="Zoom Out"><Minus size={18} /></button>
          <button className="icon-btn" onClick={handleZoomFit} title="Fit View"><Maximize size={18} /></button>
          <button className="icon-btn" onClick={handleTogglePlay} title={isPlaying ? 'Pause' : 'Play'}>{isPlaying ? <Pause size={18} /> : <Play size={18} />}</button>
          <button className="icon-btn" onClick={handleReheat} title="Reheat Simulation"><Rotate3d size={18} /></button>
          <button className={`icon-btn ${isPanMode ? 'active' : ''}`} onClick={() => setIsPanMode(!isPanMode)} title={isPanMode ? 'Rotate Mode' : 'Pan Mode'}>{isPanMode ? <Hand size={18} /> : <Rotate3d size={18} />}</button>
        </div>
      </div>
    </div>
  );
}