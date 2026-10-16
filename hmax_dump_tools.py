"""HMAX DUMP Source Tools — فهرس بطاقات الدامب حسب أداة السحب."""

import hashlib
import re
import threading

from telebot import types

BOT = None
DB = None
DATA = {}
ADMIN_ID = 0

_CONTEXT = threading.local()
_CARD_REGISTRY = {}


DUMP_TOOLS = {
    "easy_jtag": {
        "category": "jtag", "icon": "🔌",
        "name_ar": "Easy JTAG Plus", "name_en": "Easy JTAG Plus", "name_fr": "Easy JTAG Plus",
        "desc_ar": "أداة احترافية متخصصة في سحب وكتابة الدامب عبر منفذ JTAG و EMMC. من أقوى الأدوات في صيانة الذاكرة والفلاشات النادرة.",
        "desc_en": "Professional tool specialized in pulling and writing dumps via JTAG and EMMC.",
        "desc_fr": "Outil professionnel spécialisé dans l'extraction et l'écriture de dumps via JTAG et EMMC.",
        "supported_ar": "eMMC • UFS • JTAG • موديلات متعددة",
        "supported_en": "eMMC • UFS • JTAG • Many models",
        "supported_fr": "eMMC • UFS • JTAG • Plusieurs modèles",
        "url": "https://easy-jtag.com/",
        "btn_ar": "⬇️ تحميل Easy JTAG Plus", "btn_en": "⬇️ Download Easy JTAG Plus", "btn_fr": "⬇️ Télécharger Easy JTAG Plus",
    },
    "f64_ultra": {
        "category": "jtag", "icon": "⚡",
        "name_ar": "F64 ULTRA", "name_en": "F64 ULTRA", "name_fr": "F64 ULTRA",
        "desc_ar": "أداة F64 ULTRA الحديثة القوية لسحب الدامب بسرعة عالية عبر JTAG و EMMC. تُستخدم في الموديلات الحديثة.",
        "desc_en": "Modern and powerful F64 ULTRA tool for fast JTAG and EMMC dump extraction.",
        "desc_fr": "Outil moderne et puissant F64 ULTRA pour l'extraction rapide de dumps JTAG et EMMC.",
        "supported_ar": "Samsung • Redmi • Vivo • OPPO • Huawei",
        "supported_en": "Samsung • Redmi • Vivo • OPPO • Huawei",
        "supported_fr": "Samsung • Redmi • Vivo • OPPO • Huawei",
        "url": "https://flash64.com/",
        "btn_ar": "⬇️ تحميل F64 ULTRA", "btn_en": "⬇️ Download F64 ULTRA", "btn_fr": "⬇️ Télécharger F64 ULTRA",
    },
    "ufi": {
        "category": "jtag", "icon": "🚀",
        "name_ar": "UFI Box", "name_en": "UFI Box", "name_fr": "UFI Box",
        "desc_ar": "بوكس UFI الأندرويد الاحترافي، من أفضل الأدوات في سحب الدامب على معالجات Qualcomm و MediaTek عبر JTAG و EMMC.",
        "desc_en": "UFI Android box for extracting dumps on Qualcomm and MediaTek chips via JTAG and EMMC.",
        "desc_fr": "Box UFI Android pour extraire des dumps sur les puces Qualcomm et MediaTek via JTAG et EMMC.",
        "supported_ar": "Qualcomm • MediaTek",
        "supported_en": "Qualcomm • MediaTek",
        "supported_fr": "Qualcomm • MediaTek",
        "url": "https://ufibox.com/download/",
        "btn_ar": "⬇️ تحميل UFI Box", "btn_en": "⬇️ Download UFI Box", "btn_fr": "⬇️ Télécharger UFI Box",
    },
    "unlocktool": {
        "category": "normal", "icon": "🔓",
        "name_ar": "UnlockTool", "name_en": "UnlockTool", "name_fr": "UnlockTool",
        "desc_ar": "أداة رسمية شاملة لعمليات التفليش، فك الشفرات، وتخطي الحمايات لمئات الموديلات.",
        "desc_en": "Official all-in-one tool for flashing, unlocking and bypassing security.",
        "desc_fr": "Outil officiel tout-en-un pour le flashage et le déblocage.",
        "supported_ar": "Samsung • Xiaomi • Huawei • OPPO • Realme • Vivo",
        "supported_en": "Samsung • Xiaomi • Huawei • OPPO • Realme • Vivo",
        "supported_fr": "Samsung • Xiaomi • Huawei • OPPO • Realme • Vivo",
        "url": "https://file.unlocktool.net/",
        "btn_ar": "⬇️ تحميل UnlockTool", "btn_en": "⬇️ Download UnlockTool", "btn_fr": "⬇️ Télécharger UnlockTool",
    },
    "cm2": {
        "category": "normal", "icon": "📦",
        "name_ar": "Infinity CM2", "name_en": "Infinity CM2", "name_fr": "Infinity CM2",
        "desc_ar": "أداة Infinity CM2 قوية جداً في معالجات MediaTek و Spreadtrum و Qualcomm.",
        "desc_en": "Infinity CM2 is very strong with MediaTek, Spreadtrum and Qualcomm chips.",
        "desc_fr": "Infinity CM2 est très puissant avec les puces MediaTek, Spreadtrum et Qualcomm.",
        "supported_ar": "MediaTek • Unisoc/SPD • Qualcomm",
        "supported_en": "MediaTek • Unisoc/SPD • Qualcomm",
        "supported_fr": "MediaTek • Unisoc/SPD • Qualcomm",
        "url": "https://infinity-box.com/download/",
        "btn_ar": "⬇️ تحميل Infinity CM2", "btn_en": "⬇️ Download Infinity CM2", "btn_fr": "⬇️ Télécharger Infinity CM2",
    },
    "pandora": {
        "category": "normal", "icon": "🐾",
        "name_ar": "Pandora Tool", "name_en": "Pandora Tool", "name_fr": "Pandora Tool",
        "desc_ar": "أداة Pandora الشهيرة لسحب وكتابة دامب MediaTek و Spreadtrum.",
        "desc_en": "The well-known Pandora tool for MediaTek and Spreadtrum dumps.",
        "desc_fr": "L'outil Pandora pour les dumps MediaTek et Spreadtrum.",
        "supported_ar": "MediaTek • Spreadtrum/Unisoc",
        "supported_en": "MediaTek • Spreadtrum/Unisoc",
        "supported_fr": "MediaTek • Spreadtrum/Unisoc",
        "url": "https://downloads1.z3x.dev/getLatestVersion.php",
        "btn_ar": "⬇️ تحميل Pandora Tool", "btn_en": "⬇️ Download Pandora Tool", "btn_fr": "⬇️ Télécharger Pandora Tool",
    },
    "amt": {
        "category": "normal", "icon": "🛠️",
        "name_ar": "AMT Tool", "name_en": "AMT Tool", "name_fr": "AMT Tool",
        "desc_ar": "أداة AMT (Android Multi Tool) لعمليات التفليش والقراءة على معالجات Unisoc و MediaTek.",
        "desc_en": "AMT for flashing and reading on Unisoc and MediaTek chips.",
        "desc_fr": "AMT pour le flashage et la lecture sur les puces Unisoc et MediaTek.",
        "supported_ar": "Unisoc • MediaTek",
        "supported_en": "Unisoc • MediaTek",
        "supported_fr": "Unisoc • MediaTek",
        "url": "https://androidmultitool.com/download/",
        "btn_ar": "⬇️ تحميل AMT Tool", "btn_en": "⬇️ Download AMT Tool", "btn_fr": "⬇️ Télécharger AMT Tool",
    },
    "miracle": {
        "category": "normal", "icon": "✨",
        "name_ar": "Miracle Box", "name_en": "Miracle Box", "name_fr": "Miracle Box",
        "desc_ar": "بوكس Miracle Thunder الشهير لعمليات التفليش والفك.",
        "desc_en": "Famous Miracle Thunder box for flashing and unlocking.",
        "desc_fr": "Célèbre box Miracle Thunder pour le flashage et le déblocage.",
        "supported_ar": "MediaTek • SPD • Qualcomm",
        "supported_en": "MediaTek • SPD • Qualcomm",
        "supported_fr": "MediaTek • SPD • Qualcomm",
        "url": "https://miraclebox.com/download/",
        "btn_ar": "⬇️ تحميل Miracle Box", "btn_en": "⬇️ Download Miracle Box", "btn_fr": "⬇️ Télécharger Miracle Box",
    },
}


