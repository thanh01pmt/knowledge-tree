const fs = require('fs');
const file = 'apps/viewer/src/components/DataTableView.jsx';
let code = fs.readFileSync(file, 'utf8');

// 1. Optimize counts with useMemo
const newCountsLogic = `
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
  }, [rawTreeData, selectedContext, linksBySource, linksByTarget]);
`;

code = code.replace(
  /const getFilteredCount = [\s\S]*?};/,
  newCountsLogic.trim()
);

code = code.replace(
  "const count = getFilteredCount(tab.id);",
  "const count = tabCounts[tab.id] || 0;"
);

// 2. Add Pagination State
code = code.replace(
  "const [selectedContext, setSelectedContext] = useState(null);",
  "const [selectedContext, setSelectedContext] = useState(null);\n  const [currentPage, setCurrentPage] = useState(1);\n  const ITEMS_PER_PAGE = 50;"
);

// Reset page when tab or search changes
code = code.replace(
  "setActiveTab(tab.id); setSearchTerm('');",
  "setActiveTab(tab.id); setSearchTerm(''); setCurrentPage(1);"
);
code = code.replace(
  "onChange={e => setSearchTerm(e.target.value)}",
  "onChange={e => { setSearchTerm(e.target.value); setCurrentPage(1); }}"
);
code = code.replace(
  "setActiveTab(tabOrder[currentIndex + 1]);\n                      setSearchTerm('');",
  "setActiveTab(tabOrder[currentIndex + 1]);\n                      setSearchTerm('');\n                      setCurrentPage(1);"
);
code = code.replace(
  "setSelectedContext(null)",
  "setSelectedContext(null); setCurrentPage(1);" // in clear filter button
);


// 3. Slice the data for rendering
code = code.replace(
  "return data;\n  }, [rawTreeData, activeTab, searchTerm, selectedContext, linksBySource, linksByTarget]);",
  "return data;\n  }, [rawTreeData, activeTab, searchTerm, selectedContext, linksBySource, linksByTarget]);\n\n  const paginatedData = displayedData.slice((currentPage - 1) * ITEMS_PER_PAGE, currentPage * ITEMS_PER_PAGE);\n  const totalPages = Math.ceil(displayedData.length / ITEMS_PER_PAGE);"
);

// 4. Update rendering to use paginatedData and add pagination UI
code = code.replace(
  "displayedData.map((row) => (",
  "paginatedData.map((row) => ("
);
code = code.replace(
  "displayedData.length === 0",
  "paginatedData.length === 0"
);

const paginationUI = `
        <div className="flex-1 overflow-auto bg-white dark:bg-[#0f1115] flex flex-col">
          <div className="flex-1 overflow-auto">
            <table className="w-full text-left border-collapse">
`;
code = code.replace(
  '<div className="flex-1 overflow-auto bg-white dark:bg-[#0f1115]">\n          <table className="w-full text-left border-collapse">',
  paginationUI.trim()
);

const paginationFooter = `
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
`;
code = code.replace(
  /            <\/tbody>\n          <\/table>\n        <\/div>/,
  paginationFooter.trim()
);

fs.writeFileSync(file, code);
