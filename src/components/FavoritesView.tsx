import React, { useState } from 'react';
import { Star, Trash2, Search } from 'lucide-react';
import { ItemData } from '../data/hmaxData';
import { ItemCard } from './ItemCard';

interface FavoritesViewProps {
  favorites: ItemData[];
  onToggleFav: (item: ItemData) => void;
  onCopyToast: (msg: string) => void;
  onClearAll: () => void;
}

export const FavoritesView: React.FC<FavoritesViewProps> = ({
  favorites,
  onToggleFav,
  onCopyToast,
  onClearAll,
}) => {
  const [filter, setFilter] = useState('');

  const filtered = favorites.filter(
    (item) =>
      item.name.toLowerCase().includes(filter.toLowerCase()) ||
      (item.ver && item.ver.toLowerCase().includes(filter.toLowerCase())) ||
      (item.desc && item.desc.toLowerCase().includes(filter.toLowerCase()))
  );

  return (
    <div className="space-y-4">
      {/* View Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 bg-slate-900/60 border border-slate-800 rounded-2xl p-4">
        <div>
          <div className="flex items-center gap-2">
            <Star className="w-5 h-5 fill-amber-400 text-amber-400" />
            <h2 className="text-lg font-black text-slate-100">المفضلة والمحفوظات</h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            الملفات والأدوات التي قمت بتمييزها بنجمة للوصول السريع بدون إعادة البحث
          </p>
        </div>

        {favorites.length > 0 && (
          <div className="flex items-center gap-2 w-full sm:w-auto">
            <div className="relative flex-1 sm:w-56">
              <Search className="w-3.5 h-3.5 text-slate-400 absolute right-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="تصفية المحفوظات..."
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
                className="w-full h-9 pr-9 pl-3 rounded-xl bg-slate-950 border border-slate-800 focus:border-[#00b4ff]/50 text-xs text-slate-200 outline-none"
              />
            </div>
            <button
              onClick={onClearAll}
              title="مسح الكل"
              className="p-2 rounded-xl bg-slate-800 hover:bg-red-950 hover:text-red-400 text-slate-400 border border-slate-700/60 transition shrink-0"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        )}
      </div>

      {favorites.length === 0 ? (
        <div className="p-16 text-center rounded-2xl bg-slate-900/40 border border-slate-800/60 space-y-3">
          <div className="w-12 h-12 rounded-2xl bg-amber-500/10 text-amber-400 mx-auto flex items-center justify-center">
            <Star className="w-6 h-6 stroke-1" />
          </div>
          <h3 className="text-sm font-bold text-slate-200">لا توجد عناصر محفوظة حتى الآن</h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto leading-relaxed">
            اضغط على أيقونة النجمة ⭐ الموجودة في أي كارت أداة أو ملف DUMP لحفظها هنا لسهولة الوصول إليها أثناء العمل في ورشة الصيانة.
          </p>
        </div>
      ) : filtered.length === 0 ? (
        <div className="p-10 text-center text-slate-500 bg-slate-900/40 rounded-2xl border border-slate-800/60">
          لا توجد نتائج تطابق بحثك في المفضلة
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {filtered.map((item) => (
            <ItemCard
              key={item.id || item.name}
              item={item}
              isFav={true}
              onToggleFav={onToggleFav}
              onCopyToast={onCopyToast}
            />
          ))}
        </div>
      )}
    </div>
  );
};
