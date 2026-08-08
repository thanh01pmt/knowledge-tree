import React from 'react';
import { Network, Target, FolderTree, MessageSquare } from 'lucide-react';

export default function ActivityBar({ viewMode, setViewMode, toggleChat }) {
  const items = [
    { id: 'knowledge', icon: Network, title: 'Knowledge Tree' },
    { id: 'roadmap', icon: Target, title: 'Action Roadmap' },
    { id: 'project-graph', icon: FolderTree, title: 'Project Graph' },
  ];

  return (
    <div className="w-12 h-full bg-[#1e293b] flex flex-col items-center py-4 border-r border-slate-800 z-50 flex-shrink-0">
      <div className="flex-1 flex flex-col gap-4 w-full items-center">
        {items.map(item => (
          <button
            key={item.id}
            onClick={() => setViewMode(item.id)}
            title={item.title}
            className={`p-2 rounded-md transition-colors ${
              viewMode === item.id 
                ? 'text-white bg-slate-700' 
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
          >
            <item.icon className="w-5 h-5" />
          </button>
        ))}
      </div>
      
      <div className="flex flex-col gap-4 w-full items-center pb-2">
        <button
          onClick={toggleChat}
          title="AI Roadmap Builder"
          className="p-2 rounded-md text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
        >
          <MessageSquare className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
}
