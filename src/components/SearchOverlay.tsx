import React, { useState, useEffect, useMemo, useRef } from 'react';
import { Search, X, Download, Copy, Star, ExternalLink } from 'lucide-react';
import { HMAX_DATA, ItemData } from '../data/hmaxData';

interface SearchOverlayProps {
  isOpen: boolean;
  onClose: () => void;
  onCopyToast: (msg: string) => void;
  isFav: (item: ItemData) => boolean;
  onToggleFav: (item: ItemData) => void;
}

interface SearchResultItem extends ItemData {
  categoryLabel: string;
}

export const SearchOverlay: React.FC<SearchOverlayProps> = ({
  isOpen,
  onClose,
  onCopyToast,
  isFav,
  onToggleFav,
}) => {
  const [query, setQuery] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
    } else {
      setQuery('');
    }
  }, [isOpen]);

  // Aggregate all items with category labels
  const allItems = useMemo(() => {
    const list: SearchResultItem[] = [];

    HMAX_DATA.tools.forEach((it) => list.push({ ...it, categoryLabel: 'أدوات السوفت وير' }));
    HMAX_DATA.drivers.forEach((it) => list.push({ ...it, categoryLabel: 'تعريفات الموبايل' }));
    HMAX_DATA.unlocking.forEach((it) => list.push({ ...it, categoryLabel: 'فك الشفرات' }));
    HMAX_DATA.firmware_sites.forEach((it) => list.push({ ...it, categoryLabel: 'مواقع الفلاشات' }));
    HMAX_DATA.iphone_tools.forEach((it) => list.push({ ...it, categoryLabel: 'أدوات آيفون' }));
    HMAX_DATA.iphone_pwn.forEach((it) => list.push({ ...it, categoryLabel: 'قطع PWN DFU' }));
    HMAX_DATA.halabtech.forEach((it) => list.push({ ...it, categoryLabel: 'ملفات حلب تك' }));
    HMAX_DATA.offers_hitham.forEach((it) => list.push({ ...it, categoryLabel: 'عروض حصرية' }));
    HMAX_DATA.paid_offers.forEach((it) => list.push({ ...it, categoryLabel: 'عروض VIP' }));
    HMAX_DATA.ai_offers.forEach((it) => list.push({ ...it, categoryLabel: 'ذكاء اصطناعي' }));
    HMAX_DATA.free_tools.forEach((it) => list.push({ ...it, categoryLabel: 'أدوات مجانية' }));
    HMAX_DATA.gifts.forEach((it) => list.push({ ...it, categoryLabel: 'هدايا حصرية' }));
    HMAX_DATA.services.forEach((it) => list.push({ ...it, categoryLabel: 'خدمات عن بعد' }));

    // Dump cards
    Object.entries(HMAX_DATA.dump_cards).forEach(([brand, cards]) => {
      cards.forEach((c) =>
        list.push({ ...c, categoryLabel: `DUMP: ${brand.toUpperCase()}` })
      );
    });

    // Solutions
    HMAX_DATA.solutions.youtube.forEach((it) => list.push({ ...it, categoryLabel: 'شروحات يوتيوب' }));
    HMAX_DATA.solutions.volte.forEach((it) => list.push({ ...it, categoryLabel: 'تفعيل VoLTE' }));
    HMAX_DATA.solutions.rasheed.forEach((it) => list.push({ ...it, categoryLabel: 'لمسات رشيد' }));
    HMAX_DATA.solutions.haitham.forEach((it) => list.push({ ...it, categoryLabel: 'شروحات هيثم' }));

    return list;
  }, []);

  // Filtered results
  const results = useMemo(() => {
    if (!query.trim()) return [];
    const q = query.toLowerCase().trim();
    return allItems
      .filter((it) => {
        const text = `${it.name} ${it.ver || ''} ${it.desc || ''} ${it.categoryLabel} ${it.guide || ''}`.toLowerCase();
        return text.includes(q);
      })
      .slice(0, 60);
  }, [allItems, query]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex flex-col bg-[#0a0e1a]/95 backdrop-blur-xl animate-in fade-in duration-200">
      {/* Search Header */}
      <div className="sticky top-0 z-10 px-4 py-3 bg-[#0a0e1a] border-b border-slate-800">
        <div className="max-w-2xl mx-auto flex items-center gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-[#00b4ff] absolute right-3.5 top-1/2 -translate-y-1/2" />
            <input
              ref={inputRef}
              type="text"
              placeholder="اكتب اسم الجهاز، الفلاشة، الأداة، أو نوع المعالج..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full h-11 pr-10 pl-9 rounded-2xl bg-slate-900 border border-slate-700/80 focus:border-[#00b4ff] text-sm text-white placeholder-slate-500 outline-none transition"
            />
            {query && (
              <button
                onClick={() => setQuery('')}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>
          <button
            onClick={onClose}
            className="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-bold text-slate-200 transition"
          >
            إغلاق
          </button>
        </div>
      </div>

      {/* Results Body */}
      <div className="flex-1 overflow-y-auto px-4 py-4">
        <div className="max-w-2xl mx-auto space-y-2.5">
          {!query.trim() ? (
            <div className="text-center py-16 text-slate-500 space-y-2">
              <Search className="w-10 h-10 mx-auto text-slate-700 stroke-1" />
              <p className="text-sm">ابحث في قاعدة بيانات HMAX UNLOCKER الشاملة</p>
              <div className="flex items-center justify-center gap-2 pt-2 flex-wrap">
                <span className="text-xs text-slate-400">اقتراحات سريعة:</span>
                {['Samsung A14', 'Redmi Note', 'MTK Fix', 'VoLTE', 'UnlockTool', 'Tecno'].map((tag) => (
                  <button
                    key={tag}
                    onClick={() => setQuery(tag)}
                    className="px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 text-xs text-[#00b4ff] hover:border-[#00b4ff]/40"
                  >
                    {tag}
                  </button>
                ))}
              </div>
            </div>
          ) : results.length === 0 ? (
            <div className="text-center py-16 text-slate-500">
              لا توجد نتائج تطابق &quot;<span className="text-slate-300 font-bold">{query}</span>&quot;
            </div>
          ) : (
            <>
              <div className="text-xs text-slate-400 mb-2 px-1">
                تم العثور على <span className="text-[#00b4ff] font-bold">{results.length}</span> نتيجة
              </div>
              {results.map((item) => (
                <div
                  key={`${item.categoryLabel}-${item.id || item.name}`}
                  className="p-3.5 rounded-2xl bg-slate-900/90 border border-slate-800/90 hover:border-[#00b4ff]/40 flex flex-col sm:flex-row sm:items-center justify-between gap-3 transition"
                >
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-[10px] font-bold text-[#00b4ff] px-2 py-0.5 rounded-md bg-[#00b4ff]/10">
                        {item.categoryLabel}
                      </span>
                      {item.ver && (
                        <span className="text-[10px] font-mono text-slate-400">{item.ver}</span>
                      )}
                    </div>
                    <h4 className="text-xs font-bold text-white truncate">{item.name}</h4>
                    {item.desc && (
                      <p className="text-[11px] text-slate-400 line-clamp-1 mt-0.5">{item.desc}</p>
                    )}
                  </div>

                  <div className="flex items-center gap-2 shrink-0">
                    {item.link && item.link !== '#' && (
                      <a
                        href={item.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="h-8 px-3 rounded-lg bg-[#00b4ff] hover:bg-[#67e8f9] text-black text-xs font-black flex items-center gap-1 transition"
                      >
                        <Download className="w-3 h-3" />
                        <span>فتح</span>
                      </a>
                    )}
                    {item.link && (
                      <button
                        onClick={() => {
                          navigator.clipboard.writeText(item.link!);
                          onCopyToast('تم نسخ الرابط');
                        }}
                        title="نسخ الرابط"
                        className="h-8 w-8 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 flex items-center justify-center transition"
                      >
                        <Copy className="w-3.5 h-3.5" />
                      </button>
                    )}
                    <button
                      onClick={() => onToggleFav(item)}
                      title="المفضلة"
                      className="h-8 w-8 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 flex items-center justify-center transition"
                    >
                      <Star
                        className={`w-3.5 h-3.5 ${
                          isFav(item) ? 'fill-amber-400 text-amber-400' : 'text-slate-400'
                        }`}
                      />
                    </button>
                  </div>
                </div>
              ))}
            </>
          )}
        </div>
      </div>
    </div>
  );
};
