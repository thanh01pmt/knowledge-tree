import { useState, useEffect, useMemo, useCallback } from 'react';
import { ReactFlow, Background, Controls, MiniMap, useNodesState, useEdgesState, addEdge, MarkerType, Handle, Position } from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { parseFrontendData, computeRoadmapLayout } from './roadmapLayoutEngine';
import './RoadmapShRendererV2.css';

/**
 * Roadmap.sh Style ReactFlow Renderer V2
 * 
 * Uses EXACT positions from roadmap.sh API (frontend.json) OR
 * algorithmic layout engine that replicates roadmap.sh's positioning logic
 * 
 * - 156 nodes with precise x,y coordinates
 * - 69 edges with exact source/target
 * - Balsamiq hand-drawn style
 * - A4 canvas: 1097×3995 (viewBox: -675 -312 1097 3995)
 */

// ============================================================================
// CUSTOM NODE COMPONENTS - Balsamiq Style (matching roadmap.sh SVG)
// ============================================================================

function VerticalSpine({ data }) {
  const { height = 100, stroke = '#2B78E4', strokeDasharray = '0', strokeWidth = 3.5 } = data.style || {};
  const dash = strokeDasharray !== '0' 
    ? `repeating-linear-gradient(to bottom, ${stroke} 0, ${stroke} ${parseFloat(strokeDasharray) || 4}px, transparent ${parseFloat(strokeDasharray) || 4}px, transparent ${(parseFloat(strokeDasharray) || 4) + 8}px)`
    : 'none';
  
  return (
    <div className="vertical-spine" style={{
      width: '4px',
      height: `${height}px`,
      background: stroke,
      backgroundImage: dash,
      backgroundSize: '100% 100%',
    }}>
      <Handle type="target" position={Position.Top} className="spine-handle" />
      <Handle type="source" position={Position.Bottom} className="spine-handle" />
    </div>
  );
}

function HorizontalRule({ data }) {
  const { width = 200, stroke = '#2B78E4', strokeDasharray = '0', strokeWidth = 3.5 } = data.style || {};
  const dash = strokeDasharray !== '0' 
    ? `repeating-linear-gradient(to right, ${stroke} 0, ${stroke} ${parseFloat(strokeDasharray) || 4}px, transparent ${parseFloat(strokeDasharray) || 4}px, transparent ${(parseFloat(strokeDasharray) || 4) + 8}px)`
    : 'none';
  
  return (
    <div className="horizontal-rule" style={{
      width: `${width}px`,
      height: '4px',
      background: stroke,
      backgroundImage: dash,
    }}>
      <Handle type="target" position={Position.Left} />
      <Handle type="source" position={Position.Right} />
    </div>
  );
}

function SectionBox({ data, selected }) {
  const { style = {}, label = '' } = data;
  const h = style.height || 100;
  
  return (
    <div className={`section-box ${selected ? 'selected' : ''}`} style={{
      minWidth: '182px',
      minHeight: `${h}px`,
      backgroundColor: style.backgroundColor || '#ffffff',
      borderColor: style.borderColor || '#000000',
      borderWidth: '2.7px',
      borderRadius: '5px',
      position: 'relative',
    }}>
      <Handle type="target" position={Position.Top} />
      <Handle type="source" position={Position.Bottom} />
      <Handle type="target" position={Position.Left} />
      <Handle type="source" position={Position.Right} />
      {label && <div className="section-label">{label}</div>}
    </div>
  );
}

function TopicNode({ data, selected }) {
  const { label = '', style = {}, legend, progress, resources, description, note } = data;
  
  const isTopic = style.fontSize && style.fontSize >= 16;
  const topicColor = '#FDFF00';
  const subtopicColor = '#FFE599';
  const borderColor = '#000000';
  
  return (
    <div 
      className={`roadmap-node topic-node ${isTopic ? 'topic' : 'subtopic'} ${selected ? 'selected' : ''} ${legend?.label ? 'has-legend' : ''}`}
      style={{
        backgroundColor: isTopic ? topicColor : subtopicColor,
        borderColor,
        minWidth: isTopic ? '220px' : '180px',
        maxWidth: isTopic ? '300px' : '280px',
        padding: '10px 14px',
      }}
    >
      <Handle type="target" position={Position.Top} className="node-handle" />
      <Handle type="source" position={Position.Bottom} className="node-handle" />
      <Handle type="target" position={Position.Left} className="node-handle side" />
      <Handle type="source" position={Position.Right} className="node-handle side" />
      
      <div className="node-content">
        <span className={`node-label ${isTopic ? 'topic' : 'subtopic'}`}>{label}</span>
        
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
        
        {note && (
          <div className="node-note" style={{ fontSize: '11px', color: '#555', marginTop: '4px' }}>
            {note}
          </div>
        )}
      </div>
    </div>
  );
}

