import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import main


class BencoHisorlDumpTests(unittest.TestCase):
    BRANDS = {
        "dump_benco_section": {
            "label": "📱 BENCO",
            "model_callback": "dump_model_benco_v60_full",
            "model_label": "🔥 V60 Full Dump [CM2]",
            "device": "Benco V60",
            "drive_url": "https://drive.google.com/file/d/1IWj92n5541TYoYKXe-sC9eyNkbsrte6f/view",
            "photo": "benco_v60_full_dump_cm2.jpg",
            "caption_details": ("Read By: CM2", "Full Dump", "MobiFirmware.VIP"),
        },
        "dump_hisorl_section": {
            "label": "📱 HISORL",
            "model_callback": "dump_model_hisorl_t901_full",
            "model_label": "🔥 T901 Full Dump [UnlockTool]",
            "device": "HISORL T901",
            "drive_url": "https://drive.google.com/file/d/1IQMjflRd0asfRQl3_z2PaCu6FeAxvzyO/view",
            "photo": "hisorl_t901_full_dump_unlocktool.jpg",
            "caption_details": (
                "Full Dump",
                "UnlockTool",
                "Google Drive",
                "MobiFirmware.VIP",
                "ĶĦălěď Ķäbô",
            ),
        },
    }

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

    def test_dump_menu_has_benco_and_hisorl_buttons(self):
        call = self._call("dump_main_section")
        with (
            patch("main.hmaxx.allow_user", return_value=True),
            patch("main.hmaxi18n.bind_callback"),
            patch("main.hmaxi18n.get_language", return_value="en"),
            patch("main.bot.answer_callback_query"),
            patch("main.bot.edit_message_text") as edit_message_text,
        ):
            main.callback_inline(call)

        edit_message_text.assert_called_once()
        buttons = self._buttons(edit_message_text.call_args.kwargs["reply_markup"])
        button_by_callback = {button.callback_data: button for button in buttons}
        for callback_data, details in self.BRANDS.items():
            with self.subTest(brand=callback_data):
                button = button_by_callback[callback_data]
                self.assertEqual(button.text, details["label"])

    def test_brand_sections_offer_the_model_and_back_to_dump_menu(self):
        for section_callback, details in self.BRANDS.items():
            with self.subTest(brand=section_callback):
                call = self._call(section_callback)
                with (
                    patch("main.hmaxx.allow_user", return_value=True),
                    patch("main.hmaxi18n.bind_callback"),
                    patch("main.bot.answer_callback_query"),
                    patch("main.bot.edit_message_text") as edit_message_text,
                ):
                    main.callback_inline(call)

                edit_message_text.assert_called_once()
                self.assertIn(details["label"].split()[-1], edit_message_text.call_args.args[0])
                buttons = self._buttons(edit_message_text.call_args.kwargs["reply_markup"])
                self.assertEqual(buttons[0].text, details["model_label"])
                self.assertEqual(buttons[0].callback_data, details["model_callback"])
                self.assertEqual(buttons[-1].callback_data, "dump_main_section")

    def test_dump_cards_send_the_poster_caption_download_and_brand_back_button(self):
        root = Path(__file__).resolve().parents[1]
        for section_callback, details in self.BRANDS.items():
            with self.subTest(brand=section_callback):
                expected_photo = root / "images" / details["photo"]
                self.assertTrue(expected_photo.is_file())
                call = self._call(details["model_callback"])

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
                self.assertEqual(Path(send_photo.call_args.args[1].name), expected_photo)
                caption = send_photo.call_args.kwargs["caption"]
                self.assertIn(details["device"], caption)
                for detail in details["caption_details"]:
                    self.assertIn(detail, caption)

                buttons = self._buttons(send_photo.call_args.kwargs["reply_markup"])
                self.assertEqual(buttons[0].url, details["drive_url"])
                self.assertEqual(buttons[1].callback_data, section_callback)


if __name__ == "__main__":
    unittest.main()
