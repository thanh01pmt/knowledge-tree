import React, { useState, useEffect, useCallback } from 'react';
import { parseFrontendData } from './roadmapLayoutEngine';
import RoadmapShRendererV2 from './RoadmapShRendererV2';
import ActionRoadmapWeb from './ActionRoadmapWeb';
import TopicRoadmapRenderer from './TopicRoadmapRenderer';
import './RoadmapViewer.css';

// Action roadmaps (từ generate_jit_graph.py — implement-centric)
const ACTION_ROADMAPS = ['jit-bulb', 'jit-quiz'];
// Topic roadmaps (từ pipeline v3 — concept → ULO/CIO/SIO)
const TOPIC_ROADMAPS = ['jit-bulb-v3', 'talky-swiftui'];
// Roadmap.sh layout roadmaps
const ROADMAP_SH_ROADMAPS = ['rust-cli', 'portfolio-js'];
// Tự động gom tất cả roadmap từ public/roadmaps/
const knownRoadmaps = [
  ...ACTION_ROADMAPS.map(name => ({ path: `/roadmaps/${name}.json`, code: name.toUpperCase(), type: 'action' })),
  ...TOPIC_ROADMAPS.map(name => ({ path: `/roadmaps/${name}.json`, code: name.toUpperCase(), type: 'topic' })),
  ...ROADMAP_SH_ROADMAPS.map(name => ({ path: `/roadmaps/${name}.json`, code: name.toUpperCase(), type: 'roadmap-sh' })),
];

