"""HMAX DUMP Advanced Features — Phase 1.

Features:
- Recently viewed cards (per user)
- Favorites (per user)
- Search across cards
- View counter per card
- Stats per tool
- Library health (admin only)
"""

import hashlib
import threading
import time

from telebot import types
from firebase_admin import firestore


BOT = None
DB = None
ADMIN_ID = 0
_DATA = {}

_VIEW_THROTTLE = {}       # {uid: {cb: last_ts}}
_VIEW_LOCK = threading.RLock()
_FAV_MAP = {}             # {short_token: card_cb}
_FAV_MAP_LOCK = threading.RLock()


def _uid(u):
    return str(int(u))


def _user_ref(user_id):
    return DB.collection("users").document(_uid(user_id))


# ====================== FAVORITES ======================

def toggle_favorite(user_id, card_cb, card_label):
    if not DB:
        return None, "Firebase غير متصل"
    try:
        ref = _user_ref(user_id)
        txn = DB.transaction()
        added_flag = {"v": False}

        @firestore.transactional
        def apply(t):
            doc = ref.get(transaction=t)
            data = doc.to_dict() or {}
            favs = list(data.get("dump_favorites", []) or [])
            favs = [f for f in favs if isinstance(f, dict)]
            tokens = [f.get("cb") for f in favs]
            if card_cb in tokens:
                favs = [f for f in favs if f.get("cb") != card_cb]
            else:
                favs.append({"cb": card_cb, "label": card_label, "at": time.time()})
                if len(favs) > 50:
                    favs = favs[-50:]
                added_flag["v"] = True
            t.set(ref, {"dump_favorites": favs}, merge=True)

        apply(txn)
        return added_flag["v"], None
    except Exception as e:
        return None, str(e)


def get_favorites(user_id):
    if not DB:
        return []
    try:
        doc = _user_ref(user_id).get()
        return list((doc.to_dict() or {}).get("dump_favorites", []) or [])
    except Exception:
        return []


def is_favorite(user_id, card_cb):
    for f in get_favorites(user_id):
        if isinstance(f, dict) and f.get("cb") == card_cb:
            return True
    return False


# ====================== RECENT ======================

def track_view(user_id, card_cb, card_label):
    if not DB:
        return
    try:
        now = time.time()
        with _VIEW_LOCK:
            user_map = _VIEW_THROTTLE.setdefault(int(user_id), {})
            if now - user_map.get(card_cb, 0) < 300:
                return
            user_map[card_cb] = now

        ref = _user_ref(user_id)
        txn = DB.transaction()

        @firestore.transactional
        def apply(t):
            doc = ref.get(transaction=t)
            data = doc.to_dict() or {}
            recent = list(data.get("dump_recent", []) or [])
            recent = [r for r in recent if isinstance(r, dict) and r.get("cb") != card_cb]
            recent.insert(0, {"cb": card_cb, "label": card_label, "at": now})
            recent = recent[:10]
            t.set(ref, {"dump_recent": recent}, merge=True)

        apply(txn)
        DB.collection("dump_stats").document(card_cb).set(
            {"views": firestore.Increment(1)}, merge=True
        )
    except Exception as e:
        print(f"⚠️ track_view: {e}")


def get_recent(user_id, limit=5):
    if not DB:
        return []
    try:
        doc = _user_ref(user_id).get()
        return list((doc.to_dict() or {}).get("dump_recent", []) or [])[:limit]
    except Exception:
        return []


def get_view_count(card_cb):
    if not DB:
        return 0
    try:
        doc = DB.collection("dump_stats").document(card_cb).get()
        return int((doc.to_dict() or {}).get("views", 0))
    except Exception:
        return 0


# ====================== SEARCH ======================

def search_cards(query, limit=20):
    if not query or len(query.strip()) < 2:
        return []
    q = query.strip().lower()
    try:
        from hmax_dump_tools import DUMP_CARDS, DUMP_TOOLS
    except Exception:
        return []

    results = []
    for tool_key, cards in DUMP_CARDS.items():
        tool = DUMP_TOOLS.get(tool_key, {})
        icon = tool.get("icon", "🛠️")
        for label, cb in cards:
            if q in label.lower() or q in cb.lower():
                results.append({
                    "label": label, "cb": cb,
                    "icon": icon, "tool_key": tool_key,
                })
                if len(results) >= limit:
                    return results
    return results


