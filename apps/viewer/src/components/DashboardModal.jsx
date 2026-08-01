import React, { useMemo } from 'react';
import { BarChart3, X, Download, Layers, BookOpen, Hexagon, Hash, CheckCircle2, PieChart } from 'lucide-react';

export default function DashboardModal({ isOpen, onClose, graphData }) {
  if (!isOpen || !graphData || !graphData.nodes) return null;

  const stats = useMemo(() => {
    const levelCounts = {};
    const loTypes = {};
    const cs2023KAs = {};
    let totalLinks = graphData.links.length;

    graphData.nodes.forEach(node => {
      levelCounts[node.level] = (levelCounts[node.level] || 0) + 1;
      
      if (node.metadata?.lo_type) {
        loTypes[node.metadata.lo_type] = (loTypes[node.metadata.lo_type] || 0) + 1;
      }
      
      if (node.cs2023_ka) {
        cs2023KAs[node.cs2023_ka] = (cs2023KAs[node.cs2023_ka] || 0) + 1;
      }
    });

    const topConnected = [...graphData.nodes]
      .sort((a, b) => (b.linkCount || 0) - (a.linkCount || 0))
      .slice(0, 5);

    return { levelCounts, loTypes, cs2023KAs, totalLinks, topConnected };
  }, [graphData]);

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

  const levelLabels = {
    field: 'Field (Ngành)',
    subject: 'Subject (Môn)',
    category: 'Category (Danh mục)',
    topic: 'Topic (Chủ đề)',
    concept: 'Concept (Khái niệm)',
    learning_objective: 'Learning Objective',
    keyword: 'Keyword'
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-[#1a1d21] border border-slate-700 rounded-2xl max-w-2xl w-full p-6 shadow-2xl relative text-slate-200 max-h-[85vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-blue-400" />
            <h2 className="text-lg font-bold text-white">Curriculum Analytics & Insights</h2>
          </div>
          <div className="flex items-center gap-2">
            <button 
              onClick={handleExportCSV}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-blue-600/20 border border-blue-500/30 hover:bg-blue-600/30 text-blue-400 rounded-lg text-xs font-semibold transition-colors"
            >
              <Download className="w-3.5 h-3.5" />
              Export CSV
            </button>
            <button 
              onClick={onClose}
              className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto custom-scrollbar py-4 space-y-6">
          {/* Summary Cards */}
          <div className="grid grid-cols-3 gap-3">
            <div className="bg-[#23272e] p-3.5 rounded-xl border border-slate-800">
              <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Total Entities</span>
              <div className="text-2xl font-black text-blue-400 mt-1">{graphData.nodes.length}</div>
            </div>
            <div className="bg-[#23272e] p-3.5 rounded-xl border border-slate-800">
              <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Total Connections</span>
              <div className="text-2xl font-black text-purple-400 mt-1">{stats.totalLinks}</div>
            </div>
            <div className="bg-[#23272e] p-3.5 rounded-xl border border-slate-800">
              <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">CS2023 Mapped</span>
              <div className="text-2xl font-black text-emerald-400 mt-1">
                {Object.values(stats.cs2023KAs).reduce((a, b) => a + b, 0)}
              </div>
            </div>
          </div>

          {/* Level Breakdown */}
          <div>
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3 flex items-center gap-1.5">
              <Layers className="w-3.5 h-3.5 text-blue-400" /> Taxonomy Level Distribution
            </h3>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
              {Object.entries(stats.levelCounts).map(([lvl, count]) => (
                <div key={lvl} className="bg-[#23272e] p-3 rounded-lg border border-slate-800 flex justify-between items-center">
                  <span className="text-xs text-slate-300 font-medium">{levelLabels[lvl] || lvl}</span>
                  <span className="text-xs font-bold px-2 py-0.5 rounded bg-slate-800 text-slate-200">{count}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Top Connected Concepts */}
          <div>
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3 flex items-center gap-1.5">
              <Hexagon className="w-3.5 h-3.5 text-amber-400" /> Key Hubs (Top Connected Concepts)
            </h3>
            <div className="space-y-1.5">
              {stats.topConnected.map(node => (
                <div key={node.id} className="bg-[#23272e] p-2.5 rounded-lg border border-slate-800 flex justify-between items-center text-xs">
                  <div className="flex items-center gap-2 overflow-hidden pr-2">
                    <span className="px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 font-bold uppercase text-[9px]">
                      {node.level}
                    </span>
                    <span className="text-slate-200 font-semibold truncate">{node.name}</span>
                  </div>
                  <span className="text-slate-400 text-[11px] font-mono whitespace-nowrap">{node.linkCount || 0} links</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="pt-4 border-t border-slate-800 flex justify-end">
          <button 
            onClick={onClose}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg text-xs font-semibold transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
