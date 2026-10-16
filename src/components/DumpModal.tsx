import React from 'react';
import { X, Download, Copy, Shield, Cpu, HardDrive, Wrench, AlertTriangle, ExternalLink, Check, Star } from 'lucide-react';
import { ItemData, MASTER_PASS } from '../data/hmaxData';

interface DumpModalProps {
  item: ItemData | null;
  onClose: () => void;
  onCopyToast: (msg: string) => void;
  isFav?: boolean;
  onToggleFav?: (item: ItemData) => void;
}

export const DumpModal: React.FC<DumpModalProps> = ({
  item,
  onClose,
  onCopyToast,
  isFav = false,
  onToggleFav,
}) => {
  const [copiedPass, setCopiedPass] = React.useState(false);
  const [copiedLink, setCopiedLink] = React.useState(false);

  if (!item) return null;

  const pass = item.pass && item.pass !== '—' ? item.pass : MASTER_PASS;

  const handleCopyPass = () => {
    navigator.clipboard.writeText(pass);
    setCopiedPass(true);
    onCopyToast(`تم نسخ كلمة السر: ${pass}`);
    setTimeout(() => setCopiedPass(false), 2000);
  };

  const handleCopyLink = () => {
    if (!item.link) return;
    navigator.clipboard.writeText(item.link);
    setCopiedLink(true);
    onCopyToast('تم نسخ رابط التحميل');
    setTimeout(() => setCopiedLink(false), 2000);
  };

  // Guess tool / platform heuristics from name/desc
  const isJtag = item.desc?.includes('JTAG') || item.ver?.includes('JTAG') || item.desc?.includes('F64') || item.ver?.includes('F64');
  const isPandora = item.desc?.includes('Pandora') || item.ver?.includes('Pandora');
  const isUnlockTool = item.desc?.includes('UnlockTool') || item.ver?.includes('UnlockTool');
  const isCM2 = item.desc?.includes('CM2') || item.ver?.includes('CM2');

  const toolName = isJtag ? 'JTAG / EMMC / F64' : isPandora ? 'Pandora Tool' : isUnlockTool ? 'UnlockTool' : isCM2 ? 'Infinity CM2' : 'Official Hardware/Dongle';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
      <div 
        className="relative w-full max-w-lg rounded-2xl bg-slate-900 border border-slate-800 p-5 sm:p-6 shadow-2xl text-slate-100 overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Subtle accent glow */}
        <div className="absolute -top-16 -left-16 w-36 h-36 rounded-full bg-[#00b4ff]/10 blur-2xl pointer-events-none" />

        {/* Modal Header */}
        <div className="flex items-start justify-between gap-3 pb-3 border-b border-slate-800">
          <div>
            <span className="text-[11px] font-mono text-[#00b4ff] block mb-0.5">
              بطاقة تفاصيل الفلاشة والدامب
            </span>
            <h2 className="text-base sm:text-lg font-black text-white leading-snug">
              {item.name}
            </h2>
          </div>
          <div className="flex items-center gap-1 shrink-0">
            {onToggleFav && (
              <button
                onClick={() => onToggleFav(item)}
                className="p-1.5 rounded-lg text-slate-400 hover:text-amber-400 transition"
                title={isFav ? "إزالة من المفضلة" : "إضافة للمفضلة"}
              >
                <Star className={`w-4 h-4 ${isFav ? 'fill-amber-400 text-amber-400' : ''}`} />
              </button>
            )}
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Modal Body */}
        <div className="space-y-4 py-4 text-xs">
          {/* Quick Info Grid */}
          <div className="grid grid-cols-2 gap-2">
            <div className="p-2.5 rounded-xl bg-slate-950/80 border border-slate-800/80">
              <span className="text-[10px] text-slate-500 block mb-0.5">الإصدار / التوجيه</span>
              <span className="font-mono font-bold text-slate-200 truncate block">
                {item.ver || 'Official Full Dump'}
              </span>
            </div>
            <div className="p-2.5 rounded-xl bg-slate-950/80 border border-slate-800/80">
              <span className="text-[10px] text-slate-500 block mb-0.5">أداة السحب المعتمدة</span>
              <span className="font-bold text-[#00b4ff] truncate block">
                {toolName}
              </span>
            </div>
          </div>

          {/* Description */}
          {item.desc && (
            <div className="p-3 rounded-xl bg-slate-950/50 border border-slate-800/60 leading-relaxed text-slate-300">
              <span className="text-[10px] text-slate-500 block mb-1">ملاحظات الملف:</span>
              <p>{item.desc}</p>
            </div>
          )}

          {/* Password Callout */}
          <div className="flex items-center justify-between p-3 rounded-xl bg-[#00b4ff]/10 border border-[#00b4ff]/25">
            <div className="flex items-center gap-2">
              <Shield className="w-4 h-4 text-[#00b4ff] shrink-0" />
              <div>
                <span className="text-[10px] text-slate-400 block">كلمة سر فك الضغط (Password)</span>
                <code className="font-mono font-bold text-sm text-[#00b4ff]">{pass}</code>
              </div>
            </div>
            <button
              onClick={handleCopyPass}
              className="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-xs font-bold text-[#00b4ff] border border-[#00b4ff]/30 flex items-center gap-1 active:scale-95 transition"
            >
              {copiedPass ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>نسخ</span>
            </button>
          </div>

          {/* Technician Warning Note */}
          <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-300 flex items-start gap-2">
            <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />
            <div className="leading-relaxed text-[11px]">
              <strong>تنبيه فني مهم:</strong> يُرجى أخذ نسخة احتياطية كاملة من ملفات الشبكة (NVRAM / NVDATA / QCN / EFS) قبل كتابة أي فلاشة دامب لتجنب فقدان السيريال أو الشبكة.
            </div>
          </div>
        </div>

        {/* Modal Footer Actions */}
        <div className="flex items-center gap-2 pt-3 border-t border-slate-800">
          {item.link ? (
            <a
              href={item.link}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 h-10 px-4 rounded-xl bg-[#00b4ff] hover:bg-[#67e8f9] text-black font-black text-xs flex items-center justify-center gap-2 shadow-[0_0_15px_rgba(0,180,255,0.3)] active:scale-95 transition"
            >
              <Download className="w-4 h-4" />
              <span>تحميل من Google Drive</span>
            </a>
          ) : (
            <div className="flex-1 text-center text-xs text-slate-500">الرابط غير متوفر</div>
          )}

          {item.link && (
            <button
              onClick={handleCopyLink}
              title="نسخ الرابط"
              className="h-10 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs flex items-center gap-1.5 active:scale-95 transition"
            >
              {copiedLink ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span className="hidden sm:inline">نسخ الرابط</span>
            </button>
          )}

          <button
            onClick={onClose}
            className="h-10 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold active:scale-95 transition"
          >
            إغلاق
          </button>
        </div>
      </div>
    </div>
  );
};
