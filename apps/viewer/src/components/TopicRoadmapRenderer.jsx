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
      // v3: milestone = TASK đã có đủ LO riêng (ULO/CIO/SIO) — KHÔNG gom toàn cục
      // theo concept (trước đây gom mọi task dạy cùng concept → keyword của task
      // khác hiển thị nhầm, "3 mục tiêu" nhưng 7 items). Dùng LO của task này thôi.
      const los = milestone.learning_objectives || [];
      const ulos = los.filter(lo => lo.lo_type === 'UNIVERSAL');
      const cios = los.filter(lo => lo.lo_type === 'CONCEPTUAL_IMPL');
      const sios = los.filter(lo => lo.lo_type === 'SPECIFIC_IMPL');
      const primaryConcept = los[0]?.concept || los[0]?.concept_code || milestone.concept_code;
      const allLois = los;  // task-local — không gom concept toàn cục
      const allUlos = ulos;
      const allCios = cios;
      const allSios = sios;

      // Knowledge items theo thiết kế:
      // - ULO/CIO cùng concept → GOM thành 1 item "Concept <Tên>" (không tách tầng)
      // - SIO → mỗi item "Keyword <kw>" (thực hành cụ thể)
      // Hover trên item → hiện đủ các LO liên quan (ULO + CIO, hoặc SIO)
      const knowledge = [];
      const conceptLabel = humanizeCode(primaryConcept);
      const cardKey = primaryConcept || milestone.concept_code || `card-${cards.length}`;

      // Gom ULO + CIO của concept thành 1 item "Concept XYZ" (của task này)
      const conceptLois = [...allUlos, ...allCios];
      if (conceptLois.length > 0) {
        // Bloom tag đa cấp: gom các bloom khác nhau (VD understand·apply)
        const blooms = [...new Set(conceptLois.map(lo => (lo.bloom_level || '').toLowerCase()).filter(Boolean))];
        const allBlooms = blooms.length > 0 ? blooms.join(' · ') : 'understand';
        knowledge.push({
          id: `${cardKey}-concept`,
          label: `Concept ${conceptLabel}`,
          bloom: allBlooms,  // có thể nhiều cấp: "understand · apply"
          conceptCode: primaryConcept,
          conceptLabel,
          lois: conceptLois.map(lo => ({
            code: lo.code, name: cleanLabel(lo.name), description: lo.description,
            lo_type: lo.lo_type, bloom: lo.bloom_level || '',
          })),
          ulo: ulos[0] ? {
            code: ulos[0].code, name: cleanLabel(ulos[0].name), description: ulos[0].description,
            bloom: ulos[0].bloom_level || 'remember',
          } : null,
          cio: cios[0] ? {
            code: cios[0].code, name: cleanLabel(cios[0].name), description: cios[0].description,
            bloom: cios[0].bloom_level || 'understand',
          } : null,
          sio: null,
          keyword: '',
        });
      }

      // SIO → mỗi item "Keyword X" (từ MỌI phase, dedup keyword trùng)
      if (allSios.length > 0) {
        const seenKws = new Set();
        allSios.forEach((sio, i) => {
          const kw = (sio.keyword || '').trim();
          if (kw && seenKws.has(kw)) return;
          if (kw) seenKws.add(kw);
          // Badge platform: phân biệt implement cho Swift app vs ESP32 firmware
          const platform = sio.platform || '';
          const platformBadge = platform === 'esp32' ? ' [ESP32]' : '';
          const sioLabel = kw ? `Keyword ${kw}${platformBadge}` : cleanLabel(sio.name || sio.code || 'SIO');
          knowledge.push({
            id: `${cardKey}-sio-${i}`,
            label: sioLabel,
            bloom: sio.bloom_level || 'apply',
            ulo: null,
            cio: null,
            sio: {
              code: sio.code, name: cleanLabel(sio.name), description: sio.description,
              bloom: sio.bloom_level || 'apply',
            },
            keyword: kw,
            platform,
          });
        });
      }

      // Card key = milestone.id (task id — DUY NHẤT, không phải concept: nhiều
      // task có thể dạy cùng concept VD API_INTEGRATION ở 8 task → key trùng)
      cards.push({
        id: milestone.id || cardKey,
        conceptCode: primaryConcept,
        name: milestone.name || '',
        phaseId: pid,
        loCount: los.length,
        knowledge,
        description: describeImplementation(milestone, los),
      });
    });
  });

  return {
    phases: roadmap.phases.map(p => ({
      id: p.phase_id,
      name: p.title || PHASE_NAMES[p.phase_id] || `Phase ${p.phase_id}`,
      cardIds: p.milestones.map(m => m.id || m.concept_code || ''),
    })),
    cards,
  };
}

