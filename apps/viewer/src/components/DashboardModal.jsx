import React, { useMemo, useState } from 'react';
import { 
  BarChart3, X, Download, Layers, BookOpen, Hexagon, Hash, 
  CheckCircle2, PieChart, Tag, Sparkles, Link2, Database, 
  GitBranch, Filter, Circle, Zap, Eye, Share2, Copy, 
  ChevronDown, ChevronUp, Search, TrendingUp, Target
} from 'lucide-react';

const LEVEL_ICONS = {
  field: Database,
  subject: GitBranch,
  category: Layers,
  topic: Filter,
  concept: Circle,
  learning_objective: BookOpen,
  keyword: Hash,
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

const LEVEL_ORDER = ['field', 'subject', 'category', 'topic', 'concept', 'learning_objective', 'keyword'];

const Badge = ({ children, variant = 'slate', className = '' }) => {
  const variants = {
    cyan: 'bg-electric-cyan/20 text-electric-cyan border-electric-cyan/30',
    amber: 'bg-electric-amber/20 text-electric-amber border-electric-amber/30',
    magenta: 'bg-electric-magenta/20 text-electric-magenta border-electric-magenta/30',
    green: 'bg-electric-green/20 text-electric-green border-electric-green/30',
    slate: 'bg-space-700 text-text-secondary border-border-default',
    purple: 'bg-electric-magenta/20 text-electric-magenta border-electric-magenta/30',
    'electric-cyan': 'bg-electric-cyan/20 text-electric-cyan border-electric-cyan/30',
    'electric-green': 'bg-electric-green/20 text-electric-green border-electric-green/30',
    'electric-amber': 'bg-electric-amber/20 text-electric-amber border-electric-amber/30',
    'electric-magenta': 'bg-electric-magenta/20 text-electric-magenta border-electric-magenta/30',
  };
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider border ${variants[variant] || variants.slate} ${className}`}>
      {children}
    </span>
  );
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

const StatCard = ({ label, value, icon: Icon, color, trend }) => (
  <div className="panel p-4 rounded-xl">
    <div className="flex items-center justify-between mb-2">
      <span className="text-[10px] font-semibold text-text-muted uppercase tracking-wider">{label}</span>
      <Icon className={`w-5 h-5 ${color}`} />
    </div>
    <div className="text-3xl font-display font-bold text-text-primary mb-1">{value}</div>
    {trend && (
      <div className="flex items-center gap-1 text-[10px] font-medium text-electric-green">
        <TrendingUp className="w-3 h-3" />
        <span>{trend}</span>
      </div>
    )}
  </div>
);

const ProgressBar = ({ label, value, max, color, icon: Icon }) => {
  const percentage = max > 0 ? Math.round((value / max) * 100) : 0;
  const colors = {
    cyan: 'bg-electric-cyan',
    green: 'bg-electric-green',
    amber: 'bg-electric-amber',
    magenta: 'bg-electric-magenta',
    purple: 'bg-electric-magenta',
  };
  return (
    <div className="flex items-center gap-3">
      <div className="w-20 flex-shrink-0">
        <span className="text-[10px] font-semibold text-text-muted uppercase tracking-wider">{label}</span>
      </div>
      <div className="flex-1 h-2 bg-space-700 rounded-full overflow-hidden">
        <div 
          className={`${colors[color] || 'bg-electric-cyan'} h-full rounded-full transition-all duration-500 ease-out`}
          style={{ width: `${percentage}%` }}
        />
      </div>
      <span className="text-sm font-mono text-text-secondary w-16 text-right">{value}/{max}</span>
    </div>
  );
};

export default function DashboardModal({ isOpen, onClose, graphData, keywords = [] }) {
  if (!isOpen || !graphData || !graphData.nodes) return null;

  const [expandedSections, setExpandedSections] = useState({
    overview: true,
    levels: true,
    cs2023: true,
    loTypes: true,
    hubs: true,
    keywords: true,
    exports: true,
  });

  const toggleSection = (key) => {
    setExpandedSections(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const stats = useMemo(() => {
    const levelCounts = {};
    const loTypes = {};
    const cs2023KAs = {};
    let totalLinks = graphData.links.length;
    let nodesWithKeywords = 0;

    graphData.nodes.forEach(node => {
      levelCounts[node.level] = (levelCounts[node.level] || 0) + 1;
      
      if (node.metadata?.lo_type) {
        loTypes[node.metadata.lo_type] = (loTypes[node.metadata.lo_type] || 0) + 1;
      }
      
      if (node.cs2023_ka) {
        cs2023KAs[node.cs2023_ka] = (cs2023KAs[node.cs2023_ka] || 0) + 1;
      }
      
      if (node.keywords && node.keywords.length > 0) {
        nodesWithKeywords++;
      }
    });

    const topConnected = [...graphData.nodes]
      .sort((a, b) => (b.linkCount || 0) - (a.linkCount || 0))
      .slice(0, 10);

    // Calculate density
    const n = graphData.nodes.length;
    const maxPossibleLinks = n * (n - 1) / 2;
    const density = maxPossibleLinks > 0 ? (totalLinks / maxPossibleLinks * 100).toFixed(2) : 0;

    // Keyword stats
    const keywordCounts = {};
    keywords.forEach(kw => {
      try {
        const conceptCodes = JSON.parse(kw.concept_codes || '[]');
        conceptCodes.forEach(cc => {
          keywordCounts[cc] = (keywordCounts[cc] || 0) + 1;
        });
      } catch {}
    });

    const conceptsWithKeywords = Object.keys(keywordCounts).length;
    const avgKeywordsPerConcept = conceptsWithKeywords > 0 
      ? (Object.values(keywordCounts).reduce((a, b) => a + b, 0) / conceptsWithKeywords).toFixed(1)
      : 0;

    return { 
      levelCounts, 
      loTypes, 
      cs2023KAs, 
      totalLinks, 
      topConnected,
      density,
      nodesWithKeywords,
      conceptsWithKeywords,
      avgKeywordsPerConcept,
      totalKeywords: keywords.length,
    };
  }, [graphData, keywords]);

  const handleExportCSV = () => {
    const headers = ['Code', 'Name', 'Level', 'CS2023_KA', 'LO_Type', 'Description'];
    const rows = graphData.nodes.map(n => [
      `"${n.id}"`,
      `"${(n.name || '').replace(/"/g, '""')}"`,
      `"${n.level}"`,
      `"${n.cs2023_ka || ''}"`,
      `"${n.metadata?.lo_type || ''}"`,
      `"${(n.description || '').replace(/"/g, '""')}"`
    ]);

    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `knowledge_tree_export_${new Date().toISOString().slice(0,10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleExportJSON = () => {
    const exportData = {
      metadata: {
        exportedAt: new Date().toISOString(),
        version: '3.5.0',
        nodeCount: graphData.nodes.length,
        linkCount: graphData.links.length,
      },
      nodes: graphData.nodes,
      links: graphData.links,
    };
    const jsonContent = 'data:application/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(exportData, null, 2));
    const link = document.createElement('a');
    link.setAttribute('href', jsonContent);
    link.setAttribute('download', `knowledge_tree_export_${new Date().toISOString().slice(0,10)}.json`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleCopyGraphML = () => {
    let graphml = `<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns">
  <key id="level" for="node" attr.name="level" attr.type="string"/>
  <key id="name" for="node" attr.name="name" attr.type="string"/>
  <key id="cs2023_ka" for="node" attr.name="cs2023_ka" attr.type="string"/>
  <graph id="G" edgedefault="directed">
