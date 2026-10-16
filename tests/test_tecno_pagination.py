"""Tests for the paginated TECNO 141-model DUMP library.

The library used to render all 141 models inside a single inline keyboard,
which Telegram rejects (too many buttons) so the menu never opened. The list
is now split into pages of ``TECNO_PAGE_SIZE`` models with previous/next
navigation, and every dump card sends the user back to the page they came
from.
"""

import unittest
from types import SimpleNamespace
from unittest.mock import patch

import main

PAGE_SIZE = 20
EXPECTED_TOTAL_PAGES = 8  # ceil(141 / 20)


class TecnoPaginationLayoutTests(unittest.TestCase):
    def test_page_size_is_twenty_models(self):
        self.assertEqual(main.TECNO_PAGE_SIZE, PAGE_SIZE)

    def test_every_page_holds_at_most_twenty_models(self):
        _, total_pages, _ = main.hmax_tecno_page_items(1)
        self.assertEqual(total_pages, EXPECTED_TOTAL_PAGES)
        for page in range(1, total_pages + 1):
            with self.subTest(page=page):
                _, _, items = main.hmax_tecno_page_items(page)
                self.assertTrue(items)
                self.assertLessEqual(len(items), PAGE_SIZE)

    def test_pages_cover_every_model_exactly_once(self):
        _, total_pages, _ = main.hmax_tecno_page_items(1)
        seen = []
        for page in range(1, total_pages + 1):
            _, _, items = main.hmax_tecno_page_items(page)
            seen.extend(key for key, _ in items)
        self.assertEqual(seen, list(main.TECNO_DUMPS.keys()))
        self.assertEqual(len(seen), 141)

    def test_first_page_starts_at_the_first_model(self):
        page, _, items = main.hmax_tecno_page_items(1)
        keys = list(main.TECNO_DUMPS.keys())
        self.assertEqual(page, 1)
        self.assertEqual([key for key, _ in items], keys[:PAGE_SIZE])

    def test_last_page_holds_the_remainder(self):
        _, total_pages, _ = main.hmax_tecno_page_items(1)
        _, _, items = main.hmax_tecno_page_items(total_pages)
        keys = list(main.TECNO_DUMPS.keys())
        self.assertEqual(len(items), len(keys) - PAGE_SIZE * (total_pages - 1))
        self.assertEqual(items[-1][0], keys[-1])

    def test_out_of_range_pages_are_clamped(self):
        _, total_pages, _ = main.hmax_tecno_page_items(1)
        self.assertEqual(main.hmax_tecno_page_items(0)[0], 1)
        self.assertEqual(main.hmax_tecno_page_items(-5)[0], 1)
        self.assertEqual(main.hmax_tecno_page_items(999)[0], total_pages)
        self.assertEqual(main.hmax_tecno_page_items("3")[0], 3)
        self.assertEqual(main.hmax_tecno_page_items("not-a-page")[0], 1)
        self.assertEqual(main.hmax_tecno_page_items(None)[0], 1)

    def test_page_size_must_be_positive(self):
        with self.assertRaises(ValueError):
            main.hmax_tecno_page_items(1, page_size=0)

    def test_page_for_model_lookup(self):
        keys = list(main.TECNO_DUMPS.keys())
        self.assertEqual(main.hmax_tecno_page_for_model(keys[0]), 1)
        self.assertEqual(main.hmax_tecno_page_for_model(keys[PAGE_SIZE - 1]), 1)
        self.assertEqual(main.hmax_tecno_page_for_model(keys[PAGE_SIZE]), 2)
        self.assertEqual(main.hmax_tecno_page_for_model(keys[-1]), EXPECTED_TOTAL_PAGES)
        self.assertEqual(main.hmax_tecno_page_for_model("missing-model"), 1)

    def test_page_header_shows_the_page_counter(self):
        text = main.hmax_tecno_page_text(3, EXPECTED_TOTAL_PAGES)
        self.assertIn("TECNO - 141 Model", text)
        self.assertIn("صفحة 3 / 8", text)
        self.assertIn(f"حتى {PAGE_SIZE} موديل في الصفحة", text)


