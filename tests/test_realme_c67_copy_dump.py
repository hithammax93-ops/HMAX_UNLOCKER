"""Tests for the REALME C67 COPY dump card added to the COPY section.

The card lives in the shared COPY library menu (``dump_copy_full_section``),
which is also reachable under the ``dump_copy_section`` alias used by the
dump card's back button. Both names must render the same menu through
``_hmax_show_menu`` so that pressing back while a poster is on screen still
works, and the card itself must send its poster with the Drive link.
"""

import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import main


class RealmeC67CopyDumpTests(unittest.TestCase):
    MODEL_CALLBACK = "dump_model_realme_c67_copy_full_dump_pandora"
    MODEL_LABEL = "\U0001f525 REALME C67 COPY - FULL DUMP 1.1GB [Pandora]"
    COPY_SECTIONS = ("dump_copy_full_section", "dump_copy_section")
    DRIVE_URL = (
        "https://drive.google.com/file/d/1ZFf5jTLPsXjOXU48yb5C_rwmLTiX8BOx/view"
    )
    PHOTO = "realme_c67_copy_full_dump_pandora_prince_cazanova.jpg"
    CAPTION_DETAILS = (
        "REALME C67 COPY",
        "FULL DUMP | Pandora Tool",
        "Prince Cazanova",
        "1.1 GB",
        "Google Drive",
        "MobiFirmware.VIP",
        "Model: C67",
        "Board: k80hd_bsp_fwv_512m",
        "Platform: MTK6580_8.1",
        "Android Version: 8.1.0",
        "Build ID: O11019",
        "Display ID: O11019 test-keys",
        "Security Patch: 2024-03-11",
        "Userdata: F2FS",
        "Important for technicians",
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

    def test_dump_menu_reaches_the_copy_section(self):
        main.callback_inline(self._call("dump_main_section"))

        buttons = self._buttons(self.edit_message_text.call_args.kwargs["reply_markup"])
        self.assertIn("dump_copy_full_section", [b.callback_data for b in buttons])

    def test_copy_sections_list_the_dump_and_return_to_the_dump_menu(self):
        for section in self.COPY_SECTIONS:
            with self.subTest(section=section):
                self.edit_message_text.reset_mock()
                main.callback_inline(self._call(section))

                buttons = self._buttons(
                    self.edit_message_text.call_args.kwargs["reply_markup"]
                )
                by_callback = {b.callback_data: b for b in buttons}
                self.assertIn(self.MODEL_CALLBACK, by_callback)
                self.assertEqual(by_callback[self.MODEL_CALLBACK].text, self.MODEL_LABEL)
                # A section menu must fall back to the DUMP brand menu.
                self.assertEqual(buttons[-1].callback_data, "dump_main_section")

    def test_c67_card_sends_poster_caption_download_and_back_button(self):
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
        self.assertIn(buttons[1].callback_data, self.COPY_SECTIONS)

    def test_c67_card_falls_back_to_text_when_photo_fails(self):
        self.send_photo.side_effect = RuntimeError("photo failed")

        main.callback_inline(self._call(self.MODEL_CALLBACK))

        self.send_message.assert_called_once()
        caption = self.send_message.call_args.args[1]
        for detail in self.CAPTION_DETAILS:
            self.assertIn(detail, caption)
        buttons = self._buttons(self.send_message.call_args.kwargs["reply_markup"])
        self.assertEqual(buttons[0].url, self.DRIVE_URL)


if __name__ == "__main__":
    unittest.main()
