import { useState, useMemo, useEffect } from 'react';
import KnowledgeTree3D from './components/KnowledgeTree3D';
import ControlPanel from './components/ControlPanel';
import { parseKnowledgeTree } from './utils/dataParser';
import rawTreeData from './data/master_tree.json';
import './App.css';

const DEFAULT_VISUAL_CONFIG = { 
  // Points
  nodeSizeMultiplier: 3.0,
  coloringStrategy: 'hierarchy', 
  showUnselectedLabels: false,
  
  // Links
  linkOpacity: 0.75,
  linkWidth: 0.5,
  showParticles: false,
  
  // Simulation
  charge: -80, 
  linkDistance: 15,
  centerGravity: 0.5
};

const DEFAULT_LEVEL_CONFIG = {
  field: { textHeight: 15, textColor: '#f6fa00', textWeight: 'bold', shape: 'dodecahedron', opacity: 1.0 },
  subject: { textHeight: 12, textColor: '#8cba36', textWeight: 'normal', shape: 'box', opacity: 0.9 },
  category: { textHeight: 7, textColor: '#cccccc', textWeight: 'normal', shape: 'box', opacity: 0.8 },
  topic: { textHeight: 5, textColor: '#aaaaaa', textWeight: 'normal', shape: 'tetrahedron', opacity: 0.7 },
  concept: { textHeight: 3, textColor: '#888888', textWeight: 'normal', shape: 'sphere', opacity: 0.6 },
};

function App() {
  const [selectedNode, setSelectedNode] = useState(null);
  const [searchedNodeId, setSearchedNodeId] = useState(null);
  const [filters, setFilters] = useState({ showLabels: true, hideConcepts: true });
  const [visualConfig, setVisualConfig] = useState(() => {
    const saved = localStorage.getItem('kt_visualConfig');
    return saved ? JSON.parse(saved) : DEFAULT_VISUAL_CONFIG;
  });

  const [levelConfig, setLevelConfig] = useState(() => {
    const saved = localStorage.getItem('kt_levelConfig');
    return saved ? JSON.parse(saved) : DEFAULT_LEVEL_CONFIG;
  });

  // Save to local storage whenever config changes
  useEffect(() => {
    localStorage.setItem('kt_visualConfig', JSON.stringify(visualConfig));
  }, [visualConfig]);

  useEffect(() => {
    localStorage.setItem('kt_levelConfig', JSON.stringify(levelConfig));
  }, [levelConfig]);

  const resetConfigs = () => {
    setVisualConfig(DEFAULT_VISUAL_CONFIG);
    setLevelConfig(DEFAULT_LEVEL_CONFIG);
    localStorage.removeItem('kt_visualConfig');
    localStorage.removeItem('kt_levelConfig');
  };

  // Parse data once
  const { graphData, linksBySource } = useMemo(() => {
    return parseKnowledgeTree(rawTreeData);
  }, []);

  const handleNodeSearch = node => {
    setSearchedNodeId(node.id);
    setSelectedNode(node);
  };

  return (
    <div className="flex h-screen w-screen bg-[#0f172a] overflow-hidden text-slate-200">
      <ControlPanel 
        nodes={graphData.nodes} 
        onNodeSearch={handleNodeSearch}
        filters={filters}
        setFilters={setFilters}
        visualConfig={visualConfig}
        setVisualConfig={setVisualConfig}
        levelConfig={levelConfig}
        setLevelConfig={setLevelConfig}
        onReset={resetConfigs}
      />

      {/* Main 3D Graph */}
      <div className="flex-1 relative h-full w-full">
        <KnowledgeTree3D 
          graphData={graphData} 
          linksBySource={linksBySource} 
          onNodeSelect={setSelectedNode}
          searchedNodeId={searchedNodeId}
          filters={filters}
          visualConfig={visualConfig}
          levelConfig={levelConfig}
        />
      </div>

      {/* Side Panel */}
      {selectedNode && (
        <aside className="side-panel slide-in">
          <h2>{selectedNode.name}</h2>
          <span className="badge">{selectedNode.level.toUpperCase()}</span>
          <p>{selectedNode.description}</p>
          
          {selectedNode.level === 'concept' ? (
            <div className="outcomes">
              <h3>Learning Outcomes</h3>
              <p>Fetching ULO, CIO, SIO...</p>
              {/* Future: fetch from Supabase here */}
            </div>
          ) : (
            <div className="instructions">
              <p>Explore child nodes or select a specific concept to see detailed learning outcomes.</p>
            </div>
          )}
        </aside>
      )}
    </div>
  );
}

export default App;
