import React, { useEffect, useState, useMemo, useCallback, useRef } from 'react';
import './ActionRoadmapWeb.css';

// ============================================================================
// CONSTANTS & DESIGN TOKENS
// ============================================================================

const PHASE_COLORS = {
  0: 'var(--assumed)', 1: 'var(--accent)', 2: 'var(--review)', 3: '#8e44ad',
};

const PHASE_NAMES = {
  0: 'NỀN TẢNG', 1: 'MVP', 2: 'MỞ RỘNG', 3: 'HOÀN THIỆN',
};

const STORAGE_KEY = 'orchable-roadmap-progress';

// ============================================================================
// UTILITIES
// ============================================================================

function formatTime(hours) {
  if (hours < 1) return Math.round(hours * 60) + 'M';
  const h = Math.floor(hours);
  const m = Math.round((hours - h) * 60);
  return m > 0 ? h + 'H ' + m + 'M' : h + 'H';
}

function extractTimeFromNote(note) {
  // Time estimate comes from the generator (data), not hardcoded here.
  // Format: "~30M" or "~1H 30M" embedded in note by generate_jit_graph.py
  if (!note) return '';
  const match = note.match(/~(\d+[HM](?: \d+M)?)/);
  return match ? match[1] : '';
}

// ============================================================================
// DATA TRANSFORM
// ============================================================================

function transformToWebData(frontendData) {
  if (!frontendData?.nodes || !frontendData?.edges) return { phases: [], steps: [] };
  
  const edgeMap = new Map();
  frontendData.edges.forEach(function(e) {
    if (!edgeMap.has(e.source)) edgeMap.set(e.source, []);
    edgeMap.get(e.source).push(e.target);
  });
  
  const startNode = frontendData.nodes.find(function(n) { return n.data.nodeType === 'start'; });
  const flowOrder = [];
  const visited = new Set();
  
  function traverse(nodeId) {
    if (visited.has(nodeId)) return;
    visited.add(nodeId);
    const node = frontendData.nodes.find(function(n) { return n.id === nodeId; });
    if (node) flowOrder.push(node);
    const next = edgeMap.get(nodeId) || [];
    next.forEach(traverse);
  }
  
  if (startNode) traverse(startNode.id);
  frontendData.nodes.forEach(function(n) { if (!visited.has(n.id)) flowOrder.push(n); });
  
  const knowledgeRegistry = new Map();
  const implementKnowledgeMap = new Map();
  
  flowOrder.forEach(function(n) {
    if (n.data.nodeType === 'knowledge') {
      const idx = flowOrder.findIndex(function(f) { return f.id === n.id; });
      for (var i = idx + 1; i < flowOrder.length; i++) {
        if (['implement', 'verify'].includes(flowOrder[i].data.nodeType)) {
          var implId = flowOrder[i].id;
          if (!implementKnowledgeMap.has(implId)) implementKnowledgeMap.set(implId, []);
          
          var label = (n.data.label || '').trim().toLowerCase();
          // Bloom level từ data (generator sinh theo phase)
          var bloom = n.data.bloom_level || 'understand';
          // Dedup key = (label, bloom_level) — cùng label khác mức = kiến thức MỚI
          var dedupKey = label + '::' + bloom;
          var isFirstOccurrence = !knowledgeRegistry.has(dedupKey);
          var state = 'NEW';
          
          if (isFirstOccurrence) {
            state = 'NEW';
            knowledgeRegistry.set(dedupKey, { firstCardId: implId, count: 1 });
          } else {
            state = 'REVIEW';
            var reg = knowledgeRegistry.get(dedupKey);
            reg.count++;
          }
          
          var coreKeywords = ['dataclass', 'json', 'http', 'api', 'async', 'class', 'function', 'type hint', 'enum', 'path', 'file', 'list', 'dict'];
          var optionalKeywords = ['retry', 'timeout', 'schema', 'validation', 'logging', 'monitoring', 'advanced'];
          var tier = 'CORE';
          if (optionalKeywords.some(function(k) { return label.includes(k); })) tier = 'OPTIONAL';
          else if (!coreKeywords.some(function(k) { return label.includes(k); })) tier = 'SUPPORT';
          
          implementKnowledgeMap.get(implId).push({ 
            id: n.id,
            label: n.data.label || '',
            note: n.data.note || '',
            state: state, 
            tier: tier,
            bloom: bloom,
            firstCardId: knowledgeRegistry.get(dedupKey)?.firstCardId 
          });
          break;
        }
      }
    }
  });
  
  var displayNodes = flowOrder.filter(function(n) { 
    return ['implement', 'verify', 'phase', 'start', 'end'].includes(n.data.nodeType);
  });
  
  var phases = {};
  var phaseOrder = [];
  
  displayNodes.forEach(function(node) {
    if (node.data.nodeType === 'phase') {
      var p = node.data.phase;
      if (!phases[p]) {
        phases[p] = { 
          id: 'p' + p, 
          name: PHASE_NAMES[p], 
          num: String(p).padStart(2, '0'),
          steps: [], 
          headerNode: node 
        };
        phaseOrder.push(p);
      } else {
        phases[p].headerNode = node;
      }
    } else if (['implement', 'verify'].includes(node.data.nodeType)) {
      var p = node.data.phase;
      if (phases[p]) {
        phases[p].steps.push(node);
      }
    }
  });
  
  var flowIndex = {};
  flowOrder.forEach(function(n, i) { flowIndex[n.id] = i; });
  
  Object.values(phases).forEach(function(phase) {
    phase.steps.sort(function(a, b) { return (flowIndex[a.id] || 0) - (flowIndex[b.id] || 0); });
  });
  
  var webSteps = [];
  Object.values(phases).forEach(function(phase) {
    phase.steps.forEach(function(step) {
      var knowledge = implementKnowledgeMap.get(step.id) || [];
      var webStep = {
        id: step.id,
        phaseId: phase.id,
        phaseNum: phase.num,
        type: step.data.nodeType,
        label: step.data.label || '',
        note: step.data.note || '',
        featureId: step.data.feature_id,
        featureName: step.data.feature_name,
        time: extractTimeFromNote(step.data.note),
        knowledge: knowledge.map(function(k, idx) {
          return {
            id: k.id,
            label: k.label,
            note: k.note,
            state: k.state,
            tier: k.tier,
            bloom: k.bloom,
            firstCardId: k.firstCardId,
            index: idx,
          };
        }),
      };
      webSteps.push(webStep);
    });
  });
  
  return { 
    phases: Object.values(phases).map(function(p) { 
      return { 
        id: p.id, 
        name: p.name, 
        num: p.num, 
        stepIds: p.steps.map(function(s) { return s.id; }) 
      }; 
    }), 
    steps: webSteps 
  };
}

