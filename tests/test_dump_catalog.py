import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import main
from main import DUMP_SMART_SECTIONS, detect_brand


class DumpCatalogTests(unittest.TestCase):
    def test_vivo_is_detected_as_a_dump_brand(self):
        self.assertEqual(detect_brand("VIVO Y21D PD2510F"), "vivo")

    def test_vivo_y21d_is_listed_in_vivo_and_f64_sections(self):
        expected_entry = (
            "🔥 VIVO Y21D PD2510F - 256GB UFS | 8.2GB [F64 ULTRA]",
            "dump_model_vivo_y21d_pd2510f",
        )
        self.assertIn(expected_entry, DUMP_SMART_SECTIONS["vivo"])
        self.assertIn(expected_entry, DUMP_SMART_SECTIONS["jtag"])

    def test_vivo_y21d_poster_is_present(self):
        poster = Path(__file__).resolve().parents[1] / "images" / "vivo_y21d_pd2510f.png"
        self.assertTrue(poster.is_file())

    def test_vivo_y21d_callback_sends_caption_and_drive_buttons(self):
        call = SimpleNamespace(
            id="callback-1",
            data="dump_model_vivo_y21d_pd2510f",
            message=SimpleNamespace(
                chat=SimpleNamespace(id=123),
                message_id=456,
            ),
        )

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
        caption = send_photo.call_args.kwargs["caption"]
        for detail in (
            "VIVO Y21D",
            "PD2510F",
            "256GB UFS",
            "8.2 GB",
            "F64 ULTRA",
            "Reynold Bermil Leonido",
            "DUMPING-FIRMWARE",
            "Google Drive",
            "MobiFirmware.VIP",
        ):
            self.assertIn(detail, caption)

        buttons = [
            button
            for row in send_photo.call_args.kwargs["reply_markup"].keyboard
            for button in row
        ]
        self.assertEqual(
            buttons[0].url,
            "https://drive.google.com/file/d/18qzexyLM46cv_rsa9f04tvKZceTJjbJ2/view",
        )
        self.assertEqual(buttons[1].callback_data, "dump_vivo_full_section")


class VivoY03TDumpCatalogTests(unittest.TestCase):
    def test_vivo_y03t_is_detected_as_vivo_brand(self):
        self.assertEqual(detect_brand("VIVO Y03T PD2360F"), "vivo")

    def test_vivo_y03t_is_listed_in_vivo_and_f64_sections(self):
        expected_entry = (
            "🔥 VIVO Y03T PD2360F - 64GB eMMC | 4.9GB [F64 ULTRA]",
            "dump_model_vivo_y03t_pd2360f",
        )
        self.assertIn(expected_entry, DUMP_SMART_SECTIONS["vivo"])
        self.assertIn(expected_entry, DUMP_SMART_SECTIONS["jtag"])

    def test_vivo_y03t_poster_is_present(self):
        poster = Path(__file__).resolve().parents[1] / "images" / "vivo_y03t_pd2360f.png"
        self.assertTrue(poster.is_file())

    def test_vivo_y03t_callback_sends_caption_and_drive_buttons(self):
        call = SimpleNamespace(
            id="callback-y03t",
            data="dump_model_vivo_y03t_pd2360f",
            message=SimpleNamespace(
                chat=SimpleNamespace(id=123),
                message_id=456,
            ),
        )

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
        caption = send_photo.call_args.kwargs["caption"]
        for detail in (
            "VIVO Y03T",
            "PD2360F",
            "64GB eMMC",
            "PD2360F_EX_A_14.0.12.3.W20.V000L1",
            "4.9 GB",
            "F64 ULTRA",
            "Reynold Bermil Leonido",
            "DUMPING-FIRMWARE",
            "Google Drive",
            "MobiFirmware.VIP",
        ):
            self.assertIn(detail, caption)

        buttons = [
            button
            for row in send_photo.call_args.kwargs["reply_markup"].keyboard
            for button in row
        ]
        self.assertEqual(
            buttons[0].url,
            "https://drive.google.com/file/d/1S6oZd5TGZHOfT8Yt6QgeQoYKQ8gAuYJr/view",
        )
        self.assertEqual(buttons[1].callback_data, "dump_vivo_full_section")


