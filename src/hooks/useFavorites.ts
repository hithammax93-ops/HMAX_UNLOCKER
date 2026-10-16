import { useState, useEffect } from 'react';
import { ItemData } from '../data/hmaxData';

const STORAGE_KEY = 'hmax_favorites_v1';

export function useFavorites() {
  const [favorites, setFavorites] = useState<ItemData[]>(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(favorites));
    } catch (e) {
      console.error('Failed to save favorites to localStorage', e);
    }
  }, [favorites]);

  const toggleFavorite = (item: ItemData) => {
    setFavorites(prev => {
      const exists = prev.some(fav => fav.id === item.id || fav.name === item.name);
      if (exists) {
        return prev.filter(fav => fav.id !== item.id && fav.name !== item.name);
      } else {
        return [item, ...prev];
      }
    });
  };

  const isFavorite = (item: ItemData) => {
    return favorites.some(fav => fav.id === item.id || fav.name === item.name);
  };

  return { favorites, toggleFavorite, isFavorite };
}
