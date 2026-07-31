import React, { useState, useMemo, useEffect, useRef } from 'react';
import { Search, Info, Settings2, Share2, PanelLeftClose, PanelLeftOpen } from 'lucide-react';

export default function ControlPanel({ 
  nodes, 
  onNodeSearch, 
  filters, 
  setFilters,
  simulationConfig,
  setSimulationConfig
}) {
  const [activeTab, setActiveTab] = useState('points');
  const [searchTerm, setSearchTerm] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [isCollapsed, setIsCollapsed] = useState(false);
  const searchRef = useRef();

  const suggestions = useMemo(() => {
    if (!searchTerm || searchTerm.length < 2) return [];
    const term = searchTerm.toLowerCase();
    return nodes
      .filter(n => 
        n.name.toLowerCase().includes(term) || 
        (n.description && n.description.toLowerCase().includes(term))
      )
      .slice(0, 10);
  }, [searchTerm, nodes]);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setShowSuggestions(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelect = (node) => {
    setSearchTerm('');
    setShowSuggestions(false);
    if (onNodeSearch) onNodeSearch(node);
  };

  if (isCollapsed) {
    return (
      <div className="h-full w-[41px] bg-[#1a1d21] border-r border-slate-800 flex flex-col items-center py-2 z-10 transition-all duration-300">
        <button 
          onClick={() => setIsCollapsed(false)}
          className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-md transition-colors"
          title="Expand Graph Configuration"
        >
          <PanelLeftOpen className="w-5 h-5" />
        </button>
      </div>
    );
  }

  return (
    <div className="h-full w-[320px] bg-[#1a1d21] border-r border-slate-800 flex flex-col text-slate-300 z-10 transition-all duration-300 flex-shrink-0">
      {/* Header */}
      <div className="flex items-center justify-between p-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <Settings2 className="w-4 h-4 text-slate-400" />
          <h2 className="text-[11px] font-semibold text-slate-400 uppercase tracking-widest">Graph Configuration</h2>
        </div>
        <button 
          onClick={() => setIsCollapsed(true)}
          className="text-slate-500 hover:text-slate-300 p-1 rounded-md hover:bg-slate-800 transition-colors"
        >
          <PanelLeftClose className="w-4 h-4" />
        </button>
      </div>

      {/* Tabs */}
      <div className="flex px-4 border-b border-slate-800">
        <button 
          className={`px-3 py-2 text-[11px] font-semibold uppercase tracking-widest border-b-2 transition-colors ${activeTab === 'points' ? 'border-slate-300 text-slate-200' : 'border-transparent text-slate-500 hover:text-slate-400'}`}
          onClick={() => setActiveTab('points')}
        >
          Points
        </button>
        <button 
          className={`px-3 py-2 text-[11px] font-semibold uppercase tracking-widest border-b-2 transition-colors ${activeTab === 'simulation' ? 'border-slate-300 text-slate-200' : 'border-transparent text-slate-500 hover:text-slate-400'}`}
          onClick={() => setActiveTab('simulation')}
        >
          Simulation
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-4 custom-scrollbar">
        {activeTab === 'points' && (
          <div className="flex flex-col gap-6">
            
            {/* Search Section */}
            <div className="flex flex-col gap-2">
              <div className="text-[11px] font-semibold text-slate-500 uppercase tracking-widest mb-1">Search</div>
              <div className="relative" ref={searchRef}>
                <div className="relative flex items-center">
                  <Search className="absolute left-2.5 w-4 h-4 text-slate-500" />
                  <input
                    type="text"
                    className="w-full bg-[#2a2f36] border border-slate-700 text-slate-200 text-xs rounded-md pl-8 pr-3 py-1.5 focus:outline-none focus:border-blue-500 transition-colors"
                    placeholder="Search node name..."
                    value={searchTerm}
                    onChange={e => {
                      setSearchTerm(e.target.value);
                      setShowSuggestions(true);
                    }}
                    onFocus={() => setShowSuggestions(true)}
                  />
                </div>
                {showSuggestions && suggestions.length > 0 && (
                  <div className="absolute top-full left-0 right-0 mt-1 bg-[#2a2f36] border border-slate-700 rounded-md shadow-xl overflow-hidden max-h-60 overflow-y-auto z-50">
                    {suggestions.map(node => (
                      <div 
                        key={node.id}
                        className="px-3 py-2 hover:bg-slate-700 cursor-pointer border-b border-slate-700/50 last:border-0"
                        onClick={() => handleSelect(node)}
                      >
                        <div className="text-slate-200 text-sm font-medium truncate">{node.name}</div>
                        <div className="text-[10px] text-slate-400 uppercase mt-0.5">{node.level}</div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Labels Section */}
            <div className="flex flex-col gap-2">
              <div className="text-[11px] font-semibold text-slate-500 uppercase tracking-widest mb-1">Labels</div>
              <div className="bg-[#2a2f36] rounded-md p-3 flex flex-col gap-4 border border-slate-800">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-slate-300">Show Node Labels</span>
                    <Info className="w-3.5 h-3.5 text-slate-500 cursor-help" title="Hiển thị tên nổi trên các node" />
                  </div>
                  <button 
                    role="switch"
                    aria-checked={filters.showLabels}
                    onClick={() => setFilters({...filters, showLabels: !filters.showLabels})}
                    className={`relative inline-flex h-4 w-7 items-center rounded-full transition-colors focus:outline-none ${filters.showLabels ? 'bg-slate-400' : 'bg-slate-600'}`}
                  >
                    <span className={`inline-block h-3 w-3 transform rounded-full bg-white transition-transform ${filters.showLabels ? 'translate-x-3.5' : 'translate-x-0.5'}`} />
                  </button>
                </div>
              </div>
            </div>

            {/* Clusters / Concepts Section */}
            <div className="flex flex-col gap-2">
              <div className="text-[11px] font-semibold text-slate-500 uppercase tracking-widest mb-1">Hierarchy View</div>
              <div className="bg-[#2a2f36] rounded-md p-3 flex flex-col gap-4 border border-slate-800">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-slate-300">Hide Concepts (Anti-Hairball)</span>
                    <Info className="w-3.5 h-3.5 text-slate-500 cursor-help" title="Ẩn các node con cấp thấp nhất để đồ thị thoáng hơn" />
                  </div>
                  <button 
                    role="switch"
                    aria-checked={filters.hideConcepts}
                    onClick={() => setFilters({...filters, hideConcepts: !filters.hideConcepts})}
                    className={`relative inline-flex h-4 w-7 items-center rounded-full transition-colors focus:outline-none ${filters.hideConcepts ? 'bg-slate-400' : 'bg-slate-600'}`}
                  >
                    <span className={`inline-block h-3 w-3 transform rounded-full bg-white transition-transform ${filters.hideConcepts ? 'translate-x-3.5' : 'translate-x-0.5'}`} />
                  </button>
                </div>
              </div>
            </div>

          </div>
        )}

        {activeTab === 'simulation' && (
          <div className="flex flex-col gap-6">
            <div className="flex flex-col gap-2">
              <div className="text-[11px] font-semibold text-slate-500 uppercase tracking-widest mb-1">Forces</div>
              
              <div className="bg-[#2a2f36] rounded-md p-3 flex flex-col gap-5 border border-slate-800">
                {/* Charge Strength Slider */}
                <div className="flex flex-col gap-2">
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-slate-300 uppercase tracking-wider text-[10px]">Repel Force (Charge)</span>
                    <span className="text-xs text-slate-400 font-mono">{Math.abs(simulationConfig.charge)}</span>
                  </div>
                  <input 
                    type="range" 
                    min="50" max="1000" step="10"
                    value={Math.abs(simulationConfig.charge)}
                    onChange={(e) => setSimulationConfig({...simulationConfig, charge: -parseInt(e.target.value)})}
                    className="w-full h-1.5 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-slate-400"
                  />
                </div>

                {/* Link Distance Slider */}
                <div className="flex flex-col gap-2">
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-slate-300 uppercase tracking-wider text-[10px]">Link Distance</span>
                    <span className="text-xs text-slate-400 font-mono">{simulationConfig.linkDistance}</span>
                  </div>
                  <input 
                    type="range" 
                    min="10" max="300" step="5"
                    value={simulationConfig.linkDistance}
                    onChange={(e) => setSimulationConfig({...simulationConfig, linkDistance: parseInt(e.target.value)})}
                    className="w-full h-1.5 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-slate-400"
                  />
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
      
      {/* Footer Branding (Optional matching Cosmos UI) */}
      <div className="p-3 border-t border-slate-800 flex justify-between items-center text-xs text-slate-600">
        <span>{nodes.length} points</span>
        <span className="opacity-50">Knowledge Tree</span>
      </div>
    </div>
  );
}
