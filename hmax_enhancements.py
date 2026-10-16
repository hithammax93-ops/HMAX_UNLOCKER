
import base64
import datetime
import io
import json
import threading
import time
from collections import defaultdict, deque

from firebase_admin import firestore
from telebot import types

BOT = None
DB = None
DATA = {}
ADMIN_ID = 0

RATE_LIMITS = {
    "message": (35, 60),
    "callback": (70, 60),
    "start": (8, 60),
    "search": (8, 60),
    "coupon": (5, 60),
}

RATE_EVENTS = defaultdict(deque)
RATE_NOTICE = {}
RATE_LOCK = threading.RLock()
MAINT_CACHE = {"value": False, "message": "", "loaded_at": 0.0}

STREAK_REWARDS = {3: 15, 7: 40, 14: 100, 30: 250, 60: 500, 100: 1000}


def now_utc():
    return datetime.datetime.now(datetime.timezone.utc)


def yemen_today():
    tz = datetime.timezone(datetime.timedelta(hours=3))
    return now_utc().astimezone(tz).date()


def is_admin(user_id):
    try:
        return int(user_id) == int(ADMIN_ID)
    except Exception:
        return False


def uid(user_id):
    return str(int(user_id))


def audit(action, actor_id, target_id=None, details=None):
    if not DB:
        return
    try:
        payload = {
            "action": str(action),
            "actor_id": int(actor_id),
            "timestamp": now_utc().isoformat(),
        }
        if target_id is not None:
            try:
                payload["target_id"] = int(target_id)
            except Exception:
                payload["target_id"] = str(target_id)
        if details:
            payload["details"] = str(details)[:1500]
        DB.collection("admin_audit_logs").add(payload)
    except Exception as exc:
        print(f"HMAX audit error: {exc}")


def load_maintenance(force=False):
    if not DB:
        return False, ""
    current = time.time()
    if not force and current - MAINT_CACHE["loaded_at"] < 10:
        return MAINT_CACHE["value"], MAINT_CACHE["message"]
    try:
        snap = DB.collection("settings").document("system").get()
        data = snap.to_dict() or {}
        value = bool(data.get("maintenance_mode", False))
        message = data.get("maintenance_message") or "🛠️ البوت تحت صيانة مؤقتة الآن. جرّب بعد قليل."
        MAINT_CACHE.update({"value": value, "message": message, "loaded_at": current})
        return value, message
    except Exception:
        return False, ""


def set_maintenance(enabled, message=None, actor_id=None):
    if not DB:
        return False
    try:
        msg = message or "🛠️ البوت تحت صيانة مؤقتة الآن. جرّب بعد قليل."
        DB.collection("settings").document("system").set({
            "maintenance_mode": bool(enabled),
            "maintenance_message": msg,
            "updated_at": now_utc().isoformat(),
            "updated_by": int(actor_id) if actor_id is not None else None,
        }, merge=True)
        MAINT_CACHE.update({"value": bool(enabled), "message": msg, "loaded_at": time.time()})
        if actor_id is not None:
            audit("maintenance_on" if enabled else "maintenance_off", actor_id, details=msg)
        return True
    except Exception as exc:
        print(f"HMAX maintenance error: {exc}")
        return False


def allow_user(user_id, action="message", is_callback=False, callback_id=None):
    if is_admin(user_id):
        return True

    enabled, message = load_maintenance()
    if enabled:
        try:
            if is_callback and callback_id:
                BOT.answer_callback_query(callback_id, "🛠️ البوت تحت الصيانة حالياً.", show_alert=True)
            else:
                BOT.send_message(int(user_id), message)
        except Exception:
            pass
        return False

    limit, window = RATE_LIMITS.get(action, RATE_LIMITS["message"])
    key = (str(user_id), action)
    current = time.time()
    with RATE_LOCK:
        q = RATE_EVENTS[key]
        cutoff = current - window
        while q and q[0] <= cutoff:
            q.popleft()
        if len(q) >= limit:
            last_notice = RATE_NOTICE.get(key, 0)
            if current - last_notice >= 8:
                RATE_NOTICE[key] = current
                if not is_callback:
                    try:
                        BOT.send_message(int(user_id), "⏳ انتظر قليلاً، تم تفعيل حماية الضغط المتكرر.")
                    except Exception:
                        pass
                elif callback_id:
                    try:
                        BOT.answer_callback_query(callback_id, "⏳ انتظر قليلاً.", show_alert=False)
                    except Exception:
                        pass
            return False
        q.append(current)
    return True


