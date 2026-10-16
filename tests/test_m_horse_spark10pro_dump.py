"""Tests for the M-HORSE SPARK 10 Pro 3 versions full dump card.

The card lives in the M-HORSE library menu (``dump_m_horse_section``) and is
opened through ``dump_model_m_horse_spark_10_pro_full_dump_unlocktool``. It
offers three UnlockTool dumps (V02, V05, V06) and its back button must return
to the M-HORSE menu. The card text is longer than Telegram's 1024 UTF-16 code
unit photo-caption limit, so the poster is sent bare and the full text goes out
in a follow-up message carrying the buttons.
"""

import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import main


class MHorseSpark10ProDumpTests(unittest.TestCase):
    SECTION = "dump_m_horse_section"
    MODEL_CALLBACK = "dump_model_m_horse_spark_10_pro_full_dump_unlocktool"
    MODEL_LABEL = (
        "\U0001f525 M-HORSE SPARK 10 Pro - 3 VERSIONS FULL DUMP [UnlockTool]"
    )
    V02_URL = "https://drive.google.com/uc?id=1-AfazaipdbGg4z8vPomf-1EE62TfagfM"
    V05_URL = "https://drive.google.com/uc?id=1-KkjfZkiiLZnjNKwzuJLJcXFQcNB3xum"
    V06_URL = "https://drive.google.com/file/d/1tkQijRTWEyWqmiBx-23aiY-NOIw061sr/view"
    PHOTO = "m_horse_spark_10_pro_3_versions_full_dump_unlocktool.jpg"
    DETAILS_AR = (
        "M-HORSE-SPARK 10 Pro",
        "FULL DUMP",
        "UnlockTool",
        "SPARK 10 Pro M-HORSE-V02-20231027",
        "SPARK 10Pro-M-HORSE-V05-20240410",
        "SPARK 10Pro-M-HORSE-V06-20240716",
        "MobiFirmware.VIP",
        "HMAX hithamMax",
        "\u062d\u0645\u0627\u0647 \u0627\u0644\u0644\u0647 \u0639\u0628\u062f\u0627\u0644\u0645\u0627\u0644\u0643",
    )
    DETAILS = (
        "M-HORSE-SPARK 10 Pro",
        "FULL DUMP",
        "UnlockTool",
        "SPARK 10 Pro M-HORSE-V02-20231027",
        "SPARK 10Pro-M-HORSE-V05-20240410",
        "SPARK 10Pro-M-HORSE-V06-20240716",
        "MobiFirmware.VIP",
        "HMAX hithamMax",
        "Hamallah Abdelmalek",
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

    def test_card_sends_poster_then_full_text_with_all_download_links(self):
        self.stack.enter_context(patch("main.hmaxi18n.get_language", return_value="ar"))
        expected_photo = Path(__file__).resolve().parents[1] / "images" / self.PHOTO
        self.assertTrue(expected_photo.is_file())

        main.callback_inline(self._call(self.MODEL_CALLBACK))

        self.send_photo.assert_called_once()
        self.assertEqual(Path(self.send_photo.call_args.args[1].name), expected_photo)
        # The card text exceeds Telegram's 1024 UTF-16 code unit caption limit,
        # so the poster goes out bare and the full text is a follow-up message.
        self.assertNotIn("caption", self.send_photo.call_args.kwargs)

        self.send_message.assert_called_once()
        text = self.send_message.call_args.args[1]
        for detail in self.DETAILS_AR:
            self.assertIn(detail, text)

        buttons = self._buttons(self.send_message.call_args.kwargs["reply_markup"])
        self.assertEqual(
            [b.url for b in buttons[:3]],
            [self.V02_URL, self.V05_URL, self.V06_URL],
        )
        self.assertEqual(buttons[-1].callback_data, self.SECTION)

    def test_card_english_sends_one_caption_with_all_download_links(self):
        main.callback_inline(self._call(self.MODEL_CALLBACK))

        self.send_photo.assert_called_once()
        self.send_message.assert_not_called()
        caption = self.send_photo.call_args.kwargs["caption"]
        # The English card fits Telegram's 1024 UTF-16 code unit caption limit.
        self.assertLessEqual(len(caption.encode("utf-16-le")) // 2, 1024)
        for detail in self.DETAILS:
            self.assertIn(detail, caption)

    def test_card_falls_back_to_text_when_photo_fails(self):
        self.send_photo.side_effect = RuntimeError("photo failed")

        main.callback_inline(self._call(self.MODEL_CALLBACK))

        self.send_message.assert_called_once()
        text = self.send_message.call_args.args[1]
        for detail in self.DETAILS:
            self.assertIn(detail, text)
        buttons = self._buttons(self.send_message.call_args.kwargs["reply_markup"])
        self.assertEqual(
            [b.url for b in buttons[:3]],
            [self.V02_URL, self.V05_URL, self.V06_URL],
        )
        self.assertEqual(buttons[-1].callback_data, self.SECTION)


if __name__ == "__main__":
    unittest.main()