class SamsungA12DumpCatalogTests(unittest.TestCase):
    def test_samsung_a12_poster_is_present(self):
        poster = Path(__file__).resolve().parents[1] / "images" / "samsung_a12_a125f.png"
        self.assertTrue(poster.is_file())

    def test_samsung_a12_callback_sends_caption_and_drive_buttons(self):
        call = SimpleNamespace(
            id="callback-1",
            data="dump_a125f",
            message=SimpleNamespace(
                chat=SimpleNamespace(id=123),
                message_id=456,
            ),
        )

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
        caption = send_photo.call_args.kwargs["caption"]
        for detail in (
            "SAMSUNG A12",
            "SM-A125F",
            "A125FXXS6CXJ1",
            "EASY JTAG PLUS",
            "1.5 GB",
            "Google Drive",
            "MobiFirmware.VIP",
        ):
            self.assertIn(detail, caption)

        buttons = [
            button
            for row in send_photo.call_args.kwargs["reply_markup"].keyboard
            for button in row
        ]
        self.assertEqual(
            buttons[0].url,
            "https://drive.google.com/file/d/1RegTQJUux_RdrozEtt9eFR2bmECEnFq3/view",
        )
        self.assertEqual(buttons[1].callback_data, "dump_scatter_samsung")


class SamsungA25DumpCatalogTests(unittest.TestCase):
    def test_samsung_a25_is_listed_in_f64_ultra_section(self):
        expected_entry = (
            "🔥 SAMSUNG A25 5G SM-A256E - 128GB UFS | 4.5GB [F64 ULTRA]",
            "dump_a256e",
        )
        self.assertIn(expected_entry, DUMP_SMART_SECTIONS["jtag"])

    def test_samsung_dump_menu_lists_a256e_in_all_languages(self):
        for lang in ("ar", "en", "fr"):
            with self.subTest(lang=lang):
                call = SimpleNamespace(
                    id="callback-a25-menu",
                    data="dump_scatter_samsung",
                    message=SimpleNamespace(
                        chat=SimpleNamespace(id=123),
                        message_id=456,
                    ),
                )

                with (
                    patch("main.hmaxx.allow_user", return_value=True),
                    patch("main.hmaxi18n.bind_callback"),
                    patch("main.hmaxi18n.get_language", return_value=lang),
                    patch("main.bot.answer_callback_query"),
                    patch("main.bot.edit_message_text") as edit_message_text,
                ):
                    main.callback_inline(call)

                edit_message_text.assert_called_once()
                keyboard = edit_message_text.call_args.kwargs["reply_markup"].keyboard
                callbacks = [
                    button.callback_data
                    for row in keyboard
                    for button in row
                ]
                self.assertIn("dump_a256e", callbacks)

    def test_samsung_a25_poster_is_present(self):
        poster = Path(__file__).resolve().parents[1] / "images" / "samsung_a25_a256e.png"
        self.assertTrue(poster.is_file())

    def test_samsung_a25_callback_sends_caption_and_drive_buttons(self):
        call = SimpleNamespace(
            id="callback-a25",
            data="dump_a256e",
            message=SimpleNamespace(
                chat=SimpleNamespace(id=123),
                message_id=456,
            ),
        )

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
        caption = send_photo.call_args.kwargs["caption"]
        for detail in (
            "SAMSUNG A25 5G",
            "SM-A256E",
            "128GB UFS",
            "A256EXXS8CYG3",
            "F64 ULTRA",
            "4.5 GB",
            "RAR",
            "MobiFirmware.VIP",
            "Google Drive",
        ):
            self.assertIn(detail, caption)

        buttons = [
            button
            for row in send_photo.call_args.kwargs["reply_markup"].keyboard
            for button in row
        ]
        self.assertEqual(
            buttons[0].url,
            "https://drive.google.com/file/d/1Tw19y4kZPm8mHaO0raheL4nIfp3_HUv2/view",
        )
        self.assertEqual(buttons[1].callback_data, "dump_scatter_samsung")

    def test_samsung_a25_caption_translated_in_all_languages(self):
        expected = {
            "ar": ("بطاقة مواصفات الفيرموير", "تحميل - Google Drive", "العودة لقائمة سامسونج DUMP"),
            "en": ("FIRMWARE SPEC CARD", "Download - Google Drive", "Back to Samsung DUMP list"),
            "fr": ("FICHE TECHNIQUE DU FIRMWARE", "Télécharger - Google Drive", "Retour à la liste Samsung DUMP"),
        }
        for lang, (title, download, back) in expected.items():
            with self.subTest(lang=lang):
                call = SimpleNamespace(
                    id="callback-a25-lang",
                    data="dump_a256e",
                    message=SimpleNamespace(
                        chat=SimpleNamespace(id=123),
                        message_id=456,
                    ),
                )

                with (
                    patch("main.hmaxx.allow_user", return_value=True),
                    patch("main.hmaxi18n.bind_callback"),
                    patch("main.hmaxi18n.get_language", return_value=lang),
                    patch("main.bot.answer_callback_query"),
                    patch("main.bot.delete_message"),
                    patch("main.bot.send_photo") as send_photo,
                    patch("main.bot.send_message"),
                ):
                    main.callback_inline(call)

                caption = send_photo.call_args.kwargs["caption"]
                buttons = [
                    button
                    for row in send_photo.call_args.kwargs["reply_markup"].keyboard
                    for button in row
                ]
                self.assertIn(title, caption)
                self.assertIn(download, buttons[0].text)
                self.assertIn(back, buttons[1].text)


