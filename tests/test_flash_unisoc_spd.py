"""Tests for the new "تفليش Unisoc-SPD" section in the flashing tools menu.

The section lives inside the flashing tools menu (``flash_tools_menu``) as a
full-width button named "📲 تفليش Unisoc-SPD" and opens a page that offers the
three official Spreadtrum/Unisoc flashing utilities:

* SPD Upgrade Tool R27.25.4601
* SPD Research Tool R27.24.2301
* SPD Factory Tool R27.25.4601

Each button must be a direct Mediafire link and the back button must return to
the flashing tools menu.
"""

import unittest
from types import SimpleNamespace
from unittest.mock import patch

import main

UNISOC_SECTION = "flash_unisoc_spd"
FLASH_MENU = "flash_tools_menu"

EXPECTED_LINKS = {
    "SPD Upgrade Tool R27.25.4601": (
        "https://www.mediafire.com/file/17wygio8opba6na/"
        "SPD_Upgrade_Tool_R27.25.4601.zip/file"
    ),
    "SPD Research Tool R27.24.2301": (
        "https://www.mediafire.com/file/67lq7q43s7m56wz/"
        "SPD_Research_Tool_R27.24.2301.zip/file"
    ),
    "SPD Factory Tool R27.25.4601": (
        "https://www.mediafire.com/file/rtoistsbxqttyr5/"
        "SPD_Factory_Tool_R27.25.4601.zip/file"
    ),
}


class FlashUnisocSpdTests(unittest.TestCase):
    AR_LABEL = "📲 تفليش Unisoc-SPD"

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

    def test_flashing_menu_offers_the_unisoc_spd_button(self):
        args = self._open(FLASH_MENU)
        buttons = self._buttons(args.kwargs["reply_markup"])
        button_by_callback = {
            button.callback_data: button for button in buttons if button.callback_data
        }

        self.assertIn(UNISOC_SECTION, button_by_callback)
        button = button_by_callback[UNISOC_SECTION]
        self.assertEqual(button.text, self.AR_LABEL)
        # Direct links still work alongside the new menu entry.
        self.assertIn("flash_fw_extractor", button_by_callback)
        # And the flashing menu itself still goes back to the tools hub.
        self.assertEqual(button_by_callback["menu_tools_section"].text, "🔙 رجوع")

    def test_flashing_menu_labels_the_button_in_every_language(self):
        expected = {
            "ar": self.AR_LABEL,
            "en": "📲 Unisoc-SPD Flashing",
            "fr": "📲 Flashage Unisoc-SPD",
        }
        for language, label in expected.items():
            with self.subTest(language=language):
                args = self._open(FLASH_MENU, language=language)
                buttons = self._buttons(args.kwargs["reply_markup"])
                button = next(
                    button for button in buttons if button.callback_data == UNISOC_SECTION
                )
                self.assertEqual(button.text, label)

    def test_section_exposes_the_three_official_tools(self):
        args = self._open(UNISOC_SECTION)
        buttons = self._buttons(args.kwargs["reply_markup"])
        url_buttons = [button for button in buttons if button.url]

        self.assertEqual(len(url_buttons), 3)
        for button, (tool, url) in zip(url_buttons, EXPECTED_LINKS.items()):
            with self.subTest(tool=tool):
                self.assertEqual(button.url, url)
                self.assertIn(tool, button.text)
                self.assertIn("⬇️", button.text)

    def test_section_links_are_unchanged_in_every_language(self):
        for language in ("ar", "en", "fr"):
            with self.subTest(language=language):
                args = self._open(UNISOC_SECTION, language=language)
                buttons = self._buttons(args.kwargs["reply_markup"])
                urls = [button.url for button in buttons if button.url]
                self.assertEqual(urls, list(EXPECTED_LINKS.values()))

    def test_section_back_button_returns_to_the_flashing_menu(self):
        args = self._open(UNISOC_SECTION)
        buttons = self._buttons(args.kwargs["reply_markup"])
        back = buttons[-1]

        self.assertEqual(back.callback_data, FLASH_MENU)
        self.assertIsNone(back.url)
        self.assertIn("رجوع", back.text)

    def test_section_text_mentions_unisoc_and_spd(self):
        args = self._open(UNISOC_SECTION)
        text = args.args[0] if args.args else ""

        self.assertIn("Unisoc", text)
        self.assertIn("SPD", text)
        self.assertEqual(args.kwargs["parse_mode"], "Markdown")


if __name__ == "__main__":
    unittest.main()
