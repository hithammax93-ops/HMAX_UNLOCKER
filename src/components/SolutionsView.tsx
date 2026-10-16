import React, { useState } from 'react';
import {
  Youtube,
  FileText,
  Sparkles,
  Signal,
  Wrench,
  Video,
  MessageSquare,
  ExternalLink,
  Copy,
  AlertTriangle,
  CheckCircle,
  Code
} from 'lucide-react';
import { HMAX_DATA, ItemData } from '../data/hmaxData';
import { ItemCard } from './ItemCard';

interface SolutionsViewProps {
  onCopyToast: (msg: string) => void;
  isFav: (item: ItemData) => boolean;
  onToggleFav: (item: ItemData) => void;
}

type SubSection =
  | 'youtube'
  | 'text_guides'
  | 'experiences'
  | 'volte'
  | 'rasheed'
  | 'haitham'
  | 'samsung_msg';

export const SolutionsView: React.FC<SolutionsViewProps> = ({
  onCopyToast,
  isFav,
  onToggleFav,
}) => {
  const [activeSub, setActiveSub] = useState<SubSection>('youtube');
  const [selectedGuideId, setSelectedGuideId] = useState<string | null>(null);

  const subSections = [
    { id: 'youtube' as SubSection, label: 'FRP يوتيوب', icon: Youtube, count: HMAX_DATA.solutions.youtube.length },
    { id: 'text_guides' as SubSection, label: 'شروحات نصية', icon: FileText, count: HMAX_DATA.solutions.text_guides.length },
    { id: 'experiences' as SubSection, label: 'تجارب ناجحة', icon: Sparkles, count: HMAX_DATA.solutions.experiences.length },
    { id: 'volte' as SubSection, label: 'تفعيل VoLTE', icon: Signal, count: HMAX_DATA.solutions.volte.length },
    { id: 'rasheed' as SubSection, label: 'أكواد رشيد', icon: Wrench, count: HMAX_DATA.solutions.rasheed.length },
    { id: 'haitham' as SubSection, label: 'فيديوهات هيثم', icon: Video, count: HMAX_DATA.solutions.haitham.length },
    { id: 'samsung_msg' as SubSection, label: 'Samsung Msg', icon: MessageSquare, count: 1 },
  ];

  const selectedGuide = HMAX_DATA.solutions.text_guides.find((g) => g.id === selectedGuideId);

  return (
    <div className="space-y-4">
      {/* Sub-navigation bar with horizontal scroll for mobile */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none no-scrollbar">
        {subSections.map((sec) => {
          const Icon = sec.icon;
          const isActive = activeSub === sec.id;
          return (
            <button
              key={sec.id}
              onClick={() => {
                setActiveSub(sec.id);
                setSelectedGuideId(null);
              }}
              className={`flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-bold whitespace-nowrap transition-all ${
                isActive
                  ? 'bg-[#00b4ff] text-black shadow-[0_0_12px_rgba(0,180,255,0.3)]'
                  : 'bg-slate-900/80 text-slate-300 hover:bg-slate-800 border border-slate-800'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{sec.label}</span>
              <span
                className={`text-[10px] px-1.5 py-0.2 rounded-full ${
                  isActive ? 'bg-black/20 text-black' : 'bg-slate-800 text-slate-400'
                }`}
              >
                {sec.count}
              </span>
            </button>
          );
        })}
      </div>

      {/* 1. YouTube FRP */}
      {activeSub === 'youtube' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {HMAX_DATA.solutions.youtube.map((item) => (
            <ItemCard
              key={item.id}
              item={item}
              isFav={isFav(item)}
              onToggleFav={onToggleFav}
              onCopyToast={onCopyToast}
              badgeLabel="شرح فيديو يوتيوب"
            />
          ))}
        </div>
      )}

      {/* 2. Text Guides */}
      {activeSub === 'text_guides' && (
        <div className="space-y-4">
          {!selectedGuide ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {HMAX_DATA.solutions.text_guides.map((g) => (
                <div
                  key={g.id}
                  onClick={() => setSelectedGuideId(g.id)}
                  className="cursor-pointer p-4 rounded-2xl bg-slate-900/80 border border-slate-800 hover:border-[#00b4ff]/40 transition group flex flex-col justify-between"
                >
                  <div>
                    <span className="text-[11px] font-semibold text-[#00b4ff] block mb-1">
                      {g.tag}
                    </span>
                    <h3 className="text-sm font-bold text-slate-100 group-hover:text-white leading-snug mb-2">
                      {g.title}
                    </h3>
                    <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed">
                      {g.problem}
                    </p>
                  </div>
                  <div className="pt-3 border-t border-slate-800/60 mt-3 flex items-center justify-between text-xs text-[#00b4ff] font-bold">
                    <span>قراءة الحل والخطوات</span>
                    <span>←</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            /* Selected Guide Details */
            <div className="rounded-2xl bg-slate-900/90 border border-slate-800 p-5 space-y-4">
              <button
                onClick={() => setSelectedGuideId(null)}
                className="text-xs text-[#00b4ff] hover:underline font-bold mb-2 inline-flex items-center gap-1"
              >
                <span>→</span>
                <span>العودة لقائمة الشروحات</span>
              </button>

              <div>
                <span className="text-xs text-[#00b4ff] font-semibold">{selectedGuide.tag}</span>
                <h3 className="text-base font-black text-white mt-0.5">{selectedGuide.title}</h3>
              </div>

              {/* Problem Statement */}
              <div className="p-3 rounded-xl bg-red-950/20 border border-red-800/30 text-xs text-red-200 space-y-1">
                <div className="flex items-center gap-1.5 font-bold text-red-400">
                  <AlertTriangle className="w-4 h-4" />
                  <span>المشكلة:</span>
                </div>
                <p>{selectedGuide.problem}</p>
              </div>

              {/* Steps */}
              <div className="space-y-2 pt-2">
                <h4 className="text-xs font-bold text-slate-300">خطوات التنفيذ المعتمدة:</h4>
                <div className="space-y-2">
                  {selectedGuide.steps.map((step) => (
                    <div
                      key={step.num}
                      className="flex items-start gap-2.5 p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 text-xs text-slate-200"
                    >
                      <span className="w-5 h-5 rounded-full bg-[#00b4ff] text-black font-black text-[11px] flex items-center justify-center shrink-0">
                        {step.num}
                      </span>
                      <span className="leading-relaxed">{step.text}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Code Snippet if exists */}
              {selectedGuide.codeSnippet && (
                <div className="space-y-1 pt-1">
                  <span className="text-[11px] font-bold text-slate-400">الأمر البرمجي:</span>
                  <div className="flex items-center justify-between gap-2 p-2.5 rounded-xl bg-slate-950 border border-slate-800 font-mono text-xs text-[#00b4ff]">
                    <span className="overflow-x-auto">{selectedGuide.codeSnippet}</span>
                    <button
                      onClick={() => {
                        navigator.clipboard.writeText(selectedGuide.codeSnippet!);
                        onCopyToast('تم نسخ الأمر');
                      }}
                      className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200"
                    >
                      <Copy className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              )}

              {/* Conclusion Note */}
              {selectedGuide.conclusionNote && (
                <div className="p-3 rounded-xl bg-emerald-950/20 border border-emerald-800/30 text-xs text-emerald-300 flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0" />
                  <span>{selectedGuide.conclusionNote}</span>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* 3. Experiences */}
      {activeSub === 'experiences' && (
        <div className="space-y-3">
          {HMAX_DATA.solutions.experiences.map((exp) => (
            <div
              key={exp.id}
              className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-3"
            >
              <div className="flex items-center justify-between gap-2">
                <h3 className="text-sm font-bold text-slate-100">{exp.title}</h3>
                <span className="text-xs text-[#00b4ff] font-semibold">بقلم: {exp.author}</span>
              </div>

              <div className="p-3 rounded-xl bg-amber-950/20 border border-amber-800/30 text-xs text-amber-200">
                <span className="font-bold block mb-1">المشكلة والأعراض:</span>
                <p className="leading-relaxed">{exp.problem}</p>
              </div>

              {exp.solutionDesc && (
                <p className="text-xs text-slate-300 leading-relaxed">{exp.solutionDesc}</p>
              )}

              {exp.solutionSteps && (
                <div className="space-y-1.5">
                  <span className="text-xs font-bold text-slate-300">خطوات الحل:</span>
                  {exp.solutionSteps.map((step) => (
                    <div
                      key={step.num}
                      className="flex items-center gap-2 text-xs text-slate-300 bg-slate-950/40 p-2 rounded-lg"
                    >
                      <span className="w-4 h-4 rounded-full bg-[#00b4ff] text-black font-black text-[10px] flex items-center justify-center shrink-0">
                        {step.num}
                      </span>
                      <span>{step.text}</span>
                    </div>
                  ))}
                </div>
              )}

              {exp.warning && (
                <div className="p-2.5 rounded-lg bg-red-950/30 border border-red-800/30 text-xs text-red-300">
                  {exp.warning}
                </div>
              )}

              {/* Action Links */}
              <div className="flex items-center gap-2 pt-2 border-t border-slate-800 flex-wrap">
                {exp.links.map((link, idx) => (
                  <a
                    key={idx}
                    href={link.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={`h-9 px-4 rounded-xl text-xs font-bold flex items-center gap-1.5 transition ${
                      link.primary
                        ? 'bg-[#00b4ff] hover:bg-[#67e8f9] text-black font-black'
                        : 'bg-slate-800 hover:bg-slate-700 text-slate-200'
                    }`}
                  >
                    <ExternalLink className="w-3.5 h-3.5" />
                    <span>{link.label}</span>
                  </a>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* 4. VoLTE */}
      {activeSub === 'volte' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {HMAX_DATA.solutions.volte.map((item) => (
            <ItemCard
              key={item.id}
              item={item}
              isFav={isFav(item)}
              onToggleFav={onToggleFav}
              onCopyToast={onCopyToast}
              badgeLabel="تفعيل مكالمات VoLTE"
            />
          ))}
        </div>
      )}

      {/* 5. Rasheed Medghamer Secrets */}
      {activeSub === 'rasheed' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {HMAX_DATA.solutions.rasheed.map((item) => (
            <ItemCard
              key={item.id}
              item={item}
              isFav={isFav(item)}
              onToggleFav={onToggleFav}
              onCopyToast={onCopyToast}
              badgeLabel="لمسات رشيد مدغمر"
            />
          ))}
        </div>
      )}

      {/* 6. Haitham Max Videos */}
      {activeSub === 'haitham' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {HMAX_DATA.solutions.haitham.map((item) => (
            <ItemCard
              key={item.id}
              item={item}
              isFav={isFav(item)}
              onToggleFav={onToggleFav}
              onCopyToast={onCopyToast}
              badgeLabel="شروحات هيثم ماكس"
            />
          ))}
        </div>
      )}

      {/* 7. Samsung Messages APK Fix */}
      {activeSub === 'samsung_msg' && (
        <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-4">
          <div>
            <h3 className="text-base font-black text-white">
              {HMAX_DATA.solutions.samsung_msg.title}
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              حل مشكلة التحديث التلقائي إلى تطبيق جوجل ميسيجز وفقدان الرسائل
            </p>
          </div>

          <div className="p-3 rounded-xl bg-amber-950/20 border border-amber-800/30 text-xs text-amber-200">
            <span className="font-bold block mb-1">سبب المشكلة:</span>
            <p className="leading-relaxed">{HMAX_DATA.solutions.samsung_msg.problem}</p>
          </div>

          <div className="space-y-2">
            <h4 className="text-xs font-bold text-slate-300">خطوات وإضافات التحديث الجديد:</h4>
            {HMAX_DATA.solutions.samsung_msg.updates.map((up) => (
              <div
                key={up.num}
                className="flex items-center gap-2.5 p-2.5 rounded-xl bg-slate-950/60 border border-slate-800 text-xs text-slate-300"
              >
                <span className="w-5 h-5 rounded-full bg-[#00b4ff] text-black font-black text-[11px] flex items-center justify-center shrink-0">
                  {up.num}
                </span>
                <span>{up.text}</span>
              </div>
            ))}
          </div>

          <div className="flex items-center gap-2 pt-2 border-t border-slate-800 flex-wrap">
            {HMAX_DATA.solutions.samsung_msg.links.map((link, idx) => (
              <a
                key={idx}
                href={link.url}
                target="_blank"
                rel="noopener noreferrer"
                className={`h-9 px-4 rounded-xl text-xs font-bold flex items-center gap-1.5 transition ${
                  link.primary
                    ? 'bg-[#00b4ff] hover:bg-[#67e8f9] text-black font-black'
                    : 'bg-slate-800 hover:bg-slate-700 text-slate-200'
                }`}
              >
                <ExternalLink className="w-3.5 h-3.5" />
                <span>{link.label}</span>
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
