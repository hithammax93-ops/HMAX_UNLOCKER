import React from 'react';
import { Home, Database, Wrench, Lightbulb, Sparkles, Terminal } from 'lucide-react';

export type NavTab = 'home' | 'dump' | 'tech_utils' | 'tools' | 'solutions' | 'offers' | 'favorites';

interface BottomNavProps {
  activeTab: NavTab;
  onTabChange: (tab: NavTab) => void;
  favoritesCount?: number;
}

export const BottomNav: React.FC<BottomNavProps> = ({ activeTab, onTabChange }) => {
  const tabs = [
    { id: 'home' as NavTab, label: 'الرئيسية', icon: Home },
    { id: 'dump' as NavTab, label: 'DUMP', icon: Database },
    { id: 'tech_utils' as NavTab, label: 'أدوات الفني', icon: Terminal },
    { id: 'solutions' as NavTab, label: 'الحلول', icon: Lightbulb },
    { id: 'offers' as NavTab, label: 'العروض', icon: Sparkles },
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-40 bg-[#0a0e1a]/95 backdrop-blur-xl border-t border-slate-800/80 pb-safe sm:hidden">
      <div className="max-w-md mx-auto grid grid-cols-5 items-center h-16 px-1">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;

          return (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className="relative flex flex-col items-center justify-center h-full min-h-[44px] min-w-[44px] py-1 text-center transition-colors group"
            >
              <div
                className={`p-1 rounded-xl transition-all ${
                  isActive
                    ? 'text-[#00b4ff] bg-[#00b4ff]/15 scale-110 shadow-[0_0_12px_rgba(0,180,255,0.3)]'
                    : 'text-slate-400 group-hover:text-slate-200'
                }`}
              >
                <Icon className="w-5 h-5" />
              </div>
              <span
                className={`text-[10px] font-medium tracking-tight mt-1 transition-colors ${
                  isActive ? 'text-[#00b4ff] font-bold' : 'text-slate-400'
                }`}
              >
                {tab.label}
              </span>
            </button>
          );
        })}
      </div>
    </nav>
  );
};
