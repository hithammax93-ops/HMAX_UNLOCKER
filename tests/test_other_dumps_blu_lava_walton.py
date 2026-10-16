"""Regression tests for the three new OTHER DUMP models.

Covers the BLU T5 TIGO (CM2), LAVA Iris 59 (Pandora) and WALTON NEXG N72
(Pandora) Terabox cards plus their entries in the ``dump_other_full_section``
menu, in Arabic / English / French. The menu must keep listing the older
OTHER models (RAVOZ V7, POCO C65, LENOVO TB-7305X) while gaining the new ones.
"""

import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import main

IMAGES = Path(__file__).resolve().parents[1] / "images"

MENU_LABELS = {
    "ar": {
        "blu": "📱 BLU T5 TIGO - T0050TT V9.0.G.06.04 [CM2] NEW",
        "lava": "📱 LAVA Iris 59 LE9930 S121 EGY [PANDORA] NEW",
        "walton": "📱 WALTON NEXG N72 Full Dump + Nv [PANDORA] NEW",
    },
    "en": {
        "blu": "📱 BLU T5 TIGO - T0050TT [CM2] NEW",
        "lava": "📱 LAVA Iris 59 LE9930 [PANDORA] NEW",
        "walton": "📱 WALTON NEXG N72 [PANDORA] NEW",
    },
    "fr": {
        "blu": "📱 BLU T5 TIGO - T0050TT [CM2] NOUVEAU",
        "lava": "📱 LAVA Iris 59 [PANDORA] NOUVEAU",
        "walton": "📱 WALTON NEXG N72 [PANDORA] NOUVEAU",
    },
}

CARDS = {
    "dump_model_blu_t5_tigo": {
        "photo": "blu_t5_tigo_t0050tt_hmax_real.jpg",
        "terabox": "https://www.terabox.app/arabic/sharing/link?surl=TLasYwRnDISWcAK9WLzB3Q",
        "details": ("T0050TT", "V9.0.G.06.04_TIGO_30-12-2020_1638", "CM2",
                    "MobiFirmware.VIP", "Terabox", "HMAX-UNLOCKER"),
    },
    "dump_model_lava_iris_59": {
        "photo": "lava_iris_59_le9930_hmax.jpg",
        "terabox": "https://www.terabox.app/arabic/sharing/link?surl=-okpAZRO3RAKy-8YIrP7sQ",
        "details": ("LE9930", "S121_EGY_21G22_ALL_VERSIONS", "Pandora Tool",
                    "MobiFirmware.VIP", "Terabox", "HMAX-UNLOCKER"),
    },
    "dump_model_walton_nexg_n72": {
        "photo": "walton_nexg_n72_hmax.jpg",
        "terabox": "https://www.terabox.app/arabic/sharing/link?surl=UfydmqOdzA2ciqvCRFF_9A",
        "details": ("WALTON NEXG N72", "Full Dump And Nv", "Pandora Tool",
                    "MobiFirmware.VIP", "Terabox", "HMAX-UNLOCKER"),
    },
}

DL_LABELS = {
    "ar": "📥 تحميل من Terabox - VPN سايفون مطلوب",
    "en": "📥 Download Terabox - Need VPN",
    "fr": "📥 Télécharger Terabox - VPN requis",
}
BACK_LABELS = {
    "ar": "⬅️ رجوع لـ OTHER",
    "en": "⬅️ Back to OTHER",
    "fr": "⬅️ Retour à OTHER",
}


def make_call(callback_data, callback_id="callback-other-dumps"):
    return SimpleNamespace(
        id=callback_id,
        data=callback_data,
        message=SimpleNamespace(
            chat=SimpleNamespace(id=123),
            message_id=456,
        ),
    )


def keyboard_buttons(mock):
    return [
        button
        for row in mock.call_args.kwargs["reply_markup"].keyboard
        for button in row
    ]