class MHorsePop8DumpCatalogTests(unittest.TestCase):
    DRIVE_URL = "https://drive.google.com/file/d/11Ck6VqXy_UdagNjz6GvMiRg7JH2DQmuu/view"

    def test_m_horse_is_detected_as_a_dump_brand(self):
        self.assertEqual(detect_brand("M-HORSE POP 8"), "m_horse")
        self.assertEqual(detect_brand("M_HORSE POP 8"), "m_horse")

    def test_m_horse_pop8_is_listed_in_m_horse_section(self):
        expected_entry = (
            "🔥 M-HORSE POP 8 - 1GB [PANDORA]",
            "dump_model_m_horse_pop8",
        )
        self.assertIn(expected_entry, DUMP_SMART_SECTIONS["m_horse"])

    def test_m_horse_pop8_poster_is_present(self):
        poster = Path(__file__).resolve().parents[1] / "images" / "m_horse_pop8.png"
        self.assertTrue(poster.is_file())

    def test_dump_menu_lists_m_horse_in_all_languages(self):
        for lang in ("ar", "en", "fr"):
            with self.subTest(lang=lang):
                call = SimpleNamespace(
                    id="callback-m-horse-menu",
                    data="dump_main_section",
                    message=SimpleNamespace(
                        chat=SimpleNamespace(id=123),
                        message_id=456,
                    ),
                )

                with (
                    patch("main.hmaxx.allow_user", return_value=True),
                    patch("main.hmaxi18n.bind_callback"),
                    patch("main.hmaxi18n.get_language", return_value=lang),
                    patch("main.bot.answer_callback_query"),
                    patch("main.bot.edit_message_text") as edit_message_text,
                ):
                    main.callback_inline(call)

                edit_message_text.assert_called_once()
                keyboard = edit_message_text.call_args.kwargs["reply_markup"].keyboard
                callbacks = [button.callback_data for row in keyboard for button in row]
                self.assertIn("dump_m_horse_section", callbacks)

    def test_m_horse_section_lists_pop8_in_all_languages(self):
        for lang in ("ar", "en", "fr"):
            with self.subTest(lang=lang):
                call = SimpleNamespace(
                    id="callback-m-horse-section",
                    data="dump_m_horse_section",
                    message=SimpleNamespace(
                        chat=SimpleNamespace(id=123),
                        message_id=456,
                    ),
                )

                with (
                    patch("main.hmaxx.allow_user", return_value=True),
                    patch("main.hmaxi18n.bind_callback"),
                    patch("main.hmaxi18n.get_language", return_value=lang),
                    patch("main.bot.answer_callback_query"),
                    patch("main.bot.edit_message_text") as edit_message_text,
                ):
                    main.callback_inline(call)

                edit_message_text.assert_called_once()
                keyboard = edit_message_text.call_args.kwargs["reply_markup"].keyboard
                callbacks = [button.callback_data for row in keyboard for button in row]
                self.assertIn("dump_model_m_horse_pop8", callbacks)
                self.assertIn("dump_main_section", callbacks)

    def test_m_horse_pop8_callback_sends_caption_and_drive_buttons(self):
        call = SimpleNamespace(
            id="callback-m-horse-pop8",
            data="dump_model_m_horse_pop8",
            message=SimpleNamespace(
                chat=SimpleNamespace(id=123),
                message_id=456,
            ),
        )

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
        caption = send_photo.call_args.kwargs["caption"]
        for detail in (
            "M-HORSE POP 8",
            "POP 8-M-HORSE-V01-20240109",
            "Pandora Tool",
            "1 GB",
            "RAR",
            "MobiFirmware.VIP",
            "Google Drive",
            "علي الشاعر",
            "بطاقة مواصفات الفيرموير",
        ):
            self.assertIn(detail, caption)

        buttons = [
            button
            for row in send_photo.call_args.kwargs["reply_markup"].keyboard
            for button in row
        ]
        self.assertEqual(buttons[0].url, self.DRIVE_URL)
        self.assertEqual(buttons[1].callback_data, "dump_m_horse_section")

    def test_m_horse_pop8_caption_translated_in_all_languages(self):
        expected = {
            "ar": (
                "بطاقة مواصفات الفيرموير",
                "تحميل - Google Drive",
                "العودة لقائمة M-HORSE DUMP",
            ),
            "en": (
                "FIRMWARE SPEC CARD",
                "Download - Google Drive",
                "Back to M-HORSE DUMP list",
            ),
            "fr": (
                "FICHE TECHNIQUE DU FIRMWARE",
                "Télécharger - Google Drive",
                "Retour à la liste M-HORSE DUMP",
            ),
        }
        for lang, (title, download, back) in expected.items():
            with self.subTest(lang=lang):
                call = SimpleNamespace(
                    id="callback-m-horse-lang",
                    data="dump_model_m_horse_pop8",
                    message=SimpleNamespace(
                        chat=SimpleNamespace(id=123),
                        message_id=456,
                    ),
                )

                with (
                    patch("main.hmaxx.allow_user", return_value=True),
                    patch("main.hmaxi18n.bind_callback"),
                    patch("main.hmaxi18n.get_language", return_value=lang),
                    patch("main.bot.answer_callback_query"),
                    patch("main.bot.delete_message"),
                    patch("main.bot.send_photo") as send_photo,
                    patch("main.bot.send_message"),
                ):
                    main.callback_inline(call)

                caption = send_photo.call_args.kwargs["caption"]
                buttons = [
                    button
                    for row in send_photo.call_args.kwargs["reply_markup"].keyboard
                    for button in row
                ]
                self.assertIn(title, caption)
                self.assertIn(download, buttons[0].text)
                self.assertIn(back, buttons[1].text)