# ====================== STATS ======================

def get_tool_stats(tool_key):
    try:
        from hmax_dump_tools import DUMP_CARDS
        cards = DUMP_CARDS.get(tool_key, [])
        return {"cards": len(cards), "views": sum(get_view_count(cb) for _, cb in cards)}
    except Exception:
        return {"cards": 0, "views": 0}


def get_library_stats():
    try:
        from hmax_dump_tools import DUMP_CARDS
        tools = len(DUMP_CARDS)
        cards = sum(len(v) for v in DUMP_CARDS.values())
        views = 0
        if DB:
            try:
                for doc in DB.collection("dump_stats").stream():
                    views += int((doc.to_dict() or {}).get("views", 0))
            except Exception:
                pass
        return {"tools": tools, "cards": cards, "views": views}
    except Exception:
        return {"tools": 0, "cards": 0, "views": 0}


# ====================== HELPERS ======================

def _find_tool_for_card(card_cb):
    try:
        from hmax_dump_tools import DUMP_CARDS
        for tk, cards in DUMP_CARDS.items():
            for _, cb in cards:
                if cb == card_cb:
                    return tk
    except Exception:
        pass
    return None


def _register_fav_token(card_cb):
    h = hashlib.md5(card_cb.encode("utf-8")).hexdigest()[:20]
    with _FAV_MAP_LOCK:
        _FAV_MAP[h] = card_cb
    return h


def _resolve_fav_token(token):
    with _FAV_MAP_LOCK:
        return _FAV_MAP.get(token)


def _register_card_for_nav(tool_key, original_cb):
    try:
        from hmax_dump_tools import _register_card
        return _register_card(tool_key, original_cb)
    except Exception:
        return None


def _render(call, text, markup):
    try:
        BOT.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            reply_markup=markup, parse_mode="Markdown",
            disable_web_page_preview=True,
        )
        return
    except Exception as e:
        print(f"⚠️ adv render edit: {e}")
    try:
        BOT.delete_message(call.message.chat.id, call.message.message_id)
    except Exception:
        pass
    try:
        BOT.send_message(
            call.message.chat.id, text, reply_markup=markup,
            parse_mode="Markdown", disable_web_page_preview=True,
        )
    except Exception as e:
        print(f"⚠️ adv render send: {e}")


def _back_markup(lang="ar"):
    label = "🔙 رجوع" if lang == "ar" else "🔙 Back" if lang == "en" else "🔙 Retour"
    mk = types.InlineKeyboardMarkup(row_width=1)
    mk.add(types.InlineKeyboardButton(label, callback_data="dump_tools_section"))
    return mk


# ====================== UI ======================

def show_recent(call, lang="ar"):
    user_id = call.from_user.id
    recent = get_recent(user_id, 5)

    if not recent:
        text = (
            "🕐 **آخر ما زرته**\n\nلا يوجد سجل بعد."
            if lang == "ar" else
            "🕐 **Recently viewed**\n\nNo history yet."
            if lang == "en" else
            "🕐 **Consultés récemment**\n\nAucun historique."
        )
        _render(call, text, _back_markup(lang))
        return

    mk = types.InlineKeyboardMarkup(row_width=1)
    for item in recent:
        if not isinstance(item, dict):
            continue
        cb = item.get("cb", "")
        label = item.get("label", "")[:55]
        tk = _find_tool_for_card(cb)
        if not tk:
            continue
        sk = _register_card_for_nav(tk, cb)
        if sk:
            mk.add(types.InlineKeyboardButton(label, callback_data=f"dumptoolcard_{sk}"))
    mk.add(types.InlineKeyboardButton(
        "🔙 رجوع" if lang == "ar" else "🔙 Back" if lang == "en" else "🔙 Retour",
        callback_data="dump_tools_section",
    ))

    text = (
        "🕐 **آخر ما زرته**\n\nاختر بطاقة:" if lang == "ar"
        else "🕐 **Recently viewed**\n\nChoose a card:" if lang == "en"
        else "🕐 **Consultés récemment**\n\nChoisissez une fiche :"
    )
    _render(call, text, mk)


