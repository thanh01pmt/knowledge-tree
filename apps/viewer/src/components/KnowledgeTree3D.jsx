import { useRef, useEffect, useState, useCallback, useMemo } from 'react';
import ForceGraph3D from 'react-force-graph-3d';
import SpriteText from 'three-spritetext';
import * as THREE from 'three';
import { Maximize, Plus, Minus, Play, Pause, Network, Search, Camera, Hand, Rotate3d, HelpCircle, X } from 'lucide-react';

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

// Create soft glow texture once for reuse
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

export default function KnowledgeTree3D({ 
  graphData, 
  linksBySource, 
  linksByTarget, 
  prereqLinksBySource = {}, 
  prereqLinksByTarget = {}, 
  onNodeSelect, 
  searchedNodeId, 
  filters = { showLabels: true, maxLevel: 'topic', showPrerequisites: false }, 
  visualConfig, 
  levelConfig, 
  selectedNode,
  isolatedNodeId = null,
  searchMatchingIds = null,
  theme
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

  // Multi-node live search highlight effect (S3)
  useEffect(() => {
    if (searchMatchingIds && searchMatchingIds.size > 0 && !selectedNode) {
      setHighlightNodes(new Set(searchMatchingIds));
      setHighlightLinks(new Set());
    } else if (searchMatchingIds && searchMatchingIds.size === 0 && !selectedNode && highlightNodes.size > 0) {
      setHighlightNodes(new Set());
      setHighlightLinks(new Set());
    }
  }, [searchMatchingIds, selectedNode]);
  
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

  const handleSearchClick = useCallback(() => {
    document.dispatchEvent(new CustomEvent('focus-search'));
  }, []);

  // Calculate visible nodes to avoid "hairball" or apply isolation mode
  const visibleGraphData = useMemo(() => {
    if (!graphData) return { nodes: [], links: [] };

    // Subtree Isolation Mode (S1)
    if (isolatedNodeId) {
      const isoSet = new Set([isolatedNodeId]);
      let queue = [isolatedNodeId];

      // Collect all descendants
      while (queue.length > 0) {
        const nextQueue = [];
        queue.forEach(id => {
          const children = linksBySource[id] || [];
          children.forEach(childId => {
            if (!isoSet.has(childId)) {
              isoSet.add(childId);
              nextQueue.push(childId);
            }
          });
        });
        queue = nextQueue;
      }

      // Collect immediate parents for context
      const parents = linksByTarget[isolatedNodeId] || [];
      parents.forEach(pId => isoSet.add(pId));

      const isoNodes = graphData.nodes.filter(n => isoSet.has(n.id));
      const isoLinks = graphData.links.filter(l => {
        const sourceId = typeof l.source === 'object' ? l.source.id : l.source;
        const targetId = typeof l.target === 'object' ? l.target.id : l.target;
        return isoSet.has(sourceId) && isoSet.has(targetId);
      });

      return { nodes: isoNodes, links: isoLinks };
    }

    const maxLevel = filters.maxLevel || 'topic';
    const levelOrder = ['field', 'subject', 'category', 'topic', 'concept', 'learning_objective'];
    const maxIndex = levelOrder.indexOf(maxLevel) !== -1 ? levelOrder.indexOf(maxLevel) : 3;

    const visibleNodesSet = new Set();
    
    // Add default visible nodes up to maxLevel
    graphData.nodes.forEach(node => {
      const nodeIndex = levelOrder.indexOf(node.level);
      // Fallback: nếu node không có level chuẩn, vẫn cho hiển thị nếu maxLevel = concept, 
      // hoặc mặc định ẩn đi nếu không rõ level. Ở đây ta ưu tiên ẩn các node lỗi level.
      if (nodeIndex !== -1 && nodeIndex <= maxIndex) {
        visibleNodesSet.add(node.id);
      }
    });
    
    // Add children of expanded nodes (allow drill-down beyond maxLevel)
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
  }, [graphData, expandedNodes, linksBySource, linksByTarget, filters.maxLevel, isolatedNodeId]);

  // Handle Prerequisite DAG links to overlay on the graph
  const visiblePrereqLinks = useMemo(() => {
    if (!filters.showPrerequisites || !focusedNodeId) return [];
    
    // We only show prerequisite lines leading to or from the focused node
    const prereqLinks = [];
    const actualNodesSet = new Set(visibleGraphData.nodes.map(n => n.id));
    
    const tracePrereqs = (startId, linksDict, isForward) => {
      let currentIds = [startId];
      const visited = new Set([startId]);
      
      while (currentIds.length > 0) {
        const nextIds = [];
        currentIds.forEach(id => {
          const neighbors = linksDict[id] || [];
          neighbors.forEach(nId => {
            if (actualNodesSet.has(nId) && !visited.has(nId)) {
              visited.add(nId);
              nextIds.push(nId);
              if (isForward) {
                 prereqLinks.push({ source: id, target: nId, type: 'prereq_forward' });
              } else {
                 prereqLinks.push({ source: nId, target: id, type: 'prereq_backward' });
              }
            }
          });
        });
        currentIds = nextIds;
      }
    };

    tracePrereqs(focusedNodeId, prereqLinksBySource, true); // Things that depend ON focusedNode (forward)
    tracePrereqs(focusedNodeId, prereqLinksByTarget, false); // Things that focusedNode depends ON (backward)

    return prereqLinks;
  }, [filters.showPrerequisites, focusedNodeId, prereqLinksBySource, prereqLinksByTarget, visibleGraphData.nodes]);

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
        
        setTimeout(() => {
          if (fgRef.current) {
            fgRef.current.d3ReheatSimulation();
          }
        }, 100);
      } catch (e) {
        console.warn("Physics config error:", e);
      }
    }
  }, [visualConfig?.charge, visualConfig?.linkDistance, visualConfig?.centerGravity]);

  const focusOnNode = useCallback((node) => {
    setFocusedNodeId(node.id);
    
    const newHighlightNodes = new Set();
    const newHighlightLinks = new Set();
    
    newHighlightNodes.add(node.id);

    // 1. Ancestors
    let currentIds = [node.id];
    while (currentIds.length > 0) {
      const nextIds = [];
      currentIds.forEach(id => {
        const parents = linksByTarget[id] || [];
        parents.forEach(p => {
          if (!newHighlightNodes.has(p)) {
            newHighlightNodes.add(p);
            newHighlightLinks.add(`${p}-${id}`);
            nextIds.push(p);
          }
        });
      });
      currentIds = nextIds;
    }

    // 2. Children
    const children = linksBySource[node.id] || [];
    children.forEach(c => {
      newHighlightNodes.add(c);
      newHighlightLinks.add(`${node.id}-${c}`);
    });

    // 3. Siblings (Removed to reduce visual clutter when focusing on a specific path)

    setHighlightNodes(newHighlightNodes);
    setHighlightLinks(newHighlightLinks);
    
    // Camera Focus
    if (fgRef.current) {
        setIsTransforming(true);
        setHoveredNode(null);
        
        // 1. Tính trọng tâm (Centroid) của cụm node được highlight
        const neighborhoodNodes = Array.from(newHighlightNodes)
          .map(id => graphData.nodes.find(n => n.id === id))
          .filter(Boolean);
        
        let cx = 0, cy = 0, cz = 0;
        neighborhoodNodes.forEach(n => {
          cx += (n.x || 0); cy += (n.y || 0); cz += (n.z || 0);
        });
        const len = neighborhoodNodes.length;
        if (len > 0) { cx /= len; cy /= len; cz /= len; }

        // 2. Vector hướng mọc (từ Node chính đến Trọng tâm)
        let dx = cx - node.x;
        let dy = cy - node.y;
        let dz = cz - node.z;
        let dirLen = Math.hypot(dx, dy, dz);

        let camDirX, camDirY, camDirZ;
        const ox = node.x, oy = node.y, oz = node.z;
        const outLen = Math.hypot(ox, oy, oz) || 1;

        if (dirLen < 0.1 || len <= 1) {
           // Cụm quá nhỏ, dùng luôn hướng Outward từ gốc tọa độ
           camDirX = ox / outLen; camDirY = oy / outLen; camDirZ = oz / outLen;
        } else {
           dx /= dirLen; dy /= dirLen; dz /= dirLen; // Chuẩn hóa Dir

           // Trực giao hóa Gram-Schmidt: Cam = Outward - Dir * (Outward . Dir)
           const dot = ox * dx + oy * dy + oz * dz;
           camDirX = ox - dot * dx;
           camDirY = oy - dot * dy;
           camDirZ = oz - dot * dz;

           let camLen = Math.hypot(camDirX, camDirY, camDirZ);
           
           if (camLen < 0.1) {
              // Trường hợp hiếm: Cụm mọc thẳng hàng với tia Outward
              // Tạo một vector vuông góc bất kỳ để nhìn từ bên hông
              const nx = ox / outLen, ny = oy / outLen, nz = oz / outLen;
              if (Math.abs(nx) < 0.9) {
                  camDirX = 0; camDirY = nz; camDirZ = -ny;
              } else {
                  camDirX = -nz; camDirY = 0; camDirZ = nx;
              }
              camLen = Math.hypot(camDirX, camDirY, camDirZ);
           }
           
           camDirX /= camLen; camDirY /= camLen; camDirZ /= camLen;
           
           // Luôn giữ camera ở nửa bán cầu hướng ra ngoài
           if (camDirX * ox + camDirY * oy + camDirZ * oz < 0) {
               camDirX = -camDirX; camDirY = -camDirY; camDirZ = -camDirZ;
           }
        }
        
        let maxDist = 100;
        neighborhoodNodes.forEach(n => {
           const d = Math.hypot((n.x||0) - node.x, (n.y||0) - node.y, (n.z||0) - node.z);
           if (d > maxDist) maxDist = d;
        });
        const distance = Math.max(300, maxDist * 1.5); // Add margin

        fgRef.current.cameraPosition(
          { 
            x: node.x + camDirX * distance, 
            y: node.y + camDirY * distance, 
            z: node.z + camDirZ * distance 
          },
          node, // lookAt exactly at the selected node
          1500  // transition time
        );

        setTimeout(() => {
          setIsTransforming(false);
        }, 1550);
    }
  }, [linksBySource, linksByTarget, graphData.nodes]);

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
      return; 
    }

    if (onNodeSelect) {
      onNodeSelect(node);
    }
  }, [onNodeSelect]);

  // Sync external selectedNode with 3D Graph logic
  useEffect(() => {
    if (selectedNode && selectedNode.id !== focusedNodeId) {
      focusOnNode(selectedNode);
    } else if (!selectedNode && focusedNodeId) {
      setFocusedNodeId(null);
      setHighlightNodes(new Set());
      setHighlightLinks(new Set());
    }
  }, [selectedNode]); // Fix H3: avoid dependency loop

  const handleBackgroundClick = useCallback(() => {
    if (onNodeSelect) onNodeSelect(null);
  }, [onNodeSelect]);

  const handleNodeHover = useCallback((node) => {
    setHoveredNode(node || null);
  }, []);

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

    if (visualConfig && visualConfig.coloringStrategy === 'cs2023') {
       if (node.cs2023_ka) {
          const kaStr = String(node.cs2023_ka);
          let hash = 0;
          for (let i = 0; i < kaStr.length; i++) {
             hash = kaStr.charCodeAt(i) + ((hash << 5) - hash);
          }
          const kaHue = Math.abs(hash) % 360;
          
          if (highlightNodes.size === 0) return `hsl(${kaHue}, 80%, 55%)`;
          return highlightNodes.has(node.id) ? `hsl(${kaHue}, 100%, 75%)` : 'rgba(255,255,255,0.05)';
       } else {
          return highlightNodes.size > 0 && !highlightNodes.has(node.id) ? 'rgba(255,255,255,0.05)' : '#475569';
       }
    }

    if (highlightNodes.size === 0) {
      if (node.metadata && node.metadata.color && (!visualConfig || visualConfig.coloringStrategy === 'hierarchy')) return node.metadata.color;
      return levelStyles[node.level] || '#ffffff';
    }
    
    return highlightNodes.has(node.id) ? `hsl(${hue}, 100%, 75%)` : 'rgba(255,255,255,0.05)';
  }, [highlightNodes, visualConfig]);

  const nodeThreeObject = useCallback(node => {
    // Memory leak prevention: dispose previous object resources if re-creating
    if (node.__threeObj) {
      node.__threeObj.traverse(child => {
        if (child.material) {
          if (Array.isArray(child.material)) child.material.forEach(m => m.dispose());
          else child.material.dispose();
        }
      });
    }

    const group = new THREE.Group();
    const config = levelConfig ? levelConfig[node.level] || levelConfig['concept'] : null;
    
    // 1. Create Mesh (Geometry) if not text-only
    const isTextOnly = config && config.shape === 'none';
    
    const baseRadius = { field: 8, subject: 5, category: 3, topic: 3, concept: 1 }[node.level] || 1;
    const sizeMultiplier = visualConfig ? visualConfig.nodeSizeMultiplier : 1.0;
    const scale = baseRadius * (1 + ((node.linkCount || 0) * 0.03)) * sizeMultiplier;
    
    let radius = baseRadius * scale; // approximate radius for label offset
        
    const isFocused = focusedNodeId === node.id;
    const color = getNodeColor(node);

    if (!isTextOnly) {
      const shapeKey = config ? config.shape : 'sphere';
      const geometry = shapeGeometries[shapeKey] || shapeGeometries['sphere'];
      
      const nodeOpacity = config ? config.opacity : 1.0;
      const isFaded = highlightNodes.size > 0 && !highlightNodes.has(node.id);
      
      const material = new THREE.MeshLambertMaterial({ 
        color: color,
        transparent: nodeOpacity < 1.0 || isFaded,
        opacity: isFaded ? (nodeOpacity * 0.1) : nodeOpacity
      });
      const mesh = new THREE.Mesh(geometry, material);
      
      mesh.scale.set(scale, scale, scale);
      group.add(mesh);

      // Hiệu ứng Glow cho Node đang được chọn
      if (isFocused) {
        const glowMaterial = new THREE.SpriteMaterial({
          map: getGlowTexture(),
          color: color,
          transparent: true,
          opacity: 0.7,
          blending: THREE.AdditiveBlending,
          depthWrite: false
        });
        const glowSprite = new THREE.Sprite(glowMaterial);
        // Phóng to Sprite lên để tạo viền halo mềm
        glowSprite.scale.set(scale * 3.5, scale * 3.5, 1);
        group.add(glowSprite);
      }
      
      if (geometry.boundingSphere) {
         radius = geometry.boundingSphere.radius * scale;
      }
    } else {
      radius = 1; // minimal offset if no shape
    }

    // Add PointLight for environmental glow effect on nearby nodes
    if (isFocused) {
       const light = new THREE.PointLight(color, 200, 150); // color, intensity, distance
       group.add(light);
    }
        // 2. Check expansion state
        const hasChildren = linksBySource[node.id] && linksBySource[node.id].length > 0;
        const isExpanded = expandedNodes.has(node.id);
        
        // 3. Create Sprite Text Label
        const showLevels = ['field', 'subject', 'category', 'topic'];
        let yOffset = radius + 2;
        
        // Label logic
        const isSelected = focusedNodeId === node.id;
        const hasHighlight = highlightNodes.size > 0;
        const showUnselected = visualConfig ? visualConfig.showUnselectedLabels : false;
        
        // If text-only, always show label because there's no node mesh!
        const shouldShowLabel = isTextOnly || (filters.showLabels && (
           (showLevels.includes(node.level) || node.level === 'concept') &&
           (!hasHighlight || highlightNodes.has(node.id) || showUnselected)
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
        
        const isFaded = hasHighlight && !highlightNodes.has(node.id);

        if (hasChildren && !isExpanded && !isFaded) {
           const indicator = new SpriteText('(+)');
           indicator.color = '#38bdf8'; // light blue
           indicator.textHeight = 4.5;
           indicator.position.y = yOffset + 5;
           group.add(indicator);
        } else if (hasChildren && isExpanded && !isFaded) {
           const indicator = new SpriteText('(-)');
           indicator.color = '#ef4444'; // red
           indicator.textHeight = 4.5;
           indicator.position.y = yOffset + 5;
           group.add(indicator);
        }

    return group;
  }, [levelConfig, visualConfig, highlightNodes, focusedNodeId, expandedNodes, filters.showLabels, linksBySource, getNodeColor]);

  const getLinkColor = useCallback(link => {
    if (link.type === 'prereq_forward') return '#22c55e'; // Green (Unlocks)
    if (link.type === 'prereq_backward') return '#ef4444'; // Red (Requires)
    
    const sourceId = typeof link.source === 'object' ? link.source.id : link.source;
    const targetId = typeof link.target === 'object' ? link.target.id : link.target;
    const linkId = `${sourceId}-${targetId}`;
    
    const opacity = visualConfig ? visualConfig.linkOpacity : 0.3;
    
    if (highlightLinks.size === 0) return `rgba(255,255,255,${opacity})`;
    return highlightLinks.has(linkId) ? '#ffaa00' : 'rgba(255,255,255, 0.01)';
  }, [visualConfig?.linkOpacity, highlightLinks]);

  const getLinkWidth = useCallback(link => {
    if (link.type === 'prereq_forward' || link.type === 'prereq_backward') return 1.5;
    
    const sourceId = typeof link.source === 'object' ? link.source.id : link.source;
    const targetId = typeof link.target === 'object' ? link.target.id : link.target;
    const linkId = `${sourceId}-${targetId}`;
    
    const width = visualConfig ? visualConfig.linkWidth : 0.5;
    return highlightLinks.has(linkId) ? width * 3 : width;
  }, [visualConfig?.linkWidth, highlightLinks]);

  const getLinkDirectionalParticles = useCallback(link => {
    if (link.type === 'prereq_forward' || link.type === 'prereq_backward') return 4;
    if (visualConfig && !visualConfig.showParticles) return 0;
    const sourceId = typeof link.source === 'object' ? link.source.id : link.source;
    const targetId = typeof link.target === 'object' ? link.target.id : link.target;
    const linkId = `${sourceId}-${targetId}`;
    
    if (highlightLinks.size > 0 && !highlightLinks.has(linkId)) return 0;
    
    return highlightLinks.has(linkId) ? 4 : 1;
  }, [visualConfig?.showParticles, highlightLinks]);

  const getLinkDirectionalParticleColor = useCallback(link => {
    if (link.type === 'prereq_forward') return '#4ade80';
    if (link.type === 'prereq_backward') return '#f87171';
    return '#ffffff';
  }, []);

  const finalGraphData = useMemo(() => ({
    nodes: visibleGraphData.nodes,
    links: [...visibleGraphData.links, ...visiblePrereqLinks]
  }), [visibleGraphData, visiblePrereqLinks]);

  const [showHelpModal, setShowHelpModal] = useState(false);

  return (
    <div className="relative w-full h-full overflow-hidden" ref={containerRef}>
      <ForceGraph3D
        ref={fgRef}
        width={dimensions.width}
        height={dimensions.height}
        controlType="orbit"
        graphData={finalGraphData}
      
      nodeThreeObjectExtend={false}
      nodeThreeObject={nodeThreeObject}
      linkColor={getLinkColor}
      linkWidth={getLinkWidth}
      linkDirectionalParticles={getLinkDirectionalParticles}
      linkDirectionalParticleWidth={2}
      linkDirectionalParticleColor={getLinkDirectionalParticleColor}
      
      enablePointerInteraction={!isTransforming}
      onNodeClick={handleNodeClick}
      onNodeHover={handleNodeHover}
      onBackgroundClick={handleBackgroundClick}
      
      backgroundColor={theme === 'dark' ? "#0f172a" : "#f8fafc"}
    />

      {/* Hover Preview Tooltip */}
      {hoveredNode && (
        <div 
          className="absolute z-50 pointer-events-none bg-white/95 dark:bg-[#1e2227]/95 backdrop-blur shadow-2xl border border-slate-200 dark:border-slate-700 rounded-lg p-3 transition-opacity duration-200"
          style={{
            bottom: '24px',
            left: '24px',
            maxWidth: '300px'
          }}
        >
          <div className="flex items-center gap-2 mb-1">
            <span className="px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-600 dark:text-blue-400 text-[9px] font-bold uppercase tracking-wider">
              {hoveredNode.level}
            </span>
            {hoveredNode.cs2023_ka && (
              <span className="px-1.5 py-0.5 rounded bg-purple-500/20 text-purple-600 dark:text-purple-300 text-[9px] font-bold uppercase">
                {hoveredNode.cs2023_ka}
              </span>
            )}
          </div>
          <h4 className="text-slate-800 dark:text-slate-100 font-semibold text-sm line-clamp-2 leading-tight">
            {hoveredNode.name}
          </h4>
          {hoveredNode.description && (
            <p className="text-slate-500 dark:text-slate-400 text-xs mt-1 line-clamp-2">
              {hoveredNode.description}
            </p>
          )}
        </div>
      )}

      {/* Legend Badge (Bottom Right) */}
      <div className="absolute bottom-4 right-4 z-10 bg-white/80 dark:bg-[#1e2227]/80 backdrop-blur-md border border-slate-200/60 dark:border-slate-700/60 rounded-lg p-3 shadow-xl max-w-xs text-xs pointer-events-auto">
        <div className="text-[10px] font-bold uppercase text-slate-500 dark:text-slate-400 tracking-wider mb-1.5">
          Color Strategy: {visualConfig?.coloringStrategy || 'hierarchy'}
        </div>
        {visualConfig?.coloringStrategy === 'cs2023' ? (
          <div className="flex flex-col gap-1 text-[11px] text-slate-600 dark:text-slate-300">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-purple-400 inline-block" />
              <span>Color mapped to CS2023 Knowledge Area</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-slate-400 dark:bg-slate-600 inline-block" />
              <span>Unmapped concept</span>
            </div>
          </div>
        ) : visualConfig?.coloringStrategy === 'connections' ? (
          <div className="flex items-center gap-2 text-[11px] text-slate-600 dark:text-slate-300">
            <div className="h-2 flex-1 rounded bg-gradient-to-r from-blue-500 via-yellow-400 to-red-500" />
            <span>Low → High degree</span>
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-x-3 gap-y-1 text-[10px] text-slate-600 dark:text-slate-400">
            <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-cyan-400" /> Field</span>
            <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-green-500" /> Subject</span>
            <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-amber-600" /> Category</span>
            <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-slate-500" /> Topic</span>
          </div>
        )}
      </div>

      {/* Canvas Toolbars */}
      <div className="absolute top-4 left-4 flex flex-col gap-3 z-10 pointer-events-none">
        
        {/* Zoom Controls */}
        <div className="flex flex-col bg-white/80 dark:bg-slate-50 dark:bg-[#2a2f36]/80 backdrop-blur-md border border-slate-200/50 dark:border-slate-700/50 rounded-lg overflow-hidden shadow-xl pointer-events-auto">
          <button onClick={handleZoomFit} className="p-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors border-b border-slate-200/50 dark:border-slate-700/50 flex items-center justify-center" title="Fit to screen">
            <Maximize className="w-4 h-4" strokeWidth={2} />
          </button>
          <button onClick={handleZoomIn} className="p-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors border-b border-slate-200/50 dark:border-slate-700/50 flex items-center justify-center" title="Zoom In">
            <Plus className="w-4 h-4" strokeWidth={2} />
          </button>
          <button onClick={handleZoomOut} className="p-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors flex items-center justify-center" title="Zoom Out">
            <Minus className="w-4 h-4" strokeWidth={2} />
          </button>
        </div>

        {/* Action Controls */}
        <div className="flex flex-col bg-white/80 dark:bg-slate-50 dark:bg-[#2a2f36]/80 backdrop-blur-md border border-slate-200/50 dark:border-slate-700/50 rounded-lg overflow-hidden shadow-xl pointer-events-auto">
          <button onClick={() => setIsPanMode(!isPanMode)} className={`p-2 transition-colors border-b border-slate-200/50 dark:border-slate-700/50 flex items-center justify-center ${isPanMode ? 'text-blue-600 bg-slate-100 dark:text-blue-400 dark:bg-slate-700' : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-700'}`} title={isPanMode ? "Switch to Rotate (3D Orbit) Mode" : "Switch to Pan Mode"}>
            {isPanMode ? <Hand className="w-4 h-4" strokeWidth={2} /> : <Rotate3d className="w-4 h-4" strokeWidth={2} />}
          </button>
          <button onClick={handleTogglePlay} className="p-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors border-b border-slate-200/50 dark:border-slate-700/50 flex items-center justify-center" title={isPlaying ? "Pause Simulation" : "Play Simulation"}>
            {isPlaying ? <Pause className="w-4 h-4" fill="currentColor" strokeWidth={0} /> : <Play className="w-4 h-4" fill="currentColor" strokeWidth={0} />}
          </button>
          <button onClick={handleReheat} className="p-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors border-b border-slate-200/50 dark:border-slate-700/50 flex items-center justify-center" title="Reheat Simulation">
            <Network className="w-4 h-4" strokeWidth={2} />
          </button>
          <button onClick={handleSearchClick} className="p-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors border-b border-slate-200/50 dark:border-slate-700/50 flex items-center justify-center" title="Search Node">
            <Search className="w-4 h-4" strokeWidth={2} />
          </button>
          <button onClick={handleScreenshot} className="p-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors border-b border-slate-200/50 dark:border-slate-700/50 flex items-center justify-center" title="Take Screenshot">
            <Camera className="w-4 h-4" strokeWidth={2} />
          </button>
          <button onClick={() => setShowHelpModal(true)} className="p-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors flex items-center justify-center" title="Keyboard Shortcuts & Controls Help">
            <HelpCircle className="w-4 h-4" strokeWidth={2} />
          </button>
        </div>
      </div>

      {/* Keyboard Shortcuts & Help Modal */}
      {showHelpModal && (
        <div className="fixed inset-0 z-50 bg-black/40 dark:bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white dark:bg-[#1e2227] border border-slate-200 dark:border-slate-700 rounded-2xl max-w-md w-full p-6 shadow-2xl relative text-slate-800 dark:text-slate-200">
            <button 
              onClick={() => setShowHelpModal(false)}
              className="absolute top-4 right-4 p-1 text-slate-400 hover:text-slate-900 dark:hover:text-white rounded-lg hover:bg-slate-200 dark:hover:bg-slate-800 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
            <h3 className="text-lg font-bold mb-4 flex items-center gap-2 text-white">
              <HelpCircle className="w-5 h-5 text-blue-400" />
              Controls & Shortcuts Guide
            </h3>
            
            <div className="space-y-4 text-xs">
              <div>
                <h4 className="font-semibold text-blue-400 uppercase tracking-wider text-[10px] mb-2">3D Camera Navigation</h4>
                <div className="grid grid-cols-2 gap-2 bg-slate-100 dark:bg-[#252930] p-3 rounded-lg border border-slate-200 dark:border-slate-800">
                  <div><span className="font-semibold text-slate-700 dark:text-slate-300">Left Click + Drag:</span> Orbit / Rotate</div>
                  <div><span className="font-semibold text-slate-700 dark:text-slate-300">Right Click / 2-Finger:</span> Pan Camera</div>
                  <div><span className="font-semibold text-slate-700 dark:text-slate-300">Scroll / Pinch:</span> Zoom In/Out</div>
                  <div><span className="font-semibold text-slate-700 dark:text-slate-300">Double Click Node:</span> Expand/Collapse</div>
                </div>
              </div>

              <div>
                <h4 className="font-semibold text-purple-400 uppercase tracking-wider text-[10px] mb-2">Keyboard Shortcuts (When Node Selected)</h4>
                <div className="grid grid-cols-2 gap-2 bg-slate-100 dark:bg-[#252930] p-3 rounded-lg border border-slate-200 dark:border-slate-800 font-mono">
                  <div><span className="text-slate-700 dark:text-slate-300 font-sans">↑ Arrow Up:</span> Go to Parent</div>
                  <div><span className="text-slate-700 dark:text-slate-300 font-sans">↓ Arrow Down:</span> Go to First Child</div>
                  <div><span className="text-slate-700 dark:text-slate-300 font-sans">← Arrow Left:</span> Previous Sibling</div>
                  <div><span className="text-slate-700 dark:text-slate-300 font-sans">→ Arrow Right:</span> Next Sibling</div>
                </div>
              </div>

              <div className="p-3 bg-blue-500/10 border border-blue-500/20 rounded-lg text-blue-300 text-[11px] leading-relaxed">
                💡 <strong>Tip:</strong> Toggle <em>Show Prerequisites</em> in the Control Panel to visualize unlock dependencies (Green = Unlocks next, Red = Requires prior knowledge).
              </div>
            </div>

            <button 
              onClick={() => setShowHelpModal(false)}
              className="w-full mt-5 py-2 bg-blue-600 hover:bg-blue-500 text-white font-medium text-xs rounded-lg transition-colors"
            >
              Got it
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
