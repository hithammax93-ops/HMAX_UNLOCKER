import React, { useState, useEffect, useMemo, useRef } from 'react';
import { Search, X, Download, Copy, Star, ExternalLink, Smartphone, HardDrive, Cable, Wrench, BookOpen, AlertTriangle, Clock3, History, Filter, Share2 } from 'lucide-react';
import { HMAX_DATA, ItemData } from '../data/hmaxData';
import { PhoneResourceKind, searchPhoneModels } from '../data/unifiedPhoneSearch';
import { DUMP_TOOLS_CATALOG } from '../data/dumpTools';
import { ADB_FASTBOOT_COMMANDS, SECRET_DIAL_CODES, APN_PROFILES, TESTPOINT_GUIDES } from '../data/technicianToolsData';
import { IPHONE_CARRIER_CODES } from '../data/iphoneUnlockData';

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

type SearchFilter = 'all' | 'firmware' | 'dump' | 'apk' | 'esim' | 'drivers';
type SearchOrder = 'relevance' | 'recent' | 'frequent';
const normalizeSearchText = (value: string) => value.toLocaleLowerCase().replace(/[ـًٌٍَُِّْٰ]/g, '').trim();
const matchesResourceFilter = (item: SearchResultItem, filter: SearchFilter) => {
  const text = `${item.categoryLabel} ${item.name} ${item.desc ?? ''} ${item.ver ?? ''}`.toLocaleLowerCase();
  if (filter === 'all') return true;
  if (filter === 'firmware') return /firmware|فلاش|روم|samfw|mifirm/.test(text);
  if (filter === 'dump') return /\bdump\b|dump:|دامب|نسخة مسحوبة/.test(text);
  if (filter === 'drivers') return /driver|تعريف|كابل|vcom/.test(text);
  if (filter === 'apk') return /\bapk\b|android app|تطبيق أندرويد/.test(text);
  return /e.?sim|شريحة إلكترونية/.test(text);
};

const readStored = <T,>(key: string, fallback: T): T => {
  try { const value = localStorage.getItem(key); return value ? JSON.parse(value) as T : fallback; }
  catch { return fallback; }
};

