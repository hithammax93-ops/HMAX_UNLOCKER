import React, { useState } from 'react';
import { Sparkles, Gift, Crown, Bot, Headset, FolderGit2, Wrench, Send, MessageCircle, ExternalLink } from 'lucide-react';
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
      {/* Direct VIP & Support Contact Banner */}
      <div className="p-4 rounded-2xl bg-gradient-to-r from-slate-900 via-blue-950/40 to-slate-900 border border-slate-800 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 shadow-sm">
        <div>
          <span className="text-xs font-bold text-[#00b4ff] block mb-0.5">
            خدمات السيرفرات والاشتراكات الفورية 24/7
          </span>
          <p className="text-xs text-slate-300">
            تفعيل فوري لجميع البوكسات، شحن أرصدة، وسحب أي فلاشة أو ملف من سبورت حلب تك بـ 3 دولار فقط.
          </p>
        </div>
        <div className="flex items-center gap-2 shrink-0 flex-wrap">
          <a
            href="https://t.me/hithamMax"
            target="_blank"
            rel="noopener noreferrer"
            className="h-8 px-3 rounded-lg bg-[#00b4ff] hover:bg-[#67e8f9] text-black font-black text-xs flex items-center gap-1.5 transition shadow-sm"
          >
            <Send className="w-3 h-3 fill-black" />
            <span>طلب عبر تليجرام</span>
          </a>
          <a
            href="https://wa.me/967772773388"
            target="_blank"
            rel="noopener noreferrer"
            className="h-8 px-3 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center gap-1.5 transition"
          >
            <MessageCircle className="w-3.5 h-3.5" />
            <span>واتساب</span>
          </a>
        </div>
      </div>

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
