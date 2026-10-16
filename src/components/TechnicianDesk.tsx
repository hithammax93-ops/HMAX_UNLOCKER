import React, { useMemo, useState } from 'react';
import { AlertTriangle, BookOpenCheck, CheckCircle2, Clipboard, Database, HardDrive, Info, Plus, Search, ShieldCheck, Smartphone, Trash2, Wrench } from 'lucide-react';
import { searchPhoneModels, PhoneSearchResult } from '../data/unifiedPhoneSearch';

type DeskMode = 'compatibility' | 'diagnostics' | 'device_log';
interface TechnicianDeskProps { mode: DeskMode; onCopyToast?: (message: string) => void; }
interface LocalDeviceNote {
  id: string;
  deviceName: string;
  modelNumber: string;
  issue: string;
  note: string;
  updatedAt: string;
}
const STORAGE_KEY = 'hmax_device_notes_local_v1';
const normalize = (value: string) => value.toLocaleLowerCase().normalize('NFD').replace(/[\u0300-\u036f\u064b-\u065f\u0670]/g, '').replace(/[٠-٩]/g, (digit) => String('٠١٢٣٤٥٦٧٨٩'.indexOf(digit))).replace(/[۰-۹]/g, (digit) => String('۰۱۲۳۴۵۶۷۸۹'.indexOf(digit))).replace(/[^\p{L}\p{N}]+/gu, ' ').trim();
const readDeviceNotes = (): LocalDeviceNote[] => {
  try {
    const value = localStorage.getItem(STORAGE_KEY);
    const parsed = value ? JSON.parse(value) : [];
    return Array.isArray(parsed) ? parsed : [];
  } catch { return []; }
};

const warningBox = 'rounded-xl border border-amber-500/25 bg-amber-500/[0.07] p-3 text-xs leading-relaxed text-amber-200/90';
const card = 'rounded-2xl border border-slate-800 bg-slate-900/75 p-4';
const inputClass = 'w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2.5 text-sm text-white outline-none placeholder:text-slate-500 focus:border-[#00b4ff]';