export const SearchOverlay: React.FC<SearchOverlayProps> = ({
  isOpen,
  onClose,
  onCopyToast,
  isFav,
  onToggleFav,
}) => {
  const [query, setQuery] = useState('');
  const [selectedPhoneId, setSelectedPhoneId] = useState<string | null>(null);
  const [resourceFilter, setResourceFilter] = useState<SearchFilter>('all');
  const [searchOrder, setSearchOrder] = useState<SearchOrder>('relevance');
  const [recentQueries, setRecentQueries] = useState<string[]>(() => readStored('hmax_search_history_v1', []));
  const [recentItemIds, setRecentItemIds] = useState<string[]>(() => readStored('hmax_recent_items_v1', []));
  const [itemUsage, setItemUsage] = useState<Record<string, { count: number; openedAt: number }>>(() => readStored('hmax_item_usage_v1', {}));
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
    } else {
      setQuery('');
    }
  }, [isOpen]);

  useEffect(() => {
    if (!isOpen || query.trim().length < 2) return;
    const timer = window.setTimeout(() => {
      const next = [query.trim(), ...recentQueries.filter((item) => normalizeSearchText(item) !== normalizeSearchText(query))].slice(0, 8);
      setRecentQueries(next);
      try { localStorage.setItem('hmax_search_history_v1', JSON.stringify(next)); } catch { /* local history is optional */ }
    }, 700);
    return () => window.clearTimeout(timer);
  }, [isOpen, query]);

  const markItemOpened = (item: SearchResultItem) => {
    const nextIds = [item.id, ...recentItemIds.filter((id) => id !== item.id)].slice(0, 8);
    const nextUsage = { ...itemUsage, [item.id]: { count: (itemUsage[item.id]?.count ?? 0) + 1, openedAt: Date.now() } };
    setRecentItemIds(nextIds); setItemUsage(nextUsage);
    try {
      localStorage.setItem('hmax_recent_items_v1', JSON.stringify(nextIds));
      localStorage.setItem('hmax_item_usage_v1', JSON.stringify(nextUsage));
    } catch { /* opening a link must still work when storage is full */ }
  };

  const shareIssueDraft = async (text: string) => {
    try {
      if (navigator.share) await navigator.share({ title: 'بلاغ HMAX', text });
      else { await navigator.clipboard.writeText(text); onCopyToast('نُسخ البلاغ؛ أرسله إلى الدعم عند الحاجة'); }
    } catch (error) {
      if (error instanceof Error && error.name !== 'AbortError') {
        try { await navigator.clipboard.writeText(text); onCopyToast('نُسخ البلاغ؛ أرسله إلى الدعم عند الحاجة'); }
        catch { onCopyToast('تعذر فتح المشاركة أو النسخ'); }
      }
    }
  };

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

    // Extraction Tools
    DUMP_TOOLS_CATALOG.forEach((tool) => {
      list.push({
        id: tool.id,
        name: tool.name,
        desc: tool.desc,
        ver: tool.category === 'jtag' ? 'JTAG / EMMC Tool' : 'Software / Dongle Tool',
        link: tool.url,
        categoryLabel: 'أداة سحب DUMP'
      });
      tool.items.forEach((it) => {
        list.push({ ...it, categoryLabel: `DUMP: ${tool.name}` });
      });
    });

    // Solutions
    HMAX_DATA.solutions.youtube.forEach((it) => list.push({ ...it, categoryLabel: 'شروحات يوتيوب' }));
    HMAX_DATA.solutions.volte.forEach((it) => list.push({ ...it, categoryLabel: 'تفعيل VoLTE' }));
    HMAX_DATA.solutions.rasheed.forEach((it) => list.push({ ...it, categoryLabel: 'لمسات رشيد' }));
    HMAX_DATA.solutions.haitham.forEach((it) => list.push({ ...it, categoryLabel: 'شروحات هيثم' }));

    // Tech Utils (Commands, Dial Codes, APN, TestPoints)
    ADB_FASTBOOT_COMMANDS.forEach((cmd) => {
      list.push({
        id: cmd.id,
        name: cmd.name,
        desc: cmd.desc,
        ver: cmd.cmd,
        guide: cmd.cmd,
        categoryLabel: `أوامر: ${cmd.category.toUpperCase()}`
      });
    });

    SECRET_DIAL_CODES.forEach((cd) => {
      list.push({
        id: cd.id,
        name: `${cd.brand}: ${cd.purpose}`,
        desc: cd.notes || cd.purpose,
        ver: cd.code,
        guide: cd.code,
        categoryLabel: `كود سري: ${cd.brand}`
      });
    });

    APN_PROFILES.forEach((ap) => {
      list.push({
        id: ap.id,
        name: `${ap.carrier} - ${ap.country}`,
        desc: `APN: ${ap.apn} | MCC: ${ap.mcc || ''} MNC: ${ap.mnc || ''}`,
        ver: ap.apn,
        guide: ap.apn,
        categoryLabel: 'نقاط الوصول APN'
      });
    });

    TESTPOINT_GUIDES.forEach((tp) => {
      list.push({
        id: tp.id,
        name: `تيست بوينت: ${tp.brand} ${tp.model}`,
        desc: `${tp.instructions} - ${tp.tpPoint}`,
        ver: `وضع ${tp.mode} - ${tp.chipset}`,
        categoryLabel: 'نقاط التيست بوينت TP'
      });
    });

    IPHONE_CARRIER_CODES.forEach((c) => {
      list.push({
        id: `carrier-${c.carrier}`,
        name: `شفرة مشغل: ${c.carrier} (${c.country})`,
        desc: `${c.notes || ''} - أكواد IMSI: ${c.codes.join(' - ')}`,
        ver: c.codes.join(' | '),
        guide: c.codes.join(' '),
        categoryLabel: 'شفرات مشغلي الآيفون'
      });
    });

    return list;
  }, []);

  // Filtered results
  const results = useMemo(() => {
    if (!query.trim()) return [];
    const q = query.toLowerCase().trim();
    const filtered = allItems
      .filter((it) => {
        const text = `${it.name} ${it.ver || ''} ${it.desc || ''} ${it.categoryLabel} ${it.guide || ''}`.toLowerCase();
        return text.includes(q) && matchesResourceFilter(it, resourceFilter);
      });
    if (searchOrder === 'recent') filtered.sort((a, b) => (itemUsage[b.id]?.openedAt ?? 0) - (itemUsage[a.id]?.openedAt ?? 0));
    if (searchOrder === 'frequent') filtered.sort((a, b) => (itemUsage[b.id]?.count ?? 0) - (itemUsage[a.id]?.count ?? 0));
    return filtered.slice(0, 60);
  }, [allItems, query, resourceFilter, searchOrder, itemUsage]);

  const recentItems = useMemo(() => recentItemIds.map((id) => allItems.find((item) => item.id === id)).filter((item): item is SearchResultItem => Boolean(item)), [allItems, recentItemIds]);

  const phoneMatches = useMemo(() => searchPhoneModels(query), [query]);
  const selectedPhone = phoneMatches.find((phone) => phone.id === selectedPhoneId) ?? null;

  const getGroupIcon = (kind: PhoneResourceKind) => {
    switch (kind) {
      case 'dump': return HardDrive;
      case 'firmware': return Download;
      case 'driver': return Cable;
      case 'solution': return BookOpen;
      case 'testpoint': return Wrench;
      case 'flash-error': return AlertTriangle;
    }
  };

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
              placeholder="ابحث باسم الهاتف أو رقم الموديل أو أي مورد..."
              value={query}
              onChange={(e) => {
                setQuery(e.target.value);
                setSelectedPhoneId(null);
              }}
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
          {query.trim() && <div className="space-y-2 rounded-2xl border border-slate-800 bg-slate-900/60 p-3">
            <div className="flex items-center gap-2 text-[10px] font-bold text-slate-400"><Filter className="h-3.5 w-3.5 text-[#00b4ff]" />تصفية نوع المورد</div>
            <div className="flex gap-2 overflow-x-auto pb-1 no-scrollbar">{([
              ['all', 'الكل'], ['firmware', 'Firmware'], ['dump', 'DUMP'], ['apk', 'APK'], ['esim', 'eSIM'], ['drivers', 'التعريفات'],
            ] as [SearchFilter, string][]).map(([id, label]) => <button key={id} onClick={() => setResourceFilter(id)} className={`shrink-0 rounded-lg border px-3 py-1.5 text-[10px] font-bold ${resourceFilter === id ? 'border-[#00b4ff] bg-[#00b4ff]/15 text-[#67e8f9]' : 'border-slate-800 bg-slate-950 text-slate-400'}`}>{label}</button>)}</div>
            <div className="flex items-center justify-between gap-2 text-[10px] text-slate-500"><span>{results.length} نتيجة مطابقة للفلاتر</span><div className="flex gap-1">{([
              ['relevance', 'الأقرب'], ['recent', 'الأحدث استخدامًا'], ['frequent', 'الأكثر استخدامًا'],
            ] as [SearchOrder, string][]).map(([id, label]) => <button key={id} onClick={() => setSearchOrder(id)} className={`rounded-md px-2 py-1 ${searchOrder === id ? 'bg-slate-700 text-white' : 'text-slate-400'}`}>{label}</button>)}</div></div>
          </div>}
          {!query.trim() ? (
            <div className="text-center py-16 text-slate-500 space-y-2">
              <Search className="w-10 h-10 mx-auto text-slate-700 stroke-1" />
              <p className="text-sm">ابحث باسم الهاتف أو رقم الطراز لعرض ملفاته وتعريفاته وحلوله ونقاط اختباره</p>
              <div className="flex items-center justify-center gap-2 pt-2 flex-wrap">
                <span className="text-xs text-slate-400">جرّب:</span>
                {['SM-A146U1', 'Redmi 9A', 'TECNO SPARK 10', 'Vivo Y20', 'VoLTE', 'UnlockTool'].map((tag) => (
                  <button
                    key={tag}
                    onClick={() => {
                      setQuery(tag);
                      setSelectedPhoneId(null);
                    }}
                    className="px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 text-xs text-[#00b4ff] hover:border-[#00b4ff]/40"
                  >
                    {tag}
                  </button>
                ))}
              </div>
              {(recentQueries.length > 0 || recentItems.length > 0) && <div className="mt-6 space-y-4 text-right">
                {recentQueries.length > 0 && <section><div className="mb-2 flex items-center gap-2 text-xs font-bold text-slate-300"><History className="h-4 w-4 text-[#00b4ff]" />عمليات البحث الأخيرة — محفوظة محليًا</div><div className="flex flex-wrap gap-2">{recentQueries.map((item) => <button key={item} onClick={() => setQuery(item)} className="rounded-lg border border-slate-800 bg-slate-900 px-2.5 py-1.5 text-xs text-slate-300">{item}</button>)}</div></section>}
                {recentItems.length > 0 && <section><div className="mb-2 flex items-center gap-2 text-xs font-bold text-slate-300"><Clock3 className="h-4 w-4 text-amber-300" />عناصر فتحتها مؤخرًا</div><div className="flex flex-wrap gap-2">{recentItems.slice(0, 5).map((item) => <button key={`${item.categoryLabel}-${item.id}`} onClick={() => { setQuery(item.name); setResourceFilter('all'); }} className="rounded-lg border border-slate-800 bg-slate-900 px-2.5 py-1.5 text-xs text-slate-300">{item.name}</button>)}</div></section>}
              </div>}
            </div>
          ) : null}

          {query.trim() && phoneMatches.length > 0 && (
            <section className="mb-5 rounded-2xl border border-[#00b4ff]/25 bg-[#00b4ff]/[0.04] p-3 sm:p-4 space-y-3">
              <div className="flex items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <Smartphone className="w-4 h-4 text-[#00b4ff]" />
                  <h3 className="text-sm font-black text-white">بحث موحّد حسب الجهاز</h3>
                </div>
                <span className="text-[10px] text-slate-400">{phoneMatches.length} موديل مطابق</span>
              </div>

              <div className="flex gap-2 overflow-x-auto pb-1 no-scrollbar">
                {phoneMatches.map((phone) => (
                  <button
                    key={phone.id}
                    onClick={() => setSelectedPhoneId(phone.id)}
                    className={`min-w-48 max-w-64 text-right p-3 rounded-xl border transition shrink-0 ${
                      selectedPhoneId === phone.id
                        ? 'bg-[#00b4ff]/15 border-[#00b4ff]'
                        : 'bg-slate-950/70 border-slate-800 hover:border-[#00b4ff]/50'
                    }`}
                  >
                    <span className="block text-[10px] text-[#00b4ff] font-bold mb-1">{phone.brand}</span>
                    <span className="block text-xs text-white font-bold leading-snug">{phone.name}</span>
                    {phone.modelNumber && <span className="block text-[10px] text-slate-400 mt-1 font-mono truncate">{phone.modelNumber}</span>}
                  </button>
                ))}
              </div>

              {selectedPhone && (
                <div className="space-y-3 pt-2 border-t border-slate-800/80">
                  <div>
                    <div className="flex flex-wrap items-center gap-2">
                      <h4 className="text-sm font-black text-white">{selectedPhone.name}</h4>
                      <span className="text-[10px] px-2 py-0.5 rounded-lg bg-slate-800 text-[#00b4ff]">{selectedPhone.brand}</span>
                    </div>
                    <p className="text-[11px] text-slate-400 mt-1">{selectedPhone.subtitle}</p>
                    <p className="text-[10px] text-amber-300/90 mt-1">تحقق من تطابق رقم اللوحة وإصدار الحماية؛ المصادر العامة والتعاريف المقترحة ليست ضماناً لتوافق الملف.</p>
                  </div>

                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-2.5">
                  {selectedPhone.groups.filter((group) => resourceFilter === 'all' || (resourceFilter === 'dump' && group.kind === 'dump') || (resourceFilter === 'firmware' && group.kind === 'firmware') || (resourceFilter === 'drivers' && group.kind === 'driver')).map((group) => {
                      const GroupIcon = getGroupIcon(group.kind);
                      return (
                        <div key={group.kind} className="rounded-xl bg-slate-950/70 border border-slate-800 p-3">
                          <div className="flex items-center gap-2 mb-2">
                            <GroupIcon className="w-3.5 h-3.5 text-[#00b4ff]" />
                            <h5 className="text-xs font-black text-slate-200">{group.title}</h5>
                            <span className="text-[10px] text-slate-500">{group.resources.length}</span>
                          </div>
                          {group.resources.length === 0 ? (
                            <p className="text-[10px] leading-relaxed text-slate-500">{group.emptyMessage}</p>
                          ) : (
                            <div className="space-y-2">
                              {group.resources.map((resource) => (
                                <article key={resource.id} className="rounded-lg bg-slate-900/80 p-2.5">
                                  <div className="flex items-start justify-between gap-2">
                                    <div className="min-w-0">
                                      <p className="text-[11px] text-white font-bold leading-relaxed">{resource.title}</p>
                                      {resource.version && <p className="text-[10px] text-[#00b4ff] mt-0.5">{resource.version}</p>}
                                      {resource.description && <p className="text-[10px] text-slate-400 leading-relaxed mt-1">{resource.description}</p>}
                                    </div>
                                    {resource.link && resource.link !== '#' && (
                                      <a
                                        href={resource.link}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        onClick={() => markItemOpened({ id: resource.id, name: resource.title, desc: resource.description, link: resource.link, ver: resource.version, categoryLabel: group.title })}
                                        className="shrink-0 text-[10px] px-2 py-1 rounded-lg bg-[#00b4ff] text-black font-black inline-flex items-center gap-1"
                                      >
                                        فتح <ExternalLink className="w-3 h-3" />
                                      </a>
                                    )}
                                  </div>
                                  {resource.detail && resource.detail.length > 0 && (
                                    <ul className="mt-2 space-y-1 border-r border-slate-700 pr-2">
                                      {resource.detail.map((line, index) => <li key={`${resource.id}-${index}`} className="text-[10px] text-slate-300 leading-relaxed">{line}</li>)}
                                    </ul>
                                  )}
                                  {resource.note && <p className="text-[10px] text-amber-300/80 mt-2 leading-relaxed">{resource.note}</p>}
                                  <button onClick={() => shareIssueDraft(`بلاغ HMAX — ${group.title}\nالعنصر: ${resource.title}\nالوصف: ${resource.description}\nالمصدر: ${resource.link || 'لا يوجد رابط مسجل'}\nالسبب: رابط معطل أو وصف/توافق يحتاج مراجعة.`)} className="mt-2 inline-flex items-center gap-1 rounded-lg border border-slate-700 px-2 py-1 text-[10px] text-slate-300"><Share2 className="h-3 w-3" />الإبلاغ عن رابط أو وصف</button>
                                </article>
                              ))}
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </section>
          )}

          {query.trim() && !selectedPhone && results.length === 0 && phoneMatches.length === 0 ? (
            <div className="text-center py-16 text-slate-500">
              لا توجد نتائج تطابق &quot;<span className="text-slate-300 font-bold">{query}</span>&quot;
            </div>
          ) : query.trim() && !selectedPhone && results.length > 0 ? (
            <>
              <div className="text-xs text-slate-400 mb-2 px-1">
                {phoneMatches.length > 0 ? 'نتائج عامة من قاعدة الموارد: ' : 'تم العثور على '}
                <span className="text-[#00b4ff] font-bold">{results.length}</span> نتيجة
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
                        onClick={() => markItemOpened(item)}
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
                      onClick={() => shareIssueDraft(`بلاغ HMAX — ${item.categoryLabel}\nالعنصر: ${item.name}\nالوصف: ${item.desc || 'غير متوفر'}\nالرابط: ${item.link || 'غير متوفر'}\nالسبب: رابط معطل أو وصف يحتاج مراجعة.`)}
                      title="الإبلاغ عن رابط أو وصف"
                      className="h-8 w-8 rounded-lg bg-slate-800 text-slate-300 hover:text-[#67e8f9] flex items-center justify-center transition"
                    ><Share2 className="h-3.5 w-3.5" /></button>
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
          ) : null}
        </div>
      </div>
    </div>
  );
};
