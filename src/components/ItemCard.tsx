import React from 'react';
import { Download, Copy, Star, ExternalLink, Key, Check } from 'lucide-react';
import { ItemData } from '../data/hmaxData';

interface ItemCardProps {
  item: ItemData;
  isFav?: boolean;
  onToggleFav?: (item: ItemData) => void;
  onCopyToast: (msg: string) => void;
  badgeLabel?: string;
}

export const ItemCard: React.FC<ItemCardProps> = ({
  item,
  isFav = false,
  onToggleFav,
  onCopyToast,
  badgeLabel,
}) => {
  const [copiedLink, setCopiedLink] = React.useState(false);
  const [copiedPass, setCopiedPass] = React.useState(false);

  const hasLink = item.link && item.link !== '#';
  const hasSpecificPass = item.pass && item.pass !== '—';

  const handleCopyLink = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (!item.link) return;
    navigator.clipboard.writeText(item.link);
    setCopiedLink(true);
    onCopyToast('تم نسخ الرابط إلى الحافظة');
    setTimeout(() => setCopiedLink(false), 1800);
  };

  const handleCopyPass = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (!item.pass) return;
    navigator.clipboard.writeText(item.pass);
    setCopiedPass(true);
    onCopyToast(`تم نسخ الباسورد: ${item.pass}`);
    setTimeout(() => setCopiedPass(false), 1800);
  };

  const handleCopyGuide = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (!item.guide) return;
    navigator.clipboard.writeText(item.guide);
    onCopyToast(`تم نسخ الكود: ${item.guide}`);
  };

  return (
    <div className="group relative rounded-2xl bg-gradient-to-br from-slate-900/90 to-slate-900/50 border border-slate-800/80 hover:border-[#00b4ff]/40 p-4 flex flex-col justify-between transition-all duration-200 hover:-translate-y-0.5 shadow-sm hover:shadow-[0_8px_24px_rgba(0,180,255,0.08)]">
      <div>
        {item.image && (
          <img
            src={item.image}
            alt={`${item.name} preview`}
            loading="lazy"
            onError={(event) => { event.currentTarget.hidden = true; }}
            className="w-full aspect-video object-cover rounded-xl border border-slate-700/60 mb-3"
          />
        )}
        {/* Header with Title and Favorite Toggle */}
        <div className="flex items-start justify-between gap-2 mb-2">
          <div className="flex-1 min-w-0">
            {badgeLabel && (
              <span className="text-[11px] font-semibold text-[#00b4ff] mb-0.5 block">
                {badgeLabel}
              </span>
            )}
            <h3 className="text-sm font-bold text-slate-100 group-hover:text-white leading-snug line-clamp-2">
              {item.name}
            </h3>
          </div>

          {onToggleFav && (
            <button
              onClick={() => onToggleFav(item)}
              title={isFav ? 'إزالة من المفضلة' : 'إضافة إلى المفضلة'}
              className="p-1.5 rounded-lg text-slate-400 hover:text-amber-400 active:scale-90 transition shrink-0 min-w-[36px] min-h-[36px] flex items-center justify-center"
            >
              <Star
                className={`w-4 h-4 transition ${
                  isFav ? 'fill-amber-400 text-amber-400' : 'text-slate-500'
                }`}
              />
            </button>
          )}
        </div>

        {/* Clean Metadata (Version / Tag) */}
        {item.ver && (
          <div className="text-xs text-slate-400 font-mono mb-2 flex items-center gap-1.5 flex-wrap">
            <span className="text-[#00b4ff]/90">{item.ver}</span>
            {hasSpecificPass && (
              <>
                <span className="text-slate-600">·</span>
                <button
                  onClick={handleCopyPass}
                  className="inline-flex items-center gap-1 text-[11px] text-amber-400 hover:text-amber-300 transition"
                  title="نسخ الباسورد الخاص"
                >
                  <Key className="w-3 h-3" />
                  <span>كلمة السر: {item.pass}</span>
                  {copiedPass && <Check className="w-3 h-3 text-emerald-400" />}
                </button>
              </>
            )}
          </div>
        )}

        {/* Description */}
        {item.desc && (
          <p className="text-xs text-slate-400/90 leading-relaxed mb-3 whitespace-pre-line">
            {item.desc}
          </p>
        )}
      </div>

      {/* Action Buttons */}
      <div className="flex items-center gap-2 pt-2 border-t border-slate-800/60 mt-auto">
        {hasLink ? (
          <a
            href={item.link}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1 h-9 px-3 rounded-xl bg-[#00b4ff] hover:bg-[#67e8f9] text-black font-black text-xs flex items-center justify-center gap-1.5 active:scale-95 transition shadow-sm"
          >
            <Download className="w-3.5 h-3.5" />
            <span>تحميل مباشر</span>
          </a>
        ) : item.guide ? (
          <button
            onClick={handleCopyGuide}
            className="flex-1 h-9 px-3 rounded-xl bg-[#00b4ff] hover:bg-[#67e8f9] text-black font-black text-xs flex items-center justify-center gap-1.5 active:scale-95 transition"
          >
            <Copy className="w-3.5 h-3.5" />
            <span>نسخ الكود</span>
          </button>
        ) : (
          <span className="flex-1 h-9 rounded-xl bg-slate-800/50 text-slate-500 font-bold text-xs flex items-center justify-center">
            قريباً
          </span>
        )}

        {/* Copy Link Button */}
        {hasLink && (
          <button
            onClick={handleCopyLink}
            title="نسخ الرابط"
            className="h-9 w-9 rounded-xl bg-slate-800/80 hover:bg-slate-800 text-slate-300 border border-slate-700/60 flex items-center justify-center shrink-0 active:scale-90 transition"
          >
            {copiedLink ? (
              <Check className="w-3.5 h-3.5 text-emerald-400" />
            ) : (
              <Copy className="w-3.5 h-3.5" />
            )}
          </button>
        )}

        {/* Video Tutorial Link if available */}
        {item.video && (
          <a
            href={item.video}
            target="_blank"
            rel="noopener noreferrer"
            title="فيديو توضيحي"
            className="h-9 w-9 rounded-xl bg-red-950/40 hover:bg-red-900/50 text-red-400 border border-red-800/40 flex items-center justify-center shrink-0 active:scale-90 transition"
          >
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        )}
      </div>
    </div>
  );
};
