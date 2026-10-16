import { HMAX_DATA, ItemData } from './hmaxData';
import { FLASH_ERROR_DATABASE, FlashErrorItem } from './flashErrorDictionary';
import { TECNO_MODELS } from './tecnoModels';
import { LT_PHONES_CATALOG } from './ltPhonesData';
import { TESTPOINT_GUIDES, TestPointGuide } from './technicianToolsData';

export type PhoneResourceKind = 'dump' | 'firmware' | 'driver' | 'solution' | 'testpoint' | 'flash-error';

export interface PhoneResource {
  id: string;
  title: string;
  description: string;
  link?: string;
  version?: string;
  detail?: string[];
  note?: string;
}

export interface PhoneResourceGroup {
  kind: PhoneResourceKind;
  title: string;
  resources: PhoneResource[];
  emptyMessage: string;
}

export interface PhoneSearchResult {
  id: string;
  brandId: string;
  brand: string;
  name: string;
  modelNumber?: string;
  subtitle: string;
  searchText: string;
  sourceTestPointId?: string;
  groups: PhoneResourceGroup[];
}

const BRAND_ALIASES: Record<string, string[]> = {
  allcall: ['allcall', 'all call', 'ال كول'],
  kxd: ['kxd'],
  hmd: ['hmd', 'nokia'],
  benco: ['benco', 'بينكو'],
  honor: ['honor', 'honour', 'honor', 'هونر'],
  hisorl: ['hisorl'],
  blackview: ['blackview', 'black view'],
  huawei: ['huawei', 'هواوي', 'honor', 'هونر'],
  nokia: ['nokia', 'نوكيا', 'hmd'],
  infinix: ['infinix', 'انفنكس', 'إنفينيكس'],
  itel: ['itel', 'ايتل', 'إيتل'],
  mhorse: ['m-horse', 'mhorse', 'm horse', 'horse'],
  oppo: ['oppo', 'اوبو', 'أوبو'],
  realme: ['realme', 'ريلمي'],
  samsung: ['samsung', 'سامسونج', 'galaxy'],
  xiaomi: ['xiaomi', 'شاومي', 'redmi', 'ريدمي', 'poco', 'بوكـو', 'poco'],
  tecno: ['tecno', 'تكنو'],
  lt: ['lt mobile', 'lt', 'ال تي'],
  vivo: ['vivo', 'فيفو'],
  wiko: ['wiko'],
  villaon: ['villaon'],
  tab: ['tab', 'ytab', 'tablet'],
  zte: ['zte', 'زد تي اي'],
  motorola: ['motorola', 'moto', 'موتورولا'],
  copy: ['copy', 'clone', 'كوبي', 'مقلد'],
  iphone_copy: ['iphone copy', 'iphone clone', 'ايفون كوبي'],
  other: ['other', 'others', 'اخرى', 'أخرى'],
};

const BRAND_DRIVERS: Record<string, string[]> = {
  samsung: ['samsung', 'exynos', 'adb driver'],
  huawei: ['huawei', 'qcom', 'qualcomm', 'adb driver', 'vcom'],
  honor: ['huawei', 'qcom', 'qualcomm', 'adb driver', 'vcom'],
  xiaomi: ['fastboot', 'qcom', 'qualcomm', 'mtk', 'mediatek', 'adb driver'],
  tecno: ['mtk', 'mediatek', 'spd', 'spreadtrum', 'unisoc', 'adb driver'],
  infinix: ['mtk', 'mediatek', 'spd', 'spreadtrum', 'unisoc', 'adb driver'],
  itel: ['mtk', 'mediatek', 'spd', 'spreadtrum', 'unisoc', 'adb driver'],
  vivo: ['vivo', 'mtk', 'mediatek', 'qcom', 'qualcomm', 'adb driver'],
  oppo: ['oppo', 'mtk', 'mediatek', 'qcom', 'qualcomm', 'adb driver'],
  realme: ['oppo', 'realme', 'mtk', 'mediatek', 'qcom', 'qualcomm', 'adb driver'],
  motorola: ['motorola', 'fastboot', 'adb driver', 'qcom', 'qualcomm'],
  nokia: ['nokia', 'spd', 'spreadtrum', 'unisoc', 'mtk', 'mediatek', 'adb driver'],
  hmd: ['nokia', 'spd', 'spreadtrum', 'unisoc', 'mtk', 'mediatek', 'adb driver'],
};