def award_tool_reward(user_id, tool_name, points=2, daily_cap=25):
    if not DB or not user_id:
        return False
    today = str(yemen_today())
    tool_key = str(tool_name).strip().lower()[:180]
    raw = f"{uid(user_id)}|{today}|{tool_key}".encode("utf-8")
    reward_id = base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")
    cap_ref = DB.collection("daily_reward_caps").document(f"{uid(user_id)}_{today}")
    reward_ref = DB.collection("tool_reward_ledger").document(reward_id)
    user_ref = DB.collection("users").document(uid(user_id))
    txn = DB.transaction()

    @firestore.transactional
    def apply(txn_obj):
        if reward_ref.get(transaction=txn_obj).exists:
            return False
        cap = cap_ref.get(transaction=txn_obj).to_dict() or {}
        used = list(cap.get("tool_keys", []) or [])
        if len(used) >= daily_cap:
            return False
        used.append(tool_key)
        txn_obj.set(cap_ref, {"tool_keys": used, "date": today}, merge=True)
        txn_obj.set(reward_ref, {
            "user_id": int(user_id),
            "tool_name": str(tool_name)[:200],
            "points": points,
            "date": today,
            "created_at": now_utc().isoformat(),
        })
        txn_obj.set(user_ref, {"points": firestore.Increment(points)}, merge=True)
        return True

    try:
        return bool(apply(txn))
    except Exception as exc:
        print(f"HMAX tool reward error: {exc}")
        return False


def award_request_reward(user_id, points=5, daily_cap=5):
    if not DB:
        return False
    today = str(yemen_today())
    cap_ref = DB.collection("daily_reward_caps").document(f"{uid(user_id)}_{today}")
    user_ref = DB.collection("users").document(uid(user_id))
    txn = DB.transaction()

    @firestore.transactional
    def apply(txn_obj):
        cap = cap_ref.get(transaction=txn_obj).to_dict() or {}
        used = int(cap.get("request_count", 0) or 0)
        if used >= daily_cap:
            return False
        txn_obj.set(cap_ref, {"request_count": used + 1, "date": today}, merge=True)
        txn_obj.set(user_ref, {"points": firestore.Increment(points)}, merge=True)
        return True

    try:
        return bool(apply(txn))
    except Exception as exc:
        print(f"HMAX request reward error: {exc}")
        return False


def sync_daily_streak(user_id):
    if not DB:
        return {"streak": 0, "bonus": 0}
    user_ref = DB.collection("users").document(uid(user_id))
    today = yemen_today()
    today_s = str(today)
    txn = DB.transaction()

    @firestore.transactional
    def apply(txn_obj):
        data = user_ref.get(transaction=txn_obj).to_dict() or {}
        if data.get("daily_streak_date") == today_s:
            return int(data.get("daily_streak", 0) or 0), 0
        previous = data.get("daily_streak_date", "")
        try:
            previous_date = datetime.date.fromisoformat(str(previous))
        except Exception:
            previous_date = None
        streak = int(data.get("daily_streak", 0) or 0)
        streak = streak + 1 if previous_date == today - datetime.timedelta(days=1) else 1
        bonus = int(STREAK_REWARDS.get(streak, 0))
        update = {
            "daily_streak": streak,
            "daily_streak_date": today_s,
        }
        if bonus:
            update["points"] = firestore.Increment(bonus)
            update["last_streak_reward"] = streak
        txn_obj.set(user_ref, update, merge=True)
        return streak, bonus

    try:
        streak, bonus = apply(txn)
        return {"streak": streak, "bonus": bonus}
    except Exception as exc:
        print(f"HMAX streak error: {exc}")
        return {"streak": 0, "bonus": 0}


