export interface GsmServiceItem {
  id: string;
  name: string;
  category: 'frp' | 'dead_boot' | 'unlock' | 'icloud' | 'imei' | 'translation' | 'volte';
  defaultCost: number; // Server or tool credit cost in USD or Local currency
  suggestedCustomerPrice: number;
  currency: 'USD' | 'YER' | 'SAR';
  durationMins: number;
  complexity: 'simple' | 'medium' | 'high' | 'expert';
  notes: string;
}

export const GSM_SERVICES_CATALOG: GsmServiceItem[] = [
  {
    id: "srv-frp-samsung",
    name: "تخطي حساب جوجل FRP لسامسونج (حمايات حديثة 2025/2026)",
    category: "frp",
    defaultCost: 0, // Free with MobilEdit/TSM or 2$ server
    suggestedCustomerPrice: 10,
    currency: "USD",
    durationMins: 15,
    complexity: "medium",
    notes: "مجاني عبر ثغرة MobilEdit المتاحة بالموقع، أو 2-3 دولارات عبر سيرفر SamFW."
  },
  {
    id: "srv-frp-xiaomi",
    name: "تخطي FRP وحساب Mi Account شاومي وريدمي",
    category: "frp",
    defaultCost: 2,
    suggestedCustomerPrice: 12,
    currency: "USD",
    durationMins: 20,
    complexity: "medium",
    notes: "يحتاج تفليش ملف تخطي بوضع EDL أو أداة DFT Pro / UnlockTool."
  },
  {
    id: "srv-dead-boot",
    name: "إحياء هاتف ميت (Dead Boot / TestPoint / ISP JTAG)",
    category: "dead_boot",
    defaultCost: 3, // Halabtech or dump download fee
    suggestedCustomerPrice: 25,
    currency: "USD",
    durationMins: 45,
    complexity: "expert",
    notes: "عملية معقدة تشمل فك الجهاز وتوصيل نقاط ISP أو كتابة فلاشة الدامب المسحوبة."
  },
  {
    id: "srv-network-unlock",
    name: "فك شفرة شبكة دولية (Carrier Network Unlock)",
    category: "unlock",
    defaultCost: 5,
    suggestedCustomerPrice: 20,
    currency: "USD",
    durationMins: 30,
    complexity: "medium",
    notes: "تفعيل أجهزة أمريكا (AT&T, Cricket, Sprint) لتعمل على يمن موبايل وسبأفون."
  },
  {
    id: "srv-icloud-clean",
    name: "فتح آيكلود رسمي نظيف Clean (iCloud Removal)",
    category: "icloud",
    defaultCost: 115, // Server price for iPhone 12/13
    suggestedCustomerPrice: 160,
    currency: "USD",
    durationMins: 43200, // 20-30 days
    complexity: "expert",
    notes: "فتح سيرفر رسمي دائم عبر إدارة HMAX مع ضمان استرجاع الرصيد في حال الرفض."
  },
  {
    id: "srv-exynos-kg",
    name: "تخطي حماية KG Locked & MDM المؤسساتية",
    category: "frp",
    defaultCost: 0,
    suggestedCustomerPrice: 18,
    currency: "USD",
    durationMins: 25,
    complexity: "high",
    notes: "باستخدام برنامج MobilEdit + TSM Pro Edition المتوفرة في الموقع مجاناً."
  },
  {
    id: "srv-volte-yemen",
    name: "تفعيل مكالمات VoLTE وخدمة 4G يمن موبايل",
    category: "volte",
    defaultCost: 0,
    suggestedCustomerPrice: 5,
    currency: "USD",
    durationMins: 10,
    complexity: "simple",
    notes: "عبر أوامر Diag Port أو أكواد المهندس السرية أو كود CSC المرفق بالموقع."
  },
  {
    id: "srv-arabic-translation",
    name: "تعريب نظام أندرويد كامل وشامل",
    category: "translation",
    defaultCost: 0,
    suggestedCustomerPrice: 6,
    currency: "USD",
    durationMins: 10,
    complexity: "simple",
    notes: "باستخدام أداة MaxTech Server VIP V2.0 وأمر MoreLocale المتاح في الموقع."
  }
];
