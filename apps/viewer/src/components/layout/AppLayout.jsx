import React, { useState } from 'react';
import ActivityBar from './ActivityBar';
import ChatSidebar from './ChatSidebar';

export default function AppLayout({ viewMode, setViewMode, theme, setTheme, children }) {
  const [isChatOpen, setIsChatOpen] = useState(false);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  return (
    <div className={`flex h-screen w-screen bg-slate-50 dark:bg-[#0f172a] overflow-hidden text-slate-900 dark:text-slate-200 font-sans ${theme === 'dark' ? 'dark' : ''}`}>
      {/* VS Code Style Activity Bar */}
      <ActivityBar 
        viewMode={viewMode} 
        setViewMode={setViewMode} 
        toggleChat={toggleChat}
        theme={theme}
        setTheme={setTheme}
      />

      {/* Main Content Area (which may contain its own sidebars like ControlPanel) */}
      <div className="flex-1 flex min-w-0 h-full relative">
        {children}
      </div>

      {/* Global Right Sidebar for Chat */}
      <ChatSidebar isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />
    </div>
  );
}
