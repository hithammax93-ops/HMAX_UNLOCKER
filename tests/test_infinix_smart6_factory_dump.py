"""Regression tests for the Infinix Smart 6 X6511B Factory Signed card.

The card is reachable from both Infinix menus (the hand written section and
the auto generated ``DUMP_SMART_SECTIONS`` catalogue) and must keep rendering
its poster, caption and Google Drive button even when Telegram rejects the
callback ack, the menu delete or the photo upload itself.
"""

import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import main
from main import DUMP_SMART_SECTIONS


CALLBACK = "dump_model_x6511b_factory_signed"
POSTER = "infinix_smart6_x6511b_factory_hmax.jpg"
DRIVE_URL = "https://drive.google.com/file/d/1LpISua-lTGlvea_P5oR9alxyEHTVuzcR/view"


class InfinixSmart6FactoryDumpTests(unittest.TestCase):
    def setUp(self):
        for target, kwargs in (
            ("main.hmaxx.allow_user", {"return_value": True}),
            ("main.hmaxi18n.bind_callback", {}),
            ("main.hmaxi18n.get_language", {"return_value": "en"}),
            ("main.bot.answer_callback_query", {}),
            ("main.bot.delete_message", {}),
            ("main.bot.send_photo", {}),
            ("main.bot.send_message", {}),
            ("main.bot.edit_message_text", {}),
        ):
            patcher = patch(target, **kwargs)
            setattr(self, target.rsplit(".", 1)[1], patcher.start())
            self.addCleanup(patcher.stop)

    def invoke(self, callback=CALLBACK):
        main.callback_inline(SimpleNamespace(
            id="test-callback", data=callback,
            message=SimpleNamespace(chat=SimpleNamespace(id=123), message_id=456),
        ))

    def test_card_is_registered_in_the_dump_catalogue(self):
        self.assertIn(
            ("🔥 Infinix Smart 6 X6511B - Factory Signed", CALLBACK),
            DUMP_SMART_SECTIONS["infinix"],
        )

    def test_card_is_available_in_both_infinix_menus(self):
        for menu in ("dump_infinix_section", "dump_infinix_full_section"):
            with self.subTest(menu=menu):
                self.invoke(menu)
                buttons = self.edit_message_text.call_args.kwargs["reply_markup"].keyboard
                self.assertEqual(sum(b.callback_data == CALLBACK for row in buttons for b in row), 1)

    def test_photo_caption_and_buttons(self):
        self.invoke()
        self.send_photo.assert_called_once()
        self.send_message.assert_not_called()
        photo = self.send_photo.call_args.args[1]
        self.assertEqual(
            Path(photo.name),
            Path(main.__file__).resolve().parent / "images" / POSTER,
        )
        caption = self.send_photo.call_args.kwargs["caption"]
        for detail in (
            "Infinix Smart 6", "X6511B", "Factory Signed",
            "X6511B-F6318-11.0-OP-V127-20230810",
            "Verified • Official • Secure",
            "MobiFirmware.VIP", "Google Drive",
            "Unisoc SC9863A", "5000mAh",
            "HMAX-UNLOCKER - HithamMax",
        ):
            self.assertIn(detail, caption)
        self.assertLessEqual(len(caption.encode("utf-16-le")) // 2, 1024)
        buttons = [b for row in self.send_photo.call_args.kwargs["reply_markup"].keyboard for b in row]
        self.assertEqual(buttons[0].url, DRIVE_URL)
        self.assertEqual(buttons[1].callback_data, "dump_infinix_section")

    def test_missing_photo_falls_back_to_text(self):
        with patch("builtins.open", side_effect=FileNotFoundError("missing poster")):
            self.invoke()
        self.send_photo.assert_not_called()
        self.send_message.assert_called_once()
        self.assertIn("X6511B", self.send_message.call_args.args[1])

    def test_photo_api_failure_falls_back_to_same_text_and_buttons(self):
        self.send_photo.side_effect = RuntimeError("Telegram photo failure")
        self.invoke()
        self.send_message.assert_called_once_with(
            123, self.send_photo.call_args.kwargs["caption"],
            reply_markup=self.send_photo.call_args.kwargs["reply_markup"],
        )

    def test_callback_and_delete_failures_do_not_block_photo(self):
        self.answer_callback_query.side_effect = RuntimeError("expired callback")
        self.delete_message.side_effect = RuntimeError("message already deleted")
        self.invoke()
        self.delete_message.assert_called_once()
        self.send_photo.assert_called_once()

    def test_poster_file_exists(self):
        self.assertTrue((Path(main.__file__).resolve().parent / "images" / POSTER).is_file())


if __name__ == "__main__":
    unittest.main()
