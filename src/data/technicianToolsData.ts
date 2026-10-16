export interface CommandItem {
  id: string;
  name: string;
  category: 'fastboot' | 'adb' | 'edl' | 'dialer';
  cmd: string;
  desc: string;
  params?: { key: string; placeholder: string; defaultVal: string }[];
  risk: 'safe' | 'medium' | 'high';
}

export interface SecretCodeItem {
  id: string;
  brand: string;
  code: string;
  purpose: string;
  notes?: string;
}

export interface APNProfile {
  id: string;
  carrier: string;
  country: string;
  name: string;
  apn: string;
  user?: string;
  pass?: string;
  mcc?: string;
  mnc?: string;
  apnType?: string;
  apnProtocol?: string;
  dialCode?: string;
}

export interface TestPointGuide {
  id: string;
  brand: string;
  model: string;
  chipset: string;
  mode: 'EDL 9008' | 'BROM' | 'TestPoint ISP';
  instructions: string;
  tpPoint: string;
  pinoutNotes: string;
}

export const ADB_FASTBOOT_COMMANDS: CommandItem[] = [
  {
    id: "cmd-1",
    name: "إعادة تشغيل الهاتف لوضع الطوارئ كوالكوم (EDL 9008)",
    category: "adb",
    cmd: "adb reboot edl",
    desc: "لإدخال الهاتف وضع 9008 مباشرة عبر منفذ ADB لتمرير فلاشات الإحياء وتخطي FRP لكوالكوم.",
    risk: "safe"
  },
  {
    id: "cmd-2",
    name: "إعادة تشغيل من فاست بوت إلى EDL 9008",
    category: "fastboot",
    cmd: "fastboot oem edl",
    desc: "أمر فاست بوت لهواتف شاومي وكوالكوم للدخول المباشر لوضع 9008 دون الحاجة لفتح الجهاز أو التيست بوينت.",
    risk: "safe"
  },
  {
    id: "cmd-3",
    name: "فحص كافة بيانات وبوت لودر وحماية الهاتف (Fastboot Getvar)",
    category: "fastboot",
    cmd: "fastboot getvar all",
    desc: "قراءة كاملة لبيانات الجهاز: اسم البورد، حالة قفل البوت لودر، رقم الحماية، وإصدار البيسباند.",
    risk: "safe"
  },
  {
    id: "cmd-4",
    name: "تفعيل منفذ Diag Port لكوالكوم لإصلاح السيريال والشبكة",
    category: "adb",
    cmd: "adb shell setprop sys.usb.config diag,serial_cport,rmnet,adb",
    desc: "أمر فتح بورت التشخيص Diag لكتابة ملفات QCN وتعديل السيريال وتفعيل VoLTE.",
    risk: "medium"
  },
  {
    id: "cmd-5",
    name: "منح صلاحيات تعريب الهاتف لأداة MoreLocale 2 بدون روت",
    category: "adb",
    cmd: "adb shell pm grant jp.co.c_lis.ccl.morelocale android.permission.CHANGE_CONFIGURATION",
    desc: "إعطاء صلاحية تغيير لغة النظام بدون روت لتعريب جميع هواتف سامسونج وإل جي وموتورولا فوراً.",
    risk: "safe"
  },
  {
    id: "cmd-6",
    name: "استخراج كود فك البوت لودر لموتورولا (Unlock Data)",
    category: "fastboot",
    cmd: "fastboot oem get_unlock_data",
    desc: "استخراج الأسطر الخمسة المشفرة لإرسالها لموقع موتورولا الرسمي والحصول على كود الفك.",
    risk: "safe"
  },
  {
    id: "cmd-7",
    name: "فتح البوت لودر الرسمي للأجهزة الحديثة (Fastboot Flashing Unlock)",
    category: "fastboot",
    cmd: "fastboot flashing unlock",
    desc: "أمر فتح البوت لودر القياسي لأندرويد 10 إلى 15 (بيكسل، وان بلس، موتورولا، وتكنو).",
    risk: "high"
  },
  {
    id: "cmd-8",
    name: "الدخول لوضع الفاست بوت المطور (Fastbootd)",
    category: "fastboot",
    cmd: "fastboot reboot fastboot",
    desc: "ضروري لتفليش البارتشنات الديناميكية (Dynamic Partitions: system, vendor, product) في أندرويد 10 فما فوق.",
    risk: "safe"
  },
  {
    id: "cmd-9",
    name: "استدعاء لوحة اتصال سامسونج عبر ADB (Dialer Bypass)",
    category: "adb",
    cmd: "adb shell am start -n com.samsung.android.dialer/.DialerActivity",
    desc: "فتح شاشة الاتصال لتمرير أكواد *#0808# و *#0*# أثناء شاشة قفل FRP أو شاشة KNOX.",
    risk: "safe"
  },
  {
    id: "cmd-10",
    name: "تعطيل حزم التطبيقات المزعجة والبرامج المثبتة مسبقاً (Debloat)",
    category: "adb",
    cmd: "adb shell pm uninstall -k --user 0 com.facebook.katana",
    desc: "حذف أو تعطيل أي تطبيق نظام دون روت لتسريع الهاتف وتوفير البطارية.",
    params: [{ key: "com.facebook.katana", placeholder: "اسم الحزمة (Package Name)", defaultVal: "com.facebook.katana" }],
    risk: "medium"
  }
];

