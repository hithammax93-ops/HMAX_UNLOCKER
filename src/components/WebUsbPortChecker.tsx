import React, { useState } from 'react';
import { Usb, Cpu, CheckCircle, AlertTriangle, RefreshCw, Smartphone, Info, Shield } from 'lucide-react';

interface WebUsbPortCheckerProps {
  onCopyToast: (msg: string) => void;
}

interface DetectedUsbDevice {
  vendorId: number;
  productId: number;
  productName?: string;
  manufacturerName?: string;
  serialNumber?: string;
}

const COMMON_GSM_VENDORS: Record<number, { name: string; type: string; driverTip: string }> = {
  0x18d1: { name: 'Google / Fastboot / Android ADB', type: 'Fastboot / ADB Mode', driverTip: 'يحتاج تعريف Google USB Driver أو Fastboot Driver' },
  0x04e8: { name: 'Samsung Electronics', type: 'Download Mode / MTP / ACM', driverTip: 'يحتاج تثبيت SAMSUNG Mobile USB Driver v3' },
  0x2717: { name: 'Xiaomi / Redmi / Poco', type: 'Fastboot / EDL / Sideload', driverTip: 'وضع الفاست بوت لشياومي أو وضع 9008' },
  0x05c6: { name: 'Qualcomm Inc.', type: 'Qualcomm HS-USB QDLoader 9008', driverTip: 'يحتاج تعريف كوالكوم للطوارئ 9008 QCOM Driver' },
  0x0e8d: { name: 'MediaTek Inc. (MTK)', type: 'MTK USB VCOM / Preloader / BROM', driverTip: 'يحتاج تعريف Mediatek VCOM مع حزمة تصفية LibUSB' },
  0x1782: { name: 'Unisoc / Spreadtrum (SPD)', type: 'SCI USB2Serial / SPRD COM', driverTip: 'يحتاج تعريف SPD Driver R4 مع إيقاف توقيع الويندوز' },
  0x2a70: { name: 'OnePlus / Oppo', type: 'MSM Download / Fastboot', driverTip: 'يحتاج تعريف أوبو ووان بلس الرسمي' },
  0x22b8: { name: 'Motorola Solutions', type: 'Fastboot / Motorola ADB', driverTip: 'يحتاج تعريف Motorola Device Manager' },
  0x0bb4: { name: 'HTC / Generic Android', type: 'Fastboot Mode', driverTip: 'تعريف أندرويد العام Universal ADB Driver' }
};

