import { useState, useEffect, useMemo, useCallback } from 'react';
import { ReactFlow, Background, Controls, MiniMap, useNodesState, useEdgesState, addEdge, MarkerType, Handle, Position } from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import './RoadmapShRenderer.css';
/**
 * Roadmap.sh Style ReactFlow Renderer
 * 
 * Architecture:
 * - Vertical connector lines (type: 'vertical') - structural spine
 * - Section headers (type: 'section') - major category headers
 * - Topic nodes (type: 'topic') - main topics (TOPIC type from raw)
 * - Subtopic nodes (type: 'subtopic') - subtopics (SUBTOPIC type from raw)
 * - Horizontal connectors (type: 'horizontal') - section dividers
 * - Paragraph nodes (type: 'paragraph') - description text
 * - Buttons/Links (type: 'button') - external resources
 * 
 * Edge styles:
 * - solid: prerequisite relationship (required)
 * - dashed: alternative/optional relationship
 */

// ============================================================================
// CUSTOM NODE COMPONENTS
// ============================================================================

function VerticalNode({ data }) {
  const { style = {} } = data;
  return (
    <div 
      className="vertical-node"
      style={{
        width: '20px',
        height: style.height || '100%',
        background: style.stroke || '#2B78E4',
        backgroundImage: `repeating-linear-gradient(
          to bottom,
          ${style.stroke || '#2B78E4'},
          ${style.stroke || '#2B78E4'} ${parseFloat(style.strokeDasharray) || 1}px,
          transparent ${parseFloat(style.strokeDasharray) || 1}px,
          transparent ${(parseFloat(style.strokeDasharray) || 1) + 8}px
        )`,
        backgroundSize: '100% 100%',
      }}
    >
      <Handle type="target" position={Position.Top} className="vertical-handle" />
      <Handle type="source" position={Position.Bottom} className="vertical-handle" />
    </div>
  );
}

function SectionNode({ data }) {
  const { label = '', style = {} } = data;
  return (
    <div className="section-node" style={{
      backgroundColor: style.backgroundColor || '#ffffff',
      borderColor: style.borderColor || '#000000',
      minWidth: '180px',
      minHeight: '80px',
    }}>
      <Handle type="target" position={Position.Top} />
      <Handle type="source" position={Position.Bottom} />
      <div className="section-content">{label}</div>
    </div>
  );
}

function TopicNode({ data, selected, id }) {
  const { 
    label = '', 
    style = {}, 
    legend,
    progress,
    resources,
    description 
  } = data;
  
  const isTopic = style.fontSize && style.fontSize >= 16;
  const nodeClass = isTopic ? 'topic-node' : 'subtopic-node';
  
  return (
    <div 
      className={`roadmap-node ${nodeClass} ${selected ? 'selected' : ''} ${legend?.label ? 'has-legend' : ''}`}
      style={{
        minWidth: '200px',
        maxWidth: '320px',
        fontSize: `${style.fontSize || 14}px`,
        textAlign: style.textAlign || 'center',
        justifyContent: style.justifyContent || 'center',
      }}
    >
      <Handle type="target" position={Position.Top} className="node-handle" />
      <Handle type="source" position={Position.Bottom} className="node-handle" />
      
      <div className="node-content">
        <span className="node-label">{label}</span>
        
        {legend && (
          <div className="node-legend" style={{ 
            backgroundColor: legend.color,
            borderColor: legend.color,
          }}>
            {legend.label}
          </div>
        )}
        
        {progress !== undefined && (
          <div className="node-progress">
            <div className="progress-bar" style={{ width: `${progress}%` }}></div>
          </div>
        )}
        
        {description && (
          <div className="node-description">{description}</div>
        )}
        
        {resources && resources.length > 0 && (
          <div className="node-resources">
            {resources.slice(0, 3).map((r, i) => (
              <a key={i} href={r.url} target="_blank" rel="noopener noreferrer" className="resource-link">
                {r.title}
              </a>
            ))}
            {resources.length > 3 && (
              <span className="more-resources">+{resources.length - 3} more</span>
            )}
          </div>
        )}
      </div>
      
      <Handle type="target" position={Position.Left} className="node-handle side" />
      <Handle type="source" position={Position.Right} className="node-handle side" />
    </div>
  );
}