export const TechnicianDesk: React.FC<TechnicianDeskProps> = ({ mode, onCopyToast }) => {
  const [brand, setBrand] = useState('');
  const [deviceName, setDeviceName] = useState('');
  const [modelNumber, setModelNumber] = useState('');
  const [chipset, setChipset] = useState('');
  const [checked, setChecked] = useState(false);
  const [symptom, setSymptom] = useState('');
  const [diagnosisStarted, setDiagnosisStarted] = useState(false);
  const [notes, setNotes] = useState<LocalDeviceNote[]>(readDeviceNotes);
  const [newDeviceName, setNewDeviceName] = useState('');
  const [newModelNumber, setNewModelNumber] = useState('');
  const [newIssue, setNewIssue] = useState('');
  const [newNote, setNewNote] = useState('');
  const [savedLocally, setSavedLocally] = useState(true);

  React.useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(notes));
      setSavedLocally(true);
    } catch { setSavedLocally(false); }
  }, [notes]);

  const exactMatches = useMemo(() => {
    if (!checked || !modelNumber.trim()) return [];
    const code = normalize(modelNumber);
    const model = normalize(deviceName);
    const queryMatches = searchPhoneModels(`${deviceName} ${modelNumber}`, 30);
    const codeMatches = searchPhoneModels(modelNumber, 30);
    const candidates = [...new Map([...queryMatches, ...codeMatches].map((item) => [item.id, item])).values()];
    return candidates.filter((item) => {
      const indexedNumber = normalize(item.modelNumber ?? '');
      const indexedWords = new Set(normalize(`${item.name} ${item.modelNumber ?? ''} ${item.searchText}`).split(' '));
      const codeTerms = code.split(' ').filter(Boolean);
      const modelTerms = model.split(' ').filter(Boolean);
      const brandTerms = normalize(brand).split(' ').filter(Boolean);
      const codeFound = indexedNumber === code || (codeTerms.length > 0 && codeTerms.every((term) => indexedWords.has(term)));
      const nameFound = modelTerms.every((term) => indexedWords.has(term));
      const brandFound = brandTerms.every((term) => indexedWords.has(term));
      return codeFound && nameFound && brandFound;
    });
  }, [brand, checked, deviceName, modelNumber]);

  const suggestions = useMemo(() => {
    if (!checked || exactMatches.length || !modelNumber.trim()) return [];
    return searchPhoneModels(modelNumber, 5);
  }, [checked, exactMatches.length, modelNumber]);

  const addNote = (event: React.FormEvent) => {
    event.preventDefault();
    if (!newDeviceName.trim() || !newModelNumber.trim() || !newIssue.trim()) return;
    const item: LocalDeviceNote = {
      id: `device-note-${Date.now()}`,
      deviceName: newDeviceName.trim(),
      modelNumber: newModelNumber.trim(),
      issue: newIssue.trim(),
      note: newNote.trim(),
      updatedAt: new Date().toISOString(),
    };
    setNotes((current) => [item, ...current]);
    setNewDeviceName(''); setNewModelNumber(''); setNewIssue(''); setNewNote('');
    onCopyToast?.('حُفظت الملاحظة على هذا الجهاز فقط');
  };

  const deleteNote = (id: string) => setNotes((current) => current.filter((item) => item.id !== id));
  const copyText = async (text: string) => {
    try { await navigator.clipboard.writeText(text); onCopyToast?.('تم النسخ'); }
    catch { onCopyToast?.('تعذر النسخ؛ حدّد النص وانسخه يدويًا'); }
  };
  const shareDraft = async (text: string) => {
    try {
      if (navigator.share) await navigator.share({ title: 'مشاركة طلب HMAX', text });
      else await copyText(text);
    } catch (error) {
      if (error instanceof Error && error.name !== 'AbortError') await copyText(text);
    }
  };

  if (mode === 'compatibility') return (
    <section className="space-y-4">
      <header className={card}>
        <div className="flex items-center gap-2 text-[#00b4ff]"><ShieldCheck className="h-5 w-5" /><h2 className="text-base font-black text-white">فاحص التوافق حسب رقم الطراز</h2></div>
        <p className="mt-2 text-xs leading-relaxed text-slate-400">أدخل الشركة واسم الجهاز ورقم الموديل الدقيق كما يظهر على الملصق أو في Download/Fastboot Mode، ثم نبحث في الفهرس المحلي.</p>
      </header>
      <form className={`${card} grid gap-3 sm:grid-cols-2`} onSubmit={(event) => { event.preventDefault(); setChecked(true); }}>
        <label className="space-y-1 text-xs text-slate-300">الشركة<input className={inputClass} value={brand} onChange={(event) => setBrand(event.target.value)} placeholder="مثال: Samsung" /></label>
        <label className="space-y-1 text-xs text-slate-300">اسم الجهاز *<input required className={inputClass} value={deviceName} onChange={(event) => setDeviceName(event.target.value)} placeholder="مثال: Galaxy A14" /></label>
        <label className="space-y-1 text-xs text-slate-300">رقم الطراز الدقيق *<input required className={`${inputClass} font-mono`} value={modelNumber} onChange={(event) => setModelNumber(event.target.value)} placeholder="مثال: SM-A145F" /></label>
        <label className="space-y-1 text-xs text-slate-300">المعالج (اختياري)<input className={inputClass} value={chipset} onChange={(event) => setChipset(event.target.value)} placeholder="مثال: MTK / Exynos / Qualcomm" /></label>
        <button className="sm:col-span-2 inline-flex min-h-11 items-center justify-center gap-2 rounded-xl bg-[#00b4ff] px-4 py-2 text-sm font-black text-slate-950" type="submit"><Search className="h-4 w-4" />تحقق من الفهرس</button>
      </form>
      {checked && <div className="space-y-3">
        <div className={warningBox}><AlertTriangle className="ml-1 inline h-4 w-4" /> نتيجة الفهرس ليست ضمانًا للتوافق. طابق رقم اللوحة، إصدار المنطقة/الحماية والمعالج، وتحقق من مصدر الملف وبصمته قبل التفليش. لا يعرض التطبيق ملفًا على أنه مناسب لمجرد تشابه الاسم.</div>
        {exactMatches.length > 0 ? exactMatches.map((phone) => <CompatibilityResult key={phone.id} phone={phone} brand={brand} chipset={chipset} onCopy={copyText} onReport={() => shareDraft(`بلاغ توافق HMAX\nالشركة: ${brand || 'غير محددة'}\nالجهاز: ${deviceName}\nرقم الطراز: ${modelNumber}\nالمعالج: ${chipset || 'غير محدد'}\nالعنصر: ${phone.name}\nيرجى مراجعة توافق المورد.`)} />) : (
          <div className={`${card} text-sm text-slate-300`}>
            <p className="font-bold">لم نعثر على تطابق حرفي يجمع اسم الجهاز ورقم الطراز في الفهرس.</p>
            {suggestions.length > 0 && <div className="mt-3 space-y-2"><p className="text-xs text-amber-300">اقتراحات قريبة فقط — ليست نتائج توافق:</p>{suggestions.map((phone) => <div key={phone.id} className="rounded-xl border border-slate-800 bg-slate-950 p-3"><b>{phone.brand} {phone.name}</b><span className="mr-2 font-mono text-xs text-slate-400">{phone.modelNumber || 'رقم طراز غير مسجل'}</span></div>)}</div>}
            {!suggestions.length && <p className="mt-2 text-xs text-slate-500">جرّب مراجعة كتابة الرمز، أو أرسل طلب إضافة طراز غير موجود.</p>}
            <button onClick={() => shareDraft(`طلب إضافة طراز/شرح إلى HMAX\nالشركة: ${brand || 'غير محددة'}\nاسم الجهاز: ${deviceName}\nرقم الطراز الدقيق: ${modelNumber}\nالمعالج: ${chipset || 'غير محدد'}\nالاحتياج: إضافة مورد موثق أو شرح توافق.`)} className="mt-3 rounded-lg bg-slate-800 px-3 py-2 text-xs font-bold text-[#67e8f9]">طلب إضافة هذا الطراز أو شرح</button>
          </div>
        )}
      </div>}
    </section>
  );

  if (mode === 'diagnostics') return (
    <section className="space-y-4">
      <header className={card}><div className="flex items-center gap-2 text-[#00b4ff]"><BookOpenCheck className="h-5 w-5" /><h2 className="text-base font-black text-white">مساعد التشخيص خطوة بخطوة</h2></div><p className="mt-2 text-xs text-slate-400">إرشادات أولية آمنة، تعمل دون اتصال. اختر العرض الأقرب، وابدأ بالفحوص غير الإتلافية.</p></header>
      <div className="grid gap-2 sm:grid-cols-3">{[
        { id: 'boot', title: 'تعليق على الشعار', icon: Smartphone },
        { id: 'network', title: 'مشكلة شبكة / لا توجد خدمة', icon: Wrench },
        { id: 'update', title: 'فشل التحديث أو التفليش', icon: AlertTriangle },
      ].map((item) => { const Icon = item.icon; return <button key={item.id} onClick={() => { setSymptom(item.id); setDiagnosisStarted(true); }} className={`flex min-h-16 items-center gap-3 rounded-xl border p-3 text-right text-sm font-bold ${symptom === item.id ? 'border-[#00b4ff] bg-[#00b4ff]/10 text-white' : 'border-slate-800 bg-slate-900 text-slate-300'}`}><Icon className="h-5 w-5 text-[#00b4ff]" />{item.title}</button>; })}</div>
      {diagnosisStarted && <DiagnosticSteps symptom={symptom} />}
      <div className={warningBox}><AlertTriangle className="ml-1 inline h-4 w-4" /> أوقف العمل عند سخونة غير طبيعية أو تلف مادي. لا تمسح البيانات ولا تفتح الجهاز أو تستخدم Test Point إلا بعد التحقق من النسخة الاحتياطية ورقم اللوحة ومخطط الموديل الصحيح.</div>
    </section>
  );

  return (
    <section className="space-y-4">
      <header className={card}><div className="flex items-center gap-2 text-[#00b4ff]"><Database className="h-5 w-5" /><h2 className="text-base font-black text-white">دفتر ملاحظات الأجهزة</h2></div><p className="mt-2 text-xs leading-relaxed text-slate-400">يسجل اسم الجهاز ورقمه والعطل والملاحظات في التخزين المحلي على هذا الجهاز. لا يحتاج حسابًا ولا يرفع هذه البيانات إلى خادم.</p><p className="mt-2 text-[11px] text-emerald-300">{savedLocally ? 'الحفظ المحلي متاح' : 'تعذر الحفظ — مساحة التخزين غير متاحة'}</p></header>
      <form onSubmit={addNote} className={`${card} grid gap-3 sm:grid-cols-2`}>
        <label className="space-y-1 text-xs text-slate-300">اسم الجهاز *<input required className={inputClass} value={newDeviceName} onChange={(event) => setNewDeviceName(event.target.value)} placeholder="Samsung A14" /></label>
        <label className="space-y-1 text-xs text-slate-300">رقم الطراز *<input required className={`${inputClass} font-mono`} value={newModelNumber} onChange={(event) => setNewModelNumber(event.target.value)} placeholder="SM-A145F" /></label>
        <label className="space-y-1 text-xs text-slate-300 sm:col-span-2">العطل أو العملية *<input required className={inputClass} value={newIssue} onChange={(event) => setNewIssue(event.target.value)} placeholder="تعليق شعار، فحص شبكة، إصدار حماية..." /></label>
        <label className="space-y-1 text-xs text-slate-300 sm:col-span-2">ملاحظات للفني<textarea className={`${inputClass} min-h-24 resize-y`} value={newNote} onChange={(event) => setNewNote(event.target.value)} placeholder="الخطوات التي جُربت، نتيجة القياس، القطع المستبدلة..." /></label>
        <button className="sm:col-span-2 inline-flex min-h-11 items-center justify-center gap-2 rounded-xl bg-[#00b4ff] px-4 py-2 text-sm font-black text-slate-950" type="submit"><Plus className="h-4 w-4" />حفظ الملاحظة محليًا</button>
      </form>
      {notes.length ? <div className="grid gap-3 md:grid-cols-2">{notes.map((item) => <article key={item.id} className={`${card} space-y-2`}><div className="flex items-start justify-between gap-3"><div><h3 className="font-bold text-white">{item.deviceName}</h3><p className="font-mono text-xs text-[#00b4ff]">{item.modelNumber}</p></div><button onClick={() => deleteNote(item.id)} aria-label="حذف الملاحظة" className="rounded-lg p-2 text-red-300 hover:bg-red-500/10"><Trash2 className="h-4 w-4" /></button></div><p className="text-xs text-slate-300"><b>العملية:</b> {item.issue}</p>{item.note && <p className="whitespace-pre-wrap text-xs leading-relaxed text-slate-400">{item.note}</p>}<time className="block text-[10px] text-slate-500">آخر تعديل: {new Date(item.updatedAt).toLocaleString('ar')}</time></article>)}</div> : <div className={`${card} text-center text-xs text-slate-500`}>لا توجد ملاحظات مسجلة. أضف أول جهاز أعلاه.</div>}
    </section>
  );
};

