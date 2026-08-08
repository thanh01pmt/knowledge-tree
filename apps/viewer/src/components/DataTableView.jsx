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
  const [selectedContext, setSelectedContext] = useState(null); // { type, item }

  // Simple lineage tracking to find direct parents/children
  const isRelated = (item, type, context) => {
    if (!context || !context.item) return true;
    
    // Same item
    if (item.code === context.item.code) return true;
    
    // If same type, return true (show all siblings so user can switch selection)
    if (type === context.type) return true;

    // We can use linksBySource to find all descendants, and linksByTarget to find all ancestors
    const isDescendant = (startCode, targetCode) => {
      if (!linksBySource) return false;
      const visited = new Set();
      const queue = [startCode];
      while (queue.length > 0) {
        const curr = queue.shift();
        if (curr === targetCode) return true;
        if (linksBySource[curr]) {
          linksBySource[curr].forEach(child => {
            if (!visited.has(child)) {
              visited.add(child);
              queue.push(child);
            }
          });
        }
      }
      return false;
    };

    const isAncestor = (startCode, targetCode) => {
      if (!linksByTarget) return false;
      const visited = new Set();
      const queue = [startCode];
      while (queue.length > 0) {
        const curr = queue.shift();
        if (curr === targetCode) return true;
        if (linksByTarget[curr]) {
          linksByTarget[curr].forEach(parent => {
            if (!visited.has(parent)) {
              visited.add(parent);
              queue.push(parent);
            }
          });
        }
      }
      return false;
    };

    // Check if the item is a descendant of the selected context
    if (isDescendant(context.item.code, item.code)) return true;
    
    // Check if the item is an ancestor of the selected context
    if (isAncestor(context.item.code, item.code)) return true;

    return false;
  };

  
  const getFilteredCount = (tabId) => {
    if (!rawTreeData || !rawTreeData[tabId]) return 0;
    if (!selectedContext) return rawTreeData[tabId].length;
    return rawTreeData[tabId].filter(item => isRelated(item, tabId, selectedContext)).length;
  };

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
  }, [rawTreeData, activeTab, searchTerm, selectedContext, linksBySource, linksByTarget]);

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
              <button onClick={() => setSelectedContext(null)} className="ml-2 hover:text-blue-900 dark:hover:text-blue-100">
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
            onChange={e => setSearchTerm(e.target.value)}
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
             const count = getFilteredCount(tab.id);
             return (
              <button
                key={tab.id}
                onClick={() => { setActiveTab(tab.id); setSearchTerm(''); }}
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
        <div className="flex-1 overflow-auto bg-white dark:bg-[#0f1115]">
          <table className="w-full text-left border-collapse">
            <thead className="sticky top-0 bg-slate-100 dark:bg-[#1a1d21] border-b border-slate-200 dark:border-slate-800 shadow-sm z-10">
              <tr>
                <th className="py-3 px-4 text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider w-48">Code</th>
                <th className="py-3 px-4 text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider w-1/3">Name</th>
                <th className="py-3 px-4 text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Description</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800/50">
              {displayedData.map((row) => (
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
              {displayedData.length === 0 && (
                <tr>
                  <td colSpan={3} className="py-8 text-center text-slate-500 dark:text-slate-400">
                    No data found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