def encode_key(value):
    return base64.urlsafe_b64encode(str(value).encode("utf-8")).decode("ascii").rstrip("=")


def decode_key(value):
    padding = "=" * (-len(str(value)) % 4)
    return base64.urlsafe_b64decode(str(value) + padding).decode("utf-8")


def catalog_items():
    for category, items in (DATA or {}).items():
        if not isinstance(items, dict):
            continue
        for key, value in items.items():
            name = value[0] if isinstance(value, (list, tuple)) and value else str(value)
            url = value[1] if isinstance(value, (list, tuple)) and len(value) > 1 else ""
            yield category, str(key), str(name), str(url)


def search_catalog(query, limit=10):
    q = str(query or "").strip().lower()
    if not q:
        return []
    results = []
    for category, key, name, url in catalog_items():
        if q in category.lower() or q in key.lower() or q in name.lower():
            results.append((category, key, name, url))
            if len(results) >= limit:
                break
    return results


def toggle_favorite(user_id, category, key):
    if not DB:
        return False
    ref = DB.collection("users").document(uid(user_id))
    token = f"{category}:{key}"
    txn = DB.transaction()

    @firestore.transactional
    def apply(txn_obj):
        data = ref.get(transaction=txn_obj).to_dict() or {}
        favorites = list(data.get("favorites", []) or [])
        if token in favorites:
            favorites.remove(token)
            txn_obj.set(ref, {"favorites": favorites}, merge=True)
            return False
        if len(favorites) >= 100:
            favorites = favorites[-99:]
        favorites.append(token)
        txn_obj.set(ref, {"favorites": favorites}, merge=True)
        return True

    try:
        return bool(apply(txn))
    except Exception as exc:
        print(f"HMAX favorite error: {exc}")
        return False


def get_favorites(user_id):
    if not DB:
        return []
    try:
        data = DB.collection("users").document(uid(user_id)).get().to_dict() or {}
        return list(data.get("favorites", []) or [])
    except Exception:
        return []


def notification_enabled(user_id):
    if not DB:
        return True
    try:
        data = DB.collection("users").document(uid(user_id)).get().to_dict() or {}
        return bool(data.get("notifications_enabled", True))
    except Exception:
        return True


def set_notification_pref(user_id, enabled):
    if not DB:
        return False
    try:
        DB.collection("users").document(uid(user_id)).set({
            "notifications_enabled": bool(enabled),
            "is_subscribed": bool(enabled),
        }, merge=True)
        return True
    except Exception:
        return False


def user_vip(user_id):
    if not DB:
        return False, None
    try:
        data = DB.collection("users").document(uid(user_id)).get().to_dict() or {}
        until = data.get("vip_until")
        if until:
            date_value = datetime.datetime.fromisoformat(str(until))
            if date_value.tzinfo is None:
                date_value = date_value.replace(tzinfo=datetime.timezone.utc)
            if date_value > now_utc():
                return True, date_value
        return int(data.get("points", 0) or 0) >= 1200, None
    except Exception:
        return False, None


