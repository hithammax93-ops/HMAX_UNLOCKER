import React from 'react';
import {
  Wrench,
  Cpu,
  Unlock,
  HardDrive,
  Database,
  Apple,
  Lightbulb,
  FolderGit2,
  Sparkles,
  Crown,
  Bot,
  Gift,
  Headset,
  Shield,
  Copy,
  ExternalLink,
  Check,
  Send
} from 'lucide-react';
import { MASTER_PASS, HMAX_DATA } from '../data/hmaxData';

interface HomeViewProps {
  onNavigateTab: (tab: any) => void;
  onNavigateSection?: (section: string) => void;
  onCopyToast: (msg: string) => void;
}

export const HomeView: React.FC<HomeViewProps> = ({
  onNavigateTab,
  onNavigateSection,
  onCopyToast,
}) => {
  const [copiedPass, setCopiedPass] = React.useState(false);

  const handleCopyPass = () => {
    navigator.clipboard.writeText(MASTER_PASS);
    setCopiedPass(true);
    onCopyToast(`تم نسخ الباسورد الموحد: ${MASTER_PASS}`);
    setTimeout(() => setCopiedPass(false), 2000);
  };

  const sections = [
    { id: 'tools', title: '🧰 قسم الأدوات', count: `${HMAX_DATA.tools.length} أداة`, desc: 'أحدث أدوات السوفت وير وتخطي الحمايات', tab: 'tools' },
    { id: 'drivers', title: '🔧 قسم التعاريف', count: `${HMAX_DATA.drivers.length} تعريف`, desc: 'تعاريف الموبايل وكابلات البوكسات الرسمية', tab: 'tools' },
    { id: 'dump', title: '🗄️ قسم DUMP الشامل', count: '567+ ملف', desc: 'فلاشات مسحوبة ISP و JTAG و Pandora لـ 26 ماركة', tab: 'dump', feat: true },
    { id: 'unlocking', title: '🔓 فك الشفرات', count: `${HMAX_DATA.unlocking.length} أدوات`, desc: 'شبكات دولية ويمنية (CDMA / GSM / LTE)', tab: 'tools' },
    { id: 'solutions', title: '💡 حلول مضمونة', count: '60+ حل', desc: 'تجارب FRP، تفعيل VoLTE، ثغرات معالجات MTK', tab: 'solutions' },
    { id: 'iphone', title: '🍎 قسم IPHONE', count: `${HMAX_DATA.iphone_tools.length + HMAX_DATA.iphone_pwn.length} عنصر`, desc: '3uTools، فلاشات قطع PWN DFU والجيلبريك', tab: 'tools' },
    { id: 'firmware', title: '💾 مواقع الأنظمة', count: `${HMAX_DATA.firmware_sites.length} موقع`, desc: 'رومات سامسونج، شاومي، أوبو، ريلمي الرسمية', tab: 'tools' },
    { id: 'offers', title: '🔥 عروض هيثم ماكس', count: `${HMAX_DATA.offers_hitham.length} عرض`, desc: 'اشتراكات شات جي بي تي، كانفا، ويوتيوب بأسعار مخفضة', tab: 'offers' },
    { id: 'vip', title: '💰 عروض VIP مدفوعة', count: `${HMAX_DATA.paid_offers.length} باقات`, desc: 'تفعيل بوكسات فوري، جمناي برو وسيرفرات صيانة', tab: 'offers' },
    { id: 'ai', title: '🤖 ذكاء اصطناعي', count: `${HMAX_DATA.ai_offers.length} اشتراكات`, desc: 'Gemini Pro 18 شهر، GPT Plus رسمي', tab: 'offers' },
    { id: 'free', title: '🎁 أدوات مجانية', count: `${HMAX_DATA.free_tools.length} أداة`, desc: 'أدوات ويندوز، إيقاف ديفندر، SamFW، وبرامج تنشيط', tab: 'offers' },
    { id: 'gift', title: '✨ قسم هدية لكم', count: `${HMAX_DATA.gifts.length} هدايا`, desc: 'بث شاشة الآيفون، اشتراك أدوبي، وتخطي FRP مجاناً', tab: 'offers' },
    { id: 'halabtech', title: '📂 ملفات حلب تك', count: `${HMAX_DATA.halabtech.length} عناصر`, desc: 'سحب أي فلاشة أو ملف مدفوع من سبورت حلب تك', tab: 'offers' },
    { id: 'services', title: '🎯 خدمات عن بعد', count: '24/7', desc: 'فك شفرات وإصلاح البوت عبر TeamViewer فوري', tab: 'offers' },
  ];

  return (
    <div className="space-y-4">
      {/* Hero Card */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-slate-900 via-[#0a0e1a] to-slate-950 border border-slate-800 p-5 sm:p-6 shadow-xl">
        {/* Ambient Glow */}
        <div className="absolute -top-24 -left-24 w-72 h-72 rounded-full bg-[#00b4ff]/15 blur-3xl pointer-events-none" />
        <div className="absolute -bottom-24 -right-24 w-72 h-72 rounded-full bg-blue-600/10 blur-3xl pointer-events-none" />

        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-4 max-w-xl">
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#00b4ff]/10 border border-[#00b4ff]/30 text-xs font-bold text-[#00b4ff]">
              <span>✨</span>
              <span>تطبيق أندرويد المتكامل — الإصدار الكامل 6.0</span>
            </div>

            <div>
              <h2 className="text-xl sm:text-2xl font-black text-white leading-tight flex items-center gap-2">
                <span>HMAX</span>
                <span className="text-[#00b4ff]">-</span>
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#ffd768] via-[#e6b83b] to-[#ffd768]">Unlocker</span>
              </h2>
              <p className="text-xs sm:text-sm text-slate-300 mt-1.5 leading-relaxed">
                كل خدمات وأقسام بوت السوفت وير في تطبيق أندرويد واحد: أدوات احترافية، فلاشات DUMP مسحوبة، حلول ثغرات، تفعيل VoLTE، وعروض تفعيلات فورية.
              </p>
            </div>

            {/* Quick Action Buttons */}
            <div className="flex items-center gap-2 pt-1 flex-wrap">
            <button
              onClick={() => onNavigateTab('dump')}
              className="h-10 px-4 rounded-xl bg-[#00b4ff] hover:bg-[#67e8f9] text-black font-black text-xs flex items-center gap-1.5 shadow-[0_0_20px_rgba(0,180,255,0.3)] active:scale-95 transition"
            >
              <Database className="w-4 h-4" />
              <span>تصفح فلاشات DUMP</span>
            </button>
            <button
              onClick={() => onNavigateTab('solutions')}
              className="h-10 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-100 font-bold text-xs flex items-center gap-1.5 border border-slate-700 active:scale-95 transition"
            >
              <Lightbulb className="w-4 h-4 text-amber-400" />
              <span>الحلول والشروحات</span>
            </button>
              <a
                href="https://t.me/haithamMax1"
                target="_blank"
                rel="noopener noreferrer"
                className="h-10 px-4 rounded-xl bg-blue-600/20 hover:bg-blue-600/30 text-blue-300 font-bold text-xs flex items-center gap-1.5 border border-blue-500/30 active:scale-95 transition"
              >
                <Send className="w-3.5 h-3.5" />
                <span>قناة التليجرام</span>
              </a>
            </div>
          </div>

          {/* Prominent Logo Emblem */}
          <div className="hidden sm:flex items-center justify-center shrink-0 pr-2">
            <div className="relative group">
              <div className="absolute inset-0 rounded-full bg-gradient-to-tr from-[#00b4ff]/25 via-[#ffd768]/20 to-transparent blur-2xl group-hover:blur-3xl transition-all" />
              <img
                src="/logo.svg"
                alt="شعار HMAX-Unlocker"
                className="relative w-36 h-36 md:w-44 md:h-44 object-contain drop-shadow-[0_12px_30px_rgba(0,180,255,0.45)] hover:scale-105 transition-transform duration-300"
              />
            </div>
          </div>
        </div>

        {/* Quick Metrics Bar */}
        <div className="relative z-10 grid grid-cols-3 sm:grid-cols-6 gap-2 pt-4 mt-2 border-t border-slate-800/80">
          <div className="text-center p-2 rounded-xl bg-slate-900/60 border border-slate-800/60">
            <span className="block text-base font-black text-[#00b4ff] font-mono">14</span>
            <span className="text-[10px] text-slate-400">قسم رئيسي</span>
          </div>
          <div className="text-center p-2 rounded-xl bg-slate-900/60 border border-slate-800/60">
            <span className="block text-base font-black text-amber-400 font-mono">567+</span>
            <span className="text-[10px] text-slate-400">ملف DUMP</span>
          </div>
          <div className="text-center p-2 rounded-xl bg-slate-900/60 border border-slate-800/60">
            <span className="block text-base font-black text-emerald-400 font-mono">60+</span>
            <span className="text-[10px] text-slate-400">حل وثغرة</span>
          </div>
          <div className="text-center p-2 rounded-xl bg-slate-900/60 border border-slate-800/60">
            <span className="block text-base font-black text-pink-400 font-mono">26</span>
            <span className="text-[10px] text-slate-400">عرض حصري</span>
          </div>
          <div className="text-center p-2 rounded-xl bg-slate-900/60 border border-slate-800/60">
            <span className="block text-base font-black text-purple-400 font-mono">15</span>
            <span className="text-[10px] text-slate-400">أداة مجانية</span>
          </div>
          <div className="text-center p-2 rounded-xl bg-slate-900/60 border border-slate-800/60">
            <span className="block text-base font-black text-cyan-400 font-mono">9</span>
            <span className="text-[10px] text-slate-400">هدايا حصرية</span>
          </div>
        </div>
      </div>

      {/* Master Password Bar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 p-4 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900 to-slate-900/80 border border-slate-800 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-[#00b4ff]/10 text-[#00b4ff] flex items-center justify-center shrink-0">
            <Shield className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-xs font-black text-slate-200">كلمة السر الموحدة لفك ضغط الملفات</h3>
            <p className="text-[11px] text-slate-400">تستخدم لفتح جميع ملفات DUMP والأدوات المحمية</p>
          </div>
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto">
          <code className="flex-1 sm:flex-none text-center px-4 py-2 rounded-xl bg-slate-950 border border-slate-800 text-[#00b4ff] font-mono font-black text-sm tracking-wide">
            {MASTER_PASS}
          </code>
          <button
            onClick={handleCopyPass}
            className="h-10 px-4 rounded-xl bg-[#00b4ff] hover:bg-[#67e8f9] text-black font-black text-xs flex items-center gap-1.5 active:scale-95 transition"
          >
            {copiedPass ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
            <span>{copiedPass ? 'تم النسخ!' : 'نسخ الكلمة'}</span>
          </button>
        </div>
      </div>

      {/* Main Categories Section */}
      <div className="space-y-2.5">
        <div className="flex items-center justify-between px-1">
          <h3 className="text-sm font-black text-slate-100 flex items-center gap-2">
            <span className="w-2 h-4 rounded-full bg-[#00b4ff]" />
            <span>جميع أقسام التطبيق</span>
          </h3>
          <span className="text-xs text-slate-400 font-mono">14 قسم</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5">
          {sections.map((sec) => (
            <button
              key={sec.id}
              onClick={() => {
                onNavigateTab(sec.tab);
              }}
              className={`p-4 rounded-2xl bg-slate-900/80 border text-right transition-all group flex flex-col justify-between h-28 hover:-translate-y-0.5 active:scale-[0.98] ${
                sec.feat
                  ? 'border-[#00b4ff]/40 shadow-[0_0_20px_rgba(0,180,255,0.1)]'
                  : 'border-slate-800/80 hover:border-slate-700'
              }`}
            >
              <div className="flex items-start justify-between w-full">
                <h4 className="text-sm font-bold text-slate-100 group-hover:text-white leading-tight">
                  {sec.title}
                </h4>
                <span className="text-[11px] font-mono px-2 py-0.5 rounded-full bg-slate-800 text-[#00b4ff] font-bold">
                  {sec.count}
                </span>
              </div>
              <p className="text-[11px] text-slate-400 group-hover:text-slate-300 line-clamp-1 mt-1">
                {sec.desc}
              </p>
              <div className="text-[10px] text-[#00b4ff] font-bold mt-auto flex items-center gap-1">
                <span>تصفح المحتوى</span>
                <span>←</span>
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
