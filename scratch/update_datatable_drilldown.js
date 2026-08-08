const fs = require('fs');
const file = 'apps/viewer/src/components/DataTableView.jsx';
let code = fs.readFileSync(file, 'utf8');

// 1. In isRelated, if type === context.type, return true (don't filter siblings)
const oldIsRelated = `    // If same type but not same item, return false (don't show siblings)
    if (type === context.type) return false;`;
const newIsRelated = `    // If same type, return true (show all siblings so user can switch selection)
    if (type === context.type) return true;`;
code = code.replace(oldIsRelated, newIsRelated);

// 2. Add an auto-switch logic on row click
const oldRowClick = `onClick={() => setSelectedContext({ type: activeTab, item: row })}`;
const newRowClick = `onClick={() => {
                    setSelectedContext({ type: activeTab, item: row });
                    // Auto switch to next logical tab
                    const tabOrder = ['fields', 'subjects', 'categories', 'topics', 'concepts', 'learning_objectives'];
                    const currentIndex = tabOrder.indexOf(activeTab);
                    if (currentIndex !== -1 && currentIndex < tabOrder.length - 1) {
                      setActiveTab(tabOrder[currentIndex + 1]);
                      setSearchTerm('');
                    }
                  }}`;
code = code.replace(oldRowClick, newRowClick);

// 3. Highlight the selected row
const oldTrClass = `className="hover:bg-slate-50 dark:hover:bg-[#1a1d21] transition-colors cursor-pointer group"`;
const newTrClass = `className={\`transition-colors cursor-pointer group \${selectedContext && selectedContext.item.code === row.code ? 'bg-blue-50/50 dark:bg-blue-900/20' : 'hover:bg-slate-50 dark:hover:bg-[#1a1d21]'}\`}`;
code = code.replace(oldTrClass, newTrClass);

fs.writeFileSync(file, code);
