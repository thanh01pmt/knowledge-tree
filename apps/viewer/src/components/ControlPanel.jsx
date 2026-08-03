import React, { useState, useMemo, useEffect, useRef } from 'react';
import { 
  Search, Settings2, BarChart3, RotateCcw, PanelLeftClose, 
  SlidersHorizontal, Palette, Layers, Zap, Eye, EyeOff,
  Filter, ChevronDown, ChevronUp, Database, GitBranch,
  Sparkles, HelpCircle, X, ChevronLeft, ChevronRight, Hash, Tag
} from 'lucide-react';

// Dynamic icon renderer for level-based icons
function IconRenderer({ icon: Icon, className, ...props }) {
  if (!Icon) return <div className={className} {...props} />;
  return <Icon className={className} {...props} />;
}

const LEVEL_ICONS = {
  field: Database,
  subject: GitBranch,
  category: Layers,
  topic: Filter,
  concept: Sparkles,
  learning_objective: HelpCircle,
  keyword: Zap,
};

const LEVEL_LABELS = {
  field: 'Field (Ngành)',
  subject: 'Subject (Môn)',
  category: 'Category (Danh mục)',
  topic: 'Topic (Chủ đề)',
  concept: 'Concept (Khái niệm)',
  learning_objective: 'Learning Objective',
  keyword: 'Keyword',
};

const LEVEL_ORDER = ['field', 'subject', 'category', 'topic', 'concept', 'learning_objective', 'keyword'];

