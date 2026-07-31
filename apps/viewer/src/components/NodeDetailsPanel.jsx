import React, { useMemo, useEffect } from 'react';
import { ChevronRight, ArrowLeft, ArrowRight, ChevronLeft, LayoutGrid, Layers, Hexagon, Circle, Square, Minus, Map } from 'lucide-react';

const LevelIcon = ({ level, className }) => {
  switch(level) {
    case 'field': return <Map className={className} />;
    case 'subject': return <Layers className={className} />;
    case 'category': return <LayoutGrid className={className} />;
    case 'topic': return <Hexagon className={className} />;
    case 'concept': return <Circle className={className} />;
    default: return <Square className={className} />;
  }
};

export default function NodeDetailsPanel({
  selectedNode,
  onNodeSelect,
  graphData,
  linksBySource,
  linksByTarget,
  history,
  historyIndex,
  onNavigateHistory
}) {
  const breadcrumbs = useMemo(() => {
    if (!selectedNode) return [];
    const path = [];
    let currentId = selectedNode.id;
    while (currentId) {
      const node = graphData.nodes.find(n => n.id === currentId);
      if (node) {
        path.unshift(node);
        const parents = linksByTarget[currentId] || [];
        currentId = parents.length > 0 ? parents[0] : null;
      } else {
        break;
      }
    }
    return path;
  }, [selectedNode, linksByTarget, graphData.nodes]);

  const { prevSibling, nextSibling } = useMemo(() => {
    if (!selectedNode) return { prevSibling: null, nextSibling: null };
    const parents = linksByTarget[selectedNode.id] || [];
    if (parents.length === 0) {
      const fields = graphData.nodes.filter(n => n.level === selectedNode.level);
      const idx = fields.findIndex(n => n.id === selectedNode.id);
      return {
        prevSibling: idx > 0 ? fields[idx - 1] : null,
        nextSibling: idx < fields.length - 1 ? fields[idx + 1] : null
      };
    }
    
    const parentId = parents[0];
    const siblingIds = linksBySource[parentId] || [];
    const siblings = siblingIds.map(id => graphData.nodes.find(n => n.id === id)).filter(Boolean);
    
    const idx = siblings.findIndex(n => n.id === selectedNode.id);
    return {
      prevSibling: idx > 0 ? siblings[idx - 1] : null,
      nextSibling: idx < siblings.length - 1 ? siblings[idx + 1] : null
    };
  }, [selectedNode, linksByTarget, linksBySource, graphData.nodes]);

  const children = useMemo(() => {
    if (!selectedNode) return [];
    const childIds = linksBySource[selectedNode.id] || [];
    return childIds.map(id => graphData.nodes.find(n => n.id === id)).filter(Boolean);
  }, [selectedNode, linksBySource, graphData.nodes]);

  useEffect(() => {
    if (!selectedNode) return;
    
    const handleKeyDown = (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

      switch(e.key) {
        case 'ArrowUp':
          e.preventDefault();
          if (breadcrumbs.length > 1) {
            onNodeSelect(breadcrumbs[breadcrumbs.length - 2]);
          }
          break;
        case 'ArrowLeft':
          e.preventDefault();
          if (prevSibling) onNodeSelect(prevSibling);
          break;
        case 'ArrowRight':
          e.preventDefault();
          if (nextSibling) onNodeSelect(nextSibling);
          break;
        case 'ArrowDown':
          e.preventDefault();
          if (children.length > 0) onNodeSelect(children[0]);
          break;
        default:
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [selectedNode, breadcrumbs, prevSibling, nextSibling, children, onNodeSelect]);

  if (!selectedNode) return null;

  const canGoBack = historyIndex > 0;
  const canGoForward = historyIndex < history.length - 1;

  return (
    <div className="h-full w-[360px] bg-[#1a1d21] border-l border-slate-800 flex flex-col text-slate-300 z-10 transition-all duration-300 flex-shrink-0 shadow-2xl relative">
      <div className="flex items-center justify-between p-3 border-b border-slate-800 bg-[#1e2227] flex-shrink-0">
        <div className="flex items-center gap-1">
          <button 
            onClick={() => onNavigateHistory('back')}
            disabled={!canGoBack}
            className={`p-1.5 rounded-md transition-colors ${canGoBack ? 'text-slate-300 hover:bg-slate-700 hover:text-white' : 'text-slate-600 cursor-not-allowed'}`}
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <button 
            onClick={() => onNavigateHistory('forward')}
            disabled={!canGoForward}
            className={`p-1.5 rounded-md transition-colors ${canGoForward ? 'text-slate-300 hover:bg-slate-700 hover:text-white' : 'text-slate-600 cursor-not-allowed'}`}
          >
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
        
        <button 
          onClick={() => onNodeSelect(null)}
          className="text-slate-500 hover:text-slate-300 p-1.5 rounded-md hover:bg-slate-700 transition-colors text-xs font-semibold uppercase tracking-wider"
        >
          Close
        </button>
      </div>

      <div className="flex-1 overflow-y-auto custom-scrollbar flex flex-col">
        <div className="p-5 flex flex-col gap-4">
          <div className="flex flex-wrap items-center gap-1 text-[11px] text-slate-500 font-medium tracking-wide">
            {breadcrumbs.map((crumb, idx) => (
              <React.Fragment key={crumb.id}>
                {idx > 0 && <ChevronRight className="w-3 h-3 text-slate-600" />}
                <span 
                  className={`cursor-pointer hover:text-blue-400 transition-colors ${idx === breadcrumbs.length - 1 ? 'text-slate-300 cursor-default hover:text-slate-300' : ''}`}
                  onClick={() => idx !== breadcrumbs.length - 1 && onNodeSelect(crumb)}
                >
                  {crumb.name}
                </span>
              </React.Fragment>
            ))}
          </div>

          <div className="flex items-start justify-between gap-4 mt-1">
            <h2 className="text-2xl font-bold text-slate-100 leading-tight">
              {selectedNode.name}
            </h2>
            <div className="flex items-center gap-1 mt-1 bg-slate-800/50 rounded-lg p-0.5 border border-slate-700">
              <button 
                onClick={() => onNodeSelect(prevSibling)}
                disabled={!prevSibling}
                className={`p-1 rounded transition-colors ${prevSibling ? 'hover:bg-slate-600 text-slate-300' : 'text-slate-600 cursor-not-allowed'}`}
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <button 
                onClick={() => onNodeSelect(nextSibling)}
                disabled={!nextSibling}
                className={`p-1 rounded transition-colors ${nextSibling ? 'hover:bg-slate-600 text-slate-300' : 'text-slate-600 cursor-not-allowed'}`}
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-semibold uppercase tracking-widest">
              <LevelIcon level={selectedNode.level} className="w-3.5 h-3.5" />
              {selectedNode.level}
            </div>
          </div>

          {selectedNode.description && (
            <p className="text-sm text-slate-400 leading-relaxed mt-2 bg-[#2a2f36]/50 p-4 rounded-xl border border-slate-800/80">
              {selectedNode.description}
            </p>
          )}
        </div>

        {children.length > 0 ? (
          <div className="flex flex-col border-t border-slate-800/50">
            <div className="px-5 pt-5 pb-3 flex items-center justify-between">
              <div className="text-[11px] font-semibold text-slate-500 uppercase tracking-widest">
                Contents ({children.length})
              </div>
            </div>
            <div className="flex flex-col px-3 pb-5 gap-1.5">
              {children.map(child => (
                <button
                  key={child.id}
                  onClick={() => onNodeSelect(child)}
                  className="flex items-center gap-3 p-3 rounded-xl hover:bg-[#2a2f36] border border-transparent hover:border-slate-700/50 transition-all text-left group"
                >
                  <div className="p-2 rounded-lg bg-slate-800 text-slate-400 group-hover:bg-slate-700 group-hover:text-blue-400 transition-colors">
                    <LevelIcon level={child.level} className="w-4 h-4" />
                  </div>
                  <div className="flex-1 overflow-hidden">
                    <div className="text-sm font-medium text-slate-300 group-hover:text-slate-100 truncate transition-colors">
                      {child.name}
                    </div>
                    <div className="text-[10px] text-slate-500 uppercase tracking-wider mt-0.5">
                      {child.level}
                    </div>
                  </div>
                  <ChevronRight className="w-4 h-4 text-slate-600 opacity-0 group-hover:opacity-100 transform group-hover:translate-x-1 transition-all" />
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center p-8 text-center text-slate-500 border-t border-slate-800/50">
            <Minus className="w-8 h-8 mb-3 opacity-20" />
            <p className="text-sm">No child nodes available.</p>
          </div>
        )}
      </div>
    </div>
  );
}