DUMP_CARDS = {
    "easy_jtag": [
        ("📱 REDMI 9C M2006C3MG",            "dump_model_redmi_9c_m2006c3mg"),
        ("📱 Redmi Note 14 5G Beryl XML",     "dump_model_redmi_note14_5g_beryl_xml"),
        ("📱 OPPO A31 CPH2015 128GB",         "dump_model_oppo_a31_cph2015_128gb"),
        ("📱 OPPO A57 CPH2387",               "dump_model_oppo_a57_cph2387"),
        ("📱 Realme C35 XML 128GB",           "dump_model_realme_c35_rmx3511_xml"),
        ("📱 SAMSUNG A12 SM-A125F",           "dump_a125f"),
        ("📱 VIVO Y03 4GB",                   "dump_model_vivo_y03_dump_4gb"),
        ("📱 VIVO Y04 V2430 10GB",            "dump_model_vivo_y04_v2430_latest"),
        ("📱 VIVO Y04 V2430 (2) OSv15",       "dump_model_vivo_y04_v2430_2_osv15_easyjtag"),
        ("📱 VIVO Y27 & Y36 5G V2248",        "dump_model_vivo_y27_y36_5g_v2248_pd2279f_ex_a_15_2_10_2_w20"),
        ("📱 HUAWEI Y7A PPA-LX2",             "dump_model_huawei_y7a_ppa_lx2"),
    ],
    "f64_ultra": [
        ("📱 REDMI 10A 220233L2G",            "dump_model_redmi_10a_220233l2g"),
        ("📱 REDMI A3 C61",                   "dump_model_redmi_a3_c61"),
        ("📱 REDMI 15C / POCO C85",           "dump_model_redmi_15c_poco_c85"),
        ("📱 OPPO RENO 12F 4G CPH2687",       "dump_model_oppo_reno_12f_4g_cph2687"),
        ("📱 OPPO A6 PRO 5G CPH2781",         "dump_model_oppo_a6_pro_5g_cph2781"),
        ("📱 Realme 10 Pro 5G RMX3661",       "dump_model_realme_10_pro_5g_rmx3661"),
        ("📱 Realme Note 60X RMX3938",        "dump_model_realme_note_60x_rmx3938"),
        ("📱 SAMSUNG A25 5G A256E",           "dump_a256e"),
        ("📱 VIVO Y21D PD2510F",              "dump_model_vivo_y21d_pd2510f"),
        ("📱 VIVO Y03T PD2360F",              "dump_model_vivo_y03t_pd2360f"),
        ("📱 VIVO Y18 PD2327F",               "dump_model_vivo_y18_pd2327f"),
        ("📱 VIVO Y22S PD2228F",              "dump_model_vivo_y22s_pd2228f"),
        ("📱 HONOR X7a RKY-LX2 2GB",          "dump_model_honor_x7a_rky_lx2_2gb"),
        ("📱 HONOR X9c",                      "dump_model_honor_x9c_full_dump"),
        ("📱 HONOR 400 ABR-N03",              "dump_model_honor_400_abr_n03_osv15"),
        ("📱 POCO C75 / Redmi 14C / 17C",     "dump_model_lake_poco_c75_14c_17c"),
        ("📱 POCO C65 256GB",                 "dump_model_poco_c65_256gb"),
    ],
    "ufi": [
        ("📱 HONOR X7a RKY-LX2 (UFI)",        "dump_model_honor_x7a_rky_lx2"),
    ],
    "unlocktool": [
        ("📱 ITEL P37 P651W",                 "dump_model_itel_p37_p651w"),
        ("📱 ITEL A06 A669W",                 "dump_model_itel_a06_a669w_full_dump_unlocktool"),
        ("📱 Infinix Smart 5 X657C",          "dump_model_infinix_x657c_smart5"),
        ("📱 Infinix Smart 20 X6840B",        "dump_model_x6840b_full_dump"),
        ("📱 Vivo Y15s V2120",                "dump_model_vivo_y15s_v2120_pd2140f_full_dump_unlocktool"),
        ("📱 WIKO T10",                       "dump_model_wiko_t10_full_dump_unlocktool"),
        ("📱 VILLAON V20",                    "dump_model_villaon_v20_full_dump_unlocktool"),
        ("📱 M-HORSE HOT 40 Pro V03",         "dump_model_mhorse_hot40pro_v03"),
        ("📱 M-HORSE HOT 30 V05",             "dump_model_m_horse_hot_30_full_dump_unlocktool"),
        ("📱 M-HORSE SPARK 10 Pro (3v)",      "dump_model_m_horse_spark_10_pro_full_dump_unlocktool"),
        ("📱 HISORL T901",                    "dump_model_hisorl_t901_full"),
        ("📱 Honor X7B CLK-LX2",              "dump_model_honor_x7b_clk_lx2"),
        ("📱 Samsung Tab A9 X110",            "dump_model_tab_a9_sm_x110"),
        ("📱 AllCall Hero 60 Max",            "dump_model_allcall_hero_60_max_full_dump_unlocktool"),
        ("📱 OPPO A54 CPH2239 Dead Boot",     "dump_model_oppo_a54_cph2239_dead_boot"),
        ("📱 Itel L6503 Vision 2 (3 tools)",  "dump_model_itel_l6503_vision2"),
    ],
    "pandora": [
        ("📱 INFINIX NOTE 30 5G",             "dump_model_infinix_note_30_5g_x6711_v600"),
        ("📱 Moto E13 XT2345-4",              "dump_model_moto_e13_xt2345_4_pandora_full_dump"),
        ("📱 ITEL S23 S665LN",                "dump_model_itel_s23_s665ln"),
        ("📱 ITEL A49 A661L (A58 Pro)",       "dump_model_itel_a49_a661l"),
        ("📱 M-HORSE POP 8",                  "dump_model_m_horse_pop8"),
        ("📱 Redmi 13C Gale",                 "dump_model_redmi_13c_gale"),
        ("📱 Realme C35 A.55",                "dump_model_realme_c35_rmx3511_full_a55"),
        ("📱 Realme C71 RMX5303",             "dump_model_realme_c71_rmx5303"),
        ("📱 Realme C15 RMX2180",             "dump_model_realme_c15_rmx2180"),
        ("📱 Realme Note 50 RMX3834",         "dump_model_realme_note_50_rmx3834_a89"),
        ("📱 Realme C67 COPY",                "dump_model_realme_c67_copy_full_dump_pandora"),
        ("📱 OPPO A55 CPH2325",               "dump_model_oppo_a55_cph2325_f71"),
        ("📱 OPPO CPH1933 A5 2020",           "dump_model_oppo_cph1933_a5_2020_full_dump_pandora"),
        ("📱 Nokia C12 TA-1583 (Pandora)",    "dump_nokia_c12_ta1583_pandora"),
        ("📱 Nokia C10 TA-1342",              "dump_model_nokia_c10_ta_1342"),
        ("📱 Nokia 5.3 TA-1234",              "dump_model_nokia_5_3_ta_1234"),
        ("📱 iPhone 16 Pro Max Copy",         "dump_model_iphone16_pro_max_copy_mt6735"),
        ("📱 S26 Ultra Copy SAMBA65S",        "dump_model_s26_ultra_copy_samba65s"),
        ("📱 AllCall Magic 60",               "dump_model_allcall_magic_60_exclusive"),
        ("📱 KXD A07 Android 13",             "dump_kxd_a07_a13"),
        ("📱 KXD A07 Android 12",             "dump_kxd_a07_a12"),
        ("📱 LAVA Iris 59 LE9930",            "dump_model_lava_iris_59"),
        ("📱 WALTON NEXG N72",                "dump_model_walton_nexg_n72"),
        ("📱 Itel L6503 Vision 2 (3 tools)",  "dump_model_itel_l6503_vision2"),
    ],
    "cm2": [
        ("📱 Benco V60",                      "dump_model_benco_v60_full"),
        ("📱 Benco S1 Pro AE9260 (Dual)",     "dump_model_benco_s1_pro_ae9260_dual"),
        ("📱 M-Horse C55 (Dual)",             "dump_model_mhorse_c55_dual"),
        ("📱 YTAB ULTRA 35",                  "dump_model_ytab_ultra_35_full_dump_cm2"),
        ("📱 Oteeto TAB 15",                  "dump_model_the_oteeto_tab_15_full_dump_cm2"),
        ("📱 Nokia C12 TA-1583 (CM2)",        "dump_nokia_c12_ta1583_cm2"),
        ("📱 iPhone 17 Pro Copy DS-BD2",      "dump_model_iphone_17_pro_copy_ds_bd2"),
        ("📱 S26 Ultra COPY MT6580",          "dump_model_copy_s26_ultra_mt6580"),
        ("📱 BLU T5 TIGO T0050TT",            "dump_model_blu_t5_tigo"),
        ("📱 Itel L6503 Vision 2 (3 tools)",  "dump_model_itel_l6503_vision2"),
    ],
    "amt": [
        ("📱 Redmi A3x missi Android 16",     "dump_model_redmi_a3x_missi_android16"),
        ("📱 Motorola XT2523-7 Moto E15",     "dump_model_motorola_xt2523_7_moto_e15"),
        ("📱 Tecno Spark 40 Pro KM6",         "dump_model_tecno_spark_40_pro_km6"),
    ],
    "miracle": [
        ("📱 Nokia TA-1114 Copy",             "dump_model_nokia_ta_1114_copy"),
    ],
}