class HHorseM16DumpCatalogTests(unittest.TestCase):
    DRIVE_URL = "https://drive.google.com/file/d/10tCf_9gERV7oN2ewDHyGG4Qt2evP4PE1/view"

    def test_m_horse_dump_menu_lists_h_horse_in_all_languages(self):
        for lang in ("ar", "en", "fr"):
            with self.subTest(lang=lang):
                call = SimpleNamespace(
                    id="callback-m-horse-menu",
                    data="dump_m_horse_section",
                    message=SimpleNamespace(
                        chat=SimpleNamespace(id=123),
                        message_id=456,
                    ),
                )

                with (
                    patch("main.hmaxx.allow_user", return_value=True),
                    patch("main.hmaxi18n.bind_callback"),
                    patch("main.hmaxi18n.get_language", return_value=lang),
                    patch("main.bot.answer_callback_query"),
                    patch("main.bot.edit_message_text") as edit_message_text,
                ):
                    main.callback_inline(call)

                edit_message_text.assert_called_once()
                keyboard = edit_message_text.call_args.kwargs["reply_markup"].keyboard
                buttons = [button for row in keyboard for button in row]
                callbacks = [button.callback_data for button in buttons]
                self.assertIn("dump_h_horse_m16", callbacks)
                self.assertIn("📱 H-HORSE M16 PRO MAX", [button.text for button in buttons])

    def test_other_dump_menu_no_longer_lists_h_horse(self):
        call = SimpleNamespace(
            id="callback-other-menu",
            data="dump_other_full_section",
            message=SimpleNamespace(
                chat=SimpleNamespace(id=123),
                message_id=456,
            ),
        )

        with (
            patch("main.hmaxx.allow_user", return_value=True),
            patch("main.hmaxi18n.bind_callback"),
            patch("main.hmaxi18n.get_language", return_value="ar"),
            patch("main.bot.answer_callback_query"),
            patch("main.bot.edit_message_text") as edit_message_text,
        ):
            main.callback_inline(call)

        edit_message_text.assert_called_once()
        keyboard = edit_message_text.call_args.kwargs["reply_markup"].keyboard
        buttons = [button for row in keyboard for button in row]
        self.assertNotIn("dump_h_horse_m16", [button.callback_data for button in buttons])
        self.assertNotIn(
            "📱 H-HORSE M16 PRO MAX",
            [button.text for button in buttons],
        )

    def test_h_horse_callback_sends_details_and_drive_buttons(self):
        call = SimpleNamespace(
            id="callback-h-horse",
            data="dump_h_horse_m16",
            message=SimpleNamespace(
                chat=SimpleNamespace(id=123),
                message_id=456,
            ),
        )

        with (
            patch("main.hmaxx.allow_user", return_value=True),
            patch("main.hmaxi18n.bind_callback"),
            patch("main.bot.answer_callback_query"),
            patch("main.bot.edit_message_text") as edit_message_text,
        ):
            main.callback_inline(call)

        edit_message_text.assert_called_once()
        display_text = edit_message_text.call_args.args[0]
        for detail in (
            "H-HORSE M16 PRO MAX",
            "SPD",
            "12345678",
            "khulnafirmwarer.com",
            "Gsm King Khulna",
        ):
            self.assertIn(detail, display_text)

        buttons = [
            button
            for row in edit_message_text.call_args.kwargs["reply_markup"].keyboard
            for button in row
        ]
        self.assertEqual(buttons[0].url, self.DRIVE_URL)
        self.assertEqual(buttons[1].callback_data, "dump_m_horse_section")

    def test_h_horse_caption_translated_in_all_languages(self):
        expected = {
            "ar": (
                "ملف DUMP لهاتف H-HORSE M16 PRO MAX",
                "رابط تحميل الفلاشة",
                "العودة لقائمة M-HORSE DUMP",
            ),
            "en": (
                "DUMP File for H-HORSE M16 PRO MAX",
                "Firmware download link",
                "Back to M-HORSE DUMP list",
            ),
            "fr": (
                "Fichier DUMP pour H-HORSE M16 PRO MAX",
                "Lien de téléchargement",
                "Retour à la liste M-HORSE DUMP",
            ),
        }
        for lang, (title, download, back) in expected.items():
            with self.subTest(lang=lang):
                call = SimpleNamespace(
                    id="callback-h-horse-lang",
                    data="dump_h_horse_m16",
                    message=SimpleNamespace(
                        chat=SimpleNamespace(id=123),
                        message_id=456,
                    ),
                )

                with (
                    patch("main.hmaxx.allow_user", return_value=True),
                    patch("main.hmaxi18n.bind_callback"),
                    patch("main.hmaxi18n.get_language", return_value=lang),
                    patch("main.bot.answer_callback_query"),
                    patch("main.bot.edit_message_text") as edit_message_text,
                ):
                    main.callback_inline(call)

                self.assertIn(title, edit_message_text.call_args.args[0])
                buttons = [
                    button
                    for row in edit_message_text.call_args.kwargs["reply_markup"].keyboard
                    for button in row
                ]
                self.assertIn(download, buttons[0].text)
                self.assertIn(back, buttons[1].text)