export const WebUsbPortChecker: React.FC<WebUsbPortCheckerProps> = ({ onCopyToast }) => {
  const [device, setDevice] = useState<DetectedUsbDevice | null>(null);
  const [status, setStatus] = useState<string>('في انتظار فحص التوصيل...');
  const [error, setError] = useState<string | null>(null);

  const isWebUsbSupported = typeof navigator !== 'undefined' && 'usb' in navigator;

  const handleRequestDevice = async () => {
    setError(null);
    if (!isWebUsbSupported) {
      setError('المتصفح الحالي لا يدعم WebUSB. يرجى استخدام متصفح Chrome أو Edge أو Brave على الكمبيوتر.');
      return;
    }

    try {
      setStatus('يرجى اختيار الهاتف من نافذة المتصفح المنبثقة...');
      const selected = await (navigator as any).usb.requestDevice({ filters: [] });
      setDevice({
        vendorId: selected.vendorId,
        productId: selected.productId,
        productName: selected.productName || 'جهاز هاتف غير مسمى',
        manufacturerName: selected.manufacturerName || 'غير معروف',
        serialNumber: selected.serialNumber || '—'
      });
      setStatus('✅ تم فحص منفذ USB بنجاح!');
      onCopyToast(`تم التعرف على الجهاز: VID: 0x${selected.vendorId.toString(16)}`);
    } catch (err: any) {
      if (err.name === 'NotFoundError') {
        setStatus('تم إلغاء اختيار الجهاز من قبل المستخدم.');
      } else {
        setError(err.message || 'حدث خطأ أثناء قراءة منفذ الـ USB');
        setStatus('تعذر الاتصال بالمنفذ.');
      }
    }
  };

  const vendorInfo = device ? COMMON_GSM_VENDORS[device.vendorId] : null;

  return (
    <div className="space-y-6">
      {/* Banner */}
      <div className="p-5 rounded-3xl bg-gradient-to-br from-slate-900 via-slate-900 to-cyan-950/40 border border-slate-800 space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-bold">
          <Usb className="w-3.5 h-3.5" />
          <span>فاحص منافذ USB والتعريفات السحابي — WebUSB Hardware Inspector</span>
        </div>
        <h2 className="text-lg font-black text-white">
          فحص توصيل الهاتف وحالة التعريفات مباشرة من المتصفح دون فتح Device Manager
        </h2>
        <p className="text-xs text-slate-400 leading-relaxed max-w-3xl">
          أداة مبتكرة تستخدم بروتوكول WebUSB القياسي لقراءة Vendor ID و Product ID لأي هاتف موصل بكابل USB (وضع Fastboot، كوالكوم 9008، ميديا تيك BROM، أو سامسونج)، مع إخبارك بالتعريف الناقص المطلوب تنزيله.
        </p>

        <div className="pt-2">
          <button
            onClick={handleRequestDevice}
            className="px-6 py-3 rounded-2xl bg-cyan-500 hover:bg-cyan-400 text-black font-black text-xs flex items-center gap-2 transition shadow-xl"
          >
            <Usb className="w-4 h-4" />
            <span>توصيل وفحص جهاز USB الآن</span>
          </button>
        </div>
      </div>

      {/* Status Output */}
      {error ? (
        <div className="p-4 rounded-2xl bg-red-500/10 border border-red-500/30 text-red-300 text-xs font-bold flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      ) : (
        <div className="text-xs text-slate-400 px-1">{status}</div>
      )}

      {/* Detected Device Card */}
      {device && (
        <div className="p-5 rounded-3xl bg-slate-900 border border-cyan-500/30 space-y-4 shadow-xl">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 className="text-sm font-black text-white flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-emerald-400" />
              <span>بيانات المنفذ المكتشفة:</span>
              <span className="text-cyan-400 font-mono">{device.productName}</span>
            </h3>
            <span className="text-xs font-mono font-bold text-amber-300">
              VID: 0x{device.vendorId.toString(16).padStart(4, '0')} | PID: 0x{device.productId.toString(16).padStart(4, '0')}
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
            <div className="p-3.5 rounded-2xl bg-slate-950 border border-slate-800">
              <span className="text-slate-500 block text-[10px]">المصنع (Manufacturer):</span>
              <strong className="text-white block mt-0.5">{device.manufacturerName}</strong>
            </div>

            <div className="p-3.5 rounded-2xl bg-slate-950 border border-slate-800">
              <span className="text-slate-500 block text-[10px]">نوع الشريحة / المشغل المرجح:</span>
              <strong className="text-cyan-400 block mt-0.5">
                {vendorInfo ? vendorInfo.name : 'جهاز غير مدرج بالقائمة القياسية'}
              </strong>
            </div>

            <div className="p-3.5 rounded-2xl bg-slate-950 border border-slate-800">
              <span className="text-slate-500 block text-[10px]">الوضع التقديري (Mode):</span>
              <strong className="text-emerald-400 block mt-0.5">
                {vendorInfo ? vendorInfo.type : 'منفذ تسلسلي عادي'}
              </strong>
            </div>
          </div>

          {vendorInfo && (
            <div className="p-3.5 rounded-2xl bg-cyan-950/20 border border-cyan-500/30 text-xs text-slate-300 space-y-1">
              <strong className="text-cyan-300 block">💡 إرشادات التعريف الموصى به:</strong>
              <p>{vendorInfo.driverTip} (يمكنك تحميل التعريف مباشرة من قسم التعاريف في الموقع).</p>
            </div>
          )}
        </div>
      )}

      {/* Vendor ID Quick Reference Cheat-Sheet */}
      <div className="p-5 rounded-3xl bg-slate-900/80 border border-slate-800 space-y-3">
        <h3 className="text-sm font-black text-white flex items-center gap-2">
          <Info className="w-4 h-4 text-[#00b4ff]" />
          <span>جدول معرفات الأجهزة المشهورة (Hardware Vendor ID Reference)</span>
        </h3>
        <p className="text-xs text-slate-400">
          استخدم هذه الأكواد لمقارنة المنفذ في إدارة الأجهزة Device Manager إذا تعذر التوصيل عبر المتصفح:
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5 pt-1">
          {Object.entries(COMMON_GSM_VENDORS).map(([vid, info]) => {
            const vidHex = `0x${parseInt(vid, 10).toString(16).padStart(4, '0')}`;
            return (
              <div key={vid} className="p-3 rounded-2xl bg-slate-950 border border-slate-800 text-xs">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-mono text-xs font-black text-amber-400">{vidHex}</span>
                  <span className="text-[10px] text-slate-400 font-bold">{info.name.split('/')[0]}</span>
                </div>
                <p className="text-[11px] text-slate-300 font-bold">{info.type}</p>
                <p className="text-[10px] text-slate-500 mt-1">{info.driverTip}</p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