def _labels(lang):
    if lang == "en":
        return {
            "main_title": "🛠️ **DUMP Source Tools**\n\nChoose the category below:",
            "jtag_btn": "🛠️ DUMP pulled via JTAG",
            "normal_btn": "🔧 DUMP pulled via standard tools",
            "jtag_title": "🛠️ **Dumps pulled via JTAG**\n\nChoose a tool to view its DUMP cards:",
            "normal_title": "🔧 **Dumps pulled via standard tools**\n\nChoose a tool to view its DUMP cards:",
            "back_main": "🔙 Back",
            "back_category": "🔙 Back to tools",
            "desc_title": "📝 Description:",
            "supported_title": "📱 Supported platforms:",
            "usage_title": "💡 Notes:",
            "usage_text": "• Each DUMP card names the tool it was pulled with.\n• Always back up network files first.",
            "tool_info_btn": "ℹ️ Tool info",
            "cards_count": "📱 Cards:",
        }
    if lang == "fr":
        return {
            "main_title": "🛠️ **Outils de source des DUMP**\n\nChoisissez la catégorie ci-dessous :",
            "jtag_btn": "🛠️ DUMP extrait via JTAG",
            "normal_btn": "🔧 DUMP extrait via outils standards",
            "jtag_title": "🛠️ **Dumps extraits via JTAG**\n\nChoisissez un outil pour voir ses fiches DUMP :",
            "normal_title": "🔧 **Dumps extraits via outils standards**\n\nChoisissez un outil pour voir ses fiches DUMP :",
            "back_main": "🔙 Retour",
            "back_category": "🔙 Retour aux outils",
            "desc_title": "📝 Description :",
            "supported_title": "📱 Plateformes prises en charge :",
            "usage_title": "💡 Remarques :",
            "usage_text": "• Chaque fiche DUMP indique l'outil utilisé.\n• Sauvegardez d'abord les fichiers réseau.",
            "tool_info_btn": "ℹ️ Info outil",
            "cards_count": "📱 Fiches :",
        }
    return {
        "main_title": "🛠️ **أدوات سحب الدامب**\n\nكل ملف دامب داخل البوت تم سحبه بأداة معينة. اختر الفئة أدناه:",
        "jtag_btn": "🛠️ تم سحب الدامب جيتاج",
        "normal_btn": "🔧 تم سحب الدامب عبر الأدوات العادية",
        "jtag_title": "🛠️ **ملفات الدامب التي تم سحبها جيتاج**\n\nاختر الأداة لعرض البطاقات المسحوبة بها:",
        "normal_title": "🔧 **ملفات الدامب التي تم سحبها عبر الأدوات العادية**\n\nاختر الأداة لعرض البطاقات المسحوبة بها:",
        "back_main": "🔙 رجوع",
        "back_category": "🔙 رجوع للأدوات",
        "desc_title": "📝 الوصف:",
        "supported_title": "📱 المنصات المدعومة:",
        "usage_title": "💡 ملاحظات:",
        "usage_text": "• كل بطاقة دامب تُشير إلى الأداة التي سُحبت بها.\n• احتفظ بنسخة احتياطية من ملفات الشبكة قبل التفليش.",
        "tool_info_btn": "ℹ️ معلومات الأداة",
        "cards_count": "📱 البطاقات:",
    }


