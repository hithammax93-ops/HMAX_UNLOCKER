import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import main


class NokiaTA1380DumpTests(unittest.TestCase):
    @staticmethod
    def make_call(callback_data):
        return SimpleNamespace(
            id="callback-nokia-ta1380",
            data=callback_data,
            message=SimpleNamespace(
                chat=SimpleNamespace(id=123),
                message_id=456,
            ),
        )

    def test_nokia_menu_lists_the_c1_2nd_edition_card(self):
        call = self.make_call("dump_nokia_section")

        with (
            patch("main.hmaxx.allow_user", return_value=True),
            patch("main.hmaxi18n.bind_callback"),
            patch("main.bot.answer_callback_query"),
            patch("main.bot.edit_message_text") as edit_message_text,
        ):
            main.callback_inline(call)

        edit_message_text.assert_called_once()
        keyboard = edit_message_text.call_args.kwargs["reply_markup"].keyboard
        callbacks = [button.callback_data for row in keyboard for button in row]
        self.assertIn("dump_nokia_ta1380", callbacks)
        self.assertIn("dump_nokia_c12_ta1583_pandora", callbacks)
        self.assertIn("dump_nokia_c12_ta1583_cm2", callbacks)
        self.assertIn("dump_main_section", callbacks)

    def test_card_sends_poster_then_the_full_text_with_buttons(self):
        call = self.make_call("dump_nokia_ta1380")

        with (
            patch("main.hmaxx.allow_user", return_value=True),
            patch("main.hmaxi18n.bind_callback"),
            patch("main.bot.answer_callback_query"),
            patch("main.bot.delete_message"),
            patch("main.bot.send_photo") as send_photo,
            patch("main.bot.send_message") as send_message,
        ):
            main.callback_inline(call)

        send_photo.assert_called_once()
        self.assertEqual(Path(send_photo.call_args.args[1].name).name, "ta1380_hmax.jpg")
        # The card is longer than Telegram's 1024-char caption limit, so the
        # poster goes out bare and the text carries the buttons.
        self.assertNotIn("caption", send_photo.call_args.kwargs)

        send_message.assert_called_once()
        text = send_message.call_args.args[1]
        for detail in (
            "C1 2nd Edition – TA-1380",
            "TA-1380_SP7731E_HMD_Global_NOKIA_C1_2nd_Edition_OSv11_RP1A.201005.001_IRU",
            "SPD7731E",
            "Pandora Tool",
            "rom.json",
            "HMDSW_Irisumts-122H-0-00WW-B01_user-images.zip",
            "Slot A / Slot B",
            "HMAX-UNLOCKER - HithamMax",
        ):
            self.assertIn(detail, text)
        self.assertNotIn("{", text)
        self.assertNotIn("}", text)
        self.assertLessEqual(len(text), 4096)

        buttons = [
            button
            for row in send_message.call_args.kwargs["reply_markup"].keyboard
            for button in row
        ]
        self.assertEqual(
            buttons[0].url,
            "https://mirrors-hmd-1.lolinet.com/firmware/hmd/2021/irisumts/official/600WW/HMDSW_iru-122H-0-00WW-B01-user_devicekit.zip",
        )
        self.assertEqual(buttons[1].callback_data, "dump_nokia_section")

    def test_poster_file_exists(self):
        poster = Path(__file__).resolve().parents[1] / "images" / "ta1380_hmax.jpg"
        self.assertTrue(poster.is_file())


if __name__ == "__main__":
    unittest.main()
