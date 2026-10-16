import React, { useState } from 'react';
import { Search, ShieldAlert, ShieldCheck, AlertTriangle, Check, Copy, Info, Sparkles } from 'lucide-react';
import { decodeSamsungFirmware, SAMPLE_SAMSUNG_BUILDS, DecodedSamsungFirmware } from '../data/samsungFirmwareDecoder';

interface SamsungBinaryCheckerProps {
  onCopyToast: (msg: string) => void;
}

export const SamsungBinaryChecker: React.FC<SamsungBinaryCheckerProps> = ({ onCopyToast }) => {
  const [inputCode, setInputCode] = useState('A546EXXS5BXA1');
  const [currentPhoneBuild, setCurrentPhoneBuild] = useState('');
  const [targetFlashBuild, setTargetFlashBuild] = useState('');
  const [comparisonResult, setComparisonResult] = useState<{
    safe: boolean;
    reason: string;
    phoneBit?: number;
    flashBit?: number;
  } | null>(null);

  const decoded = decodeSamsungFirmware(inputCode);

  const handleCompare = () => {
    if (!currentPhoneBuild.trim() || !targetFlashBuild.trim()) {
      onCopyToast('يرجى إدخال كود الجهاز الحالي وكود الفلاشة المراد تفليشها');
      return;
    }
    const phone = decodeSamsungFirmware(currentPhoneBuild);
    const flash = decodeSamsungFirmware(targetFlashBuild);

    const pBit = parseInt(phone.binaryBit, 10);
    const fBit = parseInt(flash.binaryBit, 10);

    if (isNaN(pBit) || isNaN(fBit)) {
      setComparisonResult({
        safe: false,
        reason: 'تعذر استخراج رقم الحماية (Binary Bit) لأحد الإصدارين. تأكد من صحة كود البناء المكتوب.'
      });
      return;
    }

    if (fBit < pBit) {
      setComparisonResult({
        safe: false,
        phoneBit: pBit,
        flashBit: fBit,
        reason: `🚨 خطر مؤكد! الفلاشة بحماية Bit ${fBit} وهي أقل من حماية الهاتف الحالية Bit ${pBit}. التفليش سيفشل بخطأ SW REV CHECK FAIL وسيتوقف الهاتف!`
      });
    } else if (fBit === pBit) {
      setComparisonResult({
        safe: true,
        phoneBit: pBit,
        flashBit: fBit,
        reason: `✅ التفليش آمن تماماً 100%! كلا النظامين يحملان نفس الحماية الثنائية Bit ${pBit}. يمكنك الترقية أو تفليش نفس الإصدار بأمان.`
      });
    } else {
      setComparisonResult({
        safe: true,
        phoneBit: pBit,
        flashBit: fBit,
        reason: `⬆️ ترقية حماية (Upgrade to Bit ${fBit}): التفليش آمن وسيقوم بترقية حماية الهاتف من Bit ${pBit} إلى Bit ${fBit}. تنبيه: لن تتمكن من التراجع عن هذا الإصدار مستقبلاً.`
      });
    }
  };

  return (
    <div className="space-y-6">
      {/* Introduction Card */}
      <div className="p-5 rounded-3xl bg-gradient-to-br from-slate-900 via-slate-900 to-blue-950/40 border border-slate-800 space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#00b4ff]/10 border border-[#00b4ff]/30 text-[#00b4ff] text-xs font-bold">
          <Sparkles className="w-3.5 h-3.5" />
          <span>محلل حمايات سامسونج الذكي — Samsung Binary & Anti-Rollback Decoder</span>
        </div>
        <h2 className="text-lg font-black text-white">
          فك تشفير إصدارات سامسونج وتفادي موت الهاتف (Binary / Bit Protection)
        </h2>
        <p className="text-xs text-slate-400 leading-relaxed max-w-3xl">
          أحد أكثر الأخطاء شيوعاً التي تتسبب في موت هواتف سامسونج أو ظهور شاشة الموت الزرقاء هو محاولة تفليش فلاشة برقم حماية أقل (Downgrade Bit). استخدم هذه الأداة لتفكيك كود أي فلاشة سامسونج ومطابقتها قبل التفليش.
        </p>

        {/* Input box */}
        <div className="flex flex-col sm:flex-row gap-2 pt-2">
          <div className="relative flex-1">
            <input
              type="text"
              value={inputCode}
              onChange={(e) => setInputCode(e.target.value.toUpperCase())}
              placeholder="اكتب أو الصق كود الفلاشة الكامل مثل: S908BXXU4CWK3..."
              className="w-full px-4 py-3 rounded-2xl bg-slate-950 border border-slate-800 text-sm text-white font-mono placeholder-slate-500 focus:outline-none focus:border-[#00b4ff] transition"
            />
          </div>
          <button
            onClick={() => {
              navigator.clipboard.writeText(decoded.raw);
              onCopyToast(`تم نسخ الكود: ${decoded.raw}`);
            }}
            className="px-5 py-3 rounded-2xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs flex items-center justify-center gap-1.5 transition shrink-0"
          >
            <Copy className="w-3.5 h-3.5" />
            <span>نسخ الكود</span>
          </button>
        </div>

        {/* Quick sample chips */}
        <div className="flex items-center gap-1.5 flex-wrap pt-1">
          <span className="text-[11px] text-slate-500">أمثلة جاهزة للفحص:</span>
          {SAMPLE_SAMSUNG_BUILDS.map((s, idx) => (
            <button
              key={idx}
              onClick={() => setInputCode(s.code)}
              className="px-2.5 py-1 rounded-lg text-[11px] font-mono bg-slate-950 border border-slate-800 hover:border-slate-700 text-slate-300 hover:text-[#00b4ff] transition"
            >
              {s.label}
            </button>
          ))}
        </div>
      </div>

      {/* Decoded Breakdown Grid */}
      {decoded.isRecognized ? (
        <div className="p-5 rounded-3xl bg-slate-900/90 border border-slate-800 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span>تحليل تفاصيل الفلاشة:</span>
              <code className="text-[#00b4ff] font-mono">{decoded.raw}</code>
            </h3>
            <span className="px-3 py-1 rounded-full text-xs font-black bg-amber-400/10 text-amber-300 border border-amber-400/30">
              Binary Bit: {decoded.binaryBit}
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="p-3.5 rounded-2xl bg-slate-950 border border-slate-800">
              <span className="text-[10px] text-slate-500 block">رقم الحماية (Binary/Bootloader):</span>
              <span className="text-xl font-black text-amber-400 font-mono">Bit {decoded.binaryBit}</span>
              <span className="text-[10px] text-slate-400 block mt-0.5">U{decoded.binaryBit} / S{decoded.binaryBit}</span>
            </div>

            <div className="p-3.5 rounded-2xl bg-slate-950 border border-slate-800">
              <span className="text-[10px] text-slate-500 block">سنة التجميع (Year):</span>
              <span className="text-base font-black text-white font-mono">{decoded.year}</span>
              <span className="text-[10px] text-slate-400 block mt-0.5">الرمز: {decoded.raw.charAt(decoded.raw.length - 3)}</span>
            </div>

            <div className="p-3.5 rounded-2xl bg-slate-950 border border-slate-800">
              <span className="text-[10px] text-slate-500 block">شهر التحديث (Month):</span>
              <span className="text-xs font-bold text-white font-sans">{decoded.month}</span>
              <span className="text-[10px] text-slate-400 block mt-0.5">الرمز: {decoded.raw.charAt(decoded.raw.length - 2)}</span>
            </div>

            <div className="p-3.5 rounded-2xl bg-slate-950 border border-slate-800">
              <span className="text-[10px] text-slate-500 block">كود المنطقة / الموجه (CSC):</span>
              <span className="text-base font-black text-[#00b4ff] font-mono">{decoded.region}</span>
              <span className="text-[10px] text-slate-400 block mt-0.5">موديل: {decoded.model}</span>
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-1.5 text-xs">
            {decoded.notes.map((n, i) => (
              <p key={i} className="text-slate-300 leading-relaxed flex items-start gap-2">
                <span className="text-amber-400 font-black">•</span>
                <span>{n}</span>
              </p>
            ))}
          </div>
        </div>
      ) : null}

      {/* Side-by-Side Binary Flashing Safety Matcher */}
      <div className="p-5 rounded-3xl bg-slate-900/80 border border-slate-800 space-y-4">
        <div>
          <h3 className="text-sm font-black text-white flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 text-amber-400" />
            <span>فاحص أمان التراجع والتفليش (Downgrade & Safety Matcher)</span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            قارن بين إصدار الهاتف الموجود حالياً وبين الفلاشة التي تريد تنزيلها لمعرفة هل العملية آمنة أم خطرة.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
          <div>
            <label className="text-slate-400 block mb-1 font-bold">1. إصدار الهاتف الحالي (Current on Phone):</label>
            <input
              type="text"
              value={currentPhoneBuild}
              onChange={(e) => setCurrentPhoneBuild(e.target.value.toUpperCase())}
              placeholder="مثال: S908BXXU4CWK3 (Bit 4)"
              className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white font-mono placeholder-slate-600 focus:outline-none focus:border-[#00b4ff]"
            />
          </div>

          <div>
            <label className="text-slate-400 block mb-1 font-bold">2. الفلاشة المراد تفليشها (Target ROM):</label>
            <input
              type="text"
              value={targetFlashBuild}
              onChange={(e) => setTargetFlashBuild(e.target.value.toUpperCase())}
              placeholder="مثال: S908BXXU4DXB2 (Bit 4) أو S908BXXU3BWK1"
              className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white font-mono placeholder-slate-600 focus:outline-none focus:border-[#00b4ff]"
            />
          </div>
        </div>

        <button
          onClick={handleCompare}
          className="w-full py-2.5 rounded-xl bg-[#00b4ff] hover:bg-[#0090cc] text-black font-black text-xs transition shadow-md"
        >
          فحص ومطابقة الحماية
        </button>

        {comparisonResult && (
          <div
            className={`p-4 rounded-2xl border text-xs leading-relaxed ${
              comparisonResult.safe
                ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
                : 'bg-red-500/10 border-red-500/40 text-red-300'
            }`}
          >
            <p className="font-bold">{comparisonResult.reason}</p>
          </div>
        )}
      </div>
    </div>
  );
};