def _loc(tool, prefix, lang):
    for c in (f"{prefix}_{lang}", f"{prefix}_en", f"{prefix}_ar"):
        if tool.get(c):
            return tool[c]
    return ""


def _short(tool, lang):
    key = tool.get("_key", "")
    cards = len(DUMP_CARDS.get(key, []))
    icon = tool.get("icon", "🛠️")
    name = _loc(tool, "name", lang)
    return f"{icon} {name} ({cards})"[:60]


def _render(chat_id, msg_id, text, markup):
    try:
        BOT.edit_message_text(
            text, chat_id, msg_id,
            reply_markup=markup, parse_mode="Markdown",
            disable_web_page_preview=True,
        )
        return
    except Exception as e:
        print(f"⚠️ dump_tools edit failed: {e}")
    try:
        BOT.delete_message(chat_id, msg_id)
    except Exception:
        pass
    try:
        BOT.send_message(
            chat_id, text, reply_markup=markup,
            parse_mode="Markdown", disable_web_page_preview=True,
        )
    except Exception as e:
        print(f"⚠️ dump_tools send failed: {e}")


def _register_card(tool_key, original_cb):
    raw = f"{tool_key}|{original_cb}"
    short_key = hashlib.md5(raw.encode("utf-8")).hexdigest()[:16]
    _CARD_REGISTRY[short_key] = (tool_key, original_cb)
    return short_key