const BRAND_FIRMWARE_WORDS: Record<string, string[]> = {
  samsung: ['samsung', 'samfw'],
  xiaomi: ['xiaomi', 'mifirm', 'redmi', 'poco'],
  realme: ['realme'],
  oppo: ['oppo'],
  vivo: ['vivo'],
  tecno: ['tecno'],
  itel: ['itel'],
  motorola: ['motorola'],
  huawei: ['huawei'],
  honor: ['honor'],
  zte: ['zte'],
  wiko: ['wiko'],
  nokia: ['nokia', 'hmd'],
  hmd: ['nokia', 'hmd'],
};

const normalize = (value: string): string => value
  .toLocaleLowerCase()
  .normalize('NFD')
  .replace(/[\u0300-\u036f\u064b-\u065f\u0670]/g, '')
  .replace(/[٠-٩]/g, (digit) => String('٠١٢٣٤٥٦٧٨٩'.indexOf(digit)))
  .replace(/[۰-۹]/g, (digit) => String('۰۱۲۳۴۵۶۷۸۹'.indexOf(digit)))
  .replace(/[^\p{L}\p{N}]+/gu, ' ')
  .trim();

const brandLabel = (brandId: string): string =>
  HMAX_DATA.dump_brands.find((brand) => brand.id === brandId)?.name ?? brandId.toUpperCase();

const resolveBrandId = (brandText: string): string => {
  const normalizedBrand = normalize(brandText);
  const match = Object.entries(BRAND_ALIASES).find(([, aliases]) =>
    aliases.some((alias) => normalizedBrand.includes(normalize(alias)) || normalize(alias).includes(normalizedBrand))
  );
  return match?.[0] ?? 'other';
};

const resourceFromItem = (item: ItemData, note?: string): PhoneResource => ({
  id: item.id,
  title: item.name,
  description: item.desc ?? '',
  link: item.link,
  version: item.ver,
  note,
});

const profileSpecs: Array<Pick<PhoneSearchResult, 'id' | 'brandId' | 'brand' | 'name' | 'modelNumber' | 'subtitle' | 'searchText' | 'sourceTestPointId'>> = [];
const dumpItemsByProfile = new Map<string, ItemData[]>();

for (const [brandId, items] of Object.entries(HMAX_DATA.dump_cards)) {
  for (const item of items) {
    const profileId = `dump:${brandId}:${item.id}`;
    const aliases = BRAND_ALIASES[brandId] ?? [brandId];
    const modelNumber = item.ver && /\d/.test(item.ver) ? item.ver : undefined;
    profileSpecs.push({
      id: profileId,
      brandId,
      brand: brandLabel(brandId),
      name: item.name,
      modelNumber,
      subtitle: item.desc || item.ver || 'سجل موجود في مستودع ملفات الأجهزة',
      searchText: normalize(`${aliases.join(' ')} ${brandLabel(brandId)} ${item.name} ${item.ver ?? ''} ${item.desc ?? ''}`),
    });
    dumpItemsByProfile.set(profileId, [item]);
  }
}

// These catalogs also contain the model name and searchable codes for the dedicated dump sections.
const existingDumpItemIds = new Set(Object.values(HMAX_DATA.dump_cards).flat().map((item) => item.id));
for (const [brandId, catalog] of [['tecno', TECNO_MODELS], ['lt', LT_PHONES_CATALOG]] as const) {
  for (const item of catalog) {
    const profileId = `catalog:${brandId}:${item.id}`;
    if (existingDumpItemIds.has(item.id) || profileSpecs.some((profile) => profile.id === profileId)) continue;
    profileSpecs.push({
      id: profileId,
      brandId,
      brand: brandLabel(brandId),
      name: item.name,
      modelNumber: item.ver,
      subtitle: item.desc ?? item.ver ?? '',
      searchText: normalize(`${(BRAND_ALIASES[brandId] ?? [brandId]).join(' ')} ${item.name} ${item.ver ?? ''} ${item.desc ?? ''} ${'rawKey' in item ? item.rawKey : ''}`),
    });
    dumpItemsByProfile.set(profileId, [item]);
  }
}