class OtherDumpsMenuTests(unittest.TestCase):
    def test_menu_lists_new_models_and_keeps_existing_ones_in_all_languages(self):
        for lang, labels in MENU_LABELS.items():
            with self.subTest(lang=lang):
                with (
                    patch("main.hmaxx.allow_user", return_value=True),
                    patch("main.hmaxi18n.bind_callback"),
                    patch("main.hmaxi18n.get_language", return_value=lang),
                    patch("main.bot.answer_callback_query"),
                    patch("main.bot.edit_message_text") as edit_message_text,
                ):
                    main.callback_inline(make_call("dump_other_full_section", f"menu-{lang}"))

                edit_message_text.assert_called_once()
                buttons = keyboard_buttons(edit_message_text)
                callbacks = [button.callback_data for button in buttons]
                for callback in (
                    "dump_model_blu_t5_tigo",
                    "dump_model_lava_iris_59",
                    "dump_model_walton_nexg_n72",
                    # Older OTHER models must stay reachable.
                    "dump_model_ravoz_v7",
                    "dump_model_poco_c65_256gb",
                    "dump_lenovo_tb_7305x",
                ):
                    self.assertIn(callback, callbacks)
                self.assertEqual(callbacks[-1], "dump_main_section")
                for key, callback in (
                    ("blu", "dump_model_blu_t5_tigo"),
                    ("lava", "dump_model_lava_iris_59"),
                    ("walton", "dump_model_walton_nexg_n72"),
                ):
                    button = next(b for b in buttons if b.callback_data == callback)
                    self.assertEqual(button.text, labels[key])


class OtherDumpsPosterTests(unittest.TestCase):
    def test_posters_are_present(self):
        for card in CARDS.values():
            with self.subTest(photo=card["photo"]):
                self.assertTrue((IMAGES / card["photo"]).is_file())


class OtherDumpsCardTests(unittest.TestCase):
    def run_card(self, callback, lang, fallback):
        with (
            patch("main.hmaxx.allow_user", return_value=True),
            patch("main.hmaxi18n.bind_callback"),
            patch("main.hmaxi18n.get_language", return_value=lang),
            patch("main.bot.answer_callback_query"),
            patch("main.bot.delete_message"),
            patch(
                "main.bot.send_photo",
                side_effect=RuntimeError("photo failed") if fallback else None,
            ) as send_photo,
            patch("main.bot.send_message") as send_message,
        ):
            main.callback_inline(make_call(callback, f"{callback}-{lang}"))
        return send_photo, send_message

    def test_cards_send_photo_caption_and_terabox_buttons_in_all_languages(self):
        for callback, card in CARDS.items():
            for lang in ("ar", "en", "fr"):
                with self.subTest(callback=callback, lang=lang):
                    send_photo, send_message = self.run_card(callback, lang, fallback=False)
                    send_photo.assert_called_once()
                    send_message.assert_not_called()
                    self.assertEqual(
                        Path(send_photo.call_args.args[1].name).name, card["photo"]
                    )
                    caption = send_photo.call_args.kwargs["caption"]
                    self.assertLessEqual(len(caption.encode("utf-16-le")) // 2, 1024)
                    for detail in card["details"]:
                        self.assertIn(detail, caption)
                    buttons = keyboard_buttons(send_photo)
                    self.assertEqual(len(buttons), 2)
                    self.assertEqual(buttons[0].text, DL_LABELS[lang])
                    self.assertEqual(buttons[0].url, card["terabox"])
                    self.assertEqual(buttons[1].text, BACK_LABELS[lang])
                    self.assertEqual(buttons[1].callback_data, "dump_other_full_section")

    def test_cards_fall_back_to_text_when_photo_fails(self):
        for callback, card in CARDS.items():
            with self.subTest(callback=callback):
                send_photo, send_message = self.run_card(callback, "en", fallback=True)
                send_photo.assert_called_once()
                send_message.assert_called_once()
                text = send_message.call_args.args[1]
                for detail in card["details"]:
                    self.assertIn(detail, text)
                buttons = keyboard_buttons(send_message)
                self.assertEqual(buttons[0].url, card["terabox"])
                self.assertEqual(buttons[1].callback_data, "dump_other_full_section")


if __name__ == "__main__":
    unittest.main()
