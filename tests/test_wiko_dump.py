"""Tests for the WIKO brand entry added to the DUMP section.

The WIKO section follows the YTAB / BENCO / HISORL pattern: a brand menu
reachable from ``dump_main_section`` that lists the dump cards, and each card
sends its poster with the Google Drive link and a back button that returns to
the WIKO menu (not straight to the brand list).
"""

import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import main


class WikoDumpTests(unittest.TestCase):
    SECTION_CALLBACK = "dump_wiko_section"
    MODEL_CALLBACK = "dump_model_wiko_t10_full_dump_unlocktool"
    MODEL_LABEL = "\U0001f525 WIKO T10 - FULL DUMP V01.57 [UnlockTool]"
    SECTION_LABEL = "\U0001f4f1 WIKO"
    DRIVE_URL = "https://drive.google.com/file/d/1HGMTtBPH4TNYXIusU4G1ZO3scGphM7cq/view"
    PHOTO = "wiko_t10_full_dump_v01_57_unlocktool_hamallah.jpg"
    CAPTION_DETAILS = (
        "WIKO T10",
        "W-V673-01 / W-V673-02",
        "W-V673-V01.57-11.0-GBL",
        "Unlock Tool",
        "Hamallah",
        "MT6761",
        "MobiFirmware.VIP",
        "HMAX-UNLOCKER HithamMax",
    )

    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        for name, kwargs in (
            ("hmaxx.allow_user", {"return_value": True}),
            ("hmaxi18n.bind_callback", {}),
            ("hmaxi18n.get_language", {"return_value": "en"}),
            ("bot.answer_callback_query", {}),
            ("bot.delete_message", {}),
        ):
            self.stack.enter_context(patch("main." + name, **kwargs))
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

    def test_dump_menu_offers_the_wiko_brand_button(self):
        main.callback_inline(self._call("dump_main_section"))

        buttons = self._buttons(self.edit_message_text.call_args.kwargs["reply_markup"])
        by_callback = {button.callback_data: button for button in buttons}
        self.assertEqual(by_callback[self.SECTION_CALLBACK].text, self.SECTION_LABEL)

    def test_wiko_section_lists_the_dump_and_returns_to_the_dump_menu(self):
        main.callback_inline(self._call(self.SECTION_CALLBACK))

        self.edit_message_text.assert_called_once()
        self.assertIn("WIKO", self.edit_message_text.call_args.args[0])
        buttons = self._buttons(self.edit_message_text.call_args.kwargs["reply_markup"])
        self.assertEqual(buttons[0].text, self.MODEL_LABEL)
        self.assertEqual(buttons[0].callback_data, self.MODEL_CALLBACK)
        self.assertEqual(buttons[-1].callback_data, "dump_main_section")

    def test_t10_card_sends_poster_caption_download_and_back_button(self):
        expected_photo = Path(__file__).resolve().parents[1] / "images" / self.PHOTO
        self.assertTrue(expected_photo.is_file())

        main.callback_inline(self._call(self.MODEL_CALLBACK))

        self.send_photo.assert_called_once()
        self.send_message.assert_not_called()
        self.assertEqual(Path(self.send_photo.call_args.args[1].name), expected_photo)

        caption = self.send_photo.call_args.kwargs["caption"]
        # Telegram rejects captions longer than 1024 UTF-16 code units.
        self.assertLessEqual(len(caption.encode("utf-16-le")) // 2, 1024)
        for detail in self.CAPTION_DETAILS:
            self.assertIn(detail, caption)

        buttons = self._buttons(self.send_photo.call_args.kwargs["reply_markup"])
        self.assertEqual(buttons[0].url, self.DRIVE_URL)
        self.assertEqual(buttons[1].callback_data, self.SECTION_CALLBACK)

    def test_t10_card_falls_back_to_text_when_photo_fails(self):
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