for (const guide of TESTPOINT_GUIDES) {
  const brandId = resolveBrandId(guide.brand);
  const profileId = `testpoint:${guide.id}`;
  profileSpecs.push({
    id: profileId,
    brandId,
    brand: brandLabel(brandId),
    name: guide.model,
    modelNumber: guide.chipset,
    subtitle: `نقطة اختبار موثقة • ${guide.mode} • ${guide.chipset}`,
    searchText: normalize(`${(BRAND_ALIASES[brandId] ?? [brandId]).join(' ')} ${guide.brand} ${guide.model} ${guide.chipset}`),
    sourceTestPointId: guide.id,
  });
}

const textGuideResources: Array<PhoneResource & { searchText: string }> = HMAX_DATA.solutions.text_guides.map((guide) => ({
  id: `guide:${guide.id}`,
  title: guide.title,
  description: `${guide.tag} — ${guide.problem}`,
  detail: guide.steps.map((step) => step.text),
  note: guide.conclusionNote ?? ('warningNote' in guide ? guide.warningNote : undefined),
  searchText: normalize(`${guide.title} ${guide.tag} ${guide.problem} ${guide.solutionIntro} ${guide.steps.map((step) => step.text).join(' ')} ${guide.conclusionNote ?? ''}`),
}));

const experienceResources: Array<PhoneResource & { searchText: string }> = HMAX_DATA.solutions.experiences.map((experience) => ({
  id: `experience:${experience.id}`,
  title: experience.title,
  description: `${experience.problem} ${experience.solutionDesc ?? ''}`.trim(),
  detail: experience.solutionSteps?.map((step) => step.text),
  link: experience.links.find((link) => link.primary)?.url ?? experience.links[0]?.url,
  note: experience.warning,
  searchText: normalize(`${experience.title} ${experience.author} ${experience.problem} ${experience.solutionDesc ?? ''} ${experience.solutionSteps?.map((step) => step.text).join(' ') ?? ''}`),
}));

const generalSolutionResources: Array<PhoneResource & { searchText: string }> = [
  ...HMAX_DATA.solutions.youtube,
  ...HMAX_DATA.solutions.volte,
  ...HMAX_DATA.solutions.rasheed,
  ...HMAX_DATA.solutions.haitham,
].map((item) => ({
  id: `solution:${item.id}`,
  title: item.name,
  description: item.desc ?? '',
  link: item.link,
  searchText: normalize(`${item.name} ${item.desc ?? ''} ${'ver' in item ? item.ver : ''}`),
}));

const solutionResources: Array<PhoneResource & { searchText: string }> = [
  ...textGuideResources,
  ...experienceResources,
  ...generalSolutionResources,
];

const errorResource = (error: FlashErrorItem): PhoneResource => ({
  id: error.id,
  title: `${error.code} — ${error.title}`,
  description: error.meaning,
  version: error.tool,
  detail: error.solutionSteps,
  note: error.recommendedToolOrDriver,
});

const brandSpecificTokens = (profile: typeof profileSpecs[number]): string[] => {
  const ignored = new Set(['official', 'dump', 'full', 'rom', 'stock', 'firmware', 'android', 'flash', 'file', 'version', 'pro', 'max', 'gb', 'tool', 'samsung', 'galaxy', 'xiaomi', 'redmi', 'poco', 'tecno', 'infinix', 'itel', 'vivo', 'huawei', 'honor', 'oppo', 'realme', 'motorola', 'nokia', 'hmd']);
  return normalize(`${profile.name} ${profile.modelNumber ?? ''}`)
    .split(' ')
    .filter((token) => token.length >= 2 && !ignored.has(token));
};

const matchesTestPoint = (profile: typeof profileSpecs[number], guide: TestPointGuide): boolean => {
  if (profile.sourceTestPointId === guide.id) return true;
  if (resolveBrandId(guide.brand) !== profile.brandId) return false;
  const guideTokens = new Set(normalize(guide.model).split(' '));
  return brandSpecificTokens(profile).some((token) =>
    (token.length >= 3 || /\d/.test(token)) && guideTokens.has(token)
  );
};