function HorizontalNode({ data }) {
  const { style = {} } = data;
  return (
    <div 
      className="horizontal-node"
      style={{
        width: style.width || '100%',
        height: '4px',
        background: style.stroke || '#e2e8f0',
        backgroundImage: style.strokeDasharray ? `repeating-linear-gradient(
          to right,
          ${style.stroke || '#e2e8f0'},
          ${style.stroke || '#e2e8f0'} ${parseFloat(style.strokeDasharray) || 10}px,
          transparent ${parseFloat(style.strokeDasharray) || 10}px,
          transparent ${(parseFloat(style.strokeDasharray) || 10) + 10}px
        )` : 'none',
      }}
    >
      <Handle type="target" position={Position.Left} />
      <Handle type="source" position={Position.Right} />
    </div>
  );
}

function ParagraphNode({ data }) {
  const { label = '', style = {} } = data;
  return (
    <div className="paragraph-node" style={{
      color: style.color || '#64748b',
      fontSize: `${style.fontSize || 13}px`,
      textAlign: style.textAlign || 'left',
      maxWidth: '400px',
      lineHeight: 1.6,
    }}>
      {label}
    </div>
  );
}

function ButtonNode({ data }) {
  const { label = '', style = {}, url } = data;
  return (
    <a 
      href={url} 
      target="_blank" 
      rel="noopener noreferrer"
      className="button-node"
      style={{
        backgroundColor: style.backgroundColor || '#2B78E4',
        color: style.color || '#ffffff',
        borderColor: style.borderColor || '#2B78E4',
      }}
    >
      {label}
    </a>
  );
}

function LegendNode({ data }) {
  const { legends = [] } = data;
  return (
    <div className="legend-node">
      {legends.map((l, i) => (
        <div key={i} className="legend-item" style={{ borderColor: l.color }}>
          <span className="legend-color" style={{ backgroundColor: l.color }}></span>
          <span className="legend-label">{l.label}</span>
        </div>
      ))}
    </div>
  );
}

function TitleNode({ data }) {
  const { label = '', style = {} } = data;
  return (
    <div className="title-node" style={{
      fontSize: `${style.fontSize || 28}px`,
      fontWeight: style.fontWeight || 'bold',
      color: style.color || '#0f172a',
      textAlign: style.textAlign || 'center',
    }}>
      {label}
    </div>
  );
}

// ============================================================================
// CUSTOM EDGE COMPONENTS
// ============================================================================

function SolidEdge({ id, sourceX, sourceY, targetX, targetY, data }) {
  const path = getStraightPath(sourceX, sourceY, targetX, targetY);
  return (
    <path
      d={path}
      stroke="#2B78E4"
      strokeWidth={2}
      fill="none"
      markerEnd="url(#arrow-solid)"
      style={{ 
        opacity: 0.8,
        filter: 'drop-shadow(0 2px 4px rgba(43, 120, 228, 0.3))'
      }}
    />
  );
}

function DashedEdge({ id, sourceX, sourceY, targetX, targetY, data }) {
  const path = getStraightPath(sourceX, sourceY, targetX, targetY);
  return (
    <path
      d={path}
      stroke="#94a3b8"
      strokeWidth={2}
      fill="none"
      strokeDasharray="6,4"
      markerEnd="url(#arrow-dashed)"
      style={{ opacity: 0.6 }}
    />
  );
}

function getStraightPath(sx, sy, tx, ty) {
  // Roadmap.sh uses straight lines with slight curve
  const mx = (sx + tx) / 2;
  const my = (sy + ty) / 2;
  return `M${sx},${sy} Q${mx},${my} ${tx},${ty}`;
}

// ============================================================================
// ROADMAP DATA PROCESSOR
// ============================================================================