export const SECRET_DIAL_CODES: SecretCodeItem[] = [
  { id: "cd-1", brand: "Samsung", code: "*#0*#", purpose: "قائمة فحص الهاردوير والشاشة وتخطي FRP في SamFW Tool", notes: "يعمل على غالبية إصدارات سامسونج من شاشة الطوارئ" },
  { id: "cd-2", brand: "Samsung", code: "*#0808#", purpose: "قائمة إعدادات USB وتفعيل منافذ DM + ACM + ADB لتخطي KNOX و MDM", notes: "اختر خيار DM+ACM+ADB ثم Reboot" },
  { id: "cd-3", brand: "Xiaomi / Poco", code: "*#*#86583#*#*", purpose: "تعطيل فحص توافق مشغل VoLTE (VoLTE Carrier Check Disabled)", notes: "يكتب في لوحة الاتصال وتظهر رسالة carrier check disabled لتشغيل 4G" },
  { id: "cd-4", brand: "Xiaomi / Poco", code: "*#*#86943#*#*", purpose: "تعطيل فحص توافق مكالمات الواي فاي VoWiFi", notes: "تفعيل خيار مكالمات VoWiFi في قائمة إعدادات الشريحة" },
  { id: "cd-5", brand: "MediaTek (عام)", code: "*#*#3646633#*#*", purpose: "الدخول إلى قائمة المهندس الكاملة (MTK Engineer Mode)", notes: "ضبط الترددات، قوة الإرسال، تفعيل الباندات، وإصلاح السيريال" },
  { id: "cd-6", brand: "Vivo", code: "*#558#", purpose: "دخول قائمة مهندس مصنع هواتف فيفو (Factory Engineer Mode)", notes: "تفعيل وضع Port Mode وتصحيح USB" },
  { id: "cd-7", brand: "Vivo", code: "*#*#4636#*#*", purpose: "معلومات الهاتف والشبكة واختيار نوع الشبكة المفضل (LTE only / NR)", notes: "تثبيت شبكة 4G ومنع الرجوع إلى 3G" },
  { id: "cd-8", brand: "OPPO / Realme", code: "*#899#", purpose: "قائمة فحص المهندس لهواتف أوبو وريلمي (EngineerMode Manual Test)", notes: "قراءة إصدار السوفت وير الدقيق عبر قسم Software Version" },
  { id: "cd-9", brand: "Unisoc / Spreadtrum", code: "*#*#83781#*#*", purpose: "قائمة المهندس لمعالجات سبريدترام SPD Engineering Mode", notes: "ضبط معايرة الشبكة وتخطي الحمايات" },
  { id: "cd-10", brand: "أجهزة الكوبي (Clones)", code: "*#*#136466331#*#*", purpose: "كود رشيد مدغمر للدخول المباشر لقائمة مهندس آيفون الكوبي والأجهزة المقلدة", notes: "حصري لتعديل IMEI وتفعيل VoLTE في أجهزة الكوبي" }
];

