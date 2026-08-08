import { useState, useMemo, useEffect, useCallback, useRef } from 'react';
import KnowledgeTree3D from './components/KnowledgeTree3D';
import ControlPanel from './components/ControlPanel';
import NodeDetailsPanel from './components/NodeDetailsPanel';
import DashboardModal from './components/DashboardModal';
import OnboardingTour from './components/OnboardingTour';
import RoadmapViewer from './components/RoadmapViewer';
import ProjectGraphViewer from './components/ProjectGraphViewer';
import AppLayout from './components/layout/AppLayout';
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

  const [isolatedNodeId, setIsolatedNodeId] = useState(null);
  const [searchMatchingIds, setSearchMatchingIds] = useState(new Set());
  const [isConfigSidebarOpen, setIsConfigSidebarOpen] = useState(true);
  const [isDashboardOpen, setIsDashboardOpen] = useState(false);
  const [viewMode, setViewMode] = useState(() => {
    // Deep-link: ?view=roadmap / ?view=project-graph / ?view=knowledge
    const v = new URLSearchParams(window.location.search).get('view');
    return (v === 'roadmap' || v === 'project-graph' || v === 'knowledge') ? v : 'knowledge';
  }); // 'knowledge' | 'roadmap' | 'project-graph'

  const [theme, setTheme] = useState(() => {
    const saved = localStorage.getItem('kt_theme');
    return saved || 'dark';
  });

  useEffect(() => {
    localStorage.setItem('kt_theme', theme);
  }, [theme]);

  const [rawTreeData, setRawTreeData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        // Fallback to local supabase functions URL for testing if env is missing
        const apiUrl = import.meta.env.VITE_SUPABASE_FUNCTIONS_URL || 'http://127.0.0.1:54321/functions/v1';
        const anonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || '';
        
        const headers = {};
        if (anonKey) {
          headers['Authorization'] = `Bearer ${anonKey}`;
        }
        
        const response = await fetch(`${apiUrl}/get-knowledge-tree`, { headers });
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
  const historyIndexRef = useRef(-1);
  historyIndexRef.current = historyIndex;

  const handleNodeSelect = useCallback((node, isHistoryNavigation = false) => {
    if (!node) {
      setSelectedNode(null);
      return;
    }
    
    if (!isHistoryNavigation) {
      const currIdx = historyIndexRef.current;
      setHistory(prev => {
        const newHistory = prev.slice(0, currIdx + 1);
        newHistory.push(node);
        return newHistory;
      });
      setHistoryIndex(currIdx + 1);
    }
    
    setSelectedNode(node);
  }, []);

  const handleNavigateHistory = useCallback((direction) => {
    setHistoryIndex(prevIdx => {
      if (direction === 'back' && prevIdx > 0) {
        const newIdx = prevIdx - 1;
        setHistory(h => {
          if (h[newIdx]) setSelectedNode(h[newIdx]);
          return h;
        });
        return newIdx;
      } else if (direction === 'forward') {
        setHistory(h => {
          if (prevIdx < h.length - 1) {
            const newIdx = prevIdx + 1;
            if (h[newIdx]) setSelectedNode(h[newIdx]);
            return h;
          }
          return h;
        });
        return Math.min(prevIdx + 1, history.length - 1);
      }
      return prevIdx;
    });
  }, [history.length]);

  // Sync URL query param with selectedNode
  useEffect(() => {
    if (loading || !graphData.nodes.length) return;

    // Read initial node from URL on load
    const params = new URLSearchParams(window.location.search);
    const initialNodeId = params.get('node');

    if (initialNodeId && !selectedNode) {
      const initialNode = graphData.nodes.find(n => n.id === initialNodeId);
      if (initialNode) {
        setSelectedNode(initialNode);
      }
    }
  }, [loading, graphData.nodes]);

  // Update URL whenever selectedNode changes
  useEffect(() => {
    if (loading) return;
    const url = new URL(window.location.href);
    if (selectedNode) {
      url.searchParams.set('node', selectedNode.id);
    } else {
      url.searchParams.delete('node');
    }
    window.history.replaceState(null, '', url.pathname + url.search);
  }, [selectedNode, loading]);

  const handleNodeSearch = useCallback(node => {
    setSearchedNodeId(node.id);
    handleNodeSelect(node);
  }, [handleNodeSelect]);

  // Only show loading/error for Knowledge Tree view
  if (viewMode === 'knowledge') {
    if (loading) {
      return (
        <div className="flex h-screen w-screen flex-col items-center justify-center bg-[#0f172a] text-slate-200">
          <div className="relative flex items-center justify-center mb-6">
            <div className="w-16 h-16 rounded-full border-4 border-blue-500/20 border-t-blue-500 animate-spin" />
            <div className="absolute w-8 h-8 rounded-full bg-blue-500/10 backdrop-blur border border-blue-400/30 animate-pulse" />
          </div>
          <h2 className="text-lg font-bold text-slate-100 tracking-wide mb-1">Knowledge Tree</h2>
          <p className="text-xs text-slate-400 animate-pulse">Loading curriculum graph from Supabase Cloud...</p>
        </div>
      );
    }

    if (error) {
      return (
        <div className="flex h-screen w-screen flex-col items-center justify-center bg-[#0f172a] text-red-400 p-6 text-center">
          <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 max-w-md">
            <h3 className="font-bold text-base text-red-300 mb-2">Connection Error</h3>
            <p className="text-xs text-red-400 leading-relaxed mb-4">{error}</p>
            <button 
              onClick={() => window.location.reload()} 
              className="px-4 py-2 bg-red-600 hover:bg-red-500 text-white rounded-lg text-xs font-semibold transition-colors"
            >
              Retry Connection
            </button>
          </div>
        </div>
      );
    }
  }

  return (
    <AppLayout viewMode={viewMode} setViewMode={setViewMode} theme={theme} setTheme={setTheme}>
      <OnboardingTour />

      {viewMode === 'knowledge' ? (
        <>
          <DashboardModal 
            isOpen={isDashboardOpen} 
            onClose={() => setIsDashboardOpen(false)} 
            graphData={graphData} 
          />

          <ControlPanel 
            isOpen={isConfigSidebarOpen}
            onToggle={() => setIsConfigSidebarOpen(!isConfigSidebarOpen)} 
            nodes={graphData.nodes} 
            onNodeSearch={handleNodeSearch}
            filters={filters}
            setFilters={setFilters}
            visualConfig={visualConfig}
            setVisualConfig={setVisualConfig}
            levelConfig={levelConfig}
            setLevelConfig={setLevelConfig}
            onReset={resetConfigs}
            onSearchMatchesChange={setSearchMatchingIds}
            onOpenDashboard={() => setIsDashboardOpen(true)}
          />

          {/* Main 3D Graph */}
          <div className="flex-1 min-w-0 relative h-full w-full">
            <KnowledgeTree3D 
              isConfigSidebarOpen={isConfigSidebarOpen}
              onToggleConfigSidebar={() => setIsConfigSidebarOpen(!isConfigSidebarOpen)} 
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
              isolatedNodeId={isolatedNodeId}
              searchMatchingIds={searchMatchingIds}
              theme={theme}
            />
          </div>

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
            isolatedNodeId={isolatedNodeId}
            setIsolatedNodeId={setIsolatedNodeId}
          />
        </>
      ) : viewMode === 'roadmap' ? (
        <RoadmapViewer theme={theme} />
      ) : (
        <ProjectGraphViewer theme={theme} />
      )}
    </AppLayout>
  );
}

export default App;
