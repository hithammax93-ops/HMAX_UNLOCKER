"""Regression tests for the VIVO Y27 & Y36 5G (V2248) full-dump menu and card."""

import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import main


class VivoY27Y36DumpTests(unittest.TestCase):
    SECTION_CALLBACK = "dump_vivo_full_section"
    MODEL_CALLBACK = "dump_model_vivo_y27_y36_5g_v2248_pd2279f_ex_a_15_2_10_2_w20"
    MODEL_LABEL = "\U0001f525 VIVO Y27 & Y36 5G V2248 - PD2279F_EX_A_15.2.10.2.W20 [RARE]"
    DRIVE_URL = "https://drive.google.com/file/d/14Kuvpi_9UtSH_5jkmMmimIkmm6iK8pKZ/view"
    PHOTO = "vivo_y27_y36_5g_v2248_dump_7_3gb_hmax.jpg"
    CAPTION_DETAILS = (
        "V2248",
        "PD2279F_EX_A_15.2.10.2.W20",
        "MTK6833",
        "Android: 15",
        "Security patch: 2025-05-01",
        "EASYJTAG-PLUS",
        "FLASH64 ULTRA",
        "MIPI TESTER",
        "Compressed: 7.3 GB",
        "Extracted: 17 GB",
        "MobiFirmware.VIP",
        "HMAX-UNLOCKER - HithamMax",
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

    def test_vivo_section_lists_the_y27_y36_model(self):
        main.callback_inline(self._call(self.SECTION_CALLBACK))

        buttons = self._buttons(self.edit_message_text.call_args.kwargs["reply_markup"])
        by_callback = {button.callback_data: button for button in buttons}
        self.assertIn(self.MODEL_CALLBACK, by_callback)
        self.assertEqual(by_callback[self.MODEL_CALLBACK].text, "\U0001f525 Y27 & Y36 5G V2248 - Full Dump 7.3GB [RARE]")
        self.assertEqual(buttons[-1].callback_data, "dump_main_section")

    def test_y27_y36_card_sends_photo_caption_download_and_back_button(self):
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

    def test_y27_y36_card_falls_back_to_text_when_photo_fails(self):
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
