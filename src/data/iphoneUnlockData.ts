export interface CarrierCode {
  carrier: string;
  country: string;
  codes: string[];
  notes?: string;
}

export const IPHONE_CARRIER_CODES: CarrierCode[] = [
  { carrier: "USA AT&T", country: "الولايات المتحدة 🇺🇸", codes: ["3104101", "3131300", "3104108"], notes: "يستخدم مع شرائح التيربو سيم وأدوات تغيير الـ CSC" },
  { carrier: "USA Verizon", country: "الولايات المتحدة 🇺🇸", codes: ["2040400", "3114806"], notes: "شائع في أجهزة الفيرجن الأمريكية المغلقة" },
  { carrier: "USA Sprint (CDMA)", country: "الولايات المتحدة 🇺🇸", codes: ["3160101", "3160100", "3102605", "3101200", "3101202"], notes: "تفعيل CDMA وسباقات التغطية" },
  { carrier: "USA Cricket", country: "الولايات المتحدة 🇺🇸", codes: ["2040400", "3101508", "3101500", "3100901", "3101507"], notes: "تابع لشبكة AT&T" },
  { carrier: "USA T-Mobile", country: "الولايات المتحدة 🇺🇸", codes: ["3102620", "3102602", "3102605"], notes: "تفعيل VoLTE وشبكات GSM" },
  { carrier: "USA MetroPCS", country: "الولايات المتحدة 🇺🇸", codes: ["3102600"], notes: "شائع في هواتف موتورولا وتي موبايل" },
  { carrier: "USA Tracfone", country: "الولايات المتحدة 🇺🇸", codes: ["3114801"], notes: "أجهزة تراكفون المعقدة" },
  { carrier: "USA Total Wireless", country: "الولايات المتحدة 🇺🇸", codes: ["3114801"], notes: "متوافق مع شبكات فيريزون" },
  { carrier: "USA Boost Mobile", country: "الولايات المتحدة 🇺🇸", codes: ["3160101", "3160100"], notes: "يعمل على شبكة ديش وسبرينت" },
  { carrier: "USA Xfinity", country: "الولايات المتحدة 🇺🇸", codes: ["2040400", "2040438"], notes: "شبكة كومكاست إكسفينيتي" },
  { carrier: "US Cellular", country: "الولايات المتحدة 🇺🇸", codes: ["3115801"], notes: "هواتف يو إس سيلولار" },
  { carrier: "US Virgin", country: "الولايات المتحدة 🇺🇸", codes: ["3160101", "3101200"], notes: "فيرجن موبايل أمريكا" },
  { carrier: "USA Cable&Wireless Lime", country: "الولايات المتحدة 🇺🇸", codes: ["3461401"], notes: "شرائح لايم الدولية" },
  { carrier: "USA Straight Talk", country: "الولايات المتحدة 🇺🇸", codes: ["2040400"], notes: "ستريت توك فيريزون" },
  { carrier: "USA Consumer Cellular", country: "الولايات المتحدة 🇺🇸", codes: ["3104101", "3102620"], notes: "كونسيومر سيلولار" },
  { carrier: "USA Wireless Alaska", country: "الولايات المتحدة 🇺🇸", codes: ["3113700"], notes: "شبكة ألاسكا" },
  { carrier: "Yemen Mobile (يمن موبايل)", country: "اليمن 🇾🇪", codes: ["42102", "42101", "42103"], notes: "أكواد برمجة المشغل وبروفايل الشبكة" }
];

export interface ICloudPriceItem {
  series: string;
  price: string;
  duration: string;
  note: string;
}

export const ICLOUD_OFFICIAL_PRICES: ICloudPriceItem[] = [
  { series: "iPhone 11 Series (11 / Pro / Pro Max)", price: "$100", duration: "20 - 30 يوم", note: "فتح رسمي نظيف Clean 100%" },
  { series: "iPhone 12 Series (12 / Mini / Pro / Max)", price: "$115", duration: "20 - 30 يوم", note: "فتح رسمي نظيف Clean 100%" },
  { series: "iPhone 13 Series (13 / Mini / Pro / Max)", price: "$125", duration: "20 - 30 يوم", note: "فتح رسمي نظيف Clean 100%" },
  { series: "iPhone 14 Series (14 / Plus / Pro / Max)", price: "$135", duration: "20 - 30 يوم", note: "فتح رسمي نظيف Clean 100%" },
  { series: "iPhone 15 Series (15 / Plus / Pro / Max)", price: "$150", duration: "20 - 30 يوم", note: "فتح رسمي نظيف Clean 100%" },
  { series: "iPhone 16 Series (16 / Plus / Pro / Max)", price: "$175", duration: "20 - 30 يوم", note: "أحدث معالجات A18" },
  { series: "iPhone 17 Series (17 / Air / Pro / Max)", price: "$250", duration: "20 - 30 يوم", note: "السيرفر الرسمي العالمي" }
];

export const IPHONE_METHOD_RESOURCES = {
  esimMethod1: {
    title: "شريحة إلكترونية للآيفون - ثبات التغطية (طريقة رقم 1)",
    desc: "ملف الشرح والتكوين الكامل لتثبيت التغطية ومنع تقلب الشبكة في هواتف الآيفون المقفلة بشريحة إلكترونية.",
    url: "https://www.mediafire.com/file/78yrp0yui10rme1/%25D8%25B4%25D8%25B1%25D9%258A%25D8%25AD%25D9%2587_%25D8%25A5%25D9%2584%25D9%2583%25D8%25AA%25D8%25B1%25D9%2588%25D9%2586%25D9%258A_%25D9%2584%25D9%2584%25D8%25A7%25D9%258A%25D9%2581%25D9%2588%25D9%2586_%25D8%25AB%25D8%25A8%25D8%25A7%25D8%25AA_%25D8%25A7%25D9%2584%25D8%25AA%25D8%25BA%25D8%25B7%25D9%258A%25D9%2587.txt/file"
  },
  esimMethod2: {
    title: "الطريقة الثانية للآيفون - فك شفرة وتثبيت IMSI",
    desc: "الملف البرمجي والخطوات اليدوية للطريقة البديلة في حال عدم استجابة الشريحة للطريقة الأولى.",
    url: "https://www.mediafire.com/file/rno5wdrghobbsoo/%25D8%25A7%25D9%2584%25D8%25B7%25D8%25B1%25D9%258A%25D9%2582%25D9%2587_%25D8%25A7%25D9%2584%25D8%25AB%25D8%25A7%25D9%2586%25D9%258A%25D9%2587_%25D9%2584%25D9%2584%25D8%25A7%25D9%258A%25D9%2581%25D9%2588%25D9%2586.txt/file"
  },
  iccidPdf: {
    title: "LATEST ICCID CODE — Problem Killer PDF",
    desc: "كتيب وشرح أكواد الـ ICCID الأحدث لتجاوز شاشة التنشيط والتفعيل الدائم.",
    url: "https://www.mediafire.com/file/buaehs8iyroqqvt/LATEST_ICCID_CODE_-_Problem_Killer_%25282%2529.pdf/file"
  }
};
