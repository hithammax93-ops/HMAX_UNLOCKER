import React, { useState } from 'react';
import { Wrench, Cpu, Unlock, Globe, Apple, Shield } from 'lucide-react';
import { HMAX_DATA, ItemData } from '../data/hmaxData';
import { ItemCard } from './ItemCard';

export type ToolsSubCategory = 'tools' | 'drivers' | 'unlocking' | 'firmware' | 'iphone';

export interface ToolsViewProps {
  onCopyToast: (msg: string) => void;
  isFav: (item: ItemData) => boolean;
  onToggleFav: (item: ItemData) => void;
  initialCategory?: ToolsSubCategory;
}

export const ToolsView: React.FC<ToolsViewProps> = ({
  onCopyToast,
  isFav,
  onToggleFav,
  initialCategory = 'tools',
}) => {
  const [activeCategory, setActiveCategory] = useState<ToolsSubCategory>(initialCategory);

  React.useEffect(() => {
    if (initialCategory) {
      setActiveCategory(initialCategory);
    }
  }, [initialCategory]);

  const categories = [
    { id: 'tools' as ToolsSubCategory, label: 'أدوات السوفت وير', icon: Wrench, count: HMAX_DATA.tools.length },
    { id: 'drivers' as ToolsSubCategory, label: 'تعاريف الموبايل', icon: Cpu, count: HMAX_DATA.drivers.length },
    { id: 'unlocking' as ToolsSubCategory, label: 'فك الشفرات', icon: Unlock, count: HMAX_DATA.unlocking.length },
    { id: 'firmware' as ToolsSubCategory, label: 'مواقع الفلاشات', icon: Globe, count: HMAX_DATA.firmware_sites.length },
    { id: 'iphone' as ToolsSubCategory, label: 'أدوات آيفون و PWN', icon: Apple, count: HMAX_DATA.iphone_tools.length + HMAX_DATA.iphone_pwn.length },
  ];

  return (
    <div className="space-y-4">
      {/* Category selector chips */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none no-scrollbar">
        {categories.map((cat) => {
          const Icon = cat.icon;
          const isActive = activeCategory === cat.id;

          return (
            <button
              key={cat.id}
              onClick={() => setActiveCategory(cat.id)}
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

      {/* Render Active Category Content */}
      {activeCategory === 'tools' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {HMAX_DATA.tools.map((item) => (
            <ItemCard
              key={item.id}
              item={item}
              isFav={isFav(item)}
              onToggleFav={onToggleFav}
              onCopyToast={onCopyToast}
              badgeLabel="برنامج سوفت وير"
            />
          ))}
        </div>
      )}

      {activeCategory === 'drivers' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {HMAX_DATA.drivers.map((item) => (
            <ItemCard
              key={item.id}
              item={item}
              isFav={isFav(item)}
              onToggleFav={onToggleFav}
              onCopyToast={onCopyToast}
              badgeLabel="تعريف درايفر"
            />
          ))}
        </div>
      )}

      {activeCategory === 'unlocking' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {HMAX_DATA.unlocking.map((item) => (
            <ItemCard
              key={item.id}
              item={item}
              isFav={isFav(item)}
              onToggleFav={onToggleFav}
              onCopyToast={onCopyToast}
              badgeLabel="فك شبكة"
            />
          ))}
        </div>
      )}

      {activeCategory === 'firmware' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {HMAX_DATA.firmware_sites.map((item) => (
            <ItemCard
              key={item.id}
              item={item}
              isFav={isFav(item)}
              onToggleFav={onToggleFav}
              onCopyToast={onCopyToast}
              badgeLabel="موقع فلاشات رسمي"
            />
          ))}
        </div>
      )}

      {activeCategory === 'iphone' && (
        <div className="space-y-4">
          <div className="space-y-2">
            <h3 className="text-xs font-bold text-slate-300">أدوات الآيفون وسبريدترام:</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {HMAX_DATA.iphone_tools.map((item) => (
                <ItemCard
                  key={item.id}
                  item={item}
                  isFav={isFav(item)}
                  onToggleFav={onToggleFav}
                  onCopyToast={onCopyToast}
                  badgeLabel="برنامج آيفون / SPD"
                />
              ))}
            </div>
          </div>

          <div className="space-y-2 pt-2">
            <h3 className="text-xs font-bold text-amber-400">فلاشات وبرمجة قطع PWN DFU:</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {HMAX_DATA.iphone_pwn.map((item) => (
                <ItemCard
                  key={item.id}
                  item={item}
                  isFav={isFav(item)}
                  onToggleFav={onToggleFav}
                  onCopyToast={onCopyToast}
                  badgeLabel="فلاشة قطعة PWN"
                />
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
