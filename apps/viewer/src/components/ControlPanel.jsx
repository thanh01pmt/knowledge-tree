import React, { useState, useMemo, useEffect, useRef } from 'react';
import { Search, Info, Settings2, Share2, PanelLeftClose, PanelLeftOpen, RotateCcw } from 'lucide-react';

export default function ControlPanel({ 
  nodes, 
  onNodeSearch, 
  filters, 
  setFilters,
  visualConfig,
  setVisualConfig,
  levelConfig,
  setLevelConfig,
  onReset
}) {
  const [activeTab, setActiveTab] = useState('elements');
  const [selectedLevel, setSelectedLevel] = useState('field');
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
    
    const handleFocusSearch = () => {
      setIsCollapsed(false);
      setActiveTab('points');
      if (searchRef.current) {
        const input = searchRef.current.querySelector('input');
        if (input) {
          // Delay focus slightly to allow state update to render
          setTimeout(() => input.focus(), 100);
        }
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('focus-search', handleFocusSearch);
    
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('focus-search', handleFocusSearch);
    };
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
      <div className="flex items-center justify-between p-3 border-b border-slate-800 flex-shrink-0">
        <div className="flex items-center gap-2">
          <Settings2 className="w-4 h-4 text-slate-400" />
          <h2 className="text-[11px] font-semibold text-slate-400 uppercase tracking-widest">Graph Configuration</h2>
        </div>
        <div className="flex items-center gap-1">
          <button 
            onClick={onReset}
            className="text-slate-500 hover:text-slate-300 p-1.5 rounded-md hover:bg-slate-800 transition-colors"
            title="Reset to defaults"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
          <button 
            onClick={() => setIsCollapsed(true)}
            className="text-slate-500 hover:text-slate-300 p-1.5 rounded-md hover:bg-slate-800 transition-colors"
            title="Collapse Panel"
          >
            <PanelLeftClose className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex px-4 border-b border-slate-800 flex-shrink-0">
        <button 
          className={`px-3 py-2 text-[11px] font-semibold uppercase tracking-widest border-b-2 transition-colors ${activeTab === 'elements' ? 'border-slate-300 text-slate-200' : 'border-transparent text-slate-500 hover:text-slate-400'}`}
          onClick={() => setActiveTab('elements')}
        >
          Elements
        </button>
        <button 
          className={`px-3 py-2 text-[11px] font-semibold uppercase tracking-widest border-b-2 transition-colors ${activeTab === 'levels' ? 'border-slate-300 text-slate-200' : 'border-transparent text-slate-500 hover:text-slate-400'}`}
          onClick={() => setActiveTab('levels')}
        >
          Levels
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
        {activeTab === 'elements' && (
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

            {/* Coloring */}
            <div className="flex flex-col gap-2">
              <div className="text-[11px] font-semibold text-slate-500 uppercase tracking-widest mb-1">Coloring</div>
              <div className="bg-[#2a2f36] rounded-md p-3 flex flex-col gap-4 border border-slate-800">
                <div className="flex flex-col gap-2">
                  <label className="text-xs text-slate-300">Coloring Strategy</label>
                  <select 
                    value={visualConfig.coloringStrategy}
                    onChange={(e) => setVisualConfig({...visualConfig, coloringStrategy: e.target.value})}
                    className="w-full bg-[#1a1d21] border border-slate-700 text-slate-200 text-xs rounded-md px-2 py-1.5 focus:outline-none focus:border-slate-500"
                  >
                    <option value="hierarchy">Hierarchy (Levels)</option>
                    <option value="connections">Connections Count</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Sizing */}
            <div className="flex flex-col gap-2">
              <div className="text-[11px] font-semibold text-slate-500 uppercase tracking-widest mb-1">Sizing</div>
              <div className="bg-[#2a2f36] rounded-md p-3 flex flex-col gap-4 border border-slate-800">
                <div className="flex flex-col gap-2">
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-slate-300 tracking-wider">Node Size Multiplier</span>
                    <span className="text-xs text-slate-400 font-mono">{visualConfig.nodeSizeMultiplier}x</span>
                  </div>
                  <input 
                    type="range" 
                    min="0.1" max="3" step="0.1"
                    value={visualConfig.nodeSizeMultiplier}
                    onChange={(e) => setVisualConfig({...visualConfig, nodeSizeMultiplier: parseFloat(e.target.value)})}
                    className="w-full h-1.5 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-slate-400"
                  />
                </div>
              </div>
            </div>

            {/* Labels Section */}
            <div className="flex flex-col gap-2">
              <div className="text-[11px] font-semibold text-slate-500 uppercase tracking-widest mb-1">Labels</div>
              <div className="bg-[#2a2f36] rounded-md p-3 flex flex-col gap-4 border border-slate-800">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-slate-300">Show Node Labels</span>
                    <Info className="w-3.5 h-3.5 text-slate-500 cursor-help" title="Hiển thị tên trên các node" />
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
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-slate-300">Show Unselected Labels</span>
                  </div>
                  <button 
                    role="switch"
                    aria-checked={visualConfig.showUnselectedLabels}
                    onClick={() => setVisualConfig({...visualConfig, showUnselectedLabels: !visualConfig.showUnselectedLabels})}
                    className={`relative inline-flex h-4 w-7 items-center rounded-full transition-colors focus:outline-none ${visualConfig.showUnselectedLabels ? 'bg-slate-400' : 'bg-slate-600'}`}
                  >
                    <span className={`inline-block h-3 w-3 transform rounded-full bg-white transition-transform ${visualConfig.showUnselectedLabels ? 'translate-x-3.5' : 'translate-x-0.5'}`} />
                  </button>
                </div>
              </div>
            </div>

            {/* Hierarchy / Concepts Section */}
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

            {/* Link Appearance */}
            <div className="flex flex-col gap-2">
              <div className="text-[11px] font-semibold text-slate-500 uppercase tracking-widest mb-1">Link Appearance</div>
              <div className="bg-[#2a2f36] rounded-md p-3 flex flex-col gap-5 border border-slate-800">
                
                {/* Link Opacity */}
                <div className="flex flex-col gap-2">
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-slate-300 tracking-wider">Link Opacity</span>
                    <span className="text-xs text-slate-400 font-mono">{visualConfig.linkOpacity}</span>
                  </div>
                  <input 
                    type="range" 
                    min="0" max="1" step="0.05"
                    value={visualConfig.linkOpacity}
                    onChange={(e) => setVisualConfig({...visualConfig, linkOpacity: parseFloat(e.target.value)})}
                    className="w-full h-1.5 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-slate-400"
                  />
                </div>

                {/* Link Width */}
                <div className="flex flex-col gap-2">
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-slate-300 tracking-wider">Link Width</span>
                    <span className="text-xs text-slate-400 font-mono">{visualConfig.linkWidth}</span>
                  </div>
                  <input 
                    type="range" 
                    min="0.1" max="5" step="0.1"
                    value={visualConfig.linkWidth}
                    onChange={(e) => setVisualConfig({...visualConfig, linkWidth: parseFloat(e.target.value)})}
                    className="w-full h-1.5 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-slate-400"
                  />
                </div>
                
                {/* Particles */}
                <div className="flex items-center justify-between pt-2 border-t border-slate-700">
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-slate-300">Directional Particles</span>
                    <Info className="w-3.5 h-3.5 text-slate-500 cursor-help" title="Hiển thị luồng hạt di chuyển (Có thể giảm FPS)" />
                  </div>
                  <button 
                    role="switch"
                    aria-checked={visualConfig.showParticles}
                    onClick={() => setVisualConfig({...visualConfig, showParticles: !visualConfig.showParticles})}
                    className={`relative inline-flex h-4 w-7 items-center rounded-full transition-colors focus:outline-none ${visualConfig.showParticles ? 'bg-slate-400' : 'bg-slate-600'}`}
                  >
                    <span className={`inline-block h-3 w-3 transform rounded-full bg-white transition-transform ${visualConfig.showParticles ? 'translate-x-3.5' : 'translate-x-0.5'}`} />
                  </button>
                </div>
                
              </div>
            </div>

          </div>
        )}
        
        {activeTab === 'levels' && (
          <div className="flex flex-col gap-6">
            {/* Level Selector */}
            <div className="flex flex-col gap-2">
              <div className="text-[11px] font-semibold text-slate-500 uppercase tracking-widest mb-1">Target Level</div>
              <select 
                value={selectedLevel}
                onChange={(e) => setSelectedLevel(e.target.value)}
                className="w-full bg-[#2a2f36] border border-slate-700 text-slate-200 text-sm rounded-md px-3 py-2 focus:outline-none focus:border-slate-500 font-medium capitalize"
              >
                <option value="field">Field (Cấp 1)</option>
                <option value="subject">Subject (Cấp 2)</option>
                <option value="category">Category (Cấp 3)</option>
                <option value="topic">Topic (Cấp 4)</option>
                <option value="concept">Concept (Cấp 5)</option>
              </select>
            </div>

            {/* Text Configuration */}
            <div className="flex flex-col gap-2">
              <div className="text-[11px] font-semibold text-slate-500 uppercase tracking-widest mb-1">Text Appearance</div>
              <div className="bg-[#2a2f36] rounded-md p-3 flex flex-col gap-5 border border-slate-800">
                
                {/* Text Color */}
                <div className="flex items-center justify-between">
                  <span className="text-xs text-slate-300">Text Color</span>
                  <div className="flex items-center gap-2">
                    <input 
                      type="color" 
                      value={levelConfig[selectedLevel].textColor}
                      onChange={(e) => setLevelConfig({
                        ...levelConfig, 
                        [selectedLevel]: { ...levelConfig[selectedLevel], textColor: e.target.value }
                      })}
                      className="w-6 h-6 rounded cursor-pointer bg-transparent border-0 p-0"
                    />
                    <span className="text-xs text-slate-400 font-mono uppercase w-16">{levelConfig[selectedLevel].textColor}</span>
                  </div>
                </div>

                {/* Text Height */}
                <div className="flex flex-col gap-2">
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-slate-300">Text Size</span>
                    <span className="text-xs text-slate-400 font-mono">{levelConfig[selectedLevel].textHeight}</span>
                  </div>
                  <input 
                    type="range" 
                    min="1" max="15" step="0.5"
                    value={levelConfig[selectedLevel].textHeight}
                    onChange={(e) => setLevelConfig({
                      ...levelConfig, 
                      [selectedLevel]: { ...levelConfig[selectedLevel], textHeight: parseFloat(e.target.value) }
                    })}
                    className="w-full h-1.5 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-slate-400"
                  />
                </div>

                {/* Font Weight */}
                <div className="flex flex-col gap-2">
                  <span className="text-xs text-slate-300">Font Weight</span>
                  <select 
                    value={levelConfig[selectedLevel].textWeight}
                    onChange={(e) => setLevelConfig({
                      ...levelConfig, 
                      [selectedLevel]: { ...levelConfig[selectedLevel], textWeight: e.target.value }
                    })}
                    className="w-full bg-[#1a1d21] border border-slate-700 text-slate-200 text-xs rounded-md px-2 py-1.5 focus:outline-none focus:border-slate-500"
                  >
                    <option value="normal">Normal</option>
                    <option value="bold">Bold</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Node Configuration */}
            <div className="flex flex-col gap-2">
              <div className="text-[11px] font-semibold text-slate-500 uppercase tracking-widest mb-1">Node Appearance</div>
              <div className="bg-[#2a2f36] rounded-md p-3 flex flex-col gap-5 border border-slate-800">
                
                {/* Shape */}
                <div className="flex flex-col gap-2">
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-slate-300">Node Shape</span>
                    <Info className="w-3.5 h-3.5 text-slate-500 cursor-help" title="Chọn None để tắt Node Visual (Chỉ hiện chữ)" />
                  </div>
                  <select 
                    value={levelConfig[selectedLevel].shape}
                    onChange={(e) => setLevelConfig({
                      ...levelConfig, 
                      [selectedLevel]: { ...levelConfig[selectedLevel], shape: e.target.value }
                    })}
                    className="w-full bg-[#1a1d21] border border-slate-700 text-slate-200 text-xs rounded-md px-2 py-1.5 focus:outline-none focus:border-slate-500"
                  >
                    <option value="none">None (Text Only)</option>
                    <option value="sphere">Sphere (Khối Cầu)</option>
                    <option value="box">Box (Khối Lập Phương)</option>
                    <option value="tetrahedron">Tetrahedron (Tứ Diện)</option>
                    <option value="cylinder">Cylinder (Khối Trụ)</option>
                    <option value="dodecahedron">Dodecahedron (12 Mặt)</option>
                  </select>
                </div>

                {/* Opacity */}
                <div className="flex flex-col gap-2">
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-slate-300">Node Opacity</span>
                    <span className="text-xs text-slate-400 font-mono">{levelConfig[selectedLevel].opacity}</span>
                  </div>
                  <input 
                    type="range" 
                    min="0" max="1" step="0.1"
                    value={levelConfig[selectedLevel].opacity}
                    onChange={(e) => setLevelConfig({
                      ...levelConfig, 
                      [selectedLevel]: { ...levelConfig[selectedLevel], opacity: parseFloat(e.target.value) }
                    })}
                    className="w-full h-1.5 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-slate-400"
                  />
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
                    <span className="text-xs text-slate-400 font-mono">{Math.abs(visualConfig.charge)}</span>
                  </div>
                  <input 
                    type="range" 
                    min="10" max="1500" step="10"
                    value={Math.abs(visualConfig.charge)}
                    onChange={(e) => setVisualConfig({...visualConfig, charge: -parseInt(e.target.value)})}
                    className="w-full h-1.5 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-slate-400"
                  />
                </div>

                {/* Link Distance Slider */}
                <div className="flex flex-col gap-2">
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-slate-300 uppercase tracking-wider text-[10px]">Link Distance</span>
                    <span className="text-xs text-slate-400 font-mono">{visualConfig.linkDistance}</span>
                  </div>
                  <input 
                    type="range" 
                    min="5" max="300" step="5"
                    value={visualConfig.linkDistance}
                    onChange={(e) => setVisualConfig({...visualConfig, linkDistance: parseInt(e.target.value)})}
                    className="w-full h-1.5 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-slate-400"
                  />
                </div>
                
                {/* Center Gravity Slider */}
                <div className="flex flex-col gap-2">
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-slate-300 uppercase tracking-wider text-[10px]">Center Gravity</span>
                    <span className="text-xs text-slate-400 font-mono">{visualConfig.centerGravity}</span>
                  </div>
                  <input 
                    type="range" 
                    min="0" max="1" step="0.05"
                    value={visualConfig.centerGravity}
                    onChange={(e) => setVisualConfig({...visualConfig, centerGravity: parseFloat(e.target.value)})}
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
