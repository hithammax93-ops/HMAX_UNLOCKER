export interface FlashErrorItem {
  id: string;
  code: string;
  tool: 'SP Flash Tool' | 'Samsung Odin' | 'Qualcomm EDL / QFIL' | 'Unisoc SPD' | 'UnlockTool / Pandora';
  title: string;
  meaning: string;
  causes: string[];
  solutionSteps: string[];
  recommendedToolOrDriver?: string;
  severity: 'fatal' | 'warning' | 'driver';
}

export const FLASH_ERROR_DATABASE: FlashErrorItem[] = [
  {
    id: "err-sp-1",
    code: "0xC0050005 (STATUS_EXT_RAM_EXCEPTION)",
    tool: "SP Flash Tool",
    title: "خطأ استثناء في ذاكرة الرام الخارجية DRAM / EMMC",
    meaning: "فشل أداة SP Flash Tool في تهيئة ذاكرة الوصول العشوائي (DRAM) الداخلية للهاتف قبل بدء التفليش.",
    causes: [
      "ملف الـ DA (Download Agent) غير مطابق لحماية معالج الهاتف.",
      "فلاشة غير متوافقة مع إصدار لوحة البوردة (Board Hardware ID Mismatch).",
      "خلل فني في آيسي الفلاش eMMC أو تلف خطوط التغذية VCC/VCCQ."
    ],
    solutionSteps: [
      "اختر ملف DA مخصص لنوع المعالج (مثال: MTK_AllInOne_DA_v6.bin).",
      "استخدم أداة تجاوز الحماية MTK Auth Bypass قبل توصيل الهاتف.",
      "تأكد من شحن بطارية الهاتف بما لا يقل عن 50% أو فصل فلاتة البطارية.",
      "في حال استمرار الخطأ، يحتاج الهاتف إعادة شبلنة أو فحص هاردوير لذاكرة EMMC/UFS."
    ],
    recommendedToolOrDriver: "أداة MTK Auth Bypass + SP Flash Tool v5.2124",
    severity: "fatal"
  },
  {
    id: "err-sp-2",
    code: "BROM ERROR : S_BROM_DOWNLOAD_DA_FAIL (2004)",
    tool: "SP Flash Tool",
    title: "فشل تحميل ملف DA في وضع BROM",
    meaning: "المعالج رفض تحميل ملف البوت الداخلي بسبب غلق حماية الـ SLA/DAA.",
    causes: [
      "حماية Secure Boot مفعلة في معالجات Helio الحديثة (G25, G85, G99).",
      "استخدام كابل USB تالف أو منفذ كمبيوتر USB 3.0 غير متوافق.",
      "تعريف MTK VCOM غير مثبت بشكل صحيح أو وجود تعارض في برامج التشغيل."
    ],
    solutionSteps: [
      "استخدم منفذ USB 2.0 خلفي مباشر في اللوحة الأم للكمبيوتر.",
      "شغّل أداة MTK Bypass Tool أو AUM لتخطي حماية Auth أولاً.",
      "ثبّت حزمة تعريفات LibUSB Filter Driver على منفذ MediaTek USB Port.",
      "استخدم كابل EDL مخصص أو اعمل قفلة التيست بوينت لفرض وضع BROM."
    ],
    recommendedToolOrDriver: "تعريف LibUSB-Win32 + أداة Android Utility MTK",
    severity: "driver"
  },
  {
    id: "err-odin-1",
    code: "SW REV. CHECK FAIL (Fused X > Binary Y)",
    tool: "Samsung Odin",
    title: "فشل التحقق من رقم الحماية الثنائية لسامسونج",
    meaning: "محاولة تنزيل نظام يحمل رقم بوت لودر (Binary) أقل من الرقم المسجل في حماية الهاتف الحالية.",
    causes: [
      "تنزيل فلاشة أقدم من إصدار الجهاز (محاولة داونجريد ممنوعة).",
      "عدم التحقق من خانة الـ Bit / Binary في اسم الفلاشة قبل الضغط على Start.",
      "محاولة تفليش ملف BOOT أو SBOOT منفرد من حماية قديمة."
    ],
    solutionSteps: [
      "انظر إلى شاشة الهاتف في وضع Download Mode واقرأ سطر (B:X أو SW REV).",
      "نزّل فلاشة سامسونج رسمية تحمل نفس رقم الـ Binary أو أعلى (راجع أداة فاحص حمايات سامسونج في الموقع).",
      "لا تقم بتفليش الفلاشات القديمة نهائياً لأن معالج إكسينوس وكوالكوم يمنع التراجع أمنياً عبر صمامات eFuse."
    ],
    recommendedToolOrDriver: "موقع SamFW لتحميل الفلاشة المطابقة لحماية الجهاز",
    severity: "fatal"
  },
  {
    id: "err-odin-2",
    code: "FAIL! (Auth) / SetupConnection",
    tool: "Samsung Odin",
    title: "فشل المصادقة أو تعليق الاتصال Setup Connection",
    meaning: "أودين لا يستطيع فتح قناة اتصال مشفرة مع مودم أو بوتلودر سامسونج.",
    causes: [
      "تعريف Samsung USB Mobile Driver قديم أو تالف.",
      "الهاتف غير موجود في وضع Download Mode الحقيقي (أو معلق في وضع غامض).",
      "كابل الشحن ينقل طاقة فقط بدون خطوط البيانات D+ و D-."
    ],
    solutionSteps: [
      "أعد تشغيل الهاتف إلى وضع Download Mode الأصلي (خفض الصوت + رفع الصوت مع توصيل الكابل).",
      "أغلق برامج Smart Switch و Kies ومكافح الفيروسات لأنها تحتجز المنفذ.",
      "استخدم برنامج أودين بنسخة أحدث (Odin v3.14.4) وشغله كمسؤول (Run as Administrator)."
    ],
    recommendedToolOrDriver: "تعريف SAMSUNG USB Driver v3 الرسمي",
    severity: "driver"
  },
  {
    id: "err-qcom-1",
    code: "Sahara Fail / Firehose Handshake Failed",
    tool: "Qualcomm EDL / QFIL",
    title: "فشل بروتوكول صحارى ومعالجات كوالكوم (Sahara Error)",
    meaning: "منفذ 9008 رفض استقبال ملف اللودر (Prog_firehose_xxxx.elf/mbn) أو انقطع الاتصال فجأة.",
    causes: [
      "ملف لودر البرمجة (Firehose MBN) غير مخصص لنفس رقم معالج الهاتف (MSM HW ID).",
      "الهاتف خرج تلقائياً من وضع 9008 بسبب ضعف البطارية أو قفلة التيست بوينت.",
      "وجود مسافة أو حروف عربية في مسار مجلد الفلاشة على الكمبيوتر."
    ],
    solutionSteps: [
      "انقل مجلد الفلاشة مباشرة إلى مسار قصير باللغة الإنجليزية مثل: `C:\\firmware\\`.",
      "تأكد من اختيار ملف Firehose المناسب لـ EMMC أو UFS بدقة.",
      "استخدم أدوات السحب الحديثة (Pandora أو UnlockTool) التي تحتوي على لودرات كوالكوم مدمجة بدون حاجة للودر خارجي."
    ],
    recommendedToolOrDriver: "برنامج QFIL v2.0 أو أداة Pandora Tool كوالكوم",
    severity: "fatal"
  },
  {
    id: "err-spd-1",
    code: "BKFN Wait for Baud Rate / Port Timeout",
    tool: "Unisoc SPD",
    title: "فشل مزامنة سرعة الباود معالجات سبريدترام",
    meaning: "أداة SPD Upgrade Tool لم تستطع ضبط وتثبيت سرعة قراءة منفذ الـ COM.",
    causes: [
      "تعريف SPD Unisoc Driver يحتاج إيقاف التحقق من توقيع التعريفات في ويندوز.",
      "الزر المستخدم للتبويت تم إفلاته قبل بدء قراءة الفلاشة.",
      "تلف في كونيكتور شحن الهاتف (سوكت الشحن Micro/Type-C)."
    ],
    solutionSteps: [
      "أعد تشغيل ويندوز في وضع Disable Driver Signature Enforcement.",
      "اضغط على زر خفض الصوت (أو رفع الصوت حسب الموديل) واستمر بالضغط حتى يكتمل شريط التحميل الأزرق.",
      "نظّف منفذ الشحن وتأكد من أن كابل الـ USB أصلي ينقل البيانات بسرعة عالية."
    ],
    recommendedToolOrDriver: "أداة SPD Factory Tool R27 الرسمية المرفقة في الموقع",
    severity: "driver"
  },
  {
    id: "err-unlock-1",
    code: "Waiting for device in BROM / Preloader Crash",
    tool: "UnlockTool / Pandora",
    title: "الهاتف يدخل وضع Preloader ثم ينفصل فوراً",
    meaning: "الهاتف لا يستقر في وضع BROM ويرتد تلقائياً إلى وضع الشحن أو الإقلاع العادي.",
    causes: [
      "نظام أندرويد الحديث يمنع استقرار BROM ويحتاج قفلة تيست بوينت (TestPoint).",
      "تعريف Mediatek USB VCOM Port يحتاج تصحيح عبر تصفية الـ Filter.",
      "البطارية موصولة وتمنع الهاتف من الدخول في وضع الطوارئ."
    ],
    solutionSteps: [
      "افصل فلاتة البطارية عن البوردة تماماً قبل التوصيل.",
      "استخدم قفلة التيست بوينت الموضحة في قسم (تيست بوينت) في الموقع للموديل المحدد.",
      "في أداة UnlockTool اختر التبويب الخاص بالمعالج واضغط (Crash Preloader to BROM)."
    ],
    recommendedToolOrDriver: "قسم تيست بوينت HMAX UNLOCKER للبحث عن نقطة الموديل",
    severity: "warning"
  }
];
