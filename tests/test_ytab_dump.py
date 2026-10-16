"""Tests for the original YTAB library nested inside the TAB section.

The YTAB menu remains reachable through its existing callback and lists the
original dump cards. Each card keeps its poster, download link and a back
button returning to YTAB; the library itself now returns to TAB.
"""

import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import main


class YtabDumpTests(unittest.TestCase):
    SECTION_CALLBACK = "dump_ytab_section"
    MODEL_CALLBACK = "dump_model_ytab_ultra_35_full_dump_cm2"
    MODEL_LABEL = "\U0001f525 ULTRA 35 FULL DUMP 3GB [CM2 | Prince Cazanova]"
    SECTION_LABEL = "\U0001f4f1 YTAB - Library"
    DRIVE_URL = (
        "https://drive.google.com/file/d/1zplMZgC3PUa_MP0F5BOtosQejZaom4dZ/view"
    )
    PHOTO = "ytab_ultra_35_full_dump_cm2_prince_cazanova.jpg"
    CAPTION_DETAILS = (
        "YTAB ULTRA 35",
        "BY CM2 ONLY",
        "Prince Cazanova",
        "Infinity CM2MT2",
        "3 GB",
        "MobiFirmware.VIP",
        "k50sv1_64_bsp",
        "mt6750",
        "arm64-v8a",
        "HMAX hithamMax",
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

    def test_tab_menu_offers_the_ytab_library_button(self):
        main.callback_inline(self._call("dump_tab_section"))

        buttons = self._buttons(self.edit_message_text.call_args.kwargs["reply_markup"])
        by_callback = {button.callback_data: button for button in buttons}
        self.assertEqual(by_callback[self.SECTION_CALLBACK].text, self.SECTION_LABEL)

    def test_ytab_section_lists_the_dump_and_returns_to_the_tab_menu(self):
        main.callback_inline(self._call(self.SECTION_CALLBACK))

        self.edit_message_text.assert_called_once()
        self.assertIn("YTAB", self.edit_message_text.call_args.args[0])
        buttons = self._buttons(self.edit_message_text.call_args.kwargs["reply_markup"])
        self.assertEqual(buttons[0].text, self.MODEL_LABEL)
        self.assertEqual(buttons[0].callback_data, self.MODEL_CALLBACK)
        self.assertEqual(buttons[-1].callback_data, "dump_tab_section")

    def test_ultra_35_card_sends_poster_caption_download_and_back_button(self):
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

    def test_ultra_35_card_falls_back_to_text_when_photo_fails(self):
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