class TecnoPaginationCallbackTests(unittest.TestCase):
    def _render(self, data):
        """Run the callback and return (text, inline buttons) of the render."""
        call = SimpleNamespace(
            id="callback-tecno",
            data=data,
            message=SimpleNamespace(
                chat=SimpleNamespace(id=123),
                message_id=456,
            ),
        )

        with (
            patch("main.hmaxx.allow_user", return_value=True),
            patch("main.hmaxi18n.bind_callback"),
            patch("main.increment_click"),
            patch("main.bot.answer_callback_query"),
            patch("main._hmax_show_menu") as show_menu,
        ):
            main.callback_inline(call)

        show_menu.assert_called_once()
        _, text, markup = show_menu.call_args.args
        buttons = [button for row in markup.keyboard for button in row]
        return text, buttons

    @staticmethod
    def _navigation(buttons):
        return [b for b in buttons if b.callback_data.startswith("dump_tecno_page_")]

    @staticmethod
    def _models(buttons):
        return [b for b in buttons if b.callback_data.startswith("dump_model_")]

    def test_first_page_lists_twenty_models_and_a_next_button(self):
        text, buttons = self._render("dump_tecno_full_section")
        keys = list(main.TECNO_DUMPS.keys())

        models = self._models(buttons)
        self.assertEqual(len(models), PAGE_SIZE)
        self.assertEqual(models[0].callback_data, f"dump_model_{keys[0]}")
        self.assertIn(main.TECNO_DUMPS[keys[0]]["name"], models[0].text)
        self.assertEqual(models[-1].callback_data, f"dump_model_{keys[PAGE_SIZE - 1]}")

        navigation = self._navigation(buttons)
        self.assertEqual(len(navigation), 1)
        self.assertIn("التالي", navigation[0].text)
        self.assertEqual(navigation[0].callback_data, "dump_tecno_page_2")
        self.assertIn("صفحة 1 / 8", text)

    def test_middle_page_has_previous_and_next_buttons(self):
        text, buttons = self._render("dump_tecno_page_4")
        keys = list(main.TECNO_DUMPS.keys())

        models = self._models(buttons)
        self.assertEqual(len(models), PAGE_SIZE)
        self.assertEqual(models[0].callback_data, f"dump_model_{keys[PAGE_SIZE * 3]}")

        navigation = self._navigation(buttons)
        self.assertEqual(
            [(b.text, b.callback_data) for b in navigation],
            [("⬅️ السابق", "dump_tecno_page_3"), ("➡️ التالي", "dump_tecno_page_5")],
        )
        self.assertIn("صفحة 4 / 8", text)

    def test_last_page_has_only_a_previous_button(self):
        _, buttons = self._render("dump_tecno_page_8")
        keys = list(main.TECNO_DUMPS.keys())

        models = self._models(buttons)
        self.assertEqual(len(models), len(keys) - PAGE_SIZE * 7)
        self.assertEqual(models[-1].callback_data, f"dump_model_{keys[-1]}")

        navigation = self._navigation(buttons)
        self.assertEqual(len(navigation), 1)
        self.assertIn("السابق", navigation[0].text)
        self.assertEqual(navigation[0].callback_data, "dump_tecno_page_7")

    def test_out_of_range_page_callback_opens_the_last_page(self):
        _, buttons = self._render("dump_tecno_page_999")
        keys = list(main.TECNO_DUMPS.keys())
        self.assertEqual(self._models(buttons)[-1].callback_data, f"dump_model_{keys[-1]}")

    def test_back_button_returns_to_the_dump_brand_menu(self):
        for data in ("dump_tecno_full_section", "dump_tecno_page_5"):
            with self.subTest(data=data):
                _, buttons = self._render(data)
                back = [
                    b
                    for b in buttons
                    if b.callback_data == "dump_main_section"
                ]
                self.assertEqual(len(back), 1)

    def test_model_buttons_never_exceed_telegrams_button_limit(self):
        _, buttons = self._render("dump_tecno_full_section")
        self.assertLessEqual(len(buttons), 23)  # 20 models + navigation + back

    def test_page_callbacks_are_handled_by_the_tecno_section(self):
        """Guard against dangling targets (see test_dump_back_navigation)."""
        from pathlib import Path

        source = (Path(__file__).resolve().parents[1] / "main.py").read_text(
            encoding="utf-8"
        )
        self.assertIn('cd.startswith("dump_tecno_page_")', source)
        self.assertIn('callback_data=f"dump_tecno_page_{', source)


class TecnoModelCardBackButtonTests(unittest.TestCase):
    def test_dump_card_returns_to_the_page_that_lists_the_model(self):
        key = list(main.TECNO_DUMPS)[PAGE_SIZE * 2 + 3]  # a model on page 3
        call = SimpleNamespace(
            id="callback-tecno-model",
            data=f"dump_model_{key}",
            message=SimpleNamespace(
                chat=SimpleNamespace(id=123),
                message_id=456,
            ),
        )

        with (
            patch("main.hmaxx.allow_user", return_value=True),
            patch("main.hmaxi18n.bind_callback"),
            patch("main.increment_click"),
            patch("main.bot.answer_callback_query"),
            patch("main.bot.delete_message"),
            patch("main.bot.send_message") as send_message,
        ):
            main.callback_inline(call)

        buttons = [
            button
            for row in send_message.call_args.kwargs["reply_markup"].keyboard
            for button in row
        ]
        self.assertEqual(buttons[0].url, main.TECNO_DUMPS[key]["url"])
        self.assertEqual(buttons[1].callback_data, "dump_tecno_page_3")


if __name__ == "__main__":
    unittest.main()
