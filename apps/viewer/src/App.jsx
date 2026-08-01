import { useState, useMemo, useEffect, useCallback } from 'react';
import KnowledgeTree3D from './components/KnowledgeTree3D';
import ControlPanel from './components/ControlPanel';
import NodeDetailsPanel from './components/NodeDetailsPanel';
import { parseKnowledgeTree } from './utils/dataParser';
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
  learning_objective: { textHeight: 2, textColor: '#44bbff', textWeight: 'normal', shape: 'sphere', opacity: 0.4 },
  keyword: { textHeight: 2, textColor: '#ff44aa', textWeight: 'normal', shape: 'star', opacity: 0.8 },
};

function App() {
  const [selectedNode, setSelectedNode] = useState(null);
  const [searchedNodeId, setSearchedNodeId] = useState(null);
  const [filters, setFilters] = useState({ showLabels: true, maxLevel: 'topic', showPrerequisites: false });
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

  const [rawTreeData, setRawTreeData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        // Fallback to local supabase functions URL for testing if env is missing
        const apiUrl = import.meta.env.VITE_SUPABASE_FUNCTIONS_URL || 'http://127.0.0.1:54321/functions/v1';
        const response = await fetch(`${apiUrl}/get-knowledge-tree`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setRawTreeData(data);
      } catch (err) {
        console.error("Error fetching knowledge tree:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  // Parse data once it's loaded
  const { graphData, linksBySource, linksByTarget, prereqLinksBySource, prereqLinksByTarget } = useMemo(() => {
    if (!rawTreeData) return { graphData: { nodes: [], links: [] }, linksBySource: {}, linksByTarget: {}, prereqLinksBySource: {}, prereqLinksByTarget: {} };
    return parseKnowledgeTree(rawTreeData);
  }, [rawTreeData]);

  const [history, setHistory] = useState([]);
  const [historyIndex, setHistoryIndex] = useState(-1);

  const handleNodeSelect = useCallback((node, isHistoryNavigation = false) => {
    if (!node) {
      setSelectedNode(null);
      return;
    }
    
    if (!isHistoryNavigation) {
      setHistory(prev => {
        const newHistory = prev.slice(0, historyIndex + 1);
        newHistory.push(node);
        return newHistory;
      });
      setHistoryIndex(prev => prev + 1);
    }
    
    setSelectedNode(node);
  }, [historyIndex]);

  const handleNavigateHistory = useCallback((direction) => {
    if (direction === 'back' && historyIndex > 0) {
      setHistoryIndex(historyIndex - 1);
      handleNodeSelect(history[historyIndex - 1], true);
    } else if (direction === 'forward' && historyIndex < history.length - 1) {
      setHistoryIndex(historyIndex + 1);
      handleNodeSelect(history[historyIndex + 1], true);
    }
  }, [history, historyIndex, handleNodeSelect]);

  const handleNodeSearch = useCallback(node => {
    setSearchedNodeId(node.id);
    handleNodeSelect(node);
  }, [handleNodeSelect]);

  if (loading) {
    return <div className="flex h-screen w-screen items-center justify-center bg-[#0f172a] text-slate-200">Loading Knowledge Tree from Supabase...</div>;
  }

  if (error) {
    return <div className="flex h-screen w-screen items-center justify-center bg-[#0f172a] text-red-400">Error loading data: {error}</div>;
  }

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
      <div className="flex-1 min-w-0 relative h-full w-full">
        <KnowledgeTree3D 
          graphData={graphData} 
          linksBySource={linksBySource} 
          linksByTarget={linksByTarget}
          prereqLinksBySource={prereqLinksBySource}
          prereqLinksByTarget={prereqLinksByTarget}
          onNodeSelect={handleNodeSelect}
          searchedNodeId={searchedNodeId}
          filters={filters}
          visualConfig={visualConfig}
          levelConfig={levelConfig}
          selectedNode={selectedNode}
        />
      </div>

      {/* Side Panel */}
      {/* Side Panel */}
      <NodeDetailsPanel
        selectedNode={selectedNode}
        onNodeSelect={handleNodeSelect}
        graphData={graphData}
        linksBySource={linksBySource}
        linksByTarget={linksByTarget}
        history={history}
        historyIndex={historyIndex}
        onNavigateHistory={handleNavigateHistory}
      />
    </div>
  );
}

export default App;