const driverMatches = (brandId: string, item: ItemData): boolean => {
  const keys = BRAND_DRIVERS[brandId] ?? [];
  const searchable = normalize(`${item.name} ${item.desc ?? ''}`);
  return keys.some((key) => searchable.includes(normalize(key)));
};

const firmwareMatches = (brandId: string, item: ItemData): boolean => {
  const keys = BRAND_FIRMWARE_WORDS[brandId] ?? [];
  const searchable = normalize(`${item.name} ${item.desc ?? ''}`);
  return keys.some((key) => searchable.includes(normalize(key)));
};

const buildGroups = (profile: typeof profileSpecs[number]): PhoneResourceGroup[] => {
  const aliases = BRAND_ALIASES[profile.brandId] ?? [profile.brandId];
  const testPoints = TESTPOINT_GUIDES.filter((guide) => matchesTestPoint(profile, guide));
  const modelTokens = brandSpecificTokens(profile);
  const brandSearchTokens = aliases.map(normalize).filter((alias) => alias.length > 2);

  const matchedSolutions = solutionResources.filter((resource) => {
    const matchesModel = modelTokens.some((token) => token.length >= 3 && resource.searchText.includes(token));
    const matchesBrand = brandSearchTokens.some((alias) => resource.searchText.includes(alias));
    return matchesModel || matchesBrand;
  }).slice(0, 10);

  const brandText = normalize(`${profile.brand} ${profile.name} ${profile.modelNumber ?? ''} ${testPoints.map((point) => point.chipset).join(' ')}`);
  const relevantErrorTools = new Set<FlashErrorItem['tool']>();
  if (profile.brandId === 'samsung') relevantErrorTools.add('Samsung Odin');
  if (/qualcomm|snapdragon|qcom|edl/.test(brandText)) relevantErrorTools.add('Qualcomm EDL / QFIL');
  if (/unisoc|spreadtrum|\bspd\b|sc9863|t606/.test(brandText)) relevantErrorTools.add('Unisoc SPD');
  if (/mediatek|\bmtk\b|helio|brom/.test(brandText)) {
    relevantErrorTools.add('SP Flash Tool');
    relevantErrorTools.add('UnlockTool / Pandora');
  }
  const matchedErrors = relevantErrorTools.size
    ? FLASH_ERROR_DATABASE.filter((error) => relevantErrorTools.has(error.tool))
    : FLASH_ERROR_DATABASE;

  const dumpResources = (dumpItemsByProfile.get(profile.id) ?? []).map((item) => resourceFromItem(
    item,
    'الملف مسجل في فهرس المشروع؛ تحقق من رقم اللوحة وإصدار الحماية قبل التفليش.'
  ));
  const firmwareResources = HMAX_DATA.firmware_sites
    .filter((item) => firmwareMatches(profile.brandId, item))
    .map((item) => resourceFromItem(item, 'مصدر عام لملفات هذه الماركة، وليس تأكيداً لتوافقه مع رقم الطراز.'));
  const driverResources = HMAX_DATA.drivers
    .filter((item) => driverMatches(profile.brandId, item))
    .slice(0, 8)
    .map((item) => resourceFromItem(item, 'تعريف محتمل حسب الماركة/المعالج؛ طابق وضع USB ونوع الشريحة قبل التثبيت.'));
  const testPointResources = testPoints.map((guide) => ({
    id: guide.id,
    title: `${guide.brand} ${guide.model}`,
    description: guide.instructions,
    version: `${guide.mode} • ${guide.chipset}`,
    detail: [guide.tpPoint, guide.pinoutNotes],
    note: 'افصل الطاقة واتبع مخطط الموديل بدقة؛ لا تستخدم نقطة مشابهة على لوحة مختلفة.',
  }));
  const solutionResults = matchedSolutions.map((resource) => ({
    id: resource.id,
    title: resource.title,
    description: resource.description,
    link: resource.link,
    detail: resource.detail,
    note: resource.note,
  }));

  return [
    { kind: 'dump', title: 'ملفات الفلاش وDUMP', resources: dumpResources, emptyMessage: 'لا يوجد ملف مسجل لهذا الموديل حالياً.' },
    { kind: 'firmware', title: 'مصادر الفلاش الرسمية', resources: firmwareResources, emptyMessage: 'لا يوجد مصدر فلاش عام لهذه الماركة ضمن الفهرس.' },
    { kind: 'driver', title: 'التعاريف المحتملة', resources: driverResources, emptyMessage: 'لا توجد تعريفات مقترحة لهذه الماركة في الفهرس.' },
    { kind: 'solution', title: 'الحلول والشروحات', resources: solutionResults, emptyMessage: 'لا توجد حلول مرتبطة بهذا الموديل/الماركة في قاعدة المحتوى الحالية.' },
    { kind: 'testpoint', title: 'نقاط Test Point', resources: testPointResources, emptyMessage: 'لا توجد نقطة اختبار موثقة لهذا الطراز في قاعدة البيانات الحالية.' },
    { kind: 'flash-error', title: 'مساعدة أخطاء التفليش', resources: matchedErrors.map(errorResource), emptyMessage: 'لا توجد مراجع خطأ مناسبة.' },
  ];
};

