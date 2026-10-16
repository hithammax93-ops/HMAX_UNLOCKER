import datetime
import io
import json
import sys
import threading
import time
from firebase_admin import firestore
from telebot import types
import hmax_i18n as hmaxi18n

BOT = None
DB = None
ADMIN_ID = 0
STOP_EVENT = threading.Event()
PRODUCT_CACHE = {"items": [], "at": 0.0}
PRODUCT_CACHE_LOCK = threading.Lock()
CACHE_TTL = 60

STORE = {
    "vip7": ("👑 VIP 7 أيام", 250, 7),
    "vip30": ("👑 VIP 30 يوم", 800, 30),
}

LEVELS = [
    (0, "🌱 مبتدئ"),
    (100, "⚡ عضو نشط"),
    (300, "🔥 محترف"),
    (700, "💎 VIP Elite"),
    (1500, "👑 HMAX Legend"),
]

def now():
    return datetime.datetime.now(datetime.timezone.utc)

def uid(x):
    return str(int(x))

def admin(x):
    return int(x) == int(ADMIN_ID)

def audit(action, user_id, details=""):
    if not DB:
        return
    try:
        DB.collection("admin_audit_logs").add({
            "action": str(action),
            "user_id": int(user_id),
            "details": str(details)[:2000],
            "timestamp": now().isoformat(),
        })
    except Exception:
        pass

def level_for(points):
    current = LEVELS[0]
    for row in LEVELS:
        if points >= row[0]:
            current = row
    return current[1], current[0]

def profile(user_id):
    if not DB:
        return "⚠️ Firebase غير متصل."
    try:
        d = DB.collection("users").document(uid(user_id)).get().to_dict() or {}
        pts = int(d.get("points", 0) or 0)
        streak = int(d.get("daily_streak", 0) or 0)
        fav = len(d.get("favorites", []) or [])
        vip = d.get("vip_until")
        level, threshold = level_for(pts)
        invited = int(d.get("referral_count", d.get("invites", 0)) or 0)
        orders = DB.collection("user_requests").where("user_id", "==", int(user_id)).count().get()[0][0].value
        return (
            "👤 <b>HMAX PROFILE</b>\n━━━━━━━━━━━━━━━━\n"
            f"🆔 <code>{user_id}</code>\n"
            f"⭐ النقاط: <b>{pts}</b>\n"
            f"🏆 المستوى: <b>{level}</b>\n"
            f"🔥 السلسلة: <b>{streak}</b> يوم\n"
            f"👥 الإحالات: <b>{invited}</b>\n"
            f"📩 الطلبات: <b>{orders}</b>\n"
            f"⭐ المفضلة: <b>{fav}</b>\n"
            f"👑 VIP: <b>{'نعم' if vip else 'لا'}</b>"
        )
    except Exception as e:
        return f"❌ تعذر تحميل الملف: {e}"

def claim_achievement(user_id, aid, title, reward):
    ref = DB.collection("users").document(uid(user_id))
    led = DB.collection("achievement_claims").document(f"{uid(user_id)}_{aid}")
    tx = DB.transaction()

    @firestore.transactional
    def run(t):
        if led.get(transaction=t).exists:
            return False
        t.set(led, {"user_id": int(user_id), "achievement_id": aid, "title": title,
                    "reward": reward, "at": now().isoformat()})
        t.set(ref, {"points": firestore.Increment(reward)}, merge=True)
        return True

    try:
        return bool(run(tx))
    except Exception:
        return False

def check_achievements(user_id):
    if not DB:
        return []
    achievements = [
        ("p100", "💯 أول 100 نقطة", 100, 20),
        ("p500", "🚀 500 نقطة", 500, 60),
        ("p1000", "🔥 1000 نقطة", 1000, 150),
        ("s7", "🔥 سلسلة 7 أيام", 7, 50),
        ("s30", "🏆 سلسلة 30 يوم", 30, 250),
    ]
    try:
        d = DB.collection("users").document(uid(user_id)).get().to_dict() or {}
        pts = int(d.get("points", 0) or 0)
        streak = int(d.get("daily_streak", 0) or 0)
        out = []
        for aid, title, target, reward in achievements:
            hit = pts >= target if aid.startswith("p") else streak >= target
            if hit and claim_achievement(user_id, aid, title, reward):
                out.append((title, reward))
        return out
    except Exception:
        return []

