import React, { useMemo, useEffect, useState } from 'react';
import { 
  ChevronRight, ArrowLeft, ArrowRight, ChevronLeft, 
  LayoutGrid, Layers, Hexagon, Circle, Square, Minus, 
  Map as MapIcon, Hash, Target, X, BookOpen, Tag, 
  Link2, Eye, ExternalLink, Copy, Info, Sparkles,
  ChevronDown, ChevronUp
} from 'lucide-react';

const LEVEL_ICONS = {
  field: MapIcon,
  subject: Layers,
  category: LayoutGrid,
  topic: Hexagon,
  concept: Circle,
  keyword: Hash,
  learning_objective: BookOpen,
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

const LEVEL_COLORS = {
  field: 'electric-cyan',
  subject: 'electric-green',
  category: 'electric-amber',
  topic: 'text-text-secondary',
  concept: 'text-text-muted',
  learning_objective: 'electric-magenta',
  keyword: 'electric-magenta',
};

function IconRenderer({ icon: Icon, className, ...props }) {
  if (!Icon) return <div className={className} {...props} />;
  return <Icon className={className} {...props} />;
}

const Section = ({ title, icon: Icon, children, isOpen = true, onToggle }) => (
  <div className="panel-border rounded-xl overflow-hidden">
    <button
      onClick={onToggle}
      className="w-full flex items-center justify-between p-3 bg-space-750/50 hover:bg-space-750 transition-colors"
      aria-expanded={isOpen}
    >
      <div className="flex items-center gap-2">
        <Icon className="w-4 h-4 text-electric-cyan" />
        <span className="text-xs font-semibold text-text-secondary uppercase tracking-widest">{title}</span>
      </div>
      <div className="flex items-center gap-2 text-text-muted">
        {isOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
      </div>
    </button>
    {isOpen && (
      <div className="p-4 animate-slide-down" style={{ animationDuration: '0.25s' }}>
        {children}
      </div>
    )}
  </div>
);

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
    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider border ${variants[variant]} ${className}`}>
      {children}
    </span>
  );
};

const MetadataRow = ({ label, value, icon: Icon }) => (
  <div className="flex items-center gap-2 py-1.5">
    {Icon && <Icon className="w-4 h-4 text-text-muted flex-shrink-0" />}
    <span className="text-[10px] font-semibold text-text-muted uppercase tracking-wider w-24 flex-shrink-0">{label}</span>
    <span className="text-sm font-medium text-text-primary truncate flex-1">{value}</span>
  </div>
);

export default function NodeDetailsPanel({
  selectedNode,
  onNodeSelect,
  graphData,
  linksBySource,
  linksByTarget,
  history,
  historyIndex,
  onNavigateHistory,
  isolatedNodeId,
  setIsolatedNodeId,
  keywords = [],
}) {
  const [expandedSections, setExpandedSections] = useState({
    overview: true,
    metadata: true,
    keywords: true,
    prerequisites: true,
    children: true,
    siblings: true,
  });

  const toggleSection = (key) => {
    setExpandedSections(prev => ({ ...prev, [key]: !prev[key] }));
  };

  // Early return if no node selected
  if (!selectedNode) return null;

  // Fast O(1) node lookup map
  const nodeMap = useMemo(() => {
    const map = new Map();
    graphData?.nodes?.forEach(node => map.set(node.id, node));
    return map;
  }, [graphData]);

  const breadcrumbs = useMemo(() => {
    if (!selectedNode) return [];
    const crumbs = [];
    let current = selectedNode;
    while (current && linksByTarget[current.id]?.length) {
      const parentId = linksByTarget[current.id][0];
      const parent = nodeMap.get(parentId);
      if (parent) {
        crumbs.unshift(parent);
        current = parent;
      } else break;
    }
    return crumbs;
  }, [selectedNode, linksByTarget, nodeMap]);

  const { prevSibling, nextSibling } = useMemo(() => {
    if (!selectedNode || !linksByTarget[selectedNode.id]?.length) return { prevSibling: null, nextSibling: null };
    const parentId = linksByTarget[selectedNode.id][0];
    const siblings = linksBySource[parentId] || [];
    const idx = siblings.indexOf(selectedNode.id);
    if (idx === -1) return { prevSibling: null, nextSibling: null };
    return {
      prevSibling: idx > 0 ? nodeMap.get(siblings[idx - 1]) : null,
      nextSibling: idx < siblings.length - 1 ? nodeMap.get(siblings[idx + 1]) : null,
    };
  }, [selectedNode, linksByTarget, linksBySource, nodeMap]);

  const children = useMemo(() => {
    if (!selectedNode) return [];
    return (linksBySource[selectedNode.id] || [])
      .map(id => nodeMap.get(id))
      .filter(Boolean);
  }, [selectedNode, linksBySource, nodeMap]);

  // Find prerequisites for this node
  const prerequisites = useMemo(() => {
    if (!selectedNode) return { incoming: [], outgoing: [] };
    const incoming = (linksByTarget[selectedNode.id] || [])
      .map(id => nodeMap.get(id))
      .filter(Boolean);
    const outgoing = (linksBySource[selectedNode.id] || [])
      .map(id => nodeMap.get(id))
      .filter(Boolean);
    return { incoming, outgoing };
  }, [selectedNode, linksBySource, linksByTarget, nodeMap]);

  // Find keywords for this concept
  const nodeKeywords = useMemo(() => {
    if (!keywords.length || !selectedNode) return [];
    return keywords
      .filter(kw => {
        try {
          const conceptCodes = JSON.parse(kw.concept_codes || '[]');
          return conceptCodes.includes(selectedNode.id);
        } catch {
          return false;
        }
      })
      .slice(0, 20);
  }, [keywords, selectedNode]);

  useEffect(() => {
    if (selectedNode && !history.includes(selectedNode)) {
      // History is managed by parent
    }
  }, [selectedNode, history, historyIndex]);

  if (!selectedNode) return null;

  const canGoBack = historyIndex > 0;
  const canGoForward = historyIndex < history.length - 1;
  const isIsolated = isolatedNodeId === selectedNode.id;
  const levelColor = LEVEL_COLORS[selectedNode.level] || 'slate';

  return (
    <div className="h-[60vh] md:h-full w-full md:w-[380px] bg-space-900/95 border-l border-border-subtle flex flex-col z-20 transition-all duration-300 flex-shrink-0 glass-strong relative overflow-hidden fixed md:relative bottom-0 right-0">
      {/* Animated border glow */}
      <div className="absolute top-0 left-0 bottom-0 w-px bg-gradient-to-t from-electric-cyan/50 via-transparent to-electric-magenta/50 animate-pulse-glow" />
      
      {/* Header */}
      <div className="flex items-center justify-between p-3 border-b border-border-subtle bg-space-800/50 flex-shrink-0 relative z-10">
        <div className="flex items-center gap-1">
          <button
            onClick={() => onNavigateHistory('back')}
            disabled={!canGoBack}
            className={`btn-icon ${
              canGoBack ? 'text-text-secondary hover:text-electric-cyan hover:bg-space-700' : 'text-text-dim cursor-not-allowed'
            }`}
            aria-label="Go back in history"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <button
            onClick={() => onNavigateHistory('forward')}
            disabled={!canGoForward}
            className={`btn-icon ${
              canGoForward ? 'text-text-secondary hover:text-electric-cyan hover:bg-space-700' : 'text-text-dim cursor-not-allowed'
            }`}
            aria-label="Go forward in history"
          >
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>

        <div className="flex items-center gap-1">
          <span className={`badge ${levelColor}`}>
            <IconRenderer icon={LEVEL_ICONS[selectedNode.level]} className="w-3 h-3 mr-1" />
            {LEVEL_LABELS[selectedNode.level] || selectedNode.level}
          </span>
          
          {setIsolatedNodeId && (
            <button
              onClick={() => setIsolatedNodeId(isIsolated ? null : selectedNode.id)}
              className={`btn-icon transition-all ${
                isIsolated 
                  ? 'text-electric-amber hover:bg-electric-amber/10' 
                  : 'text-text-muted hover:text-text-secondary hover:bg-space-700'
              }`}
              title={isIsolated ? "Show Full Tree" : "Isolate Subtree"}
            >
              <Target className="w-4 h-4" />
            </button>
          )}

          <button
            onClick={() => onNodeSelect(null)}
            className="btn-icon text-text-muted hover:text-text-secondary hover:bg-space-700"
            aria-label="Close panel"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto custom-scrollbar flex flex-col relative z-10">
        <div className="p-4 flex flex-col gap-4">
          {/* Breadcrumbs */}
          <div className="flex flex-wrap items-center gap-1 text-[10px] text-text-muted font-medium tracking-wide">
            {breadcrumbs.map((crumb, idx) => (
              <React.Fragment key={crumb.id}>
                {idx > 0 && <ChevronRight className="w-3 h-3 text-text-dim" />}
                <button
                  onClick={() => onNodeSelect(crumb)}
                  className={`hover:text-electric-cyan transition-colors ${idx === breadcrumbs.length - 1 ? 'text-text-secondary cursor-default' : ''}`}
                  disabled={idx === breadcrumbs.length - 1}
                >
                  {crumb.name}
                </button>
              </React.Fragment>
            ))}
            {breadcrumbs.length > 0 && <ChevronRight className="w-3 h-3 text-text-dim" />}
            <span className="text-text-primary font-semibold truncate max-w-[200px]">{selectedNode.name}</span>
          </div>

          {/* Node Header */}
          <div className="flex items-start justify-between gap-4">
            <div className="flex-1 min-w-0">
              <h2 className="text-xl font-display font-bold text-text-primary leading-tight">
                {selectedNode.name}
              </h2>
              <div className="flex flex-wrap items-center gap-2 mt-2">
                <Badge variant={levelColor}>
                  <IconRenderer icon={LEVEL_ICONS[selectedNode.level]} className="w-3 h-3 mr-1" />
                  {selectedNode.id}
                </Badge>
                
                {selectedNode.cs2023_ka && (
                  <Badge variant="purple">
                    <Tag className="w-3 h-3 mr-1" />
                    CS2023: {selectedNode.cs2023_ka}
                  </Badge>
                )}

                {selectedNode.metadata?.lo_type && (
                  <Badge variant="green">
                    <Sparkles className="w-3 h-3 mr-1" />
                    {selectedNode.metadata.lo_type}
                  </Badge>
                )}
              </div>
            </div>
            
            {/* Sibling Navigation */}
            <div className="flex items-center gap-1 bg-space-750 rounded-lg p-0.5 border border-border-default">
              <button
                onClick={() => prevSibling && onNodeSelect(prevSibling)}
                disabled={!prevSibling}
                className={`btn-icon transition-colors ${prevSibling ? 'text-text-secondary hover:text-electric-cyan hover:bg-space-700' : 'text-text-dim cursor-not-allowed'}`}
                aria-label="Previous sibling"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <button
                onClick={() => nextSibling && onNodeSelect(nextSibling)}
                disabled={!nextSibling}
                className={`btn-icon transition-colors ${nextSibling ? 'text-text-secondary hover:text-electric-cyan hover:bg-space-700' : 'text-text-dim cursor-not-allowed'}`}
                aria-label="Next sibling"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Description */}
          {selectedNode.description && (
            <div className="panel p-4">
              <div className="flex items-center gap-2 mb-2">
                <Info className="w-4 h-4 text-electric-cyan" />
                <span className="text-xs font-semibold text-text-secondary uppercase tracking-widest">Description</span>
              </div>
              <p className="text-sm text-text-secondary leading-relaxed">{selectedNode.description}</p>
            </div>
          )}

          {/* Overview Section - Extended Metadata */}
          <Section
            title="Overview"
            icon={Info}
            isOpen={expandedSections.overview}
            onToggle={() => toggleSection('overview')}
          >
            <div className="grid grid-cols-2 gap-2">
              <MetadataRow label="Code" value={selectedNode.id} icon={Hash} />
              <MetadataRow label="Level" value={LEVEL_LABELS[selectedNode.level] || selectedNode.level} icon={Layers} />
              {selectedNode.cs2023_ka && (
                <MetadataRow label="CS2023 KA" value={selectedNode.cs2023_ka} icon={Tag} />
              )}
              {selectedNode.metadata?.lo_type && (
                <MetadataRow label="LO Type" value={selectedNode.metadata.lo_type} icon={Sparkles} />
              )}
              {selectedNode.metadata?.bloom_level && (
                <MetadataRow label="Bloom Level" value={selectedNode.metadata.bloom_level} icon={BookOpen} />
              )}
              {selectedNode.metadata?.knowledge_dimension && (
                <MetadataRow label="Knowledge Dim." value={selectedNode.metadata.knowledge_dimension} icon={BookOpen} />
              )}
              {selectedNode.metadata?.spiral_bloom && (
                <MetadataRow label="Spiral Bloom" value={selectedNode.metadata.spiral_bloom} icon={Sparkles} />
              )}
              <MetadataRow 
                label="Connections" 
                value={`${(linksBySource[selectedNode.id]?.length || 0) + (linksByTarget[selectedNode.id]?.length || 0)} total`}
                icon={Link2} 
              />
            </div>

            {/* Additional metadata */}
            {selectedNode.metadata && Object.keys(selectedNode.metadata).length > 0 && (
              <div className="mt-3 pt-3 border-t border-border-subtle">
                <span className="text-[10px] font-semibold text-text-muted uppercase tracking-wider mb-2 block">Additional Attributes</span>
                <div className="space-y-1">
                  {Object.entries(selectedNode.metadata)
                    .filter(([key]) => !['color', 'lo_type', 'bloom_level', 'knowledge_dimension', 'spiral_bloom'].includes(key))
                    .map(([key, val]) => (
                      <div key={key} className="flex items-center gap-2 py-1">
                        <span className="text-[10px] font-semibold text-text-muted uppercase tracking-wider w-28 flex-shrink-0">
                          {key.replace(/_/g, ' ')}
                        </span>
                        <span className="text-sm text-text-primary truncate flex-1 font-mono">
                          {typeof val === 'object' ? JSON.stringify(val) : String(val)}
                        </span>
                      </div>
                    ))}
                </div>
              </div>
            )}
          </Section>

          {/* Keywords Section */}
          {nodeKeywords.length > 0 && (
            <Section
              title={`Keywords (${nodeKeywords.length})`}
              icon={Tag}
              isOpen={expandedSections.keywords}
              onToggle={() => toggleSection('keywords')}
            >
              <div className="flex flex-wrap gap-1.5">
                {nodeKeywords.map(kw => (
                  <button
                    key={kw.code}
                    className="badge-cyan hover:bg-electric-cyan/30 transition-colors cursor-default"
                    title={kw.description}
                  >
                    {kw.name}
                  </button>
                ))}
                {nodeKeywords.length > 15 && (
                  <span className="badge-slate">+{nodeKeywords.length - 15} more</span>
                )}
              </div>
            </Section>
          )}

          {/* Prerequisites Section */}
          {(prerequisites.incoming.length > 0 || prerequisites.outgoing.length > 0) && (
            <Section
              title="Prerequisites"
              icon={Link2}
              isOpen={expandedSections.prerequisites}
              onToggle={() => toggleSection('prerequisites')}
            >
              {prerequisites.incoming.length > 0 && (
                <div className="mb-4">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="w-2 h-2 rounded-full bg-electric-magenta" />
                    <span className="text-xs font-semibold text-electric-magenta uppercase tracking-wider">Requires (Must Learn First)</span>
                  </div>
                  <div className="flex flex-col gap-1.5">
                    {prerequisites.incoming.slice(0, 8).map(prereq => (
                      <button
                        key={prereq.id}
                        onClick={() => onNodeSelect(prereq)}
                        className="flex items-center gap-2 p-2 panel hover:bg-space-700 hover:border-electric-magenta/30 transition-all rounded-lg"
                      >
                        <IconRenderer icon={LEVEL_ICONS[prereq.level]} className="w-4 h-4 text-electric-magenta" />
                        <div className="flex-1 min-w-0">
                          <div className="text-sm font-medium text-text-primary truncate">{prereq.name}</div>
                          <div className="flex items-center gap-1.5 mt-0.5">
                            <Badge variant={LEVEL_COLORS[prereq.level] || 'slate'} className="text-[9px]">
                              {LEVEL_LABELS[prereq.level] || prereq.level}
                            </Badge>
                          </div>
                        </div>
                        <ExternalLink className="w-3.5 h-3.5 text-text-muted" />
                      </button>
                    ))}
                    {prerequisites.incoming.length > 8 && (
                      <div className="text-center py-2 text-xs text-text-muted border-t border-border-subtle">
                        +{prerequisites.incoming.length - 8} more prerequisites
                      </div>
                    )}
                  </div>
                </div>
              )}

              {prerequisites.outgoing.length > 0 && (
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <span className="w-2 h-2 rounded-full bg-electric-green" />
                    <span className="text-xs font-semibold text-electric-green uppercase tracking-wider">Unlocks (Enables)</span>
                  </div>
                  <div className="flex flex-col gap-1.5">
                    {prerequisites.outgoing.slice(0, 8).map(prereq => (
                      <button
                        key={prereq.id}
                        onClick={() => onNodeSelect(prereq)}
                        className="flex items-center gap-2 p-2 panel hover:bg-space-700 hover:border-electric-green/30 transition-all rounded-lg"
                      >
                        <IconRenderer icon={LEVEL_ICONS[prereq.level]} className="w-4 h-4 text-electric-green" />
                        <div className="flex-1 min-w-0">
                          <div className="text-sm font-medium text-text-primary truncate">{prereq.name}</div>
                          <div className="flex items-center gap-1.5 mt-0.5">
                            <Badge variant={LEVEL_COLORS[prereq.level] || 'slate'} className="text-[9px]">
                              {LEVEL_LABELS[prereq.level] || prereq.level}
                            </Badge>
                          </div>
                        </div>
                        <ExternalLink className="w-3.5 h-3.5 text-text-muted" />
                      </button>
                    ))}
                    {prerequisites.outgoing.length > 8 && (
                      <div className="text-center py-2 text-xs text-text-muted border-t border-border-subtle">
                        +{prerequisites.outgoing.length - 8} more enabled concepts
                      </div>
                    )}
                  </div>
                </div>
              )}
            </Section>
          )}

          {/* Children Section */}
          {children.length > 0 && (
            <Section
              title={`Children (${children.length})`}
              icon={BookOpen}
              isOpen={expandedSections.children}
              onToggle={() => toggleSection('children')}
            >
              <div className="flex flex-col gap-1.5">
                {children.map(child => (
                  <button
                    key={child.id}
                    onClick={() => onNodeSelect(child)}
                    className="flex items-center gap-3 p-3 panel hover:bg-space-700 hover:border-electric-cyan/30 transition-all rounded-lg group"
                  >
                    <div className="p-2 rounded-lg bg-space-750 text-text-muted group-hover:bg-electric-cyan/20 group-hover:text-electric-cyan transition-colors">
                      <IconRenderer icon={LEVEL_ICONS[child.level]} className="w-4 h-4" />
                    </div>
                    <div className="flex-1 overflow-hidden">
                      <div className="text-sm font-medium text-text-primary group-hover:text-electric-cyan truncate transition-colors">
                        {child.name}
                      </div>
                      <div className="flex items-center gap-1.5 mt-0.5">
                        <Badge variant={LEVEL_COLORS[child.level] || 'slate'} className="text-[9px]">
                          {LEVEL_LABELS[child.level] || child.level}
                        </Badge>
                        {child.cs2023_ka && (
                          <Badge variant="purple" className="text-[9px]">
                            {child.cs2023_ka}
                          </Badge>
                        )}
                      </div>
                    </div>
                    <ChevronRight className="w-4 h-4 text-text-dim opacity-0 group-hover:opacity-100 transform group-hover:translate-x-1 transition-all" />
                  </button>
                ))}
              </div>
            </Section>
          )}

          {/* Siblings Section */}
          {(prevSibling || nextSibling) && (
            <Section
              title="Siblings"
              icon={Link2}
              isOpen={expandedSections.siblings}
              onToggle={() => toggleSection('siblings')}
            >
              <div className="flex flex-col gap-2">
                {prevSibling && (
                  <button
                    onClick={() => onNodeSelect(prevSibling)}
                    className="flex items-center gap-3 p-3 panel hover:bg-space-700 hover:border-electric-amber/30 transition-all rounded-lg"
                  >
                    <div className="p-2 rounded-lg bg-space-750 text-electric-amber">
                      <ArrowLeft className="w-4 h-4" />
                    </div>
                    <div className="flex-1">
                      <div className="text-sm font-medium text-text-primary">{prevSibling.name}</div>
                      <Badge variant={LEVEL_COLORS[prevSibling.level] || 'slate'} className="text-[9px]">
                        {LEVEL_LABELS[prevSibling.level] || prevSibling.level}
                      </Badge>
                    </div>
                  </button>
                )}
                {nextSibling && (
                  <button
                    onClick={() => onNodeSelect(nextSibling)}
                    className="flex items-center gap-3 p-3 panel hover:bg-space-700 hover:border-electric-amber/30 transition-all rounded-lg"
                  >
                    <div className="flex-1 text-right">
                      <div className="text-sm font-medium text-text-primary">{nextSibling.name}</div>
                      <Badge variant={LEVEL_COLORS[nextSibling.level] || 'slate'} className="text-[9px]">
                        {LEVEL_LABELS[nextSibling.level] || nextSibling.level}
                      </Badge>
                    </div>
                    <div className="p-2 rounded-lg bg-space-750 text-electric-amber">
                      <ArrowRight className="w-4 h-4" />
                    </div>
                  </button>
                )}
              </div>
            </Section>
          )}

          {/* Empty State */}
          {children.length === 0 && !prerequisites.incoming.length && !prerequisites.outgoing.length && (
            <div className="flex-1 flex flex-col items-center justify-center p-8 text-center text-text-muted border-t border-border-subtle">
              <Minus className="w-10 h-10 mb-3 opacity-20" />
              <p className="text-sm">No related nodes available</p>
              <p className="text-xs mt-1 opacity-50">Explore parent or sibling nodes</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}