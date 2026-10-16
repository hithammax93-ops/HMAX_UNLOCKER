"""Regression tests for the "🛠️ أدوات سحب الدامب" (DUMP source tools) section.

History: the section stopped responding entirely because ``hmax_dump_tools.py``
contained a stray duplicate ``def _register_card(...):`` header with no body.
That is a hard ``IndentationError`` at import time, so every ``import
hmax_dump_tools`` inside ``main.py`` raised and was swallowed by the surrounding
``try/except`` — the button answered the callback and then did nothing.

These tests pin the whole chain down:

1. every Python file in the repository compiles (catches the original bug);
2. the DUMP tools module imports and installs cleanly;
3. every card listed in ``DUMP_CARDS`` points at a callback that ``main.py``
   actually handles (three cards used a ``dump_model_*`` name that no handler
   answered, so they were dead buttons too);
4. pressing the section button renders a menu instead of silently dying;
5. the favourite hook resolves the real i18n module name (``hmax_i18n``, not
   the non-existent ``hmaxi18n``).
"""

import contextlib
import importlib
import io
import os
import py_compile
import re
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _new_fake_bot():
    """Minimal recorder standing in for ``telebot.TeleBot``."""

    class FakeBot:
        def __init__(self):
            self.log = []

        def _record(self, name, *args, **kwargs):
            self.log.append((name, args, kwargs))
            return SimpleNamespace(message_id=99, chat=SimpleNamespace(id=args[0] if args else 0))

        def edit_message_text(self, *a, **kw):
            return self._record("edit", *a, **kw)

        def send_message(self, *a, **kw):
            return self._record("send_msg", *a, **kw)

        def send_photo(self, *a, **kw):
            return self._record("send_photo", *a, **kw)

        def delete_message(self, *a, **kw):
            return self._record("del", *a, **kw)

        def answer_callback_query(self, *a, **kw):
            return self._record("ack", *a, **kw)

        def register_next_step_handler(self, *a, **kw):
            return self._record("next_step", *a, **kw)

        def reset(self):
            self.log = []

    return FakeBot()


class RepositoryCompilesTests(unittest.TestCase):
    """A syntax error in any module silently kills the DUMP tools section."""

    def test_every_python_file_compiles(self):
        skipped_dirs = {".git", ".venv", "__pycache__", "node_modules"}
        failures = []
        for path in sorted(REPO_ROOT.rglob("*.py")):
            if any(part in skipped_dirs for part in path.parts):
                continue
            try:
                py_compile.compile(str(path), doraise=True)
            except py_compile.PyCompileError as exc:
                failures.append(f"{path.relative_to(REPO_ROOT)}: {exc}")
        self.assertEqual(failures, [], "syntax errors found:\n" + "\n".join(failures))


class DumpToolsModuleTests(unittest.TestCase):
    def setUp(self):
        self.hdt = importlib.import_module("hmax_dump_tools")

    def test_module_imports_and_exposes_its_api(self):
        for name in ("DUMP_TOOLS", "DUMP_CARDS", "install", "resolve_card_callback"):
            self.assertTrue(hasattr(self.hdt, name), f"hmax_dump_tools is missing {name}")

    def test_install_binds_the_bot_without_raising(self):
        bot = _new_fake_bot()
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.hdt.install(bot, None, {}, 560330933)
        self.assertIn("DUMP Source Tools loaded", out.getvalue())

    def test_card_tokens_round_trip(self):
        token = self.hdt._register_card("cm2", "dump_nokia_c12_ta1583_cm2")
        self.assertEqual(
            self.hdt.resolve_card_callback(token),
            ("cm2", "dump_nokia_c12_ta1583_cm2"),
        )

    def test_advanced_nav_registration_shares_the_registry(self):
        """Search/favourites tokens must resolve through the same registry."""
        adv = importlib.import_module("hmax_dump_advanced")
        token = adv._register_card_for_nav("pandora", "dump_model_redmi_13c_gale")
        self.assertEqual(
            self.hdt.resolve_card_callback(token),
            ("pandora", "dump_model_redmi_13c_gale"),
        )


