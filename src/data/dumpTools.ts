import { ItemData } from './hmaxData';

export interface DumpToolInfo {
  id: string;
  category: 'jtag' | 'software';
  icon: string;
  name: string;
  nameEn: string;
  desc: string;
  descEn: string;
  supported: string;
  url: string;
  cardsCount: number;
  items: ItemData[];
}

export const DUMP_TOOLS_CATALOG: DumpToolInfo[] = [
  {
    id: "easy_jtag",
    category: "jtag",
    icon: "🔌",
    name: "Easy JTAG Plus",
    nameEn: "Easy JTAG Plus",
    desc: "أداة احترافية رائدة متخصصة في سحب وكتابة الدامب والذاكرة عبر منفذ JTAG و eMMC و UFS. تعتبر من أقوى أدوات صيانة الذاكرة وإصلاح أخطاء البوت المستعصية.",
    descEn: "Professional hardware tool specialized in extracting and flashing full dumps via JTAG, eMMC and UFS.",
    supported: "eMMC • UFS • ISP • Xiaomi • Samsung • OPPO • Vivo • Realme",
    url: "https://easy-jtag.com/",
    cardsCount: 11,
    items: [
      { id: "ej-1", name: "Redmi Note 14 5G Beryl XML", ver: "6.5GB Easy JTAG", desc: "XML Dump كامل مسحوب بوكس إيزي جي تاج بلس لإصلاح البوت", link: "https://drive.google.com/file/d/1zxRGj8wgYfsDQaVfn7RB53Xw78JmCToF/view", pass: "MobiFirmware.VIP" },
      { id: "ej-2", name: "REDMI 9C M2006C3MG", ver: "3GB Easy JTAG", desc: "Easy JTAG Plus سحب الذاكرة كاملة", link: "https://drive.google.com/file/d/1YxY9QvJq62wAR88VcZSIrlh6q0BMx9Ui/view", pass: "MobiFirmware.VIP" },
      { id: "ej-3", name: "SAMSUNG A12 SM-A125F", ver: "A125FXXS6CXJ1", desc: "Easy JTAG 1.5GB لإصلاح الذاكرة الميتة", link: "https://drive.google.com/file/d/1RegTQJUux_RdrozEtt9eFR2bmECEnFq3/view", pass: "MobiFirmware.VIP" },
      { id: "ej-4", name: "OPPO A31 CPH2015 128GB", ver: "Easy JTAG 2.4GB", desc: "سحب مباشر لذواكر eMMC 128GB", link: "https://drive.google.com/file/d/1ZJ6o9C8jFB9MeRHdnB1N-AkeGtpaBu64/view", pass: "MobiFirmware.VIP" },
      { id: "ej-5", name: "OPPO A57 CPH2387", ver: "BIN Dump Header", desc: "دامب بين هيدر إيزي جي تاج بلس", link: "https://drive.google.com/file/d/1iVZkaOdBacWxZEjxenBhqYJxldSBqN3i/view", pass: "MobiFirmware.VIP" },
      { id: "ej-6", name: "Realme C35 RMX3511 XML 128GB", ver: "Easy JTAG", desc: "سحب المهندس ثامر زروقي لإصلاح البوت الميت", link: "https://drive.google.com/file/d/1YBVx9kAU2yXncW-sc54NZrnHVbCOLVE9/view", pass: "MobiFirmware.VIP" },
      { id: "ej-7", name: "HUAWEI Y7A PPA-LX2", ver: "Easy JTAG Plus", desc: "إصلاح البوت لهاتف هواوي Y7A مسحوب بدقة", link: "https://drive.google.com/file/d/1R5Rku8E4MN3t4miBfgGLIcVxqPVYX6iP/view", pass: "MobiFirmware.VIP" },
      { id: "ej-8", name: "VIVO Y03 4GB", ver: "Easy JTAG 4GB", desc: "سحب ذاكرة eMMC كاملة", link: "https://drive.google.com/file/d/1S6oZd5TGZHOfT8Yt6QgeQoYKQ8gAuYJr/view", pass: "MobiFirmware.VIP" },
      { id: "ej-9", name: "VIVO Y04 V2430 10GB", ver: "Easy JTAG 10GB", desc: "سحب حديث لأجهزة فيفو الحديثة", link: "https://drive.google.com/file/d/18qzexyLM46cv_rsa9f04tvKZceTJjbJ2/view", pass: "MobiFirmware.VIP" },
      { id: "ej-10", name: "VIVO Y27 & Y36 5G V2248", ver: "EX_A_15_2", desc: "UFS Dump لأجهزة فيفو الجيل الخامس", link: "https://drive.google.com/file/d/1sJdYeZPWctAnfDScxbiDBuKzv4RPGLGO/view", pass: "MobiFirmware.VIP" },
      { id: "ej-11", name: "VIVO Y04 V2430 OSv15", ver: "OSv15 Easy JTAG", desc: "نظام أندرويد 15 الحديث", link: "https://drive.google.com/file/d/1myQP49q9I-RuOFciiCwt93pVjC50bLCC/view", pass: "MobiFirmware.VIP" }
    ]
  },
  {
    id: "f64_ultra",
    category: "jtag",
    icon: "⚡",
    name: "F64 ULTRA",
    nameEn: "F64 ULTRA",
    desc: "أداة وبوكس F64 ULTRA الحديث فائق السرعة لسحب وكتابة الدامب والذاكرة عبر JTAG و UFS و EMMC. يتميز بدعم موديلات 2024 و 2025 و 2026 وأندرويد 14 و 15.",
    descEn: "Ultra-fast modern box for pulling and writing eMMC & UFS dumps on latest 2024-2026 models.",
    supported: "Samsung • Redmi • Vivo • OPPO • Realme • Honor",
    url: "https://flash64.com/",
    cardsCount: 17,
    items: [
      { id: "f64-1", name: "HONOR X9c FULL DUMP", ver: "MagicOS 8.0 Android 14", desc: "سحب بوكس فلاش 64 ألترا معالج Snapdragon 6 Gen 1", link: "https://drive.google.com/file/d/1Kd5cp_IQeTI_6fzz0HmZVgHKT-DSZfL0/view", pass: "MobiFirmware.VIP" },
      { id: "f64-2", name: "HONOR 400 ABR-N03", ver: "OSv15 F64 ULTRA", desc: "سحب أندرويد 15 كامل مع ملفات الشبكة", link: "https://drive.google.com/file/d/1beAVNfe4wY31rb8xfjz41hVWOxX7npqn/view", pass: "MobiFirmware.VIP" },
      { id: "f64-3", name: "HONOR X7a RKY-LX2 2GB", ver: "2GB Dump + NV", desc: "سحب حسام خيري مع ملفات الشبكة كاملة", link: "https://drive.google.com/file/d/1TiQ4y7sUK6cNxaUVT2tEcjgC3vjdlEr0/view", pass: "MobiFirmware.VIP" },
      { id: "f64-4", name: "POCO C75 / Redmi 14C / 17C", ver: "Flash64 Ultra 1GB", desc: "دامب 1GB للإحياء السريع مع ملفات الشبكة", link: "https://drive.google.com/file/d/1Ki8JkDYwOBdPhDm7OWcGv7s5wvY-fYPj/view", pass: "MobiFirmware.VIP" },
      { id: "f64-5", name: "POCO C65 256GB", ver: "F64 ULTRA 7GB", desc: "دامب 7GB كامل لذاكرة 256GB", link: "https://drive.google.com/file/d/1nT9Eb1NtNSxodYzYSPBqVcynvQqNwbdO/view", pass: "MobiFirmware.VIP" },
      { id: "f64-6", name: "REDMI 15C / POCO C85", ver: "OS2.0.221 7.4GB", desc: "F64 256GB كامل مسحوب بدقة", link: "https://drive.google.com/file/d/1ztxrctjJJLCoQq6a0ka7FWm_SRal1hwz/view", pass: "MobiFirmware.VIP" },
      { id: "f64-7", name: "REDMI A3 C61", ver: "16.V816 3.6GB", desc: "F64 ULTRA أندرويد حديث", link: "https://drive.google.com/file/d/1R-6hqUPVx5k5Y5l5Umws2-f0fXZNKOHi/view", pass: "MobiFirmware.VIP" },
      { id: "f64-8", name: "REDMI 10A 220233L2G", ver: "V12.5.3 2.5GB", desc: "سحب بوكس فلاش 64 ألترا", link: "https://drive.google.com/file/d/1ApV1GSSHo74SnIgm7rQEYxrmx673uoTP", pass: "MobiFirmware.VIP" },
      { id: "f64-9", name: "SAMSUNG A25 5G SM-A256E", ver: "A256EXXS8CYG3", desc: "F64 ULTRA 4.5GB معالج إكسينوس حديث", link: "https://drive.google.com/file/d/1Tw19y4kZPm8mHaO0raheL4nIfp3_HUv2/view", pass: "MobiFirmware.VIP" },
      { id: "f64-10", name: "OPPO RENO 12F 4G CPH2687", ver: "CPH2687 8.52GB", desc: "F64 BOX 8.52GB كامل", link: "https://drive.google.com/file/d/1OY4I_TmBJsEKNlUdHPULjpiLOEyQJuIc/view", pass: "MobiFirmware.VIP" },
      { id: "f64-11", name: "OPPO A6 PRO 5G CPH2781", ver: "CPH2781_11.A.31", desc: "F64 BOX دامب حديث شبكة 5G", link: "https://drive.google.com/file/d/1cW5EhSPHntwe3W3tiDN651OpvXvf7gHJ/view", pass: "MobiFirmware.VIP" },
      { id: "f64-12", name: "Realme 10 PRO 5G RMX3661", ver: "256GB UFS", desc: "F64 BOX دامب ذاكرة يو إف إس السريعة", link: "https://drive.google.com/file/d/1a6XXCbruh394KhIMOGDwhmnzZADaSuMV/view", pass: "MobiFirmware.VIP" },
      { id: "f64-13", name: "Realme NOTE 60X RMX3938", ver: "64GB eMMC", desc: "سحب بوكس فلاش 64 ألترا", link: "https://drive.google.com/file/d/1pcICRDgQ1ZbFP0sCF0aG6wEPSksEBdln/view", pass: "MobiFirmware.VIP" },
      { id: "f64-14", name: "VIVO Y21D PD2510F", ver: "256GB UFS 8.2GB", desc: "F64 ULTRA دامب كامل ومختبر", link: "https://drive.google.com/file/d/18qzexyLM46cv_rsa9f04tvKZceTJjbJ2/view", pass: "MobiFirmware.VIP" },
      { id: "f64-15", name: "VIVO Y03T PD2360F", ver: "64GB eMMC 4.9GB", desc: "F64 ULTRA سحب موثوق", link: "https://drive.google.com/file/d/1S6oZd5TGZHOfT8Yt6QgeQoYKQ8gAuYJr/view", pass: "MobiFirmware.VIP" },
      { id: "f64-16", name: "VIVO Y18 PD2327F", ver: "128GB eMMC 4.4GB", desc: "F64 ULTRA دامب كامل 128GB", link: "https://drive.google.com/file/d/1a0oOV43ud0t9L149BD1pKRj1MK4LAGGH/view", pass: "MobiFirmware.VIP" },
      { id: "f64-17", name: "VIVO Y22S PD2228F", ver: "128GB UFS", desc: "F64 BOX دامب ذاكرة كوالكوم", link: "https://drive.google.com/file/d/1myQP49q9I-RuOFciiCwt93pVjC50bLCC/view", pass: "MobiFirmware.VIP" }
    ]
  },
  {
    id: "ufi",
    category: "jtag",
    icon: "🚀",
    name: "UFI Box",
    nameEn: "UFI Box",
    desc: "بوكس UFI الشهير لصيانة أجهزة الأندرويد والذواكر، يعتبر المفضل في استخراج وإصلاح رومات كوالكوم وميديا تيك عبر JTAG و eMMC Direct.",
    descEn: "Renowned UFI Box for repairing Qualcomm & MediaTek chips via JTAG and Direct eMMC.",
    supported: "Qualcomm • MediaTek • ISP Pinouts",
    url: "https://ufibox.com/download/",
    cardsCount: 1,
    items: [
      { id: "ufi-1", name: "HONOR X7A RKY-LX2 UFI", ver: "UFI Box Direct", desc: "دامب كامل مسحوب بواسطة UFI Box - باسورد: Melok@AbouAmr", link: "https://www.mediafire.com/file/ldl8120aynxzlhx/honor_x7a_RKY-LX2_full_dump_by_UFI.rar/file", pass: "Melok@AbouAmr" }
    ]
  },
  {
    id: "unlocktool",
    category: "software",
    icon: "🔓",
    name: "UnlockTool",
    nameEn: "UnlockTool",
    desc: "الأداة الأكثر استخداماً وشهرة عالمياً بين فنيي السوفت وير. تدعم قراءة وسحب الدامب وتخطي FRP وتفليش الهواتف لآلاف الموديلات.",
    descEn: "The world's leading multi-brand software tool for flashing, unlocking and dump reading.",
    supported: "Samsung • Xiaomi • Transsion • Vivo • OPPO • Realme • Huawei",
    url: "https://file.unlocktool.net/",
    cardsCount: 16,
    items: [
      { id: "ut-1", name: "AllCall Hero 60 Max (RARE)", ver: "UnlockTool Full Dump", desc: "دامب حصري ونادر جداً مسحوب مباشرة من الهاتف بأداة أنلوك تول", link: "https://drive.google.com/file/d/1EsPIC9Wp1h0vWDRA1Gi6k-obUHYGkEqu/view", pass: "MobiFirmware.VIP" },
      { id: "ut-2", name: "ITEL P37 P651W", ver: "UnlockTool + NVRAM", desc: "دامب كامل مسحوب مع ملفات الشبكة لإصلاح السيريال المفقود", link: "https://drive.google.com/file/d/1-FOKgpMC-oVjuyVdIS2LNeMqcQvP704J/view", pass: "MobiFirmware.VIP" },
      { id: "ut-3", name: "ITEL A06 A669W 2GB", ver: "SA375A UnlockTool", desc: "سحب المهندس حمالله عبد المالك بحجم 2GB كامل", link: "https://drive.google.com/file/d/1KJX3Zv3JPcke4sWTE8ubE-3xPAevhNjO/view", pass: "MobiFirmware.VIP" },
      { id: "ut-4", name: "Infinix Smart 5 X657C Full+NV", ver: "X657C-H6117GH", desc: "دامب أنلوك تول كامل مع ملفات الـ NV", link: "https://drive.google.com/file/d/148UbsVqN_G7H2OsJlPH5-S6kGr3YfJ-C/view", pass: "MobiFirmware.VIP" },
      { id: "ut-5", name: "Infinix Smart 20 X6840B FULL", ver: "16.1.0.150SP02", desc: "سحب أداة UnlockTool كامل ومختبر", link: "https://drive.google.com/file/d/1AZywXmJEL1BBJaB3Cx5KF7iE7G3c2RqS/view", pass: "MobiFirmware.VIP" },
      { id: "ut-6", name: "Vivo Y15s PD2140F (2 Versions)", ver: "UnlockTool Dump", desc: "نسختان لمعالجة مشكلات الإقلاع", link: "https://drive.google.com/file/d/1CCH-oDVN-Erjh1O0o3sEZcnH4QWQX-Mc/view", pass: "MobiFirmware.VIP" },
      { id: "ut-7", name: "WIKO T10 FULL DUMP", ver: "W-V673-V01.57", desc: "سحب أنلوك تول أصلي كامل", link: "https://drive.google.com/file/d/1HGMTtBPH4TNYXIusU4G1ZO3scGphM7cq/view", pass: "MobiFirmware.VIP" },
      { id: "ut-8", name: "VILLAON V20 FULL DUMP", ver: "W-V673 UnlockTool", desc: "دامب أصلي ونادر لهواتف فيلاون", link: "https://drive.google.com/file/d/10EaY1ggOVvB2Yrgf7BZYSqMcu23fIB7I/view", pass: "MobiFirmware.VIP" },
      { id: "ut-9", name: "M-HORSE HOT 40 Pro V03", ver: "V03-20240807", desc: "دامب كامل مع ملفات الشبكة", link: "https://drive.google.com/file/d/1D1-GnB2U8msn6DINNQ7qSs2Q2DkPqZtD/view", pass: "MobiFirmware.VIP" },
      { id: "ut-10", name: "M-HORSE HOT 30 V05", ver: "HOT 30-M-HORSE-V05", desc: "سحب أنلوك تول أصلي للمهندس حمالله", link: "https://drive.google.com/file/d/1tpgGTmlS8ZV_T6Pbd-5U58fXrLqV8i7T/view", pass: "MobiFirmware.VIP" },
      { id: "ut-11", name: "M-HORSE SPARK 10 Pro (3v)", ver: "V02 / V05 / V06", desc: "3 دامبات لتغطية جميع إصدارات الشاشات والبورد", link: "https://drive.google.com/file/d/1tkQijRTWEyWqmiBx-23aiY-NOIw061sr/view", pass: "MobiFirmware.VIP" },
      { id: "ut-12", name: "HISORL T901 FULL DUMP", ver: "UnlockTool", desc: "سحب خالد كابو على جوجل درايف", link: "https://drive.google.com/file/d/1IQMjflRd0asfRQl3_z2PaCu6FeAxvzyO/view", pass: "MobiFirmware.VIP" },
      { id: "ut-13", name: "Honor X7B CLK-LX2 C185", ver: "UnlockTool Dump", desc: "معالج كوالكوم مسحوب بأنلوك تول", link: "https://drive.google.com/file/d/1C2dhyqDx6WA7gb3VXcaYwG4PTQ5NweRM/view", pass: "MobiFirmware.VIP" },
      { id: "ut-14", name: "Samsung Tab A9 SM-X110", ver: "X110XXS6CYI3", desc: "سحب أداة أنلوك تول تابلت سامسونج الرسمي", link: "https://drive.google.com/file/d/199DEolDruK6iP3oh6iGJ9XkOJWJsDqil/view", pass: "MobiFirmware.VIP" },
      { id: "ut-15", name: "OPPO A54 CPH2239 Dead Boot", ver: "CPH2239_11_C.33", desc: "UnlockTool + NV لإصلاح الموت المفاجئ", link: "https://drive.google.com/file/d/1-J8LMb2OzTHZXJl0M8Y4pE6A6uNrREg1/view", pass: "MobiFirmware.VIP" },
      { id: "ut-16", name: "Itel L6503 Vision 2 (UnlockTool)", ver: "1.7GB Full Dump", desc: "سحب أنلوك تول لهاتف ايتل فيجن 2", link: "https://drive.google.com/file/d/1cUD2DdoJUYqCZcQA4mMD0PqjKv2QLDwY/view", pass: "MobiFirmware.VIP" }
    ]
  },
  {
    id: "pandora",
    category: "software",
    icon: "🐾",
    name: "Pandora Tool",
    nameEn: "Pandora Tool",
    desc: "أداة باندورا العملاقة من Z3X المتخصصة في معالجات ميديا تيك وسبريدترام (Unisoc). الحل رقم 1 عالمياً لفك الشفرات وسحب الدامب الصعب.",
    descEn: "Z3X Pandora Tool — the undisputed king of MediaTek and Unisoc/SPD dumping and repairing.",
    supported: "MediaTek • Spreadtrum / Unisoc",
    url: "https://downloads1.z3x.dev/getLatestVersion.php",
    cardsCount: 24,
    items: [
      { id: "pnd-1", name: "INFINIX NOTE 30 5G X6711", ver: "X6711 V600 Pandora", desc: "سحب بوكس باندورا كامل", link: "https://drive.google.com/file/d/1ubef2yjzrQpNB0MFPw8UWdraxPr6OtbB/view", pass: "MobiFirmware.VIP" },
      { id: "pnd-2", name: "Moto E13 XT2345-4", ver: "PND Tool Tested", desc: "دامب باندورا كامل ومختبر موثوق", link: "https://drive.google.com/file/d/101c8ovGsl5Mfg1UrkPRZv9L9OYZUKBg6/view", pass: "MobiFirmware.VIP" },
      { id: "pnd-3", name: "ITEL S23 S665LN (2 Parts)", ver: "F065-S-GL-V305", desc: "دامب باندورا كامل ومختبر", link: "https://www.terabox.app/arabic/sharing/link?surl=RMigbSPD9-7YafQPj0LlMQ", pass: "MobiFirmware.VIP" },
      { id: "pnd-4", name: "ITEL A49 A661L (A58 Pro)", ver: "Pandora Rescue", desc: "دامب بوكس باندورا لإحياء الهاتف", link: "https://www.terabox.app/arabic/sharing/link?surl=aylVN-8Y7P9jI6ye9JpsMQ", pass: "MobiFirmware.VIP" },
      { id: "pnd-5", name: "M-HORSE POP 8 - 1GB", ver: "POP 8-V01 Pandora", desc: "دامب باندورا أصلي", link: "https://drive.google.com/file/d/11Ck6VqXy_UdagNjz6GvMiRg7JH2DQmuu/view", pass: "MobiFirmware.VIP" },
      { id: "pnd-6", name: "Redmi 13C Gale", ver: "OS2.0.6.0.VGPMIXM", desc: "سحب باندورا كامل", link: "https://www.terabox.app/arabic/sharing/link?surl=h5bhksix3MWtLXRftpknUQ", pass: "MobiFirmware.VIP" },
      { id: "pnd-7", name: "Realme C35 RMX3511 A.55", ver: "Pandora Full Dump", desc: "دامب باندورا كامل لإصلاح البوت", link: "https://drive.google.com/file/d/1L6PYGzOfBmmgazHS7KT-ouc3INAU0cl7/view", pass: "MobiFirmware.VIP" },
      { id: "pnd-8", name: "Realme C71 RMX5303", ver: "export_15_C.09 7.4GB", desc: "7.4GB دامب باندورا كامل ومحدث", link: "https://drive.google.com/file/d/1xficluJ65Ny-Vlih9Ys0rBlWk6OKa9Jj/view", pass: "MobiFirmware.VIP" },
      { id: "pnd-9", name: "Realme Note 50 RMX3834 A.89", ver: "Pandora Dump", desc: "سحب المهندس عبد الله غانم", link: "https://drive.google.com/file/d/10uJP9wiJkrBzGRQIwfjOVcjpCYhAJWoJ/view", pass: "MobiFirmware.VIP" },
      { id: "pnd-10", name: "Realme C67 COPY Pandora", ver: "1.1GB Pandora", desc: "سحب برنس كازانوفا لأجهزة الكوبي", link: "https://drive.google.com/file/d/1ZFf5jTLPsXjOXU48yb5C_rwmLTiX8BOx/view", pass: "MobiFirmware.VIP" },
      { id: "pnd-11", name: "OPPO A55 CPH2325 F.71", ver: "4.7GB Pandora", desc: "سحب كامل بوكس باندورا", link: "https://drive.google.com/file/d/1KsSxwMJRtAJoAGeTA7Uq4JHgzbe2GsMz/view", pass: "MobiFirmware.VIP" },
      { id: "pnd-12", name: "OPPO CPH1933 A5 2020", ver: "3GB Pandora", desc: "3GB دامب كوالكوم كامل", link: "https://drive.google.com/file/d/1xQjwapIINwF4rewMG38Sd7n1iltoqep2/view", pass: "MobiFirmware.VIP" },
      { id: "pnd-13", name: "Nokia C12 TA-1583 (Pandora)", ver: "00WW_1_54B_SP01", desc: "دامب باندورا كامل ومختبر", link: "https://drive.google.com/file/d/1S9_2MsbRY3hfhFEnvHmdCERLWh0GxCSH/view", pass: "MobiFirmware.VIP" },
      { id: "pnd-14", name: "Nokia C10 TA-1342", ver: "SC7731E Pandora", desc: "معالج سبريدترام SC7731E", link: "https://drive.google.com/file/d/1JJMRH_rQBuxHvy_f47Y4ejv3baLRiwfV/view", pass: "MobiFirmware.VIP" },
      { id: "pnd-15", name: "Nokia 5.3 TA-1234", ver: "00WW_2_290 Pandora", desc: "دامب باندورا نوكيا 5.3", link: "https://drive.google.com/file/d/1gmkObCQDILmhXNnmumBVeyCt69a5Mflr/view", pass: "MobiFirmware.VIP" },
      { id: "pnd-16", name: "iPhone 16 Pro Max Copy", ver: "Pandora 1.4GB", desc: "معالج MT6735 سوفت وير أندرويد", link: "https://drive.google.com/file/d/1SOhno0YtFUzYGauWnXrr7GIimY6QLHuk/view", pass: "MobiFirmware.VIP" },
      { id: "pnd-17", name: "S26 ULTRA COPY SAMBA65S", ver: "Pandora Dump", desc: "IPRO SAMBA65S جهاز مقلد", link: "https://drive.google.com/file/d/1alw0UC9SxIJW9IsHQnXOP9Uvl8xYEAjU/view", pass: "MobiFirmware.VIP" },
      { id: "pnd-18", name: "AllCall Magic 60", ver: "EG_AOS14 Pandora", desc: "دامب أصلي كامل", link: "https://drive.google.com/file/d/16LeQjY7x-slLFuftE9DVFrtBdvmfCvqx/view", pass: "MobiFirmware.VIP" },
      { id: "pnd-19", name: "KXD A07 Android 13", ver: "Pandora 3GB", desc: "سحب باندورا رسمي", link: "https://drive.google.com/file/d/1SqGxl0jvG9OYeE-A0zXnJusk2kTS7xGB/view", pass: "MobiFirmware.VIP" },
      { id: "pnd-20", name: "KXD A07 Android 12", ver: "Pandora 2.2GB", desc: "إصدار أندرويد 12 القديم", link: "https://drive.google.com/file/d/1hOfF0HqTxCH0NclxiK2eJsg4uS7XPVTb/view", pass: "MobiFirmware.VIP" },
      { id: "pnd-21", name: "LAVA Iris 59 LE9930", ver: "Pandora Dump", desc: "دامب لافا أصلي ومجرب", link: "https://www.terabox.app/arabic/sharing/link?surl=-okpAZRO3RAKy-8YIrP7sQ", pass: "MobiFirmware.VIP" },
      { id: "pnd-22", name: "WALTON NEXG N72", ver: "Pandora Full+NV", desc: "دامب كامل مع ملفات الشبكة", link: "https://www.terabox.app/arabic/sharing/link?surl=UfydmqOdzA2ciqvCRFF_9A", pass: "MobiFirmware.VIP" },
      { id: "pnd-23", name: "RAVOZ V7", ver: "Pandora 3.5GB", desc: "أندرويد 14 أصلي", link: "https://drive.google.com/file/d/1qcGLeJIGgmwKVTHa-sdvUyuIYeZAv5dc/view", pass: "MobiFirmware.VIP" },
      { id: "pnd-24", name: "Itel L6503 Vision 2 (Pandora)", ver: "1.7GB Pandora", desc: "سحب بوكس باندورا لجهاز ايتل", link: "https://drive.google.com/file/d/1cUD2DdoJUYqCZcQA4mMD0PqjKv2QLDwY/view", pass: "MobiFirmware.VIP" }
    ]
  },
  {
    id: "cm2",
    category: "software",
    icon: "📦",
    name: "Infinity CM2",
    nameEn: "Infinity CM2",
    desc: "أداة InfinityBox CM2 الأسطورية لمعالجات ميديا تيك وسبريدترام، تعد الأقوى في تفليش وسحب التابلت والأجهزة الصينية الصعبة وتخطي حمايات المعالج.",
    descEn: "InfinityBox CM2 — the industry standard for MTK & Unisoc Chinese devices and tablets.",
    supported: "MediaTek • Unisoc/SPD • Qualcomm • Chinese Brands",
    url: "https://infinity-box.com/download/",
    cardsCount: 10,
    items: [
      { id: "cm2-1", name: "Benco V60 Full [CM2]", ver: "CM2 Full Dump", desc: "سحب كامل ببوكس CM2 بدون أي أخطاء", link: "https://drive.google.com/file/d/1IWj92n5541TYoYKXe-sC9eyNkbsrte6f/view", pass: "MobiFirmware.VIP" },
      { id: "cm2-2", name: "BENCO S1 Pro AE9260 DUAL", ver: "CM2 + Pandora", desc: "دامبان كاملان باندورا + CM2", link: "https://drive.google.com/file/d/1Dx6I5z92KofjEru4xveT7SZ-TeQj7a_L/view", pass: "MobiFirmware.VIP" },
      { id: "cm2-3", name: "M-Horse C55 DOOGEE X96Pro", ver: "CM2 Dump 1.7GB", desc: "سحب المهندس حسام مصطفى", link: "https://drive.google.com/file/d/12sZU4xYmYaeZErGi3zLMN_eeQf_kx7MN/view", pass: "MobiFirmware.VIP" },
      { id: "cm2-4", name: "YTAB ULTRA 35", ver: "CM2 3GB", desc: "سحب Prince Cazanova للتابلت الصيني", link: "https://drive.google.com/file/d/1zplMZgC3PUa_MP0F5BOtosQejZaom4dZ/view", pass: "MobiFirmware.VIP" },
      { id: "cm2-5", name: "Oteeto TAB 15", ver: "CM2 Rare", desc: "تاب صيني نادر جداً مسحوب ومختبر", link: "https://drive.google.com/file/d/19RaJLb3dnlcj3Wj9hdkg8I4aL-tUuHQY/view", pass: "MobiFirmware.VIP" },
      { id: "cm2-6", name: "Nokia C12 TA-1583 (CM2)", ver: "00WW_1_54B_SP01", desc: "دامب CM2 كامل مجرب", link: "https://drive.google.com/file/d/1S9_2MsbRY3hfhFEnvHmdCERLWh0GxCSH/view", pass: "MobiFirmware.VIP" },
      { id: "cm2-7", name: "iPhone 17 Pro Copy DS-BD2", ver: "CM2 Dump", desc: "DCODE DS-BD2 أندرويد بهيئة آيفون", link: "https://drive.google.com/file/d/1HNXlgyu8pInqB2RLvFQNmaHks8pA7v8-/edit", pass: "MobiFirmware.VIP" },
      { id: "cm2-8", name: "S26 Ultra COPY MT6580", ver: "CM2 Dump", desc: "معالج MT6580 قديم مع كشف الخداع Fake Detected", link: "https://drive.google.com/file/d/1imGiG3ca2omwJBxJQWsYl2w0SAObQAhl/view", pass: "MobiFirmware.VIP" },
      { id: "cm2-9", name: "BLU T5 TIGO T0050TT", ver: "CM2 Full Dump", desc: "سحب CM2 كامل", link: "https://www.terabox.app/arabic/sharing/link?surl=TLasYwRnDISWcAK9WLzB3Q", pass: "MobiFirmware.VIP" },
      { id: "cm2-10", name: "Itel L6503 Vision 2 (CM2)", ver: "CM2 3GB Dump", desc: "سحب بوكس CM2 بحجم 3 جيجابايت", link: "https://drive.google.com/file/d/1cUD2DdoJUYqCZcQA4mMD0PqjKv2QLDwY/view", pass: "MobiFirmware.VIP" }
    ]
  },
  {
    id: "amt",
    category: "software",
    icon: "🛠️",
    name: "AMT Tool",
    nameEn: "Android Multi Tool",
    desc: "أداة AMT Tool لتفليش ومعالجة رومات وسحب أقسام البارتيشن لأجهزة Unisoc و MediaTek الحديثة ونظام أندرويد 15 و 16.",
    descEn: "Android Multi Tool for reading and flashing modern Unisoc & MediaTek partitions.",
    supported: "Unisoc • MediaTek • Android 15/16",
    url: "https://androidmultitool.com/download/",
    cardsCount: 3,
    items: [
      { id: "amt-1", name: "Redmi A3x missi Android 16", ver: "4.5GB AMT Tool", desc: "سحب أداة AMT Tool أندرويد 16 الحديث", link: "https://drive.google.com/file/d/1Xxx7HG60lnaXQft27RdCmvzresdbppBb/view", pass: "MobiFirmware.VIP" },
      { id: "amt-2", name: "Motorola XT2523-7 Moto E15", ver: "AMT Tool 2.9GB", desc: "دامب كامل أندرويد حديث لموتورولا", link: "https://drive.google.com/file/d/16E-6KmWMco6QT-t-H3Mhk5xCCS6j8urw/view", pass: "MobiFirmware.VIP" },
      { id: "amt-3", name: "Tecno Spark 40 Pro KM6", ver: "Android 15 AMT 9.5GB", desc: "دامب تكنو سبارك 40 برو أندرويد 15 كامل", link: "https://drive.google.com/file/d/1VGTT7qXGlO7ZxOqMbjG77-oUcTjBwD0i/view", pass: "MobiFirmware.VIP" }
    ]
  },
  {
    id: "miracle",
    category: "software",
    icon: "✨",
    name: "Miracle Box",
    nameEn: "Miracle Thunder",
    desc: "بوكس Miracle Box / Miracle Thunder الشهير في معالجات هواتف الأزرار والكوبي والهواتف القديمة.",
    descEn: "Miracle Thunder Box for button phones, feature phones and classic MTK/SPD clones.",
    supported: "Feature Phones • MTK • SPD",
    url: "https://miraclebox.com/download/",
    cardsCount: 1,
    items: [
      { id: "mrc-1", name: "Nokia TA-1114 Copy (Miracle)", ver: "Spreadtrum Miracle", desc: "نسخة كلاكيت ميراكل بوكس", link: "https://drive.usercontent.google.com/download?id=1_c708OPmAWhZW6Fudrl7TCXRkyyU_Scb", pass: "MobiFirmware.VIP" }
    ]
  }
];
