import React, { useState, useEffect, useMemo } from 'react';
import {
  Terminal,
  Key,
  Radio,
  Cpu,
  ClipboardList,
  Copy,
  Check,
  Search,
  ExternalLink,
  Plus,
  Trash2,
  Send,
  Shield,
  AlertTriangle,
  Sparkles,
  Smartphone,
  Award,
  Calculator,
  Gift,
  Flame,
  Crown,
  ChevronDown,
  Download,
  Info,
  Layers,
  ShieldCheck,
  BookOpenCheck,
  Database
} from 'lucide-react';
import {
  ADB_FASTBOOT_COMMANDS,
  SECRET_DIAL_CODES,
  APN_PROFILES,
  TESTPOINT_GUIDES,
  CommandItem,
  SecretCodeItem,
  APNProfile,
  TestPointGuide
} from '../data/technicianToolsData';
import {
  IPHONE_CARRIER_CODES,
  ICLOUD_OFFICIAL_PRICES,
  IPHONE_METHOD_RESOURCES
} from '../data/iphoneUnlockData';
import { LT_PHONES_CATALOG } from '../data/ltPhonesData';
import { useTechRank, ACHIEVEMENTS_LIST, USER_RANKS } from '../hooks/useTechRank';
import { MASTER_PASS } from '../data/hmaxData';
import { CustomerReceiptModal, ReceiptData } from './CustomerReceiptModal';
import { SamsungBinaryChecker } from './SamsungBinaryChecker';
import { FlashScriptGenerator } from './FlashScriptGenerator';
import { FlashErrorDictionary } from './FlashErrorDictionary';
import { WebUsbPortChecker } from './WebUsbPortChecker';
import { GsmPricingCalculator } from './GsmPricingCalculator';
import { Printer, Usb, DollarSign, AlertOctagon, Play } from 'lucide-react';
import { TechnicianDesk } from './TechnicianDesk';

export type TechTab =
  | 'commands'
  | 'samsung_bin'
  | 'script_gen'
  | 'flash_errors'
  | 'codes'
  | 'iphone'
  | 'lt_phones'
  | 'ranks'
  | 'webusb'
  | 'pricing'
  | 'calc'
  | 'apn'
  | 'testpoints'
  | 'tracker'
  | 'compatibility'
  | 'diagnostics'
  | 'device_log';

export interface TechUtilsViewProps {
  onCopyToast: (msg: string) => void;
  initialTab?: TechTab;
}

interface RepairTicket {
  id: string;
  clientName: string;
  clientPhone: string;
  deviceModel: string;
  issue: string;
  price: string;
  status: 'pending' | 'ready' | 'delivered';
  date: string;
}

// Famous Samsung CSC Codes database for phone unlocking & firmware
const SAMSUNG_CSC_DATABASE = [
  { code: 'KSA', region: 'المملكة العربية السعودية', network: 'مفتوح لجميع الشبكات', volte: 'مدعوم رسمي 4G/5G' },
  { code: 'XSG', region: 'الإمارات العربية المتحدة', network: 'عام للشرق الأوسط', volte: 'مدعوم رسمي' },
  { code: 'EGY', region: 'جمهورية مصر العربية', network: 'جميع الشبكات المصرية', volte: 'مدعوم رسمي' },
  { code: 'MID', region: 'الشرق الأوسط والعراق', network: 'العراق واليمن والمنطقة', volte: 'مدعوم' },
  { code: 'SPR', region: 'الولايات المتحدة (Sprint)', network: 'CDMA / LTE مشهور لتفعيل يمن موبايل', volte: 'يحتاج تعديل ملف Diag' },
  { code: 'BST', region: 'الولايات المتحدة (Boost Mobile)', network: 'كود الانتقال الشهير لسامسونج S21', volte: 'مدعوم' },
  { code: 'VZW', region: 'الولايات المتحدة (Verizon)', network: 'تثبيت التغطية لشبكات CDMA / LTE', volte: 'يعمل بعد ضبط APN' },
  { code: 'TMB', region: 'الولايات المتحدة (T-Mobile)', network: 'أجهزة أمريكا GSM', volte: 'مدعوم' },
  { code: 'ATT', region: 'الولايات المتحدة (AT&T)', network: 'أجهزة AT&T المغلقة', volte: 'يحتاج CSC عام' },
  { code: 'TUR', region: 'تركيا (Turkey)', network: 'مشهور لتعريب الأجهزة القديمة', volte: 'مدعوم' }
];

