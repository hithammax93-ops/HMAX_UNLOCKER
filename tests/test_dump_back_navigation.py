"""Regression tests for the DUMP section back buttons.

These tests pin down the fixes for the broken "رجوع" (back) navigation in the
DUMP section:

1. Every brand sub-section must return to the DUMP brand menu
   (``dump_main_section``) instead of skipping two levels to the systems
   repository. Nested tablet libraries and cards return to their immediate
   parent inside TAB.
2. The F64 ULTRA chain must step back one level at a time
   (lists -> F64 menu -> systems repository).
3. Section menus must render through ``_hmax_show_menu``, which falls back to
   delete + send when Telegram refuses to edit the current message (the
   situation when the user presses back while a *photo* dump card is on
   screen). Without the fallback those back buttons were dead or piled up
   duplicate messages.
"""

import re
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

MAIN_PY = Path(__file__).resolve().parent.parent / "main.py"


def load_source():
    return MAIN_PY.read_text(encoding="utf-8")


def handler_blocks(source):
    """Map every callback_data name to the text of its handler block."""
    header_pattern = re.compile(r"^\s*elif cd (?:==|in\b)", re.M)
    matches = list(header_pattern.finditer(source))
    blocks = {}
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
        block = source[start:end]
        # The header may span several lines (tuple form `elif cd in (...)`).
        header = block.split(":", 1)[0]
        for name in re.findall(r'"([^"]+)"', header):
            blocks.setdefault(name, []).append(block)
    return blocks


def block_for(blocks, callback_name):
    if callback_name not in blocks:
        raise AssertionError(f"no handler found for callback {callback_name!r}")
    return "\n".join(blocks[callback_name])


BACK_KEYWORDS = re.compile(r'(Back|رجوع|عودة|العودة|Retour|\["back"\])')


def back_targets(block):
    """Collect every callback_data used by a back-looking button in a block."""
    targets = set()
    lines = block.split("\n")
    for index, line in enumerate(lines):
        if not BACK_KEYWORDS.search(line):
            continue
        # Some shared brand menus assign a localized back label first, then
        # use that variable in a button much later in the handler block.
        if re.search(r"\bbtn_back\s*=", line):
            match = re.search(
                r'InlineKeyboardButton\(\s*btn_back\s*,\s*callback_data="([^"]+)"',
                "\n".join(lines[index + 1:]),
            )
            if match:
                targets.add(match.group(1))
            continue
        # The button declaration and its callback_data may be split across
        # a few lines; scan a small window starting at the keyword line.
        start = index
        previous = lines[index - 1] if index else ""
        if (
            "callback_data" not in line
            and "InlineKeyboardButton" in previous
            and "callback_data" not in previous
        ):
            start = index - 1
        snippet = "\n".join(lines[start:index + 4])
        match = re.search(r'callback_data="([^"]+)"', snippet)
        if match:
            targets.add(match.group(1))
    return targets


class DumpBackButtonTargetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = load_source()
        cls.blocks = handler_blocks(cls.source)

    def assert_back_goes_to(self, section, expected_target):
        block = block_for(self.blocks, section)
        targets = back_targets(block)
        self.assertTrue(
            targets,
            f"{section} has no back button at all",
        )
        self.assertEqual(
            targets,
            {expected_target},
            f"{section} back button(s) point to {sorted(targets)}, "
            f"expected {expected_target}",
        )

    def test_brand_sections_return_to_the_dump_brand_menu(self):
        brand_sections = [
            "dump_itel_full_section",
            "dump_xiaomi_group_section",
            "dump_infinix_full_section",
            "dump_oppo_full_section",
            "dump_vivo_full_section",
            "dump_other_full_section",
            "dump_copy_full_section",
            "dump_zte_full_section",
            "dump_m_horse_section",
            "dump_tecno_full_section",
            "dump_nokia_section",
            "dump_scatter_samsung",
            "dump_allcall_magic_section",
            "dump_realme_section",
            "dump_pixel_section",
            "dump_benco_section",
            "dump_hisorl_section",
            "dump_tab_section",
        ]
        for section in brand_sections:
            with self.subTest(section=section):
                self.assert_back_goes_to(section, "dump_main_section")

    def test_tablet_sections_and_cards_return_to_their_parent(self):
        for section, parent in (
            ("dump_ytab_section", "dump_tab_section"),
            ("dump_model_tab_a9_sm_x110", "dump_tab_section"),
            ("dump_model_samsung_tab_a9_sm_x110", "dump_tab_section"),
            ("dump_model_the_oteeto_tab_15_full_dump_cm2", "dump_tab_section"),
            ("dump_model_ytab_ultra_35_full_dump_cm2", "dump_ytab_section"),
        ):
            with self.subTest(section=section):
                self.assert_back_goes_to(section, parent)

    def test_dump_main_section_returns_to_the_systems_repository(self):
        self.assert_back_goes_to("dump_main_section", "menu_systems_section")

    def test_f64_menu_returns_to_the_systems_repository(self):
        # The F64 menu is opened from the systems repository, not from the
        # DUMP brand menu.
        self.assert_back_goes_to("f64_ultra_dump_section", "menu_systems_section")

    def test_f64_lists_return_to_the_f64_menu(self):
        self.assert_back_goes_to("f64_redmi_section", "f64_ultra_dump_section")
        self.assert_back_goes_to("f64_all_section", "f64_ultra_dump_section")
        self.assert_back_goes_to(
            "dump_jtag_f64_ultra_section", "f64_ultra_dump_section"
        )

    def test_every_dump_button_target_has_a_handler(self):
        handlers = set(re.findall(r'elif cd == "([^"]+)"', self.source))
        for match in re.finditer(r"elif cd in \((.*?)\):", self.source, re.S):
            handlers |= set(re.findall(r'"([^"]+)"', match.group(1)))
        used = {
            target
            for target in re.findall(r'callback_data="([^"]+)"', self.source)
            if target.startswith(("dump_", "f64_"))
        }
        missing = sorted(used - handlers)
        self.assertEqual(missing, [], f"dangling back targets: {missing}")

    def test_dump_section_menus_render_through_the_safe_helper(self):
        """Section menus must not call edit_message_text directly.

        A direct edit crashes (or silently dies) when the previous message is
        a photo dump card, which is exactly the moment the user presses back.
        """
        sections = [
            "dump_main_section",
            "dump_itel_full_section",
            "dump_jtag_f64_ultra_section",
            "dump_xiaomi_group_section",
            "dump_infinix_full_section",
            "dump_other_full_section",
            "dump_copy_full_section",
            "dump_zte_full_section",
            "dump_m_horse_section",
            "dump_tecno_full_section",
            "dump_nokia_section",
            "dump_scatter_samsung",
            "dump_allcall_magic_section",
            "dump_realme_section",
            "dump_benco_section",
            "dump_hisorl_section",
            "dump_tab_section",
            "dump_ytab_section",
            "f64_ultra_dump_section",
            "f64_redmi_section",
        ]
        for section in sections:
            with self.subTest(section=section):
                block = block_for(self.blocks, section)
                self.assertIn("_hmax_show_menu", block, f"{section} must use the helper")
                self.assertNotIn(
                    "edit_message_text",
                    block,
                    f"{section} must not edit the message directly",
                )


class ShowMenuFallbackTests(unittest.TestCase):
    """Behavioural tests for the ``_hmax_show_menu`` fallback."""

    def _call(self, chat_id=777, message_id=42):
        return SimpleNamespace(
            message=SimpleNamespace(chat=SimpleNamespace(id=chat_id), message_id=message_id)
        )

    def test_edit_in_place_when_possible(self):
        import main

        bot = MagicMock()
        call = self._call()
        with patch.object(main, "bot", bot):
            main._hmax_show_menu(call, "menu text", "MARKUP", parse_mode="Markdown")

        bot.edit_message_text.assert_called_once_with(
            "menu text", 777, 42, reply_markup="MARKUP", parse_mode="Markdown"
        )
        bot.delete_message.assert_not_called()
        bot.send_message.assert_not_called()

    def test_falls_back_to_delete_and_send_when_edit_fails(self):
        """Simulates pressing back while a photo dump card is on screen."""
        import main

        bot = MagicMock()
        bot.edit_message_text.side_effect = RuntimeError(
            "there is no text in the message to edit"
        )
        call = self._call()
        with patch.object(main, "bot", bot):
            main._hmax_show_menu(call, "menu text", "MARKUP")

        bot.delete_message.assert_called_once_with(chat_id=777, message_id=42)
        bot.send_message.assert_called_once_with(
            777, "menu text", reply_markup="MARKUP", parse_mode=None
        )

    def test_still_sends_when_both_edit_and_delete_fail(self):
        import main

        bot = MagicMock()
        bot.edit_message_text.side_effect = RuntimeError("cannot edit")
        bot.delete_message.side_effect = RuntimeError("message too old")
        call = self._call()
        with patch.object(main, "bot", bot):
            main._hmax_show_menu(call, "menu text", "MARKUP")

        bot.send_message.assert_called_once_with(
            777, "menu text", reply_markup="MARKUP", parse_mode=None
        )


if __name__ == "__main__":
    unittest.main()