function ParagraphNode({ data }) {
  const { label = '', style = {} } = data;
  return (
    <div className="paragraph-node" style={{
      color: style.color || '#000000',
      fontSize: `${style.fontSize || 17}px`,
      textAlign: style.textAlign || 'left',
      maxWidth: '570px',
      lineHeight: 1.6,
      padding: style.padding || 0,
      backgroundColor: style.backgroundColor,
      borderColor: style.borderColor,
      borderWidth: style.borderColor ? '2.5px' : 0,
      borderStyle: style.borderColor ? 'solid' : 'none',
      borderRadius: '5px',
    }}>
      {label}
    </div>
  );
}

function TitleNode({ data }) {
  const { label = '', style = {} } = data;
  return (
    <div className="title-node" style={{
      fontSize: `${style.fontSize || 28}px`,
      fontWeight: style.fontWeight || 'bold',
      color: style.color || '#000000',
      textAlign: style.textAlign || 'center',
    }}>
      {label}
    </div>
  );
}

function ButtonNode({ data }) {
  const { label = '', style = {}, href } = data;
  return (
    <a 
      href={href} 
      target="_blank" 
      rel="noopener noreferrer"
      className="button-node"
      style={{
        backgroundColor: style.backgroundColor || '#2B78E4',
        color: style.color || '#FFFFFF',
        borderColor: style.borderColor || style.backgroundColor,
        fontSize: `${style.fontSize || 17}px`,
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

// ============================================================================
// CUSTOM EDGE COMPONENTS - Bezier Curves (matching roadmap.sh SVG)
// ============================================================================

function BezierEdge({ id, sourceX, sourceY, targetX, targetY, data, markerEnd }) {
  const { edgeStyle = 'solid' } = data;
  
  const isVertical = Math.abs(sourceX - targetX) < Math.abs(sourceY - targetY);
  
  let cp1x, cp1y, cp2x, cp2y;
  
  if (isVertical) {
    const midY = (sourceY + targetY) / 2;
    const offset = Math.min(80, Math.abs(targetY - sourceY) * 0.3);
    cp1x = sourceX + (targetX > sourceX ? offset : -offset);
    cp1y = midY;
    cp2x = targetX + (targetX > sourceX ? -offset : offset);
    cp2y = midY;
  } else {
    const midX = (sourceX + targetX) / 2;
    const offset = Math.min(60, Math.abs(targetX - sourceX) * 0.3);
    cp1x = midX;
    cp1y = sourceY + (targetY > sourceY ? offset : -offset);
    cp2x = midX;
    cp2y = targetY + (targetY > sourceY ? -offset : offset);
  }
  
  const path = `M${sourceX},${sourceY} C${cp1x},${cp1y} ${cp2x},${cp2y} ${targetX},${targetY}`;
  
  return (
    <path
      d={path}
      stroke="#2B78E4"
      strokeWidth={3.5}
      fill="none"
      strokeDasharray={edgeStyle === 'dashed' ? '8,8' : '0'}
      strokeLinecap="round"
      strokeLinejoin="round"
      markerEnd={markerEnd}
      style={{ opacity: edgeStyle === 'dashed' ? 0.8 : 1 }}
    />
  );
}

// ============================================================================
// MAIN RENDERER - Uses exact API data or algorithmic layout
// ============================================================================

export default function RoadmapShRendererV2({ 
  frontendData,
  onNodeClick,
  selectedNodeId,
  className = '',
  useAlgorithmic = true,
}) {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [viewport, setViewport] = useState({ x: 0, y: 0, zoom: 0.35 });
  const [layoutReady, setLayoutReady] = useState(false);

  const nodeTypes = useMemo(() => ({
    vertical: VerticalSpine,
    horizontal: HorizontalRule,
    section: SectionBox,
    topic: TopicNode,
    subtopic: TopicNode,
    paragraph: ParagraphNode,
    title: TitleNode,
    button: ButtonNode,
    legend: LegendNode,
  }), []);

  const edgeTypes = useMemo(() => ({
    bezier: BezierEdge,
    default: BezierEdge,
  }), []);

  // Use algorithmic layout (default) or exact API positions
  useEffect(() => {
    if (useAlgorithmic) {
      const { nodes: flowNodes, edges: flowEdges } = computeRoadmapLayout();
      setNodes(flowNodes);
      setEdges(flowEdges);
      setLayoutReady(true);
    } else if (frontendData?.nodes && frontendData?.edges) {
      const { nodes: flowNodes, edges: flowEdges } = parseFrontendData(frontendData);
      setNodes(flowNodes);
      setEdges(flowEdges);
      setLayoutReady(true);
    }
  }, [useAlgorithmic, frontendData, setNodes, setEdges]);

  const onConnect = useCallback((params) => setEdges((eds) => addEdge(params, eds)), [setEdges]);

  // Auto fit view on layout ready using onInit callback
  const handleInit = useCallback((reactFlowInstance) => {
    if (layoutReady) {
      reactFlowInstance.fitView({ padding: 0.1, duration: 500 });
    }
  }, [layoutReady]);

  if (!layoutReady) {
    return (
      <div className={`roadmap-sh-renderer-v2 ${className}`} style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f8fafc' }}>
        <div className="loading">Loading roadmap.sh exact layout...</div>
      </div>
    );
  }

  return (
    <div className={`roadmap-sh-renderer-v2 ${className}`} style={{ height: '100%', width: '100%', background: '#f8fafc' }}>
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
        onInit={handleInit}
        fitView={false}
        attributionPosition="bottom-right"
        defaultViewport={{ x: -675, y: -312, zoom: 0.35 }}
        connectionMode="strict"
        nodesDraggable={true}
        nodesConnectable={false}
        elementsSelectable={true}
        selectNodesOnDrag={false}
        minZoom={0.1}
        maxZoom={3}
      >
        <Background
          color="#E2E8F0"
          gap={20}
          size={1}
          style={{
            backgroundColor: '#FFFFFF',
            backgroundImage: 'radial-gradient(circle, #E2E8F0 1px, transparent 1px)',
            backgroundSize: '20px 20px',
          }}
        />
        <Controls position="bottom-right" />
        <MiniMap
          position="bottom-left"
          nodeColor={(node) => {
            if (node.type === 'topic') return '#FDFF00';
            if (node.type === 'subtopic') return '#FFE599';
            return '#94A3B8';
          }}
          maskColor="rgba(255, 255, 255, 0.9)"
        />
        
        <defs>
          <marker
            id="arrow-solid"
            viewBox="0 -5 10 10"
            refX={22}
            refY={0}
            markerWidth={10}
            markerHeight={10}
            orient="auto"
          >
            <path d="M0,-5L10,0L0,5" fill="#2B78E4" />
          </marker>
        </defs>
      </ReactFlow>
      
      <div className="renderer-toolbar-v2">
        <div className="toolbar-left">
          <h3>Frontend Developer Roadmap</h3>
          <span className="subtitle">
            {useAlgorithmic ? 'Algorithmic replica (client-side)' : 'Exact roadmap.sh layout from live API'}
          </span>
        </div>
        <div className="toolbar-center">
          <span className="legend-item">
            <span className="legend-node topic"></span> Topics
          </span>
          <span className="legend-item">
            <span className="legend-node subtopic"></span> Subtopics
          </span>
          <span className="legend-item">
            <span className="legend-line solid"></span> Required
          </span>
          <span className="legend-item">
            <span className="legend-line dashed"></span> Alternative
          </span>
        </div>
        <div className="toolbar-right">
          <span className="zoom-indicator">{Math.round(viewport.zoom * 100)}%</span>
          <button className="icon-btn" onClick={() => setViewport(v => ({...v, zoom: Math.min(3, v.zoom * 1.2)}))} title="Zoom In">+</button>
          <button className="icon-btn" onClick={() => setViewport(v => ({...v, zoom: Math.max(0.1, v.zoom / 1.2)}))} title="Zoom Out">−</button>
          <button className="icon-btn" onClick={() => setViewport({ x: -675, y: -312, zoom: 0.35 })} title="Fit View">⛶</button>
        </div>
      </div>
    </div>
  );
}