// ============================================================================
// KNOWLEDGE ITEM COMPONENT
// ============================================================================

function KnowledgeItem(_ref) {
  var item = _ref.item;
  var onJump = _ref.onJump;
  var label = item.label;
  var state = item.state;
  var tier = item.tier;
  var bloom = item.bloom;
  var firstCardId = item.firstCardId;
  var isOptional = tier === 'OPTIONAL';
  var isReview = state === 'REVIEW';
  var isAssumed = state === 'ASSUMED';
  
  var stateColors = {
    NEW: { dot: 'var(--ink)' },
    REVIEW: { dot: 'var(--review)' },
    ASSUMED: { dot: 'var(--assumed)' },
  };
  
  return React.createElement('li', {
    className: 'know-item' + (isOptional ? ' optional' : ''),
    key: item.id,
    style: { display: 'flex', alignItems: 'flexStart', gap: '8px', fontSize: '13px', marginBottom: '8px' }
  }, [
    React.createElement('span', {
      key: 'dot',
      className: 'dot' + (isOptional ? ' optional' : ''),
      style: { 
        flex: 'none', width: '6px', height: '6px', borderRadius: '50%', marginTop: '6px',
        background: isOptional ? 'transparent' : (stateColors[state]?.dot || 'var(--ink)'),
        border: isOptional ? '1px solid var(--ink-faint)' : 'none',
      }
    }),
    React.createElement('span', {
      key: 'txt',
      className: 'txt',
      style: { flex: 1, lineHeight: 1.45 }
    }, label),
    isReview && firstCardId && React.createElement('span', {
      key: 'review',
      className: 'tag review',
      onClick: function() { return onJump(firstCardId); },
      style: { 
        flex: 'none', fontFamily: '"IBM Plex Mono", monospace', fontSize: '9.5px',
        color: 'var(--review)', background: 'var(--review-bg)', padding: '1px 7px', borderRadius: '20px',
        cursor: 'pointer', marginTop: '1px', textDecoration: 'none'
      }
    }, 'đã học · ' + firstCardId.slice(0, 8)),
    isAssumed && React.createElement('span', {
      key: 'assumed',
      className: 'tag assumed',
      style: { 
        flex: 'none', fontFamily: '"IBM Plex Mono", monospace', fontSize: '9.5px',
        color: 'var(--assumed)', background: 'var(--border)', padding: '1px 7px', borderRadius: '20px',
        marginTop: '1px'
      }
    }, 'giả định biết'),
    tier === 'OPTIONAL' && React.createElement('span', {
      key: 'tier',
      className: 'tag optional',
      style: { 
        flex: 'none', fontFamily: '"IBM Plex Mono", monospace', fontSize: '9.5px',
        color: 'var(--ink-faint)', background: 'var(--border)', padding: '1px 7px', borderRadius: '20px',
        marginTop: '1px'
      }
    }, 'OPTIONAL'),
    bloom && React.createElement('span', {
      key: 'bloom',
      className: 'tag bloom',
      style: { 
        flex: 'none', fontFamily: '"IBM Plex Mono", monospace', fontSize: '9.5px',
        color: 'var(--accent)', background: 'var(--accent-bg)', padding: '1px 7px', borderRadius: '20px',
        marginTop: '1px', textTransform: 'uppercase'
      }
    }, bloom),
  ]);
}