def clear_card_context():
    _CONTEXT.tool_key = None
    _CONTEXT.original_cb = None
    _CONTEXT.card_label = None


def set_card_context(tool_key, original_cb, card_label=""):
    """Remember the DUMP tool and original callback while a card is rendered."""
    _CONTEXT.tool_key = tool_key
    _CONTEXT.original_cb = original_cb
    _CONTEXT.card_label = card_label or ""


def resolve_card_callback(short_key):
    """Return (tool_key, original_cb) for a registered short token, or None."""
    return _CARD_REGISTRY.get(short_key)


# Callbacks that render a DUMP *list* (a brand section, a paginated brand
# page, the scatter library, ...) instead of a single DUMP card. When a card is
# opened from the tools index its back button points at one of these, and we
# swap it for "back to this tool's card list" so the user is not thrown into an
# unrelated brand menu.
_DUMP_LIST_RE = re.compile(
    r"^(?:dump_.*_(?:section|list)"
    r"|dump_.*_page_\d+"
    r"|dump_scatter.*"
    r"|f64_.*_(?:section|list))$"
)


def _is_dump_list_callback(callback_data):
    """True when ``callback_data`` opens a DUMP list rather than a card."""
    if not callback_data:
        return False
    cb = str(callback_data)
    # Never rewrite our own navigation or the favourite toggle.
    if cb.startswith(("dumptool", "dumpfav_")):
        return False
    return bool(_DUMP_LIST_RE.match(cb))


