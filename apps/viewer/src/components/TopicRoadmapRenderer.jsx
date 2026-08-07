import React, { useEffect, useMemo, useState } from 'react';
import './TopicRoadmapRenderer.css';

// ============================================================================
// CONSTANTS
// ============================================================================

const PHASE_NAMES = {
  0: 'NỀN TẢNG', 1: 'MVP', 2: 'MỞ RỘNG', 3: 'HOÀN THIỆN',
};

const BLOOM_COLORS = {
  remember: '#6b6b76',
  understand: '#2b78e4',
  apply: '#0e7c6b',
  analyze: '#8e44ad',
  evaluate: '#b4530c',
  create: '#dc3545',
};

const STORAGE_KEY = 'orchable-topic-roadmap-progress';

// ============================================================================
// DATA TRANSFORM: roadmap.json (pipeline v3) → per-card concept data
// ============================================================================

function transformToCardData(roadmap) {
  if (!roadmap?.phases) return { phases: [], cards: [] };

  const cards = [];
  roadmap.phases.forEach(phase => {
    const pid = phase.phase_id;
    (phase.milestones || []).forEach(milestone => {
      const los = milestone.learning_objectives || [];
      const ulos = los.filter(lo => lo.lo_type === 'UNIVERSAL');
      const cios = los.filter(lo => lo.lo_type === 'CONCEPTUAL_IMPL');
      const sios = los.filter(lo => lo.lo_type === 'SPECIFIC_IMPL');

      // Knowledge items: SIO labels (tech-specific) — mỗi SIO 1 item
      const knowledge = sios.map(sio => ({
        label: sio.name || sio.code || 'SIO',
        code: sio.code,
        bloom: sio.bloom_level || 'apply',
        // SIO per-card (theo implementation)
        sio: {
          code: sio.code,
          name: sio.name,
          description: sio.description,
          bloom: sio.bloom_level || 'apply',
        },
        // ULO liên kết (global theo concept-set)
        ulo: ulos.length > 0 ? {
          code: ulos[0].code,
          name: ulos[0].name,
          description: ulos[0].description,
          bloom: ulos[0].bloom_level || 'remember',
        } : null,
        // CIO liên kết
        cio: cios.length > 0 ? {
          code: cios[0].code,
          name: cios[0].name,
          description: cios[0].description,
          bloom: cios[0].bloom_level || 'understand',
        } : null,
      }));

      cards.push({
        id: milestone.concept_code || `card-${cards.length}`,
        conceptCode: milestone.concept_code,
        phaseId: pid,
        // Cột trái: mô tả implementation (Cách 1 hoặc Cách 2)
        description: describeImplementation(milestone, los),
        knowledge: knowledge,
        loCount: los.length,
      });
    });
  });

  return {
    phases: roadmap.phases.map(p => ({
      id: p.phase_id,
      name: p.title || PHASE_NAMES[p.phase_id] || `Phase ${p.phase_id}`,
      cardIds: p.milestones.map(m => m.concept_code || ''),
    })),
    cards,
  };
}

// Cột trái: mô tả tính chất dự án đến implementation hiện tại
function describeImplementation(milestone, los) {
  const concept = milestone.concept_code || 'UNSPECIFIED';
  const conceptName = concept.toLowerCase().replace(/_/g, ' ');

  // Cách 1: "Triển khai chức năng X với Y"
  const sioNames = los.filter(lo => lo.lo_type === 'SPECIFIC_IMPL').map(lo => lo.name || '');
  const techHint = sioNames[0] ? ` với ${sioNames[0].replace(/^SWIFT:\s*/i, 'Swift — ')}` : '';

  // Mô tả chính từ milestone (nếu có)
  const uloDesc = los.find(lo => lo.lo_type === 'UNIVERSAL')?.description || '';
  const desc = uloDesc.replace(/^Người học có khả năng\s*/i, 'App có thể ').replace(/\.$/, '');

  return {
    approach1: `Triển khai chức năng ${conceptName}${techHint}`,
    approach2: desc ? `App có thể ${desc}.` : `App triển khai ${conceptName}.`,
  };
}

// ============================================================================
// KNOWLEDGE ITEM (cột phải) — bloom badge + hover ULO/CIO/SIO
// ============================================================================