class OppoA31DumpCatalogTests(unittest.TestCase):
    CALLBACK = "dump_model_oppo_a31_cph2015_128gb"
    DRIVE_URL = "https://drive.google.com/file/d/1ZJ6o9C8jFB9MeRHdnB1N-AkeGtpaBu64/view"

    def test_oppo_a31_is_listed_in_oppo_section(self):
        call = SimpleNamespace(
            id="callback-oppo-a31-menu",
            data="dump_oppo_section",
            message=SimpleNamespace(
                chat=SimpleNamespace(id=123),
                message_id=456,
            ),
        )

        with (
            patch("main.hmaxx.allow_user", return_value=True),
            patch("main.hmaxi18n.bind_callback"),
            patch("main.bot.answer_callback_query"),
            patch("main.bot.edit_message_text") as edit_message_text,
        ):
            main.callback_inline(call)

        buttons = [
            button
            for row in edit_message_text.call_args.kwargs["reply_markup"].keyboard
            for button in row
        ]
        self.assertIn(self.CALLBACK, [button.callback_data for button in buttons])
        self.assertTrue(any("OPPO A31 CPH2015" in button.text for button in buttons))

    def test_oppo_a31_callback_sends_dump_card_and_download_button(self):
        call = SimpleNamespace(
            id="callback-oppo-a31",
            data=self.CALLBACK,
            message=SimpleNamespace(
                chat=SimpleNamespace(id=123),
                message_id=456,
            ),
        )

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
        self.assertEqual(
            Path(send_photo.call_args.args[1].name).name,
            "oppo_a31_cph2015_128gb_emmc_dump.jpg",
        )
        caption = send_photo.call_args.kwargs["caption"]
        for detail in (
            "OPPO A31 — CPH2015",
            "128GB eMMC DUMP",
            "EASY JTAG PLUS",
            "2.4 GB",
            "Google Drive",
            "MobiFirmware.VIP",
        ):
            self.assertIn(detail, caption)

        buttons = [
            button
            for row in send_photo.call_args.kwargs["reply_markup"].keyboard
            for button in row
        ]
        self.assertEqual(buttons[0].url, self.DRIVE_URL)
        self.assertEqual(buttons[1].callback_data, "dump_oppo_section")


