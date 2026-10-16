import { useState, useEffect } from 'react';

export interface RankTier {
  threshold: number;
  name: string;
  nameEn: string;
  key: string;
  color: string;
  badge: string;
}

export const USER_RANKS: RankTier[] = [
  { threshold: 0, name: "عضو جديد", nameEn: "Newbie", key: "newbie", color: "from-slate-500 to-slate-700", badge: "⚪" },
  { threshold: 50, name: "عضو نشط", nameEn: "Active", key: "active", color: "from-emerald-500 to-teal-700", badge: "🟢" },
  { threshold: 150, name: "عضو متميز", nameEn: "Distinguished", key: "distinguished", color: "from-blue-500 to-indigo-700", badge: "🔵" },
  { threshold: 300, name: "عضو ذهبي", nameEn: "Gold Member", key: "gold", color: "from-amber-400 to-orange-600", badge: "🟡" },
  { threshold: 600, name: "عضو بلاتيني", nameEn: "Platinum", key: "platinum", color: "from-purple-500 to-pink-700", badge: "🟣" },
  { threshold: 1200, name: "VIP ملكي", nameEn: "Royal VIP", key: "vip", color: "from-yellow-400 to-amber-600", badge: "👑" },
  { threshold: 1500, name: "HMAX Legend", nameEn: "Legend", key: "legend", color: "from-cyan-400 to-blue-600", badge: "🌟" }
];

export interface Achievement {
  id: string;
  title: string;
  desc: string;
  target: number;
  type: 'points' | 'streak';
  reward: number;
}

export const ACHIEVEMENTS_LIST: Achievement[] = [
  { id: "p100", title: "💯 أول 100 نقطة", desc: "اجمع 100 نقطة من تفاعلك واستخدام الأدوات", target: 100, type: 'points', reward: 20 },
  { id: "p500", title: "🚀 500 نقطة خبرة", desc: "تخطي حاجز 500 نقطة في مركز HMAX", target: 500, type: 'points', reward: 60 },
  { id: "p1000", title: "🔥 1000 نقطة مهندس محترف", desc: "الوصول إلى 1000 نقطة نشاط فني", target: 1000, type: 'points', reward: 150 },
  { id: "s7", title: "🔥 سلسلة 7 أيام نشاط", desc: "تسجيل دخول يومي متتالي لمدة أسبوع", target: 7, type: 'streak', reward: 50 },
  { id: "s30", title: "🏆 بطل الشهر 30 يوم", desc: "سلسلة تفاعل متصلة لمدة 30 يوماً", target: 30, type: 'streak', reward: 250 }
];

export function useTechRank() {
  const [points, setPoints] = useState<number>(() => {
    try {
      const v = localStorage.getItem('hmax_tech_points_v1');
      return v ? parseInt(v, 10) : 45; // Start with active welcoming points
    } catch {
      return 45;
    }
  });

  const [streak, setStreak] = useState<number>(() => {
    try {
      const v = localStorage.getItem('hmax_tech_streak_v1');
      return v ? parseInt(v, 10) : 3;
    } catch {
      return 3;
    }
  });

  const [lastCheckin, setLastCheckin] = useState<string>(() => {
    try {
      return localStorage.getItem('hmax_last_checkin_v1') || '';
    } catch {
      return '';
    }
  });

  const [claimedAchievements, setClaimedAchievements] = useState<string[]>(() => {
    try {
      const v = localStorage.getItem('hmax_claimed_achieve_v1');
      return v ? JSON.parse(v) : [];
    } catch {
      return [];
    }
  });

  const [vipUntil, setVipUntil] = useState<string | null>(() => {
    try {
      return localStorage.getItem('hmax_vip_until_v1');
    } catch {
      return null;
    }
  });

  // Save changes
  useEffect(() => {
    try {
      localStorage.setItem('hmax_tech_points_v1', points.toString());
      localStorage.setItem('hmax_tech_streak_v1', streak.toString());
      localStorage.setItem('hmax_last_checkin_v1', lastCheckin);
      localStorage.setItem('hmax_claimed_achieve_v1', JSON.stringify(claimedAchievements));
      if (vipUntil) {
        localStorage.setItem('hmax_vip_until_v1', vipUntil);
      } else {
        localStorage.removeItem('hmax_vip_until_v1');
      }
    } catch (e) {
      console.error(e);
    }
  }, [points, streak, lastCheckin, claimedAchievements, vipUntil]);

  // Calculate current rank
  let currentRank = USER_RANKS[0];
  let nextRank: RankTier | null = USER_RANKS[1];

  for (let i = 0; i < USER_RANKS.length; i++) {
    if (points >= USER_RANKS[i].threshold) {
      currentRank = USER_RANKS[i];
      nextRank = USER_RANKS[i + 1] || null;
    }
  }

  const addPoints = (amount: number, reason?: string) => {
    setPoints((prev) => prev + amount);
  };

  const claimDailyCheckin = (): { success: boolean; message: string } => {
    const today = new Date().toISOString().split('T')[0];
    if (lastCheckin === today) {
      return { success: false, message: 'لقد سجلت حضورك اليوم بالفعل! عُد غداً لمواصلة السلسلة.' };
    }

    const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];
    const newStreak = lastCheckin === yesterday ? streak + 1 : 1;

    setStreak(newStreak);
    setLastCheckin(today);
    setPoints((p) => p + 10);

    return {
      success: true,
      message: `🎉 تم تسجيل الحضور اليومي بنجاح! +10 نقاط (سلسلتك الآن: ${newStreak} أيام)`
    };
  };

  const claimAchievement = (id: string): { success: boolean; message: string } => {
    if (claimedAchievements.includes(id)) {
      return { success: false, message: 'تم استلام مكافأة هذا الإنجاز مسبقاً.' };
    }
    const ach = ACHIEVEMENTS_LIST.find((a) => a.id === id);
    if (!ach) return { success: false, message: 'إنجاز غير معروف' };

    const satisfied = ach.type === 'points' ? points >= ach.target : streak >= ach.target;
    if (!satisfied) {
      return { success: false, message: 'لم تحقق شروط الإنجاز بعد!' };
    }

    setClaimedAchievements((prev) => [...prev, id]);
    setPoints((p) => p + ach.reward);
    return {
      success: true,
      message: `🏆 مبروك! حصلت على مكافأة ${ach.title} (+${ach.reward} نقطة)`
    };
  };

  const buyVip = (days: number, cost: number): { success: boolean; message: string } => {
    if (points < cost) {
      return { success: false, message: `عفواً، رصيد نقاطك (${points}) غير كافٍ. تحتاج إلى ${cost - points} نقطة إضافية.` };
    }
    setPoints((p) => p - cost);
    const expireDate = new Date(Date.now() + days * 86400000).toISOString();
    setVipUntil(expireDate);
    return {
      success: true,
      message: `👑 تم تفعيل اشتراك VIP الملكي لمدة ${days} يوماً بنجاح!`
    };
  };

  const isVipActive = vipUntil ? new Date(vipUntil) > new Date() : false;

  return {
    points,
    streak,
    currentRank,
    nextRank,
    claimedAchievements,
    isVipActive,
    vipUntil,
    addPoints,
    claimDailyCheckin,
    claimAchievement,
    buyVip
  };
}
