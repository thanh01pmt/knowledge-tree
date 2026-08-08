import React, { useState, useMemo } from 'react';
import { Search, Filter, ArrowRight, ChevronRight, BookOpen, Database, Target, Layers, X } from 'lucide-react';

const TABS = [
  { id: 'fields', label: 'Fields', icon: Database },
  { id: 'subjects', label: 'Subjects', icon: BookOpen },
  { id: 'categories', label: 'Categories', icon: Layers },
  { id: 'topics', label: 'Topics', icon: Layers },
  { id: 'concepts', label: 'Concepts', icon: Target },
  { id: 'learning_objectives', label: 'Learning Objectives', icon: Target }
];

export default function DataTableView({ rawTreeData, theme, linksBySource, linksByTarget }) {
  const [activeTab, setActiveTab] = useState('topics');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedContext, setSelectedContext] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const ITEMS_PER_PAGE = 50; // { type, item }

  // Simple lineage tracking to find direct parents/children
  
  const relatedIds = useMemo(() => {
    const ids = new Set();
    if (!selectedContext || !selectedContext.item) return ids;
    const startCode = selectedContext.item.code;
    ids.add(startCode);

    if (linksBySource) {
      const queue = [startCode];
      while (queue.length > 0) {
        const curr = queue.shift();
        if (linksBySource[curr]) {
          linksBySource[curr].forEach(child => {
            if (!ids.has(child)) {
              ids.add(child);
              queue.push(child);
            }
          });
        }
      }
    }

    if (linksByTarget) {
      const queue = [startCode];
      const visited = new Set([startCode]);
      while (queue.length > 0) {
        const curr = queue.shift();
        if (linksByTarget[curr]) {
          linksByTarget[curr].forEach(parent => {
            if (!visited.has(parent)) {
              visited.add(parent);
              ids.add(parent);
              queue.push(parent);
            }
          });
        }
      }
    }
    return ids;
  }, [selectedContext, linksBySource, linksByTarget]);