function KnowledgeItem({ item, index }) {
  const [hover, setHover] = useState(false);
  const bloomColor = BLOOM_COLORS[item.bloom] || '#333';
  const showReview = item.ulo && item.ulo.bloom === 'remember' && index > 0;

  return React.createElement('li', {
    className: 'tkr-knowledge-item',
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: { position: 'relative', padding: '4px 0', fontSize: '13px', cursor: 'default' },
  }, [
    React.createElement('span', {
      key: 'label',
      style: { fontWeight: 500, color: '#18181b' },
    }, item.label),

    // Bloom badge
    React.createElement('span', {
      key: 'bloom',
      className: 'tkr-bloom-badge',
      style: {
        marginLeft: '8px', fontSize: '9px', fontWeight: 600, textTransform: 'uppercase',
        color: bloomColor, background: `${bloomColor}15`, padding: '1px 6px', borderRadius: '10px',
      },
    }, item.bloom),

    // Hover: ULO/CIO/SIO (chỉ ULO dùng ở card này — JIT)
    hover && item.ulo && React.createElement('div', {
      key: 'hover',
      className: 'tkr-hover-popup',
      style: {
        position: 'absolute', left: '100%', top: 0, zIndex: 100,
        background: '#fff', border: '1px solid #e6e6e6', borderRadius: '8px',
        padding: '10px 12px', width: '320px', boxShadow: '0 4px 16px rgba(0,0,0,0.12)',
        fontSize: '12px', lineHeight: 1.5,
      },
    }, [
      React.createElement('div', { key: 'title', style: { fontWeight: 600, color: '#18181b', marginBottom: '6px' } },
        `ⓘ ${item.label} [${item.bloom}]`),
      item.ulo && React.createElement('div', { key: 'ulo', style: { marginBottom: '4px' } }, [
        React.createElement('span', { style: { color: '#2b78e4', fontWeight: 600, marginRight: '6px' } }, 'ULO:'),
        React.createElement('span', null, item.ulo.name || item.ulo.code),
        item.ulo.description && React.createElement('div', { key: 'ulod', style: { color: '#5c5c66', fontSize: '11px', marginTop: '2px' } }, item.ulo.description),
      ]),
      item.cio && React.createElement('div', { key: 'cio', style: { marginBottom: '4px' } }, [
        React.createElement('span', { style: { color: '#8e44ad', fontWeight: 600, marginRight: '6px' } }, 'CIO:'),
        React.createElement('span', null, item.cio.name || item.cio.code),
        item.cio.description && React.createElement('div', { key: 'ciod', style: { color: '#5c5c66', fontSize: '11px', marginTop: '2px' } }, item.cio.description),
      ]),
      item.sio && React.createElement('div', { key: 'sio' }, [
        React.createElement('span', { style: { color: '#0e7c6b', fontWeight: 600, marginRight: '6px' } }, 'SIO:'),
        React.createElement('span', null, item.sio.name || item.sio.code),
        item.sio.description && React.createElement('div', { key: 'siod', style: { color: '#5c5c66', fontSize: '11px', marginTop: '2px' } }, item.sio.description),
      ]),
    ]),
  ]);
}

// ============================================================================
// CARD (2 cột: Implementation | Knowledge sử dụng)
// ============================================================================

function TopicCard({ card, approach, onToggleApproach, done, onToggle }) {
  const [showApproach2, setShowApproach2] = useState(approach === 'approach2');

  return React.createElement('div', {
    className: 'tkr-card',
    style: {
      background: '#fff', border: '1px solid #e6e6e6', borderRadius: '12px',
      marginBottom: '12px', overflow: 'hidden',
      opacity: done ? 0.55 : 1,
    },
  }, [
    React.createElement('div', {
      style: { display: 'grid', gridTemplateColumns: '1.1fr 1fr', minHeight: '80px' },
    }, [
      // CỘT TRÁI: IMPLEMENTATION
      React.createElement('div', {
        key: 'left',
        style: { padding: '14px 16px', borderRight: '1px solid #e6e6e6' },
      }, [
        React.createElement('div', { style: { display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '6px' } }, [
          React.createElement('div', {
            onClick: () => onToggle(card.id),
            style: {
              width: '16px', height: '16px', borderRadius: '4px', cursor: 'pointer',
              border: `1.5px solid ${done ? '#0e7c6b' : '#d4d4d4'}`,
              background: done ? '#0e7c6b' : 'transparent',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
            },
          }, done && React.createElement('span', { style: { color: '#fff', fontSize: '10px' } }, '✓')),
          React.createElement('span', {
            style: { fontFamily: '"IBM Plex Mono", monospace', fontWeight: 600, fontSize: '12.5px', color: '#18181b' },
          }, card.conceptCode),
          React.createElement('span', {
            style: { marginLeft: 'auto', fontSize: '10px', color: '#9a9aa5', fontFamily: 'monospace' },
          }, `${card.loCount} mục tiêu`),
        ]),
        // Mô tả: Cách 1 (mặc định) hoặc Cách 2
        React.createElement('div', {
          style: { fontSize: '12.5px', color: '#5c5c66', lineHeight: 1.55 },
        }, showApproach2 ? card.description.approach2 : card.description.approach1),
        // Toggle Cách 1 / Cách 2
        React.createElement('div', { style: { marginTop: '8px', display: 'flex', gap: '6px' } }, [
          ['approach1', 'Triển khai gì', 'approach2', 'App có thể'].map((label, idx) => {
            const val = idx === 0 ? 'approach1' : 'approach2';
            return React.createElement('button', {
              key: val,
              onClick: () => setShowApproach2(val === 'approach2'),
              style: {
                fontSize: '10px', padding: '2px 8px', borderRadius: '12px', cursor: 'pointer',
                border: `1px solid ${showApproach2 === (val === 'approach2') ? '#0e7c6b' : '#e6e6e6'}`,
                background: showApproach2 === (val === 'approach2') ? '#e9f6f3' : '#fff',
                color: showApproach2 === (val === 'approach2') ? '#0e7c6b' : '#9a9aa5',
              },
            }, label);
          }),
        ]),
      ]),

      // CỘT PHẢI: KIẾN THỨC SỬ DỤNG
      React.createElement('div', {
        key: 'right',
        style: { padding: '14px 16px', background: '#fafafa' },
      }, [
        React.createElement('div', {
          style: {
            fontFamily: '"IBM Plex Mono", monospace', fontSize: '10px', letterSpacing: '0.05em',
            color: '#9a9aa5', marginBottom: '8px',
          },
        }, '📚 KIẾN THỨC SỬ DỤNG'),
        card.knowledge.length > 0 ? React.createElement('ul', {
          style: { listStyle: 'none', margin: 0, padding: 0 },
        }, card.knowledge.map((k, i) =>
          React.createElement(KnowledgeItem, { key: `${card.id}-${i}`, item: k, index: i })
        )) : React.createElement('div', { style: { fontSize: '12px', color: '#9a9aa5', fontStyle: 'italic' } },
          'Không có SIO riêng cho concept này'),
      ]),
    ]),
  ]);
}

