import React, { useState } from 'react';
import { TopBar } from './components/TopBar';
import { BottomNav, NavTab } from './components/BottomNav';
import { HomeView } from './components/HomeView';
import { DumpView } from './components/DumpView';
import { ToolsView } from './components/ToolsView';
import { SolutionsView } from './components/SolutionsView';
import { OffersView } from './components/OffersView';
import { FavoritesView } from './components/FavoritesView';
import { TechUtilsView } from './components/TechUtilsView';
import { SearchOverlay } from './components/SearchOverlay';
import { useFavorites } from './hooks/useFavorites';
import { ItemData } from './data/hmaxData';

export default function App() {
  const [activeTab, setActiveTab] = useState<NavTab | 'offers'>('home');
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const { favorites, toggleFavorite, isFavorite } = useFavorites();

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => {
      setToastMessage((current) => (current === msg ? null : current));
    }, 2200);
  };

  const handleClearFavorites = () => {
    if (window.confirm('هل أنت متأكد من مسح جميع العناصر المحفوظة في المفضلة؟')) {
      localStorage.removeItem('hmax_favorites_v1');
      window.location.reload();
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0e1a] text-slate-100 flex flex-col selection:bg-[#00b4ff]/30 selection:text-white pb-20 sm:pb-12">
      {/* Top Application Bar */}
      <TopBar
        activeTab={activeTab}
        onSelectTab={(tab) => setActiveTab(tab)}
        onSearchClick={() => setIsSearchOpen(true)}
        onCopyToast={showToast}
        favoritesCount={favorites.length}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-6xl w-full mx-auto px-3 sm:px-6 py-4">
        {/* Quick Horizontal Category Switcher on Tablet & Desktop */}
        <div className="hidden sm:flex items-center gap-2 mb-4 p-1.5 rounded-2xl bg-slate-900/60 border border-slate-800/80 overflow-x-auto no-scrollbar">
          {[
            { id: 'home', label: '⚡ الرئيسية' },
            { id: 'dump', label: '🗄️ فلاشات DUMP' },
            { id: 'tech_utils', label: '🛠️ أدوات الفني' },
            { id: 'tools', label: '🧰 البرامج والتعاريف' },
            { id: 'solutions', label: '💡 الحلول والثغرات' },
            { id: 'offers', label: '🔥 العروض والاشتراكات' },
            { id: 'favorites', label: `⭐ المفضلة (${favorites.length})` },
          ].map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id as any)}
              className={`px-4 py-2 rounded-xl text-xs font-bold whitespace-nowrap transition ${
                activeTab === item.id
                  ? 'bg-[#00b4ff] text-black shadow-[0_0_15px_rgba(0,180,255,0.3)]'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800'
              }`}
            >
              {item.label}
            </button>
          ))}
        </div>

        {/* View Switcher */}
        {activeTab === 'home' && (
          <HomeView
            onNavigateTab={(tab) => setActiveTab(tab)}
            onCopyToast={showToast}
          />
        )}

        {activeTab === 'dump' && (
          <DumpView
            onCopyToast={showToast}
            isFav={isFavorite}
            onToggleFav={toggleFavorite}
          />
        )}

        {activeTab === 'tech_utils' && (
          <TechUtilsView onCopyToast={showToast} />
        )}

        {activeTab === 'tools' && (
          <ToolsView
            onCopyToast={showToast}
            isFav={isFavorite}
            onToggleFav={toggleFavorite}
          />
        )}

        {activeTab === 'solutions' && (
          <SolutionsView
            onCopyToast={showToast}
            isFav={isFavorite}
            onToggleFav={toggleFavorite}
          />
        )}

        {activeTab === 'offers' && (
          <OffersView
            onCopyToast={showToast}
            isFav={isFavorite}
            onToggleFav={toggleFavorite}
          />
        )}

        {activeTab === 'favorites' && (
          <FavoritesView
            favorites={favorites}
            onToggleFav={toggleFavorite}
            onCopyToast={showToast}
            onClearAll={handleClearFavorites}
          />
        )}
      </main>

      {/* Floating Bottom Navigation Bar (Optimized for Mobile Ergonomics) */}
      <BottomNav
        activeTab={activeTab as NavTab}
        onTabChange={(tab) => setActiveTab(tab)}
        favoritesCount={favorites.length}
      />

      {/* Search Modal Overlay */}
      <SearchOverlay
        isOpen={isSearchOpen}
        onClose={() => setIsSearchOpen(false)}
        onCopyToast={showToast}
        isFav={isFavorite}
        onToggleFav={toggleFavorite}
      />

      {/* Modern Floating Toast Notification */}
      {toastMessage && (
        <div className="fixed bottom-20 sm:bottom-6 left-1/2 -translate-x-1/2 z-50 px-4 py-2.5 rounded-full bg-emerald-500 text-black font-black text-xs shadow-2xl flex items-center gap-2 animate-in fade-in slide-in-from-bottom-3 duration-200 pointer-events-none">
          <span>✅</span>
          <span>{toastMessage}</span>
        </div>
      )}
    </div>
  );
}