def format_admin_stats():
    if not DB:
        return "⚠️ Firebase غير متصل."
    def count(name):
        try:
            return int(DB.collection(name).count().get()[0][0].value)
        except Exception:
            return 0
    maintenance = load_maintenance(True)[0]
    return (
        "📊 <b>HMAX Analytics</b>\\n"
        "━━━━━━━━━━━━━━━━━━\\n"
        f"👥 المستخدمون: <code>{count('users')}</code>\\n"
        f"📩 الطلبات: <code>{count('user_requests')}</code>\\n"
        f"🧾 سجلات الإدارة: <code>{count('admin_audit_logs')}</code>\\n"
        f"🎟️ المطالبات بالكوبونات: <code>{count('coupon_claims')}</code>\\n"
        f"🛠️ الصيانة: <code>{'ON' if maintenance else 'OFF'}</code>"
    )


def coupon_create(admin_id, code, points, max_uses=0, days=0):
    if not DB:
        return False, "Firebase غير متصل."
    code = str(code).strip().upper()
    try:
        points = int(points)
        max_uses = int(max_uses or 0)
        days = int(days or 0)
    except Exception:
        return False, "❌ القيم الرقمية غير صحيحة."
    if not code or len(code) > 40 or points <= 0 or points > 100000:
        return False, "❌ رمز أو قيمة الكوبون غير صالحة."
    doc = {
        "code": code,
        "points": points,
        "max_uses": max_uses,
        "uses": 0,
        "active": True,
        "created_by": int(admin_id),
        "created_at": now_utc().isoformat(),
    }
    if days > 0:
        doc["expires_at"] = (now_utc() + datetime.timedelta(days=days)).isoformat()
    try:
        DB.collection("coupons").document(code).set(doc)
        audit("coupon_create", admin_id, details=f"{code} +{points}")
        return True, f"✅ تم إنشاء الكوبون <code>{code}</code> بقيمة +{points} نقطة."
    except Exception as exc:
        return False, f"❌ {exc}"


def coupon_redeem(user_id, code):
    if not DB:
        return False, "Firebase غير متصل."
    code = str(code).strip().upper()
    coupon_ref = DB.collection("coupons").document(code)
    claim_ref = DB.collection("coupon_claims").document(f"{code}_{uid(user_id)}")
    user_ref = DB.collection("users").document(uid(user_id))
    txn = DB.transaction()

    @firestore.transactional
    def apply(txn_obj):
        coupon = coupon_ref.get(transaction=txn_obj)
        if not coupon.exists:
            return None, "❌ الكوبون غير موجود."
        data = coupon.to_dict() or {}
        if not data.get("active", True):
            return None, "❌ الكوبون غير فعال."
        if claim_ref.get(transaction=txn_obj).exists:
            return None, "⚠️ استخدمت هذا الكوبون مسبقاً."
        expiry = data.get("expires_at")
        if expiry:
            try:
                exp = datetime.datetime.fromisoformat(str(expiry))
                if exp.tzinfo is None:
                    exp = exp.replace(tzinfo=datetime.timezone.utc)
                if now_utc() >= exp:
                    return None, "⌛ انتهت صلاحية الكوبون."
            except Exception:
                pass
        max_uses = int(data.get("max_uses", 0) or 0)
        uses = int(data.get("uses", 0) or 0)
        if max_uses and uses >= max_uses:
            return None, "⚠️ انتهت الكمية المتاحة."
        points = int(data.get("points", 0) or 0)
        txn_obj.set(claim_ref, {
            "user_id": int(user_id),
            "code": code,
            "points": points,
            "claimed_at": now_utc().isoformat(),
        })
        txn_obj.set(coupon_ref, {"uses": uses + 1}, merge=True)
        txn_obj.set(user_ref, {"points": firestore.Increment(points)}, merge=True)
        return points, None

    try:
        points, error = apply(txn)
        if error:
            return False, error
        audit("coupon_redeem", user_id, details=code)
        return True, f"🎉 تم استبدال الكوبون والحصول على +{points} نقطة."
    except Exception as exc:
        return False, f"❌ تعذر استخدام الكوبون: {exc}"