function humanizeCode(code) {
  // "LOCAL_VIEW_STATE" → "Local View State" | "CORE_LIBRARIES" → "Core Libraries"
  // (chỉ capitalize khi code là UPPER_SNAKE; giữ nguyên tên có sẵn như "SwiftUI")
  if (!code) return '';
  if (code === 'FOR_LOOP') return 'Definite Iteration';  // lặp với số lần xác định
  const s = String(code);
  if (s === s.toUpperCase()) {
    return s.toLowerCase().replace(/(^|_)(\w)/g, (m, sep, ch) => (sep ? ' ' : '') + ch.toUpperCase());
  }
  return s.replace(/_/g, ' ');
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
  const taskName = milestone.name || milestone.concept_code || 'UNSPECIFIED';
  const concept = milestone.concept_code || '';

  // Ưu tiên theo thứ tự mô tả thật: ULO → CIO → SIO name
  // Phase 1 (ULO): "Người học có khả năng hiểu X" từ ULO description
  // (KHÔNG đổi "App có thể" — người học thực hiện task, không phải App)
  const uloDesc = los.find(lo => lo.lo_type === 'UNIVERSAL')?.description || '';
  if (uloDesc) {
    return uloDesc.replace(/\.$/, '') + '.';
  }

  // Phase 2 (CIO): mô tả thiết kế/phân tích từ CIO description
  const cioDesc = los.find(lo => lo.lo_type === 'CONCEPTUAL_IMPL')?.description || '';
  if (cioDesc) {
    return cioDesc.replace(/\.$/, '') + '.';
  }

  // Phase 3 (SIO): "Người học triển khai X với Swift"
  const sioNames = los.filter(lo => lo.lo_type === 'SPECIFIC_IMPL').map(lo => lo.name || '');
  if (sioNames.length > 0) {
    return `Người học triển khai ${sioNames[0].replace(/^SWIFT:\s*/i, 'Swift — ')}.`;
  }
  return `Người học triển khai ${taskName}.`;
}

// ============================================================================
// KNOWLEDGE ITEM (cột phải) — bloom badge + hover ULO/CIO/SIO
// ============================================================================

