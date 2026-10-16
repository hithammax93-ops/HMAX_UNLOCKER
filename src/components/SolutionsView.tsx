import React, { useState } from 'react';
import {
  Youtube,
  FileText,
  Sparkles,
  Signal,
  Wrench,
  Video,
  MessageSquare,
  ExternalLink,
  Copy,
  AlertTriangle,
  CheckCircle,
  Code,
  Stethoscope,
  ChevronDown,
  Download,
  Shield
} from 'lucide-react';
import { HMAX_DATA, ItemData } from '../data/hmaxData';
import { ItemCard } from './ItemCard';

export type SubSection =
  | 'diagnostic'
  | 'youtube'
  | 'text_guides'
  | 'experiences'
  | 'volte'
  | 'rasheed'
  | 'haitham'
  | 'samsung_msg';

export interface SolutionsViewProps {
  onCopyToast: (msg: string) => void;
  isFav: (item: ItemData) => boolean;
  onToggleFav: (item: ItemData) => void;
  initialSubSection?: SubSection;
}

interface DiagnosticCase {
  id: string;
  title: string;
  badge: string;
  cause: string;
  action: string;
  tool: string;
  toolLink: string;
  driver: string;
  driverLink: string;
  steps: string[];
}

const DIAGNOSTIC_CASES: DiagnosticCase[] = [
  {
    id: "dead_boot",
    title: "موت الهاتف بعد تفليش خاطئ (Dead Boot / Bricked Phone)",
    badge: "طوارئ وبوت ميت",
    cause: "كتابة ملف preloader أو lk غير متطابق مع لوحة الهاتف، أو انقطاع الكابل أثناء عملية التفليش.",
    tool: "Pandora Tool / F64 ULTRA / AMT",
    toolLink: "https://downloads1.z3x.dev/getLatestVersion.php",
    driver: "MTK Bypass Auth Fix + QCOM 9008 Driver",
    driverLink: "https://www.mediafire.com/file_premium/cm92fbnnig76nn4/Driver-Mtk-Fix-ChuyenMobileGsm.zip/file",
    steps: [
      "فك ظهر الهاتف واستخراج بطاقة SIM والبطارية (أو فصل فلاتة البطارية 10 ثوانٍ).",
      "توصيل نقاط التيست بوينت (Test Point) بالأرضي أثناء توصيل كابل USB لإجبار المعالج على الدخول لوضع BROM أو 9008.",
      "تثبيت باتش تجاوز الحماية MTK Bypass Auth لتخطي حماية الـ DA.",
      "فتح أداة Pandora أو AMT واختيار موديل مشابه أو نفس المعالج ثم كتابة بارتيشن lk_a و lk_b فقط لإحياء الشاشة.",
      "إعادة تشغيل الهاتف وسحب نسخة احتياطية فورية من ملفات الشبكة."
    ],
    action: "إحياء المعالج عبر وضع الطوارئ BROM / EDL"
  },
  {
    id: "frp_bypass",
    title: "تخطي قفل حساب جوجل (FRP Google Account Bypass)",
    badge: "FRP & Google Lock",
    cause: "إعادة ضبط المصنع للهاتف بدون إزالة حساب Gmail، وتوقف الهاتف عند شاشة تأكيد الحساب.",
    tool: "SamFW Tool 6.0.1 (أداة مجانية) / UnlockTool",
    toolLink: "https://samfw.com/SamFwToolSetup_v6.0.1.zip",
    driver: "Samsung USB Driver v3 + ADB Universal",
    driverLink: "https://www.mediafire.com/file_premium/92yzwgkkvkutye5/SAMSUNG_USB_Driver_for_Mobile_Phones_3.exe/file",
    steps: [
      "لهواتف سامسونج: الدخول لشاشة الطوارئ وكتابة الكود *#0*# ثم فتح SamFW Tool والضغط على Remove FRP.",
      "لهواتف موتورولا وتكنو: إدخال الهاتف وضع Fastboot واختيار Reset FRP بنقرة واحدة على TSM Pro.",
      "لهواتف شاومي وبوكو: الدخول لوضع Mi Assistant عبر الريكفري والتخطي عبر SamFW Tool.",
      "إعادة تشغيل الهاتف والدخول مباشرة لواجهة النظام بدون الحاجة لحساب."
    ],
    action: "تخطي مباشر بنقرة واحدة عبر وضع ADB / MTP"
  },
  {
    id: "null_imei",
    title: "فقدان السيريال والشبكة (IMEI Null / Baseband Unknown)",
    badge: "إصلاح السيريال والشبكة",
    cause: "تفليش كامل بالخيار الخطأ Format All + Download مما يمسح بارتشنات NVRAM و NVDATA و EFS المشفرة.",
    tool: "Infinity CM2 / Pandora Tool",
    toolLink: "https://infinity-box.com/download/",
    driver: "ADB Fix Yemen + MTK Driver v2.0.1.1",
    driverLink: "https://mega.nz/file/UgZwSCRS#rgIJ8Wdli6yG_m6V7aWzJZmrVLIfHTrzQWZUhvU6Ums",
    steps: [
      "تحميل فلاشة DUMP مسحوبة لنفس الموديل من قسم فلاشات DUMP في التطبيق.",
      "كتابة بارتيشن NVRAM و NVDATA المرفق مع الدامب لاستعادة البيسباند (Baseband).",
      "إدخال الهاتف في وضع META Mode عبر كابل USB بدون بطارية.",
      "فتح خانة إصلاح السيريال في CM2 أو Pandora وكتابة السيريال الأصلي المطبوع خلف البطارية.",
      "إعادة تشغيل الهاتف وطلب الكود *#06# للتأكد من رجوع السيريال."
    ],
    action: "استعادة بارتشنات NVRAM المشفرة وكتابة السيريال"
  },
  {
    id: "volte_fix",
    title: "تفعيل مكالمات 4G VoLTE (يمن موبايل / سبأفون / US Carriers)",
    badge: "VoLTE & 4G Data",
    cause: "فقدان ملف تعريف شبكة الجيل الرابع IMS بعد تحديث النظام أو تشغيل شريحة يمن موبايل 4G.",
    tool: "QCDMA Tool / أكواد Engineer Mode",
    toolLink: "https://mega.nz/folder/fEQVBLab#1cPjBryW2_XPmqjxDoNZ0Q",
    driver: "Qualcomm Driver HS-USB 9008 + ADB Fix",
    driverLink: "https://www.mediafire.com/file_premium/huiyajts19ntc0y/drivers_qcom_v1.0.7z/file",
    steps: [
      "الدخول لتطبيق الاتصال وكتابة الكود *#*#86583#*#* لتعطيل فحص توافق المشغل (Carrier Check Disabled).",
      "الدخول لضبط الشبكة وإضافة نقطة وصول جديدة: Name: ymdata | APN: ymdata.",
      "لمعالجات ميديا تيك: الدخول لقائمة المهندس *#*#3646633#*#* ثم Telephony -> IMS والضغط على Set VoLTE.",
      "لمعالجات كوالكوم: تفعيل Diag Mode وتمرير ملف الـ Carrier Policy عبر أداة QCDMA.",
      "إعادة تشغيل الهاتف وستظهر أيقونة VoLTE فوراً."
    ],
    action: "تجاوز فحص المشغل وضبط إعدادات الـ IMS"
  },
  {
    id: "knox_mdm",
    title: "تخطي الحماية المؤسساتية (Samsung KNOX / MDM / KG Locked)",
    badge: "Samsung KNOX & KG",
    cause: "أجهزة تابعة لشركات أو برامج تقسيط مقفلة من السيرفر بنظام الإدارة المؤسساتية.",
    tool: "TSM Pro Edition 2026",
    toolLink: "https://www.mediafire.com/file/vqiuhtmypiv7gzs/TSM+Pro+Edition+Setup[2026.10.16].7z/file",
    driver: "Samsung USB Driver v3",
    driverLink: "https://www.mediafire.com/file_premium/92yzwgkkvkutye5/SAMSUNG_USB_Driver_for_Mobile_Phones_3.exe/file",
    steps: [
      "تفعيل وضع ADB Root عبر أداة MOBILedit أو ثغرة المتصفح.",
      "فتح موجه الأوامر وتشغيل الدايلر: adb shell am start -n com.samsung.android.dialer/.DialerActivity",
      "في لوحة الاتصال اكتب الكود *#0808# واختر وضع RNDIS + ACM + DM ثم Reboot.",
      "افتح أداة TSM Pro وتوجه إلى خانة Samsung FRP / MDM واضغط Bypass KNOX.",
      "تم تخطي القفل بنجاح وبصورة دائمة."
    ],
    action: "تفعيل منفذ DM وتخطي تطبيق الحماية عبر ADB"
  },
  {
    id: "system_destroyed",
    title: "شاشة System has been destroyed في شاومي وبوكو",
    badge: "Xiaomi HyperOS",
    cause: "تحديث خاطئ لواجهة HyperOS أو محاولة الرجوع لإصدار أندرويد أقدم مع انغلاق البوتلودر.",
    tool: "UnlockTool / DFT Pro / MiFlash",
    toolLink: "https://file.unlocktool.net/",
    driver: "Fastboot Driver + Qualcomm 9008 Driver",
    driverLink: "https://mega.nz/file/w0plHSKZ#TjvkWuc9OmOpQiJq7Nr0U-ANlPVyf7RP1-2KvcgaSO4",
    steps: [
      "تحميل روم Fastboot الرسمي المطابق لحماية الجهاز من موقع MiFirm.",
      "إدخال الهاتف وضع BROM لميديا تيك أو وضع EDL 9008 لكوالكوم عبر التيست بوينت.",
      "فتح أداة UnlockTool أو DFT Pro وتمرير الفلاشة دون تفعيل خيار قفل البوتلودر (Clean All).",
      "في حالة Redmi 12C تمرير ملف الـ lk المعالج المستخرج لتخطي حظر التحديث.",
      "إعادة تشغيل الهاتف والدخول للنظام بنجاح."
    ],
    action: "تفليش كامل عبر وضع الطوارئ وتفادي قفل البوتلودر"
  }
];

