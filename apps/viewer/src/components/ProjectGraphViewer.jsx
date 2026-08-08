import React, { useState, useEffect, useMemo, useRef, useCallback } from 'react';
import ForceGraph3D from 'react-force-graph-3d';
import SpriteText from 'three-spritetext';
import * as THREE from 'three';

const LAYER_COLORS = {
  presentation: '#4ade80', // green
  core: '#60a5fa',         // blue
  infra: '#f472b6',        // pink
  'external-service': '#fbbf24', // yellow
};

export default function ProjectGraphViewer({ theme }) {
  const [graphData, setGraphData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [selectedFeature, setSelectedFeature] = useState(null);
  const [selectedCapability, setSelectedCapability] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);
  
  const [dimensions, setDimensions] = useState({ 
    width: typeof window !== 'undefined' ? window.innerWidth - 320 : 800, 
    height: typeof window !== 'undefined' ? window.innerHeight : 600 
  });
  const containerRef = useRef();

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await fetch('/data/project_graph_verified.json');
        if (!response.ok) throw new Error('Failed to load project graph data');
        const data = await response.json();
        setGraphData(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  useEffect(() => {
    const handleResize = () => {
      setDimensions({
        width: window.innerWidth - 320,
        height: window.innerHeight
      });
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const forceGraphData = useMemo(() => {
    if (!graphData) return { nodes: [], links: [] };
    const nodes = graphData.architecture.nodes.map(n => ({
      ...n,
      val: 2 // base size
    }));
    const links = graphData.architecture.edges.map(e => ({
      source: e.from,
      target: e.to,
      type: e.type
    }));
    return { nodes, links };
  }, [graphData]);
  
  // Compute highlighted nodes based on selected feature
  const highlightedNodes = useMemo(() => {
    if (!selectedFeature && !selectedCapability) return null;
    const itemsToHighlight = new Set();
    
    const checkApiUsage = (apiUsage, node) => {
      if (!apiUsage || !node.id) return false;
      return apiUsage.some(api => api.includes(node.id) || node.id.includes(api) || node.responsibility.includes(api));
    };

    if (selectedFeature && selectedFeature.api_usage) {
      forceGraphData.nodes.forEach(n => {
        if (checkApiUsage(selectedFeature.api_usage, n)) {
          itemsToHighlight.add(n.id);
        }
      });
    }
    
    return itemsToHighlight;
  }, [selectedFeature, selectedCapability, forceGraphData.nodes]);

  const handleNodeClick = useCallback(node => {
    setSelectedNode(node);
  }, []);

  if (loading) return <div className="flex h-full items-center justify-center">Loading Project Graph...</div>;
  if (error) return <div className="flex h-full items-center justify-center text-red-500">Error: {error}</div>;
  if (!graphData) return null;

  return (
    <div className={`flex h-full w-full font-sans ${theme === 'dark' ? 'dark text-slate-200' : 'text-slate-800'}`}>
      {/* SIDEBAR */}
      <div className="w-80 h-full bg-white dark:bg-[#1e293b] border-r border-[#e6e6e6] dark:border-slate-800 flex flex-col overflow-y-auto z-10 shadow-[2px_0_10px_rgba(0,0,0,0.05)]">
        <div className="p-5 border-b border-[#e6e6e6] dark:border-slate-800 bg-[#f8f9fa] dark:bg-transparent">
          <h2 className="m-0 text-[17px] font-bold tracking-tight mb-2 text-[#18181b] dark:text-slate-100">{graphData.project.name}</h2>
          <p className="text-[13px] text-slate-500 dark:text-slate-400 line-clamp-3 leading-relaxed mb-4">{graphData.project.purpose}</p>
          
          <div className="flex flex-wrap gap-1.5">
            {graphData.project.platform?.map(p => (
              <span key={p} className="px-2 py-0.5 bg-slate-800 text-white rounded text-[10px] font-bold uppercase tracking-wider">{p}</span>
            ))}
            {graphData.project.architecture?.map(a => (
              <span key={a} className="px-2 py-0.5 bg-indigo-100 dark:bg-indigo-900/40 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-500/30 rounded text-[10px] font-bold tracking-wider">{a}</span>
            ))}
            {Object.values(graphData.project.tech_stack || {}).flat().slice(0, 10).map(tech => (
              <span key={tech} className="px-2 py-0.5 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 rounded text-[10px] font-semibold shadow-sm">{tech}</span>
            ))}
            {Object.values(graphData.project.tech_stack || {}).flat().length > 10 && (
              <span className="px-2 py-0.5 bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 text-slate-400 dark:text-slate-500 rounded text-[10px] font-semibold">+{Object.values(graphData.project.tech_stack || {}).flat().length - 10}</span>
            )}
          </div>
        </div>
        
        <div className="p-4 flex-1 overflow-y-auto">
          <h3 className="text-[11px] font-bold text-slate-400 dark:text-slate-500 mb-3 uppercase tracking-widest">Features ({graphData.features.length})</h3>
          <div className="flex flex-col gap-2 mb-8">
            {graphData.features.map(f => (
              <div 
                key={f.id}
                onClick={() => {
                  setSelectedFeature(f === selectedFeature ? null : f);
                  setSelectedCapability(null);
                  setSelectedNode(null);
                }}
                className={`p-3 rounded-lg cursor-pointer border text-sm transition-all ${
                  selectedFeature === f 
                    ? 'bg-[#f0f7f4] dark:bg-[#0e7c6b]/10 border-[#0e7c6b] shadow-sm' 
                    : 'bg-white dark:bg-[#1e293b] border-[#e6e6e6] dark:border-slate-700 hover:border-[#cbd5e1] dark:hover:border-slate-500 hover:shadow-sm'
                }`}
              >
                <div className={`font-semibold mb-1 ${selectedFeature === f ? 'text-[#0e7c6b] dark:text-[#2dd4bf]' : 'text-slate-800 dark:text-slate-200'}`}>
                  {f.name}
                </div>
                <div className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">{f.purpose}</div>
              </div>
            ))}
          </div>

          <h3 className="text-[11px] font-bold text-slate-400 dark:text-slate-500 mb-3 uppercase tracking-widest">Capabilities ({graphData.capabilities.length})</h3>
          <div className="flex flex-col gap-2 pb-4">
            {graphData.capabilities.map(c => (
              <div 
                key={c.id}
                onClick={() => {
                  setSelectedCapability(c === selectedCapability ? null : c);
                  setSelectedFeature(null);
                  setSelectedNode(null);
                }}
                className={`p-3 rounded-lg cursor-pointer border text-sm transition-all ${
                  selectedCapability === c 
                    ? 'bg-[#f0fbfd] dark:bg-[#0ea5e9]/10 border-[#0ea5e9] shadow-sm' 
                    : 'bg-white dark:bg-[#1e293b] border-[#e6e6e6] dark:border-slate-700 hover:border-[#cbd5e1] dark:hover:border-slate-500 hover:shadow-sm'
                }`}
              >
                <div className={`font-semibold mb-1 ${selectedCapability === c ? 'text-[#0ea5e9] dark:text-[#38bdf8]' : 'text-slate-800 dark:text-slate-200'}`}>
                  {c.name}
                </div>
                <div className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">{c.purpose}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* MAIN VIEW */}
      <div className="flex-1 relative bg-[#f8fafc] dark:bg-[#0f172a] min-w-0" ref={containerRef}>
        <div className="absolute inset-0">
          {dimensions.width > 0 && (
            <ForceGraph3D
              backgroundColor={theme === 'dark' ? "#0f172a" : "#f8fafc"}
              width={dimensions.width}
              height={dimensions.height}
          graphData={forceGraphData}
          nodeLabel="id"
          nodeColor={node => {
            if (highlightedNodes && highlightedNodes.size > 0) {
              return highlightedNodes.has(node.id) ? (LAYER_COLORS[node.layer] || '#999') : '#e2e8f0';
            }
            if (selectedNode) {
              return selectedNode.id === node.id ? '#ef4444' : '#e2e8f0';
            }
            return LAYER_COLORS[node.layer] || '#999';
          }}
          nodeOpacity={node => {
            if (highlightedNodes && highlightedNodes.size > 0) {
              return highlightedNodes.has(node.id) ? 1 : 0.15;
            }
            if (selectedNode) {
              return selectedNode.id === node.id ? 1 : 0.15;
            }
            return 0.9;
          }}
          linkOpacity={link => {
            if (highlightedNodes && highlightedNodes.size > 0) {
              return (highlightedNodes.has(link.source.id) && highlightedNodes.has(link.target.id)) ? 0.8 : 0.05;
            }
            return 0.4;
          }}
          linkWidth={link => {
            if (highlightedNodes && highlightedNodes.size > 0) {
              return (highlightedNodes.has(link.source.id) && highlightedNodes.has(link.target.id)) ? 1.5 : 0.5;
            }
            return 0.5;
          }}
          linkColor={() => '#94a3b8'}
          onNodeClick={handleNodeClick}
          nodeThreeObject={node => {
            const isHighlight = highlightedNodes?.has(node.id) || selectedNode?.id === node.id;
            const isFaded = (highlightedNodes?.size > 0 || selectedNode) && !isHighlight;
            
            const group = new THREE.Group();
            
            // 1. Sphere
            const sphereGeo = new THREE.SphereGeometry(isHighlight ? 4 : 2.5, 16, 16);
            const color = selectedNode?.id === node.id ? '#ef4444' : (LAYER_COLORS[node.layer] || '#94a3b8');
            const sphereMat = new THREE.MeshLambertMaterial({ 
              color: color,
              transparent: true,
              opacity: isFaded ? 0.15 : (isHighlight ? 1 : 0.9) 
            });
            const sphere = new THREE.Mesh(sphereGeo, sphereMat);
            group.add(sphere);
            
            // 2. Text
            const sprite = new SpriteText(node.id);
            sprite.color = isFaded ? (theme === 'dark' ? '#475569' : '#94a3b8') : (isHighlight ? (theme === 'dark' ? '#f8fafc' : '#0f172a') : (theme === 'dark' ? '#94a3b8' : '#334155'));
            sprite.textHeight = isHighlight ? 3.5 : 2.5;
            sprite.fontWeight = isHighlight ? 'bold' : 'normal';
            sprite.position.y = isHighlight ? 7 : 5; // Offset text above the sphere
            
            // Add a background plate for highlighted nodes so they are easier to read
            if (isHighlight) {
              sprite.backgroundColor = theme === 'dark' ? 'rgba(15, 23, 42, 0.9)' : 'rgba(255, 255, 255, 0.9)';
              sprite.padding = 2;
              sprite.borderRadius = 4;
            }
            
            group.add(sprite);
            return group;
          }}
          nodeThreeObjectExtend={false}
        />
        )}
        </div>

        {/* Node Details Overlay */}
        {selectedNode && (
          <div className="absolute top-6 right-6 w-80 bg-white/95 backdrop-blur-md shadow-[0_8px_30px_rgb(0,0,0,0.12)] rounded-xl border border-slate-200/60 p-5 z-20">
            <div className="flex justify-between items-start mb-4">
              <h3 className="font-bold text-slate-800 text-lg leading-tight pr-4">{selectedNode.id}</h3>
              <button 
                onClick={() => setSelectedNode(null)}
                className="text-slate-400 hover:text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-full w-7 h-7 flex items-center justify-center transition-colors"
              >
                ✕
              </button>
            </div>
            
            <div className="flex flex-wrap gap-2 mb-5">
              <span className="px-2.5 py-1 bg-indigo-50 text-indigo-700 border border-indigo-100 rounded-md text-[10px] font-bold uppercase tracking-wider">
                {selectedNode.type}
              </span>
              <span className="px-2.5 py-1 bg-emerald-50 text-emerald-700 border border-emerald-100 rounded-md text-[10px] font-bold uppercase tracking-wider">
                {selectedNode.layer}
              </span>
            </div>

            <div className="mb-5">
              <h4 className="text-[11px] font-bold text-slate-400 uppercase tracking-widest mb-2">Responsibility</h4>
              <p className="text-[13px] text-slate-700 leading-relaxed">{selectedNode.responsibility}</p>
            </div>

            {selectedNode.depends_on?.length > 0 && (
              <div>
                <h4 className="text-[11px] font-bold text-slate-400 uppercase tracking-widest mb-2">Depends On</h4>
                <ul className="text-[13px] text-slate-700 space-y-1.5">
                  {selectedNode.depends_on.map(d => (
                    <li key={d} className="flex items-start gap-2">
                      <span className="text-slate-300 mt-0.5">↳</span>
                      <span className="font-mono text-slate-600">{d}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
