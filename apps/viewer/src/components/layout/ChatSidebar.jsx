import React, { useState, useEffect, useRef } from 'react';
import { X, Send, Bot, Sparkles } from 'lucide-react';

export default function ChatSidebar({ isOpen, onClose }) {
  const [width, setWidth] = useState(350);
  const isResizing = useRef(false);

  useEffect(() => {
    const handleMouseMove = (e) => {
      if (!isResizing.current) return;
      // Calculate new width based on mouse position from the right edge
      const newWidth = document.body.clientWidth - e.clientX;
      if (newWidth > 250 && newWidth < 800) {
        setWidth(newWidth);
      }
    };

    const handleMouseUp = () => {
      isResizing.current = false;
      document.body.style.cursor = 'default';
    };

    if (isOpen) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div 
      className="h-full bg-[#1a1d21] border-l border-slate-800 flex flex-col z-40 relative flex-shrink-0 transition-all duration-0"
      style={{ width: `${width}px` }}
    >
      {/* Resize Handle */}
      <div 
        className="absolute left-0 top-0 bottom-0 w-1.5 cursor-col-resize hover:bg-blue-500/50 active:bg-blue-500 transition-colors z-50"
        onMouseDown={(e) => {
          isResizing.current = true;
          document.body.style.cursor = 'col-resize';
          e.preventDefault();
        }}
      />

      {/* Header */}
      <div className="flex items-center justify-between p-3 border-b border-slate-800 flex-shrink-0">
        <div className="flex items-center gap-2 text-slate-200 font-semibold">
          <Bot className="w-4 h-4 text-blue-400" />
          <span className="text-sm">AI Roadmap Builder</span>
        </div>
        <button 
          onClick={onClose}
          className="p-1.5 text-slate-500 hover:text-slate-300 hover:bg-slate-800 rounded-md transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Chat Messages Area (Placeholder) */}
      <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-4">
        <div className="flex gap-3 text-sm">
          <div className="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center flex-shrink-0">
            <Sparkles className="w-4 h-4 text-blue-400" />
          </div>
          <div className="bg-slate-800 rounded-lg p-3 text-slate-300 leading-relaxed border border-slate-700">
            Xin chào! Tôi có thể giúp bạn tạo một lộ trình học tập tùy chỉnh dựa trên mục tiêu và nền tảng của bạn. Bạn muốn học về chủ đề gì?
          </div>
        </div>
      </div>

      {/* Input Area */}
      <div className="p-3 border-t border-slate-800 flex-shrink-0">
        <div className="relative">
          <textarea 
            className="w-full bg-[#2a2f36] border border-slate-700 text-slate-200 text-sm rounded-lg pl-3 pr-10 py-2.5 focus:outline-none focus:border-blue-500 transition-colors resize-none custom-scrollbar"
            placeholder="Mô tả mục tiêu của bạn..."
            rows="2"
          />
          <button className="absolute right-2 bottom-2 p-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-md transition-colors">
            <Send className="w-4 h-4" />
          </button>
        </div>
        <div className="text-[10px] text-slate-500 text-center mt-2">
          AI có thể mắc sai lầm. Hãy kiểm tra lại lộ trình được tạo.
        </div>
      </div>
    </div>
  );
}
