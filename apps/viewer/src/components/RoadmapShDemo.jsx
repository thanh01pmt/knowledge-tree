import { useState, useEffect, useCallback } from 'react';
import RoadmapShRendererV2 from './RoadmapShRendererV2';
import './RoadmapShDemo.css';

export default function RoadmapShDemo() {
  const [rawData, setRawData] = useState(null);
  const [frontendData, setFrontendData] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);
  const [viewMode, setViewMode] = useState('v2'); // 'v2' | 'reactflow' | 'raw' | 'frontend'
  const [useAlgorithmic, setUseAlgorithmic] = useState(true);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Load raw roadmap data
      const rawResp = await fetch('/roadmap_sh_frontend/context/raw_roadmap.json');
      if (rawResp.ok) {
        const raw = await rawResp.json();
        setRawData(raw);
      }
      
      // Load frontend.json (ReactFlow format)
      const frontendResp = await fetch('/roadmap_sh_frontend/context/frontend.json');
      if (frontendResp.ok) {
        const frontend = await frontendResp.json();
        setFrontendData(frontend);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleNodeClick = useCallback((event, node) => {
    setSelectedNode(node);
  }, []);

  if (loading) {
    return (
      <div className="roadmap-sh-demo loading">
        <div className="spinner"></div>
        <p>Loading roadmap.sh data...</p>
      </div>
    );
  }

  return (
    <div className="roadmap-sh-demo">
      <header className="demo-header">
        <div className="header-left">
          <h1>🗺️ roadmap.sh Frontend Renderer V2</h1>
          <p className="subtitle">Exact A4 layout replication with Balsamiq style</p>
        </div>
        <div className="header-right">
          <div className="mode-toggle">
            <button 
              className={viewMode === 'v2' ? 'active' : ''} 
              onClick={() => setViewMode('v2')}
            >
              V2: Exact Layout
            </button>
            <button 
              className={viewMode === 'reactflow' ? 'active' : ''} 
              onClick={() => setViewMode('reactflow')}
            >
              V1: Auto Layout
            </button>
            <button 
              className={viewMode === 'raw' ? 'active' : ''} 
              onClick={() => setViewMode('raw')}
            >
              Raw Data
            </button>
            <button 
              className={viewMode === 'frontend' ? 'active' : ''} 
              onClick={() => setViewMode('frontend')}
            >
              Frontend.json
            </button>
          </div>
          <div className="layout-toggle">
            <label>
              <input 
                type="checkbox" 
                checked={useAlgorithmic}
                onChange={(e) => setUseAlgorithmic(e.target.checked)}
              />
              Algorithmic Layout
            </label>
          </div>
        </div>
      </header>

      {error && <div className="error-banner">⚠️ {error}</div>}

      {viewMode === 'v2' && frontendData && (
        <div className="renderer-container">
          <RoadmapShRendererV2 
            frontendData={frontendData}
            onNodeClick={handleNodeClick}
            selectedNodeId={selectedNode?.id}
            useAlgorithmic={useAlgorithmic}
          />
        </div>
      )}

      {viewMode === 'reactflow' && rawData && (
        <div className="renderer-container coming-soon">
          <div className="coming-soon-content">
            <h3>V1 Auto Layout</h3>
            <p>Original ReactFlow renderer with auto Dagre layout</p>
          </div>
        </div>
      )}

      {viewMode === 'raw' && rawData && (
        <RawDataView data={rawData} />
      )}

      {viewMode === 'frontend' && frontendData && (
        <FrontendJsonView data={frontendData} />
      )}

      {selectedNode && (
        <NodeDetailPanel 
          node={selectedNode} 
          rawData={rawData}
          onClose={() => setSelectedNode(null)}
        />
      )}
    </div>
  );
}