def _point_back_at_tool(markup, tool_key):
    """Rewrite every list/back button on ``markup`` to return to ``tool_key``."""
    if markup is None or not hasattr(markup, "keyboard") or not tool_key:
        return markup
    for row in markup.keyboard:
        for btn in row:
            cb = getattr(btn, "callback_data", None)
            if not cb:
                continue
            if _is_dump_list_callback(cb):
                try:
                    btn.callback_data = f"dumptool_{tool_key}"
                except Exception:
                    pass
    return markup


def _wrap_reply_markup(bot, method_name):
    """Patch a rendering method so a card's back button returns to its tool list.

    Cards are rendered three different ways depending on the model: on the
    photo, on a follow-up text message, or by editing the current message in
    place. All three have to be covered or the back button of some cards
    throws the user into an unrelated brand menu.
    """
    original = getattr(bot, method_name)

    def wrapped(*args, **kwargs):
        tool_key = getattr(_CONTEXT, "tool_key", None)
        if tool_key and kwargs.get("reply_markup") is not None:
            try:
                _point_back_at_tool(kwargs["reply_markup"], tool_key)
            except Exception as exc:
                print(f"⚠️ wrap_{method_name} patch failed: {exc}")
        return original(*args, **kwargs)

    return wrapped


def _show_main(chat_id, msg_id, lang):
    L = _labels(lang)
    mk = types.InlineKeyboardMarkup(row_width=1)
    mk.add(types.InlineKeyboardButton(L["jtag_btn"], callback_data="dump_tools_jtag"))
    mk.add(types.InlineKeyboardButton(L["normal_btn"], callback_data="dump_tools_normal"))
    # Advanced features
    if lang == "en":
        recent_lbl = "🕐 Recently viewed"
        fav_lbl = "⭐ My favorites"
        search_lbl = "🔍 Search cards"
    elif lang == "fr":
        recent_lbl = "🕐 Consultés récemment"
        fav_lbl = "⭐ Mes favoris"
        search_lbl = "🔍 Rechercher"
    else:
        recent_lbl = "🕐 آخر ما زرته"
        fav_lbl = "⭐ المفضلة"
        search_lbl = "🔍 البحث عن بطاقة"
    mk.row(
        types.InlineKeyboardButton(recent_lbl, callback_data="dumpadv_recent"),
        types.InlineKeyboardButton(fav_lbl, callback_data="dumpadv_favorites"),
    )
    mk.add(types.InlineKeyboardButton(search_lbl, callback_data="dumpadv_search"))
    mk.add(types.InlineKeyboardButton(L["back_main"], callback_data="menu_systems_section"))
    _render(chat_id, msg_id, L["main_title"], mk)