export default function RoadmapViewer() {
  const [roadmaps, setRoadmaps] = useState([]);
  const [selectedRoadmap, setSelectedRoadmap] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('renderer'); // 'renderer' | 'raw' | 'frontend'
  const [stagesOpen, setStagesOpen] = useState(false); // banner lộ trình phát triển — mặc định thu gọn

  const loadPublicRoadmaps = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const loaded = [];
      for (const rm of knownRoadmaps) {
        try {
          const resp = await fetch(rm.path);
          if (resp.ok) {
            const data = await resp.json();
            loaded.push({ ...data, _source: rm.code, _type: rm.type });
            const key = `roadmap_${data.project_brief?.project_code || rm.code}`;
            localStorage.setItem(key, JSON.stringify(data));
          }
        } catch (e) {
          console.warn(`Failed to load ${rm.path}:`, e);
        }
      }
      if (loaded.length > 0) {
        setRoadmaps(loaded);
        // Ưu tiên roadmap từ URL param ?roadmap=<source> (deep-link),
        // fallback roadmap đầu tiên
        const paramRoadmap = new URLSearchParams(window.location.search).get('roadmap');
        const initial = paramRoadmap
          ? loaded.find(m => m._source.toLowerCase() === paramRoadmap.toLowerCase())
          : null;
        setSelectedRoadmap(initial || loaded[0]);
      }
      setIsLoading(false);
    } catch (err) {
      setError(err.message);
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadPublicRoadmaps();
  }, [loadPublicRoadmaps]);

  const handleNodeClick = useCallback((_, node) => {
    console.log('Node clicked:', node.id, node.data);
  }, []);

  if (isLoading) {
    return (
      <div className="roadmap-viewer loading">
        <div className="loading-spinner">Đang tải roadmaps...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="roadmap-viewer error">
        <h2>Lỗi tải roadmap</h2>
        <pre>{error}</pre>
        <button onClick={loadPublicRoadmaps}>Thử lại</button>
      </div>
    );
  }

  if (!selectedRoadmap) {
    return (
      <div className="roadmap-viewer empty">
        <p>Không có roadmap nào</p>
      </div>
    );
  }

  const roadmapType = selectedRoadmap._type || 'action';
  const isTopic = roadmapType === 'topic';

  return (
    <div className="roadmap-viewer">
      <header className="viewer-header">
        <div className="header-left">
          <h2>{selectedRoadmap.project_brief?.title || 'Untitled Roadmap'}</h2>
          <span className={`badge ${roadmapType !== 'roadmap-sh' ? 'jit' : 'roadmap-sh'}`}>
            {roadmapType === 'topic' ? '📘 Topic Roadmap' : roadmapType === 'action' ? '🎯 Action Roadmap' : '🗺️ roadmap.sh Layout'}
          </span>
          <span className="project-code">{selectedRoadmap.project_brief?.project_code}</span>
        </div>
        <div className="header-right">
          <div className="roadmap-selector">
            <select 
              value={selectedRoadmap._source || ''} 
              onChange={(e) => {
                const rm = roadmaps.find(r => r._source === e.target.value);
                if (rm) setSelectedRoadmap(rm);
              }}
            >
              {roadmaps.map(rm => (
                <option key={rm._source} value={rm._source}>
                  {rm.project_brief?.title || rm._source} ({rm._source}) {rm._type === 'topic' ? '📘' : rm._type === 'action' ? '🎯' : '🗺️'}
                </option>
              ))}
            </select>
          </div>
          <div className="tab-selector">
            <button 
              className={activeTab === 'renderer' ? 'active' : ''}
              onClick={() => setActiveTab('renderer')}
            >
              {roadmapType !== 'roadmap-sh' ? 'Graph View' : 'Layout'}
            </button>
            <button 
              className={activeTab === 'frontend' ? 'active' : ''}
              onClick={() => setActiveTab('frontend')}
            >
              Frontend.json
            </button>
            <button 
              className={activeTab === 'raw' ? 'active' : ''}
              onClick={() => setActiveTab('raw')}
            >
              Raw Data
            </button>
          </div>
        </div>
      </header>

      <main className="viewer-main">
        {activeTab === 'renderer' ? (
          <div className="renderer-container" style={{ height: 'calc(100vh - 80px)', position: 'relative' }}>
            {selectedRoadmap.development_stages?.length > 0 && (
              <div className="dev-stages-banner" style={{
                position: 'absolute', top: 0, left: 0, right: 0, zIndex: 100,
                background: '#f0f7f4', borderBottom: '1px solid #d5e8e0',
                fontSize: '12.5px', color: '#3d5a50', boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
              }}>
                {/* Header — click để toggle (mặc định THU GỌN — không chiếm chỗ roadmap) */}
                <div onClick={() => setStagesOpen(!stagesOpen)}
                     style={{ padding: '8px 20px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{ fontWeight: 700, fontSize: '13px', color: '#0e7c6b' }}>
                    🗺️ Lộ trình phát triển ({selectedRoadmap.development_stages.length} giai đoạn)
                  </span>
                  <span style={{ fontSize: '11px', color: '#4a6b5f' }}>{stagesOpen ? '▲ thu gọn' : '▼ xem chi tiết'}</span>
                </div>
                {stagesOpen && (
                  <div style={{ maxHeight: '50vh', overflowY: 'auto', padding: '0 20px 12px' }}>
                    {selectedRoadmap.development_stages.map((s, i) => (
                      <div key={i} style={{ marginBottom: '10px', paddingLeft: '12px', borderLeft: '2px solid #a8d5c5' }}>
                        <div style={{ fontWeight: 600 }}>{s.stage}</div>
                        <div style={{ color: '#4a6b5f' }}>{s.product_state}</div>
                        {s.cross_feature_value && (
                          <div style={{ color: '#0e7c6b', fontSize: '11.5px', marginTop: '2px' }}>
                            ➕ {s.cross_feature_value}
                          </div>
                        )}
                        {s.temporary_approach && (
                          <div style={{ color: '#9a6b2f', fontSize: '11.5px', marginTop: '2px' }}>
                            🔧 {s.temporary_approach}
                          </div>
                        )}
                        {s.learn?.length > 0 && (
                          <div style={{ color: '#5c5c66', fontSize: '11.5px', marginTop: '2px' }}>
                            📚 Học: {s.learn.join(', ')}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
            {isTopic ? (
              <TopicRoadmapRenderer 
                frontendData={selectedRoadmap}
              />
            ) : roadmapType === 'action' ? (
              <ActionRoadmapWeb 
                frontendData={selectedRoadmap}
              />
            ) : (
              <RoadmapShRendererV2 
                frontendData={selectedRoadmap} 
                useAlgorithmic={true}
              />
            )}
          </div>
        ) : activeTab === 'frontend' ? (
          <div className="frontend-json">
            <h3>Frontend Data (parsed for roadmap.sh)</h3>
            <pre>{JSON.stringify(parseFrontendData(selectedRoadmap), null, 2)}</pre>
          </div>
        ) : (
          <div className="raw-data">
            <h3>Raw JSON Data</h3>
            <pre>{JSON.stringify(selectedRoadmap, null, 2)}</pre>
          </div>
        )}
      </main>
    </div>
  );
}