class OppoReno12FDumpCatalogTests(unittest.TestCase):
    CALLBACK = "dump_model_oppo_reno_12f_4g_cph2687"
    DRIVE_URL = "https://drive.google.com/file/d/1OY4I_TmBJsEKNlUdHPULjpiLOEyQJuIc/view"

    def test_oppo_reno_12f_is_listed_in_oppo_section(self):
        call = SimpleNamespace(
            id="callback-oppo-menu",
            data="dump_oppo_full_section",
            message=SimpleNamespace(
                chat=SimpleNamespace(id=123),
                message_id=456,
            ),
        )

        with (
            patch("main.hmaxx.allow_user", return_value=True),
            patch("main.hmaxi18n.bind_callback"),
            patch("main.bot.answer_callback_query"),
            patch("main.bot.edit_message_text") as edit_message_text,
        ):
            main.callback_inline(call)

        buttons = [
            button
            for row in edit_message_text.call_args.kwargs["reply_markup"].keyboard
            for button in row
        ]
        self.assertIn(self.CALLBACK, [button.callback_data for button in buttons])
        self.assertTrue(
            any("OPPO RENO 12F 4G CPH2687" in button.text for button in buttons)
        )

    def test_oppo_reno_12f_callback_sends_dump_card_and_download_button(self):
        call = SimpleNamespace(
            id="callback-oppo-reno-12f",
            data=self.CALLBACK,
            message=SimpleNamespace(
                chat=SimpleNamespace(id=123),
                message_id=456,
            ),
        )

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
        caption = send_photo.call_args.kwargs["caption"]
        for detail in (
            "OPPO RENO 12F 4G",
            "CPH2687",
            "F64 BOX",
            "MediaTek Helio G99",
            "8GB RAM • 256GB Storage",
            "8.52 GB",
            "CPH2687_F64BOX_FullDump_20240612.zip",
            "MobiFirmware.VIP",
        ):
            self.assertIn(detail, caption)

        buttons = [
            button
            for row in send_photo.call_args.kwargs["reply_markup"].keyboard
            for button in row
        ]
        self.assertEqual(buttons[0].url, self.DRIVE_URL)
        self.assertEqual(buttons[1].callback_data, "dump_oppo_full_section")


class InfinixNote30DumpCatalogTests(unittest.TestCase):
    CALLBACK = "dump_model_infinix_note_30_5g_x6711_v600"
    DRIVE_URL = "https://drive.google.com/file/d/1ubef2yjzrQpNB0MFPw8UWdraxPr6OtbB/view"

    def test_infinix_note_30_is_listed_in_infinix_section(self):
        call = SimpleNamespace(
            id="callback-infinix-menu",
            data="dump_infinix_full_section",
            message=SimpleNamespace(
                chat=SimpleNamespace(id=123),
                message_id=456,
            ),
        )

        with (
            patch("main.hmaxx.allow_user", return_value=True),
            patch("main.hmaxi18n.bind_callback"),
            patch("main.bot.answer_callback_query"),
            patch("main.bot.edit_message_text") as edit_message_text,
        ):
            main.callback_inline(call)

        buttons = [
            button
            for row in edit_message_text.call_args.kwargs["reply_markup"].keyboard
            for button in row
        ]
        self.assertIn(self.CALLBACK, [button.callback_data for button in buttons])
        self.assertTrue(any("NOTE 30 5G X6711 V600" in button.text for button in buttons))

    def test_infinix_note_30_callback_sends_photo_and_download_button(self):
        call = SimpleNamespace(
            id="callback-infinix-note-30",
            data=self.CALLBACK,
            message=SimpleNamespace(
                chat=SimpleNamespace(id=123),
                message_id=456,
            ),
        )

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
        caption = send_photo.call_args.kwargs["caption"]
        for detail in (
            "INFINIX NOTE 30 5G",
            "X6711 - V600",
            "FULL DUMP",
            "Pandora Tool",
            "MobiFirmware.VIP",
        ):
            self.assertIn(detail, caption)

        buttons = [
            button
            for row in send_photo.call_args.kwargs["reply_markup"].keyboard
            for button in row
        ]
        self.assertEqual(buttons[0].url, self.DRIVE_URL)
        self.assertEqual(buttons[1].callback_data, "dump_infinix_full_section")