def buy(user_id, item_id):
    if not DB or item_id not in STORE:
        return False, "❌ المنتج غير موجود."
    title, cost, days = STORE[item_id]
    ref = DB.collection("users").document(uid(user_id))
    tx = DB.transaction()

    @firestore.transactional
    def run(t):
        d = ref.get(transaction=t).to_dict() or {}
        pts = int(d.get("points", 0) or 0)
        if pts < cost:
            return False, f"❌ تحتاج {cost - pts} نقطة إضافية."
        base = now()
        old = d.get("vip_until")
        if old:
            try:
                olddt = datetime.datetime.fromisoformat(str(old))
                if olddt.tzinfo is None:
                    olddt = olddt.replace(tzinfo=datetime.timezone.utc)
                if olddt > base:
                    base = olddt
            except Exception:
                pass
        t.set(ref, {"points": firestore.Increment(-cost),
                    "vip_until": (base + datetime.timedelta(days=days)).isoformat()}, merge=True)
        DB.collection("point_purchases").document(
            f"{uid(user_id)}_{item_id}_{int(time.time() * 1000)}"
        ).set({"user_id": int(user_id), "item_id": item_id, "cost": cost, "at": now().isoformat()})
        return True, f"🎉 تم شراء {title}."

    try:
        return run(tx)
    except Exception as e:
        return False, f"❌ {e}"

def product_list(force=False):
    if not DB:
        return []
    # Fast path: cache hit, no lock required.
    if not force and time.time() - PRODUCT_CACHE["at"] < CACHE_TTL:
        return PRODUCT_CACHE["items"]
    with PRODUCT_CACHE_LOCK:
        # Another thread may have refreshed the cache while we waited.
        if not force and time.time() - PRODUCT_CACHE["at"] < CACHE_TTL:
            return PRODUCT_CACHE["items"]
        try:
            rows = []
            for doc in DB.collection("dynamic_products").where("active", "==", True).limit(300).stream():
                d = doc.to_dict() or {}
                rows.append((doc.id, d))
            PRODUCT_CACHE["items"] = rows
            PRODUCT_CACHE["at"] = time.time()
            return rows
        except Exception:
            return PRODUCT_CACHE["items"]

def localized_name(data, language, fallback=""):
    language = language if language in ("en", "fr") else "ar"
    return str(data.get("name_" + language) or data.get("name") or fallback)

def add_product(admin_id, payload):
    parts = [x.strip() for x in payload.split("|")]
    if len(parts) == 4:
        key, name, url, price = parts
        name_en = name_fr = ""
    elif len(parts) == 6:
        key, name, name_en, name_fr, url, price = parts
    else:
        return "⚙️ /productadd المعرف|الاسم_العربي|الرابط|السعر أو /productadd المعرف|الاسم_العربي|الاسم_الإنجليزي|الاسم_الفرنسي|الرابط|السعر"
    try:
        price = float(price)
    except ValueError:
        return "❌ السعر غير صحيح."
    DB.collection("dynamic_products").document(key).set({
        "name": name, "name_en": name_en, "name_fr": name_fr,
        "url": url, "price": price, "active": True,
        "updated_at": now().isoformat(), "updated_by": int(admin_id)
    }, merge=True)
    PRODUCT_CACHE["at"] = 0
    audit("product_add", admin_id, key)
    return "✅ تمت إضافة المنتج إلى Firebase."

def disable_product(admin_id, key):
    if not key:
        return "❌ حدد معرف المنتج."
    DB.collection("dynamic_products").document(key).set({
        "active": False, "updated_at": now().isoformat(), "updated_by": int(admin_id)
    }, merge=True)
    PRODUCT_CACHE["at"] = 0
    audit("product_disable", admin_id, key)
    return "✅ تم تعطيل المنتج."