// ============================================================================
// STEP CARD COMPONENT
// ============================================================================

function StepCard(_ref) {
  var step = _ref.step;
  var done = _ref.done;
  var onToggle = _ref.onToggle;
  var onJump = _ref.onJump;
  
  var id = step.id;
  var type = step.type;
  var label = step.label;
  var note = step.note;
  var time = step.time;
  var knowledge = step.knowledge;
  var featureName = step.featureName;
  var isVerify = type === 'verify';
  
  if (isVerify) {
    return React.createElement('div', {
      className: 'verify',
      key: id,
      style: { 
        background: 'var(--verify-bg)', border: '1px dashed var(--verify)', borderRadius: '14px',
        padding: '14px 20px', display: 'flex', alignItems: 'baseline', gap: '12px',
        marginBottom: '12px'
      }
    }, [
      React.createElement('span', {
        key: 'mark',
        className: 'verify-mark',
        style: { fontFamily: '"IBM Plex Mono", monospace', color: 'var(--verify)', fontWeight: 700, fontSize: '13px', flex: 'none' }
      }, '✓'),
      React.createElement('div', {
        key: 'body',
        className: 'verify-body',
        style: { flex: 1, fontSize: '13px', color: 'var(--ink-dim)' }
      }, [
        React.createElement('b', {
          key: 'label',
          style: { fontFamily: '"IBM Plex Mono", monospace', fontSize: '12px', color: 'var(--verify)' }
        }, 'VERIFY — ' + label),
        note && React.createElement('div', { key: 'desc', style: { marginTop: '4px', color: 'var(--ink)' } }, note),
      ]),
      time && React.createElement('span', {
        key: 'time',
        className: 'verify-time',
        style: { fontFamily: '"IBM Plex Mono", monospace', fontSize: '10.5px', color: 'var(--time)', flex: 'none' }
      }, time),
    ]);
  }
  
  var knowledgeItems = knowledge.map(function(k, i) { 
    return React.createElement(KnowledgeItem, { key: k.id + '-' + i, item: k, onJump: onJump });
  });
  
  var isParallel = note && (note.includes('song song') || note.includes('parallel'));
  
  // Build knowledge column content
  var knowledgeColumn;
  if (knowledge.length > 0) {
    knowledgeColumn = React.createElement('ul', {
      key: 'list',
      className: 'know-list',
      style: { listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '8px', margin: 0, padding: 0 }
    }, knowledgeItems);
  } else {
    knowledgeColumn = React.createElement('p', {
      key: 'empty',
      className: 'know-empty',
      style: { fontSize: '12.5px', color: 'var(--ink-faint)', fontStyle: 'italic' }
    }, 'Không có — chỉ ghép lại các bước ở trên.');
  }
  
  return React.createElement('div', {
    className: 'step' + (done ? ' done' : ''),
    'data-id': id,
    key: id,
    style: { 
      background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '14px',
      marginBottom: '12px', overflow: 'hidden',
      transition: 'box-shadow .2s ease, border-color .2s ease',
      opacity: done ? 0.55 : 1
    }
  }, [
    React.createElement('div', {
      className: 'step-grid',
      style: { display: 'grid', gridTemplateColumns: '1.25fr 1fr' }
    }, [
      // LEFT: IMPLEMENTATION
      React.createElement('div', {
        key: 'left',
        className: 'impl',
        style: { padding: '18px 20px', borderRight: '1px solid var(--border)' }
      }, [
        React.createElement('div', {
          key: 'top',
          className: 'impl-top',
          style: { display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }
        }, [
          React.createElement('div', {
            key: 'check',
            className: 'check' + (done ? ' on' : ''),
            onClick: function() { return onToggle(id); },
            style: { 
              width: '17px', height: '17px', borderRadius: '5px', 
              border: '1.5px solid ' + (done ? 'var(--accent)' : 'var(--border-strong)'), flex: 'none', cursor: 'pointer',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              background: done ? 'var(--accent)' : 'transparent',
              transition: 'background .15s ease, border-color .15s ease'
            }
          }, done && React.createElement('span', { key: 'checkmark', style: { color: 'var(--surface)', fontSize: '11px' } }, '✓')),
          React.createElement('span', {
            key: 'fn',
            className: 'impl-fn',
            style: { fontFamily: '"IBM Plex Mono", monospace', fontSize: '13.5px', fontWeight: 600, color: 'var(--ink)' }
          }, '▶ ' + label),
          featureName && React.createElement('span', {
            key: 'feature',
            className: 'tag feature',
            style: { 
              flex: 'none', fontFamily: '"IBM Plex Mono", monospace', fontSize: '9.5px',
              color: 'var(--review)', background: 'var(--review-bg)', padding: '1px 7px', borderRadius: '20px',
              marginTop: '1px'
            }
          }, featureName),
          time && React.createElement('span', {
            key: 'time',
            className: 'impl-time',
            style: { marginLeft: 'auto', fontFamily: '"IBM Plex Mono", monospace', fontSize: '10.5px', color: 'var(--time)' }
          }, time),
        ]),
        React.createElement('div', {
          key: 'desc',
          className: 'impl-desc',
          style: { fontSize: '13.5px', color: 'var(--ink-dim)', lineHeight: 1.6 }
        }, note),
        note && note.includes('song song') && React.createElement('div', {
          key: 'parallel',
          className: 'impl-note',
          style: { 
            display: 'inline-flex', alignItems: 'center', gap: '5px', marginTop: '10px',
            fontSize: '11.5px', color: 'var(--review)', background: 'var(--review-bg)',
            padding: '3px 8px', borderRadius: '20px'
          }
        }, [React.createElement('span', { key: 'icon' }, '⇄'), note.match(/có thể làm song song.*|parallel.*/)[0]]),
      ]),
      
      // RIGHT: KNOWLEDGE
      React.createElement('div', {
        key: 'right',
        className: 'know',
        style: { padding: '18px 20px' }
      }, [
        React.createElement('div', {
          key: 'head',
          className: 'know-head',
          style: { 
            display: 'flex', alignItems: 'center', gap: '6px',
            fontFamily: '"IBM Plex Mono", monospace', fontSize: '10.5px',
            letterSpacing: '0.05em', color: 'var(--ink-faint)', marginBottom: '10px'
          }
        }, '📚 KIẾN THỨC CẦN'),
        knowledgeColumn,
      ]),
    ]),
  ]);
}

