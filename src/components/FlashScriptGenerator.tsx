import React, { useState } from 'react';
import { Terminal, Download, Copy, Check, Sparkles, AlertTriangle, Layers, Play } from 'lucide-react';
import { FLASH_PARTITIONS_LIST, generateFlashScript, ScriptGenerationConfig } from '../data/scriptGeneratorTemplates';

interface FlashScriptGeneratorProps {
  onCopyToast: (msg: string) => void;
}

export const FlashScriptGenerator: React.FC<FlashScriptGeneratorProps> = ({ onCopyToast }) => {
  const [deviceBrand, setDeviceBrand] = useState('Xiaomi_MTK');
  const [selectedPartitions, setSelectedPartitions] = useState<string[]>([
    'p-boot',
    'p-vbmeta',
    'p-recovery'
  ]);
  const [rebootAtEnd, setRebootAtEnd] = useState(true);
  const [wipeData, setWipeData] = useState(false);
  const [fastbootdMode, setFastbootdMode] = useState(false);
  const [scriptType, setScriptType] = useState<'bat' | 'sh'>('bat');
  const [copied, setCopied] = useState(false);

  const togglePartition = (id: string) => {
    setSelectedPartitions((prev) =>
      prev.includes(id) ? prev.filter((p) => p !== id) : [...prev, id]
    );
  };

  const config: ScriptGenerationConfig = {
    deviceBrand,
    selectedPartitions,
    rebootAtEnd,
    wipeDataPrompt: wipeData,
    fastbootdMode,
    scriptType
  };

  const { script, filename } = generateFlashScript(config);

  const handleCopyScript = () => {
    navigator.clipboard.writeText(script);
    setCopied(true);
    onCopyToast(`تم نسخ سكريبت التفليش (${filename})`);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownloadFile = () => {
    const blob = new Blob([script], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    onCopyToast(`تم تنزيل ملف السكريبت: ${filename}`);
  };

  return (
    <div className="space-y-6">
      {/* Banner */}
      <div className="p-5 rounded-3xl bg-gradient-to-br from-slate-900 via-slate-900 to-indigo-950/40 border border-slate-800 space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold">
          <Terminal className="w-3.5 h-3.5" />
          <span>مولد أوامر وسكريبتات التفليش الذكي — Fastboot Batch Script Builder</span>
        </div>
        <h2 className="text-lg font-black text-white">
          توليد ملفات تشغيل تلقائية بنقرة واحدة لتفليش البارتيشنات دون كتابة الأوامر يدوياً
        </h2>
        <p className="text-xs text-slate-400 leading-relaxed max-w-3xl">
          حدد فقط البارتشنات التي تريد تمريرها للهاتف (مثل كيرنل الإقلاع `boot` أو فك توقيع الحماية `vbmeta --disable-verity` أو الريكفري)، وسيولد الموقع فوراً ملف `.bat` قابل للتشغيل في ويندوز بمجرد وضعه في مجلد الفلاشة!
        </p>
      </div>

      {/* Configuration Options */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Step 1: Device / Target Info */}
        <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-3 text-xs">
          <h3 className="font-bold text-white flex items-center gap-2">
            <span className="w-5 h-5 rounded-full bg-slate-800 text-[#00b4ff] flex items-center justify-center font-mono">1</span>
            <span>بيانات الجهاز ونوع السكريبت</span>
          </h3>

          <div>
            <label className="text-slate-400 block mb-1">اسم الموديل / الماركة:</label>
            <input
              type="text"
              value={deviceBrand}
              onChange={(e) => setDeviceBrand(e.target.value)}
              placeholder="مثال: Redmi_Note_12_5G أو Tecno_KM6"
              className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-white font-mono focus:outline-none focus:border-[#00b4ff]"
            />
          </div>

          <div>
            <label className="text-slate-400 block mb-1">نظام التشغيل للسكريبت:</label>
            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() => setScriptType('bat')}
                className={`py-2 rounded-xl font-bold transition ${
                  scriptType === 'bat'
                    ? 'bg-[#00b4ff] text-black shadow-md'
                    : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                }`}
              >
                Windows (.bat)
              </button>
              <button
                type="button"
                onClick={() => setScriptType('sh')}
                className={`py-2 rounded-xl font-bold transition ${
                  scriptType === 'sh'
                    ? 'bg-[#00b4ff] text-black shadow-md'
                    : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                }`}
              >
                Linux / Mac (.sh)
              </button>
            </div>
          </div>

          <div className="pt-2 border-t border-slate-800 space-y-2">
            <label className="flex items-center gap-2 cursor-pointer select-none">
              <input
                type="checkbox"
                checked={fastbootdMode}
                onChange={(e) => setFastbootdMode(e.target.checked)}
                className="rounded bg-slate-950 border-slate-700 text-[#00b4ff]"
              />
              <span className="text-slate-300">التحويل لوضع Fastbootd (للأنظمة الحديثة)</span>
            </label>

            <label className="flex items-center gap-2 cursor-pointer select-none">
              <input
                type="checkbox"
                checked={wipeData}
                onChange={(e) => setWipeData(e.target.checked)}
                className="rounded bg-slate-950 border-slate-700 text-red-400"
              />
              <span className="text-red-400">فورمات كامل للبيانات (fastboot -w)</span>
            </label>

            <label className="flex items-center gap-2 cursor-pointer select-none">
              <input
                type="checkbox"
                checked={rebootAtEnd}
                onChange={(e) => setRebootAtEnd(e.target.checked)}
                className="rounded bg-slate-950 border-slate-700 text-emerald-400"
              />
              <span className="text-emerald-400">إعادة تشغيل الهاتف تلقائياً عند الانتهاء</span>
            </label>
          </div>
        </div>

        {/* Step 2: Select Partitions */}
        <div className="md:col-span-2 p-4 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-white text-xs flex items-center gap-2">
              <span className="w-5 h-5 rounded-full bg-slate-800 text-[#00b4ff] flex items-center justify-center font-mono">2</span>
              <span>اختر البارتشنات المراد تفليشها ({selectedPartitions.length} محددة)</span>
            </h3>

            <div className="flex gap-2 text-[11px]">
              <button
                onClick={() => setSelectedPartitions(['p-boot', 'p-vbmeta', 'p-recovery'])}
                className="text-[#00b4ff] hover:underline"
              >
                تحديد كيرنل وإحياء
              </button>
              <span className="text-slate-600">•</span>
              <button
                onClick={() => setSelectedPartitions(FLASH_PARTITIONS_LIST.map((p) => p.id))}
                className="text-slate-400 hover:underline"
              >
                تحديد الكل
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-h-72 overflow-y-auto pr-1">
            {FLASH_PARTITIONS_LIST.map((part) => {
              const isChecked = selectedPartitions.includes(part.id);
              return (
                <div
                  key={part.id}
                  onClick={() => togglePartition(part.id)}
                  className={`p-2.5 rounded-xl border text-xs cursor-pointer transition select-none flex items-start gap-2.5 ${
                    isChecked
                      ? 'bg-[#00b4ff]/10 border-[#00b4ff]/40 text-white'
                      : 'bg-slate-950/60 border-slate-800/80 text-slate-400 hover:border-slate-700'
                  }`}
                >
                  <input
                    type="checkbox"
                    checked={isChecked}
                    onChange={() => {}}
                    className="mt-0.5 rounded bg-slate-950 border-slate-700 text-[#00b4ff]"
                  />
                  <div>
                    <div className="flex items-center gap-1.5">
                      <strong className="text-slate-100">{part.name}</strong>
                    </div>
                    <code className="text-[10px] text-amber-300 font-mono block mt-0.5">
                      {part.partition} ({part.fileName})
                    </code>
                    <p className="text-[10px] text-slate-400 mt-0.5 line-clamp-1">{part.desc}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Script Preview & Output Card */}
      <div className="p-5 rounded-3xl bg-slate-900 border border-slate-800 space-y-3">
        <div className="flex items-center justify-between flex-wrap gap-2">
          <div className="flex items-center gap-2">
            <Play className="w-4 h-4 text-emerald-400" />
            <h3 className="text-sm font-bold text-white">معاينة السكريبت الجاهز للتنفيذ ({filename})</h3>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={handleCopyScript}
              className={`px-3 py-1.5 rounded-xl font-bold text-xs flex items-center gap-1.5 transition ${
                copied ? 'bg-emerald-500 text-black' : 'bg-slate-800 hover:bg-slate-700 text-slate-200'
              }`}
            >
              {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'تم النسخ!' : 'نسخ الأوامر'}</span>
            </button>
            <button
              onClick={handleDownloadFile}
              className="px-4 py-1.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-black font-black text-xs flex items-center gap-1.5 transition shadow-lg"
            >
              <Download className="w-3.5 h-3.5" />
              <span>تنزيل ملف {scriptType.toUpperCase()}</span>
            </button>
          </div>
        </div>

        <pre className="p-4 rounded-2xl bg-slate-950 border border-slate-800/80 font-mono text-xs text-emerald-400 overflow-x-auto max-h-64 leading-relaxed select-all">
          {script}
        </pre>
        <p className="text-[11px] text-slate-400 italic">
          💡 طريقة الاستخدام: ضع الملف بعد تنزيله داخل نفس المجلد الذي يحتوي على ملفات الفلاشة (`boot.img`, `vbmeta.img`...) ثم انقر عليه نقراً مزدوجاً لتبدأ عملية التفليش الآلي فوراً.
        </p>
      </div>
    </div>
  );
};
