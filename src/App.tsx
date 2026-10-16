import React, { useEffect, useState } from 'react';
import { TopBar } from './components/TopBar';
import { BottomNav, NavTab } from './components/BottomNav';
import { HomeView } from './components/HomeView';
import { DumpView } from './components/DumpView';
import { ToolsView, ToolsSubCategory } from './components/ToolsView';
import { SolutionsView, SubSection } from './components/SolutionsView';
import { OffersView, OffersCategory } from './components/OffersView';
import { FavoritesView } from './components/FavoritesView';
import { TechUtilsView, TechTab } from './components/TechUtilsView';
import { SearchOverlay } from './components/SearchOverlay';
import { useFavorites } from './hooks/useFavorites';
import { ItemData } from './data/hmaxData';

export default function App() {
  const [activeTab, setActiveTab] = useState<NavTab | 'offers'>('home');
  const [techSubTab, setTechSubTab] = useState<TechTab>('commands');
  const [toolsCategory, setToolsCategory] = useState<ToolsSubCategory>('tools');
  const [offersCategory, setOffersCategory] = useState<OffersCategory>('offers');
  const [solutionsSection, setSolutionsSection] = useState<SubSection>('diagnostic');
  const [dumpBrand, setDumpBrand] = useState<string | null>(null);

  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);
  const [largeText, setLargeText] = useState(() => {
    try { return localStorage.getItem('hmax_large_text_v1') === 'true'; }
    catch { return false; }
  });

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

  const handleNavigate = (
    tab: NavTab | 'offers',
    subSection?: string,
    extra?: string
  ) => {
    setActiveTab(tab);
    if (tab === 'tech_utils' && subSection) {
      setTechSubTab(subSection as TechTab);
    }
    if (tab === 'tools' && subSection) {
      setToolsCategory(subSection as ToolsSubCategory);
    }
    if (tab === 'offers' && subSection) {
      setOffersCategory(subSection as OffersCategory);
    }
    if (tab === 'solutions' && subSection) {
      setSolutionsSection(subSection as SubSection);
    }
    if (tab === 'dump') {
      setDumpBrand(extra || null);
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  useEffect(() => {
    document.documentElement.dataset.textScale = largeText ? 'large' : 'normal';
    try { localStorage.setItem('hmax_large_text_v1', String(largeText)); }
    catch { /* Preference persistence is optional. */ }
  }, [largeText]);

  return (
    <div className="min-h-screen bg-[#0a0e1a] text-slate-100 flex flex-col selection:bg-[#00b4ff]/30 selection:text-white pb-20 sm:pb-12">
      {/* Top Application Bar */}
      <TopBar
        activeTab={activeTab}
        onSelectTab={(tab) => handleNavigate(tab)}
        onSearchClick={() => setIsSearchOpen(true)}
        onCopyToast={showToast}
        favoritesCount={favorites.length}
        largeText={largeText}
        onToggleLargeText={() => setLargeText((value) => !value)}
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
              onClick={() => handleNavigate(item.id as any)}
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
            onNavigateTab={handleNavigate}
            onCopyToast={showToast}
          />
        )}

        {activeTab === 'dump' && (
          <DumpView
            onCopyToast={showToast}
            isFav={isFavorite}
            onToggleFav={toggleFavorite}
            initialBrand={dumpBrand}
          />
        )}

        {activeTab === 'tech_utils' && (
          <TechUtilsView
            onCopyToast={showToast}
            initialTab={techSubTab}
          />
        )}

        {activeTab === 'tools' && (
          <ToolsView
            onCopyToast={showToast}
            isFav={isFavorite}
            onToggleFav={toggleFavorite}
            initialCategory={toolsCategory}
          />
        )}

        {activeTab === 'solutions' && (
          <SolutionsView
            onCopyToast={showToast}
            isFav={isFavorite}
            onToggleFav={toggleFavorite}
            initialSubSection={solutionsSection}
          />
        )}

        {activeTab === 'offers' && (
          <OffersView
            onCopyToast={showToast}
            isFav={isFavorite}
            onToggleFav={toggleFavorite}
            initialCategory={offersCategory}
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
