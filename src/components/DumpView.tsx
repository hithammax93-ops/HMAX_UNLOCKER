import React, { useState } from 'react';
import { ArrowRight, Search, ExternalLink, HardDrive, Shield } from 'lucide-react';
import { HMAX_DATA, MASTER_PASS, ItemData, DumpBrand } from '../data/hmaxData';
import { ItemCard } from './ItemCard';

interface DumpViewProps {
  onCopyToast: (msg: string) => void;
  isFav: (item: ItemData) => boolean;
  onToggleFav: (item: ItemData) => void;
}

export const DumpView: React.FC<DumpViewProps> = ({ onCopyToast, isFav, onToggleFav }) => {
  const [selectedBrand, setSelectedBrand] = useState<string | null>(null);
  const [brandSearch, setBrandSearch] = useState('');
  const [fileSearch, setFileSearch] = useState('');

  const brands = HMAX_DATA.dump_brands.filter((b) =>
    b.name.toLowerCase().includes(brandSearch.toLowerCase())
  );

  const currentBrand = HMAX_DATA.dump_brands.find((b) => b.id === selectedBrand);
  const currentCards = selectedBrand ? HMAX_DATA.dump_cards[selectedBrand] || [] : [];
  const filteredCards = currentCards.filter(
    (c) =>
      c.name.toLowerCase().includes(fileSearch.toLowerCase()) ||
      (c.ver && c.ver.toLowerCase().includes(fileSearch.toLowerCase())) ||
      (c.desc && c.desc.toLowerCase().includes(fileSearch.toLowerCase()))
  );

  return (
    <div className="space-y-4">
      {/* View Header */}
      {!selectedBrand ? (
        <>
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 bg-slate-900/60 border border-slate-800 rounded-2xl p-4">
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xl">🗄️</span>
                <h2 className="text-lg font-black text-slate-100">قسم فلاشات DUMP الشامل</h2>
              </div>
              <p className="text-xs text-slate-400 mt-1">
                أكثر من 560 ملف مسحوب عبر ISP و JTAG و Pandora و UnlockTool و CM2
              </p>
            </div>

            <div className="relative w-full sm:w-64">
              <Search className="w-3.5 h-3.5 text-slate-400 absolute right-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="تصفية الماركات (سامسونج، هونر...)"
                value={brandSearch}
                onChange={(e) => setBrandSearch(e.target.value)}
                className="w-full h-9 pr-9 pl-3 rounded-xl bg-slate-950 border border-slate-800 focus:border-[#00b4ff]/50 text-xs text-slate-200 outline-none"
              />
            </div>
          </div>

          {/* Master Password Callout */}
          <div className="flex items-center justify-between gap-3 p-3 rounded-xl bg-[#00b4ff]/10 border border-[#00b4ff]/25 text-xs text-slate-300">
            <div className="flex items-center gap-2">
              <Shield className="w-4 h-4 text-[#00b4ff]" />
              <span>باسورد فك ضغط غالبية ملفات الدامب:</span>
              <code className="px-2 py-0.5 rounded bg-slate-900 font-mono text-[#00b4ff] font-bold">
                {MASTER_PASS}
              </code>
            </div>
            <button
              onClick={() => {
                navigator.clipboard.writeText(MASTER_PASS);
                onCopyToast(`تم نسخ الباسورد: ${MASTER_PASS}`);
              }}
              className="text-[#00b4ff] hover:underline font-bold text-xs"
            >
              نسخ
            </button>
          </div>

          {/* Brands Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-2.5">
            {brands.map((b) => (
              <button
                key={b.id}
                onClick={() => setSelectedBrand(b.id)}
                className="group p-3.5 rounded-2xl bg-slate-900/80 border border-slate-800/80 hover:border-[#00b4ff]/50 hover:bg-slate-800/60 text-right flex flex-col justify-between h-28 transition-all active:scale-[0.98]"
              >
                <div className="flex items-start justify-between w-full">
                  <span
                    className="w-8 h-8 rounded-xl flex items-center justify-center text-sm"
                    style={{ backgroundColor: `${b.color}20`, color: b.color }}
                  >
                    {b.icon}
                  </span>
                  <span className="text-[11px] font-mono text-slate-400 group-hover:text-[#00b4ff]">
                    {b.count} ملف
                  </span>
                </div>
                <div>
                  <h3 className="text-xs font-bold text-slate-200 group-hover:text-white leading-tight">
                    {b.name}
                  </h3>
                  <span className="text-[10px] text-slate-500 mt-0.5 block">فتح الملفات ←</span>
                </div>
              </button>
            ))}
          </div>
        </>
      ) : (
        /* Selected Brand View */
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 bg-slate-900/60 border border-slate-800 rounded-2xl p-4">
            <div className="flex items-center gap-3">
              <button
                onClick={() => {
                  setSelectedBrand(null);
                  setFileSearch('');
                }}
                className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 transition shrink-0"
                title="رجوع للماركات"
              >
                <ArrowRight className="w-4 h-4" />
              </button>
              <div>
                <h2 className="text-base font-black text-slate-100 flex items-center gap-2">
                  <span>{currentBrand?.icon}</span>
                  <span>{currentBrand?.name}</span>
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  كلمة السر لفك الضغط: <span className="font-mono text-[#00b4ff]">{MASTER_PASS}</span>
                </p>
              </div>
            </div>

            {selectedBrand !== 'tecno' && (
              <div className="relative w-full sm:w-64">
                <Search className="w-3.5 h-3.5 text-slate-400 absolute right-3 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  placeholder="بحث في موديلات هذا البراند..."
                  value={fileSearch}
                  onChange={(e) => setFileSearch(e.target.value)}
                  className="w-full h-9 pr-9 pl-3 rounded-xl bg-slate-950 border border-slate-800 focus:border-[#00b4ff]/50 text-xs text-slate-200 outline-none"
                />
              </div>
            )}
          </div>

          {/* Special Tecno 141 Models Hub */}
          {selectedBrand === 'tecno' ? (
            <div className="rounded-2xl bg-gradient-to-br from-blue-950/40 via-slate-900 to-slate-900 border border-blue-800/40 p-6 text-center space-y-4">
              <div className="w-14 h-14 rounded-2xl bg-blue-500/20 text-blue-400 mx-auto flex items-center justify-center text-2xl shadow-[0_0_30px_rgba(37,99,235,0.2)]">
                📱
              </div>
              <div className="max-w-md mx-auto">
                <h3 className="text-lg font-black text-white">مكتبة تكنو الكاملة — 141 موديل</h3>
                <p className="text-xs text-slate-300 leading-relaxed mt-2">
                  تم جمع وتنظيم 141 فلاشة ودامب رسمي لهواتف TECNO بمختلف سلاسل Spark و Camon و Pova في مجلد سحابي موحد على Google Drive.
                </p>
              </div>
              <div className="pt-2">
                <a
                  href="https://drive.google.com/drive/folders/1-m9ZynYe8S9dI8G_bU7OtPiqTkg1wlgl"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-[#00b4ff] hover:bg-[#67e8f9] text-black font-black text-sm shadow-[0_0_20px_rgba(0,180,255,0.4)] active:scale-95 transition"
                >
                  <ExternalLink className="w-4 h-4" />
                  <span>فتح مجلد مكتبة TECNO الكاملة</span>
                </a>
              </div>
            </div>
          ) : filteredCards.length === 0 ? (
            <div className="p-12 text-center text-slate-500 bg-slate-900/40 rounded-2xl border border-slate-800/60">
              لا توجد ملفات تطابق البحث في هذا القسم
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {filteredCards.map((card) => (
                <ItemCard
                  key={card.id || card.name}
                  item={card}
                  isFav={isFav(card)}
                  onToggleFav={onToggleFav}
                  onCopyToast={onCopyToast}
                  badgeLabel={currentBrand?.name}
                />
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