class RedmiNote14G5BerylXmlDumpCatalogTests(unittest.TestCase):
    DRIVE_URL = "https://drive.google.com/file/d/1zxRGj8wgYfsDQaVfn7RB53Xw78JmCToF/view"

    def test_note14_beryl_is_detected_as_a_xiaomi_group_brand(self):
        self.assertEqual(
            detect_brand("REDMI Note 14 5G Beryl XML 6.5GB"), "xiaomi_group"
        )

    def test_note14_beryl_is_listed_in_the_xiaomi_group_section(self):
        expected_entry = (
            "🔥 REDMI Note 14 5G Beryl XML 6.5GB [EASY JTAG]",
            "dump_model_redmi_note14_5g_beryl_xml",
        )
        self.assertIn(expected_entry, DUMP_SMART_SECTIONS["xiaomi_group"])

    def test_xiaomi_group_menu_lists_the_note14_beryl_card(self):
        call = SimpleNamespace(
            id="callback-note14-menu",
            data="dump_xiaomi_group_section",
            message=SimpleNamespace(
                chat=SimpleNamespace(id=123),
                message_id=456,
            ),
        )

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
        self.assertIn("dump_model_redmi_note14_5g_beryl_xml", callbacks)

    def test_note14_beryl_poster_is_present(self):
        poster = (
            Path(__file__).resolve().parents[1]
            / "images"
            / "redmi_note14_5g_beryl_xml_6_5gb_easy_jtag.jpg"
        )
        self.assertTrue(poster.is_file())

    def test_note14_beryl_callback_sends_caption_and_drive_buttons(self):
        call = SimpleNamespace(
            id="callback-note14",
            data="dump_model_redmi_note14_5g_beryl_xml",
            message=SimpleNamespace(
                chat=SimpleNamespace(id=123),
                message_id=456,
            ),
        )

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
        caption = send_photo.call_args.kwargs["caption"]
        for detail in (
            "Redmi Note 14 5G",
            "Beryl",
            "XML FULL DUMP",
            "Easy JTAG Plus",
            "6.5 GB",
            "Google Drive",
            "MobiFirmware.VIP",
        ):
            self.assertIn(detail, caption)

        buttons = [
            button
            for row in send_photo.call_args.kwargs["reply_markup"].keyboard
            for button in row
        ]
        self.assertEqual(buttons[0].url, self.DRIVE_URL)
        self.assertEqual(buttons[1].callback_data, "dump_xiaomi_group_section")


class Redmi13cGaleDumpCatalogTests(unittest.TestCase):
    TERABOX_URL = "https://www.terabox.app/arabic/sharing/link?surl=h5bhksix3MWtLXRftpknUQ"
    CALLBACK = "dump_model_redmi_13c_gale"

    def test_redmi_13c_gale_is_listed_in_the_xiaomi_group_section(self):
        expected_entry = (
            "🔥 XIAOMI Redmi 13C (Gale) OS2.0.6.0.VGPMIXM [PANDORA]",
            self.CALLBACK,
        )
        self.assertIn(expected_entry, DUMP_SMART_SECTIONS["xiaomi_group"])

    def test_xiaomi_group_menu_lists_the_redmi_13c_gale_card(self):
        call = SimpleNamespace(
            id="callback-redmi-13c-menu",
            data="dump_xiaomi_group_section",
            message=SimpleNamespace(
                chat=SimpleNamespace(id=123),
                message_id=456,
            ),
        )

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
        self.assertIn(self.CALLBACK, callbacks)

    def test_redmi_13c_gale_poster_is_present(self):
        poster = (
            Path(__file__).resolve().parents[1]
            / "images"
            / "xiaomi_redmi_13c_gale_os2_hmax.jpg"
        )
        self.assertTrue(poster.is_file())

    def test_redmi_13c_gale_callback_sends_caption_and_terabox_buttons_in_all_languages(self):
        expected_buttons = {
            "ar": ("📥 تحميل من Terabox - VPN سايفون مطلوب", "⬅️ رجوع لـ XIAOMI"),
            "en": ("📥 Download Terabox - Need VPN", "⬅️ Back to XIAOMI"),
            "fr": ("📥 Télécharger Terabox - VPN requis", "⬅️ Retour à XIAOMI"),
        }
        for lang, (dl_label, back_label) in expected_buttons.items():
            with self.subTest(lang=lang):
                call = SimpleNamespace(
                    id="callback-redmi-13c",
                    data=self.CALLBACK,
                    message=SimpleNamespace(
                        chat=SimpleNamespace(id=123),
                        message_id=456,
                    ),
                )

                with (
                    patch("main.hmaxx.allow_user", return_value=True),
                    patch("main.hmaxi18n.bind_callback"),
                    patch("main.hmaxi18n.get_language", return_value=lang),
                    patch("main.bot.answer_callback_query"),
                    patch("main.bot.delete_message"),
                    patch("main.bot.send_photo") as send_photo,
                    patch("main.bot.send_message") as send_message,
                ):
                    main.callback_inline(call)

                send_photo.assert_called_once()
                send_message.assert_not_called()
                caption = send_photo.call_args.kwargs["caption"]
                self.assertNotIn("【entity-", caption)
                for detail in (
                    "XIAOMI Redmi 13C (Gale) OS2.0.6.0.VGPMIXM",
                    "Redmi 13C (Gale)",
                    "OS2.0.6.0.VGPMIXM",
                    "PANDORA",
                    "Full Dump",
                    "MobiFirmware.VIP",
                    "Terabox",
                    "HMAX-UNLOCKER",
                ):
                    self.assertIn(detail, caption)

                buttons = [
                    button
                    for row in send_photo.call_args.kwargs["reply_markup"].keyboard
                    for button in row
                ]
                self.assertEqual(buttons[0].text, dl_label)
                self.assertEqual(buttons[0].url, self.TERABOX_URL)
                self.assertEqual(buttons[1].text, back_label)
                self.assertEqual(buttons[1].callback_data, "dump_xiaomi_group_section")


