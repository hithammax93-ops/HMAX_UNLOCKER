import unittest
from unittest.mock import patch

from main import show_main_menu


class MainMenuLanguageTests(unittest.TestCase):
    def test_menu_uses_the_selected_language(self):
        language_examples = {
            "en": ("Welcome to HMAX UNLOCKER", "Advertise With Us"),
            "fr": ("Bienvenue au centre", "Annoncez avec nous"),
            "ar": ("أهلاً بك في مركز", "أعلن معنا"),
        }

        for language, (welcome_text, button_text) in language_examples.items():
            with self.subTest(language=language):
                with (
                    patch("main.hmaxi18n.get_language", return_value=language) as get_language,
                    patch("main.bot.send_message") as send_message,
                ):
                    show_main_menu(123)

                get_language.assert_called_once_with(123)
                args, kwargs = send_message.call_args
                self.assertEqual(args[0], 123)
                self.assertIn(welcome_text, args[1])
                self.assertTrue(
                    any(
                        button_text in button.text
                        for row in kwargs["reply_markup"].keyboard
                        for button in row
                    )
                )
                self.assertEqual(kwargs["parse_mode"], "Markdown")


if __name__ == "__main__":
    unittest.main()