def add_offer(admin_id, payload):
    parts = [x.strip() for x in payload.split("|")]
    if len(parts) == 5:
        key, name, discount, hours, max_uses = parts
        name_en = name_fr = ""
    elif len(parts) == 7:
        key, name, name_en, name_fr, discount, hours, max_uses = parts
    else:
        return "⚙️ /offeradd المعرف|الاسم_العربي|الخصم|الساعات|عدد_الاستخدامات أو /offeradd المعرف|الاسم_العربي|الاسم_الإنجليزي|الاسم_الفرنسي|الخصم|الساعات|عدد_الاستخدامات"
    try:
        discount = max(1, min(100, int(discount)))
        hours = max(1, int(hours))
        max_uses = max(0, int(max_uses))
    except ValueError:
        return "❌ بيانات العرض غير صحيحة."
    DB.collection("offers").document(key).set({
        "name": name, "name_en": name_en, "name_fr": name_fr,
        "discount": discount, "created_at": now().isoformat(),
        "expires_at": (now() + datetime.timedelta(hours=hours)).isoformat(),
        "max_uses": max_uses, "uses": 0, "active": True, "updated_by": int(admin_id)
    }, merge=True)
    audit("offer_add", admin_id, key)
    return "🎁 تم إنشاء العرض المؤقت."

def active_offers():
    if not DB:
        return []
    out = []
    for doc in DB.collection("offers").where("active", "==", True).limit(100).stream():
        d = doc.to_dict() or {}
        try:
            if datetime.datetime.fromisoformat(str(d.get("expires_at"))) <= now():
                continue
        except Exception:
            continue
        out.append((doc.id, d))
    return out

def redeem_offer(user_id, key):
    ref = DB.collection("offers").document(key)
    claim = DB.collection("offer_claims").document(f"{key}_{uid(user_id)}")
    tx = DB.transaction()

    @firestore.transactional
    def run(t):
        if claim.get(transaction=t).exists:
            return False, "⚠️ استخدمت هذا العرض من قبل."
        snap = ref.get(transaction=t)
        if not snap.exists:
            return False, "❌ العرض غير موجود."
        d = snap.to_dict() or {}
        if not d.get("active", False):
            return False, "❌ العرض غير فعال."
        try:
            if datetime.datetime.fromisoformat(str(d.get("expires_at"))) <= now():
                return False, "⏰ انتهى العرض."
        except Exception:
            return False, "❌ تاريخ العرض غير صالح."
        uses = int(d.get("uses", 0) or 0)
        max_uses = int(d.get("max_uses", 0) or 0)
        if max_uses and uses >= max_uses:
            return False, "❌ اكتمل عدد استخدامات العرض."
        t.set(claim, {"user_id": int(user_id), "offer_id": key, "at": now().isoformat()})
        t.set(ref, {"uses": firestore.Increment(1)}, merge=True)
        return True, f"🎁 تم تفعيل خصم {d.get('discount', 0)}% لك."

    try:
        return run(tx)
    except Exception as e:
        return False, f"❌ {e}"

def rate_service(user_id, service, stars):
    try:
        stars = int(stars)
    except ValueError:
        return False, "❌ التقييم يجب أن يكون من 1 إلى 5."
    if stars < 1 or stars > 5:
        return False, "❌ التقييم يجب أن يكون من 1 إلى 5."
    ref = DB.collection("service_ratings").document(f"{uid(user_id)}_{service}")
    if ref.get().exists:
        return False, "⚠️ لقد قيّمت هذه الخدمة مسبقًا."
    ref.set({"user_id": int(user_id), "service": service[:150], "stars": stars, "at": now().isoformat()})
    audit("service_rating", user_id, f"{service}:{stars}")
    return True, "⭐ تم حفظ تقييمك."

def service_rating_stats(service):
    total = count = 0
    for doc in DB.collection("service_ratings").where("service", "==", service).limit(1000).stream():
        stars = int((doc.to_dict() or {}).get("stars", 0) or 0)
        if stars:
            total += stars
            count += 1
    return count, (round(total / count, 2) if count else 0)

