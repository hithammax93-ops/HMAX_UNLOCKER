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
    { id: 'tech_utils', title: '🛠️ أدوات ومختبر الفني', count: '14 أداة 🔥', desc: 'أوامر Fastboot & ADB، أكواد المهندس، ونقاط التيست بوينت وسجل الصيانة', tab: 'tech_utils', feat: true },
    { id: 'samsung_bin', title: '🛡️ محلل حمايات سامسونج', count: 'Bit Check', desc: 'تفكيك كود الفلاشة وحساب رقم الحماية U/S وتفادي خطأ موت الهاتف', tab: 'tech_utils', feat: true },
    { id: 'script_gen', title: '⚡ مولد سكريبتات التفليش', count: 'Auto Bat', desc: 'توليد ملفات تشغيل فاست بوت تلقائية لتفليش البارتشنات دون كتابة أوامر', tab: 'tech_utils', feat: true },
    { id: 'flash_errors', title: '📖 موسوعة أخطاء التفليش', count: '20+ خطأ', desc: 'دليل وحلول أخطاء SP Flash Tool و Odin و QFIL و UnlockTool و Pandora', tab: 'tech_utils' },
    { id: 'webusb', title: '🔌 فاحص منافذ USB والتعريفات', count: 'WebUSB', desc: 'فحص اتصال الهاتف وقراءة Vendor ID مباشرة وتحديد التعريف الناقص', tab: 'tech_utils' },
    { id: 'pricing', title: '💰 حاسبة تسعير الخدمات', count: 'GSM Profit', desc: 'تقدير تكلفة السيرفرات وسعر الخدمة العادل للزبون وصافي الأرباح', tab: 'tech_utils' },
    { id: 'dump', title: '🗄️ قسم DUMP الشامل', count: '576+ ملف', desc: 'فلاشات مسحوبة ISP و JTAG و Pandora لـ 27 ماركة و 141 موديل تكنو و 9 أنظمة LT', tab: 'dump', feat: true },
    { id: 'iphone_carrier', title: '📱 شفرات الآيفون & IMSI', count: '17 شبكة', desc: 'أكواد AT&T, Verizon, Sprint والشرائح الإلكترونية وأسعار الآيكلود', tab: 'tech_utils' },
    { id: 'lt_official', title: '📂 أنظمة هواتف LT الرسمية', count: '9 هواتف', desc: 'فلاشات كاملة مجانية LT M20, M30, M50S, M25, M40, M60, M70', tab: 'tech_utils' },
    { id: 'tech_ranks', title: '🏆 رتب ومكافآت الفنيين', count: 'نقاط VIP', desc: 'سجل حضورك اليومي، اكسب نقاطاً مع كل أداة، واستبدلها باشتراكات حقيقية', tab: 'tech_utils' },
    { id: 'calc_csc', title: '🔢 حاسبة السيريال & CSC', count: 'Luhn Check', desc: 'حساب الرقم الـ 15 القانوني للسيريال وقاعدة بيانات أكواد سامسونج', tab: 'tech_utils' },
    { id: 'tools', title: '🧰 قسم الأدوات والبرامج', count: `${HMAX_DATA.tools.length} أداة`, desc: 'MaxTech VIP 2.0، Chimera، TSM Pro، و UnlockTool', tab: 'tools' },
    { id: 'drivers', title: '🔧 قسم التعاريف الرسمية', count: `${HMAX_DATA.drivers.length} تعريف`, desc: 'تعاريف الموبايل وكابلات البوكسات وكوالكوم 9008', tab: 'tools' },
    { id: 'unlocking', title: '🔓 فك الشفرات والشبكات', count: `${HMAX_DATA.unlocking.length} أدوات`, desc: 'شبكات دولية ويمنية (CDMA / GSM / LTE)', tab: 'tools' },
    { id: 'solutions', title: '💡 حلول وثغرات مجربة', count: '60+ حل', desc: 'فاحص الأعطال، تخطي Exynos مجاني، تفعيل VoLTE، وثغرات MTK', tab: 'solutions' },
    { id: 'iphone', title: '🍎 قسم IPHONE والجيلبريك', count: `${HMAX_DATA.iphone_tools.length + HMAX_DATA.iphone_pwn.length} عنصر`, desc: '3uTools، فلاشات قطع PWN DFU والجيلبريك', tab: 'tools' },
    { id: 'firmware', title: '💾 مواقع الأنظمة الرسمية', count: `${HMAX_DATA.firmware_sites.length} موقع`, desc: 'رومات سامسونج، شاومي، أوبو، ريلمي الرسمية', tab: 'tools' },
    { id: 'offers', title: '🔥 عروض هيثم ماكس', count: `${HMAX_DATA.offers_hitham.length} عرض`, desc: 'اشتراكات شات جي بي تي، كانفا، ويوتيوب بأسعار مخفضة', tab: 'offers' },
    { id: 'vip', title: '💰 عروض VIP مدفوعة', count: `${HMAX_DATA.paid_offers.length} باقات`, desc: 'تفعيل بوكسات فوري، جمناي برو وسيرفرات صيانة', tab: 'offers' },
    { id: 'halabtech', title: '📂 ملفات حلب تك المباشرة', count: `${HMAX_DATA.halabtech.length} عناصر`, desc: 'سحب أي فلاشة أو ملف مدفوع من سبورت حلب تك فوري', tab: 'offers' },
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

      {/* Official Community & Direct Channels (from main.py) */}
      <div className="p-5 rounded-3xl bg-gradient-to-br from-slate-900 to-slate-950 border border-slate-800 space-y-3 mt-4">
        <div className="flex items-center justify-between flex-wrap gap-2">
          <div>
            <h3 className="text-sm font-black text-white flex items-center gap-2">
              <span className="text-emerald-400">💬</span>
              <span>قنوات ومجتمعات هيثم ماكس الرسمية (HMAX Channels)</span>
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              انضم إلى القنوات الرسمية للحصول على أحدث التحديثات، الفلاشات الحصرية، والدعم الفني المباشر
            </p>
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2.5 pt-1">
          <a
            href="https://t.me/haithamMax1"
            target="_blank"
            rel="noreferrer"
            className="p-3 rounded-2xl bg-slate-950 border border-blue-500/30 hover:border-blue-400 hover:bg-blue-950/20 text-center transition group flex flex-col items-center justify-center gap-1.5"
          >
            <span className="text-xl">📢</span>
            <span className="text-xs font-bold text-white group-hover:text-blue-300">قناة التليجرام</span>
            <span className="text-[10px] text-slate-500 font-mono">@haithamMax1</span>
          </a>

          <a
            href="https://t.me/hithamMax"
            target="_blank"
            rel="noreferrer"
            className="p-3 rounded-2xl bg-slate-950 border border-cyan-500/30 hover:border-cyan-400 hover:bg-cyan-950/20 text-center transition group flex flex-col items-center justify-center gap-1.5"
          >
            <span className="text-xl">👤</span>
            <span className="text-xs font-bold text-white group-hover:text-cyan-300">المهندس هيثم</span>
            <span className="text-[10px] text-slate-500 font-mono">@hithamMax</span>
          </a>

          <a
            href="https://wa.me/967772773388"
            target="_blank"
            rel="noreferrer"
            className="p-3 rounded-2xl bg-slate-950 border border-emerald-500/30 hover:border-emerald-400 hover:bg-emerald-950/20 text-center transition group flex flex-col items-center justify-center gap-1.5"
          >
            <span className="text-xl">📱</span>
            <span className="text-xs font-bold text-white group-hover:text-emerald-300">واتساب مباشر</span>
            <span className="text-[10px] text-slate-500 font-mono">+967 772773388</span>
          </a>

          <a
            href="https://whatsapp.com/channel/0029VbB8JX00gcfD5Y5o1G46"
            target="_blank"
            rel="noreferrer"
            className="p-3 rounded-2xl bg-slate-950 border border-emerald-500/30 hover:border-emerald-400 hover:bg-emerald-950/20 text-center transition group flex flex-col items-center justify-center gap-1.5"
          >
            <span className="text-xl">🟢</span>
            <span className="text-xs font-bold text-white group-hover:text-emerald-300">قناة واتساب 1</span>
            <span className="text-[10px] text-slate-500 font-mono">محدثة يومياً</span>
          </a>

          <a
            href="https://whatsapp.com/channel/0029Vb6TvYnA2pLEgTFZ5S1W"
            target="_blank"
            rel="noreferrer"
            className="p-3 rounded-2xl bg-slate-950 border border-emerald-500/30 hover:border-emerald-400 hover:bg-emerald-950/20 text-center transition group flex flex-col items-center justify-center gap-1.5"
          >
            <span className="text-xl">🟢</span>
            <span className="text-xs font-bold text-white group-hover:text-emerald-300">قناة واتساب 2</span>
            <span className="text-[10px] text-slate-500 font-mono">عروض واشتراكات</span>
          </a>

          <a
            href="https://wa.me/message/A3KQWHSSERCFG1"
            target="_blank"
            rel="noreferrer"
            className="p-3 rounded-2xl bg-slate-950 border border-amber-500/30 hover:border-amber-400 hover:bg-amber-950/20 text-center transition group flex flex-col items-center justify-center gap-1.5"
          >
            <span className="text-xl">🛍️</span>
            <span className="text-xs font-bold text-white group-hover:text-amber-300">متجر التفعيلات</span>
            <span className="text-[10px] text-slate-500 font-mono">Store WhatsApp</span>
          </a>
        </div>
      </div>
    </div>
  );
};