def send_search(chat_id, query):
    results = search_catalog(query, 10)
    if not results:
        BOT.send_message(chat_id, "🔎 لم أجد نتائج مطابقة.")
        return
    markup = types.InlineKeyboardMarkup(row_width=1)
    for category, key, name, url in results:
        token = encode_key(f"{category}|{key}")
        markup.add(types.InlineKeyboardButton(f"⭐ {name}"[:60], callback_data=f"enh_fav_{token}"))
    lines = [f"🔎 <b>نتائج البحث عن:</b> {query}", ""]
    for category, key, name, url in results:
        lines.append(f"▫️ <b>{name}</b> — {category}")
    lines.append("")
    lines.append("اضغط على النتيجة لإضافتها أو إزالتها من المفضلة.")
    BOT.send_message(chat_id, "\\n".join(lines), reply_markup=markup, parse_mode="HTML")


def send_favorites(chat_id):
    favorites = get_favorites(chat_id)
    if not favorites:
        BOT.send_message(chat_id, "⭐ مفضلتك فارغة حالياً.\\nاستخدم /search اسم_الأداة لإضافة الأدوات.")
        return
    lookup = {(c, k): (n, u) for c, k, n, u in catalog_items()}
    markup = types.InlineKeyboardMarkup(row_width=1)
    shown = 0
    for token in favorites:
        if ":" not in token:
            continue
        category, key = token.split(":", 1)
        item = lookup.get((category, key))
        if not item:
            continue
        name, url = item
        enc = encode_key(token)
        markup.add(types.InlineKeyboardButton(f"🗑️ {name}"[:60], callback_data=f"enh_fav_{enc}"))
        shown += 1
        if shown >= 50:
            break
    BOT.send_message(chat_id, f"⭐ أدواتك المفضلة: {shown}", reply_markup=markup)


def send_requests_admin(chat_id):
    if not DB:
        return
    rows = []
    try:
        docs = DB.collection("user_requests").where("status", "==", "pending").limit(20).stream()
        rows = [(doc.id, doc.to_dict() or {}) for doc in docs]
    except Exception:
        try:
            docs = DB.collection("user_requests").limit(20).stream()
            rows = [(doc.id, doc.to_dict() or {}) for doc in docs]
        except Exception:
            rows = []
    if not rows:
        BOT.send_message(chat_id, "📩 لا توجد طلبات معلقة حالياً.")
        return
    for request_id, row in rows:
        uid_value = row.get("user_id", "")
        name = row.get("user_name", "غير معروف")
        request_text = row.get("request_text", "")
        status = row.get("status", "pending")
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup.add(
            types.InlineKeyboardButton("🟡 معالجة", callback_data=f"enh_req_{request_id}_processing"),
            types.InlineKeyboardButton("✅ مكتمل", callback_data=f"enh_req_{request_id}_done"),
            types.InlineKeyboardButton("❌ إلغاء", callback_data=f"enh_req_{request_id}_cancelled"),
        )
        BOT.send_message(
            chat_id,
            f"📩 <b>طلب {request_id}</b>\\n👤 {name} — {uid_value}\\n📝 {request_text}\\n📌 الحالة: <b>{status}</b>",
            reply_markup=markup,
            parse_mode="HTML",
        )


def admin_backup(chat_id):
    if not DB:
        BOT.send_message(chat_id, "❌ Firebase غير متصل.")
        return
    collections = ["users", "user_requests", "coupons", "coupon_claims", "admin_audit_logs"]
    backup = {"generated_at": now_utc().isoformat(), "service": "HMAX-UNLOCKER", "collections": {}}
    for name in collections:
        rows = []
        try:
            for doc in DB.collection(name).limit(3000).stream():
                rows.append({"id": doc.id, "data": doc.to_dict() or {}})
        except Exception as exc:
            rows.append({"error": str(exc)})
        backup["collections"][name] = rows
    payload = json.dumps(backup, ensure_ascii=False, indent=2, default=str).encode("utf-8")
    stream = io.BytesIO(payload)
    stream.name = f"HMAX_backup_{yemen_today()}.json"
    try:
        BOT.send_document(chat_id, stream, caption="🗄️ نسخة احتياطية من بيانات HMAX.")
        audit("backup_export", chat_id)
    finally:
        stream.close()


