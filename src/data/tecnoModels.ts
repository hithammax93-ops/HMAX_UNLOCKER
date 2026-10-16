import { ItemData } from './hmaxData';

export interface TecnoModelItem extends ItemData {
  series: 'spark' | 'camon' | 'pova' | 'pop' | 'phantom' | 'other';
  rawKey: string;
}

export const TECNO_MODELS: TecnoModelItem[] = [
  // SPARK SERIES
  {
    id: "tecno-spk-2",
    name: "TECNO SPARK 2 KA7",
    rawKey: "tecno_spark_2_ka7",
    series: "spark",
    ver: "KA7 Official Dump",
    desc: "فلاشة ودامب رسمي لهاتف تكنو سبارك 2 مسحوب ومختبر بالكامل",
    link: "https://drive.google.com/drive/folders/1-m9ZynYe8S9dI8G_bU7OtPiqTkg1wlgl",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-3",
    name: "TECNO SPARK 3 KB3",
    rawKey: "tecno_spark_3_kb3",
    series: "spark",
    ver: "KB3 Official Dump",
    desc: "فلاشة ودامب تكنو سبارك 3 لإصلاح البوت وتخطي الحمايات",
    link: "https://drive.google.com/drive/folders/1-vgXzJSKVqeTvZgAxc5ztZ7_AxLq9FbJ",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-3p",
    name: "TECNO SPARK 3 Pro KB8",
    rawKey: "tecno_spark_3_pro_kb8",
    series: "spark",
    ver: "KB8 Official Dump",
    desc: "فلاشة تكنو سبارك 3 برو كاملة مع بارتشنات الشبكة NVRAM",
    link: "https://drive.google.com/drive/folders/100BGo4AOd-8UmU5Ij5WYIddE4AmA37XQ",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-4",
    name: "TECNO SPARK 4 KC2",
    rawKey: "tecno_spark_4_kc2",
    series: "spark",
    ver: "KC2 Official Dump",
    desc: "دامب تكنو سبارك 4 جاهز للتفليش عبر SP Flash Tool أو البوكسات",
    link: "https://drive.google.com/drive/folders/10JG6dA0TSAysiPcG4jUczaieu0URoZw7",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-4a",
    name: "TECNO SPARK 4 Air KC1",
    rawKey: "tecno_spark_4_air_kc1",
    series: "spark",
    ver: "KC1 Official Dump",
    desc: "فلاشة سبارك 4 إير الأصلية لإصلاح التعليق على الشعار والموت المفاجئ",
    link: "https://drive.google.com/drive/folders/11dkP5rt3dg7G4H7X4Hw9TBWxx30GoH4m",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-5",
    name: "TECNO SPARK 5 KD7",
    rawKey: "tecno_spark_5_kd7",
    series: "spark",
    ver: "KD7 Official Dump",
    desc: "فلاشة ودامب تكنو سبارك 5 الموثوقة للتفليش وإصلاح أخطاء الذاكرة",
    link: "https://drive.google.com/drive/folders/12XiKIypdVAqgmfIwe2flztLkV46Uan7P",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-5a",
    name: "TECNO SPARK 5 Air KD6",
    rawKey: "tecno_spark_5_air_kd6",
    series: "spark",
    ver: "KD6 Official Dump",
    desc: "روم ودامب كامل لهاتف سبارك 5 إير KD6",
    link: "https://drive.google.com/drive/folders/133Y_Xlfj7OGXevOaTJ1ZYYQlQnLcqQ2_",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-5p",
    name: "TECNO SPARK 5 Pro KD7H",
    rawKey: "tecno_spark_5_pro_kd7h",
    series: "spark",
    ver: "KD7H Official Dump",
    desc: "فلاشة سبارك 5 برو مسحوبة بصيغة Scatter كاملة",
    link: "https://drive.google.com/drive/folders/13TGqSs7VXc6eA333_ZFlBQKpYThnmKCA",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-6",
    name: "TECNO SPARK 6 KE7",
    rawKey: "tecno_spark_6_ke7",
    series: "spark",
    ver: "KE7 Official Dump",
    desc: "دامب تكنو سبارك 6 KE7 لإصلاح مشكلة الشاشة الزرقاء وإعادة التشغيل",
    link: "https://drive.google.com/drive/folders/13wS_X7Ujn0IhfdjAbudlBVSLxMXdf9t2",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-6a",
    name: "TECNO SPARK 6 Air KE6",
    rawKey: "tecno_spark_6_air_ke6",
    series: "spark",
    ver: "KE6 Official Dump",
    desc: "فلاشة سبارك 6 إير الرسمية مجربة 100%",
    link: "https://drive.google.com/drive/folders/14Rm5LKK7359tMW0Q-cs7WmZ2sPHkdYo_",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-6g",
    name: "TECNO SPARK 6 Go KE5",
    rawKey: "tecno_spark_6_go_ke5",
    series: "spark",
    ver: "KE5 Official Dump",
    desc: "فلاشة ودامب سبارك 6 جو لحل مشكلة قفل FRP والوقوف على الافتتاحية",
    link: "https://drive.google.com/drive/folders/15JF_3ySQUmoeoh96cFlyW_azy2s0Qccq",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-7",
    name: "TECNO SPARK 7 KF6",
    rawKey: "tecno_spark_7_kf6",
    series: "spark",
    ver: "KF6 Official Dump",
    desc: "فلاشة ودامب رسمي تكنو سبارك 7",
    link: "https://drive.google.com/drive/folders/15yVmCNTjkvYYYXiJ8n0T9sskRRQj9ZQw",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-7p",
    name: "TECNO SPARK 7P KF7J",
    rawKey: "tecno_spark_7p_kf7j",
    series: "spark",
    ver: "KF7J Official Dump",
    desc: "فلاشة سبارك 7 بي مع حزمة ملفات الشبكة والمعايرة",
    link: "https://drive.google.com/drive/folders/166s4XVMuDiPJl9xmYn_WAGV1T_CdwLr4",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-7t",
    name: "TECNO SPARK 7T KF6P",
    rawKey: "tecno_spark_7t_kf6p",
    series: "spark",
    ver: "KF6P Official Dump",
    desc: "دامب تكنو سبارك 7 تي مسحوب بدون أخطاء",
    link: "https://drive.google.com/drive/folders/16BWgqWtMoM50BYzEQHPQBzwt0ljzK5Bs",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-8",
    name: "TECNO SPARK 8 KG6",
    rawKey: "tecno_spark_8_kg6",
    series: "spark",
    ver: "KG6 Official Dump",
    desc: "فلاشة ودامب تكنو سبارك 8 رسمية",
    link: "https://drive.google.com/drive/folders/16jLxWX-gPhuRTpBFU1ChqXe6sWyP-T0F",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-8c",
    name: "TECNO SPARK 8C KG5",
    rawKey: "tecno_spark_8c_kg5",
    series: "spark",
    ver: "KG5 Official Dump",
    desc: "دامب سبارك 8 سي لمعالجات سبريدترام وميديا تيك",
    link: "https://drive.google.com/drive/folders/16nTXFprwhJQjlDZ0r-W5_0l-BUTRrRdg",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-8p",
    name: "TECNO SPARK 8P KG7H",
    rawKey: "tecno_spark_8p_kg7h",
    series: "spark",
    ver: "KG7H Official Dump",
    desc: "فلاشة سبارك 8 بي KG7H لإصلاح فقدان السيريال والشبكة",
    link: "https://drive.google.com/drive/folders/179vJDld7mv8Z4kL2ZGtLyYOmhezD-t-x",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-8t",
    name: "TECNO SPARK 8T KG6P",
    rawKey: "tecno_spark_8t_kg6p",
    series: "spark",
    ver: "KG6P Official Dump",
    desc: "فلاشة سبارك 8 تي الرسمية مسحوبة بأدوات أصلية",
    link: "https://drive.google.com/drive/folders/18v-IQXQEL1T5fibe9uFoYNs1mwMAt9yT",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-9",
    name: "TECNO SPARK 9 KG10",
    rawKey: "tecno_spark_9_kg10",
    series: "spark",
    ver: "KG10 Official Dump",
    desc: "فلاشة ودامب تكنو سبارك 9",
    link: "https://drive.google.com/drive/folders/19Xe2usg_tmOXJH2KInS-F0qmx6w7z3Y1",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-9t",
    name: "TECNO SPARK 9T KH6",
    rawKey: "tecno_spark_9t_kh6",
    series: "spark",
    ver: "KH6 Official Dump",
    desc: "دامب تكنو سبارك 9 تي كامل",
    link: "https://drive.google.com/drive/folders/1A3TzPyZQY332aXRghkyL_9PYDQ9XjLzt",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-9p",
    name: "TECNO SPARK 9 Pro KH7",
    rawKey: "tecno_spark_9_pro_kh7",
    series: "spark",
    ver: "KH7 Official Dump",
    desc: "فلاشة سبارك 9 برو الرسمية مع ملفات الـ DA و Auth",
    link: "https://drive.google.com/drive/folders/1ANiLQQ2_bSrfXGUvhB_GavjnRkvJBpBq",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-10",
    name: "TECNO SPARK 10 KI5",
    rawKey: "tecno_spark_10_ki5",
    series: "spark",
    ver: "KI5 Official Dump",
    desc: "فلاشة ودامب تكنو سبارك 10 KI5 أصلية",
    link: "https://drive.google.com/drive/folders/1AtObtnhdv4KsAiPLxltE4EicTyL0rbYJ",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-10c",
    name: "TECNO SPARK 10C KI5K",
    rawKey: "tecno_spark_10c_ki5k",
    series: "spark",
    ver: "KI5K Official Dump",
    desc: "دامب تكنو سبارك 10 سي مسحوب عبر باندورا وأنلوك تول",
    link: "https://drive.google.com/drive/folders/1B1fRzLijaye9X7pWEIcvVW_-bVHTdXx6",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-10p",
    name: "TECNO SPARK 10 Pro KI7",
    rawKey: "tecno_spark_10_pro_ki7",
    series: "spark",
    ver: "KI7 Official Dump",
    desc: "فلاشة سبارك 10 برو الأصلية لإصلاح التعليق وفك الحمايات",
    link: "https://drive.google.com/drive/folders/1B6mUpM8zG2s4g9XUrRqH__iDtYYtkH1m",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-10t",
    name: "TECNO SPARK 10T KI5T",
    rawKey: "tecno_spark_10t_ki5t",
    series: "spark",
    ver: "KI5T Official Dump",
    desc: "دامب كامل سبارك 10 تي",
    link: "https://drive.google.com/drive/folders/1BIdsD8VvSqF12mUDhZ0jOwwmcen8DNeI",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-10-5g",
    name: "TECNO SPARK 10 5G KI8",
    rawKey: "tecno_spark_10_5g_ki8",
    series: "spark",
    ver: "KI8 5G Official Dump",
    desc: "فلاشة سبارك 10 فايف جي الرسمية مع ملفات المودم",
    link: "https://drive.google.com/drive/folders/1yDJP0eRcWy7mm8h1WSww9QBVemI9ZRgb",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-10p-magic",
    name: "TECNO KI7S SPARK 10 Pro Magic",
    rawKey: "tecno_ki7s_spark_10_pro_magic",
    series: "spark",
    ver: "KI7S Magic Skin Dump",
    desc: "إصدار ماجيك الخاص من سبارك 10 برو مسحوب بالكامل",
    link: "https://drive.google.com/drive/folders/1rh6MrMKGWRQpblnnFgD99VnTEkyNEMeC",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-20",
    name: "TECNO SPARK 20 KJ5",
    rawKey: "tecno_spark_20_kj5",
    series: "spark",
    ver: "KJ5 Official Dump",
    desc: "فلاشة سبارك 20 الأصلية لإحياء الهاتف والتفليش",
    link: "https://drive.google.com/drive/folders/1BOZ_TRuxytEktE7KzetkLGfu-W-A31Ke",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-20c",
    name: "TECNO SPARK 20C BG7",
    rawKey: "tecno_spark_20c_bg7",
    series: "spark",
    ver: "BG7 Official Dump",
    desc: "دامب تكنو سبارك 20 سي BG7 مسحوب بدقة",
    link: "https://drive.google.com/drive/folders/1BTpcU4CcuLKdjc6c6mrhUy-MhtjUzcxn",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-20p",
    name: "TECNO SPARK 20 Pro KJ6",
    rawKey: "tecno_spark_20_pro_kj6",
    series: "spark",
    ver: "KJ6 Official Dump",
    desc: "فلاشة سبارك 20 برو KJ6 حماية حديثة",
    link: "https://drive.google.com/drive/folders/1C1Dy3CqiWhtmpeD7IhE14fKy2UPdir45",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-20pp",
    name: "TECNO SPARK 20 Pro+ KJ7",
    rawKey: "tecno_spark_20_proplus_kj7",
    series: "spark",
    ver: "KJ7 Official Dump",
    desc: "فلاشة سبارك 20 برو بلس الشاشة المنحنية معالج Helio G99",
    link: "https://drive.google.com/drive/folders/1C7lwkjCxl3fEi1WQyQb3J9DhD24nV1E_",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-20p-5g",
    name: "TECNO SPARK 20 Pro 5G KJ8",
    rawKey: "tecno_spark_20_pro_5g_kj8",
    series: "spark",
    ver: "KJ8 5G Official Dump",
    desc: "فلاشة سبارك 20 برو فايف جي الحديثة",
    link: "https://drive.google.com/drive/folders/1yw7gCCzm-SkN5FAcRpuu7QE1ZlDx4DM_",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-go-2020",
    name: "TECNO SPARK Go 2020 KE5J",
    rawKey: "tecno_spark_go_2020_ke5j",
    series: "spark",
    ver: "KE5J Official Dump",
    desc: "دامب سبارك جو 2020 كامل",
    link: "https://drive.google.com/drive/folders/1CXDyNx7_vafU9-AA2NWBM68_zOCGRs37",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-go-2021",
    name: "TECNO SPARK Go 2021 KE5K",
    rawKey: "tecno_spark_go_2021_ke5k",
    series: "spark",
    ver: "KE5K Official Dump",
    desc: "دامب سبارك جو 2021 رسمي",
    link: "https://drive.google.com/drive/folders/1D6qrusumdFXMQof2R2ab2hwE4QTwHmId",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-go-2022",
    name: "TECNO SPARK Go 2022 KG5A",
    rawKey: "tecno_spark_go_2022_kg5a",
    series: "spark",
    ver: "KG5A Official Dump",
    desc: "فلاشة سبارك جو 2022 كاملة",
    link: "https://drive.google.com/drive/folders/1DJk3VhPoo11D197NfhyAn1b1qR1YQgHk",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-go-2022p",
    name: "TECNO KG5P SPARK Go 2022",
    rawKey: "tecno_kg5p_spark_go_2022",
    series: "spark",
    ver: "KG5P Official Dump",
    desc: "إصدار KG5P من سبارك جو 2022 مسحوب رسمي",
    link: "https://drive.google.com/drive/folders/1pbx7dbOiKByjp91azZOZNKIKs_JQmxOU",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-go-2023",
    name: "TECNO SPARK Go 2023 BF7",
    rawKey: "tecno_spark_go_2023_bf7",
    series: "spark",
    ver: "BF7 Official Dump",
    desc: "فلاشة ودامب سبارك جو 2023 الرسمية",
    link: "https://drive.google.com/drive/folders/1DRuZfy4O3LdvAwHxrc901ocf_D58W4gj",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-go-2024",
    name: "TECNO SPARK Go 2024 BG6",
    rawKey: "tecno_spark_go_2024_bg6",
    series: "spark",
    ver: "BG6 Official Dump",
    desc: "فلاشة ودامب سبارك جو 2024 أحدث إصدار",
    link: "https://drive.google.com/drive/folders/1D_KXbos9taI9TfXzOsumHsDIluakoD8a",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-40",
    name: "TECNO SPARK 40 KL5",
    rawKey: "tecno_spark_40_kl5",
    series: "spark",
    ver: "KL5 Official Dump",
    desc: "فلاشة تكنو سبارك 40 الحديثة أندرويد 15/16",
    link: "https://drive.google.com/drive/folders/1DdzE_ZeytpSUnY2KqsiOdSBzb44iov1Q",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-40c",
    name: "TECNO KL4 SPARK 40C",
    rawKey: "tecno_kl4_spark_40c",
    series: "spark",
    ver: "KL4 Official Dump",
    desc: "دامب تكنو سبارك 40 سي KL4 رسمي",
    link: "https://drive.google.com/drive/folders/1un4LGdDRfu-wp41gzT8AjNMYxqWs91UQ",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-40-km5",
    name: "TECNO KM5 SPARK 40",
    rawKey: "tecno_km5_spark_40",
    series: "spark",
    ver: "KM5 Official Dump",
    desc: "نسخة KM5 الرسمية من سبارك 40",
    link: "https://drive.google.com/drive/folders/1wGRPHLwQGUWfNVBzSUUqNZD5HJrgpKuI",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-40p",
    name: "TECNO SPARK 40 Pro KM6",
    rawKey: "tecno_spark_40_pro_km6",
    series: "spark",
    ver: "KM6 Official Dump",
    desc: "فلاشة سبارك 40 برو KM6 أحدث أندرويد عبر AMT",
    link: "https://drive.google.com/drive/folders/1DqVSTBr0tVeSEtpnZ6_C7BzOHj_3OkzW",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-40pp",
    name: "TECNO SPARK 40 Pro+ KM7",
    rawKey: "tecno_spark_40_proplus_km7",
    series: "spark",
    ver: "KM7 Official Dump",
    desc: "فلاشة سبارك 40 برو بلس KM7 كاملة",
    link: "https://drive.google.com/drive/folders/1EIrAZ0WC7b7_1SX_C5JKHuLiU9PQNr_a",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spk-8p-kg7",
    name: "TECNO KG7 SPARK 8P",
    rawKey: "tecno_kg7_spark_8p",
    series: "spark",
    ver: "KG7 Official Dump",
    desc: "فلاشة سبارك 8 بي KG7 الرسمية",
    link: "https://drive.google.com/drive/folders/1qcKTvJd4hBHDxOb64KnqKbLJIV9xkfO0",
    pass: "MobiFirmware.VIP"
  },

  // CAMON SERIES
  {
    id: "tecno-cam-11",
    name: "TECNO CAMON 11 CF7",
    rawKey: "tecno_camon_11_cf7",
    series: "camon",
    ver: "CF7 Official Dump",
    desc: "فلاشة كامون 11 الأصلية لإصلاح التعليق وفقدان الصوت",
    link: "https://drive.google.com/drive/folders/1EgJaPwILRLezqUNJBiLcDuceth2QEemT",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-11p",
    name: "TECNO CAMON 11 Pro CF8",
    rawKey: "tecno_camon_11_pro_cf8",
    series: "camon",
    ver: "CF8 Official Dump",
    desc: "فلاشة كامون 11 برو الرسمية مسحوبة ونظيفة",
    link: "https://drive.google.com/drive/folders/1En3QMKRLs86WQ7rVsZq-waZSiHT-zoRc",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-12",
    name: "TECNO CAMON 12 CC7",
    rawKey: "tecno_camon_12_cc7",
    series: "camon",
    ver: "CC7 Official Dump",
    desc: "فلاشة ودامب تكنو كامون 12 كاملة",
    link: "https://drive.google.com/drive/folders/1F70V8JGMSBfurVOu_hxoFT1Bi8Bi84fp",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-12a",
    name: "TECNO CAMON 12 Air CC6",
    rawKey: "tecno_camon_12_air_cc6",
    series: "camon",
    ver: "CC6 Official Dump",
    desc: "فلاشة كامون 12 إير الرسمية",
    link: "https://drive.google.com/drive/folders/1G1jf_9jSOMoAcSfO1FBRRcsDz1TxpW-R",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-12p",
    name: "TECNO CAMON 12 Pro CC9",
    rawKey: "tecno_camon_12_pro_cc9",
    series: "camon",
    ver: "CC9 Official Dump",
    desc: "فلاشة كامون 12 برو شاشة أموليد وبصمة مدمجة",
    link: "https://drive.google.com/drive/folders/1GbCaREdOSHXjJkcGwmXA7otBLLGz78RB",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-15",
    name: "TECNO CAMON 15 CD7",
    rawKey: "tecno_camon_15_cd7",
    series: "camon",
    ver: "CD7 Official Dump",
    desc: "فلاشة ودامب تكنو كامون 15 CD7",
    link: "https://drive.google.com/drive/folders/1Ge92FTek3V7wiZNm-68plo5MvJir0evK",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-15a",
    name: "TECNO CAMON 15 Air CD6",
    rawKey: "tecno_camon_15_air_cd6",
    series: "camon",
    ver: "CD6 Official Dump",
    desc: "فلاشة كامون 15 إير الرسمية",
    link: "https://drive.google.com/drive/folders/1GkV2AlbKSA4JfnIhUUtFTqtCdPsvM9ww",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-15p",
    name: "TECNO CAMON 15 Pro CD8",
    rawKey: "tecno_camon_15_pro_cd8",
    series: "camon",
    ver: "CD8 Official Dump",
    desc: "فلاشة كامون 15 برو الكاميرا المنبثقة Pop-up",
    link: "https://drive.google.com/drive/folders/1HfDnMnZ7Hd9UeM5DeDZ6xu4LZumDaxiq",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-16",
    name: "TECNO CAMON 16 CE7",
    rawKey: "tecno_camon_16_ce7",
    series: "camon",
    ver: "CE7 Official Dump",
    desc: "فلاشة ودامب تكنو كامون 16 مع ملفات المصنع",
    link: "https://drive.google.com/drive/folders/1IF7wNE1POKbBcYmTDbwjAvlX2q78V3XW",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-16p",
    name: "TECNO CAMON 16 Pro CE8",
    rawKey: "tecno_camon_16_pro_ce8",
    series: "camon",
    ver: "CE8 Official Dump",
    desc: "فلاشة كامون 16 برو الرسمية",
    link: "https://drive.google.com/drive/folders/1IjwY4qrA5iLCtnwc0e5wYUCcExtFmYCr",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-16pr",
    name: "TECNO CAMON 16 Premier CE9",
    rawKey: "tecno_camon_16_premier_ce9",
    series: "camon",
    ver: "CE9 Official Dump",
    desc: "فلاشة كامون 16 بريمير معالج Helio G90T وشاشة 90Hz",
    link: "https://drive.google.com/drive/folders/1Js9pYoralgMhLlDhZ_gGfExDhdxzMwLC",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-17",
    name: "TECNO CAMON 17 CG6",
    rawKey: "tecno_camon_17_cg6",
    series: "camon",
    ver: "CG6 Official Dump",
    desc: "فلاشة تكنو كامون 17 الرسمية مع ملفات السوفت وير",
    link: "https://drive.google.com/drive/folders/1L1MIMkaHU-IbW2v9uymQxcaE0_0XQxmq",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-17p",
    name: "TECNO CAMON 17 Pro CG7",
    rawKey: "tecno_camon_17_pro_cg7",
    series: "camon",
    ver: "CG7 Official Dump",
    desc: "فلاشة كامون 17 برو CG7 معالج Helio G95",
    link: "https://drive.google.com/drive/folders/1LxXDNnMg4D5ztqJLrSORG6swNl8yg5ef",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-17ps",
    name: "TECNO CAMON 17P CG7S",
    rawKey: "tecno_camon_17p_cg7s",
    series: "camon",
    ver: "CG7S Official Dump",
    desc: "دامب كامون 17 بي CG7S كامل ومجرب",
    link: "https://drive.google.com/drive/folders/1MCDr3yYTWQzLkBOh9lYWu6zJAM5rW30K",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-18",
    name: "TECNO CAMON 18 CH6",
    rawKey: "tecno_camon_18_ch6",
    series: "camon",
    ver: "CH6 Official Dump",
    desc: "فلاشة ودامب تكنو كامون 18 CH6",
    link: "https://drive.google.com/drive/folders/1N29KtZ55cWdj5-CCelL5gLDCzqtdb-qG",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-18p",
    name: "TECNO CAMON 18P CH7",
    rawKey: "tecno_camon_18p_ch7",
    series: "camon",
    ver: "CH7 Official Dump",
    desc: "فلاشة كامون 18 بي CH7 معالج Helio G96",
    link: "https://drive.google.com/drive/folders/1N3qhvJhcmxg4CrSVmpN-xwWfP6XOUMan",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-18pr",
    name: "TECNO CAMON 18 Premier CH9",
    rawKey: "tecno_camon_18_premier_ch9",
    series: "camon",
    ver: "CH9 Official Dump",
    desc: "فلاشة كامون 18 بريمير كاملة مع كاميرا الجيمبال",
    link: "https://drive.google.com/drive/folders/1NOkjzkgtpdsCcmYSoyKn0TeJS3FufJRD",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-19",
    name: "TECNO CAMON 19 CI6",
    rawKey: "tecno_camon_19_ci6",
    series: "camon",
    ver: "CI6 Official Dump",
    desc: "فلاشة ودامب تكنو كامون 19 CI6 الرسمية",
    link: "https://drive.google.com/drive/folders/1Oogz7PC5JuSeXDzc_YIVe6ZMv8QeYWTl",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-19p",
    name: "TECNO CAMON 19 Pro CI7",
    rawKey: "tecno_camon_19_pro_ci7",
    series: "camon",
    ver: "CI7 Official Dump",
    desc: "فلاشة كامون 19 برو CI7 شاشة 120Hz",
    link: "https://drive.google.com/drive/folders/1PMf3SFB-w97nEFSD7SKLVxtPAFVcLyHR",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-19n",
    name: "TECNO CAMON 19 Neo CI6S",
    rawKey: "tecno_camon_19_neo_ci6s",
    series: "camon",
    ver: "CI6S Official Dump",
    desc: "فلاشة كامون 19 نيو الرسمية",
    link: "https://drive.google.com/drive/folders/1PU3A1x-9ciWjbgMgMtkw2gbcuV44PeCd",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-19p-5g",
    name: "TECNO CAMON 19 Pro 5G CI7N",
    rawKey: "tecno_camon_19_pro_5g_ci7n",
    series: "camon",
    ver: "CI7N 5G Official Dump",
    desc: "فلاشة كامون 19 برو فايف جي معالج Dimensity 810",
    link: "https://drive.google.com/drive/folders/1PZKt-Xq_XPmM5SzxsoiI6oZ0lTYC_NbB",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-19-mon",
    name: "TECNO CAMON 19 Pro Mondrian",
    rawKey: "tecno_camon_19_pro_mondrian",
    series: "camon",
    ver: "Mondrian Special Dump",
    desc: "نسخة موندريان الفنية لتكنو كامون 19 برو",
    link: "https://drive.google.com/drive/folders/1z1NI5Orbd4XZmVfdZVEJfZGB33d_HGcY",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-20",
    name: "TECNO CAMON 20 CK6",
    rawKey: "tecno_camon_20_ck6",
    series: "camon",
    ver: "CK6 Official Dump",
    desc: "فلاشة ودامب تكنو كامون 20 CK6 أصلية",
    link: "https://drive.google.com/drive/folders/1PgU9O2Zskj9pNYEIvnBJXIcNUPNk_e9o",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-20p",
    name: "TECNO CAMON 20 Pro CK7",
    rawKey: "tecno_camon_20_pro_ck7",
    series: "camon",
    ver: "CK7 Official Dump",
    desc: "فلاشة كامون 20 برو معالج Helio G99",
    link: "https://drive.google.com/drive/folders/1PmZkaGMt7QwKEgCWjX5IcySLbkQT_8-R",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-20p-5g",
    name: "TECNO CAMON 20 Pro 5G CK8",
    rawKey: "tecno_camon_20_pro_5g_ck8",
    series: "camon",
    ver: "CK8 5G Official Dump",
    desc: "فلاشة كامون 20 برو 5G معالج Dimensity 8050",
    link: "https://drive.google.com/drive/folders/1QK9zkmewm6wYm-ijZ0Fn3wrpU3z0XhZk",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-20pr",
    name: "TECNO CAMON 20 Premier CK9",
    rawKey: "tecno_camon_20_premier_ck9",
    series: "camon",
    ver: "CK9 Premier Dump",
    desc: "فلاشة كامون 20 بريمير 512GB UFS",
    link: "https://drive.google.com/drive/folders/1Qb08q0gLLjRRqBQtWGgo8XwLrVywBJag",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-30",
    name: "TECNO CAMON 30 CL6",
    rawKey: "tecno_camon_30_cl6",
    series: "camon",
    ver: "CL6 Official Dump",
    desc: "فلاشة ودامب تكنو كامون 30 CL6",
    link: "https://drive.google.com/drive/folders/1SWp8MskCdmM0w271E1Bm6cmRQTKV1VTd",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-30p",
    name: "TECNO CAMON 30 Pro CL7",
    rawKey: "tecno_camon_30_pro_cl7",
    series: "camon",
    ver: "CL7 Official Dump",
    desc: "فلاشة كامون 30 برو Dimensity 8200 Ultra",
    link: "https://drive.google.com/drive/folders/1Soku2BdxP4F5CU3w7rVYfVSdNIwwydjV",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-30-5g",
    name: "TECNO CAMON 30 5G CL6K",
    rawKey: "tecno_camon_30_5g_cl6k",
    series: "camon",
    ver: "CL6K 5G Official Dump",
    desc: "فلاشة كامون 30 فايف جي الرسمية",
    link: "https://drive.google.com/drive/folders/1SrYkhvbZYH_ftz3UQM_W7RUV2xPt4o-N",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-30pr",
    name: "TECNO CAMON 30 Premier CL9",
    rawKey: "tecno_camon_30_premier_cl9",
    series: "camon",
    ver: "CL9 Premier Dump",
    desc: "فلاشة كامون 30 بريمير كاميرات 50MP Sony IMX890",
    link: "https://drive.google.com/drive/folders/1T9CHlE2Bu3wqlGj8XzvgFw2ZbcQwyzpN",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-30s",
    name: "TECNO CL8 CAMON 30S",
    rawKey: "tecno_cl8_camon_30s",
    series: "camon",
    ver: "CL8 Official Dump",
    desc: "دامب تكنو كامون 30S موديل CL8 رسمي",
    link: "https://drive.google.com/drive/folders/1ujOIZetpCF8LDzPA2h9xjcWFk76A0y7p",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-40",
    name: "TECNO CAMON 40 CM5",
    rawKey: "tecno_camon_40_cm5",
    series: "camon",
    ver: "CM5 Official Dump",
    desc: "فلاشة ودامب تكنو كامون 40 الحديثة",
    link: "https://drive.google.com/drive/folders/1TSIAMGesn5dm0eBLXKRroWu1vIcyUYmS",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-40p",
    name: "TECNO CAMON 40 Pro CM6",
    rawKey: "tecno_camon_40_pro_cm6",
    series: "camon",
    ver: "CM6 Official Dump",
    desc: "فلاشة كامون 40 برو CM6 الرسمية",
    link: "https://drive.google.com/drive/folders/1TSY4ypTu_VW0qxhbUuSYxMM7v067g65k",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-40p-5g",
    name: "TECNO CAMON 40 Pro 5G CM7",
    rawKey: "tecno_camon_40_pro_5g_cm7",
    series: "camon",
    ver: "CM7 5G Official Dump",
    desc: "فلاشة كامون 40 برو 5G معالج حديث",
    link: "https://drive.google.com/drive/folders/1TUHgVOOuTD36wangf2t2SWfm95zKDszC",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-i",
    name: "TECNO CAMON i IN1",
    rawKey: "tecno_camon_i_in1",
    series: "camon",
    ver: "IN1 Official Dump",
    desc: "فلاشة كامون آي إن 1 نادرة ومضمونة",
    link: "https://drive.google.com/drive/folders/1g8h21VBnGY41j_ePj14EL08XmW-OqMwK",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-i2",
    name: "TECNO CAMON i2 ID5",
    rawKey: "tecno_camon_i2_id5",
    series: "camon",
    ver: "ID5 Official Dump",
    desc: "فلاشة كامون آي 2 الرسمية",
    link: "https://drive.google.com/drive/folders/1gXfF2ZZ2sh0EJm7imyUmDuYhf0Be78_U",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-i2x",
    name: "TECNO CAMON i2X ID5A",
    rawKey: "tecno_camon_i2x_id5a",
    series: "camon",
    ver: "ID5A Official Dump",
    desc: "فلاشة كامون آي 2 إكس كاملة",
    link: "https://drive.google.com/drive/folders/1ghOf2LWJfnnCBMJTy-YyVxABhUfqk07k",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-i4",
    name: "TECNO CAMON i4 CB7",
    rawKey: "tecno_camon_i4_cb7",
    series: "camon",
    ver: "CB7 Official Dump",
    desc: "فلاشة كامون آي 4 مسحوبة",
    link: "https://drive.google.com/drive/folders/1h1F1oMpBzdk7LtmnoF6wa8ZH90jeBEOw",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-iclick",
    name: "TECNO CAMON iClick IN6",
    rawKey: "tecno_camon_iclick_in6",
    series: "camon",
    ver: "IN6 Official Dump",
    desc: "فلاشة كامون آي كليك الأصلية",
    link: "https://drive.google.com/drive/folders/1hC3SExzTxBtig_5QEDk8ACDsS0wPIr9g",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-cx",
    name: "TECNO CAMON CX CC5",
    rawKey: "tecno_camon_cx_cc5",
    series: "camon",
    ver: "CC5 Official Dump",
    desc: "فلاشة كامون سي إكس كلاسيك",
    link: "https://drive.google.com/drive/folders/1iPD3U-Gy8QRMR4aIfiDpOdQGAh--n-Mj",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-cm",
    name: "TECNO CAMON CM CA6",
    rawKey: "tecno_camon_cm_ca6",
    series: "camon",
    ver: "CA6 Official Dump",
    desc: "فلاشة كامون سي إم الأصلية",
    link: "https://drive.google.com/drive/folders/1jCPkzP-8YuW7Zywln1JVTAJBHLpR4Pd0",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-c8",
    name: "TECNO CAMON C8 C8",
    rawKey: "tecno_camon_c8_c8",
    series: "camon",
    ver: "C8 Official Dump",
    desc: "فلاشة كامون C8 الكلاسيكية مع ملفات scatter",
    link: "https://drive.google.com/drive/folders/1jsGTx_JTCNIQnmXw2dDAo0UgPxGbK5ok",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-cam-c9",
    name: "TECNO CAMON C9 C9",
    rawKey: "tecno_camon_c9_c9",
    series: "camon",
    ver: "C9 Official Dump",
    desc: "فلاشة كامون C9 الرسمية مسحوبة ونظيفة",
    link: "https://drive.google.com/drive/folders/1kTU_3fttuP4Gq5ZvB99vkFoEoOQDWiyd",
    pass: "MobiFirmware.VIP"
  },

  // POVA SERIES
  {
    id: "tecno-pova-1",
    name: "TECNO POVA LD7",
    rawKey: "tecno_pova_ld7",
    series: "pova",
    ver: "LD7 Official Dump",
    desc: "فلاشة ودامب تكنو بوفا الأول بطارية 6000mAh",
    link: "https://drive.google.com/drive/folders/1TUKIpMGs3N8E72-s3NjfLTdKX_UHWAkC",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pova-2",
    name: "TECNO POVA 2 LE7",
    rawKey: "tecno_pova_2_le7",
    series: "pova",
    ver: "LE7 Official Dump",
    desc: "فلاشة بوفا 2 بطارية 7000mAh وشاشة عملاقة",
    link: "https://drive.google.com/drive/folders/1TqPyN9Tu0QNT9xCY0a-nlckxfgUadhxF",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pova-3",
    name: "TECNO POVA 3 LF7",
    rawKey: "tecno_pova_3_lf7",
    series: "pova",
    ver: "LF7 Official Dump",
    desc: "فلاشة تكنو بوفا 3 LF7 الرسمية",
    link: "https://drive.google.com/drive/folders/1U-iyUYdZSoG1tNlKbn7abn3jmb8NWB7T",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pova-4",
    name: "TECNO POVA 4 LG6",
    rawKey: "tecno_pova_4_lg6",
    series: "pova",
    ver: "LG6 Official Dump",
    desc: "فلاشة ودامب تكنو بوفا 4 معالج Helio G99",
    link: "https://drive.google.com/drive/folders/1Uby3PRJ1y2kNzRq_b0cFGu9rdAmaWm5b",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pova-4p",
    name: "TECNO POVA 4 Pro LG8",
    rawKey: "tecno_pova_4_pro_lg8",
    series: "pova",
    ver: "LG8 Official Dump",
    desc: "فلاشة بوفا 4 برو شاشة أموليد",
    link: "https://drive.google.com/drive/folders/1Ue7ghoXDkRPDqAFkhNp4Uig8v7Tgzo-M",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pova-5",
    name: "TECNO POVA 5 LH6",
    rawKey: "tecno_pova_5_lh6",
    series: "pova",
    ver: "LH6 Official Dump",
    desc: "فلاشة ودامب تكنو بوفا 5 LH6 الأصلية",
    link: "https://drive.google.com/drive/folders/1UzcWfXVs7tvdsF3zaZ-oQHsTM1w4cFB9",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pova-5p",
    name: "TECNO POVA 5 Pro LH8",
    rawKey: "tecno_pova_5_pro_lh8",
    series: "pova",
    ver: "LH8 Official Dump",
    desc: "فلاشة بوفا 5 برو إضاءة LED خلفية",
    link: "https://drive.google.com/drive/folders/1VHB_2vcwsLHRBv4bwyb0OwpANgh_p8Yj",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pova-5p-5g",
    name: "TECNO LH7N POVA 5 Pro 5G",
    rawKey: "tecno_lh7n_pova_5_pro_5g",
    series: "pova",
    ver: "LH7N 5G Official Dump",
    desc: "فلاشة بوفا 5 برو فايف جي موديل LH7N",
    link: "https://drive.google.com/drive/folders/1smKi3GKpYQ38qba6QAzvoiQKM-fnhlhJ",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pova-6",
    name: "TECNO POVA 6 LI6",
    rawKey: "tecno_pova_6_li6",
    series: "pova",
    ver: "LI6 Official Dump",
    desc: "فلاشة ودامب تكنو بوفا 6 LI6 أحدث سوفت وير",
    link: "https://drive.google.com/drive/folders/1W1WrXoLCrnXuGwVLrZKtZElDOI-qmiY1",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pova-6p",
    name: "TECNO POVA 6 Pro LI8",
    rawKey: "tecno_pova_6_pro_li8",
    series: "pova",
    ver: "LI8 Official Dump",
    desc: "فلاشة بوفا 6 برو 5G معالج Dimensity 6080",
    link: "https://drive.google.com/drive/folders/1WUS5Htr9HKfZSC3X2ix8sZseyHxNr6Ey",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pova-6-neo",
    name: "TECNO LI9 POVA 6 Neo",
    rawKey: "tecno_li9_pova_6_neo",
    series: "pova",
    ver: "LI9 Official Dump",
    desc: "دامب تكنو بوفا 6 نيو LI9 مسحوب كامل",
    link: "https://drive.google.com/drive/folders/1wn-NWGsD4485xfkBS_mBI9EsrS3lOqC4",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pova-curve",
    name: "TECNO POVA Curve LI8S",
    rawKey: "tecno_pova_curve_li8s",
    series: "pova",
    ver: "LI8S Curve Dump",
    desc: "فلاشة بوفا المنحني LI8S نادرة جداً",
    link: "https://drive.google.com/drive/folders/1zH2J5-kn7wemLKmUydwlwgxEpaxBTzyw",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pova-neo",
    name: "TECNO POVA Neo LE6",
    rawKey: "tecno_pova_neo_le6",
    series: "pova",
    ver: "LE6 Official Dump",
    desc: "فلاشة بوفا نيو LE6 الأصلية",
    link: "https://drive.google.com/drive/folders/1Wlx97JQPXcr6UOnSfxcoNg5PMaBsnYx3",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pova-neo-2",
    name: "TECNO POVA Neo 2 LG6N",
    rawKey: "tecno_pova_neo_2_lg6n",
    series: "pova",
    ver: "LG6N Official Dump",
    desc: "فلاشة بوفا نيو 2 LG6N بطارية 7000mAh",
    link: "https://drive.google.com/drive/folders/1WwDRbCtlGW3hqPXKq5RyFRdOcBlmqtqy",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pova-neo-3",
    name: "TECNO POVA Neo 3 LE6S",
    rawKey: "tecno_pova_neo_3_le6s",
    series: "pova",
    ver: "LE6S Official Dump",
    desc: "فلاشة بوفا نيو 3 LE6S الرسمية كاملة",
    link: "https://drive.google.com/drive/folders/1X3j2ps9BUKabqKGNvrEWxB5yx65YJz2M",
    pass: "MobiFirmware.VIP"
  },

  // POP SERIES
  {
    id: "tecno-pop-2",
    name: "TECNO POP 2 B1",
    rawKey: "tecno_pop_2_b1",
    series: "pop",
    ver: "B1 Official Dump",
    desc: "فلاشة ودامب تكنو بوب 2 B1",
    link: "https://drive.google.com/drive/folders/1XcOpSv2VT06_TRsTUy_OV6Lx-bStUt-k",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pop-2f",
    name: "TECNO POP 2F B1F",
    rawKey: "tecno_pop_2f_b1f",
    series: "pop",
    ver: "B1F Official Dump",
    desc: "فلاشة تكنو بوب 2 إف الرسمية",
    link: "https://drive.google.com/drive/folders/1XiqgNIWzb2f0NUS6LqRZR56ZF4n9xBo3",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pop-2p",
    name: "TECNO POP 2 Power B1P",
    rawKey: "tecno_pop_2_power_b1p",
    series: "pop",
    ver: "B1P Official Dump",
    desc: "فلاشة بوب 2 باور B1P",
    link: "https://drive.google.com/drive/folders/1XsLIkhWWT2CcxJWu5JwLKJFJn0avvil7",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pop-3",
    name: "TECNO POP 3 BB2",
    rawKey: "tecno_pop_3_bb2",
    series: "pop",
    ver: "BB2 Official Dump",
    desc: "فلاشة تكنو بوب 3 BB2",
    link: "https://drive.google.com/drive/folders/1XvdOQdzHOTd3ID3jaIuJk1Jeq-G5ALbv",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pop-4",
    name: "TECNO POP 4 BC2",
    rawKey: "tecno_pop_4_bc2",
    series: "pop",
    ver: "BC2 Official Dump",
    desc: "فلاشة ودامب تكنو بوب 4 BC2 كاملة",
    link: "https://drive.google.com/drive/folders/1XzL99j2NoLpTCLjHCj5uWdu-ivoHouL4",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pop-4a",
    name: "TECNO POP 4 Air BC1",
    rawKey: "tecno_pop_4_air_bc1",
    series: "pop",
    ver: "BC1 Official Dump",
    desc: "فلاشة تكنو بوب 4 إير BC1 الرسمية",
    link: "https://drive.google.com/drive/folders/1Y3CIQlAoSi8328AuT36NZdrCzxxfv60a",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pop-5",
    name: "TECNO POP 5 BD2",
    rawKey: "tecno_pop_5_bd2",
    series: "pop",
    ver: "BD2 Official Dump",
    desc: "فلاشة ودامب تكنو بوب 5 BD2",
    link: "https://drive.google.com/drive/folders/1YHq7GwqDLoRAHUlENzWMC51GMegjtCEW",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pop-5-lte",
    name: "TECNO POP 5 LTE BD4",
    rawKey: "tecno_pop_5_lte_bd4",
    series: "pop",
    ver: "BD4 Official Dump",
    desc: "فلاشة بوب 5 إل تي إي BD4 معالج سبريدترام",
    link: "https://drive.google.com/drive/folders/1YPiu-vapMTL960vE9rdce5D7shBrP3yz",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pop-5-go",
    name: "TECNO POP 5 Go BD1",
    rawKey: "tecno_pop_5_go_bd1",
    series: "pop",
    ver: "BD1 Official Dump",
    desc: "فلاشة تكنو بوب 5 جو BD1 مسحوبة",
    link: "https://drive.google.com/drive/folders/1YYPHeGty78_SBrn2qDCFu08kQDnyznqI",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pop-6",
    name: "TECNO POP 6 BE7",
    rawKey: "tecno_pop_6_be7",
    series: "pop",
    ver: "BE7 Official Dump",
    desc: "فلاشة ودامب تكنو بوب 6 BE7",
    link: "https://drive.google.com/drive/folders/1Yfp9Cj3hvE2vdEVxTe0qLw9rPocK7NcX",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pop-6-go",
    name: "TECNO POP 6 Go BE6",
    rawKey: "tecno_pop_6_go_be6",
    series: "pop",
    ver: "BE6 Official Dump",
    desc: "فلاشة تكنو بوب 6 جو BE6 الأصلية",
    link: "https://drive.google.com/drive/folders/1_T3F4BFVYFXg-qF4f0MTvtzuElzDzxaR",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pop-7",
    name: "TECNO POP 7 BF6",
    rawKey: "tecno_pop_7_bf6",
    series: "pop",
    ver: "BF6 Official Dump",
    desc: "فلاشة ودامب تكنو بوب 7 BF6",
    link: "https://drive.google.com/drive/folders/1_jMnJeKNEr0Kgxd2ydUOOIcKp4zMALY3",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pop-7-bf6m",
    name: "TECNO BF6 POP 7",
    rawKey: "tecno_bf6_pop_7",
    series: "pop",
    ver: "BF6 Version Dump",
    desc: "إصدار بديل من تكنو بوب 7 موديل BF6",
    link: "https://drive.google.com/drive/folders/1wpb569X4ljOHme4Z_8g4Pueaj2WqBAFZ",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pop-7p",
    name: "TECNO POP 7 Pro BF7H",
    rawKey: "tecno_pop_7_pro_bf7h",
    series: "pop",
    ver: "BF7H Official Dump",
    desc: "فلاشة بوب 7 برو BF7H الرسمية",
    link: "https://drive.google.com/drive/folders/1_w5Yl_YVMFa4QI5QADZPgP_nuzr4qTqh",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pop-8",
    name: "TECNO POP 8 BG6",
    rawKey: "tecno_pop_8_bg6",
    series: "pop",
    ver: "BG6 Official Dump",
    desc: "فلاشة ودامب تكنو بوب 8 BG6",
    link: "https://drive.google.com/drive/folders/1afEUxMLViJWmP5u7_UQXzrq0QiMp6y-D",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pop-8-bg6m",
    name: "TECNO BG6M POP 8",
    rawKey: "tecno_bg6m_pop_8",
    series: "pop",
    ver: "BG6M Official Dump",
    desc: "نسخة BG6M من تكنو بوب 8",
    link: "https://drive.google.com/drive/folders/1xOxdR5dx7ISLQFFpbIE0HYkF_UXrDOqh",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-pop-9",
    name: "TECNO POP 9 BG8",
    rawKey: "tecno_pop_9_bg8",
    series: "pop",
    ver: "BG8 Official Dump",
    desc: "فلاشة ودامب تكنو بوب 9 BG8 أحدث إصدار",
    link: "https://drive.google.com/drive/folders/1anFAH8BvWXw5_fncRu6gZ0m4SNO_hDaC",
    pass: "MobiFirmware.VIP"
  },

  // PHANTOM SERIES
  {
    id: "tecno-ph-6",
    name: "TECNO PHANTOM 6 A6",
    rawKey: "tecno_phantom_6_a6",
    series: "phantom",
    ver: "A6 Official Dump",
    desc: "فلاشة فانتوم 6 A6 الرسمية مع ملفات التفليش",
    link: "https://drive.google.com/drive/folders/1cFn6IPYeZGpHxnj4u9qwtYJSg6TB5pJN",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-ph-6p",
    name: "TECNO PHANTOM 6 Plus A9",
    rawKey: "tecno_phantom_6_plus_a9",
    series: "phantom",
    ver: "A9 Official Dump",
    desc: "فلاشة فانتوم 6 بلس A9 معالج عشاري الأنوية Helio X20",
    link: "https://drive.google.com/drive/folders/1cQA7kiXQPjRbpLli4ccBkFp_r4EkAUYK",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-ph-8",
    name: "TECNO PHANTOM 8 AX8",
    rawKey: "tecno_phantom_8_ax8",
    series: "phantom",
    ver: "AX8 Official Dump",
    desc: "فلاشة تكنو فانتوم 8 AX8 كاملة",
    link: "https://drive.google.com/drive/folders/1cXHqpQMT-_FhencX0moRlBiQ5yQ4fuPr",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-ph-9",
    name: "TECNO PHANTOM 9 AB7",
    rawKey: "tecno_phantom_9_ab7",
    series: "phantom",
    ver: "AB7 Official Dump",
    desc: "فلاشة فانتوم 9 AB7 شاشة أموليد وبصمة في الشاشة",
    link: "https://drive.google.com/drive/folders/1cxIxNMh9yBwEWLFWy1HPWwmMAkYdKTZA",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-ph-x",
    name: "TECNO PHANTOM X AC8",
    rawKey: "tecno_phantom_x_ac8",
    series: "phantom",
    ver: "AC8 Official Dump",
    desc: "فلاشة فانتوم إكس الفلاجشيب AC8 شاشة منحنية",
    link: "https://drive.google.com/drive/folders/1e2lYtYkZINZjjxKVctz3nJ6c53KlDTmD",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-ph-x2",
    name: "TECNO PHANTOM X2 AD8",
    rawKey: "tecno_phantom_x2_ad8",
    series: "phantom",
    ver: "AD8 Official Dump",
    desc: "فلاشة فانتوم X2 الرائدة معالج Dimensity 9000",
    link: "https://drive.google.com/drive/folders/1eJ-IeCyFFZ3QfCu7HvtOEsAmb7BcNOeJ",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-ph-x2p",
    name: "TECNO PHANTOM X2 Pro AD9",
    rawKey: "tecno_phantom_x2_pro_ad9",
    series: "phantom",
    ver: "AD9 Official Dump",
    desc: "فلاشة فانتوم X2 برو مع عدسة تصوير البورتريه المتحركة",
    link: "https://drive.google.com/drive/folders/1eJoaxxnI7gbPonJe5AxzhDGs0chwS6_L",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-ph-v-fold",
    name: "TECNO PHANTOM V Fold AD10",
    rawKey: "tecno_phantom_v_fold_ad10",
    series: "phantom",
    ver: "AD10 Fold Official Dump",
    desc: "فلاشة ودامب هاتف فانتوم القابل للطي V Fold AD10 كاملة",
    link: "https://drive.google.com/drive/folders/1f5AcRbxawfIYZEBSQlxjt_pHtogX5qZu",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-ph-v-flip",
    name: "TECNO PHANTOM V Flip AD11",
    rawKey: "tecno_phantom_v_flip_ad11",
    series: "phantom",
    ver: "AD11 Flip Official Dump",
    desc: "فلاشة هاتف فانتوم القابل للطي عمودياً V Flip AD11",
    link: "https://drive.google.com/drive/folders/1f_irEyI_ZAK9320eU9MN8MRwppgkVc8H",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-ph-v2-fold",
    name: "TECNO AD12 PHANTOM V2 Fold",
    rawKey: "tecno_ad12_phantom_v2_fold",
    series: "phantom",
    ver: "AD12 V2 Fold Dump",
    desc: "فلاشة الجيل الثاني من فانتوم V2 Fold موديل AD12",
    link: "https://drive.google.com/drive/folders/1xWcwiB_4i6wms_fpBsd6YMsv7IoX_Rw1",
    pass: "MobiFirmware.VIP"
  },

  // LEGACY W / F / L / OTHER MODELS
  {
    id: "tecno-wx3",
    name: "TECNO WX3 WX3",
    rawKey: "tecno_wx3_wx3",
    series: "other",
    ver: "WX3 Official Dump",
    desc: "فلاشة تكنو WX3 الكلاسيكية",
    link: "https://drive.google.com/drive/folders/1lhkiAMH8yub61EesvZQz9AAz_19KCepG",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-wx4",
    name: "TECNO WX4 WX4",
    rawKey: "tecno_wx4_wx4",
    series: "other",
    ver: "WX4 Official Dump",
    desc: "فلاشة تكنو WX4 الرسمية كاملة",
    link: "https://drive.google.com/drive/folders/1mWOpulIdNcOjCA9FlbRknrQnfbo_R7ua",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-w1",
    name: "TECNO W1 W1",
    rawKey: "tecno_w1_w1",
    series: "other",
    ver: "W1 Official Dump",
    desc: "فلاشة تكنو W1 الأصلية",
    link: "https://drive.google.com/drive/folders/1n7htCb91mB0ewlbRBNfklq__wz0Es4f7",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-w2",
    name: "TECNO W2 W2",
    rawKey: "tecno_w2_w2",
    series: "other",
    ver: "W2 Official Dump",
    desc: "فلاشة تكنو W2 الكلاسيكية",
    link: "https://drive.google.com/drive/folders/1nnXvU52FrCaUQe6gUH45TZFpo6KPflPD",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-w3",
    name: "TECNO W3 W3",
    rawKey: "tecno_w3_w3",
    series: "other",
    ver: "W3 Official Dump",
    desc: "فلاشة تكنو W3 الكلاسيكية الشهيرة",
    link: "https://drive.google.com/drive/folders/1nooB25MuhICQvAAUqG_NsubKmPJso7uX",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-w5",
    name: "TECNO W5 W5",
    rawKey: "tecno_w5_w5",
    series: "other",
    ver: "W5 Official Dump",
    desc: "فلاشة تكنو W5 الأصلية",
    link: "https://drive.google.com/drive/folders/1o3_P8i2VQcDJR7Ceb1Jk5Y4l_0p_KSDY",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-l8",
    name: "TECNO L8 L8",
    rawKey: "tecno_l8_l8",
    series: "other",
    ver: "L8 Official Dump",
    desc: "فلاشة تكنو L8 بطارية 5050mAh",
    link: "https://drive.google.com/drive/folders/1o7xBTah4TNngTb8NJmOshk_hW-oj3P60",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-l9p",
    name: "TECNO L9 Plus L9P",
    rawKey: "tecno_l9_plus_l9p",
    series: "other",
    ver: "L9P Official Dump",
    desc: "فلاشة تكنو L9 بلس الأصلية",
    link: "https://drive.google.com/drive/folders/1oiw6CekpmI_5a0LQcbS4AXCTrGUgaOEP",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-f1",
    name: "TECNO F1 F1",
    rawKey: "tecno_f1_f1",
    series: "other",
    ver: "F1 Official Dump",
    desc: "فلاشة تكنو F1 بنظام Android Go",
    link: "https://drive.google.com/drive/folders/1opniGT7fQFE7HNrPbo_eU5TsBDQvukz5",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-f2",
    name: "TECNO F2 F2",
    rawKey: "tecno_f2_f2",
    series: "other",
    ver: "F2 Official Dump",
    desc: "فلاشة تكنو F2 الرسمية",
    link: "https://drive.google.com/drive/folders/1p82ycxTBXapuOp7GfLjZ6I2NkQZ7JYNN",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-sa1s",
    name: "TECNO SA1S SA1S",
    rawKey: "tecno_sa1s_sa1s",
    series: "other",
    ver: "SA1S Official Dump",
    desc: "فلاشة تكنو SA1S نادرة مسحوبة كاملة",
    link: "https://drive.google.com/drive/folders/1pW14QX2HFu9OJVtA-8SQePpOLX1ebBHB",
    pass: "MobiFirmware.VIP"
  },
  {
    id: "tecno-spec-ext",
    name: "TECNO Special Edition Model",
    rawKey: "tecno_zybiq2eqxxkjt6tpq2t_gutwfv0qphss",
    series: "other",
    ver: "Rare Factory Dump",
    desc: "فلاشة ودامب إصدار حصري ونادر من هواتف TECNO",
    link: "https://drive.google.com/drive/folders/1zyBIQ2EqxxkJT6tpQ2t_gutwfV0qPHSS",
    pass: "MobiFirmware.VIP"
  }
];