function processRawRoadmap(rawData) {
  const { topics = [] } = rawData;
  const nodes = [];
  const edges = [];
  const nodeMap = new Map(); // prerequisite name -> node id
  
  // First pass: create all nodes
  topics.forEach((topic, index) => {
    const nodeId = `node-${topic.order || index}`;
    const isTopic = topic.type === 'TOPIC';
    const isSubtopic = topic.type === 'SUBTOPIC';
    
    let node;
    if (isTopic) {
      node = {
        id: nodeId,
        type: 'topic',
        position: { x: 0, y: 0 }, // Will be set by layout
        data: {
          label: topic.name,
          style: { fontSize: 17, justifyContent: 'flex-start', textAlign: 'center' },
          legend: topic.legend,
          progress: topic.progress,
          resources: topic.resources,
          description: topic.description,
        },
        originalData: topic,
      };
    } else {
      node = {
        id: nodeId,
        type: 'subtopic',
        position: { x: 0, y: 0 },
        data: {
          label: topic.name,
          style: { fontSize: 14, justifyContent: 'flex-start', textAlign: 'center' },
          legend: topic.legend,
        },
        originalData: topic,
      };
    }
    
    nodes.push(node);
    nodeMap.set(topic.name, nodeId);
  });
  
  // Second pass: create edges based on prerequisites
  topics.forEach((topic) => {
    const targetId = nodeMap.get(topic.name);
    if (!targetId) return;
    
    const prereqName = topic.prerequisite;
    if (!prereqName) return;
    
    const sourceId = nodeMap.get(prereqName);
    if (!sourceId) return;
    
    // Determine edge style: solid for direct prerequisite, dashed for alternative
    const edgeStyle = topic.legend?.label === 'Alternative Option' ? 'dashed' : 'solid';
    
    edges.push({
      id: `edge-${sourceId}-${targetId}`,
      source: sourceId,
      target: targetId,
      type: edgeStyle === 'dashed' ? 'dashed' : 'solid',
      data: { edgeStyle },
      style: { 
        stroke: edgeStyle === 'dashed' ? '#94a3b8' : '#2B78E4',
        strokeWidth: 2,
      },
      markerEnd: {
        type: MarkerType.ArrowClosed,
        color: edgeStyle === 'dashed' ? '#94a3b8' : '#2B78E4',
        width: 16,
        height: 16,
      },
    });
  });
  
  return { nodes, edges };
}

function applyHierarchicalLayout(nodes, edges) {
  // Group nodes by their prerequisite chain depth
  const nodeMap = new Map(nodes.map(n => [n.id, n]));
  const adjacency = new Map();
  const reverseAdjacency = new Map();
  
  edges.forEach(e => {
    if (!adjacency.has(e.source)) adjacency.set(e.source, []);
    adjacency.get(e.source).push(e.target);
    if (!reverseAdjacency.has(e.target)) reverseAdjacency.set(e.target, []);
    reverseAdjacency.get(e.target).push(e.source);
  });
  
  // Find root nodes (no incoming edges)
  const roots = nodes.filter(n => !reverseAdjacency.has(n.id) || reverseAdjacency.get(n.id).length === 0);
  
  // BFS to assign levels
  const levels = new Map();
  const queue = [...roots.map(r => ({ id: r.id, level: 0 }))];
  const visited = new Set();
  
  while (queue.length > 0) {
    const { id, level } = queue.shift();
    if (visited.has(id)) continue;
    visited.add(id);
    levels.set(id, level);
    
    const children = adjacency.get(id) || [];
    children.forEach(childId => {
      if (!visited.has(childId)) {
        queue.push({ id: childId, level: level + 1 });
      }
    });
  }
  
  // Assign positions
  const levelGroups = new Map();
  levels.forEach((level, id) => {
    if (!levelGroups.has(level)) levelGroups.set(level, []);
    levelGroups.get(level).push(id);
  });
  
  const NODE_WIDTH = 280;
  const NODE_HEIGHT = 60;
  const HORIZONTAL_SPACING = 320;
  const VERTICAL_SPACING = 100;
  
  levelGroups.forEach((nodeIds, level) => {
    const startX = -(nodeIds.length - 1) * HORIZONTAL_SPACING / 2;
    nodeIds.forEach((nodeId, idx) => {
      const node = nodeMap.get(nodeId);
      if (node) {
        node.position = {
          x: startX + idx * HORIZONTAL_SPACING,
          y: level * VERTICAL_SPACING + 100,
        };
      }
    });
  });
  
  return nodes;
}