def install(bot, db, data, admin_id):
    global BOT, DB, DATA, ADMIN_ID
    BOT = bot
    DB = db
    DATA = data or {}
    ADMIN_ID = int(admin_id)
    print("✅ HMAX Enhancement Layer loaded.")

    @bot.message_handler(commands=["maintenance"])
    def maintenance_cmd(message):
        if not is_admin(message.chat.id):
            return
        parts = (message.text or "").split(maxsplit=2)
        if len(parts) < 2 or parts[1].lower() not in {"on", "off"}:
            bot.send_message(message.chat.id, "⚙️ الاستخدام: /maintenance on أو /maintenance off")
            return
        enabled = parts[1].lower() == "on"
        custom = parts[2].strip() if len(parts) > 2 else None
        ok = set_maintenance(enabled, custom, message.chat.id)
        bot.send_message(message.chat.id, "✅ تم تحديث وضع الصيانة." if ok else "❌ تعذر تحديث وضع الصيانة.")

    @bot.message_handler(commands=["stats"])
    def stats_cmd(message):
        if is_admin(message.chat.id):
            audit("view_stats", message.chat.id)
            bot.send_message(message.chat.id, format_admin_stats(), parse_mode="HTML")

    @bot.message_handler(commands=["audit"])
    def audit_cmd(message):
        if not is_admin(message.chat.id) or not DB:
            return
        lines = ["🧾 <b>آخر سجلات الإدارة</b>", ""]
        try:
            docs = DB.collection("admin_audit_logs").order_by(
                "timestamp", direction=firestore.Query.DESCENDING
            ).limit(25).stream()
            for doc in docs:
                row = doc.to_dict() or {}
                lines.append(
                    f"▫️ {row.get('timestamp', '')} — <b>{row.get('action', '')}</b> — {row.get('actor_id', '')}"
                )
        except Exception as exc:
            lines.append(f"❌ {exc}")
        bot.send_message(message.chat.id, "\\n".join(lines), parse_mode="HTML")

    @bot.message_handler(commands=["requests"])
    def requests_cmd(message):
        if is_admin(message.chat.id):
            audit("view_requests", message.chat.id)
            send_requests_admin(message.chat.id)

    @bot.message_handler(commands=["search"])
    def search_cmd(message):
        if not allow_user(message.chat.id, "search"):
            return
        parts = (message.text or "").split(maxsplit=1)
        if len(parts) < 2:
            bot.send_message(message.chat.id, "🔎 الاستخدام: /search chimera")
            return
        send_search(message.chat.id, parts[1])

    @bot.message_handler(commands=["favorites"])
    def favorites_cmd(message):
        if allow_user(message.chat.id):
            send_favorites(message.chat.id)

    @bot.message_handler(commands=["notify"])
    def notify_cmd(message):
        if not allow_user(message.chat.id):
            return
        current = notification_enabled(message.chat.id)
        new_value = not current
        set_notification_pref(message.chat.id, new_value)
        bot.send_message(
            message.chat.id,
            "🔔 الإشعارات مفعّلة ✅" if new_value else "🔕 الإشعارات متوقفة ✅",
        )

    @bot.message_handler(commands=["coupon"])
    def coupon_cmd(message):
        if not allow_user(message.chat.id, "coupon"):
            return
        args = (message.text or "").split()
        if len(args) >= 2 and args[1].lower() == "create":
            if not is_admin(message.chat.id):
                return
            if len(args) < 4:
                bot.send_message(message.chat.id, "⚙️ مثال: /coupon create HMAX100 100 50 30")
                return
            max_uses = int(args[4]) if len(args) >= 5 and args[4].isdigit() else 0
            days = int(args[5]) if len(args) >= 6 and args[5].isdigit() else 0
            ok, msg = coupon_create(message.chat.id, args[2], int(args[3]), max_uses, days)
            bot.send_message(message.chat.id, msg, parse_mode="HTML")
            return
        code = args[1] if len(args) > 1 else ""
        _, msg = coupon_redeem(message.chat.id, code)
        bot.send_message(message.chat.id, msg)

    @bot.message_handler(commands=["vip"])
    def vip_cmd(message):
        args = (message.text or "").split()
        if len(args) >= 3 and args[1].lower() == "grant" and is_admin(message.chat.id):
            try:
                target = int(args[2])
                days = max(1, int(args[3])) if len(args) > 3 else 30
                until = now_utc() + datetime.timedelta(days=days)
                DB.collection("users").document(str(target)).set({
                    "vip_until": until.isoformat(),
                    "vip_granted_by": int(message.chat.id),
                }, merge=True)
                audit("vip_grant", message.chat.id, target, f"{days} days")
                bot.send_message(message.chat.id, f"✅ تم منح VIP للمستخدم {target} حتى {until.date()}.")
            except Exception as exc:
                bot.send_message(message.chat.id, f"❌ {exc}")
            return
        vip, until = user_vip(message.chat.id)
        if vip:
            extra = f" حتى {until.date()}" if until else " تلقائياً بسبب الرتبة"
            bot.send_message(message.chat.id, f"👑 حالتك: VIP{extra}\\n🎁 أولوية الدعم والمزايا القادمة.")
        else:
            bot.send_message(message.chat.id, "⭐ حالتك: عضو عادي. تصل إلى VIP تلقائياً عند 1200 نقطة.")

    @bot.message_handler(commands=["streak"])
    def streak_cmd(message):
        if not DB:
            return
        try:
            data = DB.collection("users").document(uid(message.chat.id)).get().to_dict() or {}
            streak = int(data.get("daily_streak", 0) or 0)
            last_reward = int(data.get("last_streak_reward", 0) or 0)
            bot.send_message(message.chat.id, f"🔥 سلسلة الزيارات: {streak} يوم\\n🎁 آخر محطة مكافأة: {last_reward}")
        except Exception:
            pass

    @bot.message_handler(commands=["backup"])
    def backup_cmd(message):
        if is_admin(message.chat.id):
            admin_backup(message.chat.id)

    @bot.callback_query_handler(func=lambda call: str(call.data).startswith("enh_fav_"))
    def favorite_callback(call):
        try:
            raw = decode_key(str(call.data)[len("enh_fav_"):])
            if "|" in raw:
                category, key = raw.split("|", 1)
            else:
                category, key = raw.split(":", 1)
            changed = toggle_favorite(call.from_user.id, category, key)
            bot.answer_callback_query(
                call.id,
                "⭐ تمت الإضافة للمفضلة." if changed else "🗑️ تمت الإزالة من المفضلة.",
            )
        except Exception:
            bot.answer_callback_query(call.id, "❌ تعذر تحديث المفضلة.", show_alert=True)

    @bot.callback_query_handler(func=lambda call: str(call.data).startswith("enh_req_"))
    def request_status_callback(call):
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "❌ للإدارة فقط.", show_alert=True)
            return
        try:
            parts = str(call.data).split("_", 3)
            request_id = parts[2]
            status = parts[3]
            DB.collection("user_requests").document(request_id).set({
                "status": status,
                "status_updated_at": now_utc().isoformat(),
                "status_updated_by": int(call.from_user.id),
            }, merge=True)
            audit("request_status", call.from_user.id, details=f"{request_id}: {status}")
            bot.answer_callback_query(call.id, f"✅ {status}")
        except Exception as exc:
            bot.answer_callback_query(call.id, f"❌ {exc}", show_alert=True)