`;
    graphData.nodes.forEach(node => {
      graphml += `    <node id="${node.id}">\n`;
      graphml += `      <data key="level">${node.level}</data>\n`;
      graphml += `      <data key="name">${node.name.replace(/&/g, '&').replace(/</g, '<').replace(/>/g, '>')}</data>\n`;
      if (node.cs2023_ka) {
        graphml += `      <data key="cs2023_ka">${node.cs2023_ka}</data>\n`;
      }
      graphml += `    </node>\n`;
    });
    graphData.links.forEach((link, i) => {
      const source = typeof link.source === 'object' ? link.source.id : link.source;
      const target = typeof link.target === 'object' ? link.target.id : link.target;
      graphml += `    <edge id="e${i}" source="${source}" target="${target}"/>\n`;
    });
    graphml += `  </graph>\n</graphml>`;

    navigator.clipboard.writeText(graphml).then(() => {
      // Could show a toast here
    });
  };

  return (
    <div className="fixed inset-0 z-50 bg-space-950/90 backdrop-blur-md flex items-center justify-center p-4 animate-fade-in">
      <div className="modal-content max-w-4xl w-full max-h-[90vh] animate-scale-in">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-border-subtle flex-shrink-0">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-electric-cyan/10">
              <BarChart3 className="w-5 h-5 text-electric-cyan" />
            </div>
            <div>
              <h2 className="text-lg font-display font-bold text-text-primary">Curriculum Analytics & Insights</h2>
              <p className="text-[10px] text-text-muted">Knowledge Tree v3.5 • {graphData.nodes.length} nodes • {graphData.links.length} connections</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button onClick={handleExportJSON} className="btn-icon text-text-muted hover:text-electric-green hover:bg-space-750" title="Export JSON">
              <BookOpen className="w-4 h-4" />
            </button>
            <button onClick={handleExportCSV} className="btn-icon text-text-muted hover:text-electric-amber hover:bg-space-750" title="Export CSV">
              <Download className="w-4 h-4" />
            </button>
            <button onClick={handleCopyGraphML} className="btn-icon text-text-muted hover:text-electric-cyan hover:bg-space-750" title="Copy GraphML">
              <Link2 className="w-4 h-4" />
            </button>
            <button onClick={onClose} className="btn-icon text-text-muted hover:text-text-secondary hover:bg-space-750">
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto custom-scrollbar p-4 space-y-4">
          {/* Summary Stats Row */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 animate-fade-in stagger-1">
            <StatCard 
              label="Total Entities" 
              value={graphData.nodes.length} 
              icon={Database} 
              color="text-electric-cyan" 
            />
            <StatCard 
              label="Total Connections" 
              value={stats.totalLinks} 
              icon={Link2} 
              color="text-electric-magenta"
            />
            <StatCard 
              label="Graph Density" 
              value={`${stats.density}%`} 
              icon={Target} 
              color="text-electric-green"
            />
            <StatCard 
              label="CS2023 Mapped" 
              value={Object.values(stats.cs2023KAs).reduce((a, b) => a + b, 0)} 
              icon={Tag} 
              color="text-electric-amber"
            />
          </div>

          {/* Keyword Stats Row */}
          {stats.totalKeywords > 0 && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 animate-fade-in stagger-2">
              <StatCard 
                label="Total Keywords" 
                value={stats.totalKeywords} 
                icon={Hash} 
                color="text-electric-cyan"
              />
              <StatCard 
                label="Concepts w/ Keywords" 
                value={stats.conceptsWithKeywords} 
                icon={Sparkles} 
                color="text-electric-green"
              />
              <StatCard 
                label="Nodes w/ Keywords" 
                value={stats.nodesWithKeywords} 
                icon={Eye} 
                color="text-electric-amber"
              />
              <StatCard 
                label="Avg Keywords/Concept" 
                value={stats.avgKeywordsPerConcept} 
                icon={TrendingUp} 
                color="text-electric-magenta"
              />
            </div>
          )}

          {/* Taxonomy Level Distribution */}
          <Section
            title="Taxonomy Level Distribution"
            icon={Layers}
            isOpen={expandedSections.levels}
            onToggle={() => toggleSection('levels')}
          >
            <div className="space-y-3">
              {LEVEL_ORDER.map(level => {
                const count = stats.levelCounts[level] || 0;
                const percentage = graphData.nodes.length > 0 
                  ? Math.round((count / graphData.nodes.length) * 100) 
                  : 0;
                return (
                  <div key={level} className="panel p-3 rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <IconRenderer icon={LEVEL_ICONS[level]} className={`w-4 h-4 ${LEVEL_COLORS[level] || 'text-text-secondary'}`} />
                        <span className="text-xs font-semibold text-text-secondary uppercase tracking-wider">
                          {LEVEL_LABELS[level] || level}
                        </span>
                      </div>
                      <span className="text-sm font-mono text-text-primary">{count} <span className="text-text-muted">({percentage}%)</span></span>
                    </div>
                    <div className="h-1.5 bg-space-700 rounded-full overflow-hidden">
                      <div 
                        className={`h-full rounded-full transition-all duration-500 ${LEVEL_COLORS[level] ? `bg-${LEVEL_COLORS[level]}` : 'bg-text-secondary'}`}
                        style={{ width: `${percentage}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </Section>

          {/* CS2023 Knowledge Areas */}
          <Section
            title="CS2023 Knowledge Area Mapping"
            icon={Tag}
            isOpen={expandedSections.cs2023}
            onToggle={() => toggleSection('cs2023')}
          >
            <div className="space-y-2">
              {Object.entries(stats.cs2023KAs)
                .sort((a, b) => b[1] - a[1])
                .map(([ka, count]) => (
                  <div key={ka} className="panel p-3 rounded-lg flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <span className="badge-purple">{ka}</span>
                      <span className="text-sm font-medium text-text-primary">
                        {count} concept{count !== 1 ? 's' : ''}
                      </span>
                    </div>
                    <ProgressBar 
                      value={count} 
                      max={Math.max(...Object.values(stats.cs2023KAs))} 
                      color="purple" 
                      label=""
                    />
                  </div>
                ))}
              {Object.keys(stats.cs2023KAs).length === 0 && (
                <div className="text-center py-8 text-text-muted">
                  <Tag className="w-8 h-8 mx-auto mb-2 opacity-20" />
                  <p>No CS2023 Knowledge Area mappings found</p>
                </div>
              )}
            </div>
          </Section>

          {/* Learning Objective Types */}
          {Object.keys(stats.loTypes).length > 0 && (
            <>
              <Section
                title="Learning Objective Types"
                icon={BookOpen}
                isOpen={expandedSections.loTypes}
                onToggle={() => toggleSection('loTypes')}
              >
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  {Object.entries(stats.loTypes)
                    .sort((a, b) => b[1] - a[1])
                    .map(([type, count]) => (
                      <div key={type} className="panel p-4 rounded-xl text-center hover:border-electric-cyan/30 transition-colors">
                        <Sparkles className="w-8 h-8 mx-auto mb-2 text-electric-cyan" />
                        <div className="text-2xl font-display font-bold text-text-primary">{count}</div>
                        <div className="text-xs font-semibold text-text-secondary uppercase tracking-wider mt-1">{type}</div>
                      </div>
                    ))}
                </div>
              </Section>
            </>
          )}
          {/* Key Hubs - Top Connected Concepts */}
          <Section
            title="Key Hubs (Top Connected Concepts)"
            icon={Target}
            isOpen={expandedSections.hubs}
            onToggle={() => toggleSection('hubs')}
          >
            <div className="space-y-2">
              {stats.topConnected.map((node, index) => (
                <button
                  key={node.id}
                  className="panel p-3 rounded-lg flex items-center gap-3 hover:bg-space-700 hover:border-electric-cyan/30 transition-all group"
                >
                  <div className="w-8 h-8 flex items-center justify-center rounded-lg bg-electric-cyan/10 text-electric-cyan font-display font-bold text-lg">
                    {index + 1}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <IconRenderer icon={LEVEL_ICONS[node.level]} className={`w-4 h-4 ${LEVEL_COLORS[node.level] || 'text-text-secondary'}`} />
                      <span className="text-sm font-medium text-text-primary truncate group-hover:text-electric-cyan transition-colors">{node.name}</span>
                    </div>
                    <div className="flex items-center gap-2 mt-1">
                      <Badge variant={LEVEL_COLORS[node.level] || 'slate'} className="text-[9px]">
                        {LEVEL_LABELS[node.level] || node.level}
                      </Badge>
                      {node.cs2023_ka && <Badge variant="purple" className="text-[9px]">{node.cs2023_ka}</Badge>}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-display font-bold text-electric-cyan">{node.linkCount || 0}</div>
                    <div className="text-[10px] font-mono text-text-muted">connections</div>
                  </div>
                </button>
              ))}
            </div>
          </Section>

          {/* Keywords Overview */}
          {stats.totalKeywords > 0 && (
            <Section
              title={`Keywords Overview (${stats.totalKeywords} tokens)`}
              icon={Hash}
              isOpen={expandedSections.keywords}
              onToggle={() => toggleSection('keywords')}
            >
              <div className="space-y-3">
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  <StatCard label="Unique Keywords" value={stats.totalKeywords} icon={Hash} color="text-electric-cyan" />
                  <StatCard label="Concepts Covered" value={stats.conceptsWithKeywords} icon={Sparkles} color="text-electric-green" />
                  <StatCard label="Nodes Referenced" value={stats.nodesWithKeywords} icon={Eye} color="text-electric-amber" />
                  <StatCard label="Avg per Concept" value={stats.avgKeywordsPerConcept} icon={TrendingUp} color="text-electric-magenta" />
                </div>
                <div className="panel p-3 rounded-lg">
                  <span className="text-[10px] font-semibold text-text-muted uppercase tracking-wider mb-2 block">Keyword Coverage by Level</span>
                  <div className="space-y-2">
                    {LEVEL_ORDER.map(level => {
                      const nodesAtLevel = graphData.nodes.filter(n => n.level === level);
                      const nodesWithKw = nodesAtLevel.filter(n => n.keywords && n.keywords.length > 0).length;
                      const percentage = nodesAtLevel.length > 0 ? Math.round((nodesWithKw / nodesAtLevel.length) * 100) : 0;
                      return (
                        <div key={level} className="flex items-center gap-3">
                          <IconRenderer icon={LEVEL_ICONS[level]} className={`w-4 h-4 ${LEVEL_COLORS[level] || 'text-text-secondary'}`} />
                          <span className="text-xs font-semibold text-text-secondary uppercase tracking-wider w-24 flex-shrink-0">{LEVEL_LABELS[level] || level}</span>
                          <div className="flex-1 h-1.5 bg-space-700 rounded-full overflow-hidden">
                            <div 
                              className={`${LEVEL_COLORS[level] ? `bg-${LEVEL_COLORS[level]}` : 'bg-text-secondary'} h-full rounded-full transition-all duration-500`}
                              style={{ width: `${percentage}%` }}
                            />
                          </div>
                          <span className="text-sm font-mono text-text-secondary">{nodesWithKw}/{nodesAtLevel.length} ({percentage}%)</span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            </Section>
          )}

          {/* Export Options */}
          <Section
            title="Export Options"
            icon={Download}
            isOpen={expandedSections.exports}
            onToggle={() => toggleSection('exports')}
          >
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <button onClick={handleExportJSON} className="btn-secondary p-4 flex flex-col items-center gap-2 hover:border-electric-green/30 transition-all">
                <BookOpen className="w-6 h-6 text-electric-green" />
                <span className="font-medium">Export JSON</span>
                <span className="text-[10px] text-text-muted">Full graph data</span>
              </button>
              <button onClick={handleExportCSV} className="btn-secondary p-4 flex flex-col items-center gap-2 hover:border-electric-amber/30 transition-all">
                <Download className="w-6 h-6 text-electric-amber" />
                <span className="font-medium">Export CSV</span>
                <span className="text-[10px] text-text-muted">Tabular format</span>
              </button>
              <button onClick={handleCopyGraphML} className="btn-secondary p-4 flex flex-col items-center gap-2 hover:border-electric-cyan/30 transition-all">
                <Link2 className="w-6 h-6 text-electric-cyan" />
                <span className="font-medium">Copy GraphML</span>
                <span className="text-[10px] text-text-muted">To clipboard</span>
              </button>
            </div>
          </Section>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-border-subtle flex justify-end gap-2 flex-shrink-0">
          <button onClick={onClose} className="btn-primary px-6 py-2">
            Close Dashboard
          </button>
        </div>
      </div>
    </div>
  );
}