def show_favorites(call, lang="ar"):
    user_id = call.from_user.id
    favs = get_favorites(user_id)

    if not favs:
        text = (
            "⭐ **المفضلة**\n\nلا توجد بطاقات محفوظة." if lang == "ar"
            else "⭐ **Favorites**\n\nNo saved cards." if lang == "en"
            else "⭐ **Favoris**\n\nAucune fiche enregistrée."
        )
        _render(call, text, _back_markup(lang))
        return

    mk = types.InlineKeyboardMarkup(row_width=1)
    for item in favs[:30]:
        if not isinstance(item, dict):
            continue
        cb = item.get("cb", "")
        label = item.get("label", "")[:55]
        tk = _find_tool_for_card(cb)
        if not tk:
            continue
        sk = _register_card_for_nav(tk, cb)
        if sk:
            mk.add(types.InlineKeyboardButton(f"⭐ {label}", callback_data=f"dumptoolcard_{sk}"))
    mk.add(types.InlineKeyboardButton(
        "🔙 رجوع" if lang == "ar" else "🔙 Back" if lang == "en" else "🔙 Retour",
        callback_data="dump_tools_section",
    ))

    text = (
        "⭐ **المفضلة**\n\nبطاقاتك المحفوظة:" if lang == "ar"
        else "⭐ **Favorites**\n\nYour saved cards:" if lang == "en"
        else "⭐ **Favoris**\n\nVos fiches :"
    )
    _render(call, text, mk)


def show_search_results(call, query, lang="ar"):
    results = search_cards(query)

    if not results:
        text = (
            f"🔍 **بحث:** {query}\n\nلا توجد نتائج." if lang == "ar"
            else f"🔍 **Search:** {query}\n\nNo results." if lang == "en"
            else f"🔍 **Recherche :** {query}\n\nAucun résultat."
        )
        _render(call, text, _back_markup(lang))
        return

    mk = types.InlineKeyboardMarkup(row_width=1)
    for r in results:
        sk = _register_card_for_nav(r["tool_key"], r["cb"])
        if sk:
            label = f"{r['icon']} {r['label']}"[:60]
            mk.add(types.InlineKeyboardButton(label, callback_data=f"dumptoolcard_{sk}"))
    mk.add(types.InlineKeyboardButton(
        "🔙 رجوع" if lang == "ar" else "🔙 Back" if lang == "en" else "🔙 Retour",
        callback_data="dump_tools_section",
    ))

    text = (
        f"🔍 **نتائج البحث عن:** `{query}`  ({len(results)})" if lang == "ar"
        else f"🔍 **Results for:** `{query}`  ({len(results)})" if lang == "en"
        else f"🔍 **Résultats pour :** `{query}`  ({len(results)})"
    )
    _render(call, text, mk)


def show_tool_stats(call, tool_key, lang="ar"):
    try:
        from hmax_dump_tools import DUMP_TOOLS
    except Exception:
        DUMP_TOOLS = {}
    tool = DUMP_TOOLS.get(tool_key, {})
    stats = get_tool_stats(tool_key)
    name = tool.get("name_ar" if lang == "ar" else "name_en" if lang == "en" else "name_fr", tool_key)

    text = (
        f"📊 **إحصائيات الأداة**\n━━━━━━━━━━━━━━━━━━\n\n"
        f"{tool.get('icon','🛠️')} **{name}**\n\n"
        f"📱 عدد البطاقات: **{stats['cards']}**\n"
        f"👁️ إجمالي المشاهدات: **{stats['views']}**"
    ) if lang == "ar" else (
        f"📊 **Tool stats**\n━━━━━━━━━━━━━━━━━━\n\n"
        f"{tool.get('icon','🛠️')} **{name}**\n\n"
        f"📱 Cards: **{stats['cards']}**\n"
        f"👁️ Views: **{stats['views']}**"
    ) if lang == "en" else (
        f"📊 **Stats outil**\n━━━━━━━━━━━━━━━━━━\n\n"
        f"{tool.get('icon','🛠️')} **{name}**\n\n"
        f"📱 Fiches : **{stats['cards']}**\n"
        f"👁️ Vues : **{stats['views']}**"
    )

    mk = types.InlineKeyboardMarkup(row_width=1)
    mk.add(types.InlineKeyboardButton(
        "🔙 رجوع" if lang == "ar" else "🔙 Back" if lang == "en" else "🔙 Retour",
        callback_data=f"dumptool_{tool_key}",
    ))
    _render(call, text, mk)