export const APN_PROFILES: APNProfile[] = [
  {
    id: "apn-ym-4g",
    carrier: "يمن موبايل 4G LTE",
    country: "اليمن 🇾🇪",
    name: "Yemen Mobile 4G",
    apn: "ymdata",
    user: "yemencode",
    pass: "yemencode",
    mcc: "421",
    mnc: "03",
    apnType: "default,supl,mms",
    apnProtocol: "IPv4/IPv6",
    dialCode: "*#*#86583#*#*"
  },
  {
    id: "apn-ym-cdma",
    carrier: "يمن موبايل 3G CDMA",
    country: "اليمن 🇾🇪",
    name: "YMobile 3G",
    apn: "#777",
    user: "ymobile",
    pass: "ymobile",
    mcc: "421",
    mnc: "03",
    apnType: "default",
    apnProtocol: "IPv4"
  },
  {
    id: "apn-saba-4g",
    carrier: "سبأفون 4G LTE (SabaFon)",
    country: "اليمن 🇾🇪",
    name: "Sabafon 4G",
    apn: "sabafon",
    user: "",
    pass: "",
    mcc: "421",
    mnc: "01",
    apnType: "default,supl",
    apnProtocol: "IPv4/IPv6"
  },
  {
    id: "apn-you-4g",
    carrier: "يو (YOU Telecom 4G)",
    country: "اليمن 🇾🇪",
    name: "YOU 4G",
    apn: "you",
    user: "",
    pass: "",
    mcc: "421",
    mnc: "02",
    apnType: "default,supl",
    apnProtocol: "IPv4/IPv6"
  },
  {
    id: "apn-stc",
    carrier: "STC (السعودية)",
    country: "السعودية 🇸🇦",
    name: "Jawalnet",
    apn: "jawalnet.com.sa",
    mcc: "420",
    mnc: "01",
    apnType: "default,supl",
    apnProtocol: "IPv4/IPv6"
  },
  {
    id: "apn-mobily",
    carrier: "Mobily (موبايلي)",
    country: "السعودية 🇸🇦",
    name: "Mobily Web",
    apn: "web2",
    mcc: "420",
    mnc: "03",
    apnType: "default,supl",
    apnProtocol: "IPv4/IPv6"
  }
];

export const TESTPOINT_GUIDES: TestPointGuide[] = [
  {
    id: "tp-redmi-9a",
    brand: "Xiaomi / Redmi",
    model: "Redmi 9A / 9C (MT6762G)",
    chipset: "MediaTek Helio G25 / G35",
    mode: "BROM",
    instructions: "فصل البطارية، لمس نقطة CLK / KCO0 بالأرضي (GND) بملاقيط دقيقة، ثم توصيل كابل USB لتخطي حماية DA.",
    tpPoint: "النقطة الذهبية بجوار آيسي الفلاش EMMC أسفل الشيلد المعدني",
    pinoutNotes: "يفتح وضع BROM لقراءة وكتابة الدامب عبر Pandora و UnlockTool و SP Flash Tool"
  },
  {
    id: "tp-redmi-note11",
    brand: "Xiaomi / Redmi",
    model: "Redmi Note 11 (Qualcomm SM6225)",
    chipset: "Snapdragon 680",
    mode: "EDL 9008",
    instructions: "فصل فلاتة البطارية، لمس النقطتين الصغيرتين أعلى كونيكتور الشاشة وتوصيل كابل USB.",
    tpPoint: "نقطتان متجاورتان أعلى يمين البوردة بجوار فلاتة الشحن",
    pinoutNotes: "يقرأ منفذ Qualcomm HS-USB QDLoader 9008 في إدارة الأجهزة Device Manager فوراً"
  },
  {
    id: "tp-sam-a03",
    brand: "Samsung",
    model: "Samsung Galaxy A03 / A03 Core (SM-A032F / SM-A035F)",
    chipset: "Unisoc SC9863A / T606",
    mode: "BROM",
    instructions: "فصل البطارية، عمل قفلة بين نقطة التيست بوينت والأرضي وتوصيل الكابل.",
    tpPoint: "نقطة TP مخصصة خلف زر رفع وخفض الصوت بجوار المعالج",
    pinoutNotes: "ضروري لتمرير ملف الدامب وتخطي FRP في حالة عدم استجابة الهاتف للفاست بوت"
  },
  {
    id: "tp-tecno-spark-10",
    brand: "TECNO",
    model: "TECNO SPARK 10 / 10C / 10 Pro",
    chipset: "Unisoc T606 / Helio G88",
    mode: "BROM",
    instructions: "نزع كابل البطارية، ملامسة نقطة الـ BROM GND مع الأرضي لمدة ثانية أثناء توصيل USB.",
    tpPoint: "النقطة الأولى أسفل كونيكتور البطارية مباشرة",
    pinoutNotes: "يتيح سحب دامب كامل عبر Pandora Tool أو UnlockTool دون الحاجة لتفكيك الشيلد بالكامل"
  },
  {
    id: "tp-vivo-y20",
    brand: "Vivo",
    model: "Vivo Y20 / Y20s (Qualcomm)",
    chipset: "Snapdragon 460",
    mode: "EDL 9008",
    instructions: "فصل البطارية، قفلة النقطتين الذهبيتين بجانب فلاتة البصمة وتوصيل الكابل.",
    tpPoint: "نقطتان متوازيتان بجوار آيسي الباور الصغير",
    pinoutNotes: "وضع EDL 9008 لتخطي حساب فيفو VIVO Cloud وقفل الشاشة دون فقدان البيانات"
  }
];
