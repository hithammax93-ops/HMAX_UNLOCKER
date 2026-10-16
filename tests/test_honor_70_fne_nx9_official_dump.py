import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import main

CARD_CALLBACK = "dump_model_fne_nx9_official"
CARD_LABEL = "🔥 HONOR 70 FNE-NX9 - Official FREE"
DRIVE_URL = "https://drive.google.com/file/d/1sPDlg3-8j4OiL12Zh1DZNHF4Y5mHNjJd/view"
POSTER = "honor_70_fne-nx9_official_hmax.jpg"


class Honor70FneNx9OfficialDumpTests(unittest.TestCase):
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

    def test_honor_section_offers_the_official_card_and_keeps_old_buttons(self):
        call = self._call("dump_honor_section")
        with (
            patch("main.hmaxx.allow_user", return_value=True),
            patch("main.hmaxi18n.bind_callback"),
            patch("main.bot.answer_callback_query"),
            patch("main.bot.edit_message_text") as edit_message_text,
        ):
            main.callback_inline(call)

        edit_message_text.assert_called_once()
        buttons = self._buttons(edit_message_text.call_args.kwargs["reply_markup"])
        callbacks = [button.callback_data for button in buttons]
        self.assertIn(CARD_CALLBACK, callbacks)
        card_button = next(b for b in buttons if b.callback_data == CARD_CALLBACK)
        self.assertEqual(card_button.text, CARD_LABEL)
        # The pre-existing HONOR entries must survive the new card.
        for kept in (
            "dump_model_honor_x7a_rky_lx2_2gb",
            "dump_model_honor_x9c_full_dump",
            "dump_huawei_honor_section",
            "dump_main_section",
        ):
            self.assertIn(kept, callbacks)

    def test_card_sends_the_poster_caption_download_and_back_buttons(self):
        expected_photo = Path(__file__).resolve().parents[1] / "images" / POSTER
        self.assertTrue(expected_photo.is_file())
        call = self._call(CARD_CALLBACK)

        with (
            patch("main.hmaxx.allow_user", return_value=True),
            patch("main.hmaxi18n.bind_callback"),
            patch("main.bot.answer_callback_query"),
            patch("main.bot.delete_message") as delete_message,
            patch("main.bot.send_photo") as send_photo,
            patch("main.bot.send_message") as send_message,
        ):
            main.callback_inline(call)

        delete_message.assert_called_once_with(chat_id=123, message_id=456)
        send_photo.assert_called_once()
        send_message.assert_not_called()
        self.assertEqual(Path(send_photo.call_args.args[1].name), expected_photo)

        caption = send_photo.call_args.kwargs["caption"]
        for detail in (
            "HONOR 70 — FNE-NX9 — Official Firmware",
            "FNE-N29_def_meafnaf_8.0.0.292_C185E7R2P1",
            "MagicOS: 8.0_0501AAEM",
            "Password: MobiFirmware.VIP",
            "HMAX-UNLOCKER - HithamMax",
        ):
            self.assertIn(detail, caption)

        buttons = self._buttons(send_photo.call_args.kwargs["reply_markup"])
        self.assertEqual([b.url for b in buttons], [DRIVE_URL, None])
        self.assertEqual(buttons[0].text, "📥 Download")
        self.assertEqual(buttons[1].callback_data, "dump_honor_section")

    def test_card_finds_the_poster_from_any_working_directory(self):
        # The poster path is anchored to the repository, not the process cwd.
        call = self._call(CARD_CALLBACK)
        previous_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)
            try:
                with (
                    patch("main.hmaxx.allow_user", return_value=True),
                    patch("main.hmaxi18n.bind_callback"),
                    patch("main.bot.answer_callback_query"),
                    patch("main.bot.delete_message"),
                    patch("main.bot.send_photo") as send_photo,
                    patch("main.bot.send_message") as send_message,
                ):
                    main.callback_inline(call)
            finally:
                os.chdir(previous_cwd)

        send_photo.assert_called_once()
        send_message.assert_not_called()


if __name__ == "__main__":
    unittest.main()
