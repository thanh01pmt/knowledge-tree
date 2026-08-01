import React, { useState, useEffect } from 'react';
import { Compass, Sparkles, Search, Network, Check, X, ArrowRight } from 'lucide-react';

export default function OnboardingTour() {
  const [step, setStep] = useState(0);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const seen = localStorage.getItem('kt_onboarding_seen');
    if (!seen) {
      setIsVisible(true);
    }
  }, []);

  const handleFinish = () => {
    localStorage.setItem('kt_onboarding_seen', 'true');
    setIsVisible(false);
  };

  if (!isVisible) return null;

  const tourSteps = [
    {
      title: "Welcome to Knowledge Tree 3D",
      desc: "Explore multi-level curriculum taxonomy, concept relationships, and CS2023 knowledge area mapping in interactive 3D.",
      icon: <Sparkles className="w-8 h-8 text-blue-400 mb-2" />
    },
    {
      title: "1. Search & Orbit Navigation",
      desc: "Use the Search bar to jump to any subject or concept. Drag with Left-Click to orbit in 3D, and Right-Click or 2 fingers to pan.",
      icon: <Search className="w-8 h-8 text-purple-400 mb-2" />
    },
    {
      title: "2. Double-Click to Drill Down",
      desc: "Double-click any node to expand or collapse its sub-topics dynamically without cluttering your view.",
      icon: <Compass className="w-8 h-8 text-emerald-400 mb-2" />
    },
    {
      title: "3. Prerequisite Pathways",
      desc: "Toggle 'Show Prerequisites' in the left Control Panel to visualize unlock requirements (Green = Unlocks next, Red = Required prior knowledge).",
      icon: <Network className="w-8 h-8 text-amber-400 mb-2" />
    }
  ];

  const current = tourSteps[step];

  return (
    <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-[#1e2227] border border-slate-700 rounded-2xl max-w-sm w-full p-6 shadow-2xl relative text-slate-200 text-center flex flex-col items-center">
        <button 
          onClick={handleFinish}
          className="absolute top-3 right-3 p-1 text-slate-500 hover:text-white rounded-lg hover:bg-slate-800 transition-colors"
        >
          <X className="w-4 h-4" />
        </button>

        {current.icon}
        <h3 className="text-base font-bold text-white mb-2">{current.title}</h3>
        <p className="text-xs text-slate-400 leading-relaxed mb-6">{current.desc}</p>

        {/* Dots Indicator */}
        <div className="flex items-center justify-center gap-1.5 mb-6">
          {tourSteps.map((_, idx) => (
            <span 
              key={idx} 
              className={`h-1.5 rounded-full transition-all ${idx === step ? 'w-6 bg-blue-500' : 'w-1.5 bg-slate-700'}`}
            />
          ))}
        </div>

        {/* Buttons */}
        <div className="flex items-center gap-2 w-full">
          {step < tourSteps.length - 1 ? (
            <>
              <button 
                onClick={handleFinish}
                className="flex-1 py-2 text-xs font-semibold text-slate-400 hover:text-slate-200 transition-colors"
              >
                Skip
              </button>
              <button 
                onClick={() => setStep(step + 1)}
                className="flex-1 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-semibold flex items-center justify-center gap-1 transition-colors"
              >
                Next <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </>
          ) : (
            <button 
              onClick={handleFinish}
              className="w-full py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold flex items-center justify-center gap-1 transition-colors"
            >
              Get Started <Check className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
