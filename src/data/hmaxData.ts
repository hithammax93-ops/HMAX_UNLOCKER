import { TECNO_MODELS } from './tecnoModels';
import { LT_PHONES_CATALOG } from './ltPhonesData';

export const MASTER_PASS = "MobiFirmware.VIP";

export interface ItemData {
  id: string;
  name: string;
  ver?: string;
  desc?: string;
  link?: string;
  image?: string;
  pass?: string;
  category?: string;
  video?: string;
  guide?: string;
}

export interface DumpBrand {
  id: string;
  name: string;
  count: number;
  color: string;
  icon: string;
}

export interface TextGuide {
  id: string;
  title: string;
  tag: string;
  steps: { num: number; text: string }[];
  problem: string;
  solutionIntro: string;
  conclusionNote?: string;
  warningNote?: string;
  codeSnippet?: string;
}

export interface Experience {
  id: string;
  title: string;
  author: string;
  problem: string;
  solutionSteps?: { num: number; text: string }[];
  solutionDesc?: string;
  warning?: string;
  links: { label: string; url: string; primary?: boolean }[];
}

export const HMAX_DATA = {
  tools: [
    { id: "tool-1", name: "Chimera Tool", ver: "v38.72.1026 PRO", desc: "أقوى أداة سامسونج وهواوي وشاومي", link: "https://chimeratool.com/ar/download", pass: "—" },
    { id: "tool-2", name: "Hydra Dongle", ver: "Latest", desc: "دعم MTK - Qualcomm - SPD شامل", link: "https://www.hydradongle.com/download/software", pass: "—" },
    { id: "tool-3", name: "PANDORA Tool", ver: "Latest", desc: "Z3X Pandora — إصلاح وشحن ودامب شامل", link: "https://downloads1.z3x.dev/getLatestVersion.php", pass: "—" },
    { id: "tool-4", name: "QCDMA Tool", ver: "Latest", desc: "أداة كوالكوم لبرمجة يمن موبايل", link: "https://mega.nz/folder/fEQVBLab#1cPjBryW2_XPmqjxDoNZ0Q", pass: "—" },
    { id: "tool-5", name: "CDMA Yemen", ver: "Latest", desc: "برمجة يمن موبايل وتفعيل CDMA", link: "https://www.mediafire.com/folder/kz5v059ycm44j/CDMA_YEMEN_TOOL", pass: "—" },
    { id: "tool-6", name: "TSM Tool Pro", ver: "v2.4.1", desc: "TSM Pro Setup للسامسونج وموتورولا", link: "https://www.mediafire.com/file/vqh1h1uhwq9s2xo/TSM_SetupV2.4.1.7z/file", pass: "—" },
    {
      id: "tool-7",
      name: "TSM PRO EDITION",
      ver: "2026.10.16",
      desc: `TSM PRO EDITION 2026.10.16 | Update

Added Nothing 4B Support [EDL Mode]
Added Unisoc ADL Mode [Unknown USB Mode] [ZTE Devices]
• Remove FRP
• Factory reset
Tested ZTE models:
• ZTE nubia Neo 2 5G [Z2352N]
• ZTE Blade A56 [Z2473]
• ZTE nubia V80 Pro [Z2576]
• ZTE Blade A36 [Z2472]
• ZTE nubia Neo 3 GT 5G [Z2465N]
• ZTE Blade A55 [Z2450]
• ZTE Blade A75 4G [Z2359]
Note: Method covers ZTE devices.

Added New Bits Samsung 2026 [EDL Mode]
• Remove FRP
• Factory Reset
• Read/Write Firmware/Dump
Supported Samsung models:
• Galaxy A23 5G [SM-A236B bitH]
• Galaxy A23 5G [SM-A236E bitH]
• Galaxy A23 5G [SM-A236M bitH]
• Galaxy F14 4G [SM-E145F bitD]
• Galaxy Z Flip4 [SM-F721N bit8]
• Galaxy Z Fold3 5G [SM-F926N bitE]
• Galaxy Z Fold6 [SM-F956N bit4]
• Galaxy S21 FE 5G [SM-G990B2 bitK]
• Galaxy Tab A9+ 5G [SM-X216C bitC]
• Galaxy Tab A9+ 5G [SM-X216N bitD]

Added More Support:
• TCL 9185W
• TCL T513Z
• TCL 30+ [T676K]
• ZTE NUBIA NEO 5G [8150N]
• ZTE BLADE A112 [P635A60]
• REDMAGIC 11S Pro [NX809J]
• REDMAGIC Nova Gaming Table [NP03J]
• honor play 20a
• lenovo Tab M11 [TB330XU]
• OUKITEL C68

Improved Fastboot Flasher Moto/Xiaomi

Fixed Bugs:
• Preloader Mode: Redmi A3 [blue], Poco C61 [blue], Poco C50 [blue]
• Crash with Remove FRP MTP OS16
• Change CSC
• Select Moto Maps flashfile*/servicefile*`,
      link: "https://www.mediafire.com/file/vqiuhtmypiv7gzs/TSM+Pro+Edition+Setup[2026.10.16].7z/file",
      image: "/images/tsmtool.jpg",
      pass: "—",
    },
    { id: "tool-8", name: "DFT Pro", ver: "v8.0.0", desc: "Dongle For Tools الشهير لشياومي وهواوي", link: "https://www.mediafire.com/file/m4ssk83p5wr5mxa/DFTPRO_v8.0.0.exe/file", pass: "—" },
    { id: "tool-9", name: "Sigma Plus", ver: "v1.01.13", desc: "SigmaKey — هواوي وميدياتك وكوالكوم", link: "https://sigmakey.com/nfs/content/5802/file/sigmaplus-software-setup-v1.01.13.exe", pass: "—" },
    { id: "tool-10", name: "Sigma Kirin", ver: "Kirin Files", desc: "ملفات تفليش ودعم معالجات Kirin", link: "https://mega.nz/file/HpgniKDT#OjCTB2_Ki_TxcKs7mCBNgd08eDVa1jPwOsU1aci0KXU", pass: "—" },
    { id: "tool-11", name: "Sigma Exynos", ver: "Exynos Files", desc: "ملفات تفليش ودعم Exynos", link: "https://www.mediafire.com/file/fwqvfmq5om67t69/exynos.rar/file", pass: "—" },
    { id: "tool-12", name: "UnlockTool", ver: "Latest", desc: "الأشهر عالمياً لفك الشفرات وتخطي FRP", link: "https://file.unlocktool.net/", pass: "—" },
    { id: "tool-13", name: "AndroidUtility", ver: "v200", desc: "AUM — حلول الطوارئ والبوتلودر", link: "https://www.mediafire.com/file/dp73po1rf9x4rgz/AndroidUtility.v200.7z/file", pass: "—" },
    { id: "tool-14", name: "MaxTech Server VIP", ver: "v2.0 PRO", desc: "تعريب سامسونج أندرويد 15 و16 وتفعيل VoLTE وإظهار 4G/5G هدية عاهد وبشير وهيثم ماكس", link: "https://t.me/haithamMax1", pass: "—" },
    { id: "tool-15", name: "MobilEdit Forensic / Bypass", ver: "Pro Bypass", desc: "تجاوز حماية FRP وKG Lock لمعالجات Exynos عبر وضع الشريحة", link: "https://www.mobiledit.com/", pass: "—" },
    { id: "tool-16", name: "MobiMover Pro", ver: "Full Transfer", desc: "نقل الرسائل والبيانات بين iPhone و Android والعكس", link: "https://www.easeus.com/phone-transfer/mobimover.html", pass: "—" },
    { id: "tool-17", name: "iTunes Paid Extractor", ver: "App Suite", desc: "تنزيل وتثبيت تطبيقات وألعاب الآيفون بدون متجر رسمي", link: "https://t.me/hithamMax", pass: "—" }
  ],

  drivers: [
    { id: "drv-1", name: "ADB Driver Universal", ver: "v6.0", desc: "تعريف شامل لأجهزة الأندرويد في وضع ADB", link: "https://www.mediafire.com/file_premium/yx9pry29zxw0rsd/UniversalAdbDriverSetup.msi/file" },
    { id: "drv-2", name: "MTK Driver", ver: "v2.0.1.1", desc: "تعريف معالجات ميديا تيك MediaTek الرسمية", link: "https://www.mediafire.com/file_premium/0psu8awm57or6jj/drivers_mtk_v2.0.1.1_2.7z/file" },
    { id: "drv-3", name: "Samsung USB Driver", ver: "v3", desc: "التعريف الرسمي لهواتف وتك رومات سامسونج", link: "https://www.mediafire.com/file_premium/92yzwgkkvkutye5/SAMSUNG_USB_Driver_for_Mobile_Phones_3.exe/file" },
    { id: "drv-4", name: "Fastboot Driver", ver: "Latest", desc: "تعريف وضع Fastboot و Bootloader", link: "https://mega.nz/file/w0plHSKZ#TjvkWuc9OmOpQiJq7Nr0U-ANlPVyf7RP1-2KvcgaSO4" },
    { id: "drv-5", name: "Exynos Driver", ver: "Latest", desc: "تعريف خاص بمعالجات سامسونج إكسينوس", link: "https://mega.nz/file/ksYGmJ6T#_7DeakMDKI9lPkGIvUA0TIN9qHGCUtSrDfTDAump3WU" },
    { id: "drv-6", name: "ADB Fix Yemen", ver: "Fix", desc: "إصلاح قراءة الـ ADB في اليمن لجميع البوكسات", link: "https://mega.nz/file/UgZwSCRS#rgIJ8Wdli6yG_m6V7aWzJZmrVLIfHTrzQWZUhvU6Ums" },
    { id: "drv-7", name: "QCOM Driver 9008", ver: "HS-USB", desc: "تعريف كوالكوم بورت 9008 للطوارئ EDL", link: "https://www.mediafire.com/file_premium/huiyajts19ntc0y/drivers_qcom_v1.0.7z/file" },
    { id: "drv-8", name: "COM-1 Prolific Driver", ver: "Prolific", desc: "تعريف كابلات البوكسات وكابلات السيريال COM", link: "https://mega.nz/file/M9IgjQxB#lPAouwiWNAwxPjfKuj0OQT1fqcplCKjyeCdIb7WFSqQ" },
    { id: "drv-9", name: "SPD Driver", ver: "R4.20", desc: "تعريف معالجات سبريدترام SPD Unisoc", link: "https://www.mediafire.com/file_premium/faeoenrr0yjbj91/SPD_Driver_R4.20.0201_last_drivers.zip/file" },
    { id: "drv-10", name: "MTK Bypass Auth Fix", ver: "Bypass", desc: "باتش تجاوز حماية الـ SLA/DA لمعالجات MTK", link: "https://www.mediafire.com/file_premium/cm92fbnnig76nn4/Driver-Mtk-Fix-ChuyenMobileGsm.zip/file" },
    { id: "drv-11", name: "OnePlus USB Driver", ver: "Latest", desc: "التعريف الرسمي لهواتف وان بلس في جميع الأوضاع", link: "https://www.mediafire.com/file/1l2vuh3c7pes193/OnePlus-USB-Drivers.zip/file" },
    { id: "drv-12", name: "MTP Fix Windows 11", ver: "Win 11 Fix", desc: "إصلاح ظهور الهاتف في وضع نقل الملفات MTP", link: "https://www.mediafire.com/file/6ezxozqj73vnear/fix_mtp_by_halabtech.zip/file" },
    { id: "drv-13", name: "Motorola Fastboot Driver", ver: "64-bit", desc: "تعريف هواتف موتورولا في وضع الفاست بوت", link: "https://www.mediafire.com/file/5u9kpffk8r5tb7t/Motorola_Mobile_Drivers_64bit.msi/file" },
    { id: "drv-14", name: "TSM Exynos Fix", ver: "v1.2", desc: "حزمة MSVC وإصلاحات تشغيل TSM للأكسينوس", link: "https://www.mediafire.com/folder/9wcn6zcmqbkyk/MicrosoftMSVC" },
    { id: "drv-15", name: "15 Second ADB Installer", ver: "v1.4.2", desc: "تثبيت سريع لنظام الـ ADB والفولدر العام", link: "https://www.mediafire.com/file/22ko126iuh42w21/15+Second+ADB+Installer+v1.4.2.zip/file" },
    { id: "drv-16", name: "Huawei ADB Driver", ver: "Latest", desc: "تعريف هواتف هواوي وضع ADB و HiSuite", link: "https://www.mediafire.com/file/o0x4xs2e6b4u846/latest_usb_driver_windows.zip/file" },
    { id: "drv-17", name: "Huawei QC Driver", ver: "Qualcomm", desc: "تعريف هواتف هواوي معالجات كوالكوم", link: "https://www.mediafire.com/file/mclznqmya1s5i8c/qualcomm_driver.zip" },
    { id: "drv-18", name: "Huawei CDC Driver", ver: "CDC", desc: "تعريف مودم وتصحيح هواوي CDC", link: "https://www.mediafire.com/file/wr9d19ctlmyqfcr/android_cdc_driver.zip" },
    { id: "drv-19", name: "Huawei VCOM Driver", ver: "VCOM", desc: "تعريف وضع VCOM لهواوي MTK", link: "https://www.mediafire.com/file/facdq2tkdiajrs9/android_vcom_driver.zip" },
    { id: "drv-20", name: "SPRD UNISOC CM2", ver: "v4.21.39", desc: "التعريف الرسمي المعتمد من دونقل CM2", link: "https://www.mediafire.com/file_premium/jy0yomuk3mg0ncf/SPRD_UNISOC_4.21.39.134_pass-1111_official_by_cm2.7z/file", pass: "1111" },
    { id: "drv-21", name: "SPRD NPI USB Driver", ver: "v1.4", desc: "تعريف المصنع NPI لمعالجات Spreadtrum", link: "https://www.mediafire.com/file_premium/ma7h9hc885no62b/SPRD_NPI_USBDriver_1.4.rar/file" }
  ],

  unlocking: [
    { id: "unl-1", name: "Global Unlocker", ver: "Premium", desc: "فك شفرة دولي مباشر لجميع الشبكات العالمية", link: "https://global-unlocker-pro.com/Download" },
    { id: "unl-2", name: "Tira Unlocker", ver: "Latest", desc: "فك شفرات يمن موبايل وسبأفون وشبكات أمريكا", link: "http://www.tiraunlocker.com" },
    { id: "unl-3", name: "Fast Unlocker Pro", ver: "v3.0", desc: "سريع ومضمون — يدعم آلاف الموديلات", link: "https://fast-unlocker-pro.com/" },
    { id: "unl-4", name: "Q-Unlocker", ver: "v2.5", desc: "حصري يمن موبايل 4G وتفعيل البيانات", link: "https://www.q-unlocker.com/" }
  ],

  firmware_sites: [
    { id: "fw-1", name: "Samsung (SamFW)", ver: "Official", desc: "أكبر قاعدة فلاشات سامسونج رسمية مجانية ومباشرة", link: "https://samfw.com/" },
    { id: "fw-2", name: "LG (LG ROM)", ver: "Official", desc: "فلاشات ورومات إل جي بصيغة KDZ الرسمية", link: "https://lgrom.com/" },
    { id: "fw-3", name: "Xiaomi (MiFirm)", ver: "MiFirm", desc: "رومات شاومي وريدمي وبوكو Fastboot و Recovery", link: "https://mifirm.net/" },
    { id: "fw-4", name: "Realme (RomProvider)", ver: "Official", desc: "فلاشات ريلمي الرسمية بصيغة OFP وتفليش SP Tool", link: "https://romprovider.com/firmware/realme/" },
    { id: "fw-5", name: "OnePlus Stock ROM", ver: "Official", desc: "فلاشات وان بلس ومستودع MSM Download Tool", link: "https://androidmtk.com/download-oneplus-stock-rom-for-all-models" },
    { id: "fw-6", name: "OPPO Firmware File", ver: "Official", desc: "فلاشات أوبو الرسمية بصيغة Scatter و OFP", link: "https://firmwarefile.com/category/oppo" },
    { id: "fw-7", name: "TracFone MediaFire", ver: "Official", desc: "مستودع رومات هواتف تراكفون الأمريكية", link: "https://www.mediafire.com/folder/2z9cmetgup90m/TrecFone_Firmware" },
    { id: "fw-8", name: "Vivo Stock ROM", ver: "Official", desc: "فلاشات فيفو الأصلية للتفليش وإصلاح الموت", link: "https://androidmtk.com/download-vivo-stock-rom" },
    { id: "fw-9", name: "Motorola Stock ROM", ver: "Official", desc: "فلاشات موتورولا Fastboot لجميع الموديلات", link: "https://androidmtk.com/download-motorola-stock-rom-for-all-models" },
    { id: "fw-10", name: "ZTE Stock ROM", ver: "Official", desc: "فلاشات زد تي إي وبليد الرسمية", link: "https://androidmtk.com/download-zte-stock-rom-for-all-models" },
    { id: "fw-11", name: "Itel Stock ROM", ver: "Official", desc: "فلاشات ايتل الرسمية لمعالجات SPD و MTK", link: "https://androidmtk.com/download-itel-stock-rom" },
    { id: "fw-12", name: "Honor Firmware File", ver: "Official", desc: "فلاشات هونر الأصلية لجميع المناطق والموديلات", link: "https://firmwarefile.com/category/honor/page/2" }
  ],

  iphone_tools: [
    { id: "iph-1", name: "3uTools V3.28", ver: "v3.28", desc: "النسخة المستقرة الموثوقة لتفليش وتخطي الآيفون", link: "https://www.mediafire.com/file/peba8a9wshyi1bb/3utools-3-28-012.7z/file" },
    { id: "iph-2", name: "3uTools Latest", ver: "v9.0.088", desc: "أحدث إصدار يدعم iOS الحديث وتخطي القيود", link: "https://www.mediafire.com/file/zruyfcl2aem7tjq/3utools-9-0-088.7z/file" },
    { id: "iph-3", name: "iTunes 12.13.9", ver: "64-bit", desc: "نسخة آيتونز معدلة ومتوافقة مع أدوات الجيلبريك", link: "https://www.mediafire.com/file/whfr41knzymf2n9/itunes-64-bit-12-13-9-1.exe/file" },
    { id: "iph-4", name: "Firmware Extractor", ver: "by Rasheed", desc: "استخراج أي بارتيشن من فلاشات السوفت وير", link: "https://drive.google.com/file/d/1WnxIdOCT1hxOWsHHPwBOx6upw_puCcKQ/view" },
    { id: "iph-5", name: "SIMUNLOCKER_ODIN", ver: "v1.1", desc: "أودين معدل لتفليش سامسونج وفك قيود الشبكة", link: "https://www.mediafire.com/file/ji1cgxb398up8lp/SIMUNLOCKER_ODIN1.1-V-1.rar/file" },
    { id: "iph-6", name: "SPD Upgrade Tool", ver: "R27.25.4601", desc: "أداة تفليش أجهزة Unisoc / SPD الرسمية", link: "https://www.mediafire.com/file/17wygio8opba6na/SPD_Upgrade_Tool_R27.25.4601.zip/file" },
    { id: "iph-7", name: "SPD Research Tool", ver: "R27.24.2301", desc: "أداة البحث والتفليش لسبريدترام", link: "https://www.mediafire.com/file/67lq7q43s7m56wz/SPD_Research_Tool_R27.24.2301.zip/file" },
    { id: "iph-8", name: "SPD Factory Tool", ver: "R27.25.4601", desc: "أداة المصنع لتفليش ومعالجة سبريدترام", link: "https://www.mediafire.com/file/rtoistsbxqttyr5/SPD_Factory_Tool_R27.25.4601.zip/file" }
  ],

  iphone_pwn: [
    { id: "pwn-1", name: "Magico Mango DFU V1 Firmware", ver: "Pass: 321", desc: "برمجة وتحديث قطعة MAGICO MANGO لإدخال DFU", link: "https://drive.google.com/drive/folders/1S3mxUolL46j6sP2s1KFE7cBs-UkUsPfL", pass: "321" },
    { id: "pwn-2", name: "RP2354A Firmware", ver: "Latest", desc: "فلاشة برمجة قطعة RP2354A لفك آيفون", link: "https://drive.google.com/file/d/1hfgqgmoZxF-zgrcAjMt9hy-gJ5mpawd5/view", video: "https://youtu.be/jAv0QW_ApGs" },
    { id: "pwn-3", name: "All-in-One PWN Tool", ver: "Pass: HITHAMMAX", desc: "برنامج شامل لتشغيل وضبط جميع قطع PWN", link: "https://drive.google.com/file/d/1BrnX0b3Ma5B0kZbvioWZ0502Fwgk4LXm/view", pass: "HITHAMMAX" }
  ],

  dump_brands: [
    { id: "allcall", name: "ALLCALL MAGIC", count: 2, color: "#f59e0b", icon: "🔥" },
    { id: "kxd", name: "KXD A07", count: 2, color: "#8b5cf6", icon: "📱" },
    { id: "hmd", name: "HMD", count: 1, color: "#06b6d4", icon: "📱" },
    { id: "benco", name: "BENCO", count: 2, color: "#22c55e", icon: "📱" },
    { id: "honor", name: "HONOR", count: 4, color: "#7c3aed", icon: "🔥" },
    { id: "hisorl", name: "HISORL", count: 1, color: "#f97316", icon: "📱" },
    { id: "blackview", name: "BLACKVIEW", count: 1, color: "#0891b2", icon: "📱" },
    { id: "huawei", name: "HUAWEI & HONOR", count: 5, color: "#dc2626", icon: "🗄️" },
    { id: "nokia", name: "NOKIA", count: 7, color: "#2563eb", icon: "📱" },
    { id: "infinix", name: "INFINIX", count: 4, color: "#00c950", icon: "🔥" },
    { id: "itel", name: "ITEL", count: 5, color: "#e7000b", icon: "📱" },
    { id: "mhorse", name: "M-HORSE", count: 7, color: "#6366f1", icon: "🔥" },
    { id: "oppo", name: "OPPO", count: 7, color: "#1a9e47", icon: "📱" },
    { id: "realme", name: "REALME", count: 7, color: "#ffcc00", icon: "📱" },
    { id: "samsung", name: "SAMSUNG SCATTER", count: 7, color: "#1428a0", icon: "📁" },
    { id: "xiaomi", name: "XIAOMI / REDMI / POCO", count: 9, color: "#ff6900", icon: "📱" },
    { id: "tecno", name: "TECNO (141)", count: 141, color: "#2563eb", icon: "📱" },
    { id: "lt", name: "LT MOBILE (9)", count: 9, color: "#10b981", icon: "📱" },
    { id: "vivo", name: "VIVO", count: 15, color: "#00b4ff", icon: "📱" },
    { id: "wiko", name: "WIKO", count: 1, color: "#ec4899", icon: "📱" },
    { id: "villaon", name: "VILLAON", count: 1, color: "#a855f7", icon: "📱" },
    { id: "tab", name: "TAB / YTAB", count: 3, color: "#14b8a6", icon: "📱" },
    { id: "zte", name: "ZTE", count: 1, color: "#db2777", icon: "🗄️" },
    { id: "motorola", name: "MOTOROLA", count: 2, color: "#0891b2", icon: "📱" },
    { id: "copy", name: "COPY", count: 4, color: "#6b7280", icon: "💾" },
    { id: "iphone_copy", name: "iPhone COPY", count: 1, color: "#000000", icon: "🍎" },
    { id: "other", name: "OTHER", count: 5, color: "#6b7280", icon: "💿" }
  ],

  dump_cards: {
    honor: [
      { id: "hnr-1", name: "HONOR 70 FNE-NX9 - Official", ver: "FNE-N29_def_meafnaf", desc: "Official FREE روم كامل", link: "https://drive.google.com/file/d/1sPDlg3-8j4OiL12Zh1DZNHF4Y5mHNjJd/view" },
      { id: "hnr-2", name: "X7a RKY-LX2 2GB [F64]", ver: "2GB Dump + NV", desc: "سحب Hossam Khairy مع ملفات الشبكة", link: "https://drive.google.com/file/d/1TiQ4y7sUK6cNxaUVT2tEcjgC3vjdlEr0/view" },
      { id: "hnr-3", name: "X9c FULL DUMP [Flash64]", ver: "MagicOS 8.0", desc: "أندرويد 14 مسحوب بوكس فلاش 64", link: "https://drive.google.com/file/d/1Kd5cp_IQeTI_6fzz0HmZVgHKT-DSZfL0/view" },
      { id: "hnr-4", name: "X7b 5G CLK-NX2 FRP [YMTC]", ver: "MagicOS 9.0", desc: "معالج Dimensity 6020 حماية حديثة", link: "https://www.mediafire.com/file/oqlqu315m5kutkh/" }
    ],
    hmd: [
      { id: "hmd-1", name: "HMD AURA TA-1631 (2 ROMs)", ver: "rck_116A + rck_1100", desc: "Official Stock ROMs أصلية", link: "https://drive.google.com/file/d/1hp-B3jh0q0tTGNYLxq8R4yWy4Y0W_3tw/view" }
    ],
    benco: [
      { id: "bnc-1", name: "Benco V60 Full [CM2]", ver: "CM2 Dump", desc: "سحب كامل ببوكس CM2", link: "https://drive.google.com/file/d/1IWj92n5541TYoYKXe-sC9eyNkbsrte6f/view" },
      { id: "bnc-2", name: "BENCO S1 Pro AE9260 DUAL", ver: "Pandora + CM2", desc: "دامبان كاملان باندورا + CM2", link: "https://drive.google.com/file/d/1Dx6I5z92KofjEru4xveT7SZ-TeQj7a_L/view" }
    ],
    nokia: [
      { id: "nok-1", name: "C12 TA-1583 (Pandora)", ver: "00WW_1_54B_SP01", desc: "دامب باندورا كامل ومختبر", link: "https://drive.google.com/file/d/1S9_2MsbRY3hfhFEnvHmdCERLWh0GxCSH/view" },
      { id: "nok-2", name: "C12 TA-1583 (CM2)", ver: "00WW_1_54B_SP01", desc: "دامب CM2 كامل مجرب", link: "https://drive.google.com/file/d/1S9_2MsbRY3hfhFEnvHmdCERLWh0GxCSH/view" },
      { id: "nok-3", name: "C10 TA-1342 SC7731E", ver: "Pandora", desc: "معالج سبريدترام SC7731E", link: "https://drive.google.com/file/d/1JJMRH_rQBuxHvy_f47Y4ejv3baLRiwfV/view" },
      { id: "nok-4", name: "5.3 TA-1234 00WW_2_290", ver: "Pandora", desc: "دامب باندورا نوكيا 5.3", link: "https://drive.google.com/file/d/1gmkObCQDILmhXNnmumBVeyCt69a5Mflr/view" },
      { id: "nok-5", name: "C1 2nd Edition TA-1380", ver: "SP7731E", desc: "روم نوكيا رسمي HMD Official", link: "https://mirrors-hmd-1.lolinet.com/firmware/hmd/2021/irisumts/official/600WW/HMDSW_iru-122H-0-00WW-B01-user_devicekit.zip" },
      { id: "nok-6", name: "TA-1114 COPY VERSION", ver: "Spreadtrum", desc: "نسخة كلاكيت ميراكل بوكس", link: "https://drive.usercontent.google.com/download?id=1_c708OPmAWhZW6Fudrl7TCXRkyyU_Scb" },
      { id: "nok-7", name: "G21 TA-1418", ver: "HalabTech", desc: "دامب حلب تك لإصلاح البوت", link: "https://drive.google.com/file/d/19folWxmv3vi1sqiWm_NfvmfRDhKR3Tb9/view" }
    ],
    infinix: [
      { id: "inf-1", name: "Smart 6 X6511B - Factory", ver: "X6511B-F6318", desc: "فلاشة مصنع موقعة Factory Signed", link: "https://drive.google.com/file/d/1LpISua-lTGlvea_P5oR9alxyEHTVuzcR/view" },
      { id: "inf-2", name: "Smart 20 X6840B FULL", ver: "16.1.0.150SP02", desc: "سحب أداة UnlockTool كامل", link: "https://drive.google.com/file/d/1AZywXmJEL1BBJaB3Cx5KF7iE7G3c2RqS/view" },
      { id: "inf-3", name: "NOTE 30 5G X6711 V600", ver: "X6711", desc: "سحب بوكس باندورا Pandora", link: "https://drive.google.com/file/d/1ubef2yjzrQpNB0MFPw8UWdraxPr6OtbB/view" },
      { id: "inf-4", name: "Smart 5 X657C Full+NV", ver: "X657C-H6117GH", desc: "دامب كامل مع ملفات الشبكة NVRAM", link: "https://drive.google.com/file/d/148UbsVqN_G7H2OsJlPH5-S6kGr3YfJ-C/view" }
    ],
    itel: [
      { id: "itl-1", name: "P37 P651W", ver: "F3116-10.0", desc: "UnlockTool + NVRAM لإصلاح السيريال", link: "https://drive.google.com/file/d/1-FOKgpMC-oVjuyVdIS2LNeMqcQvP704J/view" },
      { id: "itl-2", name: "A661L - A49 (A58 Pro)", ver: "Pandora", desc: "دامب بوكس باندورا لإحياء الجهاز", link: "https://www.terabox.app/arabic/sharing/link?surl=aylVN-8Y7P9jI6ye9JpsMQ" },
      { id: "itl-3", name: "A06 A669W 2GB [UnlockTool]", ver: "A669W-SA375A", desc: "نسخة 2 جيجا رام أنلوك تول", link: "https://drive.google.com/file/d/1KJX3Zv3JPcke4sWTE8ubE-3xPAevhNjO/view" },
      { id: "itl-4", name: "S23 S665LN (2 Parts)", ver: "F065-S-GL-V305", desc: "دامب باندورا كامل (يتطلب VPN أحياناً)", link: "https://www.terabox.app/arabic/sharing/link?surl=RMigbSPD9-7YafQPj0LlMQ" },
      { id: "itl-5", name: "L6503 Vision 2 (3 Tools)", ver: "L6503-F6315", desc: "CM2 + UnlockTool + Pandora", link: "https://drive.google.com/file/d/1cUD2DdoJUYqCZcQA4mMD0PqjKv2QLDwY/view" }
    ],
    mhorse: [
      { id: "mh-1", name: "POP 8 - 1GB [Pandora]", ver: "POP 8-M-HORSE-V01", desc: "دامب باندورا أصلي", link: "https://drive.google.com/file/d/11Ck6VqXy_UdagNjz6GvMiRg7JH2DQmuu/view" },
      { id: "mh-2", name: "H-HORSE M16 PRO MAX", ver: "SPD", desc: "معالج سبريدترام مع تجارب الباسورد", link: "https://drive.google.com/file/d/10tCf_9gERV7oN2ewDHyGG4Qt2evP4PE1/view" },
      { id: "mh-3", name: "INFINIX HOT 40 Pro [M-HORSE]", ver: "V01-V03", desc: "نسختان لمعالجة أجهزة الكوبي", link: "https://drive.google.com/file/d/1D1-GnB2U8msn6DINNQ7qSs2Q2DkPqZtD/view" },
      { id: "mh-4", name: "M-Horse C55 DOOGEE X96Pro", ver: "C55-M-HORSE-V02", desc: "CM2 + Pandora مسحوب", link: "https://drive.google.com/file/d/12sZU4xYmYaeZErGi3zLMN_eeQf_kx7MN/view" },
      { id: "mh-5", name: "HOT 40 Pro V03 Full", ver: "V03-20240807", desc: "UnlockTool دامب كامل", link: "https://drive.google.com/file/d/1D1-GnB2U8msn6DINNQ7qSs2Q2DkPqZtD/view" },
      { id: "mh-6", name: "HOT 30 V05 [UnlockTool]", ver: "HOT 30-M-HORSE-V05", desc: "سحب أنلوك تول أصلي", link: "https://drive.google.com/file/d/1tpgGTmlS8ZV_T6Pbd-5U58fXrLqV8i7T/view" },
      { id: "mh-7", name: "SPARK 10 Pro (3 VERSIONS)", ver: "V02/V05/V06", desc: "3 دامبات لجميع إصدارات الجهاز", link: "https://drive.google.com/file/d/1tkQijRTWEyWqmiBx-23aiY-NOIw061sr/view" }
    ],
    oppo: [
      { id: "opp-1", name: "A55 CPH2325 F.71 [Pandora]", ver: "CPH2325_11_F.71", desc: "4.7GB سحب كامل بوكس باندورا", link: "https://drive.google.com/file/d/1KsSxwMJRtAJoAGeTA7Uq4JHgzbe2GsMz/view" },
      { id: "opp-2", name: "CPH1933 A5 2020 [Pandora]", ver: "CPH1933_11_F.01", desc: "3GB دامب كوالكوم كامل", link: "https://drive.google.com/file/d/1xQjwapIINwF4rewMG38Sd7n1iltoqep2/view" },
      { id: "opp-3", name: "A31 CPH2015 128GB eMMC", ver: "Easy JTAG", desc: "2.4GB مسحوب إيزي جي تاج", link: "https://drive.google.com/file/d/1ZJ6o9C8jFB9MeRHdnB1N-AkeGtpaBu64/view" },
      { id: "opp-4", name: "A54 CPH2239 Dead Boot", ver: "CPH2239_11_C.33", desc: "UnlockTool + NV لإصلاح الموت المفاجئ", link: "https://drive.google.com/file/d/1-J8LMb2OzTHZXJl0M8Y4pE6A6uNrREg1/view" },
      { id: "opp-5", name: "A57 CPH2387 [Easy JTAG]", ver: "BIN DUMP", desc: "دامب بين هيدر إيزي جي تاج بلس", link: "https://drive.google.com/file/d/1iVZkaOdBacWxZEjxenBhqYJxldSBqN3i/view" },
      { id: "opp-6", name: "A6 PRO 5G CPH2781", ver: "CPH2781_11.A.31", desc: "F64 BOX دامب حديث", link: "https://drive.google.com/file/d/1cW5EhSPHntwe3W3tiDN651OpvXvf7gHJ/view" },
      { id: "opp-7", name: "RENO 12F 4G CPH2687", ver: "CPH2687", desc: "F64 BOX 8.52GB كامل", link: "https://drive.google.com/file/d/1OY4I_TmBJsEKNlUdHPULjpiLOEyQJuIc/view" }
    ],
    realme: [
      { id: "rlm-1", name: "C71 RMX5303 [Pandora]", ver: "export_15_C.09", desc: "7.4GB دامب باندورا كامل ومحدث", link: "https://drive.google.com/file/d/1xficluJ65Ny-Vlih9Ys0rBlWk6OKa9Jj/view" },
      { id: "rlm-2", name: "NOTE 60X RMX3938", ver: "F64 BOX", desc: "64GB eMMC سحب بوكس فلاش 64", link: "https://drive.google.com/file/d/1pcICRDgQ1ZbFP0sCF0aG6wEPSksEBdln/view" },
      { id: "rlm-3", name: "10 PRO 5G RMX3661", ver: "F64 BOX", desc: "256GB UFS دامب ذاكرة يو إف إس", link: "https://drive.google.com/file/d/1a6XXCbruh394KhIMOGDwhmnzZADaSuMV/view" },
      { id: "rlm-4", name: "C35 RMX3511 XML 128GB", ver: "Easy JTAG", desc: "سحب Thamer Zarouki لإصلاح البوت", link: "https://drive.google.com/file/d/1YBVx9kAU2yXncW-sc54NZrnHVbCOLVE9/view" },
      { id: "rlm-5", name: "C35 RMX3511 A.55", ver: "Pandora", desc: "دامب باندورا كامل", link: "https://drive.google.com/file/d/1L6PYGzOfBmmgazHS7KT-ouc3INAU0cl7/view" },
      { id: "rlm-6", name: "Note 50 RMX3834 A.89", ver: "Pandora", desc: "سحب عبد الله غانم", link: "https://drive.google.com/file/d/10uJP9wiJkrBzGRQIwfjOVcjpCYhAJWoJ/view" },
      { id: "rlm-7", name: "REALME C67 COPY", ver: "Pandora", desc: "1.1GB نسخة الكوبي", link: "https://drive.google.com/file/d/1ZFf5jTLPsXjOXU48yb5C_rwmLTiX8BOx/view" }
    ],
    samsung: [
      { id: "sam-1", name: "SM-A146U1 Revive Dump", ver: "A146U1UEUDEYF5", desc: "إحياء سامسونج A14 أمريكي تحديث يوليو", link: "https://www.mediafire.com/file_premium/hos3d6lm6b4fsem/" },
      { id: "sam-2", name: "A075FXXU1AYG6", ver: "A075FXXU1AYG6", desc: "طريقة وسحب TSM Method", link: "https://mega.nz/file/qlRy2I4S#-6N_7i99hCGswx5ZwScoTILzk3k2Pn1gBEUrB-sVQ-0" },
      { id: "sam-3", name: "A07 4G SM-A075F Android 16", ver: "A075FXXS6CZF6", desc: "UnlockTool أحدث حماية", link: "https://drive.google.com/file/d/1YCwzU2B9XZlQK-A-zDNhbLpWpWxwFnAP/view" },
      { id: "sam-4", name: "X216b XXUD XML", ver: "Abdullah Ghanem", desc: "أحدث حماية مسحوبة بصيغة XML", link: "https://drive.usercontent.google.com/open?id=17G7p16ZkVWq_qllLn_of3zg3L-L_83wh" },
      { id: "sam-5", name: "A12 SM-A125F", ver: "A125FXXS6CXJ1", desc: "Easy JTAG 1.5GB لإصلاح الذاكرة", link: "https://drive.google.com/file/d/1RegTQJUux_RdrozEtt9eFR2bmECEnFq3/view" },
      { id: "sam-6", name: "A25 5G SM-A256E", ver: "A256EXXS8CYG3", desc: "F64 ULTRA 4.5GB إكسينوس حديث", link: "https://drive.google.com/file/d/1Tw19y4kZPm8mHaO0raheL4nIfp3_HUv2/view" },
      { id: "sam-7", name: "Tab A9 SM-X110", ver: "X110XXS6CYI3", desc: "سحب أداة أنلوك تول كامل", link: "https://drive.google.com/file/d/199DEolDruK6iP3oh6iGJ9XkOJWJsDqil/view" }
    ],
    xiaomi: [
      { id: "mi-1", name: "REDMI 9C M2006C3MG", ver: "3GB Easy JTAG", desc: "Easy JTAG Plus سحب الذاكرة", link: "https://drive.google.com/file/d/1YxY9QvJq62wAR88VcZSIrlh6q0BMx9Ui/view" },
      { id: "mi-2", name: "Redmi Note 14 5G Beryl XML", ver: "6.5GB Easy JTAG", desc: "XML Dump كامل لإصلاح البوت", link: "https://drive.google.com/file/d/1zxRGj8wgYfsDQaVfn7RB53Xw78JmCToF/view" },
      { id: "mi-3", name: "REDMI A3 C61", ver: "16.V816.0.7.0", desc: "F64 ULTRA 3.6GB أندرويد حديث", link: "https://drive.google.com/file/d/1R-6hqUPVx5k5Y5l5Umws2-f0fXZNKOHi/view" },
      { id: "mi-4", name: "REDMI 10A 220233L2G", ver: "V12.5.3.0.RCZMIXM", desc: "F64 ULTRA 2.5GB", link: "https://drive.google.com/file/d/1ApV1GSSHo74SnIgm7rQEYxrmx673uoTP" },
      { id: "mi-5", name: "REDMI 15C / POCO C85", ver: "OS2.0.221.0.VBNMIXM", desc: "F64 256GB 7.4GB", link: "https://drive.google.com/file/d/1ztxrctjJJLCoQq6a0ka7FWm_SRal1hwz/view" },
      { id: "mi-6", name: "Redmi A3x missi Android 16", ver: "AMT Tool", desc: "4.5GB AMT Tool", link: "https://drive.google.com/file/d/1Xxx7HG60lnaXQft27RdCmvzresdbppBb/view" },
      { id: "mi-7", name: "POCO C75 / Redmi 14C / 17C", ver: "Flash64 Ultra", desc: "1GB Dump للإحياء السريع", link: "https://drive.google.com/file/d/1Ki8JkDYwOBdPhDm7OWcGv7s5wvY-fYPj/view" },
      { id: "mi-8", name: "POCO C65 256GB", ver: "F64 ULTRA", desc: "MAY.1 2025 7GB", link: "https://drive.google.com/file/d/1nT9Eb1NtNSxodYzYSPBqVcynvQqNwbdO/view" },
      { id: "mi-9", name: "Redmi 13C Gale", ver: "OS2.0.6.0.VGPMIXM", desc: "Pandora — يتطلب VPN للتحميل", link: "https://www.terabox.app/arabic/sharing/link?surl=h5bhksix3MWtLXRftpknUQ" }
    ],
    vivo: [
      { id: "viv-1", name: "Y21D PD2510F", ver: "256GB UFS 8.2GB", desc: "F64 ULTRA دامب كامل", link: "https://drive.google.com/file/d/18qzexyLM46cv_rsa9f04tvKZceTJjbJ2/view" },
      { id: "viv-2", name: "Y03T PD2360F", ver: "64GB eMMC 4.9GB", desc: "F64 ULTRA", link: "https://drive.google.com/file/d/1S6oZd5TGZHOfT8Yt6QgeQoYKQ8gAuYJr/view" },
      { id: "viv-3", name: "Y18 PD2327F", ver: "128GB eMMC 4.4GB", desc: "F64 ULTRA", link: "https://drive.google.com/file/d/1a0oOV43ud0t9L149BD1pKRj1MK4LAGGH/view" },
      { id: "viv-4", name: "Y22S PD2228F", ver: "128GB UFS", desc: "F64 BOX دامب ذاكرة", link: "https://drive.google.com/file/d/1myQP49q9I-RuOFciiCwt93pVjC50bLCC/view" },
      { id: "viv-5", name: "Y20S[G] Y12S FAKE 8+256GB", ver: "EX_A_10.5.2", desc: "Fixed Dump لإصلاح الجهاز المزيف", link: "https://drive.google.com/file/d/1-Umiavto0B6I3f2sRai9Qaci2k7PfRWj/view" },
      { id: "viv-6", name: "Y12S V2026 / PD2036F", ver: "EX_A_11.0.8", desc: "Full Dump أصلي", link: "https://drive.google.com/file/d/1Bbk56EkNG0Mxt5v6_h0jmNmWQbg-6uw-/view" },
      { id: "viv-7", name: "Y100 V2239 / PD2257F", ver: "EX_A_13.0.5.3.W30", desc: "UFS Dump مسحوب بدقة", link: "https://drive.google.com/file/d/1euPnx7zmh9Q9p_aZpualyyw7ciF5AeFw/view" },
      { id: "viv-8", name: "Y53S V2058 / PD2103F", ver: "EX_A_1.8.1", desc: "Preloader + Dump كامل", link: "https://drive.google.com/file/d/12j9rGKlKl3a9L-LCbJmBB0AWALy_t0da/view" },
      { id: "viv-9", name: "Y75A PD2142F", ver: "EX_A_12.0.16", desc: "UFS Dump كامل", link: "https://drive.google.com/file/d/1-XxEgR5FRyYhNYjQAT2of0ZGewvlNf2e/view" },
      { id: "viv-10", name: "Y21 PD2139F", ver: "EX_A_6.25.6", desc: "EMMC Dump", link: "https://drive.google.com/file/d/1qpax6D1yamapS6ZlA7i52MXMm6pWENZU/view" },
      { id: "viv-11", name: "V27E V2237", ver: "EX_A_13.0.8.1", desc: "Full UFS Dump", link: "https://drive.google.com/file/d/1sJdYeZPWctAnfDScxbiDBuKzv4RPGLGO/view" },
      { id: "viv-12", name: "Y02s V2203 / PD2216F", ver: "EX_A_12.0.32.0.W20", desc: "EMMC Dump مجرب", link: "https://drive.google.com/file/d/1Vv3DXV2CS0XtBpYtSCUt-iA8ZlO6YcHh/view" },
      { id: "viv-13", name: "Y15s PD2140F (2 Versions)", ver: "EX_A_6.37.2 / 6.45.5", desc: "UnlockTool مسحوب", link: "https://drive.google.com/file/d/1CCH-oDVN-Erjh1O0o3sEZcnH4QWQX-Mc/view" },
      { id: "viv-14", name: "Y1s PD2014F", ver: "EX_A_1.13.50", desc: "EMMC Dump", link: "https://drive.google.com/file/d/1p5SiaGVwU0LFGmYZ6dgyfJyV8aZwkA88/view" },
      { id: "viv-15", name: "Y83 PD1803BF", ver: "EX_A_9.9.9", desc: "Old Fix Dump إصدار قديم", link: "https://drive.google.com/file/d/1kzAc42uBYlwxW2F308aGFU4NJtoDc1c_/view" }
    ],
    tab: [
      { id: "tab-1", name: "YTAB ULTRA 35", ver: "CM2 3GB", desc: "سحب Prince Cazanova", link: "https://drive.google.com/file/d/1zplMZgC3PUa_MP0F5BOtosQejZaom4dZ/view" },
      { id: "tab-2", name: "TAB A9 SM-X110", ver: "UnlockTool", desc: "Samsung Tab الأصلي", link: "https://drive.google.com/file/d/199DEolDruK6iP3oh6iGJ9XkOJWJsDqil/view" },
      { id: "tab-3", name: "Oteeto TAB 15", ver: "CM2 Rare", desc: "تاب صيني نادر جداً", link: "https://drive.google.com/file/d/19RaJLb3dnlcj3Wj9hdkg8I4aL-tUuHQY/view" }
    ],
    motorola: [
      { id: "mot-1", name: "Moto E15 5G XT2523-7", ver: "AMT Tool 2.9GB", desc: "Full Dump أندرويد حديث", link: "https://drive.google.com/file/d/16E-6KmWMco6QT-t-H3Mhk5xCCS6j8urw/view" },
      { id: "mot-2", name: "Moto E13 XT2345-4", ver: "Pandora", desc: "دامب باندورا كامل ومختبر", link: "https://drive.google.com/file/d/101c8ovGsl5Mfg1UrkPRZv9L9OYZUKBg6/view" }
    ],
    copy: [
      { id: "cpy-1", name: "S26 ULTRA COPY SAMBA65S", ver: "Pandora", desc: "IPRO SAMBA65S جهاز مقلد", link: "https://drive.google.com/file/d/1alw0UC9SxIJW9IsHQnXOP9Uvl8xYEAjU/view" },
      { id: "cpy-2", name: "iPhone 17 Pro Copy DS-BD2", ver: "CM2", desc: "DCODE DS-BD2 أندرويد بهيئة آيفون", link: "https://drive.google.com/file/d/1HNXlgyu8pInqB2RLvFQNmaHks8pA7v8-/edit" },
      { id: "cpy-3", name: "S26 Ultra COPY MT6580", ver: "CM2", desc: "معالج قديم Fake Detected", link: "https://drive.google.com/file/d/1imGiG3ca2omwJBxJQWsYl2w0SAObQAhl/view" },
      { id: "cpy-4", name: "REALME C67 COPY Pandora", ver: "Pandora", desc: "1.1GB سحب باندورا", link: "https://drive.google.com/file/d/1ZFf5jTLPsXjOXU48yb5C_rwmLTiX8BOx/view" }
    ],
    iphone_copy: [
      { id: "ip-cpy-1", name: "iPhone 16 Pro Max Copy", ver: "Pandora 1.4GB", desc: "معالج MT6735 سوفت وير أندرويد", link: "https://drive.google.com/file/d/1SOhno0YtFUzYGauWnXrr7GIimY6QLHuk/view" }
    ],
    other: [
      { id: "oth-1", name: "RAVOZ V7", ver: "Pandora 3.5GB", desc: "أندرويد 14 أصلي", link: "https://drive.google.com/file/d/1qcGLeJIGgmwKVTHa-sdvUyuIYeZAv5dc/view" },
      { id: "oth-2", name: "LENOVO TB-7305X", ver: "Scatter", desc: "تفليش SP Flash Tool", link: "https://drive.google.com/file/d/1B5VzL2H1A51NQ33_H6C8vDywObFolbz7/view" },
      { id: "oth-3", name: "BLU T5 TIGO T0050TT", ver: "CM2", desc: "يتطلب سايفون VPN للتحميل", link: "https://www.terabox.app/arabic/sharing/link?surl=TLasYwRnDISWcAK9WLzB3Q" },
      { id: "oth-4", name: "LAVA Iris 59 LE9930", ver: "Pandora", desc: "دامب لافا أصلي", link: "https://www.terabox.app/arabic/sharing/link?surl=-okpAZRO3RAKy-8YIrP7sQ" },
      { id: "oth-5", name: "WALTON NEXG N72", ver: "Pandora", desc: "Full + NV دامب كامل", link: "https://www.terabox.app/arabic/sharing/link?surl=UfydmqOdzA2ciqvCRFF_9A" }
    ],
    wiko: [
      { id: "wik-1", name: "WIKO T10 FULL DUMP", ver: "W-V673-V01.57", desc: "UnlockTool مسحوب", link: "https://drive.google.com/file/d/1HGMTtBPH4TNYXIusU4G1ZO3scGphM7cq/view" }
    ],
    villaon: [
      { id: "vil-1", name: "VILLAON V20 FULL DUMP", ver: "W-V673-V01.57", desc: "UnlockTool دامب أصلي", link: "https://drive.google.com/file/d/10EaY1ggOVvB2Yrgf7BZYSqMcu23fIB7I/view" }
    ],
    zte: [
      { id: "zte-1", name: "BLADE V70 MAX Z2467", ver: "MyOS15.0.3", desc: "6.1GB UnlockTool", link: "https://drive.google.com/file/d/1FYp9WGh_4o7ycHVaQzC1iB6s_LNjByGr/view" }
    ],
    allcall: [
      { id: "alc-1", name: "Hero 60 Max (RARE)", ver: "UnlockTool", desc: "دامب نادر جداً معالج ميديا تيك", link: "https://drive.google.com/file/d/1EsPIC9Wp1h0vWDRA1Gi6k-obUHYGkEqu/view" },
      { id: "alc-2", name: "AllCall Magic 60", ver: "EG_AOS14.0_28.05.2025", desc: "Pandora أصلي", link: "https://drive.google.com/file/d/16LeQjY7x-slLFuftE9DVFrtBdvmfCvqx/view" }
    ],
    blackview: [
      { id: "blk-1", name: "Blackview A55", ver: "A55_V1.0_20250523", desc: "UnlockTool 1.7GB", link: "https://drive.google.com/file/d/18xsJ8qLtParycTU0qx6KcGO1eabb5Rws/view" }
    ],
    hisorl: [
      { id: "his-1", name: "HISORL T901", ver: "UnlockTool", desc: "Full Dump كامل", link: "https://drive.google.com/file/d/1IQMjflRd0asfRQl3_z2PaCu6FeAxvzyO/view" }
    ],
    huawei: [
      { id: "hua-1", name: "HUAWEI Y7A PPA-LX2", ver: "Easy JTAG", desc: "Easy JTAG Plus لإصلاح البوت", link: "https://drive.google.com/file/d/1R5Rku8E4MN3t4miBfgGLIcVxqPVYX6iP/view" },
      { id: "hua-2", name: "X7B CLK-LX2 C185", ver: "UnlockTool", desc: "Honor X7B معالج حديث", link: "https://drive.google.com/file/d/1C2dhyqDx6WA7gb3VXcaYwG4PTQ5NweRM/view" },
      { id: "hua-3", name: "HONOR 400 ABR-N03", ver: "F64 ULTRA", desc: "OSv15 Full Dump كامل", link: "https://drive.google.com/file/d/1beAVNfe4wY31rb8xfjz41hVWOxX7npqn/view" },
      { id: "hua-4", name: "Honor 50 Lite NTN-L22", ver: "UnlockTool", desc: "New Region C185", link: "https://drive.google.com/file/d/1V977zxhIp-2bDbiaDWD07wTrKyRiU11Z/view" },
      { id: "hua-5", name: "X7A RKY-LX2 UFI", ver: "UFI Box", desc: "Pass: Melok@AbouAmr", link: "https://www.mediafire.com/file/ldl8120aynxzlhx/honor_x7a_RKY-LX2_full_dump_by_UFI.rar/file", pass: "Melok@AbouAmr" }
    ],
    kxd: [
      { id: "kxd-1", name: "KXD A07 Android 13", ver: "A07_KXD_A13_V1.263", desc: "Pandora 3GB", link: "https://drive.google.com/file/d/1SqGxl0jvG9OYeE-A0zXnJusk2kTS7xGB/view" },
      { id: "kxd-2", name: "KXD A07 Android 12", ver: "A07_KXD_V1.03", desc: "Pandora 2.2GB", link: "https://drive.google.com/file/d/1hOfF0HqTxCH0NclxiK2eJsg4uS7XPVTb/view" }
    ],
    lt: LT_PHONES_CATALOG,
    tecno: TECNO_MODELS
  } as Record<string, ItemData[]>,

  halabtech: [
    { id: "hlb-1", name: "فلاشات ورومات رسمية", ver: "Firmware", desc: "سحب وطلب أي ملف رسمي — 3$", link: "https://t.me/hithamMax" },
    { id: "hlb-2", name: "قسم تعريب أنظمة", ver: "Translation", desc: "ملفات تعريب رسمية لهواتف سامسونج وLG", link: "https://t.me/hithamMax" },
    { id: "hlb-3", name: "تخطي وحمايات FRP & Dump", ver: "Security", desc: "ملفات حمايات متقدمة وبوت لودر", link: "https://t.me/hithamMax" },
    { id: "hlb-4", name: "طلب ملف حلب تك", ver: "3 دولار", desc: "سحب فوري لأي ملف من سبورت حلب تك", link: "https://t.me/hithamMax" },
    { id: "hlb-5", name: "ملفات مجانية حلب تك", ver: "Free Files", desc: "ملفات واتساب، وحلول شاومي مجاناً", link: "https://t.me/haithamMax1" },
    { id: "hlb-6", name: "SM-T387V U3 (Arabic)", ver: "Translation", desc: "تعريب تاب سامسونج T387V حماية U3", link: "https://www.mediafire.com/file/cfqitvgt28yi089/Setup_New_Translation_Language_HalabTech.rar/file" },
    { id: "hlb-7", name: "T377R4 7.0 Arabic Turkey", ver: "Pass: HOSAM", desc: "تعريب T377R4 أندرويد 7", link: "https://drive.google.com/file/d/1Ws6OmwXHWFtwyE2r2iRYos2hLp2SqDjN/view", pass: "HOSAM" }
  ],

  offers_hitham: [
    { id: "off-1", name: "ChatGPT Plus — 1 شهر", ver: "$9.91", desc: "حساب تجريبي مستقر + 2FA", link: "https://t.me/hithamMax" },
    { id: "off-2", name: "ChatGPT Plus Level 30D", ver: "$9.91", desc: "Apple Pay Vietnam — ضمان واستقرار", link: "https://t.me/hithamMax" },
    { id: "off-3", name: "ChatGPT Plus ApplePay 30D", ver: "$9.91", desc: "Super Durable فائق الاستقرار", link: "https://t.me/hithamMax" },
    { id: "off-4", name: "ChatGPT Plus ApplePay 1M", ver: "$8.77", desc: "ضمان 24 ساعة وتفعيل فوري", link: "https://t.me/hithamMax" },
    { id: "off-5", name: "Netflix Premium 4K — شهر", ver: "$3.50", desc: "4K UHD + بروفايل خاص برمز قفل", link: "https://t.me/hithamMax" },
    { id: "off-6", name: "CapCut Pro — شهر", ver: "حسب الطلب", desc: "ضمان كامل للمونتاج وصناع المحتوى", link: "https://t.me/hithamMax" },
    { id: "off-7", name: "CapCut Pro — 3 أشهر", ver: "حسب الطلب", desc: "ضمان 3 أشهر مستقر", link: "https://t.me/hithamMax" },
    { id: "off-8", name: "CapCut Pro — 6 أشهر", ver: "حسب الطلب", desc: "ضمان 6 أشهر", link: "https://t.me/hithamMax" },
    { id: "off-9", name: "CapCut Pro — سنة", ver: "حسب الطلب", desc: "ضمان سنة كاملة", link: "https://t.me/hithamMax" },
    { id: "off-10", name: "Canva Pro — سنة", ver: "$8", desc: "مقعد رسمي على إيميلك الشخصي", link: "https://t.me/hithamMax" },
    { id: "off-11", name: "YouTube Premium — 6 أشهر", ver: "$11", desc: "ترقية خلال 5 ثوانٍ بدون إعلانات", link: "https://t.me/hithamMax" },
    { id: "off-12", name: "YouTube Premium — 12 شهر", ver: "$25", desc: "حساب مخصص مستقر سنة كاملة", link: "https://t.me/hithamMax" },
    { id: "off-13", name: "Cursor Pro — 200/day", ver: "$18", desc: "200 نقطة ذكاء اصطناعي يومياً", link: "https://t.me/hithamMax" },
    { id: "off-14", name: "Cursor Pro — 2600", ver: "$15", desc: "2600 نقطة برمجة", link: "https://t.me/hithamMax" },
    { id: "off-15", name: "Cursor Pro — 6500", ver: "$18", desc: "6500 نقطة للمطورين", link: "https://t.me/hithamMax" },
    { id: "off-16", name: "Lovable AI PRO — شهر", ver: "$20", desc: "اشتراك PRO الرسمي لتطوير التطبيقات", link: "https://t.me/hithamMax" },
    { id: "off-17", name: "Lovable Pro Lite — سنة", ver: "$10", desc: "300 نقطة بناء مواقع", link: "https://t.me/hithamMax" },
    { id: "off-18", name: "Figma Pro Education — سنة", ver: "$11", desc: "3000 نقطة شهرياً وتصميم كامل", link: "https://t.me/hithamMax" },
    { id: "off-19", name: "Leonardo AI — 8,500", ver: "$5", desc: "8,500 نقطة لتوليد الصور", link: "https://t.me/hithamMax" },
    { id: "off-20", name: "Grok Super — 1 شهر", ver: "$18", desc: "إيميل + باسورد وصول كامل لـ Grok 3", link: "https://t.me/hithamMax" },
    { id: "off-21", name: "Grok Super — 3 أشهر", ver: "$26", desc: "ضمان 3 أشهر مستقر", link: "https://t.me/hithamMax" },
    { id: "off-22", name: "Grok Super — 6 أشهر", ver: "$40", desc: "ضمان 6 أشهر", link: "https://t.me/hithamMax" },
    { id: "off-23", name: "Grok Super — 12 شهر", ver: "$75", desc: "ضمان سنة كاملة", link: "https://t.me/hithamMax" },
    { id: "off-24", name: "SUNO PRO — شهر", ver: "$12", desc: "2500 نقطة لتوليد الموسيقى", link: "https://t.me/hithamMax" },
    { id: "off-25", name: "Elevenlabs Creator 131K", ver: "$12", desc: "131,000 حرف لتوليد الأصوات الواقعية", link: "https://t.me/hithamMax" },
    { id: "off-26", name: "Kling Ultra 27.5K — شهر", ver: "$85", desc: "27,500 نقطة لتوليد الفيديو الاحترافي", link: "https://t.me/hithamMax" }
  ],

  paid_offers: [
    { id: "vip-1", name: "جمناي برو + 5 تيرا مساحة", ver: "18 شهر - $10", desc: "عرض هيثم ماكس الحصري — تفعيل فوري", link: "https://t.me/hithamMax" },
    { id: "vip-2", name: "حسابات آيكلاود جاهزة ومفعلة", ver: "$3 USDT / 20 دينار", desc: "مفعل رسمي مع الإيميل وضمان", link: "https://t.me/hithamMax" },
    { id: "vip-3", name: "سيرفرات وتفعيل بوكسات فوري", ver: "تواصل", desc: "شحن رصيد وتفعيل فوري 24/7", link: "https://t.me/hithamMax" },
    { id: "vip-4", name: "حسابات وساعات دنقل مدفوعة", ver: "تواصل", desc: "تفعيل أوقات عمل لجميع الدنقلات", link: "https://t.me/hithamMax" }
  ],

  ai_offers: [
    { id: "ai-1", name: "GEMINI PRO 12 شهر", ver: "Gemini", desc: "مقعد رسمي مع سعة تخزين سحابية ضخمة", link: "https://t.me/hithamMax" },
    { id: "ai-2", name: "GEMINI PRO 18 شهر", ver: "Gemini", desc: "أقوى عرض لجمناي برو مدة 18 شهراً", link: "https://t.me/hithamMax" },
    { id: "ai-3", name: "GPT PLUS شهر", ver: "GPT", desc: "حساب مستقر ومفعل بضمان كامل", link: "https://t.me/hithamMax" },
    { id: "ai-4", name: "GPT GO سنة", ver: "GPT", desc: "حساب سنوي مستقر للأعمال والطلاب", link: "https://t.me/hithamMax" }
  ],

  free_tools: [
    { id: "fr-1", name: "Server 1 Mega Repository", ver: "Mega", desc: "ملفات سيرفر فلاشات ومخططات صيانة", link: "https://mega.nz/folder/JpJmnaKK#0CkdhqlqyuBPqWZqPSbTVA" },
    { id: "fr-2", name: "IDM Tool V1.5", ver: "v1.5", desc: "Freezer + Activator لبرنامج التحميل دون توقف", link: "https://www.mediafire.com/file/mqzcpgbzcy8k7hg/IDM_Tool_V1.5.rar/file" },
    { id: "fr-3", name: "أداة فك حظر واتساب", ver: "Latest", desc: "أداة فك الحظر المؤقت والدائم للأرقام", link: "https://mega.nz/file/VRM00TgD#cu0R1eaDrzeGlz0Mn-AsXIcQGsA0CtrsYIZhltb-9ag" },
    { id: "fr-4", name: "App Manager Tool", ver: "v1.2", desc: "إدارة ونقل تطبيقات الهاتف عبر الكمبيوتر", link: "https://www.mediafire.com/file/pqrfqni4gb3j98y/AppManager.exe/file" },
    { id: "fr-5", name: "Network Control V2", ver: "v2.0", desc: "التحكم في منافذ وشبكات الكمبيوتر والراوتر", link: "https://www.mediafire.com/file/uuy8x5k128vvbak/Ultimate-Network-Control-V2-2.0.zip/file" },
    { id: "fr-6", name: "SamFW Tool", ver: "v6.0.1", desc: "أشهر أداة مجانية لتخطي FRP بنقرة واحدة وتغيير CSC", link: "https://samfw.com/SamFwToolSetup_v6.0.1.zip" },
    { id: "fr-7", name: "MaxTech VIP", ver: "v2.0", desc: "تعريب هواتف سامسونج وإل جي بنقرة واحدة", link: "https://mega.nz/file/XLRlVRDL#VwmnEJdpTDSB_TFEjA6YGdDJ8k6dgafs6ANgFTj3FW0" },
    { id: "fr-8", name: "نقل هاتف EaseUS MobiMover", ver: "6.2.3", desc: "نقل كامل للبيانات والصور بين أندرويد وآيفون", link: "https://www.mediafire.com/file/ixrm0wgzm2zx64u/EaseUS.MobiMover.6.2.3.25122.rar/file" },
    { id: "fr-9", name: "سايفون VPN Psiphon", ver: "Latest", desc: "تجاوز حظر مواقع التحميل وسيرفرات تيرا بوكس", link: "https://www.mediafire.com/file/e75qx3oap8c70fc/VPN-Psiphon.rar/file" },
    { id: "fr-10", name: "Defender Control", ver: "v2.1", desc: "إيقاف حماية Windows Defender لتشغيل الكراكات", link: "https://www.mediafire.com/file_premium/r2jmxq0ps0ymq66/Defender_Control_v2.1.zip/file" },
    { id: "fr-11", name: "Activator Master Windows", ver: "v8.0 Pass: Morocco", desc: "تفعيل جميع إصدارات ويندوز وأوفيس بنقرة واحدة", link: "https://www.mediafire.com/file/7n00k39c4du7cvz/0_Activator_Master_v8.0_%2528Pass%253DMorocco%2529.zip/file", pass: "Morocco" },
    { id: "fr-12", name: "Mysterious-Dev Tool", ver: "v2025", desc: "أداة صيانة شاملة تدعم معالجات متعددة", link: "https://mysterious-dev.com/download.html" },
    { id: "fr-13", name: "Honor Fastboot Reader", ver: "v2", desc: "قراءة معلومات وموديل وبوت هواتف هونر", link: "https://www.mediafire.com/file/8voavhswgbnz6dn/FastbootReader_2.zip/file" },
    { id: "fr-14", name: "Acronis True Image", ver: "2021 Pass: @software_application", desc: "نسخ احتياطي واستعادة كاملة لقرص الويندوز", link: "https://t.me/haithamMax1/1005", pass: "@software_application" },
    { id: "fr-15", name: "3uRecorder Screen", ver: "Latest", desc: "تصوير شاشة الهاتف والكمبيوتر بجودة عالية 60FPS", link: "https://www.mediafire.com/file/f6cv7heduztxjcv/3uRecorder.zip/file" }
  ],

  gifts: [
    { id: "gft-1", name: "عرض شاشة الآيفون على الكمبيوتر", ver: "بدون كابل", desc: "بث شاشة الآيفون بجودة فائقة بدون أسلاك", link: "https://youtu.be/Y3spa6koDnI" },
    { id: "gft-2", name: "3uRecorder — تصوير الشاشة", ver: "Best Tool", desc: "برنامج خفيف واحترافي بدون علامة مائية", link: "https://www.mediafire.com/file/f6cv7heduztxjcv/3uRecorder.zip/file" },
    { id: "gft-3", name: "أداة تخطي الآيكلاود A5", ver: "Pass: 1988", desc: "تخطي آيكلاود أجهزة A5 القديمة بدون جيلبريك", link: "https://t.me/gaddtech/1572", pass: "1988" },
    { id: "gft-4", name: "قنوات كأس العالم والرياضة للآيفون", ver: "Code: 22455", desc: "تطبيق Vozi Pro مع كود التفعيل المباشر", link: "https://apps.apple.com/us/app/vozi-pro/id6779024508" },
    { id: "gft-5", name: "Adobe Creative Cloud", ver: "4 أشهر مجاناً", desc: "طريقة الحصول على اشتراك أدوبي الرسمي فيزا 0$", link: "https://commerce.adobe.com/store/checkout" },
    { id: "gft-6", name: "FRP SAMSUNG EXYNOS 2026", ver: "Free Tool", desc: "أداة تخطي حساب جوجل لمعالجات إكسينوس مجاناً", link: "https://www.mediafire.com/file/szt3rhif4sac9yc/FrpSamsung_2026.zip/file" },
    { id: "gft-7", name: "بوت كاشف الأرقام اليمني", ver: "Free Bot", desc: "معرفة صاحب الرقم اليمني وشبكة الاتصال", link: "https://t.me/Yemennumber_bot" },
    { id: "gft-8", name: "FMI OFF — Open Menu 2026", ver: "Generation 2026", desc: "إيقاف البحث عن الآيفون من القائمة المفتوحة", link: "https://fmip.indofind.my.id/2026/" },
    { id: "gft-9", name: "تخطي الآيفون iOS 9 - 27.x", ver: "Free Bypass", desc: "أداة تسجيل سيريال مجاناً وتجاوز شاشة الترحيب", link: "https://mega.nz/folder/zcJyzKJB#Xnw5ZTRM_U-Yv0VdpJUkLQ" }
  ],

  services: [
    { id: "srv-1", name: "فك شفرات الهواتف عن بعد", ver: "24/7 Remote", desc: "عبر برنامج TeamViewer أو AnyDesk بنقرة واحدة", link: "https://t.me/hithamMax" },
    { id: "srv-2", name: "إصلاح مشاكل البوت والموت المفاجئ", ver: "Remote JTAG", desc: "إحياء الهواتف المعلقة والميتة عبر البورتات", link: "https://t.me/hithamMax" },
    { id: "srv-3", name: "تفعيل البوكسات والدنقلات فوري", ver: "Instant Activation", desc: "تفعيل فوري لدنقل DFT, UnlockTool, Pandora, TSM", link: "https://t.me/hithamMax" },
    { id: "srv-4", name: "سحب وطلب أي فلاشة غير متوفرة", ver: "Custom Dump", desc: "طلب سحب دامب خاص أو روم حصري غير مجاني", link: "https://t.me/hithamMax" }
  ],

  solutions: {
    youtube: [
      { id: "yt-1", name: "تخطي حساب جوجل TCL 40 XE T609L", ver: "TCL 40 XE", desc: "شرح عملي لتخطي حماية FRP كاملة", link: "https://youtu.be/P3Cnn5mIK_w" },
      { id: "yt-2", name: "تخطي FRP موتورولا Moto G Fast XT2045-3", ver: "XT2045-3", desc: "طريقة ثغرة الهاتف بدون بوكسات", link: "https://youtu.be/JWP-W1DkK-sP" },
      { id: "yt-3", name: "تخطي FRP موتورولا Moto G Pure XT2163", ver: "XT2163", desc: "تجاوز حساب جوجل بآخر حماية أندرويد 12", link: "https://youtu.be/jMiHCwQBbdo" },
      { id: "yt-4", name: "تخطي FRP TCL K24 T434D", ver: "TCL K24", desc: "حل حماية 2026 المستعصية", link: "https://youtu.be/aHN1YnslJx4" },
      { id: "yt-5", name: "تخطي FRP TCL K11 T432W", ver: "TCL K11", desc: "حل حاسم وسريع لهواتف تي سي إل", link: "https://youtu.be/85XhrheNTDo" },
      { id: "yt-6", name: "تخطي FRP TCL A507DL A2", ver: "A507DL", desc: "طريقة الدخول للإعدادات وتجاوز الحساب", link: "https://youtu.be/s4X0X45eZ28" },
      { id: "yt-7", name: "Reset Frp FOXXD A65U", ver: "FOXXD A65U", desc: "طريقة مجانية لتخطي أجهزة فوكسد", link: "https://www.facebook.com/share/v/1P1jsZnu2z/" },
      { id: "yt-8", name: "حل البرامج غير مدعومة — Redmi Note 12 5G", ver: "Xiaomi", desc: "شرح المهندس سعيد الزعزعي لتشغيل التطبيقات", link: "https://m.youtube.com/watch?v=woydpMu6rc0" },
      { id: "yt-9", name: "إيقاف الرد التلقائي — شاومي", ver: "Xiaomi", desc: "شرح عمر بروجرامر لإيقاف الرد الآلي", link: "https://youtube.com/shorts/McoeDcAd6DQ" }
    ],

    text_guides: [
      {
        id: "mtk_fix",
        title: "حل مشاكل معالجات MTK العالقة (Brom Mode)",
        tag: "A326U, S326DL, A136U, A216U, S127DL",
        problem: "الهاتف لا يقبل الدخول لوضع Brom، أو يظل معلقاً بوضعية Brom ولا يخرج منها، أو يظل معلقاً بوضعية Download Mode.",
        solutionIntro: "الحل النهائي المعتمد باستخدام أداة FastUnlocker Pro وباتش تعريفات الـ SLA:",
        steps: [
          { num: 1, text: "تثبيت حزمة تعريفات MTK Bypass Auth Fix الرسمية وإيقاف توقيع التعريفات." },
          { num: 2, text: "توصيل الهاتف مع الضغط المستمر على زر خفض الصوت + رفع الصوت معاً." },
          { num: 3, text: "فتح أداة FastUnlocker Pro واختيار وضع Force Brom Exit / Fix Download." },
          { num: 4, text: "إعادة تشغيل الجهاز بشكل طبيعي وسيخرج الهاتف من وضع التعليق فوراً." }
        ],
        conclusionNote: "مقدم من فريق برمجة موبايل الرسمي — t.me/BrmagaMobile"
      },
      {
        id: "s21_yemen",
        title: "تفعيل شريحة يمن موبايل — Samsung S21 Ultra 5G",
        tag: "Samsung Galaxy S21 Series",
        problem: "بعد الفورمات أو التحديث للجهاز لا تتعرف الشريحة ولا تظهر شبكة يمن موبايل CDMA/LTE.",
        solutionIntro: "طريقتان معتمدتان لضبط الشبكة:",
        steps: [
          { num: 1, text: "طريقة هيثم ماكس: أخرج الشريحة من الهاتف أولاً." },
          { num: 2, text: "حوّل CSC عبر أداة SamFW إلى كود Sprint (SPR)." },
          { num: 3, text: "ثم حوّل CSC إلى Boost Mobile (BST)." },
          { num: 4, text: "أدخل شريحة يمن موبايل وغيّر نمط الشبكة إلى CDMA / LTE." },
          { num: 5, text: "أعد الجهاز إلى كود فرايزون (VZW) لتثبيت الاتصال والبيانات فوراً." }
        ],
        conclusionNote: "بمساهمة المهندس إبراهيم الصيري وهيثم ماكس"
      },
      {
        id: "knox",
        title: "تخطي حماية Bypass KNOX / MDM / KG — Samsung Exynos",
        tag: "Samsung Exynos A13, A135U, G715U",
        problem: "قفل الحماية المؤسساتية KNOX و MDM و KG Locked على معالجات سامسونج إكسينوس.",
        solutionIntro: "الخطوات البرمجية المعتمدة:",
        steps: [
          { num: 1, text: "تفعيل وضع ADB Root عبر برنامج MOBILedit." },
          { num: 2, text: "تشغيل لوحة الاتصال عبر موجه الأوامر بالسطر التالي:" },
          { num: 3, text: "في لوحة الاتصال اكتب الكود *#0808# ثم اختر RNDIS + ACM + DM ثم Reboot." },
          { num: 4, text: "افتح أداة QCDMA أو TSM Pro وتوجه إلى خانة FRP / MDM." },
          { num: 5, text: "اختر الأمر Bypass KNOX وسيتم فتح الجهاز وتخطي القفل بصورة دائمة." }
        ],
        codeSnippet: "adb shell am start -n com.samsung.android.dialer/.DialerActivity",
        conclusionNote: "مجرب وناجح على A13 SM-A135U و XCover Pro SM-G715U"
      },
      {
        id: "exynos_all_models_gift",
        title: "🎁 FRP & KG SAMSUNG All Model EXYNOS — الطريقة المجانية المعتمدة",
        tag: "Samsung Exynos أندرويد 14/15/16 وحمايات 2025/2026",
        problem: "تخطي حماية حساب جوجل FRP و KG Locked لجميع هواتف سامسونج بمعالجات إكسينوس بدون سيرفرات مدفوعة.",
        solutionIntro: "الخطوات المعتمدة خطوة بخطوة عبر برنامج MobilEdit:",
        steps: [
          { num: 1, text: "افتح برنامج MobilEdit على جهاز الكمبيوتر." },
          { num: 2, text: "اضغط على (بدء Start)." },
          { num: 3, text: "اختر خيار (التجاوز الأمني Security Bypass)." },
          { num: 4, text: "اختر (حسب الشريحة By Chipset)." },
          { num: 5, text: "اختر نوع معالج Exynos وفق موديل الجهاز المستهدف." },
          { num: 6, text: "اضغط بدء وقم بتوصيل الهاتف وهو في وضع الداونلود Download Mode." },
          { num: 7, text: "انتظر حتى يُعيد الهاتف التشغيل تلقائياً وتظهر رسالة شاشة الاسترداد." },
          { num: 8, text: "أغلق MobilEdit واستخدم أي برنامج يدعم ADB FRP (TSM Tool أو UnlockTool أو CDMA Yemen)." },
          { num: 9, text: "فعّل خيار المطور وانتظر اكتمال التخطي الفوري وتجاوز شاشة الترحيب." }
        ],
        conclusionNote: "البرامج المجربة: TSM TOOL Pro, CDMA Yemen Tool Pro, UnlockTool — إهداء مجاني لكل الفنيين من هيثم ماكس."
      }
    ],

    experiences: [
      {
        id: "redmi12c",
        title: "حل مشكلة تدمير النظام System has been destroyed — REDMI 12C",
        author: "ماجد المسوري",
        problem: "ظهور الشاشة السوداء ورسالة 'The system has been destroyed' بعد محاولة التحديث أو التفليش الخاطئ على واجهة HyperOS مع انغلاق البوت لودر.",
        solutionDesc: "تم حل المشكلة بتفليش الفلاشة المعتمدة عبر وضع EDL / BROM باستخدام الأداة المناسبة دون الحاجة لفتح البوتلودر.",
        links: [
          { label: "صور التجربة والخطوات", url: "https://t.me/haithamMax1/1088" },
          { label: "تحميل الفلاشة المعالجة من MiFirm", url: "https://mifirm.net/download/9275", primary: true }
        ]
      },
      {
        id: "motog56",
        title: "حل موت هاتف MOTO G56 5G بعد عملية تخطي FRP",
        author: "محمود الدخاخني",
        problem: "فصل الهاتف ومات تماماً ولا يقبل الإقلاع بعد محاولة FRP عبر Fastboot على أداة TSM Pro.",
        solutionSteps: [
          { num: 1, text: "افتح أداة AMT Tool وتوجه إلى تبويب معالجات ميديا تيك." },
          { num: 2, text: "اختر موديل مشابه: Redmi Note 14 5G." },
          { num: 3, text: "ادخل إلى خيار Partition Manager لقراءة أقسام الجهاز." },
          { num: 4, text: "حدد بارتيشن lk_a و lk_b." },
          { num: 5, text: "اكتب ملف الـ lk المرفق المستخرج من أندرويد 16 ثم أعد تشغيل الجهاز." }
        ],
        warning: "ملاحظة: إذا لم يقرأ الهاتف بورت USB ستحتاج لحام نقاط JTAG لتمرير نفس الملف.",
        links: [
          { label: "تحميل ملف lk المعالج", url: "https://drive.google.com/file/d/1Y_2SgV1LVr0hyfFjLycBHc1Ywa1P6YIt/view", primary: true },
          { label: "تحميل فلاشة Android 16", url: "https://drive.google.com/file/d/1jord8coH93pqrtyQ6FxONIdZG93c8Y0o/view", primary: true },
          { label: "المنشور ومناقشة الحل", url: "https://t.me/haithamMax1/1090" }
        ]
      }
    ],

    volte: [
      { id: "vol-1", name: "Xiaomi & Redmi VoLTE", ver: "Diag Mode", desc: "تفعيل VoLTE لشياومي وريدمي بدون روت عبر أكواد الاتصال", link: "https://youtu.be/lddDl97pVTQ" },
      { id: "vol-2", name: "Samsung VoLTE 2026", ver: "حمايات حديثة", desc: "تفعيل مكالمات VoLTE للسامسونج حمايات One UI 6 & 7", link: "https://youtu.be/KUYST91E33Q" },
      { id: "vol-3", name: "OnePlus & Pixel VoLTE", ver: "Secret Codes", desc: "أكواد مخفية لتفعيل IMS و VoLTE في بيكسل ووان بلس", link: "https://youtu.be/n6Xx6P5fNF0" },
      { id: "vol-4", name: "حل اختفاء VoLTE بعد التحديث", ver: "Yemen Mobile", desc: "استعادة المكالمات عبر 4G بعد تحديث النظام", link: "https://youtu.be/n0vHgu9zKY" },
      { id: "vol-5", name: "إظهار أيقونة 4G / 5G المفقودة", ver: "Fastboot Scripts", desc: "سكريبتات إظهار شبكات الجيل الرابع والخامس", link: "https://youtu.be/CrD_StHVURo" },
      { id: "vol-6", name: "MediaTek MTK VoLTE", ver: "Engineer Mode", desc: "تفعيل المكالمات الصوتية لجميع معالجات ميديا تيك", link: "https://youtu.be/bg7I-MpqkwQ" }
    ],

    rasheed: [
      { id: "rsh-1", name: "كود فيفو السري Vivo New Code 2026", desc: "فتح بورت VCOM وتخطي FRP وتفعيل VoLTE", link: "https://www.facebook.com/share/r/1DJRE2srbS/" },
      { id: "rsh-2", name: "سر هواتف TCL لضبط APN والاتصال", desc: "حل مشكلة تعذر حفظ نقاط الوصول APN", link: "https://www.facebook.com/share/r/191MJSABCU/" },
      { id: "rsh-3", name: "رمز معالجات سبريدترام SPD الجديد", desc: "دخول قائمة المهندس وتخطي FRP و VoLTE", link: "https://www.facebook.com/share/r/1EZn7wQLhC/" },
      { id: "rsh-4", name: "كود تغيير وإصلاح السيريال IMEI", desc: "لهواتف M-Horse والأجهزة الصينية", link: "https://www.facebook.com/share/r/1CkGwXuRfw/" },
      { id: "rsh-5", name: "كود قائمة المهندس للآيفون الكوبي", desc: "كود الدخول المباشر: *#*#136466331#*#*", link: "#", guide: "*#*#136466331#*#*" },
      { id: "rsh-6", name: "تغيير IMEI S25 Ultra Clone", desc: "لتفعيل خدمات VoLTE على النسخ الكوبي", link: "https://www.facebook.com/share/r/1BQS2DaRSb/" },
      { id: "rsh-7", name: "تفعيل VoLTE MTK لشبكات Cricket و AT&T", desc: "عبر قائمة المهندس Engineer Mode", link: "https://www.facebook.com/share/r/1DdtHk6S4C/" },
      { id: "rsh-8", name: "VoLTE هواتف LG خطوة بخطوة", desc: "طريقة سريعة ومضمونة لجميع موديلات LG", link: "https://www.facebook.com/share/r/1947EtzJUY/" },
      { id: "rsh-9", name: "فتح أكواد المهندس لهواتف TCL المقفلة", desc: "تجاوز إغلاق قائمة *#*#3646633#*#*", link: "https://www.facebook.com/share/r/1DsYfYH1wN/" },
      { id: "rsh-10", name: "تجاوز شاشة التنشيط Activation بدون كمبيوتر", desc: "تجاوز مباشر من إعدادات الهاتف", link: "https://www.facebook.com/share/r/1CYAKe7Y4j/" },
      { id: "rsh-11", name: "خيارات المطور للآيفون الكوبي", desc: "إظهار خيارات تصحيح الـ USB المخفية", link: "https://www.facebook.com/share/r/1Do91w5fqM/" },
      { id: "rsh-12", name: "استخراج رموز قفل التطبيقات عبر SetEdit", desc: "قراءة الباسورد بدون فورمات", link: "https://www.facebook.com/share/r/14fXAMKGktm/" },
      { id: "rsh-13", name: "تفعيل VoLTE هواتف Revvl T-Mobile", desc: "فتح القائمة المخفية لتثبيت 4G VoLTE", link: "https://www.facebook.com/share/r/1DYhjz7pUL/" },
      { id: "rsh-14", name: "حل مشكلة VoLTE سامسونج العالقة", desc: "استعادة الصوت بعد فقدان الاتصال", link: "https://www.facebook.com/share/r/1TtX56DoXG/" },
      { id: "rsh-15", name: "طريقة فكفكة وتعديل هواتف Vortex", desc: "تعديل IMEI وضبط الشبكة", link: "https://www.facebook.com/share/r/17oUxMZJFV/" },
      { id: "rsh-16", name: "إصلاح سيريال هواتف Coolpad", desc: "قائمة إصلاح السيريال المفقود 0049", link: "https://youtube.com/shorts/NJ5qhnjGUOc" },
      { id: "rsh-17", name: "تفعيل باندات التغطية Coolpad MTK", desc: "تحسين استقبال إشارة الشبكة في المناطق الضعيفة", link: "https://youtube.com/shorts/a8Toa_7plek" }
    ],

    haitham: [
      { id: "htm-1", name: "FRP LT Mobile عبر TSM PRO", ver: "TSM Pro", desc: "شرح فك حماية حساب جوجل لهواتف إل تي", link: "https://youtu.be/b45iEOYj8BE" },
      { id: "htm-2", name: "FRP Moto G05 XT2523-4", ver: "Moto G05", desc: "تخطي كامل لآخر حماية موتورولا", link: "https://youtu.be/M153OfllQtU" },
      { id: "htm-3", name: "FRP Moto XT2515-2 عبر TSM PRO", ver: "XT2515", desc: "شرح فك موتورولا بنقرة واحدة", link: "https://youtu.be/PLY4u9ANCpg" },
      { id: "htm-4", name: "FRP Benco AE9240 عبر TSM PRO", ver: "Benco", desc: "حل حماية هواتف بينكو", link: "https://youtu.be/ingczBKUFGc" },
      { id: "htm-5", name: "عرض شاشة الآيفون بدون كابل", ver: "iPhone Mirror", desc: "طريقة حصرية لعرض شاشة الآيفون على البي سي", link: "https://youtu.be/Y3spa6koDnI" },
      { id: "htm-6", name: "Root & VoLTE Moto G Power 2025", ver: "Moto G Power", desc: "ترويت وتفعيل مكالمات 4G VoLTE", link: "https://youtu.be/ut2CB7t3A-4" },
      { id: "htm-7", name: "FRP Tecno Spark Go 2 KM4", ver: "Tecno KM4", desc: "تخطي حساب جوجل تكنو سبارك جو", link: "https://youtu.be/t9roIUgeu1Y" },
      { id: "htm-8", name: "FRP Moto G 5G 2025", ver: "FastBoot", desc: "تخطي سريع عبر وضع الفاست بوت", link: "https://youtu.be/w-HN_7ASnCM" },
      { id: "htm-9", name: "FRP Moto G06 One Click", ver: "TSM Tool", desc: "بنقرة واحدة بدون ثغرات معقدة", link: "https://youtu.be/Chfxjh1Byd8" },
      { id: "htm-10", name: "Root & VoLTE Moto G 2025 Android 16", ver: "Android 16", desc: "دعم أحدث إصدارات الأندرويد 16", link: "https://youtu.be/Q06v_VY5yT8" },
      { id: "htm-11", name: "FRP Moto G35 Android 15", ver: "Android 15", desc: "شرح عملي أندرويد 15", link: "https://youtu.be/4kBRW5ZK7do" },
      { id: "htm-12", name: "FRP Moto E15 Android 14", ver: "Android 14", desc: "تخطي أندرويد 14", link: "https://youtu.be/ToE5Ke2LzEk" }
    ],

    samsung_msg: {
      title: "إصلاح تطبيق رسائل سامسونج الأصلي (Samsung Messages APK)",
      problem: "تطبيق الرسائل الأصلي من سامسونج يتم حذفه أو تحديثه تلقائياً من Galaxy Store إلى تطبيق Google Messages وتفشل السكربتات المؤقتة.",
      updates: [
        { num: 1, text: "حظر التحديثات التلقائية الإجبارية من سيرفرات سامسونج ومتجر Galaxy Store." },
        { num: 2, text: "ترشيح نسختين APK متوافقتين مع أندرويد 10 إلى 14 وأندرويد 15 إلى 16." },
        { num: 3, text: "إعادة التثبيت كتطبيق نظام رئيسي بدون روت." },
        { num: 4, text: "اكتشاف هواتف S25 Ultra: سامسونج نقلت مسار التطبيق إلى /product/app." }
      ],
      links: [
        { label: "تحميل السكربت المحدث والمصلح", url: "https://mega.nz/file/chQQmJCR#AsBHKctU4oxIOSKB7H-_vcgijpgh1kmMHzO8IJ8o6xg", primary: true },
        { label: "رابط المنشور والشرح السابق", url: "https://shorturl.at/fFiTX" }
      ]
    }
  }
};