// ============================================================================
// MAIN RENDERER COMPONENT
// ============================================================================

export default function RoadmapShRenderer({ 
  rawData,
  onNodeClick,
  selectedNodeId,
  className = '',
}) {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [viewport, setViewport] = useState({ x: 0, y: 0, zoom: 1 });
  const [layoutReady, setLayoutReady] = useState(false);
  const nodeTypes = useMemo(() => ({
    vertical: VerticalNode,
    section: SectionNode,
    topic: TopicNode,
    subtopic: TopicNode,
    horizontal: HorizontalNode,
    paragraph: ParagraphNode,
    button: ButtonNode,
    legend: LegendNode,
    title: TitleNode,
  }), []);

  const edgeTypes = useMemo(() => ({
    solid: SolidEdge,
    dashed: DashedEdge,
  }), []);

  // Process data when rawData changes
  useEffect(() => {
    if (!rawData) return;
    
    const { nodes: processedNodes, edges: processedEdges } = processRawRoadmap(rawData);
    const laidOutNodes = applyHierarchicalLayout(processedNodes, processedEdges);
    
    setNodes(laidOutNodes);
    setEdges(processedEdges);
    setLayoutReady(true);
  }, [rawData, setNodes, setEdges]);

  const onConnect = useCallback((params) => setEdges((eds) => addEdge(params, eds)), [setEdges]);

  if (!layoutReady) {
    return (
      <div className={`roadmap-sh-renderer ${className}`} style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f8fafc' }}>
        <div className="loading">Loading roadmap...</div>
      </div>
    );
  }

  return (
    <div className={`roadmap-sh-renderer ${className}`} style={{ height: '100%', width: '100%', background: '#f8fafc' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onViewportChange={setViewport}
        viewport={viewport}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        fitView={true}
        attributionPosition="bottom-right"
        defaultViewport={{ x: 0, y: 0, zoom: 0.7 }}
        connectionMode="strict"
        nodesDraggable={true}
        nodesConnectable={true}
        elementsSelectable={true}
        selectNodesOnDrag={false}
      >
        <Background 
          color="#e2e8f0" 
          gap={20} 
          size={1} 
          style={{ 
            backgroundColor: '#f8fafc',
          }}
        />
        <Controls position="bottom-right" />
        <MiniMap 
          position="bottom-left" 
          nodeColor={(node) => node.type === 'topic' ? '#2B78E4' : '#94a3b8'}
          maskColor="rgba(248, 250, 252, 0.9)"
        />
        
        <defs>
          <marker 
            id="arrow-solid" 
            viewBox="0 -5 10 10" 
            refX={20} 
            refY={0} 
            markerWidth={8} 
            markerHeight={8} 
            orient="auto"
          >
            <path d="M0,-5L10,0L0,5" fill="#2B78E4" />
          </marker>
          <marker 
            id="arrow-dashed" 
            viewBox="0 -5 10 10" 
            refX={20} 
            refY={0} 
            markerWidth={8} 
            markerHeight={8} 
            orient="auto"
          >
            <path d="M0,-5L10,0L0,5" fill="#94a3b8" />
          </marker>
        </defs>
      </ReactFlow>
      
      <div className="renderer-toolbar">
        <div className="toolbar-left">
          <h3>{rawData?.slug || 'Roadmap'}</h3>
        </div>
        <div className="toolbar-center">
          <span className="legend-item">
            <span className="legend-line solid"></span> Required
          </span>
          <span className="legend-item">
            <span className="legend-line dashed"></span> Alternative
          </span>
        </div>
        <div className="toolbar-right">
          <span className="zoom-indicator">{Math.round(viewport.zoom * 100)}%</span>
        </div>
      </div>
    </div>
  );
}