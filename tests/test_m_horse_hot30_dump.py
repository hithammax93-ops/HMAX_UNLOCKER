"""Tests for the M-HORSE HOT 30 V05 full dump card.

The card lives in the M-HORSE library menu (``dump_m_horse_section``) and is
opened through ``dump_model_m_horse_hot_30_full_dump_unlocktool``. It must
send its poster with the Drive link, and its back button must return to the
M-HORSE menu (which itself falls back to the DUMP brand menu).
"""

import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import main


class MHorseHot30DumpTests(unittest.TestCase):
    SECTION = "dump_m_horse_section"
    MODEL_CALLBACK = "dump_model_m_horse_hot_30_full_dump_unlocktool"
    MODEL_LABEL = "\U0001f525 M-HORSE HOT 30 V05 - FULL DUMP [UnlockTool]"
    DRIVE_URL = (
        "https://drive.google.com/file/d/1tpgGTmlS8ZV_T6Pbd-5U58fXrLqV8i7T/view"
    )
    PHOTO = "mhorse_hot_30_full_dump_unlocktool_hamallah.jpg"
    CAPTION_DETAILS = (
        "M-HORSE HOT 30",
        "FULL DUMP",
        "BY UNLOCKTOOL | DUMPING-FIRMWARE",
        "HOT 30-M-HORSE-V05-20240410",
        "Hamallah",
        "MobiFirmware.VIP",
        "HMAX hithamMax",
        "Device: M-HORSE HOT 30",
        "Tool: UnlockTool",
        "do NOT flash a different version",
        "back up",
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

    def test_callback_data_stays_within_the_telegram_limit(self):
        self.assertLessEqual(len(self.MODEL_CALLBACK.encode("utf-8")), 64)

    def test_m_horse_section_lists_the_dump_and_returns_to_the_dump_menu(self):
        main.callback_inline(self._call(self.SECTION))

        buttons = self._buttons(self.edit_message_text.call_args.kwargs["reply_markup"])
        by_callback = {b.callback_data: b for b in buttons}
        self.assertIn(self.MODEL_CALLBACK, by_callback)
        self.assertEqual(by_callback[self.MODEL_CALLBACK].text, self.MODEL_LABEL)
        self.assertEqual(buttons[-1].callback_data, "dump_main_section")

    def test_hot30_card_sends_poster_caption_download_and_back_button(self):
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
        self.assertEqual(buttons[-1].callback_data, self.SECTION)

    def test_hot30_card_falls_back_to_text_when_photo_fails(self):
        self.send_photo.side_effect = RuntimeError("photo failed")

        main.callback_inline(self._call(self.MODEL_CALLBACK))

        self.send_message.assert_called_once()
        caption = self.send_message.call_args.args[1]
        for detail in self.CAPTION_DETAILS:
            self.assertIn(detail, caption)
        buttons = self._buttons(self.send_message.call_args.kwargs["reply_markup"])
        self.assertEqual(buttons[0].url, self.DRIVE_URL)
        self.assertEqual(buttons[-1].callback_data, self.SECTION)


if __name__ == "__main__":
    unittest.main()
