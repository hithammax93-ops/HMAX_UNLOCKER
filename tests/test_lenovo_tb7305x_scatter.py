import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import main


DRIVE_ID = "1B5VzL2H1A51NQ33_H6C8vDywObFolbz7"
POSTER = "lenovo_tb_7305x_scatter_hmax.jpg"


class LenovoTb7305xScatterTests(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        for name, kwargs in (
            ("hmaxx.allow_user", {"return_value": True}),
            ("hmaxi18n.bind_callback", {}),
            ("bot.answer_callback_query", {}),
            ("bot.delete_message", {}),
        ):
            self.stack.enter_context(patch("main." + name, **kwargs))

    def call(self, data, lang="ar"):
        with patch("main.hmaxi18n.get_language", return_value=lang):
            main.callback_inline(SimpleNamespace(
                id="test",
                data=data,
                message=SimpleNamespace(chat=SimpleNamespace(id=123), message_id=456),
            ))

    @staticmethod
    def buttons(mock):
        return [b for row in mock.call_args.kwargs["reply_markup"].keyboard for b in row]

    def test_poster_is_present(self):
        poster = Path(__file__).resolve().parents[1] / "images" / POSTER
        self.assertTrue(poster.is_file())

    def test_button_listed_in_other_section_for_each_language(self):
        for lang in ("ar", "en", "fr"):
            with self.subTest(lang=lang):
                with patch("main.bot.edit_message_text") as edit, \
                        patch("main.bot.send_message") as send:
                    self.call("dump_other_full_section", lang)
                    mock = edit if edit.called else send
                    buttons = self.buttons(mock)
                    callbacks = [b.callback_data for b in buttons]
                    self.assertEqual(callbacks.count("dump_lenovo_tb_7305x"), 1)
                    label = next(b.text for b in buttons
                                 if b.callback_data == "dump_lenovo_tb_7305x")
                    self.assertIn("TB-7305X", label)

    def test_model_card_has_drive_link_and_back_button(self):
        for lang in ("ar", "en", "fr"):
            with self.subTest(lang=lang):
                with patch("main.bot.send_photo") as photo, \
                        patch("main.bot.send_message") as send:
                    self.call("dump_lenovo_tb_7305x", lang)
                    mock = photo if photo.called else send
                    caption = mock.call_args.kwargs.get("caption") or mock.call_args.args[1]
                    self.assertIn("TB-7305X", caption)
                    self.assertIn("SP Flash Tool", caption)
                    self.assertIn("MobiFirmware.VIP", caption)
                    buttons = self.buttons(mock)
                    self.assertTrue(any(b.url and DRIVE_ID in b.url for b in buttons))
                    self.assertTrue(any(b.callback_data == "dump_other_full_section"
                                        for b in buttons))


if __name__ == "__main__":
    unittest.main()
