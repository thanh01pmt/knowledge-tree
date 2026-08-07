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

      // Knowledge items: mỗi ULO = 1 item (concept có NHIỀU ULO)
      // Mỗi item mang ULO + CIO (global) + SIO (per-card, nếu có)
      const knowledge = [];

      // Nếu có SIO: mỗi SIO gắn với ULO/CIO liên quan (hoặc ULO đầu tiên)
      if (sios.length > 0) {
        const seenKws = new Set();
        sios.forEach((sio, i) => {
          const ulo = ulos[Math.min(i, ulos.length - 1)] || null;
          const cio = cios[Math.min(i, cios.length - 1)] || null;
          const kw = (sio.keyword || '').trim();
          // Bỏ SIO trùng keyword (VD 3× "for-in") — chỉ hiện 1, hover vẫn đủ
          if (kw && seenKws.has(kw)) return;
          if (kw) seenKws.add(kw);
          // Hiển thị keyword thực hành (VD "Keyword @State") thay vì tên SIO máy
          const sioLabel = kw ? `Keyword ${kw}` : cleanLabel(sio.name || sio.code || 'SIO');
          knowledge.push({
            id: `${milestone.concept_code}-sio-${i}`,
            label: sioLabel,
            bloom: sio.bloom_level || 'apply',
            ulo: ulo ? {
              code: ulo.code, name: cleanLabel(ulo.name), description: ulo.description,
              bloom: ulo.bloom_level || 'remember',
            } : null,
            cio: cio ? {
              code: cio.code, name: cleanLabel(cio.name), description: cio.description,
              bloom: cio.bloom_level || 'understand',
            } : null,
            sio: {
              code: sio.code, name: cleanLabel(sio.name), description: sio.description,
              bloom: sio.bloom_level || 'apply',
            },
            keyword: kw,
          });
        });
      } else if (ulos.length > 0) {
        // Không có SIO: vẫn hiện ULO/CIO (kiến thức sử dụng)
        ulos.forEach((ulo, i) => {
          const cio = cios[Math.min(i, cios.length - 1)] || null;
          knowledge.push({
            id: `${milestone.concept_code}-ulo-${i}`,
            label: cleanLabel(ulo.name || ulo.code),
            bloom: ulo.bloom_level || 'remember',
            ulo: {
              code: ulo.code, name: cleanLabel(ulo.name), description: ulo.description,
              bloom: ulo.bloom_level || 'remember',
            },
            cio: cio ? {
              code: cio.code, name: cleanLabel(cio.name), description: cio.description,
              bloom: cio.bloom_level || 'understand',
            } : null,
            sio: null,
          });
        });
      } else if (cios.length > 0) {
        // Phase 2 (MỞ RỘNG): chỉ có CIOs — hiện CIO làm knowledge item
        cios.forEach((cio, i) => {
          knowledge.push({
            id: `${milestone.concept_code}-cio-${i}`,
            label: cleanLabel(cio.name || cio.code),
            bloom: cio.bloom_level || 'understand',
            ulo: null,
            cio: {
              code: cio.code, name: cleanLabel(cio.name), description: cio.description,
              bloom: cio.bloom_level || 'understand',
            },
            sio: null,
          });
        });
      }

      cards.push({
        id: milestone.concept_code || `card-${cards.length}`,
        conceptCode: milestone.concept_code,
        phaseId: pid,
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

function cleanLabel(label) {
  if (!label) return '';
  // "Understand CORE_LIBRARIES" → "Hiểu CORE_LIBRARIES"
  let s = String(label);
  s = s.replace(/^Understand\s+/i, 'Hiểu ');
  s = s.replace(/^Apply\s+/i, 'Áp dụng ');
  s = s.replace(/^SWIFT:\s*/i, 'Swift — ');
  s = s.replace(/^PYTHON:\s*/i, 'Python — ');
  return s.trim();
}

// Cột trái: mô tả tính chất dự án đến implementation hiện tại
function describeImplementation(milestone, los) {
  const concept = milestone.concept_code || 'UNSPECIFIED';
  const conceptName = concept.toLowerCase().replace(/_/g, ' ');

  // Ưu tiên theo thứ tự mô tả thật: ULO → CIO → SIO name
  // Phase 1 (ULO): "App có thể hiểu X" từ ULO description
  const uloDesc = los.find(lo => lo.lo_type === 'UNIVERSAL')?.description || '';
  if (uloDesc) {
    return uloDesc.replace(/^Người học có khả năng\s*/i, 'App có thể ').replace(/\.$/, '') + '.';
  }

  // Phase 2 (CIO): mô tả thiết kế/phân tích từ CIO description
  const cioDesc = los.find(lo => lo.lo_type === 'CONCEPTUAL_IMPL')?.description || '';
  if (cioDesc) {
    return cioDesc.replace(/^Người học có khả năng\s*/i, 'App có thể ').replace(/\.$/, '') + '.';
  }

  // Phase 3 (SIO): "App triển khai X với Swift"
  const sioNames = los.filter(lo => lo.lo_type === 'SPECIFIC_IMPL').map(lo => lo.name || '');
  if (sioNames.length > 0) {
    return `App triển khai ${sioNames[0].replace(/^SWIFT:\s*/i, 'Swift — ')}.`;
  }
  return `App triển khai ${conceptName}.`;
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
    style: { position: 'relative', display: 'flex', alignItems: 'flex-start', gap: '8px', fontSize: '13px', marginBottom: '8px', cursor: 'default' },
  }, [
    // Dot (giống ActionRoadmapWeb cũ)
    React.createElement('span', {
      key: 'dot',
      className: 'dot',
      style: {
        flex: 'none', width: '6px', height: '6px', borderRadius: '50%', marginTop: '6px',
        background: '#18181b',
      },
    }),
    // Text label (flex chiếm phần còn lại)
    React.createElement('span', {
      key: 'txt',
      className: 'txt',
      style: { flex: 1, lineHeight: 1.45, color: '#18181b', fontWeight: 500 },
    }, item.label),
    // Bloom tag bên phải (giống ActionRoadmapWeb cũ, màu theo BLOOM_COLORS)
    React.createElement('span', {
      key: 'bloom',
      className: 'tag bloom',
      style: {
        flex: 'none', fontFamily: '"IBM Plex Mono", monospace', fontSize: '9.5px',
        color: bloomColor, background: `${bloomColor}15`, padding: '1px 7px', borderRadius: '20px',
        marginTop: '1px', textTransform: 'uppercase',
      },
    }, item.bloom),

    // Hover: CHỈ hiện objective TƯƠNG ỨNG theo bloom của keyword
    // remember → ULO | understand → CIO | apply/create → SIO
    hover && (() => {
      // Chọn objective theo bloom
      let obj = null;
      let objLabel = '';
      if (item.bloom === 'remember' && item.ulo) {
        obj = item.ulo; objLabel = 'ULO';
      } else if ((item.bloom === 'understand' || item.bloom === 'analyze') && item.cio) {
        obj = item.cio; objLabel = 'CIO';
      } else if (item.sio) {
        obj = item.sio; objLabel = 'SIO';
      } else if (item.cio) {
        obj = item.cio; objLabel = 'CIO';
      } else if (item.ulo) {
        obj = item.ulo; objLabel = 'ULO';
      }
      if (!obj) return null;
      return React.createElement('div', {
        key: 'hover',
        className: 'tkr-hover-popup',
        style: {
          position: 'absolute', left: '100%', top: 0, zIndex: 9999,
          background: '#fff', border: '1px solid #e6e6e6', borderRadius: '8px',
          padding: '10px 12px', width: '300px', boxShadow: '0 4px 16px rgba(0,0,0,0.12)',
          fontSize: '12px', lineHeight: 1.5,
        },
      }, [
        React.createElement('div', { key: 'title', style: { fontWeight: 600, color: '#18181b', marginBottom: '4px' } },
          `ⓘ ${item.label}`),
        React.createElement('div', { key: 'obj', style: { color: '#0e7c6b', fontWeight: 600, marginBottom: '4px' } },
          `${objLabel} · ${obj.bloom || ''}`),
        React.createElement('div', { key: 'name', style: { color: '#18181b', fontWeight: 500, marginBottom: '2px' } },
          obj.name || obj.code),
        obj.description && React.createElement('div', { key: 'desc', style: { color: '#5c5c66', fontSize: '11px', marginTop: '2px' } },
          obj.description),
      ]);
    })(),
  ]);
}

// ============================================================================
// CARD (2 cột: Implementation | Knowledge sử dụng)
// ============================================================================

function TopicCard({ card, approach, onToggleApproach, done, onToggle }) {

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
        // Mô tả: "App có thể..." (hướng đã chọn)
        React.createElement('div', {
          style: { fontSize: '12.5px', color: '#5c5c66', lineHeight: 1.55 },
        }, card.description),
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
        }, '📚 KIẾN THỨC CẦN'),
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