def show_library_health(call, lang="ar"):
    stats = get_library_stats()
    text = (
        f"🏥 **فحص صحة المكتبة**\n━━━━━━━━━━━━━━━━━━\n\n"
        f"🛠️ عدد الأدوات: **{stats['tools']}**\n"
        f"📱 عدد البطاقات: **{stats['cards']}**\n"
        f"👁️ إجمالي المشاهدات: **{stats['views']}**"
    ) if lang == "ar" else (
        f"🏥 **Library health**\n━━━━━━━━━━━━━━━━━━\n\n"
        f"🛠️ Tools: **{stats['tools']}**\n"
        f"📱 Cards: **{stats['cards']}**\n"
        f"👁️ Views: **{stats['views']}**"
    )
    _render(call, text, _back_markup(lang))


# ====================== BOT WRAPPERS ======================

# Index of the chat id argument for each patched method, when it is passed
# positionally rather than as a keyword.
_CHAT_ID_ARG = {"send_photo": 0, "send_message": 0, "edit_message_text": 1}


def _already_favourited(markup):
    for row in getattr(markup, "keyboard", []) or []:
        for btn in row:
            if str(getattr(btn, "callback_data", "") or "").startswith("dumpfav_"):
                return True
    return False


def _augment(method_name):
    """Track the view and add the ⭐ button to every DUMP card.

    Cards reach the user through three different calls — the photo, a follow-up
    text message, or an in-place edit — so all three are wrapped. Without the
    ``send_message`` hook the cards that reply with a text message never got
    their favourite button.
    """
    bot = BOT
    original = getattr(bot, method_name)
    chat_id_pos = _CHAT_ID_ARG.get(method_name, 0)

    def wrapped(*args, **kwargs):
        try:
            from hmax_dump_tools import _CONTEXT as _dt_ctx
            tool_key = getattr(_dt_ctx, "tool_key", None)
            original_cb = getattr(_dt_ctx, "original_cb", None)
            card_label = getattr(_dt_ctx, "card_label", None)

            if tool_key and original_cb:
                chat_id = kwargs.get(
                    "chat_id",
                    args[chat_id_pos] if len(args) > chat_id_pos else None,
                )
                if chat_id:
                    track_view(chat_id, original_cb, card_label or "")
                mk = kwargs.get("reply_markup")
                if mk is not None and hasattr(mk, "keyboard") and not _already_favourited(mk):
                    from hmax_i18n import get_language
                    lang = get_language(chat_id) if chat_id else "ar"
                    fav_label = (
                        "⭐ حفظ" if lang == "ar"
                        else "⭐ Save" if lang == "en"
                        else "⭐ Enregistrer"
                    )
                    fav_token = _register_fav_token(original_cb)
                    try:
                        mk.row(types.InlineKeyboardButton(
                            fav_label, callback_data=f"dumpfav_{fav_token}"
                        ))
                    except Exception:
                        pass
        except Exception as e:
            print(f"⚠️ adv {method_name}: {e}")
        return original(*args, **kwargs)

    return wrapped


# ====================== INSTALL ======================

def install(bot, db, admin_id):
    global BOT, DB, ADMIN_ID
    BOT = bot
    DB = db
    ADMIN_ID = int(admin_id)

    for _method in ("send_photo", "send_message", "edit_message_text"):
        setattr(bot, _method, _augment(_method))

    print("✅ HMAX DUMP Advanced loaded (Phase 1).")