// ============================================================================
// PHASE SECTION COMPONENT
// ============================================================================

function PhaseSection(_ref) {
  var phase = _ref.phase;
  var steps = _ref.steps;
  var doneSteps = _ref.doneSteps;
  var onToggle = _ref.onToggle;
  var onJump = _ref.onJump;
  
  var phaseTime = steps.reduce(function(sum, s) {
    var timeMatch = s.time ? s.time.match(/(\d+)([MH])/) : null;
    if (timeMatch) {
      return sum + (timeMatch[2] === 'H' ? parseInt(timeMatch[1]) * 60 : parseInt(timeMatch[1]));
    }
    return sum;
  }, 0);
  
  var phaseColor = PHASE_COLORS[parseInt(phase.num)] || 'var(--accent)';
  var doneInPhase = steps.filter(function(s) { return doneSteps.has(s.id); }).length;
  
  return React.createElement('section', {
    className: 'phase-section',
    id: phase.id,
    key: phase.id,
    style: { marginBottom: '44px', scrollMarginTop: '24px' }
  }, [
    React.createElement('div', {
      key: 'head',
      className: 'phase-head',
      style: { display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }
    }, [
      React.createElement('span', {
        key: 'badge',
        className: 'phase-badge',
        style: { 
          fontFamily: '"IBM Plex Mono", monospace', fontSize: '11px', fontWeight: 600,
          color: phaseColor, background: 'var(--accent-bg)', padding: '3px 9px', borderRadius: '20px'
        }
      }, 'PHASE ' + phase.num),
      React.createElement('h2', {
        key: 'name',
        style: { fontSize: '17px', fontWeight: 700, letterSpacing: '-0.005em', margin: 0 }
      }, phase.name),
      phaseTime > 0 && React.createElement('span', {
        key: 'time',
        className: 'phase-time',
        style: { 
          marginLeft: 'auto', fontFamily: '"IBM Plex Mono", monospace', fontSize: '11.5px',
          color: 'var(--time)', background: 'var(--time-bg)', padding: '3px 9px', borderRadius: '20px'
        }
      }, '~' + formatTime(phaseTime / 60) + ' · ' + steps.length + ' bước'),
    ]),
    
    steps.map(function(step) {
      return React.createElement(StepCard, {
        key: step.id,
        step: step,
        done: doneSteps.has(step.id),
        onToggle: function(id) { return onToggle(id); },
        onJump: function(targetId) {
          var targetEl = document.querySelector('[data-id="' + targetId + '"]');
          if (targetEl) {
            targetEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
            targetEl.classList.add('flash');
            setTimeout(function() { return targetEl.classList.remove('flash'); }, 1300);
          }
        }
      });
    }),
  ]);
}