class DumpCardHandlerTests(unittest.TestCase):
    """Every card button must point at a callback ``main.py`` really handles."""

    @classmethod
    def setUpClass(cls):
        cls.hdt = importlib.import_module("hmax_dump_tools")
        cls.source = (REPO_ROOT / "main.py").read_text(encoding="utf-8")

    @staticmethod
    def _handled_callbacks(source):
        handled = set(re.findall(r'elif cd == "([^"]+)"', source))
        handled |= set(re.findall(r'^\s*if cd == "([^"]+)"', source, re.M))
        for match in re.finditer(r"elif cd in \((.*?)\):", source, re.S):
            handled |= set(re.findall(r'"([^"]+)"', match.group(1)))
        return handled

    def test_every_dump_card_has_a_handler(self):
        handled = self._handled_callbacks(self.source)
        dangling = []
        for tool_key, cards in self.hdt.DUMP_CARDS.items():
            for label, callback in cards:
                if callback not in handled:
                    dangling.append(f"{tool_key}: {label} -> {callback}")
        self.assertEqual(dangling, [], "dead DUMP cards:\n" + "\n".join(dangling))

    def test_every_section_button_has_a_handler(self):
        handled = self._handled_callbacks(self.source)
        required = {
            "dump_tools_section",
            "dump_tools_jtag",
            "dump_tools_normal",
            "dumpadv_recent",
            "dumpadv_favorites",
            "dumpadv_search",
        }
        self.assertEqual(required - handled, set())


