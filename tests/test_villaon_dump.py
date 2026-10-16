"""Regression tests for the VILLAON V20 full-dump menu and download card."""

import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import main


class VillaonDumpTests(unittest.TestCase):
    SECTION_CALLBACK = "dump_villaon_section"
    MODEL_CALLBACK = "dump_model_villaon_v20_full_dump_unlocktool"
    SECTION_LABEL = "\U0001f4f1 VILLAON"
    MODEL_LABEL = "\U0001f525 VILLAON V20 - FULL DUMP V01.57 [UnlockTool]"
    DRIVE_URL = "https://drive.google.com/file/d/10EaY1ggOVvB2Yrgf7BZYSqMcu23fIB7I/view"
    PHOTO = "villaon_v20_full_dump_v01_57_unlocktool_hamallah.jpg"
    CAPTION_DETAILS = (
        "VILLAON V20",
        "Full Dump Firmware",
        "W-V673-V01.57-11.0-GBL",
        "Unlock Tool",
        "Hamallah",
        "MobiFirmware.VIP",
        "HMAX-UNLOCKER HithamMax",
    )

    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        for target, kwargs in (
            ("main.hmaxx.allow_user", {"return_value": True}),
            ("main.hmaxi18n.bind_callback", {}),
            ("main.hmaxi18n.get_language", {"return_value": "en"}),
            ("main.bot.answer_callback_query", {}),
            ("main.bot.delete_message", {}),
        ):
            self.stack.enter_context(patch(target, **kwargs))
        self.edit_message_text = self.stack.enter_context(
            patch("main.bot.edit_message_text")
        )
        self.send_photo = self.stack.enter_context(patch("main.bot.send_photo"))
        self.send_message = self.stack.enter_context(patch("main.bot.send_message"))

    @staticmethod
    def _call(callback_data):
        return SimpleNamespace(
            id="callback-test",
            data=callback_data,
            message=SimpleNamespace(
                chat=SimpleNamespace(id=123),
                message_id=456,
            ),
        )

    @staticmethod
    def _buttons(markup):
        return [button for row in markup.keyboard for button in row]

    def test_dump_menu_offers_the_villaon_brand_button(self):
        main.callback_inline(self._call("dump_main_section"))

        buttons = self._buttons(self.edit_message_text.call_args.kwargs["reply_markup"])
        by_callback = {button.callback_data: button for button in buttons}
        self.assertEqual(by_callback[self.SECTION_CALLBACK].text, self.SECTION_LABEL)

    def test_villaon_section_lists_the_model_and_returns_to_dump_menu(self):
        main.callback_inline(self._call(self.SECTION_CALLBACK))

        self.edit_message_text.assert_called_once()
        self.assertIn("VILLAON", self.edit_message_text.call_args.args[0])
        buttons = self._buttons(self.edit_message_text.call_args.kwargs["reply_markup"])
        self.assertEqual(buttons[0].text, self.MODEL_LABEL)
        self.assertEqual(buttons[0].callback_data, self.MODEL_CALLBACK)
        self.assertEqual(buttons[-1].callback_data, "dump_main_section")

    def test_v20_card_sends_poster_caption_download_and_back_button(self):
        expected_photo = Path(__file__).resolve().parents[1] / "images" / self.PHOTO
        self.assertTrue(expected_photo.is_file())

        main.callback_inline(self._call(self.MODEL_CALLBACK))

        self.send_photo.assert_called_once()
        self.send_message.assert_not_called()
        self.assertEqual(Path(self.send_photo.call_args.args[1].name), expected_photo)

        caption = self.send_photo.call_args.kwargs["caption"]
        self.assertLessEqual(len(caption.encode("utf-16-le")) // 2, 1024)
        for detail in self.CAPTION_DETAILS:
            self.assertIn(detail, caption)

        buttons = self._buttons(self.send_photo.call_args.kwargs["reply_markup"])
        self.assertEqual(buttons[0].url, self.DRIVE_URL)
        self.assertEqual(buttons[1].callback_data, self.SECTION_CALLBACK)

    def test_v20_card_falls_back_to_text_when_photo_fails(self):
        self.send_photo.side_effect = RuntimeError("photo failed")

        main.callback_inline(self._call(self.MODEL_CALLBACK))

        self.send_message.assert_called_once()
        caption = self.send_message.call_args.args[1]
        for detail in self.CAPTION_DETAILS:
            self.assertIn(detail, caption)
        buttons = self._buttons(self.send_message.call_args.kwargs["reply_markup"])
        self.assertEqual(buttons[1].callback_data, self.SECTION_CALLBACK)


if __name__ == "__main__":
    unittest.main()
