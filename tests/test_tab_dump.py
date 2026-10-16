"""Regression tests for the merged TAB library and its tablet dump cards."""

import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import main


class TabDumpTests(unittest.TestCase):
    SECTION_CALLBACK = "dump_tab_section"
    A9_CALLBACK = "dump_model_tab_a9_sm_x110"
    LEGACY_A9_CALLBACK = "dump_model_samsung_tab_a9_sm_x110"
    OTEETO_CALLBACK = "dump_model_the_oteeto_tab_15_full_dump_cm2"
    CARDS = {
        A9_CALLBACK: {
            "photo": "samsung_tab_a9_sm_x110_full_dump.jpg",
            "url": "https://drive.google.com/file/d/199DEolDruK6iP3oh6iGJ9XkOJWJsDqil/view",
            "details": (
                "Samsung Galaxy Tab A9", "SM-X110", "X110XXS6CYI3",
                "FULL DUMP", "UnlockTool", "DUMPING-FIRMWARE",
                "Google Drive", "MobiFirmware.VIP",
                "make sure SM-X110 and X110XXS6CYI3 match before writing",
            ),
        },
        OTEETO_CALLBACK: {
            "photo": "the_oteeto_tab_15_full_dump_cm2_rare.jpg",
            "url": "https://drive.google.com/file/d/19RaJLb3dnlcj3Wj9hdkg8I4aL-tUuHQY/view",
            "details": (
                "The Oteeto TAB 15", "FULL DUMP", "CM2", "Google Drive",
                "MobiFirmware.VIP", "A very rare file", "made for technicians",
                "HMAX-UNLOCKER HithamMax",
            ),
        },
    }

    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        for name, kwargs in (
            ("hmaxx.allow_user", {"return_value": True}),
            ("hmaxi18n.bind_callback", {}),
            ("hmaxi18n.get_language", {"return_value": "en"}),
            ("is_user_banned", {"return_value": False}),
            ("increment_click", {}),
        ):
            self.stack.enter_context(patch("main." + name, **kwargs))
        for name in (
            "answer_callback_query", "delete_message", "edit_message_text",
            "send_photo", "send_message",
        ):
            setattr(self, name, self.stack.enter_context(patch("main.bot." + name)))

    def _call(self, callback_data):
        main.callback_inline(SimpleNamespace(
            id="callback-tab-test",
            data=callback_data,
            message=SimpleNamespace(
                chat=SimpleNamespace(id=123),
                message_id=456,
            ),
        ))

    @staticmethod
    def _buttons(mock):
        return [
            button
            for row in mock.call_args.kwargs["reply_markup"].keyboard
            for button in row
        ]

    def _reset_bot_mocks(self):
        for name in (
            "answer_callback_query", "delete_message", "edit_message_text",
            "send_photo", "send_message",
        ):
            getattr(self, name).reset_mock()

    def _assert_card(self, mock, card, text_only=False):
        caption = mock.call_args.args[1] if text_only else mock.call_args.kwargs["caption"]
        # Telegram's photo caption limit counts UTF-16 code units.
        self.assertLessEqual(len(caption.encode("utf-16-le")) // 2, 1024)
        for detail in card["details"]:
            self.assertIn(detail, caption)
        buttons = self._buttons(mock)
        self.assertEqual(len(buttons), 2)
        self.assertEqual(buttons[0].url, card["url"])
        self.assertEqual(buttons[-1].text, "⬅️ Back to TAB")
        self.assertEqual(buttons[-1].callback_data, self.SECTION_CALLBACK)

    def test_dump_menu_replaces_ytab_with_tab_in_all_languages(self):
        for language in ("ar", "en", "fr"):
            with self.subTest(language=language), patch(
                "main.hmaxi18n.get_language", return_value=language
            ):
                self._reset_bot_mocks()
                self._call("dump_main_section")
                self.edit_message_text.assert_called_once()
                buttons = self._buttons(self.edit_message_text)
                callbacks = [button.callback_data for button in buttons]
                self.assertEqual(callbacks.count(self.SECTION_CALLBACK), 1)
                self.assertNotIn("dump_ytab_section", callbacks)
                tab = next(button for button in buttons if button.callback_data == self.SECTION_CALLBACK)
                self.assertEqual(tab.text, "📱 TAB")
                self.assertEqual(buttons[-1].callback_data, "menu_systems_section")

    def test_tab_menu_lists_ytab_a9_and_oteeto(self):
        self._call(self.SECTION_CALLBACK)

        self.edit_message_text.assert_called_once()
        self.answer_callback_query.assert_called_once_with("callback-tab-test")
        buttons = self._buttons(self.edit_message_text)
        self.assertEqual(
            [(button.text, button.callback_data) for button in buttons],
            [
                ("📱 YTAB - Library", "dump_ytab_section"),
                ("📱 TAB A9 SM-X110", self.A9_CALLBACK),
                ("🔥 The Oteeto TAB 15 - FULL DUMP [CM2] RARE", self.OTEETO_CALLBACK),
                ("⬅️ Back to DUMP", "dump_main_section"),
            ],
        )
        self.assertIn("YTAB + TAB A9 + Oteeto", self.edit_message_text.call_args.args[0])
        self.send_message.assert_not_called()

    def test_tablet_menus_can_be_opened_from_photo_cards(self):
        self.edit_message_text.side_effect = RuntimeError("no text in photo message")
        for callback, parent in (
            (self.SECTION_CALLBACK, "dump_main_section"),
            ("dump_ytab_section", self.SECTION_CALLBACK),
        ):
            with self.subTest(callback=callback):
                self._reset_bot_mocks()
                self._call(callback)
                self.delete_message.assert_called_once_with(chat_id=123, message_id=456)
                self.send_message.assert_called_once()
                self.assertEqual(self._buttons(self.send_message)[-1].callback_data, parent)

    def test_tab_a9_is_moved_out_of_the_samsung_menu_in_all_languages(self):
        for language in ("ar", "en", "fr"):
            with self.subTest(language=language), patch(
                "main.hmaxi18n.get_language", return_value=language
            ):
                self._call("dump_scatter_samsung")
                callbacks = [button.callback_data for button in self._buttons(self.edit_message_text)]
                self.assertNotIn(self.A9_CALLBACK, callbacks)
                self.assertNotIn(self.LEGACY_A9_CALLBACK, callbacks)
                for callback in ("dump_a146u1", "dump_a075f", "dump_x216b_xxud", "dump_a125f", "dump_a256e"):
                    self.assertIn(callback, callbacks)

    def test_cards_send_original_posters_details_and_download_links(self):
        for callback, card in self.CARDS.items():
            with self.subTest(callback=callback):
                self._reset_bot_mocks()
                photo = Path(__file__).resolve().parents[1] / "images" / card["photo"]
                self.assertTrue(photo.is_file())
                self._call(callback)
                self.answer_callback_query.assert_called_once_with("callback-tab-test")
                self.delete_message.assert_called_once_with(chat_id=123, message_id=456)
                self.send_photo.assert_called_once()
                self.assertEqual(Path(self.send_photo.call_args.args[1].name), photo)
                self.send_message.assert_not_called()
                self._assert_card(self.send_photo, card)

    def test_legacy_tab_a9_callback_sends_the_same_card(self):
        self._call(self.A9_CALLBACK)
        caption = self.send_photo.call_args.kwargs["caption"]
        markup = self.send_photo.call_args.kwargs["reply_markup"].to_dict()
        photo = self.send_photo.call_args.args[1].name
        self._reset_bot_mocks()

        self._call(self.LEGACY_A9_CALLBACK)

        self.send_photo.assert_called_once()
        self.assertEqual(self.send_photo.call_args.kwargs["caption"], caption)
        self.assertEqual(self.send_photo.call_args.kwargs["reply_markup"].to_dict(), markup)
        self.assertEqual(self.send_photo.call_args.args[1].name, photo)
        self._assert_card(self.send_photo, self.CARDS[self.A9_CALLBACK])

    def test_cards_fall_back_to_text_when_photo_send_fails(self):
        self.send_photo.side_effect = RuntimeError("photo failed")
        for callback, card in self.CARDS.items():
            with self.subTest(callback=callback):
                self._reset_bot_mocks()
                self._call(callback)
                self.send_photo.assert_called_once()
                self.send_message.assert_called_once()
                self._assert_card(self.send_message, card, text_only=True)

    def test_cards_fall_back_to_text_when_poster_is_missing(self):
        with patch("main.open", side_effect=FileNotFoundError("poster missing")):
            for callback, card in self.CARDS.items():
                with self.subTest(callback=callback):
                    self._reset_bot_mocks()
                    self._call(callback)
                    self.send_photo.assert_not_called()
                    self.send_message.assert_called_once()
                    self._assert_card(self.send_message, card, text_only=True)

    def test_cards_still_send_if_callback_acknowledgement_or_deletion_fails(self):
        for failed_method in (self.answer_callback_query, self.delete_message):
            failed_method.side_effect = RuntimeError("Telegram request failed")
            try:
                for callback, card in self.CARDS.items():
                    with self.subTest(method=failed_method, callback=callback):
                        self._reset_bot_mocks()
                        self._call(callback)
                        self.delete_message.assert_called_once_with(chat_id=123, message_id=456)
                        self.send_photo.assert_called_once()
                        self._assert_card(self.send_photo, card)
            finally:
                failed_method.side_effect = None

    def test_oteeto_back_button_restores_the_tab_menu(self):
        self._call(self.OTEETO_CALLBACK)
        back = self._buttons(self.send_photo)[-1].callback_data
        self.edit_message_text.side_effect = RuntimeError("no text in photo message")

        self._call(back)

        self.send_message.assert_called_once()
        callbacks = [button.callback_data for button in self._buttons(self.send_message)]
        self.assertEqual(callbacks, ["dump_ytab_section", self.A9_CALLBACK, self.OTEETO_CALLBACK, "dump_main_section"])

    def test_callback_data_stays_within_the_telegram_limit(self):
        for callback in (
            self.SECTION_CALLBACK, self.A9_CALLBACK, self.LEGACY_A9_CALLBACK,
            self.OTEETO_CALLBACK, "dump_ytab_section",
        ):
            with self.subTest(callback=callback):
                self.assertGreater(len(callback.encode("utf-8")), 0)
                self.assertLessEqual(len(callback.encode("utf-8")), 64)


if __name__ == "__main__":
    unittest.main()