class DumpToolsFlowTests(unittest.TestCase):
    """End-to-end: press the section button and the sub-menus it leads to."""

    @classmethod
    def setUpClass(cls):
        os.environ.setdefault("BOT_TOKEN", "123456:FAKE-TOKEN-FOR-TESTS")
        with contextlib.redirect_stdout(io.StringIO()):
            cls.main = importlib.import_module("main")
            cls.hdt = importlib.import_module("hmax_dump_tools")
            cls.adv = importlib.import_module("hmax_dump_advanced")

    def setUp(self):
        self.bot = _new_fake_bot()
        with contextlib.redirect_stdout(io.StringIO()):
            self.hdt.install(self.bot, None, {}, 560330933)
            self.adv.install(self.bot, None, 560330933)
        self.main.bot = self.bot
        self.chat_id = 560330933
        self.call = SimpleNamespace(
            id="cb",
            data="",
            from_user=SimpleNamespace(id=self.chat_id),
            message=SimpleNamespace(
                chat=SimpleNamespace(id=self.chat_id), message_id=42
            ),
        )

    def press(self, data):
        self.call.data = data
        self.bot.reset()
        with contextlib.redirect_stdout(io.StringIO()):
            self.main.callback_inline(self.call)
        return self.bot.log

    @staticmethod
    def rendered(log):
        for name, args, kwargs in log:
            if name == "edit":
                return args[0], kwargs.get("reply_markup")
        for name, args, kwargs in log:
            if name == "send_msg":
                return args[1], kwargs.get("reply_markup")
        return None, None

    @staticmethod
    def buttons(markup):
        return [button for row in markup.keyboard for button in row]

    def test_section_button_renders_the_tools_menu(self):
        log = self.press("dump_tools_section")
        text, markup = self.rendered(log)
        self.assertIsNotNone(markup, "dump_tools_section rendered nothing")
        self.assertIn("أدوات سحب الدامب", text)
        labels = {b.callback_data for b in self.buttons(markup)}
        self.assertEqual(
            labels,
            {
                "dump_tools_jtag",
                "dump_tools_normal",
                "dumpadv_recent",
                "dumpadv_favorites",
                "dumpadv_search",
                "menu_systems_section",
            },
        )

    def test_category_menus_list_their_tools(self):
        for category, expected in (
            ("dump_tools_jtag", {"easy_jtag", "f64_ultra", "ufi"}),
            ("dump_tools_normal", {"unlocktool", "cm2", "pandora", "amt", "miracle"}),
        ):
            with self.subTest(category=category):
                _, markup = self.rendered(self.press(category))
                tools = {
                    b.callback_data[len("dumptool_"):]
                    for b in self.buttons(markup)
                    if str(b.callback_data).startswith("dumptool_")
                }
                self.assertEqual(tools, expected)

    def test_tool_menu_lists_registered_cards(self):
        _, markup = self.rendered(self.press("dumptool_easy_jtag"))
        cards = [
            b for b in self.buttons(markup)
            if str(b.callback_data).startswith("dumptoolcard_")
        ]
        self.assertEqual(len(cards), len(self.hdt.DUMP_CARDS["easy_jtag"]))

    def test_every_card_responds(self):
        """A dead card is exactly the 'button does nothing' symptom."""
        for tool_key in self.hdt.DUMP_TOOLS:
            _, markup = self.rendered(self.press(f"dumptool_{tool_key}"))
            for button in self.buttons(markup):
                if not str(button.callback_data).startswith("dumptoolcard_"):
                    continue
                with self.subTest(tool=tool_key, card=button.text):
                    log = self.press(button.callback_data)
                    names = {name for name, _, _ in log}
                    self.assertTrue(
                        names & {"send_photo", "send_msg", "edit"},
                        f"{button.text} produced no output ({sorted(names)})",
                    )

    def card_markups(self, log):
        """Every keyboard a card renders — photo, text message, or in-place edit."""
        markups = []
        for name, _, kwargs in log:
            if name in ("send_photo", "send_msg", "edit"):
                markup = kwargs.get("reply_markup")
                if markup is not None:
                    markups.append(markup)
        return markups

    def test_card_back_button_returns_to_the_tool_list(self):
        """Every card must lead back to the tool that pulled it.

        Cards carry their keyboard in three different places depending on the
        model: on the photo, on a follow-up text message, or on an in-place
        edit. All three paths are patched — miss one and "back" throws the
        user into an unrelated brand menu instead of the tool's card list.
        """
        for tool_key in self.hdt.DUMP_TOOLS:
            _, markup = self.rendered(self.press(f"dumptool_{tool_key}"))
            for button in self.buttons(markup):
                if not str(button.callback_data).startswith("dumptoolcard_"):
                    continue
                log = self.press(button.callback_data)
                markups = self.card_markups(log)
                with self.subTest(tool=tool_key, card=button.text):
                    backs = [
                        b.callback_data
                        for card_markup in markups
                        for b in self.buttons(card_markup)
                        if b.callback_data == f"dumptool_{tool_key}"
                    ]
                    self.assertTrue(
                        backs,
                        "card kept its original back button: "
                        + str(
                            [
                                b.callback_data
                                for card_markup in markups
                                for b in self.buttons(card_markup)
                                if b.callback_data
                            ]
                        ),
                    )
                    _, back_markup = self.rendered(self.press(backs[0]))
                    first = self.buttons(back_markup)[0].callback_data
                    self.assertEqual(first, f"dumptoolinfo_{tool_key}")

    def test_no_card_keeps_a_stale_dump_list_back_button(self):
        """No card opened from the tools index may still point at a brand list."""
        hdt = self.hdt
        for tool_key in hdt.DUMP_TOOLS:
            _, markup = self.rendered(self.press(f"dumptool_{tool_key}"))
            for button in self.buttons(markup):
                if not str(button.callback_data).startswith("dumptoolcard_"):
                    continue
                log = self.press(button.callback_data)
                with self.subTest(tool=tool_key, card=button.text):
                    leftovers = [
                        b.callback_data
                        for card_markup in self.card_markups(log)
                        for b in self.buttons(card_markup)
                        if b.callback_data
                        and hdt._is_dump_list_callback(b.callback_data)
                    ]
                    self.assertEqual(leftovers, [], "stale back button left on card")

    def test_every_card_gets_exactly_one_favorite_button(self):
        """Two regressions at once.

        ``from hmaxi18n import get_language`` raised ``ModuleNotFoundError``
        (the module is ``hmax_i18n``), so the button never appeared; and cards
        rendered through ``send_message`` were never hooked at all. Adding the
        hook to every render path must not attach the button twice either.
        """
        for tool_key in self.hdt.DUMP_TOOLS:
            _, markup = self.rendered(self.press(f"dumptool_{tool_key}"))
            for card in self.buttons(markup):
                if not str(card.callback_data).startswith("dumptoolcard_"):
                    continue
                log = self.press(card.callback_data)
                with self.subTest(tool=tool_key, card=card.text):
                    favs = [
                        b.callback_data
                        for card_markup in self.card_markups(log)
                        for b in self.buttons(card_markup)
                        if str(b.callback_data).startswith("dumpfav_")
                    ]
                    self.assertEqual(
                        len(favs), 1,
                        f"expected one favourite button, got {favs}",
                    )
                    token = favs[0][len("dumpfav_"):]
                    resolved = self.adv._resolve_fav_token(token)
                    self.assertTrue(
                        resolved,
                        "favourite token does not resolve back to a card",
                    )


class FavoriteHookImportTests(unittest.TestCase):
    def test_advanced_module_references_the_real_i18n_module(self):
        source = (REPO_ROOT / "hmax_dump_advanced.py").read_text(encoding="utf-8")
        self.assertNotIn("from hmaxi18n import", source)
        self.assertIn("from hmax_i18n import get_language", source)

    def test_get_language_is_importable(self):
        module = importlib.import_module("hmax_i18n")
        self.assertTrue(callable(module.get_language))


if __name__ == "__main__":
    unittest.main()
