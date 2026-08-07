import React, { useState, useEffect, useCallback } from 'react';
import { parseFrontendData } from './roadmapLayoutEngine';
import RoadmapShRendererV2 from './RoadmapShRendererV2';
import ActionRoadmapWeb from './ActionRoadmapWeb';
import TopicRoadmapRenderer from './TopicRoadmapRenderer';
import './RoadmapViewer.css';

// Action roadmaps (từ generate_jit_graph.py — implement-centric)
const ACTION_ROADMAPS = ['jit-bulb', 'jit-quiz'];
// Topic roadmaps (từ pipeline v3 — concept → ULO/CIO/SIO)
const TOPIC_ROADMAPS = ['jit-bulb-v3'];
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
        const manifest = loaded.map(m => ({
          project_code: m.project_brief?.project_code,
          title: m.project_brief?.title,
          created_at: new Date().toISOString(),
          key: `roadmap_${m.project_brief?.project_code}`,
          _type: m._type
        }));
        localStorage.setItem('roadmap_manifest', JSON.stringify(manifest));
        setSelectedRoadmap(loaded[0]);
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
              value={selectedRoadmap.project_brief?.project_code || ''} 
              onChange={(e) => {
                const rm = roadmaps.find(r => r.project_brief?.project_code === e.target.value);
                if (rm) setSelectedRoadmap(rm);
              }}
            >
              {roadmaps.map(rm => (
                <option key={rm.project_brief?.project_code} value={rm.project_brief?.project_code}>
                  {rm.project_brief?.title} ({rm.project_brief?.project_code}) {rm._type === 'topic' ? '📘' : rm._type === 'action' ? '🎯' : '🗺️'}
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
          <div className="renderer-container" style={{ height: 'calc(100vh - 80px)' }}>
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