const PHONE_INDEX: PhoneSearchResult[] = profileSpecs.map((profile) => ({
  ...profile,
  groups: buildGroups(profile),
}));

const editDistance = (left: string, right: string): number => {
  if (Math.abs(left.length - right.length) > 2) return 3;
  let previous = Array.from({ length: right.length + 1 }, (_, index) => index);
  for (let row = 1; row <= left.length; row += 1) {
    const current = [row];
    for (let column = 1; column <= right.length; column += 1) {
      current[column] = Math.min(
        current[column - 1] + 1,
        previous[column] + 1,
        previous[column - 1] + (left[row - 1] === right[column - 1] ? 0 : 1),
      );
    }
    previous = current;
  }
  return previous[right.length];
};

export const searchPhoneModels = (query: string, limit = 8): PhoneSearchResult[] => {
  const normalizedQuery = normalize(query);
  const terms = normalizedQuery.split(' ').filter((term) => term.length > 1);
  if (terms.length === 0) return [];

  const exactMatches = PHONE_INDEX.map((profile) => {
    const searchable = profile.searchText;
    if (!terms.every((term) => searchable.includes(term))) return null;
    const name = normalize(profile.name);
    const score = (name === normalizedQuery ? 120 : 0)
      + (name.startsWith(normalizedQuery) ? 50 : 0)
      + terms.reduce((total, term) => total + (name.includes(term) ? 12 : 0), 0)
      + (profile.sourceTestPointId ? 4 : 0);
    return { profile, score };
  })
    .filter((match): match is { profile: PhoneSearchResult; score: number } => match !== null)
    .sort((a, b) => b.score - a.score || a.profile.name.localeCompare(b.profile.name))
    .slice(0, limit)
    .map(({ profile }) => profile);

  if (exactMatches.length > 0) return exactMatches;

  // Only offer typo-tolerant suggestions when the normal search has no hit;
  // require every query token to be close to an indexed word to avoid noise.
  return PHONE_INDEX.map((profile) => {
    const words = [...new Set(profile.searchText.split(' '))].filter((word) => word.length >= 3);
    let totalDistance = 0;
    for (const term of terms) {
      if (term.length < 4) {
        if (!words.includes(term)) return null;
        continue;
      }
      const maxDistance = term.length >= 8 ? 2 : 1;
      const closest = words.reduce((best, word) => Math.min(best, editDistance(term, word)), 3);
      if (closest > maxDistance) return null;
      totalDistance += closest;
    }
    const name = normalize(profile.name);
    const score = 10 - totalDistance + terms.reduce((total, term) => total + (name.includes(term) ? 2 : 0), 0);
    return { profile, score };
  })
    .filter((match): match is { profile: PhoneSearchResult; score: number } => match !== null)
    .sort((a, b) => b.score - a.score || a.profile.name.localeCompare(b.profile.name))
    .slice(0, limit)
    .map(({ profile }) => profile);
};

export const PHONE_SEARCH_COUNTS = {
  models: PHONE_INDEX.length,
  testPoints: TESTPOINT_GUIDES.length,
  flashErrors: FLASH_ERROR_DATABASE.length,
};
