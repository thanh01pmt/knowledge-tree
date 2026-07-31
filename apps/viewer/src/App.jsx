import { useState, useMemo } from 'react';
import KnowledgeTree3D from './components/KnowledgeTree3D';
import { parseKnowledgeTree } from './utils/dataParser';
import rawTreeData from './data/master_tree.json';
import './App.css';

function App() {
  const [selectedNode, setSelectedNode] = useState(null);

  // Parse data once
  const { graphData, linksBySource } = useMemo(() => {
    return parseKnowledgeTree(rawTreeData);
  }, []);

  return (
    <div className="app-container">
      {/* Top Header / Search Bar Placeholder */}
      <header className="app-header">
        <h1>Knowledge Tree Viewer</h1>
        <div className="search-bar-placeholder">
          🔍 Search...
        </div>
      </header>

      {/* Main 3D Graph */}
      <div className="graph-container">
        <KnowledgeTree3D 
          graphData={graphData} 
          linksBySource={linksBySource} 
          onNodeSelect={setSelectedNode} 
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
