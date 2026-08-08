import React, { useState, useEffect, useRef } from 'react';
import { X, Send, Bot, Sparkles } from 'lucide-react';

export default function ChatSidebar({ isOpen, onClose }) {
  const [width, setWidth] = useState(350);
  const isResizing = useRef(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;
    
    const userMessage = { role: 'user', content: input };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput('');
    setIsLoading(true);

    try {
      // In local dev without Netlify CLI, this might fail unless proxied.
      // We call the Netlify function endpoint we defined.
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: newMessages })
      });

      if (!response.ok) {
        throw new Error('API request failed');
      }

      // Handle streaming response
      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      
      setMessages(prev => [...prev, { role: 'assistant', content: '' }]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');
        
        for (const line of lines) {
          if (line.startsWith('data: ') && line !== 'data: [DONE]') {
            try {
              const data = JSON.parse(line.slice(6));
              const text = data.choices[0]?.delta?.content || '';
              if (text) {
                setMessages(prev => {
                  const updated = [...prev];
                  const last = updated[updated.length - 1];
                  last.content += text;
                  return updated;
                });
              }
            } catch (e) {
              // Ignore parse errors on incomplete chunks
            }
          }
        }
      }
    } catch (error) {
      console.error(error);
      setMessages(prev => [...prev, { role: 'system', content: 'Lỗi kết nối. Vui lòng kiểm tra lại cấu hình Netlify.' }]);
    } finally {
      setIsLoading(false);
    }
  };


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

      {/* Chat Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-4 custom-scrollbar">
        <div className="flex gap-3 text-sm">
          <div className="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center flex-shrink-0">
            <Sparkles className="w-4 h-4 text-blue-400" />
          </div>
          <div className="bg-slate-800 rounded-lg p-3 text-slate-300 leading-relaxed border border-slate-700">
            Xin chào! Tôi có thể giúp bạn tạo một lộ trình học tập tùy chỉnh dựa trên mục tiêu và nền tảng của bạn. Bạn muốn học về chủ đề gì?
          </div>
        </div>
        
        {messages.map((msg, index) => (
          <div key={index} className={`flex gap-3 text-sm ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
            {msg.role === 'assistant' && (
              <div className="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center flex-shrink-0 mt-1">
                <Bot className="w-4 h-4 text-blue-400" />
              </div>
            )}
            <div className={`rounded-lg p-3 leading-relaxed max-w-[85%] whitespace-pre-wrap ${
              msg.role === 'user' 
                ? 'bg-blue-600 text-white' 
                : msg.role === 'system'
                  ? 'bg-red-500/20 text-red-200 border border-red-500/50'
                  : 'bg-slate-800 text-slate-300 border border-slate-700'
            }`}>
              {msg.content}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex gap-3 text-sm">
            <div className="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center flex-shrink-0">
              <Sparkles className="w-4 h-4 text-blue-400 animate-pulse" />
            </div>
            <div className="bg-slate-800 rounded-lg p-3 text-slate-400 leading-relaxed border border-slate-700 flex items-center gap-1">
              <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce"></span>
              <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
              <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-3 border-t border-slate-800 flex-shrink-0">
        <div className="relative">
          <textarea 
            className="w-full bg-[#2a2f36] border border-slate-700 text-slate-200 text-sm rounded-lg pl-3 pr-10 py-2.5 focus:outline-none focus:border-blue-500 transition-colors resize-none custom-scrollbar"
            placeholder="Mô tả mục tiêu của bạn..."
            rows="2"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
          />
          <button 
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
            className="absolute right-2 bottom-2 p-1.5 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 disabled:text-slate-400 text-white rounded-md transition-colors"
          >
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