def _show_category(chat_id, msg_id, category, lang):
    L = _labels(lang)
    text = L["jtag_title"] if category == "jtag" else L["normal_title"]
    mk = types.InlineKeyboardMarkup(row_width=1)
    for key, tool in DUMP_TOOLS.items():
        if tool.get("category") != category:
            continue
        tool_with_key = dict(tool)
        tool_with_key["_key"] = key
        mk.add(types.InlineKeyboardButton(
            _short(tool_with_key, lang),
            callback_data=f"dumptool_{key}",
        ))
    mk.add(types.InlineKeyboardButton(L["back_main"], callback_data="dump_tools_section"))
    _render(chat_id, msg_id, text, mk)


def _show_tool_cards(call, key, lang):
    tool = DUMP_TOOLS.get(key)
    if not tool:
        try:
            BOT.answer_callback_query(call.id, "❌ Tool not found", show_alert=True)
        except Exception:
            pass
        return

    L = _labels(lang)
    cards = DUMP_CARDS.get(key, [])
    is_jtag = tool.get("category") == "jtag"
    back_to = "dump_tools_jtag" if is_jtag else "dump_tools_normal"

    icon = tool.get("icon", "🛠️")
    name = _loc(tool, "name", lang)
    text = (
        f"{icon} **{name}**\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"{L['cards_count']} **{len(cards)}**"
    )

    mk = types.InlineKeyboardMarkup(row_width=1)
    mk.add(types.InlineKeyboardButton(
        L["tool_info_btn"],
        callback_data=f"dumptoolinfo_{key}",
    ))
    for card_label, card_cb in cards:
        short_key = _register_card(key, card_cb)
        mk.add(types.InlineKeyboardButton(
            card_label,
            callback_data=f"dumptoolcard_{short_key}",
        ))
    mk.add(types.InlineKeyboardButton(L["back_category"], callback_data=back_to))

    try:
        BOT.answer_callback_query(call.id)
    except Exception:
        pass
    _render(call.message.chat.id, call.message.message_id, text, mk)


def _show_tool_info(call, key, lang):
    tool = DUMP_TOOLS.get(key)
    if not tool:
        try:
            BOT.answer_callback_query(call.id, "❌ Tool not found", show_alert=True)
        except Exception:
            pass
        return

    L = _labels(lang)
    text = (
        f"{tool.get('icon', '🛠️')} **{_loc(tool, 'name', lang)}**\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"{L['desc_title']}\n{_loc(tool, 'desc', lang)}\n\n"
        f"{L['supported_title']}\n{_loc(tool, 'supported', lang)}\n\n"
        f"{L['usage_title']}\n{L['usage_text']}"
    )
    mk = types.InlineKeyboardMarkup(row_width=1)
    if tool.get("url"):
        mk.add(types.InlineKeyboardButton(
            _loc(tool, "btn", lang) or "⬇️ Download",
            url=tool["url"],
        ))
    mk.add(types.InlineKeyboardButton(
        L["back_category"],
        callback_data=f"dumptool_{key}",
    ))

    try:
        BOT.answer_callback_query(call.id)
    except Exception:
        pass
    _render(call.message.chat.id, call.message.message_id, text, mk)


def install(bot, db, data, admin_id):
    global BOT, DB, DATA, ADMIN_ID
    BOT = bot
    DB = db
    DATA = data or {}
    ADMIN_ID = int(admin_id)
    bot.send_photo = _wrap_reply_markup(bot, "send_photo")
    bot.send_message = _wrap_reply_markup(bot, "send_message")
    bot.edit_message_text = _wrap_reply_markup(bot, "edit_message_text")
    print("✅ HMAX DUMP Source Tools loaded (cards index + back-button patch).")