def safe_action(user_id, action, cooldown=10):
    if not DB:
        return True
    ref = DB.collection("anti_fraud").document(f"{uid(user_id)}_{action}")
    tx = DB.transaction()

    @firestore.transactional
    def run(t):
        snap = ref.get(transaction=t)
        d = snap.to_dict() or {}
        last = float(d.get("last", 0) or 0)
        if time.time() - last < cooldown:
            return False
        t.set(ref, {"last": time.time(), "count": firestore.Increment(1)}, merge=True)
        return True

    try:
        return bool(run(tx))
    except Exception:
        return False

def admin_stats():
    if not DB:
        return "❌ Firebase غير متصل."
    try:
        users = DB.collection("users").count().get()[0][0].value
        requests = DB.collection("user_requests").count().get()[0][0].value
        ratings = DB.collection("service_ratings").count().get()[0][0].value
        products = DB.collection("dynamic_products").where("active", "==", True).count().get()[0][0].value
        return f"📊 <b>HMAX Dashboard</b>\n👥 المستخدمون: {users}\n📩 الطلبات: {requests}\n⭐ تقييمات الخدمات: {ratings}\n🛒 المنتجات الديناميكية: {products}"
    except Exception as e:
        return f"❌ {e}"

def daily_report():
    if not DB:
        return "❌ Firebase غير متصل."
    try:
        today = now().astimezone(datetime.timezone(datetime.timedelta(hours=3))).date().isoformat()
        data = DB.collection("daily_stats").document(today).get().to_dict() or {}
        return f"📅 <b>تقرير اليوم {today}</b>\n👥 زيارات: {data.get('visits', 0)}\n🛠️ نقرات أدوات: {data.get('tool_clicks', 0)}\n📩 طلبات: {data.get('requests', 0)}"
    except Exception as e:
        return f"❌ {e}"

def export_backup():
    collections = ["users", "user_requests", "dynamic_products", "dynamic_tools",
                    "offers", "offer_claims", "service_ratings", "admin_audit_logs"]
    data = {"service": "HMAX-UNLOCKER", "generated_at": now().isoformat(), "collections": {}}
    for name in collections:
        rows = []
        try:
            for doc in DB.collection(name).limit(10000).stream():
                rows.append({"id": doc.id, "data": doc.to_dict()})
        except Exception:
            pass
        data["collections"][name] = rows
    return json.dumps(data, ensure_ascii=False, default=str, indent=2).encode("utf-8")

def scheduled_backup_loop():
    while not STOP_EVENT.wait(300):
        try:
            setting = DB.collection("settings").document("backup_schedule").get().to_dict() or {}
            if not setting.get("enabled"):
                continue
            hour = int(setting.get("hour", 3))
            today = now().astimezone(datetime.timezone(datetime.timedelta(hours=3))).date().isoformat()
            last = str(setting.get("last_run", ""))
            local = now().astimezone(datetime.timezone(datetime.timedelta(hours=3)))
            if local.hour != hour or last == today:
                continue
            payload = export_backup()
            msg = io.BytesIO(payload)
            msg.name = f"HMAX_auto_backup_{today}.json"
            BOT.send_document(ADMIN_ID, msg, caption=f"💾 النسخة الاحتياطية التلقائية — {today}")
            DB.collection("settings").document("backup_schedule").set({"last_run": today}, merge=True)
        except Exception as exc:
            try:
                DB.collection("runtime_errors").add({"kind": "scheduled_backup", "error": str(exc)[:2000], "at": now().isoformat()})
            except Exception:
                pass

