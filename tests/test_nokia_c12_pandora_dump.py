import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import main


class NokiaC12DumpTests(unittest.TestCase):
    @staticmethod
    def make_call(callback_data):
        return SimpleNamespace(
            id="callback-nokia-c12",
            data=callback_data,
            message=SimpleNamespace(
                chat=SimpleNamespace(id=123),
                message_id=456,
            ),
        )

    def test_nokia_menu_includes_c12_options_and_keeps_existing_models(self):
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
        self.assertIn("dump_nokia_c12_ta1583_pandora", callbacks)
        self.assertIn("dump_nokia_c12_ta1583_cm2", callbacks)
        self.assertIn("dump_model_nokia_c10_ta_1342", callbacks)
        self.assertIn("dump_nokia_g21", callbacks)
        self.assertIn("dump_main_section", callbacks)

    def test_c12_pandora_card_sends_photo_caption_and_download_buttons(self):
        call = self.make_call("dump_nokia_c12_ta1583_pandora")

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
        send_message.assert_not_called()
        photo = send_photo.call_args.args[1]
        self.assertEqual(Path(photo.name).name, "nokia_c12_ta1583_pandora_hmax.jpg")

        caption = send_photo.call_args.kwargs["caption"]
        for detail in (
            "C12 | TA-1583",
            "00WW_1_54B_SP01",
            "PANDORA TOOL",
            "CM2",
            "File Size: 2 GB",
            "Google Drive",
            "MobiFirmware.VIP",
            "NETWORK BACKUP",
            "SLOT A / B",
        ):
            self.assertIn(detail, caption)
        self.assertLessEqual(len(caption), 1024)

        buttons = [
            button
            for row in send_photo.call_args.kwargs["reply_markup"].keyboard
            for button in row
        ]
        self.assertEqual(
            buttons[0].url,
            "https://drive.google.com/file/d/1S9_2MsbRY3hfhFEnvHmdCERLWh0GxCSH/view",
        )
        self.assertEqual(buttons[1].callback_data, "dump_nokia_section")

    def test_c12_cm2_option_has_a_back_button_until_dump_details_are_added(self):
        call = self.make_call("dump_nokia_c12_ta1583_cm2")

        with (
            patch("main.hmaxx.allow_user", return_value=True),
            patch("main.hmaxi18n.bind_callback"),
            patch("main.bot.answer_callback_query"),
            patch("main.bot.delete_message"),
            patch("main.bot.send_message") as send_message,
        ):
            main.callback_inline(call)

        send_message.assert_called_once()
        self.assertIn("not available yet", send_message.call_args.args[1])
        keyboard = send_message.call_args.kwargs["reply_markup"].keyboard
        buttons = [button for row in keyboard for button in row]
        self.assertEqual(buttons[0].callback_data, "dump_nokia_section")


if __name__ == "__main__":
    unittest.main()
