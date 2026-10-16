export interface DecodedSamsungFirmware {
  raw: string;
  model: string;
  region: string;
  binaryBit: string;
  androidLetter: string;
  year: string;
  month: string;
  revision: string;
  isRecognized: boolean;
  notes: string[];
  safeDowngradeTo: string[];
}

const YEAR_CODES: Record<string, string> = {
  'A': '2001', 'B': '2002', 'C': '2003', 'D': '2004', 'E': '2005',
  'F': '2006', 'G': '2007', 'H': '2008', 'I': '2009', 'J': '2010',
  'K': '2011', 'L': '2012', 'M': '2013', 'N': '2014', 'O': '2015',
  'P': '2016', 'Q': '2017', 'R': '2018', 'S': '2019', 'T': '2020',
  'U': '2021', 'V': '2022', 'W': '2023', 'X': '2024', 'Y': '2025',
  'Z': '2026'
};

const MONTH_CODES: Record<string, string> = {
  'A': 'يناير (January)',
  'B': 'فبراير (February)',
  'C': 'مارس (March)',
  'D': 'أبريل (April)',
  'E': 'مايو (May)',
  'F': 'يونيو (June)',
  'G': 'يوليو (July)',
  'H': 'أغسطس (August)',
  'I': 'سبتمبر (September)',
  'J': 'أكتوبر (October)',
  'K': 'نوفمبر (November)',
  'L': 'ديسمبر (December)'
};

export function decodeSamsungFirmware(buildCode: string): DecodedSamsungFirmware {
  const clean = buildCode.trim().toUpperCase();
  if (clean.length < 12) {
    return {
      raw: clean,
      model: '—',
      region: '—',
      binaryBit: '—',
      androidLetter: '—',
      year: '—',
      month: '—',
      revision: '—',
      isRecognized: false,
      notes: ['الكود المدخل قصير جداً، تأكد من كتابة كود الإصدار الكامل (مثال: A546EXXS5BXA1 أو S908BXXU4CWK3)'],
      safeDowngradeTo: []
    };
  }

  // Common Samsung Build structure: [Model][Region/Carrier][Bootloader/Binary][OS Letter][Year][Month][Revision]
  // e.g., A546E XX S 5 B X A 1 -> Binary is at index len - 5
  const len = clean.length;
  const binaryChar = clean.charAt(len - 5);
  const osLetter = clean.charAt(len - 4);
  const yearChar = clean.charAt(len - 3);
  const monthChar = clean.charAt(len - 2);
  const revChar = clean.charAt(len - 1);

  const yearName = YEAR_CODES[yearChar] || `سنة مشفرة (${yearChar})`;
  const monthName = MONTH_CODES[monthChar] || `شهر مشفر (${monthChar})`;

  const binaryNumber = parseInt(binaryChar, 10);
  const isNumericBinary = !isNaN(binaryNumber);

  const notes: string[] = [];
  if (isNumericBinary) {
    notes.push(`رقم الحماية الثنائية المعتمد هو: Bit / Binary ${binaryNumber} (أو U${binaryNumber} / S${binaryNumber}).`);
    notes.push(`قاعدة سامسونج الصارمة: يُسمح بتفليش أي فلاشة تحمل نفس رقم الحماية (${binaryNumber}) أو أعلى (≥ ${binaryNumber}).`);
    notes.push(`تحذير أمني: يمنع منعاً باتاً تفليش فلاشة بحماية أقل (< ${binaryNumber}) لأن الهاتف سيرفضها فوراً بخطأ SW REV CHECK FAIL.`);
  } else {
    notes.push(`الحماية محددة بالحرف: ${binaryChar}`);
  }

  return {
    raw: clean,
    model: clean.slice(0, 5),
    region: clean.slice(5, 7),
    binaryBit: binaryChar,
    androidLetter: osLetter,
    year: yearName,
    month: monthName,
    revision: revChar,
    isRecognized: true,
    notes,
    safeDowngradeTo: isNumericBinary ? [`U${binaryNumber}`, `S${binaryNumber}`] : []
  };
}

export const SAMPLE_SAMSUNG_BUILDS = [
  { label: 'Galaxy A54 5G (Bit 5 / 2026)', code: 'A546EXXS5BXA1', desc: 'حماية حديثة Bit 5' },
  { label: 'Galaxy S22 Ultra (Bit 4 / Android 14)', code: 'S908BXXU4CWK3', desc: 'حماية Bit 4 المستقرة' },
  { label: 'Galaxy S24 Ultra (Bit 2 / One UI 6.1)', code: 'S928BXXU2AXB5', desc: 'أحدث فلاشات معالج Snapdragon 8 Gen 3' },
  { label: 'Galaxy A14 4G (Bit 6 / One UI)', code: 'A145FXXU6CXC2', desc: 'حماية Bit 6 المرتفعة' },
  { label: 'Galaxy Note 20 Ultra (Bit 8)', code: 'N986BXXS8HXE1', desc: 'آخر تحديثات الحماية لسلسلة النوت' }
];
