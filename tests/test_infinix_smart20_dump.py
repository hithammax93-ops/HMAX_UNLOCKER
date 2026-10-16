import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import main


CALLBACK = "dump_model_x6840b_full_dump"


class InfinixSmart20DumpTests(unittest.TestCase):
    def setUp(self):
        for target, kwargs in (
            ("main.hmaxx.allow_user", {"return_value": True}),
            ("main.hmaxi18n.bind_callback", {}),
            ("main.bot.answer_callback_query", {}),
            ("main.bot.delete_message", {}),
            ("main.bot.send_photo", {}),
            ("main.bot.send_message", {}),
            ("main.bot.edit_message_text", {}),
        ):
            patcher = patch(target, **kwargs)
            setattr(self, target.rsplit(".", 1)[1], patcher.start())
            self.addCleanup(patcher.stop)

    def invoke(self, callback=CALLBACK):
        main.callback_inline(SimpleNamespace(
            id="test-callback", data=callback,
            message=SimpleNamespace(chat=SimpleNamespace(id=123), message_id=456),
        ))

    def test_card_is_available_in_both_infinix_menus(self):
        for menu in ("dump_infinix_section", "dump_infinix_full_section"):
            with self.subTest(menu=menu):
                self.invoke(menu)
                buttons = self.edit_message_text.call_args.kwargs["reply_markup"].keyboard
                self.assertEqual(sum(b.callback_data == CALLBACK for row in buttons for b in row), 1)

    def test_photo_caption_and_buttons(self):
        self.invoke()
        self.send_photo.assert_called_once()
        self.send_message.assert_not_called()
        photo = self.send_photo.call_args.args[1]
        self.assertEqual(Path(photo.name), Path(main.__file__).resolve().parent / "images" / "infinix_smart20_x6840b_dump_hmax.jpg")
        caption = self.send_photo.call_args.kwargs["caption"]
        for detail in ("Smart 20", "X6840B", "16.1.0.150SP02", "OP001PF001AZ",
                       "FULL DUMP", "READBACK FROM DEVICE", "UnlockTool",
                       "Model & Build", "Full Backup", "Network / Calibration Files",
                       "MobiFirmware.VIP", "HMAX-UNLOCKER - HithamMax"):
            self.assertIn(detail, caption)
        self.assertLessEqual(len(caption.encode("utf-16-le")) // 2, 1024)
        buttons = [b for row in self.send_photo.call_args.kwargs["reply_markup"].keyboard for b in row]
        self.assertEqual(buttons[0].url, "https://drive.google.com/file/d/1AZywXmJEL1BBJaB3Cx5KF7iE7G3c2RqS/view")
        self.assertEqual(buttons[1].callback_data, "dump_infinix_section")

    def test_missing_photo_falls_back_to_text(self):
        with patch("builtins.open", side_effect=FileNotFoundError("missing poster")):
            self.invoke()
        self.send_photo.assert_not_called()
        self.send_message.assert_called_once()
        self.assertIn("X6840B", self.send_message.call_args.args[1])

    def test_photo_api_failure_falls_back_to_same_text_and_buttons(self):
        self.send_photo.side_effect = RuntimeError("Telegram photo failure")
        self.invoke()
        self.send_message.assert_called_once_with(
            123, self.send_photo.call_args.kwargs["caption"],
            reply_markup=self.send_photo.call_args.kwargs["reply_markup"],
        )

    def test_callback_and_delete_failures_do_not_block_photo(self):
        self.answer_callback_query.side_effect = RuntimeError("expired callback")
        self.delete_message.side_effect = RuntimeError("message already deleted")
        self.invoke()
        self.delete_message.assert_called_once()
        self.send_photo.assert_called_once()


if __name__ == "__main__":
    unittest.main()
