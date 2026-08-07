import React, { useState, useEffect, useCallback } from 'react';
import { parseFrontendData } from './roadmapLayoutEngine';
import RoadmapShRendererV2 from './RoadmapShRendererV2';
import ActionRoadmapWeb from './ActionRoadmapWeb';
import './RoadmapViewer.css';

const knownRoadmaps = [
  { path: '/roadmaps/jit-bulb.json', code: 'JIT_BULB', isJIT: true },
  { path: '/roadmaps/jit-quiz.json', code: 'JIT_QUIZ', isJIT: true },
  { path: '/roadmaps/rust-cli.json', code: 'RUST_CLI_001', isJIT: false },
  { path: '/roadmaps/portfolio-js.json', code: 'PORTFOLIO_GAME', isJIT: false }
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
            loaded.push({ ...data, _source: rm.code, _isJIT: rm.isJIT });
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
          _isJIT: m._isJIT
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

  const isJIT = selectedRoadmap._isJIT === true;

  return (
    <div className="roadmap-viewer">
      <header className="viewer-header">
        <div className="header-left">
          <h2>{selectedRoadmap.project_brief?.title || 'Untitled Roadmap'}</h2>
          <span className={`badge ${isJIT ? 'jit' : 'roadmap-sh'}`}>
            {isJIT ? '🧠 JIT Knowledge Graph' : '🗺️ roadmap.sh Layout'}
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
                  {rm.project_brief?.title} ({rm.project_brief?.project_code}) {rm._isJIT ? '🧠' : '🗺️'}
                </option>
              ))}
            </select>
          </div>
          <div className="tab-selector">
            <button 
              className={activeTab === 'renderer' ? 'active' : ''}
              onClick={() => setActiveTab('renderer')}
            >
              {isJIT ? 'Graph View' : 'Layout'}
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
            {isJIT ? (
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
