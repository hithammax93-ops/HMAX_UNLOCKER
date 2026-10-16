import React from 'react';
import { Search, Download, ShieldCheck, Copy, Check, Smartphone } from 'lucide-react';
import { MASTER_PASS } from '../data/hmaxData';
import { usePWAInstall } from '../hooks/usePWAInstall';

interface TopBarProps {
  onSearchClick: () => void;
  onCopyToast: (msg: string) => void;
}

export const TopBar: React.FC<TopBarProps> = ({ onSearchClick, onCopyToast }) => {
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

  return (
    <header className="sticky top-0 z-40 bg-[#0a0e1a]/90 backdrop-blur-md border-b border-slate-800/80 px-4 py-3">
      <div className="max-w-6xl mx-auto flex items-center justify-between gap-3">
        {/* Brand Lockup */}
        <div className="flex items-center gap-2.5 shrink-0">
          <img
            src="/logo.svg"
            alt="HMAX-Unlocker Logo"
            className="w-10 h-10 object-contain drop-shadow-[0_0_15px_rgba(0,180,255,0.4)] hover:scale-105 transition-transform"
          />
          <div className="leading-tight">
            <h1 className="text-sm font-black tracking-tight flex items-center gap-1">
              <span>HMAX</span>
              <span className="text-[#00b4ff]">-</span>
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#ffd768] to-[#e6b83b]">Unlocker</span>
            </h1>
            <p className="text-[10px] text-slate-400 font-medium">أندرويد PWA الإصدار 6.0</p>
          </div>
        </div>

        {/* Center Quick Search Trigger */}
        <button
          onClick={onSearchClick}
          className="flex-1 max-w-sm hidden sm:flex items-center justify-between gap-2 px-3.5 py-1.5 rounded-full bg-slate-900/90 border border-slate-800 hover:border-[#00b4ff]/40 text-xs text-slate-400 transition"
        >
          <div className="flex items-center gap-2">
            <Search className="w-3.5 h-3.5 text-[#00b4ff]" />
            <span>ابحث في الفلاشات، الأدوات، والأعطال...</span>
          </div>
          <kbd className="hidden md:inline px-1.5 py-0.5 rounded bg-slate-800 text-[10px] text-slate-300 font-mono">/</kbd>
        </button>

        {/* Actions Zone */}
        <div className="flex items-center gap-2 shrink-0">
          {/* Master Password Quick Button */}
          <button
            onClick={handleCopyPassword}
            title="نسخ باسورد فك الضغط الموحد"
            className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-800 text-xs text-slate-300 border border-slate-700/60 active:scale-95 transition"
          >
            <ShieldCheck className="w-3.5 h-3.5 text-[#00b4ff]" />
            <span className="font-mono text-[11px] font-semibold hidden xs:inline">{MASTER_PASS}</span>
            {copiedPass ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5 text-slate-400" />}
          </button>

          {/* Search Mobile Icon Button */}
          <button
            onClick={onSearchClick}
            aria-label="البحث"
            className="sm:hidden p-2 rounded-lg bg-slate-800/80 text-slate-200 border border-slate-700/60 hover:text-[#00b4ff] active:scale-95 transition"
          >
            <Search className="w-4 h-4" />
          </button>

          {/* PWA Install Button for Android */}
          {isInstallable && !isInstalled && (
            <button
              onClick={install}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#00b4ff] hover:bg-[#67e8f9] text-black text-xs font-black shadow-[0_0_15px_rgba(0,180,255,0.3)] active:scale-95 transition"
            >
              <Smartphone className="w-3.5 h-3.5" />
              <span>تثبيت كـ تطبيق</span>
            </button>
          )}

          {/* iOS Safari Guide Button */}
          {isIOS && !isInstalled && (
            <button
              onClick={() => setShowIOSModal(true)}
              className="flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-200 border border-slate-700 active:scale-95 transition"
            >
              <Download className="w-3.5 h-3.5 text-[#00b4ff]" />
              <span>تثبيت</span>
            </button>
          )}
        </div>
      </div>

      {/* iOS Safari Installation Modal */}
      {showIOSModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="w-full max-w-sm rounded-2xl bg-slate-900 border border-slate-800 p-6 shadow-2xl text-slate-100">
            <h3 className="text-base font-bold mb-3 flex items-center gap-2">
              <span className="text-xl">🍎</span>
              <span>تثبيت HMAX UNLOCKER على الآيفون</span>
            </h3>
            <p className="text-xs text-slate-300 leading-relaxed mb-4">
              1. اضغط على زر <strong>مشاركة (Share)</strong> في شريط متصفح سفاري.<br />
              2. مرر لأسفل واختر <strong>إضافة إلى الشاشة الرئيسية (Add to Home Screen)</strong>.<br />
              3. سيظهر التطبيق على شاشتك الرئيسية ويعمل بدون شريط المتصفح!
            </p>
            <button
              onClick={() => setShowIOSModal(false)}
              className="w-full py-2.5 rounded-xl bg-[#00b4ff] text-black font-black text-xs hover:bg-[#67e8f9] transition"
            >
              فهمت، إغلاق
            </button>
          </div>
        </div>
      )}
    </header>
  );
};