// ============================================================================
// SIDEBAR COMPONENT
// ============================================================================

function Sidebar(_ref) {
  var phases = _ref.phases;
  var doneSteps = _ref.doneSteps;
  var onNavigate = _ref.onNavigate;
  
  var totalAllSteps = phases.reduce(function(sum, p) { return sum + p.stepIds.length; }, 0);
  var totalSteps = doneSteps.size;
  var pct = totalAllSteps > 0 ? Math.round((totalSteps / totalAllSteps) * 100) : 0;
  
  var phaseStats = {};
  phases.forEach(function(p) {
    var done = p.stepIds.filter(function(id) { return doneSteps.has(id); }).length;
    phaseStats[p.id] = { done: done, total: p.stepIds.length, pct: Math.round((done / p.stepIds.length) * 100) };
  });
  
  return React.createElement('aside', {
    className: 'sidebar',
    style: { 
      width: '252px', flex: 'none', position: 'sticky', top: 0, height: '100%',
      overflowY: 'auto', borderRight: '1px solid var(--border)', background: 'var(--surface)',
      padding: '24px 18px 24px'
    }
  }, [
    React.createElement('div', { key: 'title', className: 'sidebar-title', style: { fontSize: '15px', fontWeight: 700, marginBottom: '2px' } }, 'AI Quiz Generator'),
    React.createElement('div', { key: 'sub', className: 'sidebar-sub', style: { fontSize: '12px', color: 'var(--ink-faint)', marginBottom: '18px' } }, 'Action Roadmap · Orchable'),
    
    React.createElement('div', { key: 'progress', className: 'progress-wrap', style: { marginBottom: '22px' } }, [
      React.createElement('div', { key: 'top', className: 'progress-top', style: { display: 'flex', justifyContent: 'space-between', fontFamily: '"IBM Plex Mono", monospace', fontSize: '11px', color: 'var(--ink-dim)', marginBottom: '6px' } }, [
        React.createElement('span', { key: 'label', id: 'pctLabel' }, pct + '% hoàn thành'),
        React.createElement('span', { key: 'count', id: 'doneCount' }, totalSteps + '/' + totalAllSteps),
      ]),
      React.createElement('div', { key: 'bar', className: 'progress-bar', style: { height: '6px', background: 'var(--border)', borderRadius: '4px', overflow: 'hidden' } }, [
        React.createElement('div', { key: 'fill', className: 'progress-fill', id: 'progressFill', style: { height: '100%', width: pct + '%', background: 'var(--accent)', transition: 'width .35s ease' } }),
      ]),
    ]),
    
    React.createElement('ul', { key: 'nav', className: 'nav-list', style: { listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '2px' } }, 
      phases.map(function(p) {
        var stat = phaseStats[p.id] || { done: 0, total: p.stepIds.length, pct: 0 };
        return React.createElement('li', { key: p.id }, 
          React.createElement('a', {
            className: 'nav-item' + (stat.pct === 100 ? ' active' : ''),
            href: '#' + p.id,
            'data-target': p.id,
            onClick: function(e) {
              e.preventDefault();
              var el = document.getElementById(p.id);
              if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
            },
            style: { 
              display: 'block', padding: '9px 10px', borderRadius: '7px', textDecoration: 'none',
              fontSize: '13px', color: 'var(--ink-dim)', borderLeft: '2px solid transparent', cursor: 'pointer',
              transition: 'background .15s ease, color .15s ease',
              background: stat.pct === 100 ? 'var(--accent-bg)' : 'transparent',
              color: stat.pct === 100 ? 'var(--accent)' : 'var(--ink-dim)',
              borderLeftColor: stat.pct === 100 ? 'var(--accent)' : 'transparent',
              fontWeight: stat.pct === 100 ? 600 : 400,
            }
          }, [
            React.createElement('span', { key: 'num', className: 'n', style: { fontFamily: '"IBM Plex Mono", monospace', fontSize: '10.5px', color: stat.pct === 100 ? 'var(--accent)' : 'var(--ink-faint)', marginRight: '6px' } }, p.num),
            p.name,
            React.createElement('span', { key: 'pct', className: 'pct', id: 'pct-' + p.id, style: { float: 'right', fontFamily: '"IBM Plex Mono", monospace', fontSize: '10.5px', color: 'var(--ink-faint)' } }, stat.pct + '%'),
          ])
        );
      })
    ),
    
    React.createElement('div', { key: 'foot', className: 'sidebar-foot', style: { marginTop: '26px', paddingTop: '14px', borderTop: '1px solid var(--border)', fontSize: '11px', color: 'var(--ink-faint)', lineHeight: 1.7 } }, [
      React.createElement('div', { key: 'l1', className: 'row', style: { display: 'flex', alignItems: 'center', gap: '7px', marginBottom: '4px' } }, [
        React.createElement('span', { key: 'dot', className: 'dotc', style: { width: '7px', height: '7px', borderRadius: '50%', flex: 'none', background: 'var(--time)' } }),
        'Thời gian ước tính'
      ]),
      React.createElement('div', { key: 'l2', className: 'row', style: { display: 'flex', alignItems: 'center', gap: '7px', marginBottom: '4px' } }, [
        React.createElement('span', { key: 'dot', className: 'dotc', style: { width: '7px', height: '7px', borderRadius: '50%', flex: 'none', background: 'var(--review)' } }),
        'Đã học / làm song song'
      ]),
      React.createElement('div', { key: 'l3', className: 'row', style: { display: 'flex', alignItems: 'center', gap: '7px', marginBottom: '4px' } }, [
        React.createElement('span', { key: 'dot', className: 'dotc', style: { width: '7px', height: '7px', borderRadius: '50%', flex: 'none', background: 'var(--assumed)' } }),
        'Giả định đã biết'
      ]),
      React.createElement('div', { key: 'l4', className: 'row', style: { display: 'flex', alignItems: 'center', gap: '7px', marginBottom: '4px' } }, [
        React.createElement('span', { key: 'dot', className: 'dotc', style: { width: '7px', height: '7px', borderRadius: '50%', flex: 'none', background: 'var(--verify)' } }),
        'Điểm kiểm chứng'
      ]),
    ]),
  ]);
}