// ============================================================================
// MAIN COMPONENT
// ============================================================================

export default function TopicRoadmapRenderer({ frontendData }) {
  const { phases, cards } = useMemo(() => transformToCardData(frontendData), [frontendData]);
  const [doneCards, setDoneCards] = useState(new Set());
  const [approach, setApproach] = useState('approach1');

  useEffect(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) setDoneCards(new Set(JSON.parse(saved)));
    } catch (e) {}
  }, []);

  useEffect(() => {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify([...doneCards])); } catch (e) {}
  }, [doneCards]);

  const totalCards = cards.length;
  const doneCount = doneCards.size;
  const pct = totalCards > 0 ? Math.round((doneCount / totalCards) * 100) : 0;

  const toggleCard = (id) => {
    setDoneCards(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id); else next.add(id);
      return next;
    });
  };

  return React.createElement('div', {
    className: 'tkr-root',
    style: { background: '#fafafa', minHeight: '100%', fontFamily: '"IBM Plex Sans", sans-serif' },
  }, [
    // Header + progress
    React.createElement('div', {
      style: {
        background: '#fff', borderBottom: '1px solid #e6e6e6', padding: '16px 24px',
        display: 'flex', alignItems: 'center', gap: '20px', flexWrap: 'wrap',
      },
    }, [
      React.createElement('h1', { style: { fontSize: '20px', fontWeight: 700, margin: 0, color: '#18181b' } },
        '📘 Topic Roadmap'),
      React.createElement('span', { style: { fontSize: '12px', color: '#9a9aa5' } },
        frontendData?.project_brief?.goal ? frontendData.project_brief.goal.slice(0, 70) + '...' : ''),
      React.createElement('div', {
        style: {
          marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '10px',
          fontFamily: 'monospace', fontSize: '11px', color: '#5c5c66',
        },
      }, [
        React.createElement('div', {
          style: { width: '160px', height: '6px', background: '#e6e6e6', borderRadius: '3px', overflow: 'hidden' },
        }, React.createElement('div', {
          style: { height: '100%', width: `${pct}%`, background: '#0e7c6b', transition: 'width .35s' },
        })),
        React.createElement('span', null, `${doneCount}/${totalCards} · ${pct}%`),
      ]),
    ]),

    // Phases
    React.createElement('div', { style: { padding: '24px', maxWidth: '1100px', margin: '0 auto' } },
      phases.map(phase => {
        const phaseCards = cards.filter(c => c.phaseId === phase.id);
        if (phaseCards.length === 0) return null;
        return React.createElement('section', {
          key: phase.id,
          style: { marginBottom: '36px' },
        }, [
          React.createElement('div', {
            style: {
              display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px',
              borderBottom: '1.5px solid #0e7c6b', paddingBottom: '8px',
            },
          }, [
            React.createElement('span', {
              style: {
                fontFamily: 'monospace', fontSize: '11px', fontWeight: 600, color: '#0e7c6b',
                background: '#e9f6f3', padding: '3px 10px', borderRadius: '20px',
              },
            }, `PHASE ${String(phase.id).padStart(2, '0')}`),
            React.createElement('h2', { style: { fontSize: '17px', fontWeight: 700, margin: 0, color: '#18181b' } },
              phase.name),
            React.createElement('span', { style: { marginLeft: 'auto', fontSize: '11px', color: '#9a9aa5', fontFamily: 'monospace' } },
              `${phaseCards.length} khái niệm`),
          ]),
          phaseCards.map(card =>
            React.createElement(TopicCard, {
              key: card.id,
              card,
              approach,
              onToggleApproach: setApproach,
              done: doneCards.has(card.id),
              onToggle: toggleCard,
            })
          ),
        ]);
      }),
    ),
  ]);
}
