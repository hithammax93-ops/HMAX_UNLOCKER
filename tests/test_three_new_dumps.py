import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import main


class ThreeNewDumpsTests(unittest.TestCase):
    CASES = (
        ('benco_s1_pro_ae9260_dual', 'benco', 'benco_s1_pro_ae9260_dual_dump.jpg',
         ['1Dx6I5z92KofjEru4xveT7SZ-TeQj7a_L', '19xbfXJYSKw-PN1d6QBrscmOFwqqoKDjY'],
         ['Pandora', 'CM2', 'MobiFirmware.VIP']),
        ('honor_x7a_rky_lx2_2gb', 'honor', 'honor_x7a_rky_lx2_2gb_dump_f64.jpg',
         ['1TiQ4y7sUK6cNxaUVT2tEcjgC3vjdlEr0'],
         ['F64 Ultra', 'Hossam Khairy', 'Network Files Included', 'MobiFirmware.VIP']),
        ('nokia_ta_1114_copy', 'nokia', 'nokia_ta_1114_copy_spreadtrum_miracle.jpg',
         ['1_c708OPmAWhZW6Fudrl7TCXRkyyU_Scb'],
         ['COPY VERSION', 'SPREADTRUM', 'Miracle Box', 'Ahmed ClaSsic']),
    )

    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        for name, kwargs in (
            ('hmaxx.allow_user', {'return_value': True}),
            ('hmaxi18n.bind_callback', {}),
            ('hmaxi18n.get_language', {'return_value': 'en'}),
            ('bot.answer_callback_query', {}),
            ('bot.delete_message', {}),
        ):
            self.stack.enter_context(patch('main.' + name, **kwargs))

    def call(self, data):
        main.callback_inline(SimpleNamespace(
            id='test', data=data,
            message=SimpleNamespace(chat=SimpleNamespace(id=123), message_id=456)))

    @staticmethod
    def buttons(mock):
        return [b for row in mock.call_args.kwargs['reply_markup'].keyboard for b in row]

    def test_menu_and_sections(self):
        with patch('main.bot.edit_message_text') as edit:
            self.call('dump_main_section')
            callbacks = [b.callback_data for b in self.buttons(edit)]
            for model, brand, *_ in self.CASES:
                self.assertEqual(callbacks.count('dump_' + brand + '_section'), 1)
                self.call('dump_' + brand + '_section')
                buttons = self.buttons(edit)
                self.assertIn('dump_model_' + model, [b.callback_data for b in buttons])
                self.assertEqual(buttons[-1].callback_data, 'dump_main_section')

    def test_cards_and_text_fallback(self):
        for model, brand, photo, ids, details in self.CASES:
            for fallback in (False, True):
                with self.subTest(model=model, fallback=fallback), \
                     patch('main.bot.send_photo', side_effect=RuntimeError('photo failed') if fallback else None) as send_photo, \
                     patch('main.bot.send_message') as send_message:
                    self.call('dump_model_' + model)
                    send_photo.assert_called_once()
                    self.assertEqual(Path(send_photo.call_args.args[1].name).name, photo)
                    result = send_message if fallback else send_photo
                    result.assert_called_once()
                    if not fallback:
                        send_message.assert_not_called()
                    caption = result.call_args.args[1] if fallback else result.call_args.kwargs['caption']
                    self.assertLessEqual(len(caption.encode('utf-16-le')) // 2, 1024)
                    self.assertNotIn('【entity-', caption)
                    for detail in details:
                        self.assertIn(detail, caption)
                    buttons = self.buttons(result)
                    self.assertEqual(len(buttons), len(ids) + 1)
                    for button, file_id in zip(buttons, ids):
                        self.assertIn(file_id, button.url)
                    self.assertEqual(buttons[-1].callback_data, 'dump_' + brand + '_section')
