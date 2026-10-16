import React from 'react';
import { Search, Download, ShieldCheck, Copy, Check, Smartphone, Send, Star } from 'lucide-react';
import { MASTER_PASS } from '../data/hmaxData';
import { usePWAInstall } from '../hooks/usePWAInstall';
import { NavTab } from './BottomNav';

interface TopBarProps {
  activeTab?: NavTab | 'offers';
  onSelectTab?: (tab: NavTab | 'offers') => void;
  onSearchClick: () => void;
  onCopyToast: (msg: string) => void;
  favoritesCount?: number;
}

export const TopBar: React.FC<TopBarProps> = ({
  activeTab = 'home',
  onSelectTab,
  onSearchClick,
  onCopyToast,
  favoritesCount = 0,
}) => {
  const { isInstallable, isInstalled, isIOS, install } = usePWAInstall();
  const [copiedPass, setCopiedPass] = React.useState(false);
  const [showIOSModal, setShowIOSModal] = React.useState(false);

  const handleCopyPassword = (e: React.MouseEvent) => {
    e.stopPropagation();
    navigator.clipboard.writeText(MASTER_PASS);
    setCopiedPass(true);
    onCopyToast(`تم نسخ كلمة السر: ${MASTER_PASS}`);
    setTimeout(() => setCopiedPass(false), 2000);
  };

  const navLinks = [
    { id: 'home', label: 'الرئيسية' },
    { id: 'dump', label: 'فلاشات DUMP' },
    { id: 'tech_utils', label: 'أدوات الفني' },
    { id: 'tools', label: 'البرامج والتعاريف' },
    { id: 'solutions', label: 'الحلول والثغرات' },
    { id: 'offers', label: 'العروض والخدمات' },
    { id: 'favorites', label: `المفضلة (${favoritesCount})` },
  ];

  return (
    <header className="sticky top-0 z-40 bg-[#0a0e1a]/95 backdrop-blur-md border-b border-slate-800/80 px-3 sm:px-6 py-2.5">
      <div className="max-w-6xl mx-auto flex items-center justify-between gap-4 md:gap-8">
        {/* Zone 1: Brand Wordmark (Single Element) */}
        <button
          onClick={() => onSelectTab && onSelectTab('home')}
          className="flex items-center gap-2.5 whitespace-nowrap shrink-0 group text-right"
        >
          <img
            src="/logo.svg"
            alt="HMAX-Unlocker Logo"
            className="w-9 h-9 object-contain drop-shadow-[0_0_12px_rgba(0,180,255,0.35)] group-hover:scale-105 transition-transform"
          />
          <div className="leading-none">
            <span className="text-base font-black tracking-tight text-white flex items-center gap-1">
              <span>HMAX</span>
              <span className="text-[#00b4ff]">·</span>
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#ffd768] to-[#e6b83b]">UNLOCKER</span>
            </span>
          </div>
        </button>

        {/* Zone 2: Primary Nav Links (Desktop) */}
        <nav className="hidden lg:flex items-center gap-6 text-xs font-semibold text-slate-300">
          {navLinks.map((link) => {
            const isActive = activeTab === link.id;
            return (
              <button
                key={link.id}
                onClick={() => onSelectTab && onSelectTab(link.id as any)}
                className={`whitespace-nowrap shrink-0 transition-colors py-1 ${
                  isActive
                    ? 'text-[#00b4ff] border-b-2 border-[#00b4ff] font-bold'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                {link.label}
              </button>
            );
          })}
        </nav>

        {/* Zone 3: Primary Action & Controls */}
        <div className="flex items-center gap-2 shrink-0">
          {/* Quick Search Button */}
          <button
            onClick={onSearchClick}
            aria-label="البحث في كل الأقسام"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-[#00b4ff]/40 text-xs text-slate-400 hover:text-white transition active:scale-95"
          >
            <Search className="w-3.5 h-3.5 text-[#00b4ff]" />
            <span className="hidden sm:inline">بحث...</span>
            <kbd className="hidden md:inline px-1 py-0.2 rounded bg-slate-800 text-[10px] text-slate-400 font-mono">/</kbd>
          </button>

          {/* Favorites Button (Visible on mobile/tablet) */}
          <button
            onClick={() => onSelectTab && onSelectTab('favorites')}
            title="العناصر المحفوظة في المفضلة"
            className="lg:hidden relative p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 hover:text-amber-400 active:scale-95 transition"
          >
            <Star className={`w-3.5 h-3.5 ${activeTab === 'favorites' ? 'fill-amber-400 text-amber-400' : ''}`} />
            {favoritesCount > 0 && (
              <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-amber-500 text-black text-[9px] font-black flex items-center justify-center shadow-sm">
                {favoritesCount}
              </span>
            )}
          </button>

          {/* Master Password Quick Copy */}
          <button
            onClick={handleCopyPassword}
            title="نسخ باسورد فك الضغط الموحد"
            className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 text-xs text-slate-300 border border-slate-800 hover:border-[#00b4ff]/30 active:scale-95 transition"
          >
            <ShieldCheck className="w-3.5 h-3.5 text-[#00b4ff]" />
            <span className="font-mono text-[11px] font-bold text-[#00b4ff] hidden md:inline">{MASTER_PASS}</span>
            {copiedPass ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5 text-slate-400" />}
          </button>

          {/* Official Telegram Channel Link */}
          <a
            href="https://t.me/haithamMax1"
            target="_blank"
            rel="noopener noreferrer"
            className="h-8 px-3 rounded-xl bg-[#00b4ff] hover:bg-[#67e8f9] text-black font-black text-xs flex items-center gap-1.5 shadow-[0_0_15px_rgba(0,180,255,0.3)] active:scale-95 transition whitespace-nowrap shrink-0"
          >
            <Send className="w-3.5 h-3.5 fill-black" />
            <span className="hidden sm:inline">قناة التليجرام</span>
            <span className="sm:hidden">تليجرام</span>
          </a>

          {/* PWA Install Button for Android / Desktop */}
          {isInstallable && !isInstalled && (
            <button
              onClick={install}
              className="hidden sm:flex items-center gap-1 px-2.5 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-bold text-slate-200 border border-slate-700 active:scale-95 transition"
            >
              <Smartphone className="w-3.5 h-3.5 text-emerald-400" />
              <span>تثبيت</span>
            </button>
          )}
        </div>
      </div>
    </header>
  );
};
