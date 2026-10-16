"""Tests for the SIMUNLOCKER_ODIN entry in the flashing tools menu.

The button lives inside the flashing tools menu (``flash_tools_menu``) as a
full-width direct-download button. Its label carries the tool name
(``SIMUNLOCKER_ODIN``) plus the description "أداة لتفليش أنظمة السامسونج كاملة
أو قطاعات محددة", in all three bot languages, and the URL points to the
Mediafire archive of the tool.
"""

import unittest
from types import SimpleNamespace
from unittest.mock import patch

import main

FLASH_MENU = "flash_tools_menu"

ODIN_URL = (
    "https://www.mediafire.com/file/ji1cgxb398up8lp/"
    "SIMUNLOCKER_ODIN1.1-V-1.rar/file"
)

EXPECTED_LABELS = {
    "ar": "🧰 SIMUNLOCKER_ODIN — أداة لتفليش أنظمة السامسونج كاملة أو قطاعات محددة",
    "en": "🧰 SIMUNLOCKER_ODIN — Flash full Samsung firmware or selected partitions",
    "fr": "🧰 SIMUNLOCKER_ODIN — Flasher un firmware Samsung complet ou des partitions choisies",
}


class FlashSimunlockerOdinTests(unittest.TestCase):
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

    def _open(self, callback_data, language="ar"):
        call = self._call(callback_data)
        with (
            patch("main.hmaxx.allow_user", return_value=True),
            patch("main.hmaxi18n.bind_callback"),
            patch("main.hmaxi18n.get_language", return_value=language),
            patch("main.bot.answer_callback_query"),
            patch("main.bot.edit_message_text") as edit_message_text,
        ):
            main.callback_inline(call)
        edit_message_text.assert_called_once()
        return edit_message_text.call_args

    def _odin_button(self, language="ar"):
        args = self._open(FLASH_MENU, language=language)
        buttons = self._buttons(args.kwargs["reply_markup"])
        candidates = [button for button in buttons if button.url == ODIN_URL]
        self.assertEqual(len(candidates), 1)
        return candidates[0]

    def test_flashing_menu_offers_the_odin_download_button(self):
        button = self._odin_button()
        self.assertEqual(button.text, EXPECTED_LABELS["ar"])
        self.assertIn("SIMUNLOCKER_ODIN", button.text)
        self.assertIsNone(button.callback_data)

    def test_odin_button_label_in_every_language(self):
        for language, label in EXPECTED_LABELS.items():
            with self.subTest(language=language):
                button = self._odin_button(language)
                self.assertEqual(button.text, label)
                # The tool keeps its exact name in every language.
                self.assertIn("SIMUNLOCKER_ODIN", button.text)

    def test_odin_link_is_a_direct_mediafire_download(self):
        for language in ("ar", "en", "fr"):
            with self.subTest(language=language):
                self.assertEqual(self._odin_button(language).url, ODIN_URL)

    def test_existing_menu_entries_and_back_button_are_untouched(self):
        args = self._open(FLASH_MENU)
        buttons = self._buttons(args.kwargs["reply_markup"])
        callback_by_button = {
            button.callback_data: button for button in buttons if button.callback_data
        }

        self.assertIn("flash_fw_extractor", callback_by_button)
        self.assertIn("flash_unisoc_spd", callback_by_button)
        self.assertEqual(
            callback_by_button["menu_tools_section"].text, "🔙 رجوع"
        )


if __name__ == "__main__":
    unittest.main()