export const TechUtilsView: React.FC<TechUtilsViewProps> = ({ onCopyToast, initialTab = 'commands' }) => {
  const [activeTab, setActiveTab] = useState<TechTab>(initialTab);

  useEffect(() => {
    if (initialTab) {
      setActiveTab(initialTab);
    }
  }, [initialTab]);
  const [cmdFilter, setCmdFilter] = useState<'all' | 'fastboot' | 'adb'>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [copiedId, setCopiedId] = useState<string | null>(null);

  // Technician Gamification Hook
  const {
    points,
    streak,
    currentRank,
    nextRank,
    claimedAchievements,
    isVipActive,
    vipUntil,
    claimDailyCheckin,
    claimAchievement,
    buyVip,
    addPoints
  } = useTechRank();

  // IMEI Luhn Calculator State
  const [imeiInput, setImeiInput] = useState('');
  const [calculatedChecksum, setCalculatedChecksum] = useState<{
    valid: boolean;
    completeImei: string;
    checkDigit: number;
    error?: string;
  } | null>(null);

  // Shop Repair Tracker state
  const [tickets, setTickets] = useState<RepairTicket[]>(() => {
    try {
      const saved = localStorage.getItem('hmax_repair_tickets_v1');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  const [receiptToPrint, setReceiptToPrint] = useState<ReceiptData | null>(null);
  const [newClient, setNewClient] = useState('');
  const [newPhone, setNewPhone] = useState('');
  const [newModel, setNewModel] = useState('');
  const [newIssue, setNewIssue] = useState('');
  const [newPrice, setNewPrice] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);

  useEffect(() => {
    try {
      localStorage.setItem('hmax_repair_tickets_v1', JSON.stringify(tickets));
    } catch (e) {
      console.error(e);
    }
  }, [tickets]);

  const handleCopy = (id: string, text: string, label: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    onCopyToast(`تم نسخ ${label}: ${text}`);
    addPoints(1); // Give micro reward for interacting
    setTimeout(() => setCopiedId(null), 1800);
  };

  // Luhn Algorithm for IMEI Checksum
  const calculateLuhn = (raw: string) => {
    const clean = raw.replace(/[^0-9]/g, '');
    if (clean.length < 14) {
      setCalculatedChecksum({
        valid: false,
        completeImei: '',
        checkDigit: 0,
        error: 'يرجى إدخال 14 أو 15 رقماً للسيريال'
      });
      return;
    }

    const first14 = clean.slice(0, 14);
    let sum = 0;
    for (let i = 0; i < 14; i++) {
      let digit = parseInt(first14[i], 10);
      if (i % 2 !== 0) {
        digit *= 2;
        if (digit > 9) digit -= 9;
      }
      sum += digit;
    }
    const checkDigit = (10 - (sum % 10)) % 10;
    const complete = first14 + checkDigit;
    const isValid = clean.length === 15 ? parseInt(clean[14], 10) === checkDigit : true;

    setCalculatedChecksum({
      valid: isValid,
      completeImei: complete,
      checkDigit,
      error: undefined
    });
  };

  const handleAddTicket = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newModel.trim() || !newClient.trim()) return;
    const item: RepairTicket = {
      id: `ticket-${Date.now()}`,
      clientName: newClient.trim(),
      clientPhone: newPhone.trim(),
      deviceModel: newModel.trim(),
      issue: newIssue.trim() || 'سوفت وير وفك شفرة',
      price: newPrice.trim() || '—',
      status: 'pending',
      date: new Date().toLocaleDateString('ar-EG', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    };
    setTickets([item, ...tickets]);
    setNewClient('');
    setNewPhone('');
    setNewModel('');
    setNewIssue('');
    setNewPrice('');
    setShowAddModal(false);
    addPoints(5);
    onCopyToast('تم تسجيل بطاقة صيانة الجهاز (+5 نقاط)');
  };

  const handleDeleteTicket = (id: string) => {
    setTickets(tickets.filter((t) => t.id !== id));
    onCopyToast('تم حذف بطاقة الصيانة');
  };

  const handleUpdateStatus = (id: string, status: 'pending' | 'ready' | 'delivered') => {
    setTickets(tickets.map((t) => (t.id === id ? { ...t, status } : t)));
    onCopyToast('تم تحديث حالة الجهاز');
  };

  const handleSendWhatsApp = (t: RepairTicket) => {
    const msg = `مرحباً أخي ${t.clientName}، نفيدك بأن جهازك (${t.deviceModel}) في مركز الصيانة تم الانتهاء من صيانته وبرمجته وهو الآن جاهز للاستلام. التكلفة: ${t.price} — شكراً لثقتكم بنا!`;
    const cleanPhone = t.clientPhone.replace(/[^0-9]/g, '');
    const url = cleanPhone
      ? `https://wa.me/${cleanPhone}?text=${encodeURIComponent(msg)}`
      : `https://wa.me/?text=${encodeURIComponent(msg)}`;
    window.open(url, '_blank');
  };

  // Filters
  const filteredCommands = useMemo(() => {
    return ADB_FASTBOOT_COMMANDS.filter((cmd) => {
      const matchCat = cmdFilter === 'all' || cmd.category === cmdFilter;
      const matchSearch =
        cmd.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        cmd.cmd.toLowerCase().includes(searchQuery.toLowerCase()) ||
        cmd.desc.toLowerCase().includes(searchQuery.toLowerCase());
      return matchCat && matchSearch;
    });
  }, [cmdFilter, searchQuery]);

  const filteredCodes = useMemo(() => {
    return SECRET_DIAL_CODES.filter((cd) => {
      return (
        cd.brand.toLowerCase().includes(searchQuery.toLowerCase()) ||
        cd.code.toLowerCase().includes(searchQuery.toLowerCase()) ||
        cd.purpose.toLowerCase().includes(searchQuery.toLowerCase())
      );
    });
  }, [searchQuery]);

  const filteredCarriers = useMemo(() => {
    return IPHONE_CARRIER_CODES.filter((item) => {
      return (
        item.carrier.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.country.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.codes.some((c) => c.includes(searchQuery))
      );
    });
  }, [searchQuery]);

  const filteredLT = useMemo(() => {
    return LT_PHONES_CATALOG.filter((item) => {
      return (
        item.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (item.desc && item.desc.toLowerCase().includes(searchQuery.toLowerCase())) ||
        (item.ver && item.ver.toLowerCase().includes(searchQuery.toLowerCase()))
      );
    });
  }, [searchQuery]);

  const filteredAPN = useMemo(() => {
    return APN_PROFILES.filter((ap) => {
      return (
        ap.carrier.toLowerCase().includes(searchQuery.toLowerCase()) ||
        ap.apn.toLowerCase().includes(searchQuery.toLowerCase()) ||
        ap.country.toLowerCase().includes(searchQuery.toLowerCase())
      );
    });
  }, [searchQuery]);

  const filteredTP = useMemo(() => {
    return TESTPOINT_GUIDES.filter((tp) => {
      return (
        tp.brand.toLowerCase().includes(searchQuery.toLowerCase()) ||
        tp.model.toLowerCase().includes(searchQuery.toLowerCase()) ||
        tp.chipset.toLowerCase().includes(searchQuery.toLowerCase())
      );
    });
  }, [searchQuery]);

  const tabsConfig = [
    { id: 'commands', label: 'أوامر Fastboot & ADB', icon: Terminal, count: ADB_FASTBOOT_COMMANDS.length },
    { id: 'samsung_bin', label: 'محلل حمايات سامسونج', icon: Shield, count: 'Bit Check', badge: 'حصري 🔥' },
    { id: 'script_gen', label: 'مولد سكريبتات التفليش', icon: Play, count: 'Auto Bat', badge: 'جديد' },
    { id: 'flash_errors', label: 'قاموس أخطاء التفليش', icon: AlertOctagon, count: '20+ خطأ', badge: 'حلول' },
    { id: 'webusb', label: 'فاحص منافذ USB والتعريفات', icon: Usb, count: 'WebUSB' },
    { id: 'pricing', label: 'حاسبة تسعير الخدمات', icon: DollarSign, count: 'Profit' },
    { id: 'codes', label: 'أكواد المهندس السرية', icon: Key, count: SECRET_DIAL_CODES.length },
    { id: 'iphone', label: 'شفرات الآيفون & IMSI', icon: Smartphone, count: IPHONE_CARRIER_CODES.length, badge: 'جديد' },
    { id: 'lt_phones', label: 'أنظمة LT مجانية', icon: Layers, count: LT_PHONES_CATALOG.length, badge: 'رسمي' },
    { id: 'ranks', label: 'نقاط ورتب الفنيين', icon: Award, count: `${points}⭐`, badge: currentRank.badge },
    { id: 'calc', label: 'حاسبة السيريال & CSC', icon: Calculator, count: 'Tool' },
    { id: 'apn', label: 'نقاط وصول APN', icon: Radio, count: APN_PROFILES.length },
    { id: 'testpoints', label: 'تيست بوينت EDL/BROM', icon: Cpu, count: TESTPOINT_GUIDES.length },
    { id: 'compatibility', label: 'فاحص توافق الطراز', icon: ShieldCheck, count: 'رقم دقيق', badge: 'تحقق' },
    { id: 'diagnostics', label: 'مساعد التشخيص', icon: BookOpenCheck, count: '3 أعطال', badge: 'دليل' },
    { id: 'device_log', label: 'ملاحظات الأجهزة المحلية', icon: Database, count: 'محلي فقط' },
    { id: 'tracker', label: 'دفتر الصيانة وطباعة الوصل', icon: ClipboardList, count: tickets.length }
  ];

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-slate-900 via-slate-900/90 to-blue-950/40 border border-slate-800 p-5 sm:p-7 shadow-2xl">
        <div className="absolute top-0 right-0 w-80 h-80 bg-[#00b4ff]/10 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#00b4ff]/10 border border-[#00b4ff]/30 text-[#00b4ff] text-xs font-bold mb-2">
              <Sparkles className="w-3.5 h-3.5" />
              <span>مختبر أدوات الفني الاحترافية — HMAX UNLOCKER</span>
            </div>
            <h1 className="text-xl sm:text-2xl font-black text-white flex items-center gap-2">
              <span>الأدوات الميدانية والحاسبات البرمجية</span>
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-2xl">
              تجميعة شاملة لكل ما يحتاجه فني السوفت وير: أوامر فاست بوت، أكواد الشفرات الأمريكية، أنظمة هواتف LT الرسمية، حساب السيريال القانوني، ونظام مكافآت ونقاط الفنيين المعتمد في السيرفر.
            </p>
          </div>

          {/* Technician Profile Card Pill */}
          <div className="flex items-center gap-3 p-3 rounded-2xl bg-slate-950/80 border border-slate-800 shadow-inner">
            <div className="w-11 h-11 rounded-xl bg-gradient-to-tr from-amber-500 to-yellow-300 flex items-center justify-center text-xl shadow-lg">
              {currentRank.badge}
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="text-xs text-slate-400">رتبتك:</span>
                <span className="text-xs font-black text-amber-300">{currentRank.name}</span>
                {isVipActive && (
                  <span className="px-1.5 py-0.5 rounded text-[10px] bg-yellow-400/20 text-yellow-300 border border-yellow-400/30 font-bold">
                    VIP
                  </span>
                )}
              </div>
              <div className="flex items-center gap-2 mt-0.5">
                <span className="text-base font-black text-white font-mono">{points}</span>
                <span className="text-[11px] text-slate-400">نقطة</span>
                <span className="text-slate-600">•</span>
                <span className="text-xs text-orange-400 font-bold flex items-center gap-0.5">
                  <Flame className="w-3.5 h-3.5" /> {streak} يوم
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Responsive sub-tabs grid: all technician categories stay visible */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2 mt-6 pt-4 border-t border-slate-800/80">
          {tabsConfig.map((t) => {
            const Icon = t.icon;
            const isActive = activeTab === t.id;
            return (
              <button
                key={t.id}
                onClick={() => {
                  setActiveTab(t.id as TechTab);
                  setSearchQuery('');
                }}
                className={`min-h-12 min-w-0 flex flex-wrap items-center justify-center gap-x-1.5 gap-y-1 px-2 py-2 rounded-xl text-[11px] sm:text-xs text-center leading-tight font-bold transition ${
                  isActive
                    ? 'bg-[#00b4ff] text-black shadow-[0_0_20px_rgba(0,180,255,0.4)]'
                    : 'bg-slate-900/80 text-slate-400 hover:text-white hover:bg-slate-800 border border-slate-800'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{t.label}</span>
                {t.badge ? (
                  <span
                    className={`px-1.5 py-0.2 rounded-full text-[10px] font-black ${
                      isActive ? 'bg-black text-white' : 'bg-[#00b4ff]/20 text-[#00b4ff]'
                    }`}
                  >
                    {t.badge}
                  </span>
                ) : (
                  <span
                    className={`px-1.5 py-0.2 rounded-full text-[10px] ${
                      isActive ? 'bg-black/20 text-black' : 'bg-slate-800 text-slate-400'
                    }`}
                  >
                    {t.count}
                  </span>
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* Global Search Bar within the selected tool tab */}
      {activeTab !== 'ranks' && activeTab !== 'calc' && activeTab !== 'tracker' && activeTab !== 'compatibility' && activeTab !== 'diagnostics' && activeTab !== 'device_log' && (
        <div className="relative">
          <Search className="w-4 h-4 absolute right-4 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder={`بحث في ${tabsConfig.find((x) => x.id === activeTab)?.label}...`}
            className="w-full pl-4 pr-11 py-3 rounded-2xl bg-slate-900/90 border border-slate-800 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-[#00b4ff] transition shadow-inner"
          />
        </div>
      )}

      {/* ======================= TAB 1: ADB & FASTBOOT COMMANDS ======================= */}
      {activeTab === 'commands' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between flex-wrap gap-2">
            <div className="flex items-center gap-1.5 p-1 rounded-xl bg-slate-900 border border-slate-800">
              {(['all', 'fastboot', 'adb'] as const).map((cat) => (
                <button
                  key={cat}
                  onClick={() => setCmdFilter(cat)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold transition ${
                    cmdFilter === cat ? 'bg-[#00b4ff] text-black' : 'text-slate-400 hover:text-white'
                  }`}
                >
                  {cat === 'all' ? 'جميع الأوامر' : cat.toUpperCase()}
                </button>
              ))}
            </div>
            <span className="text-xs text-slate-400">
              تم العثور على <strong className="text-white">{filteredCommands.length}</strong> أمر
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {filteredCommands.map((item) => {
              const isCopied = copiedId === item.id;
              return (
                <div
                  key={item.id}
                  className="rounded-2xl bg-slate-900/70 border border-slate-800 p-4 hover:border-slate-700 transition flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center justify-between gap-2 mb-2">
                      <span className="px-2 py-0.5 rounded-md text-[10px] font-black uppercase tracking-wider bg-slate-800 text-[#00b4ff] border border-slate-700">
                        {item.category}
                      </span>
                      <span
                        className={`text-[10px] px-2 py-0.5 rounded-full font-bold ${
                          item.risk === 'high'
                            ? 'bg-red-500/10 text-red-400 border border-red-500/30'
                            : item.risk === 'medium'
                            ? 'bg-amber-500/10 text-amber-400 border border-amber-500/30'
                            : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                        }`}
                      >
                        {item.risk === 'high' ? '⚠️ تحذير: يمسح البيانات' : item.risk === 'medium' ? 'متقدم' : 'آمن'}
                      </span>
                    </div>

                    <h3 className="text-sm font-bold text-white mb-1.5">{item.name}</h3>
                    <p className="text-xs text-slate-400 leading-relaxed mb-3">{item.desc}</p>
                  </div>

                  <div className="mt-2 pt-2 border-t border-slate-800/80">
                    <div className="flex items-center justify-between gap-2 p-2.5 rounded-xl bg-slate-950 font-mono text-xs text-emerald-400 border border-slate-800/60 overflow-x-auto">
                      <span className="select-all whitespace-nowrap">{item.cmd}</span>
                      <button
                        onClick={() => handleCopy(item.id, item.cmd, 'الأمر')}
                        className={`p-1.5 rounded-lg transition shrink-0 ${
                          isCopied ? 'bg-emerald-500 text-black' : 'bg-slate-800 text-slate-300 hover:text-white'
                        }`}
                        title="نسخ الأمر"
                      >
                        {isCopied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {activeTab === 'compatibility' && <TechnicianDesk mode="compatibility" onCopyToast={onCopyToast} />}
      {activeTab === 'diagnostics' && <TechnicianDesk mode="diagnostics" onCopyToast={onCopyToast} />}
      {activeTab === 'device_log' && <TechnicianDesk mode="device_log" onCopyToast={onCopyToast} />}

      {/* ======================= TAB: SAMSUNG BINARY / BIT CHECKER ======================= */}
      {activeTab === 'samsung_bin' && (
        <SamsungBinaryChecker onCopyToast={onCopyToast} />
      )}

      {/* ======================= TAB: FLASH SCRIPT GENERATOR ======================= */}
      {activeTab === 'script_gen' && (
        <FlashScriptGenerator onCopyToast={onCopyToast} />
      )}

      {/* ======================= TAB: FLASH ERROR DICTIONARY ======================= */}
      {activeTab === 'flash_errors' && (
        <FlashErrorDictionary onCopyToast={onCopyToast} />
      )}

      {/* ======================= TAB: WEBUSB PORT CHECKER ======================= */}
      {activeTab === 'webusb' && (
        <WebUsbPortChecker onCopyToast={onCopyToast} />
      )}

      {/* ======================= TAB: GSM PRICING CALCULATOR ======================= */}
      {activeTab === 'pricing' && (
        <GsmPricingCalculator onCopyToast={onCopyToast} />
      )}

      {/* ======================= TAB 2: SECRET DIAL CODES ======================= */}
      {activeTab === 'codes' && (
        <div className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5">
            {filteredCodes.map((cd) => {
              const isCopied = copiedId === cd.id;
              return (
                <div
                  key={cd.id}
                  className="rounded-2xl bg-slate-900/70 border border-slate-800 p-4 hover:border-slate-700 transition flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="px-2 py-0.5 rounded-md text-[11px] font-bold bg-blue-500/10 text-blue-400 border border-blue-500/20">
                        {cd.brand}
                      </span>
                    </div>
                    <h4 className="text-xs font-bold text-slate-200 mb-1">{cd.purpose}</h4>
                    {cd.notes && <p className="text-[11px] text-slate-400">{cd.notes}</p>}
                  </div>

                  <div className="mt-3 pt-2 border-t border-slate-800 flex items-center justify-between">
                    <span className="font-mono text-base font-black text-amber-400 select-all tracking-wider">
                      {cd.code}
                    </span>
                    <button
                      onClick={() => handleCopy(cd.id, cd.code, 'كود الاتصال')}
                      className={`flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-xs font-bold transition ${
                        isCopied ? 'bg-emerald-500 text-black' : 'bg-slate-800 text-slate-300 hover:text-white'
                      }`}
                    >
                      {isCopied ? <Check className="w-3 h-3" /> : <Copy className="w-3 h-3" />}
                      <span>{isCopied ? 'تم النسخ' : 'نسخ'}</span>
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* ======================= TAB 3: IPHONE CARRIER CODES & ICLOUD ======================= */}
      {activeTab === 'iphone' && (
        <div className="space-y-6">
          {/* Quick Notice Banner */}
          <div className="p-4 rounded-2xl bg-gradient-to-r from-blue-900/30 to-purple-900/30 border border-blue-500/30 flex items-start gap-3">
            <Info className="w-5 h-5 text-blue-400 shrink-0 mt-0.5" />
            <div className="text-xs leading-relaxed text-slate-300">
              <strong className="text-white block mb-0.5">📟 أكواد ومراجع فتح شفرة الآيفون والشرائح الإلكترونية</strong>
              هذه الأكواد خاصة ببرمجة شرائح التيربو سيم وتجاوز قفل الشبكات الأمريكية (AT&T, Verizon, Sprint, Cricket) بالإضافة إلى ملفات ثبات التغطية الإلكترونية وأسعار فتح الآيكلود الرسمي المعتمدة في بوت هيثم ماكس.
            </div>
          </div>

          {/* Electronic SIM & PDF Guides Downloads */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3.5">
            <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col justify-between">
              <div>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  شريحة إلكترونية رقم 1
                </span>
                <h4 className="text-sm font-bold text-white mt-2 mb-1">{IPHONE_METHOD_RESOURCES.esimMethod1.title}</h4>
                <p className="text-xs text-slate-400 leading-relaxed mb-3">
                  {IPHONE_METHOD_RESOURCES.esimMethod1.desc}
                </p>
              </div>
              <a
                href={IPHONE_METHOD_RESOURCES.esimMethod1.url}
                target="_blank"
                rel="noreferrer"
                className="w-full py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-black font-bold text-xs flex items-center justify-center gap-1.5 transition"
              >
                <Download className="w-3.5 h-3.5" />
                <span>تحميل ملف الطريقة 1 (MediaFire)</span>
              </a>
            </div>

            <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col justify-between">
              <div>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">
                  شريحة إلكترونية رقم 2
                </span>
                <h4 className="text-sm font-bold text-white mt-2 mb-1">{IPHONE_METHOD_RESOURCES.esimMethod2.title}</h4>
                <p className="text-xs text-slate-400 leading-relaxed mb-3">
                  {IPHONE_METHOD_RESOURCES.esimMethod2.desc}
                </p>
              </div>
              <a
                href={IPHONE_METHOD_RESOURCES.esimMethod2.url}
                target="_blank"
                rel="noreferrer"
                className="w-full py-2 rounded-xl bg-blue-500 hover:bg-blue-400 text-black font-bold text-xs flex items-center justify-center gap-1.5 transition"
              >
                <Download className="w-3.5 h-3.5" />
                <span>تحميل ملف الطريقة 2 (MediaFire)</span>
              </a>
            </div>

            <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col justify-between">
              <div>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20">
                  كتيب الأكواد PDF
                </span>
                <h4 className="text-sm font-bold text-white mt-2 mb-1">{IPHONE_METHOD_RESOURCES.iccidPdf.title}</h4>
                <p className="text-xs text-slate-400 leading-relaxed mb-3">
                  {IPHONE_METHOD_RESOURCES.iccidPdf.desc}
                </p>
              </div>
              <a
                href={IPHONE_METHOD_RESOURCES.iccidPdf.url}
                target="_blank"
                rel="noreferrer"
                className="w-full py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-black font-bold text-xs flex items-center justify-center gap-1.5 transition"
              >
                <Download className="w-3.5 h-3.5" />
                <span>تحميل كتيب الـ ICCID (PDF)</span>
              </a>
            </div>
          </div>

          {/* Carrier IMSI Codes Grid */}
          <div className="space-y-3">
            <h3 className="text-sm font-black text-white flex items-center gap-2">
              <Radio className="w-4 h-4 text-[#00b4ff]" />
              <span>أكواد مشغلي الشبكات IMSI Carrier Codes</span>
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {filteredCarriers.map((item, idx) => (
                <div key={idx} className="p-4 rounded-2xl bg-slate-900/70 border border-slate-800 hover:border-slate-700 transition">
                  <div className="flex items-center justify-between mb-1.5">
                    <h4 className="text-sm font-bold text-white">{item.carrier}</h4>
                    <span className="text-[11px] text-slate-400">{item.country}</span>
                  </div>
                  {item.notes && <p className="text-[11px] text-slate-400 mb-2.5">{item.notes}</p>}

                  <div className="flex flex-wrap gap-1.5">
                    {item.codes.map((code) => {
                      const isCopied = copiedId === `${item.carrier}-${code}`;
                      return (
                        <button
                          key={code}
                          onClick={() => handleCopy(`${item.carrier}-${code}`, code, `كود ${item.carrier}`)}
                          className={`px-2.5 py-1 rounded-lg font-mono text-xs font-bold transition flex items-center gap-1 ${
                            isCopied
                              ? 'bg-emerald-500 text-black'
                              : 'bg-slate-950 text-[#00b4ff] hover:bg-slate-800 border border-slate-800'
                          }`}
                        >
                          <span>{code}</span>
                          {isCopied ? <Check className="w-2.5 h-2.5" /> : <Copy className="w-2.5 h-2.5 opacity-60" />}
                        </button>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Official iCloud Unlock Price List Table */}
          <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-3">
            <div className="flex items-center justify-between flex-wrap gap-2">
              <div>
                <h3 className="text-sm font-black text-white flex items-center gap-2">
                  <Crown className="w-4 h-4 text-amber-400" />
                  <span>قائمة الأسعار الرسمية لفتح الآيكلود Clean (iCloud Unlock Official)</span>
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  فتح دائم رسمي من السيرفر — مدة التنفيذ: 20 إلى 30 يوماً
                </p>
              </div>
              <a
                href="https://t.me/hithamMax"
                target="_blank"
                rel="noreferrer"
                className="px-3 py-1.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-black font-bold text-xs flex items-center gap-1 transition"
              >
                <Send className="w-3.5 h-3.5" />
                <span>طلب التفعيل عبر الإدارة</span>
              </a>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-right text-xs">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400">
                    <th className="py-2.5 px-3">سلسلة الجهاز</th>
                    <th className="py-2.5 px-3">السعر التقديري</th>
                    <th className="py-2.5 px-3">الوقت المتوقع</th>
                    <th className="py-2.5 px-3">حالة السيرفر</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 font-medium">
                  {ICLOUD_OFFICIAL_PRICES.map((row, idx) => (
                    <tr key={idx} className="hover:bg-slate-800/30 transition">
                      <td className="py-2.5 px-3 font-bold text-white">{row.series}</td>
                      <td className="py-2.5 px-3 font-black text-amber-400 font-mono text-sm">{row.price}</td>
                      <td className="py-2.5 px-3 text-slate-300">{row.duration}</td>
                      <td className="py-2.5 px-3 text-emerald-400 font-bold">{row.note}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* ======================= TAB 4: FREE LT PHONES OFFICIAL SYSTEMS ======================= */}
      {activeTab === 'lt_phones' && (
        <div className="space-y-4">
          <div className="p-4 rounded-2xl bg-emerald-950/20 border border-emerald-500/30 flex items-start justify-between flex-wrap gap-3">
            <div className="flex items-start gap-3">
              <Layers className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
              <div>
                <strong className="text-white block text-sm mb-0.5">📂 مكتبة أنظمة ورومات هواتف LT الرسمية المجانية</strong>
                <p className="text-xs text-slate-300">
                  فلاشات خام أصلية ومجانية بالكامل لعلاج موت الهاتف وتخطي التوقف على الشعار وحل مشاكل شبكة يمن موبايل. كلمة سر فك الضغط لجميع الملفات: <code className="text-amber-300 font-mono font-bold">{MASTER_PASS}</code>
                </p>
              </div>
            </div>
            <button
              onClick={() => handleCopy('lt-pass', MASTER_PASS, 'كلمة السر')}
              className="px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-700 text-xs font-bold text-amber-300 hover:text-white flex items-center gap-1.5 transition"
            >
              <Copy className="w-3.5 h-3.5" />
              <span>نسخ كلمة السر</span>
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5">
            {filteredLT.map((item) => (
              <div
                key={item.id}
                className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 hover:border-slate-700 transition flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="px-2 py-0.5 rounded text-[10px] font-black bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                      {item.ver}
                    </span>
                    <span className="text-[10px] text-slate-400 font-mono">Google Drive</span>
                  </div>
                  <h4 className="text-sm font-bold text-white mb-1.5">{item.name}</h4>
                  <p className="text-xs text-slate-400 leading-relaxed mb-3">{item.desc}</p>
                </div>

                <div className="pt-2 border-t border-slate-800 flex items-center justify-between gap-2">
                  <a
                    href={item.link}
                    target="_blank"
                    rel="noreferrer"
                    className="flex-1 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-black font-bold text-xs flex items-center justify-center gap-1.5 transition shadow-md"
                  >
                    <Download className="w-3.5 h-3.5" />
                    <span>تحميل الفلاشة</span>
                  </a>
                  <button
                    onClick={() => handleCopy(`pass-${item.id}`, MASTER_PASS, 'كلمة السر')}
                    className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
                    title="نسخ باسورد الملف"
                  >
                    <Key className="w-3.5 h-3.5 text-amber-300" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ======================= TAB 5: TECHNICIAN RANKS & VIP STORE ======================= */}
      {activeTab === 'ranks' && (
        <div className="space-y-6">
          {/* Main Status & Daily Checkin Card */}
          <div className="p-6 rounded-3xl bg-gradient-to-br from-slate-900 via-slate-900 to-indigo-950/60 border border-slate-800 relative overflow-hidden">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-5 relative z-10">
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-amber-400 to-yellow-600 flex items-center justify-center text-3xl shadow-2xl">
                  {currentRank.badge}
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <h2 className="text-xl font-black text-white">{currentRank.name}</h2>
                    <span className="text-xs text-slate-400 font-mono">({currentRank.nameEn})</span>
                    {isVipActive && (
                      <span className="px-2 py-0.5 rounded-full text-xs bg-yellow-400 text-black font-black">
                        VIP Active
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-slate-400 mt-1">
                    رصيدك الحالي: <strong className="text-amber-400 text-sm font-mono">{points}</strong> نقطة خبرة • سلسلة التفاعل: <strong className="text-orange-400">{streak}</strong> أيام متصلة
                  </p>
                </div>
              </div>

              {/* Daily Check-in Button */}
              <button
                onClick={() => {
                  const res = claimDailyCheckin();
                  onCopyToast(res.message);
                }}
                className="px-5 py-3 rounded-2xl bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-400 hover:to-amber-400 text-black font-black text-sm flex items-center justify-center gap-2 transition shadow-xl shrink-0"
              >
                <Flame className="w-4 h-4 fill-black" />
                <span>تسجيل الحضور اليومي (+10 نقاط)</span>
              </button>
            </div>

            {/* Progress to next rank */}
            {nextRank && (
              <div className="mt-6 pt-4 border-t border-slate-800">
                <div className="flex items-center justify-between text-xs mb-1.5">
                  <span className="text-slate-400">
                    الترقية التالية: <strong className="text-white">{nextRank.name}</strong> ({nextRank.threshold} نقطة)
                  </span>
                  <span className="text-amber-300 font-mono font-bold">
                    متبقي {Math.max(0, nextRank.threshold - points)} نقطة
                  </span>
                </div>
                <div className="w-full h-2.5 rounded-full bg-slate-950 overflow-hidden border border-slate-800">
                  <div
                    className="h-full bg-gradient-to-r from-[#00b4ff] to-emerald-400 transition-all duration-500"
                    style={{
                      width: `${Math.min(100, Math.round((points / nextRank.threshold) * 100))}%`
                    }}
                  />
                </div>
              </div>
            )}
          </div>

          {/* VIP Perks & Store (from hmax_pro.py) */}
          <div className="space-y-3">
            <h3 className="text-sm font-black text-white flex items-center gap-2">
              <Crown className="w-4 h-4 text-yellow-400" />
              <span>متجر نقاط HMAX VIP — استبدل نقاطك بعروض حقيقية</span>
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-yellow-400/20 text-yellow-300 border border-yellow-400/30">
                      باقة 7 أيام
                    </span>
                    <span className="text-sm font-black text-amber-400 font-mono">250 نقطة</span>
                  </div>
                  <h4 className="text-base font-bold text-white mb-1">👑 اشتراك VIP ملكي أسبوعي</h4>
                  <p className="text-xs text-slate-400 leading-relaxed mb-3">
                    أولوية قصوى في طلبات الفلاشات الحصرية، تخطي حدود السرعة، وتفعيل الشارة الملكية في حسابك.
                  </p>
                </div>
                <button
                  onClick={() => {
                    const res = buyVip(7, 250);
                    onCopyToast(res.message);
                  }}
                  className="w-full py-2.5 rounded-xl bg-gradient-to-r from-amber-500 to-yellow-400 hover:from-amber-400 hover:to-yellow-300 text-black font-black text-xs transition"
                >
                  استبدال بـ 250 نقطة
                </button>
              </div>

              <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-yellow-400/20 text-yellow-300 border border-yellow-400/30">
                      باقة 30 يوماً
                    </span>
                    <span className="text-sm font-black text-amber-400 font-mono">800 نقطة</span>
                  </div>
                  <h4 className="text-base font-bold text-white mb-1">👑 اشتراك VIP ملكي شهري</h4>
                  <p className="text-xs text-slate-400 leading-relaxed mb-3">
                    عضوية كاملة لمدة شهر كامل مع وصول مباشر لملفات سيرفر حلب تك وسبورت VIP بدون أي انتظار.
                  </p>
                </div>
                <button
                  onClick={() => {
                    const res = buyVip(30, 800);
                    onCopyToast(res.message);
                  }}
                  className="w-full py-2.5 rounded-xl bg-gradient-to-r from-amber-500 to-yellow-400 hover:from-amber-400 hover:to-yellow-300 text-black font-black text-xs transition"
                >
                  استبدال بـ 800 نقطة
                </button>
              </div>
            </div>
          </div>

          {/* Achievements List */}
          <div className="space-y-3">
            <h3 className="text-sm font-black text-white flex items-center gap-2">
              <Gift className="w-4 h-4 text-emerald-400" />
              <span>إنجازات ومكافآت المهندس (Achievements)</span>
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {ACHIEVEMENTS_LIST.map((ach) => {
                const isClaimed = claimedAchievements.includes(ach.id);
                const currentVal = ach.type === 'points' ? points : streak;
                const canClaim = !isClaimed && currentVal >= ach.target;

                return (
                  <div
                    key={ach.id}
                    className={`p-3.5 rounded-2xl border transition flex flex-col justify-between ${
                      isClaimed
                        ? 'bg-slate-950/60 border-emerald-900/40 opacity-75'
                        : canClaim
                        ? 'bg-emerald-950/30 border-emerald-500/50 shadow-[0_0_15px_rgba(16,185,129,0.15)]'
                        : 'bg-slate-900/60 border-slate-800'
                    }`}
                  >
                    <div>
                      <div className="flex items-center justify-between mb-1">
                        <h4 className="text-xs font-bold text-white">{ach.title}</h4>
                        <span className="text-[11px] font-black text-amber-400 font-mono">+{ach.reward} pt</span>
                      </div>
                      <p className="text-[11px] text-slate-400 leading-relaxed mb-2.5">{ach.desc}</p>
                    </div>

                    <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between">
                      <span className="text-[10px] text-slate-400 font-mono">
                        {currentVal} / {ach.target}
                      </span>
                      {isClaimed ? (
                        <span className="text-[11px] font-bold text-emerald-400 flex items-center gap-1">
                          <Check className="w-3 h-3" /> تم الاستلام
                        </span>
                      ) : (
                        <button
                          disabled={!canClaim}
                          onClick={() => {
                            const res = claimAchievement(ach.id);
                            onCopyToast(res.message);
                          }}
                          className={`px-3 py-1 rounded-lg text-xs font-bold transition ${
                            canClaim
                              ? 'bg-emerald-500 text-black hover:bg-emerald-400 shadow-md cursor-pointer'
                              : 'bg-slate-800 text-slate-500 cursor-not-allowed'
                          }`}
                        >
                          استلام الجائزة
                        </button>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* ======================= TAB 6: CALCULATOR & CSC FINDER ======================= */}
      {activeTab === 'calc' && (
        <div className="space-y-6">
          {/* Luhn Algorithm IMEI Calculator */}
          <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-4">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold mb-1.5">
                <Calculator className="w-3.5 h-3.5" />
                <span>حاسبة وفاحص صحة السيريال (IMEI Luhn Checksum)</span>
              </div>
              <h3 className="text-base font-bold text-white">
                توليد وفحص الرقم الأخير للرقم التسلسلي القانوني (Check Digit 15)
              </h3>
              <p className="text-xs text-slate-400 mt-1">
                تستخدم خوارزمية Luhn لحساب الخانة رقم 15 للسيريال لضمان قبوله في أجهزة سامسونج وشاومي ومودمات يمن موبايل ومنع مشكلة (Invalid IMEI).
              </p>
            </div>

            <div className="flex flex-col sm:flex-row gap-3">
              <input
                type="text"
                maxLength={15}
                value={imeiInput}
                onChange={(e) => {
                  setImeiInput(e.target.value);
                  calculateLuhn(e.target.value);
                }}
                placeholder="أدخل أول 14 أو 15 رقماً من السيريال..."
                className="flex-1 px-4 py-3 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white font-mono placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition"
              />
              <button
                onClick={() => calculateLuhn(imeiInput)}
                className="px-5 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-black font-bold text-xs transition"
              >
                فحص الخوارزمية
              </button>
            </div>

            {calculatedChecksum && (
              <div
                className={`p-4 rounded-xl border ${
                  calculatedChecksum.error
                    ? 'bg-red-500/10 border-red-500/30 text-red-400'
                    : calculatedChecksum.valid
                    ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
                    : 'bg-amber-500/10 border-amber-500/30 text-amber-300'
                }`}
              >
                {calculatedChecksum.error ? (
                  <p className="text-xs font-bold">{calculatedChecksum.error}</p>
                ) : (
                  <div className="space-y-1.5 text-xs">
                    <div className="flex items-center justify-between flex-wrap gap-2">
                      <span className="font-bold">
                        {calculatedChecksum.valid
                          ? '✅ السيريال صحيح ومطابق لمواصفات GSMA و Luhn 100%'
                          : '⚠️ تنبيه: الرقم الأخير غير متطابق مع خانة التحقق!'}
                      </span>
                      <button
                        onClick={() => handleCopy('calc-imei', calculatedChecksum.completeImei, 'السيريال المكتمل')}
                        className="px-2.5 py-1 rounded bg-slate-900 border border-slate-700 text-xs font-bold text-white hover:bg-slate-800 flex items-center gap-1 transition"
                      >
                        <Copy className="w-3 h-3" />
                        <span>نسخ السيريال الكامل</span>
                      </button>
                    </div>
                    <div className="font-mono text-base font-black text-white mt-1">
                      {calculatedChecksum.completeImei.slice(0, 14)}
                      <span className="text-amber-400 underline font-black">
                        {calculatedChecksum.completeImei.slice(14)}
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-400">
                      رقم التحقق المحسوب (Check Digit): <strong className="text-white">{calculatedChecksum.checkDigit}</strong>
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Samsung CSC Database Finder */}
          <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-3">
            <div>
              <h3 className="text-sm font-black text-white flex items-center gap-2">
                <Radio className="w-4 h-4 text-[#00b4ff]" />
                <span>دليل أكواد المناطق والشبكات لسامسونج (Samsung CSC Lookup)</span>
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">
                أشهر رموز الموجه والشبكات لتغيير الـ CSC عبر أداة SamFW لتفعيل VoLTE ويمن موبايل والتخلص من التطبيقات المغلقة.
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {SAMSUNG_CSC_DATABASE.map((item) => {
                const isCopied = copiedId === `csc-${item.code}`;
                return (
                  <div
                    key={item.code}
                    className="p-3.5 rounded-xl bg-slate-950 border border-slate-800 hover:border-slate-700 transition flex items-center justify-between gap-3"
                  >
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-mono text-base font-black text-amber-400">{item.code}</span>
                        <span className="text-xs font-bold text-white">{item.region}</span>
                      </div>
                      <p className="text-[11px] text-slate-400 mt-0.5">{item.network}</p>
                      <span className="text-[10px] text-emerald-400 font-bold block mt-1">{item.volte}</span>
                    </div>
                    <button
                      onClick={() => handleCopy(`csc-${item.code}`, item.code, `كود CSC (${item.code})`)}
                      className={`p-2 rounded-lg transition shrink-0 ${
                        isCopied ? 'bg-emerald-500 text-black' : 'bg-slate-800 text-slate-300 hover:text-white'
                      }`}
                    >
                      {isCopied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
                    </button>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* ======================= TAB 7: APN PROFILES ======================= */}
      {activeTab === 'apn' && (
        <div className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5">
            {filteredAPN.map((item) => (
              <div
                key={item.id}
                className="p-4 rounded-2xl bg-slate-900/70 border border-slate-800 flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-[11px] font-bold text-emerald-400">{item.country}</span>
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-slate-800 text-slate-400">
                      MCC: {item.mcc} | MNC: {item.mnc}
                    </span>
                  </div>
                  <h4 className="text-sm font-bold text-white mb-2">{item.carrier}</h4>

                  <div className="space-y-1.5 text-xs font-mono bg-slate-950 p-3 rounded-xl border border-slate-800/80 mb-3">
                    <div className="flex justify-between">
                      <span className="text-slate-500">APN:</span>
                      <span className="text-[#00b4ff] font-bold select-all">{item.apn}</span>
                    </div>
                    {item.user && (
                      <div className="flex justify-between">
                        <span className="text-slate-500">User:</span>
                        <span className="text-slate-300 select-all">{item.user}</span>
                      </div>
                    )}
                    {item.pass && (
                      <div className="flex justify-between">
                        <span className="text-slate-500">Password:</span>
                        <span className="text-slate-300 select-all">{item.pass}</span>
                      </div>
                    )}
                  </div>
                </div>

                <button
                  onClick={() => handleCopy(item.id, item.apn, `APN ${item.carrier}`)}
                  className="w-full py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold transition flex items-center justify-center gap-1.5"
                >
                  <Copy className="w-3.5 h-3.5" />
                  <span>نسخ اسم نقطة الوصول APN</span>
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ======================= TAB 8: TESTPOINTS EDL & BROM ======================= */}
      {activeTab === 'testpoints' && (
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {filteredTP.map((tp) => (
              <div key={tp.id} className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-400">{tp.brand}</span>
                  <span
                    className={`px-2.5 py-0.5 rounded-full text-[11px] font-black ${
                      tp.mode === 'EDL 9008'
                        ? 'bg-amber-500/10 text-amber-400 border border-amber-500/30'
                        : 'bg-purple-500/10 text-purple-400 border border-purple-500/30'
                    }`}
                  >
                    {tp.mode}
                  </span>
                </div>

                <div>
                  <h4 className="text-sm font-black text-white">{tp.model}</h4>
                  <span className="text-xs text-cyan-400 font-mono">{tp.chipset}</span>
                </div>

                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800/80 space-y-2 text-xs">
                  <div>
                    <span className="text-slate-400 font-bold block mb-0.5">طريقة التوصيل:</span>
                    <p className="text-slate-300 leading-relaxed">{tp.instructions}</p>
                  </div>
                  <div>
                    <span className="text-slate-400 font-bold block mb-0.5">مكان النقطة (TP Location):</span>
                    <p className="text-amber-300/90 leading-relaxed">{tp.tpPoint}</p>
                  </div>
                </div>

                <p className="text-[11px] text-slate-400 italic">💡 {tp.pinoutNotes}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ======================= TAB 9: WORKSHOP REPAIR TICKETS ======================= */}
      {activeTab === 'tracker' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between flex-wrap gap-3">
            <div>
              <h3 className="text-sm font-bold text-white">دفتر استلام أجهزة الزبائن في المركز</h3>
              <p className="text-xs text-slate-400 mt-0.5">
                تسجيل ومتابعة أجهزة السوفت وير وإشعار الزبائن فوراً عبر واتساب بضغطة زر واحدة.
              </p>
            </div>
            <button
              onClick={() => setShowAddModal(true)}
              className="px-4 py-2 rounded-xl bg-[#00b4ff] hover:bg-[#0090cc] text-black font-bold text-xs flex items-center gap-1.5 transition shadow-lg"
            >
              <Plus className="w-4 h-4" />
              <span>استلام جهاز جديد</span>
            </button>
          </div>

          {/* Add Ticket Modal */}
          {showAddModal && (
            <div className="p-5 rounded-2xl bg-slate-900 border border-[#00b4ff]/40 shadow-2xl space-y-3">
              <h4 className="text-sm font-black text-white">تسجيل بطاقة استلام هاتف جديد</h4>
              <form onSubmit={handleAddTicket} className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                <div>
                  <label className="text-slate-400 block mb-1">اسم العميل *</label>
                  <input
                    required
                    type="text"
                    value={newClient}
                    onChange={(e) => setNewClient(e.target.value)}
                    placeholder="مثال: محمد العمري"
                    className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-white focus:outline-none focus:border-[#00b4ff]"
                  />
                </div>
                <div>
                  <label className="text-slate-400 block mb-1">رقم واتساب العميل</label>
                  <input
                    type="text"
                    value={newPhone}
                    onChange={(e) => setNewPhone(e.target.value)}
                    placeholder="مثال: 967771234567"
                    className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-white focus:outline-none focus:border-[#00b4ff]"
                  />
                </div>
                <div>
                  <label className="text-slate-400 block mb-1">موديل الهاتف *</label>
                  <input
                    required
                    type="text"
                    value={newModel}
                    onChange={(e) => setNewModel(e.target.value)}
                    placeholder="مثال: Samsung A54 5G أو Tecno KM6"
                    className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-white focus:outline-none focus:border-[#00b4ff]"
                  />
                </div>
                <div>
                  <label className="text-slate-400 block mb-1">التكلفة المتفق عليها</label>
                  <input
                    type="text"
                    value={newPrice}
                    onChange={(e) => setNewPrice(e.target.value)}
                    placeholder="مثال: 3000 ريال أو 15$"
                    className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-white focus:outline-none focus:border-[#00b4ff]"
                  />
                </div>
                <div className="sm:col-span-2">
                  <label className="text-slate-400 block mb-1">العطل والمطلوب برمجته</label>
                  <input
                    type="text"
                    value={newIssue}
                    onChange={(e) => setNewIssue(e.target.value)}
                    placeholder="مثال: تفليش فلاشة إحياء + تخطي FRP حساب جوجل"
                    className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-white focus:outline-none focus:border-[#00b4ff]"
                  />
                </div>
                <div className="sm:col-span-2 flex justify-end gap-2 pt-2">
                  <button
                    type="button"
                    onClick={() => setShowAddModal(false)}
                    className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 font-bold"
                  >
                    إلغاء
                  </button>
                  <button
                    type="submit"
                    className="px-5 py-2 rounded-xl bg-[#00b4ff] text-black font-black"
                  >
                    حفظ البطاقة
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* Tickets List */}
          {tickets.length === 0 ? (
            <div className="p-8 rounded-2xl bg-slate-900/40 border border-dashed border-slate-800 text-center text-slate-400 text-xs">
              لا توجد أجهزة مسجلة حالياً. اضغط على زر "استلام جهاز جديد" لبدء تنظيم عمل المركز.
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
              {tickets.map((t) => (
                <div
                  key={t.id}
                  className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 hover:border-slate-700 transition flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-bold text-white text-sm">{t.deviceModel}</span>
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          t.status === 'delivered'
                            ? 'bg-slate-800 text-slate-400'
                            : t.status === 'ready'
                            ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                            : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                        }`}
                      >
                        {t.status === 'delivered' ? 'تم التسليم' : t.status === 'ready' ? 'جاهز للاستلام' : 'قيد الصيانة'}
                      </span>
                    </div>

                    <p className="text-xs text-slate-300 mb-1">
                      الزبون: <strong>{t.clientName}</strong> {t.clientPhone && <span className="text-slate-500">({t.clientPhone})</span>}
                    </p>
                    <p className="text-xs text-slate-400 mb-2">العطل: {t.issue}</p>
                    <div className="flex items-center justify-between text-xs text-slate-400 pt-2 border-t border-slate-800">
                      <span>التكلفة: <strong className="text-emerald-400 font-mono">{t.price}</strong></span>
                      <span className="text-[10px] text-slate-500">{t.date}</span>
                    </div>
                  </div>

                  <div className="mt-3 pt-2 border-t border-slate-800/80 flex items-center justify-between gap-1.5 flex-wrap">
                    <div className="flex items-center gap-1">
                      <button
                        onClick={() => handleUpdateStatus(t.id, 'ready')}
                        className="px-2.5 py-1 rounded-lg text-[11px] font-bold bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20 transition"
                      >
                        جاهز
                      </button>
                      <button
                        onClick={() => handleUpdateStatus(t.id, 'delivered')}
                        className="px-2.5 py-1 rounded-lg text-[11px] font-bold bg-slate-800 text-slate-300 hover:bg-slate-700 transition"
                      >
                        تم التسليم
                      </button>
                    </div>

                    <div className="flex items-center gap-1">
                      <button
                        onClick={() => setReceiptToPrint({
                          ticketId: t.id,
                          clientName: t.clientName,
                          clientPhone: t.clientPhone,
                          deviceModel: t.deviceModel,
                          issue: t.issue,
                          price: t.price,
                          date: t.date,
                          status: t.status
                        })}
                        className="p-1.5 rounded-lg bg-[#00b4ff]/15 hover:bg-[#00b4ff]/25 text-[#00b4ff] transition"
                        title="معاينة وطباعة الوصل الحراري 80mm"
                      >
                        <Printer className="w-3.5 h-3.5" />
                      </button>
                      <button
                        onClick={() => handleSendWhatsApp(t)}
                        className="p-1.5 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-black transition"
                        title="إشعار الزبون عبر واتساب"
                      >
                        <Send className="w-3.5 h-3.5" />
                      </button>
                      <button
                        onClick={() => handleDeleteTicket(t.id)}
                        className="p-1.5 rounded-lg bg-red-500/10 hover:bg-red-500/20 text-red-400 transition"
                        title="حذف البطاقة"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Customer Receipt Thermal Modal */}
      {receiptToPrint && (
        <CustomerReceiptModal
          receipt={receiptToPrint}
          onClose={() => setReceiptToPrint(null)}
        />
      )}
    </div>
  );
};