function KnowledgeItem({ item, index }) {
  const [hover, setHover] = useState(false);
  const [pos, setPos] = useState(null); // {x, y} cho popup fixed — không bị cắt bởi overflow ancestor
  const bloomColor = BLOOM_COLORS[item.bloom] || '#333';
  const showReview = item.ulo && item.ulo.bloom === 'remember' && index > 0;

  const onEnter = (e) => {
    setHover(true);
    // Tính vị trí fixed từ item rect — tránh popup tràn ra ngoài scroll container
    const r = e.currentTarget.getBoundingClientRect();
    const popupW = 320;
    const popupH = Math.round(window.innerHeight * 0.7);  // = maxHeight 70vh
    let x = r.right + 8;
    if (x + popupW > window.innerWidth - 8) x = Math.max(8, r.left - popupW - 8);
    // Clamp dọc: popup (tối đa 70vh) không tràn dưới đáy viewport
    let y = r.top;
    if (y + popupH > window.innerHeight - 8) y = Math.max(8, window.innerHeight - popupH - 8);
    setPos({ x, y });
  };

  return React.createElement('li', {
    className: 'tkr-knowledge-item',
    onMouseEnter: onEnter,
    onMouseLeave: () => { setHover(false); setPos(null); },
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

    // Hover: hiện ĐỦ các LO liên quan đến item — POPUP FIXED (không bị cắt)
    // - "Concept X" → danh sách ULO + CIO (mỗi cái kèm bloom + desc)
    // - "Keyword X" → SIO tương ứng
    hover && pos && (() => {
      if (item.lois && item.lois.length > 0) {
        // CONCEPT ITEM: hiện tất cả ULO + CIO
        const lois = item.lois;
        const tierLabel = lo => lo.lo_type === 'UNIVERSAL' ? 'ULO' : 'CIO';
        return React.createElement('div', {
          key: 'hover',
          className: 'tkr-hover-popup',
          style: {
            position: 'fixed', left: pos.x, top: pos.y, zIndex: 99999,
            background: '#fff', border: '1px solid #e6e6e6', borderRadius: '8px',
            padding: '10px 12px', width: '320px', maxHeight: '70vh', overflowY: 'auto',
            boxShadow: '0 4px 16px rgba(0,0,0,0.12)', fontSize: '12px', lineHeight: 1.5,
          },
        }, [
          React.createElement('div', { key: 'title', style: { fontWeight: 600, color: '#18181b', marginBottom: '6px' } },
            `ⓘ ${item.label}`),
          ...lois.map((lo, i) => React.createElement('div', {
            key: `lo-${i}`,
            style: { marginBottom: '8px', paddingBottom: '6px', borderBottom: i < lois.length - 1 ? '1px solid #f0f0f0' : 'none' },
          }, [
            React.createElement('div', { key: 'tag', style: { color: '#0e7c6b', fontWeight: 600, fontSize: '11px', marginBottom: '2px' } },
              `${tierLabel(lo)} · ${lo.bloom || ''}`),
            React.createElement('div', { key: 'name', style: { color: '#18181b', fontWeight: 500, fontSize: '11.5px', marginBottom: '2px' } },
              lo.name || lo.code),
            lo.description && React.createElement('div', { key: 'desc', style: { color: '#5c5c66', fontSize: '10.5px' } },
              lo.description),
          ])),
        ]);
      }
      // SIO ITEM ("Keyword X")
      if (item.sio) {
        const sio = item.sio;
        return React.createElement('div', {
          key: 'hover',
          className: 'tkr-hover-popup',
          style: {
            position: 'fixed', left: pos.x, top: pos.y, zIndex: 99999,
            background: '#fff', border: '1px solid #e6e6e6', borderRadius: '8px',
            padding: '10px 12px', width: '300px', maxHeight: '70vh', overflowY: 'auto',
            boxShadow: '0 4px 16px rgba(0,0,0,0.12)', fontSize: '12px', lineHeight: 1.5,
          },
        }, [
          React.createElement('div', { key: 'title', style: { fontWeight: 600, color: '#18181b', marginBottom: '4px' } },
            `ⓘ ${item.label}`),
          React.createElement('div', { key: 'obj', style: { color: '#0e7c6b', fontWeight: 600, marginBottom: '4px' } },
            `SIO · ${sio.bloom || ''}`),
          React.createElement('div', { key: 'name', style: { color: '#18181b', fontWeight: 500, marginBottom: '2px' } },
            sio.name || sio.code),
          sio.description && React.createElement('div', { key: 'desc', style: { color: '#5c5c66', fontSize: '11px', marginTop: '2px' } },
            sio.description),
        ]);
      }
      return null;
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
      marginBottom: '12px',
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
          }, card.name || card.conceptCode),
          React.createElement('span', {
            style: { marginLeft: 'auto', fontSize: '10px', color: '#9a9aa5', fontFamily: 'monospace' },
          }, card.conceptCode ? `📚 ${card.conceptCode} · ${card.loCount} mục tiêu` : `${card.loCount} mục tiêu`),
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