// ============================================================================
// MAIN COMPONENT
// ============================================================================

export default function ActionRoadmapWeb(_ref) {
  var frontendData = _ref.frontendData;
  
  var _useState = React.useState(new Set());
  var doneSteps = _useState[0];
  var setDoneSteps = _useState[1];
  
  var _useState2 = React.useState([]);
  var doneStepsArray = _useState2[0];
  var setDoneStepsArray = _useState2[1];
  
  var _useMemo = React.useMemo(function() { return transformToWebData(frontendData); }, [frontendData]);
  var phases = _useMemo.phases;
  var steps = _useMemo.steps;
  
  var observerRef = React.useRef(null);
  
  React.useEffect(function() {
    try {
      var saved = localStorage.getItem('orchable-roadmap-progress');
      if (saved) {
        var parsed = JSON.parse(saved);
        if (Array.isArray(parsed)) {
          setDoneSteps(new Set(parsed));
          setDoneStepsArray(parsed);
        }
      }
    } catch (e) {}
  }, []);
  
  React.useEffect(function() {
    try {
      localStorage.setItem('orchable-roadmap-progress', JSON.stringify(doneStepsArray));
    } catch (e) {}
  }, [doneStepsArray]);
  
  React.useEffect(function() {
    var sections = document.querySelectorAll('.phase-section');
    var navItems = document.querySelectorAll('.nav-item');
    
    observerRef.current = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          navItems.forEach(function(n) {
            n.classList.toggle('active', n.dataset.target === entry.target.id);
          });
        }
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    
    sections.forEach(function(s) { return observerRef.current.observe(s); });
    return function() { return observerRef.current?.disconnect(); };
  }, [phases]);
  
  var toggleStep = React.useCallback(function(id) {
    setDoneSteps(function(prev) {
      var next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
    setDoneStepsArray(function(prev) {
      var next = prev.slice();
      var idx = next.indexOf(id);
      if (idx >= 0) next.splice(idx, 1);
      else next.push(id);
      return next;
    });
  }, []);
  
  var totalSteps = steps.length;
  var doneCount = doneSteps.size;
  var pct = totalSteps > 0 ? Math.round((doneCount / totalSteps) * 100) : 0;
  
  var phaseStats = React.useMemo(function() {
    var stats = {};
    phases.forEach(function(p) {
      var done = p.stepIds.filter(function(id) { return doneSteps.has(id); }).length;
      stats[p.id] = { done: done, total: p.stepIds.length, pct: Math.round((done / p.stepIds.length) * 100) };
    });
    return stats;
  }, [phases, doneSteps]);
  
  return React.createElement('div', { className: 'app action-roadmap-scope', style: { display: 'flex', minHeight: '100%', height: '100%' } }, [
    React.createElement(Sidebar, {
      key: 'sidebar',
      phases: phases,
      doneSteps: doneSteps,
      onNavigate: function() {},
    }),
    
    React.createElement('main', {
      key: 'main',
      className: 'main',
      style: { 
        flex: 1, minWidth: 0, 
        padding: '40px clamp(20px, 5vw, 64px) 100px',
        maxWidth: '920px'
      }
    }, [
      React.createElement('div', {
        key: 'hero',
        className: 'hero',
        style: { marginBottom: '36px' }
      }, [
        React.createElement('h1', { 
          key: 'h1', 
          style: { fontSize: 'clamp(22px, 3vw, 30px)', fontWeight: 700, letterSpacing: '-0.01em', marginBottom: '8px' } 
        }, 'Action Roadmap'),
        React.createElement('p', { 
          key: 'desc', 
          style: { fontSize: '14px', color: 'var(--ink-dim)', maxWidth: '60ch' } 
        }, 'Lộ trình dựng từ source code thật — mỗi bước implement đi kèm đúng kiến thức tối thiểu cần để làm bước đó. Tick vào từng bước khi hoàn thành, tiến độ được lưu lại trên trình duyệt này.'),
      ]),
      
      phases.map(function(phase) {
        return React.createElement(PhaseSection, {
          key: phase.id,
          phase: phase,
          steps: steps.filter(function(s) { return phase.stepIds.includes(s.id); }),
          doneSteps: doneSteps,
          onToggle: function(id) { 
            setDoneSteps(function(prev) { 
              var n = new Set(prev); 
              n.has(id) ? n.delete(id) : n.add(id); 
              return n; 
            }); 
          },
          onJump: function() {},
        });
      }),
    ]),
  ]);
}