class ItelA49DumpCatalogTests(unittest.TestCase):
    CALLBACK = "dump_model_itel_a49_a661l"
    TERABOX_URL = "https://www.terabox.app/arabic/sharing/link?surl=aylVN-8Y7P9jI6ye9JpsMQ"

    def _make_call(self, callback_data, callback_id="callback-itel-a49"):
        return SimpleNamespace(
            id=callback_id,
            data=callback_data,
            message=SimpleNamespace(
                chat=SimpleNamespace(id=123),
                message_id=456,
            ),
        )

    def test_a49_is_listed_in_the_itel_menu_in_all_languages(self):
        expected = {
            "ar": ("📱 ITEL DUMP", "🔥 A661L - A49 (A58 Pro) [PANDORA] - نادر NEW"),
            "en": ("📱 ITEL DUMP", "🔥 A661L - A49 (A58 Pro) [PANDORA] - Rare NEW"),
            "fr": ("📱 DUMP ITEL", "🔥 A661L - A49 (A58 Pro) [PANDORA] - Rare NEW"),
        }
        for lang, (title, a49_label) in expected.items():
            with self.subTest(lang=lang):
                call = self._make_call("dump_itel_full_section", f"callback-itel-menu-{lang}")
                with (
                    patch("main.hmaxx.allow_user", return_value=True),
                    patch("main.hmaxi18n.bind_callback"),
                    patch("main.hmaxi18n.get_language", return_value=lang),
                    patch("main.bot.answer_callback_query"),
                    patch("main.bot.edit_message_text") as edit_message_text,
                ):
                    main.callback_inline(call)

                edit_message_text.assert_called_once()
                self.assertEqual(edit_message_text.call_args.args[0], title)
                keyboard = edit_message_text.call_args.kwargs["reply_markup"].keyboard
                buttons = [button for row in keyboard for button in row]
                callbacks = [button.callback_data for button in buttons]
                self.assertIn(self.CALLBACK, callbacks)
                self.assertIn("dump_model_itel_p37_p651w", callbacks)
                self.assertIn("dump_model_itel_l6503_vision2", callbacks)
                self.assertIn("dump_model_itel_a06_a669w_full_dump_unlocktool", callbacks)
                a49_button = next(button for button in buttons if button.callback_data == self.CALLBACK)
                self.assertEqual(a49_button.text, a49_label)

    def test_a49_poster_is_present(self):
        poster = (
            Path(__file__).resolve().parents[1]
            / "images"
            / "itel_a49_a661l_a58pro_pandora_hmax.jpg"
        )
        self.assertTrue(poster.is_file())

    def test_a49_callback_sends_localized_caption_and_terabox_buttons(self):
        expected_buttons = {
            "ar": ("📥 تحميل Terabox", "⬅️ رجوع لـ ITEL"),
            "en": ("📥 Download Terabox", "⬅️ Back to ITEL"),
            "fr": ("📥 Télécharger Terabox", "⬅️ Retour à ITEL"),
        }
        for lang, (download_label, back_label) in expected_buttons.items():
            with self.subTest(lang=lang):
                call = self._make_call(self.CALLBACK, f"callback-itel-a49-{lang}")
                with (
                    patch("main.hmaxx.allow_user", return_value=True),
                    patch("main.hmaxi18n.bind_callback"),
                    patch("main.hmaxi18n.get_language", return_value=lang),
                    patch("main.bot.answer_callback_query"),
                    patch("main.bot.delete_message"),
                    patch("main.bot.send_photo") as send_photo,
                    patch("main.bot.send_message") as send_message,
                ):
                    main.callback_inline(call)

                send_photo.assert_called_once()
                send_message.assert_not_called()
                caption = send_photo.call_args.kwargs["caption"]
                self.assertNotIn("【entity-", caption)
                for detail in (
                    "A661L / A49 / A58 Pro",
                    "Pandora Tool",
                    "MobiFirmware.VIP",
                    "HMAX-UNLOCKER",
                ):
                    self.assertIn(detail, caption)
                self.assertTrue(
                    "tested" in caption.lower()
                    or "testé" in caption.lower()
                    or "مجرب" in caption
                )

                buttons = [
                    button
                    for row in send_photo.call_args.kwargs["reply_markup"].keyboard
                    for button in row
                ]
                self.assertEqual(buttons[0].text, download_label)
                self.assertEqual(buttons[0].url, self.TERABOX_URL)
                self.assertEqual(buttons[1].text, back_label)
                self.assertEqual(buttons[1].callback_data, "dump_itel_full_section")


if __name__ == "__main__":
    unittest.main()
