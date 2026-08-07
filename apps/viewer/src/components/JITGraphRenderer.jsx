import React, { useEffect, useCallback, useMemo, useState } from 'react';
import { 
  ReactFlow, 
  Background, 
  Controls, 
  MiniMap, 
  Handle, 
  Position, 
  MarkerType, 
  useNodesState,
  useEdgesState 
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import './JITGraphRenderer.css';

// ============================================================================
// CONSTANTS & DESIGN TOKENS
// ============================================================================

const PHASE_COLORS = {
  1: '#0e7c6b', 2: '#27ae60', 3: '#8e44ad', 
  4: '#f39c12', 5: '#e74c3c', 6: '#16a085',
};

const PHASE_NAMES = {
  1: 'THIẾT LẬP', 2: 'DATA MODEL', 3: 'AI CORE', 
  4: 'CẤU HÌNH', 5: 'UI', 6: 'KIỂM THỬ',
};

// Knowledge State markers
const KNOWLEDGE_STATE = {
  NEW: { icon: '●', color: '#0e7c6b', label: 'NEW' },
  REVIEW: { icon: '◐', color: '#4f46e5', label: 'REVIEW' },
  ASSUMED: { icon: '○', color: '#7a7a85', label: 'ASSUMED' },
};

// Knowledge Tier
const KNOWLEDGE_TIER = {
  CORE: { icon: '●', color: '#0e7c6b', label: 'CORE' },
  SUPPORT: { icon: '◐', color: '#b4530c', label: 'SUPPORT' },
  OPTIONAL: { icon: '○', color: '#7a7a85', label: 'OPTIONAL' },
};

const NODE_HEIGHT = 52;
const V_GAP_SAME_PHASE = 16;
const V_GAP_PHASE_BREAK = 48;

// ============================================================================
// UTILITIES
// ============================================================================

function truncateLabel(label, maxWords = 10) {
  const words = label.trim().split(/\s+/);
  if (words.length <= maxWords) return label;
  return words.slice(0, maxWords).join(' ') + '…';
}

function formatTime(hours) {
  if (hours < 1) return `${Math.round(hours * 60)}M`;
  const h = Math.floor(hours);
  const m = Math.round((hours - h) * 60);
  return m > 0 ? `${h}H ${m}M` : `${h}H`;
}

// ============================================================================
// LAYOUT ENGINE: Vertical Flow with Phase Headers + Intra-Phase DAG
// ============================================================================

function computeVerticalLayout(nodes, edges) {
  // Build adjacency
  const edgeMap = new Map();
  const reverseEdgeMap = new Map();
  edges.forEach(e => {
    if (!edgeMap.has(e.source)) edgeMap.set(e.source, []);
    edgeMap.get(e.source).push(e.target);
    if (!reverseEdgeMap.has(e.target)) reverseEdgeMap.set(e.target, []);
    reverseEdgeMap.get(e.target).push(e.source);
  });
  
  // Get flow order from START
  const startNode = nodes.find(n => n.data.nodeType === 'start');
  const flowOrder = [];
  const visited = new Set();
  
  function traverse(nodeId) {
    if (visited.has(nodeId)) return;
    visited.add(nodeId);
    const node = nodes.find(n => n.id === nodeId);
    if (node) flowOrder.push(node);
    const next = edgeMap.get(nodeId) || [];
    next.forEach(traverse);
  }
  
  if (startNode) traverse(startNode.id);
  nodes.forEach(n => { if (!visited.has(n.id)) flowOrder.push(n); });
  
  // Build Knowledge Registry (global dedup + state)
  const knowledgeRegistry = new Map(); // knowledgeLabel -> { firstCardId, count, nodes: [] }
  const implementKnowledgeMap = new Map(); // implementId -> [{ knowledgeNode, state, tier }]
  
  // First pass: collect all knowledge nodes per implement
  flowOrder.forEach(n => {
    if (n.data.nodeType === 'knowledge') {
      const idx = flowOrder.findIndex(f => f.id === n.id);
      for (let i = idx - 1; i >= 0; i--) {
        if (flowOrder[i].data.nodeType === 'implement' || flowOrder[i].data.nodeType === 'verify') {
          const implId = flowOrder[i].id;
          if (!implementKnowledgeMap.has(implId)) implementKnowledgeMap.set(implId, []);
          
          // Determine state & tier
          const label = (n.data.label || '').trim().toLowerCase();
          const isFirstOccurrence = !knowledgeRegistry.has(label);
          
          let state = 'NEW';
          let tier = 'CORE';
          
          if (isFirstOccurrence) {
            state = 'NEW';
            knowledgeRegistry.set(label, { firstCardId: implId, count: 1, nodes: [n] });
          } else {
            state = 'REVIEW';
            const reg = knowledgeRegistry.get(label);
            reg.count++;
            reg.nodes.push(n);
          }
          
          // Heuristic tier assignment
          const coreKeywords = ['dataclass', 'json', 'http', 'api', 'async', 'class', 'function', 'type hint', 'enum', 'path', 'file'];
          const optionalKeywords = ['retry', 'timeout', 'schema', 'validation', 'logging', 'monitoring', 'advanced'];
          
          if (coreKeywords.some(k => label.includes(k))) tier = 'CORE';
          else if (optionalKeywords.some(k => label.includes(k))) tier = 'OPTIONAL';
          else tier = 'SUPPORT';
          
          implementKnowledgeMap.get(implId).push({ 
            knowledgeNode: n, 
            state, 
            tier,
            firstCardId: knowledgeRegistry.get(label)?.firstCardId 
          });
          break;
        }
      }
    }
  });
  
  // Filter display nodes
  const displayNodes = flowOrder.filter(n => 
    ['implement', 'verify', 'phase', 'start', 'end'].includes(n.data.nodeType)
  );
  
  // Compute vertical positions
  const positions = new Map();
  let y = 40;
  
  displayNodes.forEach((node, idx) => {
    const isPhase = node.data.nodeType === 'phase';
    const isImplement = node.data.nodeType === 'implement';
    const isVerify = node.data.nodeType === 'verify';
    
    if (idx > 0) {
      const prev = displayNodes[idx - 1];
      const prevPhase = prev.data.phase;
      const currPhase = node.data.phase;
      if (prevPhase && currPhase && prevPhase !== currPhase) {
        y += V_GAP_PHASE_BREAK;
      } else {
        y += V_GAP_SAME_PHASE;
      }
    }
    
    positions.set(node.id, { 
      x: 40,
      y,
      isPhase,
      isImplement,
      isVerify,
      knowledgeItems: isImplement || isVerify ? (implementKnowledgeMap.get(node.id) || []) : [],
    });
    
    y += NODE_HEIGHT;
  });
  
  // Apply positions
  const positionedNodes = displayNodes.map(node => {
    const pos = positions.get(node.id) || { x: 40, y: 0 };
    const truncatedLabel = truncateLabel(node.data.label || '');
    
    return {
      ...node,
      position: { x: pos.x, y: pos.y },
      data: {
        ...node.data,
        label: truncatedLabel,
        _fullLabel: node.data.label,
        _knowledgeItems: pos.knowledgeItems || [],
        _isPhase: pos.isPhase,
        _isImplement: pos.isImplement,
        _isVerify: pos.isVerify,
      },
      sourcePosition: Position.Bottom,
      targetPosition: Position.Top,
      style: {
        width: pos.isPhase ? 900 : 880,
        minHeight: NODE_HEIGHT,
      },
      draggable: true,
      selectable: true,
    };
  });
  
  // Create edges (skip phase-to-phase)
  const displayEdges = [];
  for (let i = 0; i < displayNodes.length - 1; i++) {
    const source = displayNodes[i];
    const target = displayNodes[i + 1];
    if (!(source.data.nodeType === 'phase' && target.data.nodeType === 'phase')) {
      displayEdges.push({
        id: `edge-${source.id}-${target.id}`,
        source: source.id,
        target: target.id,
        type: 'smoothstep',
        style: { stroke: '#0e7c6b', strokeWidth: 2 },
        markerEnd: { type: MarkerType.ArrowClosed, color: '#0e7c6b', width: 14, height: 14 },
        animated: true,
      });
    }
  }
  
  return { nodes: positionedNodes, edges: displayEdges };
}

// ============================================================================
// PARSE JIT GRAPH DATA
// ============================================================================

function parseJITGraphData(frontendData) {
  if (!frontendData?.nodes || !frontendData?.edges) return { nodes: [], edges: [] };
  
  const baseNodes = frontendData.nodes.map((apiNode) => {
    const nodeData = apiNode.data || {};
    const phase = nodeData.phase;
    const nodeType = nodeData.nodeType || apiNode.type || 'topic';
    const color = nodeData.color || (phase ? PHASE_COLORS[phase] : '#333');
    
    return {
      id: apiNode.id,
      type: 'actionNode',
      data: {
        label: nodeData.label || '',
        note: nodeData.note,
        phase: phase,
        nodeType: nodeType,
        color: color,
      },
      style: { height: NODE_HEIGHT },
      draggable: false,
      selectable: true,
    };
  });
  
  const baseEdges = frontendData.edges.map((apiEdge, idx) => ({
    id: apiEdge.id || `edge-${apiEdge.source}-${apiEdge.target}-${idx}`,
    source: apiEdge.source,
    target: apiEdge.target,
    type: 'smoothstep',
    data: { edgeStyle: apiEdge.data?.edgeStyle || 'solid' },
    style: { stroke: '#0e7c6b', strokeWidth: 2 },
    markerEnd: { type: MarkerType.ArrowClosed, color: '#0e7c6b', width: 14, height: 14 },
    animated: true,
  }));
  
  return { nodes: baseNodes, edges: baseEdges };
}

// ============================================================================
// KNOWLEDGE ITEM COMPONENT
// ============================================================================

function KnowledgeItem({ item, index }) {
  const { state, tier, firstCardId, knowledgeNode } = item;
  const stateInfo = KNOWLEDGE_STATE[state] || KNOWLEDGE_STATE.NEW;
  const tierInfo = KNOWLEDGE_TIER[tier] || KNOWLEDGE_TIER.CORE;
  const label = truncateLabel(knowledgeNode.data.label || '', 8);
  const isOptional = tier === 'OPTIONAL';
  
  const noteText = state === 'REVIEW' 
    ? `đã học ở card ${firstCardId ? firstCardId.slice(0, 8) : 'trước'}`
    : state === 'ASSUMED' 
      ? 'giả định đã biết' 
      : '';
  
  return React.createElement('li', {
    className: `action-knowledge-item ${isOptional ? 'optional' : ''}`,
    style: { 
      fontSize: '11px', 
      paddingLeft: '18px', 
      position: 'relative', 
      marginBottom: '4px',
      color: isOptional ? '#7a7a85' : '#1a1a1a',
      lineHeight: 1.5,
      listStyle: 'none',
    }
  }, [
    React.createElement('span', {
      key: 'num',
      style: { 
        position: 'absolute', left: 0, 
        fontFamily: '"IBM Plex Mono", monospace', 
        fontSize: '10px', color: '#8a8a8a' 
      }
    }, `${index + 1}.`),
    
    // State icon
    React.createElement('span', {
      key: 'state',
      style: { 
        marginRight: '6px', 
        color: stateInfo.color,
        fontSize: '10px' 
      }
    }, stateInfo.icon),
    
    // Tier badge (for core/support)
    tier !== 'CORE' && React.createElement('span', {
      key: 'tier',
      style: { 
        marginRight: '6px', 
        fontSize: '8px', 
        fontWeight: 600,
        color: tierInfo.color,
        background: `${tierInfo.color}15`,
        padding: '1px 5px',
        borderRadius: '3px',
        textTransform: 'uppercase'
      }
    }, tierInfo.label),
    
    React.createElement('span', { key: 'label' }, label),
    
    noteText && React.createElement('span', {
      key: 'note',
      className: `note ${state.toLowerCase()}`,
      style: { 
        fontSize: '9px', 
        fontStyle: 'italic', 
        color: state === 'REVIEW' ? '#4f46e5' : '#7a7a85',
        marginLeft: '8px' 
      }
    }, ` — ${noteText}`),
  ]);
}

// ============================================================================
// CUSTOM NODE COMPONENTS
// ============================================================================

function ActionNode({ data, selected, sourcePosition, targetPosition }) {
  const { label = '', note, color, nodeType, phase, _fullLabel, _knowledgeItems, _isPhase, _isImplement, _isVerify } = data;
  const pColor = color || (phase ? PHASE_COLORS[phase] : '#333');
  const pName = phase ? PHASE_NAMES[phase] : '';
  
  if (_isPhase) {
    return React.createElement('div', {
      className: `action-node action-node-phase ${selected ? 'selected' : ''}`,
      style: { 
        backgroundColor: '#f4faf7', borderColor: pColor, borderWidth: '2px',
        borderStyle: 'solid', borderRadius: '6px', minWidth: '880px',
        padding: '8px 16px', height: NODE_HEIGHT, display: 'flex', alignItems: 'center',
        position: 'relative', boxShadow: selected ? '0 4px 12px rgba(0,0,0,0.1)' : '0 1px 3px rgba(0,0,0,0.05)',
      }
    }, [
      React.createElement(Handle, { key: 't', type: 'target', position: Position.Top, className: 'action-handle', style: { background: pColor }}),
      React.createElement(Handle, { key: 'b', type: 'source', position: Position.Bottom, className: 'action-handle', style: { background: pColor }}),
      React.createElement('div', { key: 'content', style: { display: 'flex', alignItems: 'center', gap: '12px', width: '100%' } }, [
        React.createElement('span', { key: 'dot', style: { width: '10px', height: '10px', borderRadius: '50%', background: pColor }}),
        React.createElement('span', { key: 'label', style: { fontFamily: '"IBM Plex Mono", monospace', fontWeight: 600, fontSize: '13px', color: pColor, textTransform: 'uppercase', letterSpacing: '0.03em' } }, `Phase ${phase} — ${pName}`),
      ]),
    ]);
  }
  
  if (nodeType === 'start') {
    return React.createElement('div', {
      className: `action-node action-node-start ${selected ? 'selected' : ''}`,
      style: { backgroundColor: '#d4edda', borderColor: '#28a745', borderWidth: '2px', borderStyle: 'solid', borderRadius: '6px', padding: '10px 16px', height: NODE_HEIGHT, display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: '13px', color: '#155724', fontFamily: '"IBM Plex Sans", sans-serif' }
    }, [React.createElement(Handle, { key: 'b', type: 'source', position: Position.Bottom, className: 'action-handle', style: { background: '#28a745' }}), '▶ START']);
  }
  
  if (nodeType === 'end') {
    return React.createElement('div', {
      className: `action-node action-node-end ${selected ? 'selected' : ''}`,
      style: { backgroundColor: '#f8d7da', borderColor: '#dc3545', borderWidth: '2px', borderStyle: 'solid', borderRadius: '6px', padding: '10px 16px', height: NODE_HEIGHT, display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: '13px', color: '#721c24', fontFamily: '"IBM Plex Sans", sans-serif' }
    }, [React.createElement(Handle, { key: 't', type: 'target', position: Position.Top, className: 'action-handle', style: { background: '#dc3545' }}), '■ END']);
  }
  
  // VERIFY CARD (full width, no knowledge column)
  if (_isVerify) {
    return React.createElement('div', {
      className: `action-node action-node-verify ${selected ? 'selected' : ''}`,
      style: { 
        backgroundColor: '#f4faf7', borderColor: '#0f9d63', borderWidth: '1px',
        borderStyle: 'dashed', borderRadius: '6px', width: '880px',
        padding: '10px 16px', minHeight: NODE_HEIGHT, display: 'flex', alignItems: 'center',
        position: 'relative', boxShadow: selected ? '0 4px 12px rgba(0,0,0,0.1)' : '0 1px 3px rgba(0,0,0,0.05)',
      },
      title: _fullLabel
    }, [
      React.createElement(Handle, { key: 't', type: 'target', position: Position.Top, className: 'action-handle', style: { background: '#0f9d63' }}),
      React.createElement(Handle, { key: 'b', type: 'source', position: Position.Bottom, className: 'action-handle', style: { background: '#0f9d63' }}),
      React.createElement('div', { key: 'content', style: { display: 'flex', alignItems: 'center', gap: '12px', width: '100%' } }, [
        React.createElement('span', { key: 'icon', style: { color: '#0f9d63', fontSize: '14px' } }, '✓'),
        React.createElement('span', { key: 'label', style: { fontFamily: '"IBM Plex Mono", monospace', fontWeight: 600, fontSize: '11px', color: '#0f9d63' } }, `VERIFY: ${label}`),
        note && React.createElement('span', { key: 'desc', style: { fontSize: '10px', color: '#5c5c5c', flex: 1 } }, note),
      ]),
    ]);
  }
  
  // IMPLEMENT CARD: 2-Column (Implementation | Knowledge)
  const knowledgeItems = (_knowledgeItems || []).map((k, i) => 
    React.createElement(KnowledgeItem, { key: k.knowledgeNode.id, item: k, index: i })
  );
  
  return React.createElement('div', {
    className: `action-node action-node-implement ${selected ? 'selected' : ''}`,
    style: { 
      backgroundColor: '#fff', borderColor: '#d8d8d8', borderWidth: '1px',
      borderStyle: 'solid', borderRadius: '6px', width: '880px',
      padding: '0', minHeight: NODE_HEIGHT,
      display: 'grid', gridTemplateColumns: '56% 44%',
      position: 'relative',
      boxShadow: selected ? '0 4px 12px rgba(0,0,0,0.1)' : '0 1px 3px rgba(0,0,0,0.05)',
    },
    title: _fullLabel
  }, [
    React.createElement(Handle, { key: 't', type: 'target', position: Position.Top, className: 'action-handle', style: { background: pColor }}),
    React.createElement(Handle, { key: 'b', type: 'source', position: Position.Bottom, className: 'action-handle', style: { background: pColor }}),
    
    // LEFT COLUMN: IMPLEMENTATION
    React.createElement('div', {
      key: 'left',
      className: 'action-col-left',
      style: { 
        padding: '10pt 12pt', display: 'flex', flexDirection: 'column', 
        borderRight: '1px solid #d8d8d8', minHeight: NODE_HEIGHT,
      }
    }, [
      React.createElement('div', { key: 'header', style: { display: 'flex', alignItems: 'baseline', gap: '6pt', marginBottom: '4pt' } }, [
        React.createElement('span', { key: 'idx', style: { fontFamily: '"IBM Plex Mono", monospace', fontSize: '9pt', color: '#8a8a8a' } }, '▶'),
        React.createElement('span', { key: 'fn', style: { fontFamily: '"IBM Plex Mono", monospace', fontWeight: 600, fontSize: '10pt', color: '#1a1a1a' } }, label),
      ]),
      note && React.createElement('div', { 
        key: 'desc', 
        style: { fontSize: '9.5pt', color: '#5c5c5c', lineHeight: 1.5, fontFamily: '"IBM Plex Sans", sans-serif' } 
      }, note),
    ]),
    
    // RIGHT COLUMN: KNOWLEDGE
    React.createElement('div', {
      key: 'right',
      className: 'action-col-right',
      style: { 
        padding: '10pt 12pt', display: 'flex', flexDirection: 'column',
        background: '#fafafa', minHeight: NODE_HEIGHT, maxHeight: '320px',
        overflowY: 'auto',
      }
    }, [
      React.createElement('div', { key: 'title', style: { fontFamily: '"IBM Plex Mono", monospace', fontSize: '8pt', letterSpacing: '0.06em', color: '#8a8a8a', marginBottom: '4pt' } }, 'KIẾN THỨC CẦN'),
      React.createElement('ul', { 
        key: 'list', 
        className: 'action-knowledge-list',
        style: { margin: 0, padding: 0, listStyle: 'none', flex: 1 } 
      }, knowledgeItems.length > 0 ? knowledgeItems : React.createElement('li', { 
        key: 'empty', 
        style: { fontSize: '9pt', color: '#8a8a8a', fontStyle: 'italic', paddingLeft: 0 } 
      }, '— Không có —')),
    ]),
  ]);
}

// ============================================================================
// MAIN COMPONENT
// ============================================================================

export default function ActionRoadmapRenderer({ frontendData, onNodeClick }) {
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [layoutReady, setLayoutReady] = useState(false);

  const [nodes, setNodes, onNodesChange] = useNodesState([]);

  // Compute layout when data changes
  useEffect(() => {
    if (!frontendData?.nodes || !frontendData?.edges) return;
    
    const { nodes: baseNodes, edges: baseEdges } = parseJITGraphData(frontendData);
    const { nodes: laidOutNodes, edges: laidOutEdges } = computeVerticalLayout(baseNodes, baseEdges);
    
    setNodes(laidOutNodes);
    setEdges(laidOutEdges);
    setLayoutReady(true);
  }, [frontendData, setNodes, setEdges]);

  // Stats
  const stats = useMemo(() => {
    const phaseCount = {};
    nodes.forEach(n => {
      const p = n.data.phase;
      if (p) phaseCount[p] = (phaseCount[p] || 0) + 1;
    });
    return { 
      nodes: nodes.length, 
      edges: edges.length, 
      phases: phaseCount,
      implements: nodes.filter(n => n.data._isImplement).length,
      verifies: nodes.filter(n => n.data._isVerify).length,
      knowledgeItems: nodes.reduce((sum, n) => sum + (n.data._knowledgeItems?.length || 0), 0),
    };
  }, [nodes, edges]);

  if (!layoutReady) {
    return React.createElement('div', { 
      style: { width: '100%', height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#e9e9e9', fontFamily: '"IBM Plex Sans", sans-serif' }
    }, 'Đang tính layout Action Roadmap...');
  }

  // Calculate total time
  const totalTime = stats.implements * 0.5 + stats.verifies * 0.25; // rough estimate

  return React.createElement('div', { style: { width: '100%', height: '100vh', background: '#e9e9e9', fontFamily: '"IBM Plex Sans", sans-serif' } }, [
    // Toolbar
    React.createElement('div', {
      key: 'toolbar',
      className: 'action-toolbar no-print',
      style: { 
        maxWidth: '210mm', margin: '0 auto', padding: '10px 0', 
        display: 'flex', justifyContent: 'flex-end', gap: '8px',
        zIndex: 100
      }
    }, [
      React.createElement('button', {
        key: 'print',
        onClick: () => window.print(),
        style: { 
          fontFamily: '"IBM Plex Mono", monospace', fontSize: '11px', letterSpacing: '0.04em',
          background: '#fff', border: '1px solid #bbb', padding: '6px 12px',
          cursor: 'pointer', color: '#5c5c5c' 
        }
      }, 'In / Xuất PDF'),
    ]),
    
    // Page (A4)
    React.createElement('div', {
      key: 'page',
      className: 'action-page',
      style: { 
        width: '210mm', minHeight: '297mm', margin: '0 auto 24px', 
        background: '#fff', padding: '18mm 16mm',
        boxShadow: '0 0 0 1px #ccc, 0 6px 18px rgba(0,0,0,.08)',
        fontSize: '10.5pt', lineHeight: 1.5, fontFamily: '"IBM Plex Sans", sans-serif',
        color: '#1a1a1a',
        position: 'relative',
      }
    }, [
      // Document Header
      React.createElement('div', {
        key: 'doc-head',
        className: 'doc-head',
        style: { 
          display: 'flex', justifyContent: 'space-between', alignItems: 'flexEnd',
          borderBottom: '3px solid #0e7c6b', paddingBottom: '8pt', marginBottom: '16pt' 
        }
      }, [
        React.createElement('div', { key: 'left' }, [
          React.createElement('h1', { 
            key: 'title', 
            style: { fontSize: '16pt', fontWeight: 600, letterSpacing: '0.01em', margin: 0 } 
          }, 'Action Roadmap'),
          React.createElement('div', { 
            key: 'sub', 
            style: { fontSize: '9pt', color: '#5c5c5c', marginTop: '3pt' } 
          }, frontendData?.project_brief?.title || 'AI Quiz Generator'),
        ]),
        React.createElement('div', { 
          key: 'total', 
          className: 'total',
          style: { 
            fontFamily: '"IBM Plex Mono", monospace', fontSize: '9pt', 
            color: '#b4530c', fontWeight: 600, textAlign: 'right', whiteSpace: 'nowrap' 
          } 
        }, [
          React.createElement('div', null, `TỔNG ~${formatTime(totalTime)}`),
          React.createElement('div', null, `${stats.implements} BƯỚC · ${stats.verifies} VERIFY`),
        ]),
      ]),
      
      // Phases & Steps
      React.createElement('div', {
        key: 'phases',
        style: { display: 'flex', flexDirection: 'column' }
      }, renderPhases(nodes)),
      
      // Footer
      React.createElement('div', {
        key: 'doc-foot',
        className: 'doc-foot',
        style: { 
          marginTop: '18pt', paddingTop: '8pt', borderTop: '2px solid #1a1a1a',
          display: 'flex', justifyContent: 'space-between',
          fontFamily: '"IBM Plex Mono", monospace', fontSize: '8.5pt', color: '#8a8a8a' 
        }
      }, [
        React.createElement('span', null, 'ACTION ROADMAP · ORCHABLE'),
        React.createElement('span', null, 'TRANG 1/1'),
      ]),
      
      // Legend
      React.createElement('div', {
        key: 'legend',
        className: 'legend',
        style: { marginTop: '10pt', fontSize: '8pt', color: '#8a8a8a' }
      }, [
        React.createElement('span', { key: 'time', style: { color: '#b4530c' } }, '■ thời gian ước tính'),
        React.createElement('span', { key: 'sep1' }, ' · '),
        React.createElement('span', { key: 'review', style: { color: '#4f46e5' } }, '■ đã học ở bước khác / có thể làm song song'),
        React.createElement('span', { key: 'sep2' }, ' · '),
        React.createElement('span', { key: 'assumed', style: { color: '#7a7a85' } }, '■ giả định đã biết'),
        React.createElement('span', { key: 'sep3' }, ' · '),
        React.createElement('span', { key: 'verify', style: { color: '#0f9d63' } }, '■ điểm kiểm chứng'),
        React.createElement('span', { key: 'sep4' }, ' · '),
        React.createElement('span', { key: 'dim', style: { fontWeight: 600 } }, 'Chữ mờ = kiến thức tham khảo, không bắt buộc.'),
      ]),
    ]),
  ]);
}

// ============================================================================
// RENDER PHASES & STEPS
// ============================================================================

function renderPhases(nodes) {
  const phases = {};
  let phaseOrder = [];
  
  nodes.forEach(n => {
    if (n.data._isPhase) {
      if (!phases[n.data.phase]) {
        phases[n.data.phase] = { header: n, steps: [] };
        phaseOrder.push(n.data.phase);
      } else {
        phases[n.data.phase].header = n;
      }
    } else if (n.data._isImplement || n.data._isVerify) {
      const p = n.data.phase;
      if (phases[p]) {
        phases[p].steps.push(n);
      }
    }
  });
  
  return phaseOrder.map((phaseNum, phaseIdx) => {
    const phase = phases[phaseNum];
    if (!phase) return null;
    
    const header = phase.header;
    const steps = phase.steps.sort((a, b) => a.position.y - b.position.y);
    
    // Calculate phase time
    const phaseTime = steps.reduce((sum, s) => {
      const note = s.data.note || '';
      const timeMatch = note.match(/~(\d+)([MH])/);
      if (timeMatch) {
        return sum + (timeMatch[2] === 'H' ? parseInt(timeMatch[1]) * 60 : parseInt(timeMatch[1]));
      }
      return sum + 30; // default 30min
    }, 0);
    
    const pColor = PHASE_COLORS[phaseNum] || '#333';
    
    return React.createElement('div', {
      key: `phase-${phaseNum}`,
      className: 'action-phase',
      style: { marginBottom: '20pt', pageBreakInside: 'avoid' }
    }, [
      // Phase Header
      React.createElement('div', {
        key: 'head',
        className: 'phase-head',
        style: { 
          display: 'flex', alignItems: 'baseline', gap: '10pt',
          borderBottom: '1.5px solid', borderColor: pColor,
          paddingBottom: '4pt', marginBottom: '8pt' 
        }
      }, [
        React.createElement('span', { 
          key: 'num', 
          className: 'num',
          style: { fontFamily: '"IBM Plex Mono", monospace', fontSize: '9pt', color: pColor, fontWeight: 600 } 
        }, String(phaseNum).padStart(2, '0')),
        React.createElement('span', { 
          key: 'name', 
          className: 'name',
          style: { fontFamily: '"IBM Plex Mono", monospace', fontSize: '11pt', fontWeight: 600, letterSpacing: '0.03em' } 
        }, PHASE_NAMES[phaseNum]),
        React.createElement('span', { 
          key: 'meta', 
          className: 'meta',
          style: { marginLeft: 'auto', fontFamily: '"IBM Plex Mono", monospace', fontSize: '8.5pt', color: '#b4530c' } 
        }, `~${formatTime(phaseTime / 60)} · ${steps.length} BƯỚC`),
      ]),
      
      // Steps
      React.createElement('div', {
        key: 'steps',
        style: { borderTop: '1px solid #d8d8d8', borderBottom: '1px solid #d8d8d8' }
      }, steps.map((step, stepIdx) => {
        const isVerify = step.data._isVerify;
        const truncatedLabel = step.data.label;
        const note = step.data.note || '';
        
        if (isVerify) {
          // VERIFY ROW
          return React.createElement('div', {
            key: `verify-${step.id}`,
            className: 'action-verify',
            style: { 
              padding: '8pt 0', borderTop: '1.5px dashed #0f9d63', 
              borderBottom: '1px solid #d8d8d8', background: '#f4faf7',
              fontSize: '9.3pt', breakInside: 'avoid', display: 'flex', alignItems: 'center', justifyContent: 'space-between'
            }
          }, [
            React.createElement('div', { key: 'content', style: { flex: 1 } }, [
              React.createElement('b', { 
                key: 'label',
                style: { fontFamily: '"IBM Plex Mono", monospace', fontSize: '9pt', color: '#0f9d63' } 
              }, `✓ VERIFY — ${truncatedLabel}`),
              note && React.createElement('div', { 
                key: 'desc', 
                style: { marginTop: '2pt', fontSize: '9.3pt', color: '#1a1a1a' } 
              }, note),
            ]),
            React.createElement('span', { 
              key: 'time', 
              className: 'time',
              style: { fontFamily: '"IBM Plex Mono", monospace', fontSize: '8.5pt', color: '#b4530c' } 
            }, note.match(/~(\d+)([MH])/) ? note.match(/~(\d+)([MH])/)[0] : '~15M'),
          ]);
        }
        
        // IMPLEMENT STEP
        const knowledgeItems = step.data._knowledgeItems || [];
        const truncatedKnowledge = knowledgeItems.map((k, i) => ({
          ...k,
          index: i,
        }));
        
        return React.createElement('div', {
          key: `step-${step.id}`,
          className: 'action-step',
          style: { 
            display: 'grid', gridTemplateColumns: '56% 44%', gap: '0 14pt',
            padding: '9pt 0', borderBottom: stepIdx === steps.length - 1 ? 'none' : '1px solid #d8d8d8',
            breakInside: 'avoid', pageBreakInside: 'avoid',
            alignItems: 'start'
          }
        }, [
          // LEFT: IMPLEMENTATION
          React.createElement('div', { key: 'left' }, [
            React.createElement('div', { 
              key: 'header', className: 'step-name',
              style: { display: 'flex', alignItems: 'baseline', gap: '6pt', marginBottom: '4pt' }
            }, [
              React.createElement('span', { 
                key: 'idx', className: 'idx',
                style: { fontFamily: '"IBM Plex Mono", monospace', fontSize: '9pt', color: '#8a8a8a' } 
              }, `▶`),
              React.createElement('span', { 
                key: 'fn', className: 'fn',
                style: { fontFamily: '"IBM Plex Mono", monospace', fontSize: '10pt', fontWeight: 600, color: '#1a1a1a' } 
              }, truncatedLabel),
            ]),
            React.createElement('div', { 
              key: 'desc', className: 'step-desc',
              style: { fontSize: '9.5pt', color: '#5c5c5c', lineHeight: 1.5, fontFamily: '"IBM Plex Sans", sans-serif' } 
            }, note),
            note.match(/có thể viết song song|song song/) && React.createElement('div', {
              key: 'parallel',
              className: 'step-note',
              style: { fontSize: '8.5pt', fontStyle: 'italic', color: '#4f46e5', marginTop: '4pt' }
            }, note.match(/có thể viết song song.*/)[0]),
          ]),
          
          // RIGHT: KNOWLEDGE
          React.createElement('div', { key: 'right' }, [
            React.createElement('div', { 
              key: 'label', className: 'know-label',
              style: { fontFamily: '"IBM Plex Mono", monospace', fontSize: '8pt', letterSpacing: '0.06em', color: '#8a8a8a', marginBottom: '4pt' } 
            }, 'KIẾN THỨC CẦN'),
            React.createElement('ul', { 
              key: 'list', className: 'know-list',
              style: { listStyle: 'none', margin: 0, padding: 0 } 
            }, truncatedKnowledge.length > 0 ? truncatedKnowledge.map((k, i) => 
              React.createElement(KnowledgeItem, { 
                key: k.knowledgeNode.id, 
                item: { ...k, state: k.state, tier: k.tier, firstCardId: k.firstCardId, knowledgeNode: k.knowledgeNode },
                index: i 
              })
            ) : React.createElement('li', { 
              key: 'empty', 
              style: { fontSize: '9.3pt', color: '#8a8a8a', fontStyle: 'italic', paddingLeft: 0 } 
            }, '— Không có —')),
          ]),
        ]);
      })),
    ]);
  });
}