function RawDataView({ data }) {
  const topics = data.topics || [];
  
  return (
    <div className="data-view">
      <div className="data-toolbar">
        <h3>Raw Roadmap Data ({topics.length} items)</h3>
        <input 
          type="text" 
          placeholder="Filter by name..." 
          className="filter-input"
          onChange={(e) => {
            const term = e.target.value.toLowerCase();
            document.querySelectorAll('.raw-topic').forEach(el => {
              const text = el.textContent.toLowerCase();
              el.style.display = text.includes(term) ? '' : 'none';
            });
          }}
        />
      </div>
      <div className="topics-list">
        {topics.map((topic, idx) => (
          <div key={idx} className={`raw-topic ${topic.type === 'TOPIC' ? 'topic' : 'subtopic'}`}>
            <div className="topic-header">
              <span className="topic-order">#{topic.order}</span>
              <span className={`topic-type ${topic.type.toLowerCase()}`}>{topic.type}</span>
              <span className="topic-name">{topic.name}</span>
              <span className="topic-prereq">→ {topic.prerequisite}</span>
            </div>
            {topic.legend && (
              <div className="topic-legend" style={{ borderColor: topic.legend.color }}>
                {topic.legend.label} ({topic.legend.position})
              </div>
            )}
            {topic.resources && topic.resources.length > 0 && (
              <div className="topic-resources">
                {topic.resources.slice(0, 3).map((r, i) => (
                  <a key={i} href={r.url} target="_blank" rel="noopener" className="resource-link">
                    {r.title}
                  </a>
                ))}
                {topic.resources.length > 3 && <span>+{topic.resources.length - 3} more</span>}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

function FrontendJsonView({ data }) {
  const nodes = data.nodes || [];
  const edges = data.edges || [];
  
  return (
    <div className="data-view">
      <div className="data-toolbar">
        <h3>Frontend.json (ReactFlow Format)</h3>
        <div className="stats">
          <span>{nodes.length} nodes</span>
          <span>{edges.length} edges</span>
        </div>
      </div>
      <div className="json-tabs">
        <div className="tab-buttons">
          <button className="active">Nodes</button>
          <button>Edges</button>
          <button>Metadata</button>
        </div>
        <div className="tab-content">
          <div className="json-tree">
            {nodes.map((node, idx) => (
              <details key={idx} className="json-node">
                <summary>
                  <span className="node-id">{node.id}</span>
                  <span className={`node-type ${node.type}`}>{node.type}</span>
                  {node.data?.label && <span className="node-label">{node.data.label}</span>}
                  <span className="node-position">({node.position?.x?.toFixed(0)}, {node.position?.y?.toFixed(0)})</span>
                </summary>
                <pre>{JSON.stringify(node, null, 2)}</pre>
              </details>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function NodeDetailPanel({ node, rawData, onClose }) {
  // Find matching raw topic
  const rawTopic = rawData?.topics?.find(t => 
    t.name === node.data?.label || 
    `topic-${t.order}` === node.id ||
    `subtopic-${t.order}` === node.id
  );

  return (
    <div className="side-panel-overlay" onClick={onClose}>
      <div className="side-panel" onClick={e => e.stopPropagation()}>
        <div className="side-panel-header">
          <h3>{node.data?.label || node.id}</h3>
          <button className="side-panel-close" onClick={onClose}>×</button>
        </div>
        <div className="side-panel-content">
          <dl>
            <dt>ReactFlow ID</dt><dd>{node.id}</dd>
            <dt>Type</dt><dd>{node.type}</dd>
            <dt>Position</dt><dd>({node.position?.x?.toFixed(1)}, {node.position?.y?.toFixed(1)})</dd>
            <dt>Measured</dt><dd>{node.measured?.width}×{node.measured?.height}</dd>
          </dl>
          
          {rawTopic && (
            <div className="panel-section">
              <h4>Raw Data</h4>
              <dl>
                <dt>Order</dt><dd>{rawTopic.order}</dd>
                <dt>Type</dt><dd>{rawTopic.type}</dd>
                <dt>Prerequisite</dt><dd>{rawTopic.prerequisite}</dd>
                {rawTopic.legend && (
                  <>
                    <dt>Legend</dt><dd>{rawTopic.legend.label}</dd>
                    <dt>Legend Color</dt><dd><span style={{color: rawTopic.legend.color}}>■</span> {rawTopic.legend.color}</dd>
                  </>
                )}
                {rawTopic.progress !== undefined && (
                  <>
                    <dt>Progress</dt><dd>{rawTopic.progress}%</dd>
                  </>
                )}
                {rawTopic.description && (
                  <>
                    <dt>Description</dt><dd>{rawTopic.description}</dd>
                  </>
                )}
              </dl>
            </div>
          )}
          
          {node.originalData && (
            <div className="panel-section">
              <h4>Full ReactFlow Node Data</h4>
              <pre>{JSON.stringify(node, null, 2)}</pre>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}