const CompatibilityResult: React.FC<{ phone: PhoneSearchResult; brand: string; chipset: string; onCopy: (text: string) => void; onReport: () => void }> = ({ phone, brand, chipset, onCopy, onReport }) => (
  <article className={`${card} space-y-3`}>
    <div className="flex flex-wrap items-center gap-2"><CheckCircle2 className="h-4 w-4 text-emerald-400" /><h3 className="font-black text-white">تطابق في فهرس الطرازات</h3><span className="rounded-lg bg-slate-800 px-2 py-1 text-[10px] text-[#00b4ff]">{phone.brand}</span></div>
    <div><p className="font-bold text-slate-100">{phone.name}</p><p className="font-mono text-xs text-slate-400">{phone.modelNumber || 'لا يوجد رقم طراز مسجل'}</p><p className="mt-1 text-xs text-slate-400">{phone.subtitle}</p></div>
    {(brand.trim() || chipset.trim()) && <p className="text-[11px] text-slate-500">بيانات البحث التي أدخلتها: {brand || 'الشركة غير محددة'}{chipset ? ` • ${chipset}` : ''}</p>}
    <div className="space-y-2">{phone.groups.filter((group) => ['dump', 'firmware', 'driver'].includes(group.kind)).map((group) => <div key={group.kind} className="rounded-xl border border-slate-800 bg-slate-950 p-3"><h4 className="mb-2 text-xs font-bold text-slate-200">{group.title}</h4>{group.resources.length ? group.resources.slice(0, 4).map((resource) => <div key={resource.id} className="mb-2 border-b border-slate-800 pb-2 last:mb-0 last:border-0 last:pb-0"><p className="text-xs font-semibold text-white">{resource.title}</p>{resource.version && <p className="font-mono text-[10px] text-[#00b4ff]">{resource.version}</p>}<p className="mt-1 text-[10px] leading-relaxed text-slate-400">{resource.description}</p>{resource.note && <p className="mt-1 text-[10px] text-amber-300/80">{resource.note}</p>}{resource.link && resource.link !== '#' && <div className="mt-2 flex flex-wrap gap-2"><a href={resource.link} target="_blank" rel="noreferrer" className="rounded-lg bg-[#00b4ff] px-3 py-1.5 text-[10px] font-bold text-black">فتح المصدر</a><button onClick={() => onCopy(resource.link!)} className="inline-flex items-center gap-1 rounded-lg bg-slate-800 px-3 py-1.5 text-[10px] text-slate-200"><Clipboard className="h-3 w-3" />نسخ الرابط</button></div>}</div>) : <p className="text-[10px] text-slate-500">{group.emptyMessage}</p>}</div>)}</div>
    <p className="flex items-start gap-1 text-[10px] leading-relaxed text-amber-200/80"><Info className="mt-0.5 h-3 w-3 shrink-0" /> تطابق هذا الاسم/الرمز في الفهرس فقط؛ لم تُسجل قاعدة البيانات المنطقة أو حجم الملف أو بصمته أو تاريخ تحقق الرابط.</p>
    <button onClick={onReport} className="rounded-lg border border-slate-700 px-3 py-2 text-[10px] font-bold text-slate-300">الإبلاغ عن خطأ في التوافق</button>
  </article>
);