export const SolutionsView: React.FC<SolutionsViewProps> = ({
  onCopyToast,
  isFav,
  onToggleFav,
  initialSubSection = 'diagnostic',
}) => {
  const [activeSub, setActiveSub] = useState<SubSection>(initialSubSection);
  const [selectedGuideId, setSelectedGuideId] = useState<string | null>(null);
  const [selectedCaseId, setSelectedCaseId] = useState<string>('dead_boot');

  React.useEffect(() => {
    if (initialSubSection) {
      setActiveSub(initialSubSection);
    }
  }, [initialSubSection]);

  const subSections = [
    { id: 'diagnostic' as SubSection, label: '🔍 فاحص وحلول الأعطال', icon: Stethoscope, count: DIAGNOSTIC_CASES.length },
    { id: 'youtube' as SubSection, label: 'FRP يوتيوب', icon: Youtube, count: HMAX_DATA.solutions.youtube.length },
    { id: 'text_guides' as SubSection, label: 'شروحات نصية', icon: FileText, count: HMAX_DATA.solutions.text_guides.length },
    { id: 'experiences' as SubSection, label: 'تجارب ناجحة', icon: Sparkles, count: HMAX_DATA.solutions.experiences.length },
    { id: 'volte' as SubSection, label: 'تفعيل VoLTE', icon: Signal, count: HMAX_DATA.solutions.volte.length },
    { id: 'rasheed' as SubSection, label: 'أكواد رشيد', icon: Wrench, count: HMAX_DATA.solutions.rasheed.length },
    { id: 'haitham' as SubSection, label: 'فيديوهات هيثم', icon: Video, count: HMAX_DATA.solutions.haitham.length },
    { id: 'samsung_msg' as SubSection, label: 'Samsung Msg', icon: MessageSquare, count: 1 },
  ];

  const selectedGuide = HMAX_DATA.solutions.text_guides.find((g) => g.id === selectedGuideId);
  const activeCase = DIAGNOSTIC_CASES.find((c) => c.id === selectedCaseId) || DIAGNOSTIC_CASES[0];

  return (
    <div className="space-y-4">
      {/* Sub-navigation bar with horizontal scroll for mobile */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none no-scrollbar">
        {subSections.map((sec) => {
          const Icon = sec.icon;
          const isActive = activeSub === sec.id;
          return (
            <button
              key={sec.id}
              onClick={() => {
                setActiveSub(sec.id);
                setSelectedGuideId(null);
              }}
              className={`flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-bold whitespace-nowrap transition-all ${
                isActive
                  ? 'bg-[#00b4ff] text-black shadow-[0_0_12px_rgba(0,180,255,0.3)]'
                  : 'bg-slate-900/80 text-slate-300 hover:bg-slate-800 border border-slate-800'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{sec.label}</span>
              <span
                className={`text-[10px] px-1.5 py-0.2 rounded-full ${
                  isActive ? 'bg-black/20 text-black' : 'bg-slate-800 text-slate-400'
                }`}
              >
                {sec.count}
              </span>
            </button>
          );
        })}
      </div>

      {/* 0. INTERACTIVE DIAGNOSTIC TROUBLESHOOTER */}
      {activeSub === 'diagnostic' && (
        <div className="space-y-4">
          <div className="p-4 rounded-2xl bg-gradient-to-br from-slate-900 via-slate-900 to-slate-950 border border-slate-800">
            <span className="text-xs font-bold text-[#00b4ff] block mb-1">
              اختر العطل البرمجي لتشخيصه والاطلاع على طريقة الحل المعتمدة:
            </span>

            {/* Diagnostic Cases Pills */}
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2 mt-3">
              {DIAGNOSTIC_CASES.map((c) => {
                const isSelected = selectedCaseId === c.id;
                return (
                  <button
                    key={c.id}
                    onClick={() => setSelectedCaseId(c.id)}
                    className={`p-3 rounded-xl text-right transition border text-xs flex flex-col justify-between ${
                      isSelected
                        ? 'bg-[#00b4ff]/15 border-[#00b4ff] text-white shadow-sm'
                        : 'bg-slate-950/70 border-slate-800 text-slate-300 hover:border-slate-700'
                    }`}
                  >
                    <div className="flex items-center justify-between gap-1 w-full mb-1">
                      <span className="text-[10px] font-mono text-[#00b4ff]">{c.badge}</span>
                      {isSelected && <span className="w-2 h-2 rounded-full bg-[#00b4ff]" />}
                    </div>
                    <span className="font-bold leading-snug">{c.title}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Active Diagnostic Detail Card */}
          <div className="rounded-2xl bg-slate-900/90 border border-slate-800 p-5 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-slate-800">
              <div>
                <span className="text-xs text-[#00b4ff] font-bold">{activeCase.badge}</span>
                <h3 className="text-base font-black text-white">{activeCase.title}</h3>
              </div>
              <span className="text-xs font-mono px-3 py-1 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 self-start sm:self-auto font-bold">
                {activeCase.action}
              </span>
            </div>

            {/* Cause Statement */}
            <div className="p-3.5 rounded-xl bg-red-950/20 border border-red-900/30 text-xs text-red-200">
              <span className="font-bold text-red-400 block mb-1">السبب الجذري للمشكلة:</span>
              <p className="leading-relaxed">{activeCase.cause}</p>
            </div>

            {/* Recommended Tools & Drivers */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between gap-2">
                <div>
                  <span className="text-[10px] text-slate-500 block mb-0.5">الأداة الموصى بها</span>
                  <span className="text-xs font-bold text-white block">{activeCase.tool}</span>
                </div>
                <a
                  href={activeCase.toolLink}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-2.5 py-1.5 rounded-lg bg-[#00b4ff] hover:bg-[#67e8f9] text-black font-black text-[11px] flex items-center gap-1 transition shrink-0"
                >
                  <Download className="w-3 h-3" />
                  <span>تحميل</span>
                </a>
              </div>

              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between gap-2">
                <div>
                  <span className="text-[10px] text-slate-500 block mb-0.5">التعريف المطلوب</span>
                  <span className="text-xs font-bold text-white block truncate max-w-[180px]">{activeCase.driver}</span>
                </div>
                <a
                  href={activeCase.driverLink}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-bold text-[11px] flex items-center gap-1 transition shrink-0"
                >
                  <Download className="w-3 h-3 text-[#00b4ff]" />
                  <span>التعريف</span>
                </a>
              </div>
            </div>

            {/* Step by Step Action Plan */}
            <div className="space-y-2 pt-1">
              <span className="text-xs font-bold text-slate-200 block">خطوات التنفيذ والإصلاح المعتمدة:</span>
              {activeCase.steps.map((st, i) => (
                <div
                  key={i}
                  className="flex items-start gap-3 p-3 rounded-xl bg-slate-950/70 border border-slate-800 text-xs text-slate-300 leading-relaxed"
                >
                  <span className="w-5 h-5 rounded-full bg-[#00b4ff] text-black font-black text-xs flex items-center justify-center shrink-0 mt-0.5">
                    {i + 1}
                  </span>
                  <span>{st}</span>
                </div>
              ))}
            </div>

            {/* Support Note */}
            <div className="flex items-center justify-between gap-3 p-3 rounded-xl bg-blue-950/30 border border-blue-800/40 text-xs text-blue-200">
              <div className="flex items-center gap-2">
                <Shield className="w-4 h-4 text-[#00b4ff] shrink-0" />
                <span>تحتاج مساعدة أو ملفاً مخصصاً لجهازك؟</span>
              </div>
              <a
                href="https://t.me/hithamMax"
                target="_blank"
                rel="noopener noreferrer"
                className="font-bold text-[#00b4ff] hover:underline shrink-0"
              >
                تواصل مع هيثم ماكس ←
              </a>
            </div>
          </div>
        </div>
      )}

      {/* 1. YouTube FRP */}
      {activeSub === 'youtube' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {HMAX_DATA.solutions.youtube.map((item) => (
            <ItemCard
              key={item.id}
              item={item}
              isFav={isFav(item)}
              onToggleFav={onToggleFav}
              onCopyToast={onCopyToast}
              badgeLabel="شرح فيديو يوتيوب"
            />
          ))}
        </div>
      )}

      {/* 2. Text Guides */}
      {activeSub === 'text_guides' && (
        <div className="space-y-4">
          {!selectedGuide ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {HMAX_DATA.solutions.text_guides.map((g) => (
                <div
                  key={g.id}
                  onClick={() => setSelectedGuideId(g.id)}
                  className="cursor-pointer p-4 rounded-2xl bg-slate-900/80 border border-slate-800 hover:border-[#00b4ff]/40 transition group flex flex-col justify-between"
                >
                  <div>
                    <span className="text-[11px] font-semibold text-[#00b4ff] block mb-1">
                      {g.tag}
                    </span>
                    <h3 className="text-sm font-bold text-slate-100 group-hover:text-white leading-snug mb-2">
                      {g.title}
                    </h3>
                    <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed">
                      {g.problem}
                    </p>
                  </div>
                  <div className="pt-3 border-t border-slate-800/60 mt-3 flex items-center justify-between text-xs text-[#00b4ff] font-bold">
                    <span>قراءة الحل والخطوات</span>
                    <span>←</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            /* Selected Guide Details */
            <div className="rounded-2xl bg-slate-900/90 border border-slate-800 p-5 space-y-4">
              <button
                onClick={() => setSelectedGuideId(null)}
                className="text-xs text-[#00b4ff] hover:underline font-bold mb-2 inline-flex items-center gap-1"
              >
                <span>→</span>
                <span>العودة لقائمة الشروحات</span>
              </button>

              <div>
                <span className="text-xs text-[#00b4ff] font-semibold">{selectedGuide.tag}</span>
                <h3 className="text-base font-black text-white mt-0.5">{selectedGuide.title}</h3>
              </div>

              {/* Problem Statement */}
              <div className="p-3 rounded-xl bg-red-950/20 border border-red-800/30 text-xs text-red-200 space-y-1">
                <div className="flex items-center gap-1.5 font-bold text-red-400">
                  <AlertTriangle className="w-4 h-4" />
                  <span>المشكلة:</span>
                </div>
                <p>{selectedGuide.problem}</p>
              </div>

              {/* Steps */}
              <div className="space-y-2 pt-2">
                <h4 className="text-xs font-bold text-slate-300">خطوات التنفيذ المعتمدة:</h4>
                {selectedGuide.steps.map((st) => (
                  <div
                    key={st.num}
                    className="flex items-start gap-3 p-3 rounded-xl bg-slate-950/60 border border-slate-800 text-xs text-slate-300 leading-relaxed"
                  >
                    <span className="w-5 h-5 rounded-full bg-[#00b4ff] text-black font-black text-xs flex items-center justify-center shrink-0 mt-0.5">
                      {st.num}
                    </span>
                    <span>{st.text}</span>
                  </div>
                ))}
              </div>

              {/* Code Snippet if exists */}
              {selectedGuide.codeSnippet && (
                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-[11px] font-mono text-slate-400 flex items-center gap-1">
                      <Code className="w-3.5 h-3.5 text-[#00b4ff]" />
                      <span>كود / أمر ADB:</span>
                    </span>
                    <button
                      onClick={() => {
                        navigator.clipboard.writeText(selectedGuide.codeSnippet!);
                        onCopyToast('تم نسخ الأمر إلى الحافظة');
                      }}
                      className="text-xs text-[#00b4ff] hover:underline font-bold"
                    >
                      نسخ
                    </button>
                  </div>
                  <pre className="text-xs font-mono text-emerald-400 overflow-x-auto p-2 bg-black/40 rounded-lg">
                    {selectedGuide.codeSnippet}
                  </pre>
                </div>
              )}

              {/* Conclusion / Note */}
              {selectedGuide.conclusionNote && (
                <div className="p-3 rounded-xl bg-emerald-950/20 border border-emerald-800/30 text-xs text-emerald-300 flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 shrink-0" />
                  <span>{selectedGuide.conclusionNote}</span>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* 3. Experiences */}
      {activeSub === 'experiences' && (
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {HMAX_DATA.solutions.experiences.map((exp) => (
              <div
                key={exp.id}
                className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-3 flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between gap-2 mb-1">
                    <span className="text-[11px] font-mono text-[#00b4ff]">
                      بواسطة: {exp.author}
                    </span>
                  </div>
                  <h3 className="text-sm font-bold text-white leading-snug mb-2">
                    {exp.title}
                  </h3>

                  <div className="p-2.5 rounded-xl bg-slate-950/70 border border-slate-800/80 text-xs text-slate-300 mb-2">
                    <span className="text-slate-500 font-bold block mb-0.5">الحالة:</span>
                    <p className="line-clamp-2">{exp.problem}</p>
                  </div>

                  {exp.solutionDesc && (
                    <p className="text-xs text-emerald-400 leading-relaxed">
                      ✓ {exp.solutionDesc}
                    </p>
                  )}

                  {exp.warning && (
                    <p className="text-[11px] text-amber-400 leading-relaxed mt-1">
                      ⚠️ {exp.warning}
                    </p>
                  )}
                </div>

                <div className="flex items-center gap-2 pt-3 border-t border-slate-800/60 flex-wrap">
                  {exp.links.map((link, idx) => (
                    <a
                      key={idx}
                      href={link.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className={`h-8 px-3 rounded-lg text-xs font-bold flex items-center gap-1 transition ${
                        link.primary
                          ? 'bg-[#00b4ff] hover:bg-[#67e8f9] text-black font-black'
                          : 'bg-slate-800 hover:bg-slate-700 text-slate-200'
                      }`}
                    >
                      <ExternalLink className="w-3 h-3" />
                      <span>{link.label}</span>
                    </a>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 4. VoLTE Guides */}
      {activeSub === 'volte' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {HMAX_DATA.solutions.volte.map((item) => (
            <ItemCard
              key={item.id}
              item={item}
              isFav={isFav(item)}
              onToggleFav={onToggleFav}
              onCopyToast={onCopyToast}
              badgeLabel="تفعيل شبكة VoLTE"
            />
          ))}
        </div>
      )}

      {/* 5. Rasheed Mdghmer Codes */}
      {activeSub === 'rasheed' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {HMAX_DATA.solutions.rasheed.map((item) => (
            <ItemCard
              key={item.id}
              item={item}
              isFav={isFav(item)}
              onToggleFav={onToggleFav}
              onCopyToast={onCopyToast}
              badgeLabel="لمسات رشيد مدغمر"
            />
          ))}
        </div>
      )}

      {/* 6. Haitham Max Videos */}
      {activeSub === 'haitham' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {HMAX_DATA.solutions.haitham.map((item) => (
            <ItemCard
              key={item.id}
              item={item}
              isFav={isFav(item)}
              onToggleFav={onToggleFav}
              onCopyToast={onCopyToast}
              badgeLabel="شروحات هيثم ماكس"
            />
          ))}
        </div>
      )}

      {/* 7. Samsung Messages APK Fix */}
      {activeSub === 'samsung_msg' && (
        <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-4">
          <div>
            <h3 className="text-base font-black text-white">
              {HMAX_DATA.solutions.samsung_msg.title}
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              حل مشكلة التحديث التلقائي إلى تطبيق جوجل ميسيجز وفقدان الرسائل
            </p>
          </div>

          <div className="p-3 rounded-xl bg-amber-950/20 border border-amber-800/30 text-xs text-amber-200">
            <span className="font-bold block mb-1">سبب المشكلة:</span>
            <p className="leading-relaxed">{HMAX_DATA.solutions.samsung_msg.problem}</p>
          </div>

          <div className="space-y-2">
            <h4 className="text-xs font-bold text-slate-300">خطوات وإضافات التحديث الجديد:</h4>
            {HMAX_DATA.solutions.samsung_msg.updates.map((up) => (
              <div
                key={up.num}
                className="flex items-center gap-2.5 p-2.5 rounded-xl bg-slate-950/60 border border-slate-800 text-xs text-slate-300"
              >
                <span className="w-5 h-5 rounded-full bg-[#00b4ff] text-black font-black text-[11px] flex items-center justify-center shrink-0">
                  {up.num}
                </span>
                <span>{up.text}</span>
              </div>
            ))}
          </div>

          <div className="flex items-center gap-2 pt-2 border-t border-slate-800 flex-wrap">
            {HMAX_DATA.solutions.samsung_msg.links.map((link, idx) => (
              <a
                key={idx}
                href={link.url}
                target="_blank"
                rel="noopener noreferrer"
                className={`h-9 px-4 rounded-xl text-xs font-bold flex items-center gap-1.5 transition ${
                  link.primary
                    ? 'bg-[#00b4ff] hover:bg-[#67e8f9] text-black font-black'
                    : 'bg-slate-800 hover:bg-slate-700 text-slate-200'
                }`}
              >
                <ExternalLink className="w-3.5 h-3.5" />
                <span>{link.label}</span>
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