def install(bot, db, admin_id):
    global BOT, DB, ADMIN_ID
    BOT, DB, ADMIN_ID = bot, db, int(admin_id)
    if not DB:
        return

    @bot.message_handler(commands=["profile"])
    def profile_cmd(m):
        bot.send_message(m.chat.id, profile(m.chat.id), parse_mode="HTML")
        new = check_achievements(m.chat.id)
        if new:
            bot.send_message(m.chat.id, "🏆 إنجازات جديدة:\n" + "\n".join(f"{a} (+{r})" for a, r in new))

    @bot.message_handler(commands=["achievements"])
    def achievements_cmd(m):
        claimed = set()
        try:
            for x in DB.collection("achievement_claims").where("user_id", "==", int(m.chat.id)).limit(100).stream():
                claimed.add((x.to_dict() or {}).get("achievement_id"))
        except Exception:
            pass
        labels = [("p100","💯 أول 100 نقطة",20),("p500","🚀 500 نقطة",60),("p1000","🔥 1000 نقطة",150),("s7","🔥 سلسلة 7 أيام",50),("s30","🏆 سلسلة 30 يوم",250)]
        bot.send_message(m.chat.id, "🏆 <b>إنجازات HMAX</b>\n" + "\n".join(
            f"{'✅' if a in claimed else '🔒'} {t} (+{r})" for a,t,r in labels
        ), parse_mode="HTML")

    @bot.message_handler(commands=["store"])
    def store_cmd(m):
        mk = types.InlineKeyboardMarkup(row_width=1)
        for k, (title, cost, days) in STORE.items():
            mk.add(types.InlineKeyboardButton(f"{title} — {cost} نقطة", callback_data=f"probuy_{k}"))
        bot.send_message(m.chat.id, "🛒 <b>متجر نقاط HMAX</b>", reply_markup=mk, parse_mode="HTML")

    @bot.callback_query_handler(func=lambda c: str(c.data).startswith("probuy_"))
    def buy_cb(c):
        if not safe_action(c.from_user.id, "store", 2):
            bot.answer_callback_query(c.id, "⏳ انتظر قليلًا.", show_alert=True)
            return
        ok, msg = buy(c.from_user.id, str(c.data)[7:])
        bot.answer_callback_query(c.id, msg[:190], show_alert=True)
        if ok:
            new = check_achievements(c.from_user.id)
            if new:
                bot.send_message(c.from_user.id, "🏆 إنجاز جديد:\n" + "\n".join(f"{a} (+{r})" for a, r in new))

    @bot.message_handler(commands=["products"])
    def products_cmd(m):
        language = hmaxi18n.get_language(m.chat.id)
        rows = product_list()
        if not rows:
            bot.send_message(m.chat.id, "🛒 لا توجد منتجات ديناميكية منشورة حاليًا.")
            return
        bot.send_message(m.chat.id, "🛒 <b>المنتجات المنشورة</b>\n\n" + "\n".join(
            f"• <b>{localized_name(d, language, k)}</b> — {d.get('price', 0)}\n{d.get('url', '')}" for k,d in rows[:30]
        ), parse_mode="HTML", disable_web_page_preview=True)

    @bot.message_handler(commands=["offers"])
    def offers_cmd(m):
        language = hmaxi18n.get_language(m.chat.id)
        rows = active_offers()
        if not rows:
            bot.send_message(m.chat.id, "🎁 لا توجد عروض فعالة الآن.")
            return
        bot.send_message(m.chat.id, "🎁 <b>العروض الحالية</b>\n\n" + "\n".join(
            f"• <code>{k}</code> — {localized_name(d, language, 'عرض')} — {d.get('discount',0)}% off — {d.get('expires_at')}" for k,d in rows
        ), parse_mode="HTML")

    @bot.message_handler(commands=["rate"])
    def rate_cmd(m):
        p = (m.text or "").split(maxsplit=2)
        if len(p) < 3:
            bot.send_message(m.chat.id, "⭐ الاستخدام: /rate معرف_الخدمة 1-5")
            return
        ok, msg = rate_service(m.chat.id, p[1], p[2])
        bot.send_message(m.chat.id, msg)

    @bot.message_handler(commands=["ratings"])
    def ratings_cmd(m):
        p = (m.text or "").split(maxsplit=1)
        if len(p) < 2:
            bot.send_message(m.chat.id, "⭐ الاستخدام: /ratings معرف_الخدمة")
            return
        count, avg = service_rating_stats(p[1])
        bot.send_message(m.chat.id, f"⭐ {p[1]}\nالمشاركون: {count}\nالمتوسط: {avg}/5")

    @bot.message_handler(commands=["productadd"])
    def productadd_cmd(m):
        if admin(m.chat.id):
            p=(m.text or "").split(maxsplit=1)
            bot.send_message(m.chat.id, add_product(m.chat.id, p[1] if len(p)>1 else ""))

    @bot.message_handler(commands=["productdel"])
    def productdel_cmd(m):
        if admin(m.chat.id):
            p=(m.text or "").split(maxsplit=1)
            bot.send_message(m.chat.id, disable_product(m.chat.id, p[1] if len(p)>1 else ""))

    @bot.message_handler(commands=["offeradd"])
    def offeradd_cmd(m):
        if admin(m.chat.id):
            p=(m.text or "").split(maxsplit=1)
            bot.send_message(m.chat.id, add_offer(m.chat.id, p[1] if len(p)>1 else ""))

    @bot.message_handler(commands=["offeruse"])
    def offeruse_cmd(m):
        p=(m.text or "").split(maxsplit=1)
        if len(p) < 2:
            bot.send_message(m.chat.id, "⚙️ /offeruse معرف_العرض")
            return
        ok,msg=redeem_offer(m.chat.id,p[1])
        bot.send_message(m.chat.id,msg)

    @bot.message_handler(commands=["dashboard"])
    def dashboard_cmd(m):
        if admin(m.chat.id):
            bot.send_message(m.chat.id, admin_stats(), parse_mode="HTML")

    @bot.message_handler(commands=["report"])
    def report_cmd(m):
        if admin(m.chat.id):
            bot.send_message(m.chat.id, daily_report(), parse_mode="HTML")

    @bot.message_handler(commands=["backup_auto"])
    def backup_auto_cmd(m):
        if not admin(m.chat.id):
            return
        p=(m.text or "").split()
        if len(p) < 2 or p[1].lower() not in ("on","off"):
            bot.send_message(m.chat.id, "⚙️ /backup_auto on 3\nأو /backup_auto off")
            return
        enabled=p[1].lower()=="on"
        hour=int(p[2]) if len(p)>2 and p[2].isdigit() else 3
        DB.collection("settings").document("backup_schedule").set({"enabled":enabled,"hour":max(0,min(23,hour))},merge=True)
        bot.send_message(m.chat.id, f"💾 النسخ التلقائي: {'🟢' if enabled else '🔴'}")

    @bot.message_handler(commands=["release"])
    def release_cmd(m):
        if not admin(m.chat.id):
            return
        p=(m.text or "").split(maxsplit=2)
        if len(p)<3:
            bot.send_message(m.chat.id, "⚙️ /release الإصدار ملاحظات")
            return
        DB.collection("settings").document("latest_release").set({"version":p[1],"notes":p[2],"at":now().isoformat()},merge=True)
        audit("release_publish",m.chat.id,p[1])
        bot.send_message(m.chat.id,"✅ تم تسجيل الإصدار داخليًا.")

    @bot.message_handler(commands=["version"])
    def version_cmd(m):
        d=DB.collection("settings").document("latest_release").get().to_dict() or {}
        bot.send_message(m.chat.id,f"🔄 <b>HMAX</b>\nالإصدار: <b>{d.get('version','غير محدد')}</b>\n{d.get('notes','')}",parse_mode="HTML")

    @bot.message_handler(commands=["health"])
    def health_cmd(m):
        if admin(m.chat.id):
            ok=True
            try: DB.collection("settings").document("system").get()
            except Exception: ok=False
            bot.send_message(m.chat.id, "🩺 HMAX Health\nFirebase: "+("🟢 OK" if ok else "🔴 ERROR"))

    def uncaught(exc_type, exc_value, exc_tb):
        try:
            DB.collection("runtime_errors").add({"kind":"uncaught","error":str(exc_value)[:3000],"at":now().isoformat()})
        except Exception:
            pass
        sys.__excepthook__(exc_type, exc_value, exc_tb)

    sys.excepthook = uncaught
    if not any(t.name == "HMAX-BackupScheduler" for t in threading.enumerate()):
        threading.Thread(target=scheduled_backup_loop, name="HMAX-BackupScheduler", daemon=True).start()
