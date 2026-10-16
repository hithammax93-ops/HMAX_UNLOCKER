import React, { useState } from 'react';
import { Sparkles, Gift, Crown, Bot, Headset, FolderGit2, Wrench } from 'lucide-react';
import { HMAX_DATA, ItemData } from '../data/hmaxData';
import { ItemCard } from './ItemCard';

interface OffersViewProps {
  onCopyToast: (msg: string) => void;
  isFav: (item: ItemData) => boolean;
  onToggleFav: (item: ItemData) => void;
}

type OffersCategory = 'offers' | 'vip' | 'ai' | 'free' | 'gifts' | 'services' | 'halabtech';

export const OffersView: React.FC<OffersViewProps> = ({
  onCopyToast,
  isFav,
  onToggleFav,
}) => {
  const [activeCat, setActiveCat] = useState<OffersCategory>('offers');

  const categories = [
    { id: 'offers' as OffersCategory, label: 'عروض هيثم ماكس', icon: Sparkles, count: HMAX_DATA.offers_hitham.length },
    { id: 'vip' as OffersCategory, label: 'عروض مدفوعة VIP', icon: Crown, count: HMAX_DATA.paid_offers.length },
    { id: 'ai' as OffersCategory, label: 'ذكاء اصطناعي', icon: Bot, count: HMAX_DATA.ai_offers.length },
    { id: 'free' as OffersCategory, label: 'أدوات مجانية', icon: Wrench, count: HMAX_DATA.free_tools.length },
    { id: 'gifts' as OffersCategory, label: 'قسم هدية لكم', icon: Gift, count: HMAX_DATA.gifts.length },
    { id: 'services' as OffersCategory, label: 'خدمات عن بعد', icon: Headset, count: HMAX_DATA.services.length },
    { id: 'halabtech' as OffersCategory, label: 'ملفات حلب تك', icon: FolderGit2, count: HMAX_DATA.halabtech.length },
  ];

  return (
    <div className="space-y-4">
      {/* Category Chips with Horizontal Scroll */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none no-scrollbar">
        {categories.map((cat) => {
          const Icon = cat.icon;
          const isActive = activeCat === cat.id;

          return (
            <button
              key={cat.id}
              onClick={() => setActiveCat(cat.id)}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-bold whitespace-nowrap transition-all ${
                isActive
                  ? 'bg-[#00b4ff] text-black shadow-[0_0_12px_rgba(0,180,255,0.3)]'
                  : 'bg-slate-900/80 text-slate-300 hover:bg-slate-800 border border-slate-800'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{cat.label}</span>
              <span
                className={`text-[10px] px-1.5 py-0.2 rounded-full ${
                  isActive ? 'bg-black/20 text-black' : 'bg-slate-800 text-slate-400'
                }`}
              >
                {cat.count}
              </span>
            </button>
          );
        })}
      </div>

      {/* Offers Hitham */}
      {activeCat === 'offers' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {HMAX_DATA.offers_hitham.map((item) => (
            <ItemCard
              key={item.id}
              item={item}
              isFav={isFav(item)}
              onToggleFav={onToggleFav}
              onCopyToast={onCopyToast}
              badgeLabel="اشتراك رسمي مضمون"
            />
          ))}
        </div>
      )}

      {/* VIP Paid */}
      {activeCat === 'vip' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {HMAX_DATA.paid_offers.map((item) => (
            <ItemCard
              key={item.id}
              item={item}
              isFav={isFav(item)}
              onToggleFav={onToggleFav}
              onCopyToast={onCopyToast}
              badgeLabel="باقة VIP مدفوعة"
            />
          ))}
        </div>
      )}

      {/* AI Subscriptions */}
      {activeCat === 'ai' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {HMAX_DATA.ai_offers.map((item) => (
            <ItemCard
              key={item.id}
              item={item}
              isFav={isFav(item)}
              onToggleFav={onToggleFav}
              onCopyToast={onCopyToast}
              badgeLabel="اشتراك ذكاء اصطناعي"
            />
          ))}
        </div>
      )}

      {/* Free Tools */}
      {activeCat === 'free' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {HMAX_DATA.free_tools.map((item) => (
            <ItemCard
              key={item.id}
              item={item}
              isFav={isFav(item)}
              onToggleFav={onToggleFav}
              onCopyToast={onCopyToast}
              badgeLabel="أداة مجانية للكمبيوتر"
            />
          ))}
        </div>
      )}

      {/* Gifts */}
      {activeCat === 'gifts' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {HMAX_DATA.gifts.map((item) => (
            <ItemCard
              key={item.id}
              item={item}
              isFav={isFav(item)}
              onToggleFav={onToggleFav}
              onCopyToast={onCopyToast}
              badgeLabel="هدية خاصة"
            />
          ))}
        </div>
      )}

      {/* Services */}
      {activeCat === 'services' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {HMAX_DATA.services.map((item) => (
            <ItemCard
              key={item.id}
              item={item}
              isFav={isFav(item)}
              onToggleFav={onToggleFav}
              onCopyToast={onCopyToast}
              badgeLabel="خدمة عن بعد 24/7"
            />
          ))}
        </div>
      )}

      {/* Halabtech */}
      {activeCat === 'halabtech' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {HMAX_DATA.halabtech.map((item) => (
            <ItemCard
              key={item.id}
              item={item}
              isFav={isFav(item)}
              onToggleFav={onToggleFav}
              onCopyToast={onCopyToast}
              badgeLabel="سبورت حلب تك"
            />
          ))}
        </div>
      )}
    </div>
  );
};