const isRelated = (item, type, context) => {
    if (!context || !context.item) return true;
    if (type === context.type) return true;
    return relatedIds.has(item.code);
  };

  
  // Optimize: Memoize counts so they only recalculate when selectedContext changes
  const tabCounts = useMemo(() => {
    const counts = {};
    if (!rawTreeData) return counts;
    
    TABS.forEach(tab => {
      if (!rawTreeData[tab.id]) {
        counts[tab.id] = 0;
        return;
      }
      if (!selectedContext) {
        counts[tab.id] = rawTreeData[tab.id].length;
        return;
      }
      
      // If it's the active context type, don't filter siblings for count
      if (tab.id === selectedContext.type) {
        counts[tab.id] = rawTreeData[tab.id].length;
        return;
      }
      
      let count = 0;
      for (let i = 0; i < rawTreeData[tab.id].length; i++) {
        if (isRelated(rawTreeData[tab.id][i], tab.id, selectedContext)) {
          count++;
        }
      }
      counts[tab.id] = count;
    });
    return counts;
  }, [rawTreeData, selectedContext, relatedIds]);

  const displayedData = useMemo(() => {
    if (!rawTreeData || !rawTreeData[activeTab]) return [];
    let data = rawTreeData[activeTab];

    // 1. Cross-table Context Filter (only direct parent/child for now)
    if (selectedContext) {
      data = data.filter(item => isRelated(item, activeTab, selectedContext));
    }

    // 2. Search Filter
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      data = data.filter(item => 
        (item.name && item.name.toLowerCase().includes(term)) ||
        (item.code && item.code.toLowerCase().includes(term)) ||
        (item.description && item.description.toLowerCase().includes(term))
      );
    }

    return data;
  }, [rawTreeData, activeTab, searchTerm, selectedContext, relatedIds]);

  const paginatedData = displayedData.slice((currentPage - 1) * ITEMS_PER_PAGE, currentPage * ITEMS_PER_PAGE);
  const totalPages = Math.ceil(displayedData.length / ITEMS_PER_PAGE);

  return (
    <div className="flex-1 flex flex-col h-full bg-white dark:bg-[#0f1115] text-slate-900 dark:text-slate-100 overflow-hidden">
      {/* Header */}
      <div className="flex-shrink-0 border-b border-slate-200 dark:border-slate-800 p-4 flex items-center justify-between bg-slate-50 dark:bg-[#16181d]">
        <div className="flex items-center gap-4">
          <h1 className="text-lg font-bold text-slate-800 dark:text-slate-200">Knowledge Database</h1>
          {selectedContext && (
            <div className="flex items-center gap-2 text-sm bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 px-3 py-1.5 rounded-md border border-blue-200 dark:border-blue-800/50">
              <span className="font-medium">Filtered by {TABS.find(t => t.id === selectedContext.type)?.label}:</span>
              <span className="truncate max-w-[200px]">{selectedContext.item.name}</span>
              <button onClick={() => { setSelectedContext(null); setCurrentPage(1); }} className="ml-2 hover:text-blue-900 dark:hover:text-blue-100">
                <X className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>
        <div className="relative w-64">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input 
            type="text" 
            placeholder={`Search ${TABS.find(t=>t.id===activeTab)?.label}...`}
            value={searchTerm}
            onChange={e => { setSearchTerm(e.target.value); setCurrentPage(1); }}
            className="w-full pl-9 pr-4 py-2 bg-white dark:bg-[#1a1d21] border border-slate-200 dark:border-slate-700 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition-shadow"
          />
        </div>
      </div>

      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar Tabs */}
        <div className="w-64 border-r border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-[#16181d] flex flex-col p-3 gap-1 overflow-y-auto">
          <div className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-2 px-2">Tables</div>
          {TABS.map(tab => {
             const Icon = tab.icon;
             const count = tabCounts[tab.id] || 0;
             return (
              <button
                key={tab.id}
                onClick={() => { setActiveTab(tab.id); setSearchTerm(''); setCurrentPage(1); }}
                className={`flex items-center justify-between p-2.5 rounded-md transition-colors text-sm font-medium ${
                  activeTab === tab.id 
                  ? 'bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-400' 
                  : 'text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-800/50 hover:text-slate-900 dark:hover:text-slate-200'
                }`}
              >
                <div className="flex items-center gap-2">
                  <Icon className="w-4 h-4" />
                  {tab.label}
                </div>
                <span className="text-xs bg-slate-200 dark:bg-slate-800 px-2 py-0.5 rounded-full">{count}</span>
              </button>
             );
          })}
        </div>

        {/* Data Grid */}
        <div className="flex-1 overflow-auto bg-white dark:bg-[#0f1115] flex flex-col">
          <div className="flex-1 overflow-auto">
            <table className="w-full text-left border-collapse">
            <thead className="sticky top-0 bg-slate-100 dark:bg-[#1a1d21] border-b border-slate-200 dark:border-slate-800 shadow-sm z-10">
              <tr>
                <th className="py-3 px-4 text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider w-48">Code</th>
                <th className="py-3 px-4 text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider w-1/3">Name</th>
                <th className="py-3 px-4 text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Description</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800/50">
              {paginatedData.map((row) => (
                <tr 
                  key={row.code} 
                  onClick={() => {
                    setSelectedContext({ type: activeTab, item: row });
                    // Auto switch to next logical tab
                    const tabOrder = ['fields', 'subjects', 'categories', 'topics', 'concepts', 'learning_objectives'];
                    const currentIndex = tabOrder.indexOf(activeTab);
                    if (currentIndex !== -1 && currentIndex < tabOrder.length - 1) {
                      setActiveTab(tabOrder[currentIndex + 1]);
                      setSearchTerm('');
                      setCurrentPage(1);
                    }
                  }}
                  className={`transition-colors cursor-pointer group ${selectedContext && selectedContext.item.code === row.code ? 'bg-blue-50/50 dark:bg-blue-900/20' : 'hover:bg-slate-50 dark:hover:bg-[#1a1d21]'}`}
                >
                  <td className="py-3 px-4 text-sm font-mono text-slate-500 dark:text-slate-400 whitespace-nowrap">
                    {row.code}
                  </td>
                  <td className="py-3 px-4 text-sm font-medium text-slate-900 dark:text-slate-200">
                    {row.name}
                  </td>
                  <td className="py-3 px-4 text-sm text-slate-600 dark:text-slate-400 max-w-xl truncate" title={row.description}>
                    {row.description}
                  </td>
                </tr>
              ))}
              {paginatedData.length === 0 && (
                <tr>
                  <td colSpan={3} className="py-8 text-center text-slate-500 dark:text-slate-400">
                    No data found.
                  </td>
                </tr>
              )}
</tbody>
          </table>
          </div>
          {totalPages > 1 && (
            <div className="flex items-center justify-between px-4 py-3 border-t border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-[#16181d] flex-shrink-0">
              <div className="text-sm text-slate-500 dark:text-slate-400">
                Showing {((currentPage - 1) * ITEMS_PER_PAGE) + 1} to {Math.min(currentPage * ITEMS_PER_PAGE, displayedData.length)} of {displayedData.length} entries
              </div>
              <div className="flex items-center gap-2">
                <button 
                  onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                  disabled={currentPage === 1}
                  className="px-3 py-1 text-sm rounded-md border border-slate-200 dark:border-slate-700 disabled:opacity-50 hover:bg-slate-200 dark:hover:bg-slate-800 transition-colors"
                >
                  Previous
                </button>
                <div className="text-sm font-medium px-2">Page {currentPage} of {totalPages}</div>
                <button 
                  onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                  disabled={currentPage === totalPages}
                  className="px-3 py-1 text-sm rounded-md border border-slate-200 dark:border-slate-700 disabled:opacity-50 hover:bg-slate-200 dark:hover:bg-slate-800 transition-colors"
                >
                  Next
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
