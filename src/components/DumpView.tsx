import React, { useState, useMemo } from 'react';
import { ArrowRight, Search, ExternalLink, HardDrive, Shield, Wrench, Cpu, Sparkles, Filter, Check, Copy } from 'lucide-react';
import { HMAX_DATA, MASTER_PASS, ItemData, DumpBrand } from '../data/hmaxData';
import { TECNO_MODELS, TecnoModelItem } from '../data/tecnoModels';
import { DUMP_TOOLS_CATALOG, DumpToolInfo } from '../data/dumpTools';
import { withDumpPresentation } from '../data/dumpPresentation';
import { ItemCard } from './ItemCard';
import { DumpModal } from './DumpModal';

export interface DumpViewProps {
  onCopyToast: (msg: string) => void;
  isFav: (item: ItemData) => boolean;
  onToggleFav: (item: ItemData) => void;
  initialBrand?: string | null;
}

type BrowseMode = 'brand' | 'tool';

export const DumpView: React.FC<DumpViewProps> = ({
  onCopyToast,
  isFav,
  onToggleFav,
  initialBrand = null,
}) => {
  const [browseMode, setBrowseMode] = useState<BrowseMode>('brand');
  const [selectedBrand, setSelectedBrand] = useState<string | null>(initialBrand);
  const [selectedToolId, setSelectedToolId] = useState<string | null>(null);
  const [brandSearch, setBrandSearch] = useState('');
  const [fileSearch, setFileSearch] = useState('');
  const [tecnoSeries, setTecnoSeries] = useState<string>('all');
  const [inspectItem, setInspectItem] = useState<ItemData | null>(null);
  const [copiedPass, setCopiedPass] = useState(false);

  React.useEffect(() => {
    if (initialBrand !== undefined) {
      setSelectedBrand(initialBrand);
      if (initialBrand) {
        setBrowseMode('brand');
      }
    }
  }, [initialBrand]);

  // Filter Brands
  const brands = useMemo(() => {
    return HMAX_DATA.dump_brands.filter((b) =>
      b.name.toLowerCase().includes(brandSearch.toLowerCase())
    );
  }, [brandSearch]);

  const currentBrand = HMAX_DATA.dump_brands.find((b) => b.id === selectedBrand);

  // Filtered Cards for regular brand
  const currentCards = useMemo(() => {
    if (!selectedBrand) return [];
    if (selectedBrand === 'tecno') {
      let list = TECNO_MODELS;
      if (tecnoSeries !== 'all') {
        list = list.filter((m) => m.series === tecnoSeries);
      }
      if (fileSearch.trim()) {
        const q = fileSearch.toLowerCase();
        list = list.filter(
          (m) =>
            m.name.toLowerCase().includes(q) ||
            m.rawKey.toLowerCase().includes(q) ||
            (m.desc && m.desc.toLowerCase().includes(q))
        );
      }
      return list;
    }
    const cards = HMAX_DATA.dump_cards[selectedBrand] || [];
    if (!fileSearch.trim()) return cards;
    const q = fileSearch.toLowerCase();
    return cards.filter(
      (c) =>
        c.name.toLowerCase().includes(q) ||
        (c.ver && c.ver.toLowerCase().includes(q)) ||
        (c.desc && c.desc.toLowerCase().includes(q))
    );
  }, [selectedBrand, tecnoSeries, fileSearch]);

  // Selected Tool
  const selectedTool = useMemo(() => {
    return DUMP_TOOLS_CATALOG.find((t) => t.id === selectedToolId);
  }, [selectedToolId]);

  const handleCopyMasterPass = () => {
    navigator.clipboard.writeText(MASTER_PASS);
    setCopiedPass(true);
    onCopyToast(`تم نسخ الباسورد الموحد: ${MASTER_PASS}`);
    setTimeout(() => setCopiedPass(false), 2000);
  };

  return (
    <div className="space-y-4">
      {/* Detail Inspector Modal */}
      <DumpModal
        item={inspectItem}
        onClose={() => setInspectItem(null)}
        onCopyToast={onCopyToast}
        isFav={inspectItem ? isFav(inspectItem) : false}
        onToggleFav={onToggleFav}
      />

      {/* Repository heading and responsive browse sections */}
      <div className="space-y-3 bg-slate-900/60 border border-slate-800 rounded-2xl p-3 sm:p-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xl">🗄️</span>
            <h2 className="text-base sm:text-lg font-black text-slate-100">
              مستودع فلاشات DUMP الشامل
            </h2>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            أكثر من 560 ملف دامب مسحوبة عبر JTAG و EMMC و Pandora و UnlockTool و CM2
          </p>
        </div>

        {/* Browse modes displayed as distinct repository sections */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5" aria-label="أقسام مستودع فلاشات DUMP">
          <button
            type="button"
            aria-pressed={browseMode === 'brand'}
            onClick={() => {
              setBrowseMode('brand');
              setSelectedToolId(null);
            }}
            className={`min-h-16 flex items-center gap-3 p-3 rounded-xl text-right border transition ${
              browseMode === 'brand'
                ? 'bg-[#00b4ff]/15 border-[#00b4ff] text-white shadow-sm'
                : 'bg-slate-950/70 border-slate-800 text-slate-300 hover:border-slate-700 hover:bg-slate-900'
            }`}
          >
            <span className={`w-10 h-10 shrink-0 rounded-xl flex items-center justify-center text-xl ${browseMode === 'brand' ? 'bg-[#00b4ff]/20' : 'bg-slate-800'}`}>📱</span>
            <span className="min-w-0 flex-1">
              <span className="flex items-center justify-between gap-2 text-sm font-black">
                <span>حسب الماركات</span>
                <span className="text-[11px] font-mono text-[#00b4ff]">{brands.length} ماركة</span>
              </span>
              <span className="block text-[11px] text-slate-400 mt-0.5">تصفح ملفات الدامب حسب الشركة المصنّعة</span>
            </span>
          </button>
          <button
            type="button"
            aria-pressed={browseMode === 'tool'}
            onClick={() => {
              setBrowseMode('tool');
              setSelectedBrand(null);
            }}
            className={`min-h-16 flex items-center gap-3 p-3 rounded-xl text-right border transition ${
              browseMode === 'tool'
                ? 'bg-[#00b4ff]/15 border-[#00b4ff] text-white shadow-sm'
                : 'bg-slate-950/70 border-slate-800 text-slate-300 hover:border-slate-700 hover:bg-slate-900'
            }`}
          >
            <span className={`w-10 h-10 shrink-0 rounded-xl flex items-center justify-center ${browseMode === 'tool' ? 'bg-[#00b4ff]/20 text-[#00b4ff]' : 'bg-slate-800 text-slate-300'}`}><Wrench className="w-5 h-5" /></span>
            <span className="min-w-0 flex-1">
              <span className="flex items-center justify-between gap-2 text-sm font-black">
                <span>حسب أداة السحب</span>
                <span className="text-[11px] font-mono text-[#00b4ff]">{DUMP_TOOLS_CATALOG.length} أداة</span>
              </span>
              <span className="block text-[11px] text-slate-400 mt-0.5">اعثر على الملفات بحسب البوكس أو الأداة</span>
            </span>
          </button>
        </div>
      </div>

      {/* Master Password Callout Banner */}
      <div className="flex items-center justify-between gap-3 p-3 rounded-xl bg-[#00b4ff]/10 border border-[#00b4ff]/25 text-xs text-slate-300">
        <div className="flex items-center gap-2 flex-wrap">
          <Shield className="w-4 h-4 text-[#00b4ff] shrink-0" />
          <span>باسورد فك ضغط غالبية ملفات الدامب:</span>
          <code className="px-2 py-0.5 rounded bg-slate-900 font-mono text-[#00b4ff] font-bold">
            {MASTER_PASS}
          </code>
        </div>
        <button
          onClick={handleCopyMasterPass}
          className="text-[#00b4ff] hover:underline font-bold text-xs flex items-center gap-1 shrink-0"
        >
          {copiedPass ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
          <span>{copiedPass ? 'تم النسخ' : 'نسخ'}</span>
        </button>
      </div>

      {/* ============================================================== */}
      {/* MODE 1: BY BRAND */}
      {/* ============================================================== */}
      {browseMode === 'brand' && (
        <>
          {!selectedBrand ? (
            /* Brands Index Grid */
            <div className="space-y-4">
              <div className="flex items-center justify-between gap-3">
                <span className="text-xs text-slate-400">
                  اختر ماركة الهاتف لتصفح وتحميل ملفات الدامب الخاصة بها:
                </span>
                <div className="relative w-48 sm:w-64">
                  <Search className="w-3.5 h-3.5 text-slate-400 absolute right-3 top-1/2 -translate-y-1/2" />
                  <input
                    type="text"
                    placeholder="تصفية الماركات (سامسونج، تكنو...)"
                    value={brandSearch}
                    onChange={(e) => setBrandSearch(e.target.value)}
                    className="w-full h-8 pr-9 pl-3 rounded-xl bg-slate-950 border border-slate-800 focus:border-[#00b4ff]/50 text-xs text-slate-200 outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-2.5">
                {brands.map((b) => (
                  <button
                    key={b.id}
                    onClick={() => {
                      setSelectedBrand(b.id);
                      setFileSearch('');
                      setTecnoSeries('all');
                    }}
                    className={`group p-3.5 rounded-2xl bg-slate-900/80 border text-right flex flex-col justify-between h-28 transition-all active:scale-[0.98] ${
                      b.id === 'tecno'
                        ? 'border-blue-500/50 bg-gradient-to-br from-blue-950/30 to-slate-900 shadow-[0_0_15px_rgba(37,99,235,0.15)]'
                        : 'border-slate-800/80 hover:border-[#00b4ff]/50 hover:bg-slate-800/60'
                    }`}
                  >
                    <div className="flex items-start justify-between w-full">
                      <span
                        className="w-8 h-8 rounded-xl flex items-center justify-center text-sm"
                        style={{ backgroundColor: `${b.color}20`, color: b.color }}
                      >
                        {b.icon}
                      </span>
                      <span className="text-[11px] font-mono text-slate-400 group-hover:text-[#00b4ff]">
                        {b.id === 'tecno' ? `${TECNO_MODELS.length} ملف` : `${b.count} ملف`}
                      </span>
                    </div>
                    <div>
                      <h3 className="text-xs font-bold text-slate-200 group-hover:text-white leading-tight">
                        {b.name}
                      </h3>
                      <span className="text-[10px] text-slate-500 mt-0.5 block">
                        فتح الملفات ←
                      </span>
                    </div>
                  </button>
                ))}
              </div>
            </div>
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
                      <span className="text-xs font-normal text-slate-400">
                        ({currentCards.length} ملف متوفر)
                      </span>
                    </h2>
                    <p className="text-xs text-slate-400 mt-0.5">
                      كلمة السر لفك الضغط: <span className="font-mono text-[#00b4ff]">{MASTER_PASS}</span>
                    </p>
                  </div>
                </div>

                <div className="relative w-full sm:w-64">
                  <Search className="w-3.5 h-3.5 text-slate-400 absolute right-3 top-1/2 -translate-y-1/2" />
                  <input
                    type="text"
                    placeholder="بحث في موديلات هذا القسم..."
                    value={fileSearch}
                    onChange={(e) => setFileSearch(e.target.value)}
                    className="w-full h-9 pr-9 pl-3 rounded-xl bg-slate-950 border border-slate-800 focus:border-[#00b4ff]/50 text-xs text-slate-200 outline-none"
                  />
                </div>
              </div>

              {/* Special Tecno 141 Filter Header */}
              {selectedBrand === 'tecno' && (
                <div className="rounded-2xl bg-slate-900/50 border border-slate-800 p-3 space-y-3">
                  <div className="flex items-center justify-between gap-2 flex-wrap">
                    <span className="text-xs font-bold text-slate-300 flex items-center gap-1.5">
                      <Filter className="w-3.5 h-3.5 text-[#00b4ff]" />
                      <span>تصفية سلاسل هواتف تكنو:</span>
                    </span>
                    <a
                      href="https://drive.google.com/drive/folders/1-m9ZynYe8S9dI8G_bU7OtPiqTkg1wlgl"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-[11px] text-[#00b4ff] hover:underline inline-flex items-center gap-1 font-bold"
                    >
                      <ExternalLink className="w-3 h-3" />
                      <span>مجلد Google Drive الرئيسي</span>
                    </a>
                  </div>

                  <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar pb-1">
                    {[
                      { id: 'all', label: `الكل (${TECNO_MODELS.length})` },
                      { id: 'spark', label: `Spark (${TECNO_MODELS.filter(m => m.series === 'spark').length})` },
                      { id: 'camon', label: `Camon (${TECNO_MODELS.filter(m => m.series === 'camon').length})` },
                      { id: 'pova', label: `Pova (${TECNO_MODELS.filter(m => m.series === 'pova').length})` },
                      { id: 'pop', label: `Pop (${TECNO_MODELS.filter(m => m.series === 'pop').length})` },
                      { id: 'phantom', label: `Phantom (${TECNO_MODELS.filter(m => m.series === 'phantom').length})` },
                      { id: 'other', label: `أخرى (${TECNO_MODELS.filter(m => m.series === 'other').length})` },
                    ].map((pill) => (
                      <button
                        key={pill.id}
                        onClick={() => setTecnoSeries(pill.id)}
                        className={`px-3 py-1.5 rounded-lg text-xs font-bold whitespace-nowrap transition ${
                          tecnoSeries === pill.id
                            ? 'bg-[#00b4ff] text-black shadow-sm'
                            : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                        }`}
                      >
                        {pill.label}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Cards Grid */}
              {currentCards.length === 0 ? (
                <div className="p-12 text-center text-slate-500 bg-slate-900/40 rounded-2xl border border-slate-800/60">
                  لا توجد ملفات تطابق البحث في هذا القسم
                </div>
              ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                  {currentCards.map((card) => {
                    const displayCard = withDumpPresentation(card, currentBrand?.id ?? selectedBrand);
                    return (
                      <div
                        key={card.id || card.name}
                        onClick={() => setInspectItem(displayCard)}
                        className="cursor-pointer"
                      >
                        <ItemCard
                          item={displayCard}
                          isFav={isFav(card)}
                          onToggleFav={onToggleFav}
                          onCopyToast={onCopyToast}
                          badgeLabel={currentBrand?.name}
                          showMissingImageNotice
                        />
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          )}
        </>
      )}

      {/* ============================================================== */}
      {/* MODE 2: BY EXTRACTION TOOL (DUMP SOURCE TOOLS) */}
      {/* ============================================================== */}
      {browseMode === 'tool' && (
        <div className="space-y-4">
          {!selectedTool ? (
            /* Tools Index */
            <div className="space-y-4">
              <p className="text-xs text-slate-400">
                فهرس أدوات وبوكسات سحب الدامب المعتمدة، اختر الأداة لعرض الملفات المسحوبة بها:
              </p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {DUMP_TOOLS_CATALOG.map((tool) => (
                  <div
                    key={tool.id}
                    className="p-4 rounded-2xl bg-slate-900/70 border border-slate-800 hover:border-[#00b4ff]/40 transition flex flex-col justify-between space-y-3"
                  >
                    <div>
                      <div className="flex items-center justify-between gap-2 mb-2">
                        <div className="flex items-center gap-2">
                          <span className="text-xl">{tool.icon}</span>
                          <div>
                            <h3 className="text-sm font-bold text-white">{tool.name}</h3>
                            <span className="text-[10px] text-slate-500 font-mono">
                              {tool.category === 'jtag' ? 'بوكس JTAG / ISP / الذاكرة' : 'أداة سوفت وير / دونجل'}
                            </span>
                          </div>
                        </div>

                        <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-slate-800 text-[#00b4ff]">
                          {tool.items.length} ملف
                        </span>
                      </div>

                      <p className="text-xs text-slate-300 leading-relaxed line-clamp-2 mb-2">
                        {tool.desc}
                      </p>

                      <div className="text-[11px] text-slate-400">
                        <span className="text-slate-500">المدعوم: </span>
                        <span>{tool.supported}</span>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 pt-2 border-t border-slate-800/80">
                      <button
                        onClick={() => setSelectedToolId(tool.id)}
                        className="flex-1 h-8 rounded-lg bg-[#00b4ff] hover:bg-[#67e8f9] text-black font-black text-xs transition"
                      >
                        عرض ملفات الدامب ({tool.items.length})
                      </button>
                      <a
                        href={tool.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="h-8 px-3 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs flex items-center gap-1 transition"
                      >
                        <ExternalLink className="w-3 h-3" />
                        <span>تحميل الأداة</span>
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            /* Selected Tool Dumps View */
            <div className="space-y-4">
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 bg-slate-900/60 border border-slate-800 rounded-2xl p-4">
                <div className="flex items-center gap-3">
                  <button
                    onClick={() => setSelectedToolId(null)}
                    className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 transition shrink-0"
                    title="رجوع للأدوات"
                  >
                    <ArrowRight className="w-4 h-4" />
                  </button>
                  <div>
                    <h2 className="text-base font-black text-slate-100 flex items-center gap-2">
                      <span>{selectedTool.icon}</span>
                      <span>{selectedTool.name}</span>
                      <span className="text-xs font-normal text-[#00b4ff]">
                        ({selectedTool.items.length} ملف مسحوب)
                      </span>
                    </h2>
                    <p className="text-xs text-slate-400 mt-0.5">
                      {selectedTool.supported}
                    </p>
                  </div>
                </div>

                <a
                  href={selectedTool.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-bold text-slate-200 border border-slate-700 flex items-center gap-1.5 transition self-end sm:self-auto"
                >
                  <ExternalLink className="w-3.5 h-3.5 text-[#00b4ff]" />
                  <span>الموقع الرسمي للأداة</span>
                </a>
              </div>

              {/* Tool Cards */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {selectedTool.items.map((card) => {
                  const displayCard = withDumpPresentation(card, selectedTool.name);
                  return (
                    <div
                      key={card.id || card.name}
                      onClick={() => setInspectItem(displayCard)}
                      className="cursor-pointer"
                    >
                      <ItemCard
                        item={displayCard}
                        isFav={isFav(card)}
                        onToggleFav={onToggleFav}
                        onCopyToast={onCopyToast}
                        badgeLabel={selectedTool.name}
                        showMissingImageNotice
                      />
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