const Badge = ({ children, variant = 'slate', className = '' }) => {
  const variants = {
    cyan: 'bg-electric-cyan/20 text-electric-cyan border-electric-cyan/30',
    amber: 'bg-electric-amber/20 text-electric-amber border-electric-amber/30',
    magenta: 'bg-electric-magenta/20 text-electric-magenta border-electric-magenta/30',
    green: 'bg-electric-green/20 text-electric-green border-electric-green/30',
    slate: 'bg-space-700 text-text-secondary border-border-default',
    purple: 'bg-electric-magenta/20 text-electric-magenta border-electric-magenta/30',
  };
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider border ${variants[variant] || variants.slate} ${className}`}>
      {children}
    </span>
  );
};

export default function ControlPanel({ 
  nodes, 
  onNodeSearch, 
  filters, 
  setFilters,
  visualConfig,
  setVisualConfig,
  levelConfig,
  setLevelConfig,
  onReset,
  onSearchMatchesChange,
  onOpenDashboard
}) {
  const [activeTab, setActiveTab] = useState('elements');
  const [selectedLevel, setSelectedLevel] = useState('field');
  const [searchTerm, setSearchTerm] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [expandedSections, setExpandedSections] = useState({
    search: true,
    coloring: true,
    sizing: true,
    labels: true,
    hierarchy: true,
    links: true,
  });
  const searchRef = useRef();
  const suggestionsRef = useRef();

  const matchingNodeIds = useMemo(() => {
    if (!searchTerm || searchTerm.trim().length < 2) return new Set();
    const term = searchTerm.toLowerCase();
    const matches = nodes
      .filter(n => 
        n.name.toLowerCase().includes(term) || 
        (n.description && n.description.toLowerCase().includes(term)) ||
        (n.id && n.id.toLowerCase().includes(term))
      )
      .map(n => n.id);
    return new Set(matches);
  }, [searchTerm, nodes]);

  useEffect(() => {
    onSearchMatchesChange?.(matchingNodeIds);
  }, [matchingNodeIds, onSearchMatchesChange]);

  const suggestions = useMemo(() => {
    if (!searchTerm || searchTerm.trim().length < 2) return [];
    const term = searchTerm.toLowerCase();
    return nodes
      .filter(n => 
        n.name.toLowerCase().includes(term) || 
        (n.description && n.description.toLowerCase().includes(term)) ||
        (n.id && n.id.toLowerCase().includes(term))
      )
      .slice(0, 10);
  }, [searchTerm, nodes]);


  const handleSelect = (node) => {
    onNodeSearch(node);
    setSearchTerm(node.name);
    setShowSuggestions(false);
  };

  const toggleSection = (section) => {
    setExpandedSections(prev => ({ ...prev, [section]: !prev[section] }));
  };

  const Section = ({ title, icon: Icon, children, sectionKey, className = '' }) => {
    const isExpanded = expandedSections[sectionKey];
    return (
      <div className={`panel-border rounded-xl overflow-hidden transition-all duration-300 ${className}`}>
        <button
          onClick={() => toggleSection(sectionKey)}
          className="w-full flex items-center justify-between p-3 bg-space-750/50 hover:bg-space-750 transition-colors"
          aria-expanded={isExpanded}
        >
          <div className="flex items-center gap-2">
            <Icon className="w-4 h-4 text-electric-cyan" />
            <span className="text-xs font-semibold text-text-secondary uppercase tracking-widest">{title}</span>
          </div>
          <div className="flex items-center gap-2 text-text-muted">
            {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </div>
        </button>
        {isExpanded && (
          <div className="p-4 animate-slide-down" style={{ animationDuration: '0.3s' }}>
            {children}
          </div>
        )}
      </div>
    );
  };

  const Slider = ({ label, value, min, max, step, onChange, unit = '', format = (v) => v }) => (
    <div className="flex flex-col gap-2">
      <div className="flex justify-between items-center">
        <label className="text-xs text-text-secondary tracking-wider">{label}</label>
        <span className="text-xs text-text-dim font-mono">{format(value)}{unit}</span>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        className="w-full h-1.5 bg-space-700 rounded-lg appearance-none cursor-pointer accent-electric-cyan"
        aria-label={label}
      />
    </div>
  );

  const Toggle = ({ label, checked, onChange, icon: Icon, helpText }) => (
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-2">
        {Icon && <Icon className="w-3.5 h-3.5 text-text-muted" />}
        <span className="text-xs text-text-secondary">{label}</span>
        {helpText && <HelpCircle className="w-3.5 h-3.5 text-text-muted cursor-help" title={helpText} />}
      </div>
      <button
        role="switch"
        aria-checked={checked}
        onClick={onChange}
        className={`relative inline-flex h-4 w-7 items-center rounded-full transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-electric-cyan/50 ${
          checked ? 'bg-electric-cyan shadow-[0_0_8px_rgba(0,245,255,0.4)]' : 'bg-space-600'
        }`}
      >
        <span className={`inline-block h-3 w-3 transform rounded-full bg-white transition-transform duration-200 ${
          checked ? 'translate-x-3.5' : 'translate-x-0.5'
        }`} />
      </button>
    </div>
  );

  const Select = ({ value, onChange, options, className = '' }) => (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className={`w-full bg-space-800 border border-border-default text-text-primary text-xs rounded-lg px-3 py-2 focus:outline-none focus:border-electric-cyan focus:ring-2 focus:ring-electric-cyan/20 transition-all ${className}`}
    >
      {options.map(opt => (
        <option key={opt.value} value={opt.value}>{opt.label}</option>
      ))}
    </select>
  );

  if (isCollapsed) {
    return (
      <div className="h-full w-12 bg-space-800/95 border-r border-border-subtle flex flex-col items-center justify-between z-10 transition-all duration-300 flex-shrink-0 glass-strong">
        <div className="p-3">
          <button
            onClick={() => setIsCollapsed(false)}
            className="w-full p-2 text-text-muted hover:text-electric-cyan rounded-lg hover:bg-space-700 transition-colors"
            title="Expand Panel"
          >
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>
        <div className="p-3 space-y-2">
          <button
            onClick={onReset}
            className="w-full p-2 text-text-muted hover:text-text-primary rounded-lg hover:bg-space-700 transition-colors"
            title="Reset to defaults"
          >
            <RotateCcw className="w-5 h-5" />
          </button>
          {onOpenDashboard && (
            <button
              onClick={onOpenDashboard}
              className="w-full p-2 text-text-muted hover:text-electric-amber rounded-lg hover:bg-space-700 transition-colors"
              title="Curriculum Analytics Dashboard"
            >
              <BarChart3 className="w-5 h-5" />
            </button>
          )}
        </div>
        <div className="p-3 text-center">
          <span className="text-[9px] font-mono text-text-dim writing-vertical text-right">KNOWLEDGE TREE</span>
        </div>
      </div>
    );
  }

  const tabs = [
    { key: 'elements', label: 'Elements', icon: SlidersHorizontal },
    { key: 'levels', label: 'Levels', icon: Layers },
    { key: 'simulation', label: 'Physics', icon: Zap },
    { key: 'visualization', label: 'Keywords', icon: Hash },
    { key: 'search', label: 'Search', icon: Search },
  ];

  return (
    <div className="h-full w-[340px] bg-space-900/95 border-r border-border-subtle flex flex-col text-text-primary z-10 transition-all duration-300 flex-shrink-0 glass-strong relative overflow-hidden">
      {/* Animated border glow */}
      <div className="absolute top-0 right-0 bottom-0 w-px bg-gradient-to-b from-electric-cyan/50 via-transparent to-electric-magenta/50 animate-pulse-glow" />
      
      {/* Header */}
      <div className="flex items-center justify-between p-3 border-b border-border-subtle flex-shrink-0 relative z-10">
        <div className="flex items-center gap-2">
          <Settings2 className="w-4 h-4 text-electric-cyan" />
          <h2 className="text-[11px] font-display font-semibold text-text-secondary uppercase tracking-widest">Graph Configuration</h2>
        </div>
        <div className="flex items-center gap-1">
          {onOpenDashboard && (
            <button
              onClick={onOpenDashboard}
              className="btn-icon text-text-muted hover:text-electric-amber hover:bg-space-750"
              title="Curriculum Analytics Dashboard"
            >
              <BarChart3 className="w-4 h-4" />
            </button>
          )}
          <button
            onClick={onReset}
            className="btn-icon text-text-muted hover:text-text-primary hover:bg-space-750"
            title="Reset to defaults"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
          <button
            onClick={() => setIsCollapsed(true)}
            className="btn-icon text-text-muted hover:text-text-primary hover:bg-space-750"
            title="Collapse Panel"
          >
            <PanelLeftClose className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex px-3 py-2 border-b border-border-subtle flex-shrink-0 relative z-10">
        {tabs.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            className={`flex-1 flex items-center justify-center gap-1.5 px-2 py-2 text-[10px] font-semibold uppercase tracking-widest transition-all duration-200 rounded-lg relative ${
              activeTab === tab.key
                ? 'text-electric-cyan bg-electric-cyan/10'
                : 'text-text-muted hover:text-text-secondary hover:bg-space-750'
            }`}
            aria-current={activeTab === tab.key ? 'page' : undefined}
          >
            <tab.icon className="w-3.5 h-3.5" />
            {tab.label}
          </button>
        ))}
        {/* Active tab indicator */}
        {activeTab && (
          <div
            className="absolute bottom-0 left-0 h-0.5 bg-electric-cyan rounded-full transition-transform duration-300 ease-out"
            style={{
              width: `${100 / tabs.length}%`,
              transform: `translateX(${tabs.findIndex(t => t.key === activeTab) * (100 / tabs.length)}%)`,
            }}
          />
        )}
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-3 custom-scrollbar relative z-10">
        {/* ELEMENTS TAB */}
        {activeTab === 'elements' && (
          <div className="flex flex-col gap-4 animate-fade-in">
            {/* Search Section */}
            <Section
              title="Search"
              icon={Search}
              sectionKey="search"
              className="glow-cyan"
            >
              <div className="flex flex-col gap-2">
                <div className="relative" ref={searchRef}>
                  <div className="relative flex items-center">
                    <Search className="absolute left-3 w-4 h-4 text-text-muted" />
                    <input
                      type="text"
                      className="input pl-10 pr-3"
                      placeholder="Search by name, ID, or description..."
                      value={searchTerm}
                      onChange={(e) => {
                        setSearchTerm(e.target.value);
                        setShowSuggestions(true);
                      }}
                      onFocus={() => setShowSuggestions(true)}
                      aria-label="Search nodes"
                    />
                    {searchTerm && (
                      <button
                        onClick={() => setSearchTerm('')}
                        className="absolute right-3 text-text-muted hover:text-electric-cyan transition-colors"
                        aria-label="Clear search"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    )}
                  </div>
                  {showSuggestions && suggestions.length > 0 && (
                    <div className="absolute top-full left-0 right-0 mt-1 panel rounded-xl shadow-elevation-3 overflow-hidden z-50 animate-scale-in">
                      {suggestions.map(node => (
                        <button
                          key={node.id}
                          onClick={() => handleSelect(node)}
                          className="w-full px-3 py-2.5 hover:bg-space-700 transition-colors flex items-center gap-3 text-left border-b border-border-subtle/50 last:border-0"
                        >
                          <IconRenderer icon={LEVEL_ICONS[node.level]} className="w-4 h-4 text-electric-cyan flex-shrink-0" />
                          <div className="flex-1 min-w-0">
                            <div className="text-text-primary text-sm font-medium truncate">{node.name}</div>
                            <div className="flex items-center gap-1.5 mt-0.5">
                              <span className="badge-cyan text-[9px]">{LEVEL_LABELS[node.level] || node.level}</span>
                              {node.cs2023_ka && (
                                <span className="badge-magenta text-[9px]">{node.cs2023_ka}</span>
                              )}
                            </div>
                          </div>
                          <ChevronRight className="w-4 h-4 text-text-muted" />
                        </button>
                      ))}
                      {suggestions.length === 10 && (
                        <div className="px-3 py-2 text-center text-xs text-text-muted border-t border-border-subtle">
                          Showing top 10 results
                        </div>
                      )}
                    </div>
                  )}
                </div>
                <div className="text-[10px] text-text-dim text-center">
                  {matchingNodeIds.size > 0 ? (
                    <>
                      <span className="font-mono text-electric-cyan">{matchingNodeIds.size}</span> matches found
                    </>
                  ) : (
                    'Type to search...'
                  )}
                </div>
              </div>
            </Section>

            {/* Coloring */}
            <Section
              title="Coloring"
              icon={Palette}
              sectionKey="coloring"
            >
              <div className="flex flex-col gap-3">
                <div>
                  <label className="label">Coloring Strategy</label>
                  <Select
                    value={visualConfig.coloringStrategy}
                    onChange={(v) => setVisualConfig({ ...visualConfig, coloringStrategy: v })}
                    options={[
                      { value: 'hierarchy', label: 'Hierarchy (by Level)' },
                      { value: 'connections', label: 'Connections Count' },
                      { value: 'cs2023', label: 'CS2023 Knowledge Areas' },
                    ]}
                  />
                </div>
              </div>
            </Section>

            {/* Sizing */}
            <Section
              title="Sizing"
              icon={Layers}
              sectionKey="sizing"
            >
              <Slider
                label="Node Size Multiplier"
                value={visualConfig.nodeSizeMultiplier}
                min={0.1}
                max={3}
                step={0.1}
                format={(v) => v.toFixed(1)}
                onChange={(v) => setVisualConfig({ ...visualConfig, nodeSizeMultiplier: v })}
                unit="x"
              />
            </Section>

            {/* Labels */}
            <Section
              title="Labels"
              icon={Eye}
              sectionKey="labels"
            >
              <Toggle
                label="Show Node Labels"
                checked={filters.showLabels}
                onChange={() => setFilters({ ...filters, showLabels: !filters.showLabels })}
                icon={Eye}
                helpText="Toggle node name labels on the graph"
              />
              <div className="pt-2 border-t border-border-subtle" />
              <Toggle
                label="Show Unselected Labels"
                checked={visualConfig.showUnselectedLabels}
                onChange={() => setVisualConfig({ ...visualConfig, showUnselectedLabels: !visualConfig.showUnselectedLabels })}
                icon={EyeOff}
                helpText="Show labels for non-hovered nodes"
              />
            </Section>

            {/* Hierarchy View */}
            <Section
              title="Hierarchy View"
              icon={GitBranch}
              sectionKey="hierarchy"
            >
              <div className="flex flex-col gap-3">
                <div>
                  <label className="label">Max Render Level</label>
                  <Select
                    value={filters.maxLevel || 'topic'}
                    onChange={(v) => setFilters({ ...filters, maxLevel: v })}
                    options={[
                      { value: 'field', label: '1. Field (Ngành)' },
                      { value: 'subject', label: '2. Subject (Môn)' },
                      { value: 'category', label: '3. Category (Danh mục)' },
                      { value: 'topic', label: '4. Topic (Chủ đề)' },
                      { value: 'concept', label: '5. Concept (Khái niệm)' },
                      { value: 'learning_objective', label: '6. Learning Objective' },
                      { value: 'keyword', label: '7. Keyword' },
                    ]}
                  />
                </div>
                <div className="pt-2 border-t border-border-subtle" />
                <Toggle
                  label="Show Prerequisites"
                  checked={filters.showPrerequisites}
                  onChange={() => setFilters({ ...filters, showPrerequisites: !filters.showPrerequisites })}
                  icon={Filter}
                  helpText="Show prerequisite chains when clicking a concept (Red = requires, Green = unlocks)"
                />
              </div>
            </Section>

            {/* Link Appearance */}
            <Section
              title="Link Appearance"
              icon={Zap}
              sectionKey="links"
            >
              <Slider
                label="Link Opacity"
                value={visualConfig.linkOpacity}
                min={0}
                max={1}
                step={0.05}
                format={(v) => v.toFixed(2)}
                onChange={(v) => setVisualConfig({ ...visualConfig, linkOpacity: v })}
              />
              <Slider
                label="Link Width"
                value={visualConfig.linkWidth}
                min={0.1}
                max={5}
                step={0.1}
                format={(v) => v.toFixed(1)}
                onChange={(v) => setVisualConfig({ ...visualConfig, linkWidth: v })}
                unit="px"
              />
              <div className="pt-2 border-t border-border-subtle" />
              <Toggle
                label="Directional Particles"
                checked={visualConfig.showParticles}
                onChange={() => setVisualConfig({ ...visualConfig, showParticles: !visualConfig.showParticles })}
                icon={Zap}
                helpText="Show animated particles flowing along links (may reduce FPS)"
              />
            </Section>
          </div>
        )}

        {/* LEVELS TAB */}
        {activeTab === 'levels' && (
          <div className="flex flex-col gap-4 animate-fade-in">
            {/* Level Selector */}
            <Section
              title="Target Level"
              icon={Layers}
              sectionKey="levelSelector"
            >
              <Select
                value={selectedLevel}
                onChange={(v) => setSelectedLevel(v)}
                options={[
                  { value: 'field', label: 'Field (Cấp 1)' },
                  { value: 'subject', label: 'Subject (Cấp 2)' },
                  { value: 'category', label: 'Category (Cấp 3)' },
                  { value: 'topic', label: 'Topic (Cấp 4)' },
                  { value: 'concept', label: 'Concept (Cấp 5)' },
                  { value: 'learning_objective', label: 'Learning Objective' },
                  { value: 'keyword', label: 'Keyword' },
                ]}
                className="font-medium capitalize"
              />
            </Section>

            {/* Text Appearance */}
            <Section
              title="Text Appearance"
              icon={Palette}
              sectionKey="textAppearance"
            >
              <div className="flex flex-col gap-4">
                <div className="flex items-center justify-between">
                  <label className="label mb-0">Text Color</label>
                  <div className="flex items-center gap-2">
                    <input
                      type="color"
                      value={levelConfig[selectedLevel]?.textColor || '#888888'}
                      onChange={(e) => setLevelConfig({
                        ...levelConfig,
                        [selectedLevel]: { ...levelConfig[selectedLevel], textColor: e.target.value }
                      })}
                      className="w-8 h-8 rounded cursor-pointer bg-transparent border-0 p-0"
                      aria-label="Text color picker"
                    />
                    <span className="text-xs text-text-dim font-mono uppercase w-16 text-center">
                      {levelConfig[selectedLevel]?.textColor || '#888888'}
                    </span>
                  </div>
                </div>
                
                <Slider
                  label="Text Size"
                  value={levelConfig[selectedLevel]?.textHeight || 5}
                  min={1}
                  max={15}
                  step={0.5}
                  onChange={(v) => setLevelConfig({
                    ...levelConfig,
                    [selectedLevel]: { ...levelConfig[selectedLevel], textHeight: v }
                  })}
                />
                
                <div>
                  <label className="label">Font Weight</label>
                  <Select
                    value={levelConfig[selectedLevel]?.textWeight || 'normal'}
                    onChange={(v) => setLevelConfig({
                      ...levelConfig,
                      [selectedLevel]: { ...levelConfig[selectedLevel], textWeight: v }
                    })}
                    options={[
                      { value: 'normal', label: 'Normal' },
                      { value: 'bold', label: 'Bold' },
                    ]}
                  />
                </div>
              </div>
            </Section>

            {/* Node Appearance */}
            <Section
              title="Node Appearance"
              icon={Sparkles}
              sectionKey="nodeAppearance"
            >
              <div className="flex flex-col gap-4">
                <div>
                  <label className="label">Node Shape</label>
                  <Select
                    value={levelConfig[selectedLevel]?.shape || 'sphere'}
                    onChange={(v) => setLevelConfig({
                      ...levelConfig,
                      [selectedLevel]: { ...levelConfig[selectedLevel], shape: v }
                    })}
                    options={[
                      { value: 'none', label: 'None (Text Only)' },
                      { value: 'sphere', label: 'Sphere (Khối Cầu)' },
                      { value: 'box', label: 'Box (Khối Lập Phương)' },
                      { value: 'tetrahedron', label: 'Tetrahedron (Tứ Diện)' },
                      { value: 'cylinder', label: 'Cylinder (Khối Trụ)' },
                      { value: 'dodecahedron', label: 'Dodecahedron (12 Mặt)' },
                    ]}
                  />
                </div>
                
                <Slider
                  label="Node Opacity"
                  value={levelConfig[selectedLevel]?.opacity || 0.8}
                  min={0}
                  max={1}
                  step={0.05}
                  format={(v) => v.toFixed(2)}
                  onChange={(v) => setLevelConfig({
                    ...levelConfig,
                    [selectedLevel]: { ...levelConfig[selectedLevel], opacity: v }
                  })}
                />
              </div>
            </Section>

            {/* Quick Stats */}
            <Section
              title="Level Statistics"
              icon={BarChart3}
              sectionKey="levelStats"
            >
              <div className="grid grid-cols-2 gap-2">
                {LEVEL_ORDER.map(level => (
                  <button
                    key={level}
                    onClick={() => setSelectedLevel(level)}
                    className={`panel p-2 rounded-lg text-left transition-all ${
                      selectedLevel === level
                        ? 'bg-electric-cyan/10 border-electric-cyan/30'
                        : 'hover:bg-space-750'
                    }`}
                  >
                    <div className="flex items-center gap-1.5">
                      <IconRenderer icon={LEVEL_ICONS[level]} className="w-4 h-4 text-electric-cyan" />
                      <span className="text-xs font-medium text-text-secondary truncate">
                        {LEVEL_LABELS[level]}
                      </span>
                    </div>
                    <div className="mt-1">
                      <span className="text-[10px] font-mono text-electric-cyan">
                        {nodes.filter(n => n.level === level).length}
                      </span>
                      <span className="text-[10px] text-text-muted ml-1">nodes</span>
                    </div>
                  </button>
                ))}
              </div>
            </Section>
          </div>
        )}

        {/* SIMULATION TAB */}
        {activeTab === 'simulation' && (
          <div className="flex flex-col gap-4 animate-fade-in">
            <Section
              title="Force Simulation"
              icon={Zap}
              sectionKey="forces"
            >
              <Slider
                label="Repel Force (Charge)"
                value={Math.abs(visualConfig.charge || 80)}
                min={10}
                max={1500}
                step={10}
                onChange={(v) => setVisualConfig({ ...visualConfig, charge: -v })}
              />
              <Slider
                label="Link Distance"
                value={visualConfig.linkDistance || 15}
                min={5}
                max={300}
                step={5}
                onChange={(v) => setVisualConfig({ ...visualConfig, linkDistance: v })}
                unit="px"
              />
              <Slider
                label="Center Gravity"
                value={visualConfig.centerGravity || 0.5}
                min={0}
                max={1}
                step={0.05}
                format={(v) => v.toFixed(2)}
                onChange={(v) => setVisualConfig({ ...visualConfig, centerGravity: v })}
              />
            </Section>

            <Section
              title="Actions"
              icon={RotateCcw}
              sectionKey="actions"
            >
              <div className="flex flex-col gap-2">
                <button
                  onClick={() => {
                    if (window.fgRef?.current) {
                      window.fgRef.current.d3ReheatSimulation();
                    }
                  }}
                  className="btn-secondary w-full justify-start gap-2"
                >
                  <RotateCcw className="w-4 h-4" />
                  <span>Reheat Simulation</span>
                </button>
                <button
                  onClick={() => {
                    if (window.fgRef?.current) {
                      window.fgRef.current.zoomToFit(400);
                    }
                  }}
                  className="btn-secondary w-full justify-start gap-2"
                >
                  <Zap className="w-4 h-4" />
                  <span>Zoom to Fit</span>
                </button>
              </div>
            </Section>
          </div>
        )}

        {/* SEARCH TAB - Advanced */}
        {activeTab === 'search' && (
          <div className="flex flex-col gap-4 animate-fade-in">
            <Section
              title="Advanced Search"
              icon={Search}
              sectionKey="advSearch"
            >
              <div className="flex flex-col gap-3">
                <div>
                  <label className="label">Filter by CS2023 KA</label>
                  <Select
                    value="all"
                    onChange={() => {}}
                    options={[
                      { value: 'all', label: 'All Knowledge Areas' },
                      { value: 'AL', label: 'AL - Algorithms' },
                      { value: 'AI', label: 'AI - Artificial Intelligence' },
                      { value: 'AR', label: 'AR - Architecture' },
                      { value: 'DM', label: 'DM - Data Management' },
                      { value: 'FPL', label: 'FPL - Programming Languages' },
                      { value: 'GIT', label: 'GIT - Graphics' },
                      { value: 'HCI', label: 'HCI - Human-Computer Interaction' },
                      { value: 'MSF', label: 'MSF - Mathematical Foundations' },
                      { value: 'NC', label: 'NC - Networking' },
                      { value: 'OS', label: 'OS - Operating Systems' },
                      { value: 'PDC', label: 'PDC - Parallel Computing' },
                      { value: 'SE', label: 'SE - Software Engineering' },
                      { value: 'SDF', label: 'SDF - Software Dev Fundamentals' },
                      { value: 'SF', label: 'SF - Systems Fundamentals' },
                      { value: 'SPD', label: 'SPD - Specialized Platform Dev' },
                    ]}
                  />
                </div>
                <div>
                  <label className="label">Filter by Bloom Level</label>
                  <Select
                    value="all"
                    onChange={() => {}}
                    options={[
                      { value: 'all', label: 'All Levels' },
                      { value: 'REMEMBER', label: 'Remember' },
                      { value: 'UNDERSTAND', label: 'Understand' },
                      { value: 'APPLY', label: 'Apply' },
                      { value: 'ANALYZE', label: 'Analyze' },
                      { value: 'EVALUATE', label: 'Evaluate' },
                      { value: 'CREATE', label: 'Create' },
                    ]}
                  />
                </div>
                <div>
                  <label className="label">Filter by Knowledge Dimension</label>
                  <Select
                    value="all"
                    onChange={() => {}}
                    options={[
                      { value: 'all', label: 'All Dimensions' },
                      { value: 'FACTUAL', label: 'Factual' },
                      { value: 'CONCEPTUAL', label: 'Conceptual' },
                      { value: 'PROCEDURAL', label: 'Procedural' },
                      { value: 'METACOGNITIVE', label: 'Metacognitive' },
                    ]}
                  />
                </div>
                <div className="pt-2 border-t border-border-subtle">
                  <button className="btn-primary w-full justify-center gap-2">
                    <Search className="w-4 h-4" />
                    <span>Apply Filters</span>
                  </button>
                </div>
              </div>
            </Section>
          </div>
        )}

        {/* VISUALIZATION TAB - Keywords */}
        {activeTab === 'visualization' && (
          <div className="flex flex-col gap-4 animate-fade-in">
            <Section
              title="Keyword Visualization"
              icon={Hash}
              sectionKey="kwViz"
            >
              <div className="flex flex-col gap-3">
                <div>
                  <label className="label">Visualization Mode</label>
                  <Select
                    value="concept-cloud"
                    onChange={() => {}}
                    options={[
                      { value: 'concept-cloud', label: 'Concept Keyword Cloud' },
                      { value: 'level-distribution', label: 'Keywords by Level' },
                      { value: 'concept-coverage', label: 'Coverage Heatmap' },
                      { value: 'token-frequency', label: 'Token Frequency' },
                    ]}
                  />
                </div>
                <div className="pt-2 border-t border-border-subtle">
                  <button className="btn-primary w-full justify-center gap-2">
                    <Hash className="w-4 h-4" />
                    <span>Open Keyword Explorer</span>
                  </button>
                </div>
              </div>
            </Section>

            <Section
              title="Quick Keyword Stats"
              icon={BarChart3}
              sectionKey="kwStats"
            >
              <div className="grid grid-cols-2 gap-2">
                <div className="panel p-3 rounded-lg">
                  <div className="text-[10px] font-semibold text-text-muted uppercase tracking-wider mb-1">Total Keywords</div>
                  <div className="text-2xl font-display font-bold text-electric-cyan">1,169</div>
                </div>
                <div className="panel p-3 rounded-lg">
                  <div className="text-[10px] font-semibold text-text-muted uppercase tracking-wider mb-1">Concepts Covered</div>
                  <div className="text-2xl font-display font-bold text-electric-green">268/269</div>
                </div>
                <div className="panel p-3 rounded-lg">
                  <div className="text-[10px] font-semibold text-text-muted uppercase tracking-wider mb-1">Keyword Links</div>
                  <div className="text-2xl font-display font-bold text-electric-amber">2,113</div>
                </div>
                <div className="panel p-3 rounded-lg">
                  <div className="text-[10px] font-semibold text-text-muted uppercase tracking-wider mb-1">Avg per Concept</div>
                  <div className="text-2xl font-display font-bold text-electric-magenta">7.9</div>
                </div>
              </div>
            </Section>

            <Section
              title="Top Keywords by Concept"
              icon={Tag}
              sectionKey="topKeywords"
            >
              <div className="space-y-2 max-h-64 overflow-y-auto custom-scrollbar">
                {[
                  { concept: 'PRIMITIVE_TYPE_DECLARATION', keywords: ['var', 'let', 'const', 'int', 'float', 'bool', 'string'] },
                  { concept: 'FIRST_CLASS_FUNCTIONS_CONCEPT', keywords: ['function', 'lambda', 'arrow', 'async', 'await', 'callback'] },
                  { concept: 'CLASS_DEFINITION', keywords: ['class', 'interface', 'implements', 'extends', 'constructor', 'this'] },
                  { concept: 'ASYNCHRONOUS_PROG_CONCEPT', keywords: ['async', 'await', 'promise', 'then', 'catch', 'finally'] },
                  { concept: 'ACCESS_MODIFIERS', keywords: ['public', 'private', 'protected', 'internal', 'static', 'readonly'] },
                ].map((item, idx) => (
                  <div key={idx} className="panel p-3 rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs font-semibold text-electric-cyan uppercase tracking-wider truncate max-w-[200px]">
                        {item.concept}
                      </span>
                      <Badge variant="cyan" className="text-[9px]">{item.keywords.length} tokens</Badge>
                    </div>
                    <div className="flex flex-wrap gap-1.5">
                      {item.keywords.map(kw => (
                        <span key={kw} className="badge-slate hover:bg-electric-cyan/10 hover:text-electric-cyan transition-colors cursor-default">
                          {kw}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </Section>
          </div>
        )}

        {/* SEARCH TAB */}

      </div>

      {/* Footer */}
      <div className="p-3 border-t border-border-subtle flex justify-between items-center text-[10px] font-mono text-text-dim relative z-10">
        <span>{nodes.length} nodes</span>
        <span className="opacity-50">Knowledge Tree v3.5</span>
      </div>
    </div>
  );
}