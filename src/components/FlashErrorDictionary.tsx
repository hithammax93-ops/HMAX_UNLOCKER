import React, { useState, useMemo } from 'react';
import { Search, AlertOctagon, HelpCircle, Wrench, CheckCircle, ExternalLink, Filter } from 'lucide-react';
import { FLASH_ERROR_DATABASE, FlashErrorItem } from '../data/flashErrorDictionary';

interface FlashErrorDictionaryProps {
  onCopyToast: (msg: string) => void;
}

export const FlashErrorDictionary: React.FC<FlashErrorDictionaryProps> = ({ onCopyToast }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [toolFilter, setToolFilter] = useState<string>('all');
  const [selectedError, setSelectedError] = useState<FlashErrorItem | null>(null);

  const toolsList = ['all', 'SP Flash Tool', 'Samsung Odin', 'Qualcomm EDL / QFIL', 'Unisoc SPD', 'UnlockTool / Pandora'];

  const filteredErrors = useMemo(() => {
    return FLASH_ERROR_DATABASE.filter((err) => {
      const matchTool = toolFilter === 'all' || err.tool === toolFilter;
      const q = searchQuery.toLowerCase();
      const matchQuery =
        err.code.toLowerCase().includes(q) ||
        err.title.toLowerCase().includes(q) ||
        err.meaning.toLowerCase().includes(q) ||
        err.tool.toLowerCase().includes(q);
      return matchTool && matchQuery;
    });
  }, [toolFilter, searchQuery]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-5 rounded-3xl bg-gradient-to-br from-slate-900 via-slate-900 to-rose-950/40 border border-slate-800 space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs font-bold">
          <AlertOctagon className="w-3.5 h-3.5" />
          <span>قاموس وموسوعة أخطاء التفليش والبوكسات — GSM Error Code Encyclopedia</span>
        </div>
        <h2 className="text-lg font-black text-white">
          دليل الإسعاف السريع لحل أخطاء SP Flash Tool و Odin و QFIL و UnlockTool
        </h2>
        <p className="text-xs text-slate-400 leading-relaxed max-w-3xl">
          عندما يتوقف التفليش وتظهر رسالة خطأ غامضة مثل (0xC0050005) أو (SW REV CHECK FAIL) أو (Sahara Protocol Failed)، ابحث هنا لمعرفة السبب الحقيقي والخطوات الـ 3 المضمونة لتجاوز المشكلة فوراً.
        </p>

        {/* Search Input */}
        <div className="relative">
          <Search className="w-4 h-4 absolute right-4 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="ابحث برمز الخطأ أو اسم البرنامج (مثل: 2004 أو Fused أو DRAM أو Odin)..."
            className="w-full pl-4 pr-11 py-3 rounded-2xl bg-slate-950 border border-slate-800 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-rose-500 transition shadow-inner"
          />
        </div>

        {/* Filter Pills */}
        <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar pt-1">
          {toolsList.map((t) => (
            <button
              key={t}
              onClick={() => setToolFilter(t)}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold transition whitespace-nowrap ${
                toolFilter === t
                  ? 'bg-rose-500 text-white shadow-md'
                  : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
              }`}
            >
              {t === 'all' ? 'جميع البرامج' : t}
            </button>
          ))}
        </div>
      </div>

      {/* Errors Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredErrors.map((err) => (
          <div
            key={err.id}
            className="p-5 rounded-3xl bg-slate-900/80 border border-slate-800 hover:border-slate-700 transition flex flex-col justify-between space-y-4"
          >
            <div>
              <div className="flex items-center justify-between gap-2 mb-2">
                <span className="px-2.5 py-0.5 rounded-md text-[11px] font-black bg-rose-500/10 text-rose-400 border border-rose-500/30">
                  {err.tool}
                </span>
                <span
                  className={`text-[10px] px-2 py-0.5 rounded-full font-bold ${
                    err.severity === 'fatal'
                      ? 'bg-red-500/15 text-red-400 border border-red-500/30'
                      : err.severity === 'driver'
                      ? 'bg-blue-500/15 text-blue-400 border border-blue-500/30'
                      : 'bg-amber-500/15 text-amber-400 border border-amber-500/30'
                  }`}
                >
                  {err.severity === 'fatal' ? 'خطأ هاردوير / أمان' : err.severity === 'driver' ? 'خلل تعريفات' : 'تنبيه'}
                </span>
              </div>

              <div className="space-y-1">
                <code className="text-xs font-mono font-bold text-amber-300 block select-all">
                  {err.code}
                </code>
                <h3 className="text-sm font-black text-white">{err.title}</h3>
                <p className="text-xs text-slate-300 leading-relaxed mt-1">{err.meaning}</p>
              </div>

              {/* Causes */}
              <div className="mt-3 pt-3 border-t border-slate-800/80 space-y-1.5">
                <span className="text-[11px] font-bold text-slate-400 block">الأسباب الرئيسية للعطل:</span>
                <ul className="text-xs text-slate-400 space-y-1 pr-3">
                  {err.causes.map((c, i) => (
                    <li key={i} className="list-disc leading-relaxed">
                      {c}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Fix Steps */}
              <div className="mt-3 p-3 rounded-2xl bg-slate-950 border border-slate-800/80 space-y-1.5">
                <span className="text-[11px] font-bold text-emerald-400 flex items-center gap-1">
                  <CheckCircle className="w-3.5 h-3.5" />
                  <span>خطوات الحل المعتمدة:</span>
                </span>
                <ol className="text-xs text-slate-300 space-y-1 pr-4 list-decimal leading-relaxed">
                  {err.solutionSteps.map((s, i) => (
                    <li key={i}>{s}</li>
                  ))}
                </ol>
              </div>
            </div>

            {err.recommendedToolOrDriver && (
              <div className="pt-2 border-t border-slate-800 text-[11px] text-cyan-400 flex items-center justify-between">
                <span>الأداة أو التعريف الموصى به:</span>
                <strong className="text-white font-mono">{err.recommendedToolOrDriver}</strong>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