const DiagnosticSteps: React.FC<{ symptom: string }> = ({ symptom }) => {
  const guides: Record<string, { title: string; steps: string[]; stop: string }> = {
    boot: { title: 'تشخيص تعليق الشعار', steps: ['تحقق من مستوى الشحن وافصل الملحقات وجرّب إعادة تشغيل قسرية حسب دليل الشركة.', 'إن أمكن، ادخل Recovery واقرأ رسالة الخطأ؛ لا تختَر مسح البيانات قبل موافقة صاحب الجهاز ووجود نسخة احتياطية.', 'دوّن رقم الطراز وإصدار البناء، وتحقق من مساحة التخزين وسلامة النظام قبل التفكير في تحديث رسمي مطابق.', 'إذا لم يعمل Recovery، افحص الكابل والمنفذ والطاقة، ثم استخدم أداة الشركة الرسمية فقط بعد التحقق من الطراز والمنطقة.'], stop: 'أوقف التفليش عند اختلاف رقم الطراز/المنطقة أو عند طلب أداة ملفًا غير موثوق.' },
    network: { title: 'تشخيص فقدان الشبكة', steps: ['تحقق من وضع الطيران والشريحة والتغطية، ثم أعد التشغيل واختبر الشريحة في جهاز آخر.', 'راجع إعدادات الشبكة/APN الرسمية للمشغل، وتحقق من أن اختيار الشبكة ونوعها مناسب للمنطقة.', 'اقرأ حالة IMEI وBaseband من الإعدادات دون نشر الرقم؛ إذا كان IMEI مفقودًا أو Baseband مجهولًا فتوقف عن أي كتابة عشوائية.', 'بعد تحديث أو إصلاح، قارن إصدار المودم/المنطقة مع النسخة الرسمية المناسبة، واحتفظ بنسخة من بيانات المعايرة قبل أي خدمة معتمدة.'], stop: 'لا تغيّر IMEI ولا تكتب ملفات QCN/NVRAM من جهاز آخر؛ قد يتسبب ذلك بتعطيل الشبكة أو مخالفة الأنظمة.' },
    update: { title: 'تشخيص فشل التحديث أو التفليش', steps: ['سجّل نص رمز الخطأ كاملًا واسم الأداة وإصدارها؛ لا تكرر المحاولة دون معرفة السبب.', 'تحقق من رقم الطراز الدقيق والمنطقة/CSC وإصدار الحماية/Bootloader، وأن الحزمة رسمية ومطابقة.', 'بدّل الكابل والمنفذ، اشحن الجهاز، وثبّت التعريف المناسب وتحقق من اتصال USB قبل بدء العملية.', 'راجع مساحة التخزين وتوقيع الحزمة وسلامة التنزيل؛ إن لم تتوفر بصمة موثقة فلا تعتبر الملف سليمًا تلقائيًا.', 'خذ نسخة احتياطية، ثم اتبع دليل الشركة الرسمي. لا تخفّض إصدار Bootloader ولا تعِد تقسيم الأقسام دون معرفة موثقة.'], stop: 'توقف إن كان الرمز يشير إلى فشل كتابة أو اختلاف الطراز/الحماية، أو إن لم تستطع تأكيد الملف والنسخة الاحتياطية.' },
  };
  const guide = guides[symptom];
  if (!guide) return null;
  return <article className={`${card} space-y-3`}><h3 className="font-black text-white">{guide.title}</h3><ol className="space-y-2">{guide.steps.map((step, index) => <li key={step} className="flex gap-2 text-xs leading-relaxed text-slate-300"><span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-[#00b4ff]/15 text-[10px] font-bold text-[#00b4ff]">{index + 1}</span><span>{step}</span></li>)}</ol><p className={warningBox}><AlertTriangle className="ml-1 inline h-4 w-4" />{guide.stop}</p></article>;
};
