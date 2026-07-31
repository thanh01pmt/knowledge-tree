import { useState, useMemo } from 'react';
import KnowledgeTree3D from './components/KnowledgeTree3D';
import ControlPanel from './components/ControlPanel';
import { parseKnowledgeTree } from './utils/dataParser';
import rawTreeData from './data/master_tree.json';
import './App.css';

function App() {
  const [selectedNode, setSelectedNode] = useState(null);
  const [searchedNodeId, setSearchedNodeId] = useState(null);
  const [filters, setFilters] = useState({ showLabels: true, hideConcepts: true });
  const [simulationConfig, setSimulationConfig] = useState({ charge: -200, linkDistance: 80 });

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
        simulationConfig={simulationConfig}
        setSimulationConfig={setSimulationConfig}
      />

      {/* Main 3D Graph */}
      <div className="flex-1 relative h-full w-full">
        <KnowledgeTree3D 
          graphData={graphData} 
          linksBySource={linksBySource} 
          onNodeSelect={setSelectedNode}
          searchedNodeId={searchedNodeId}
          filters={filters}
          simulationConfig={simulationConfig}
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
