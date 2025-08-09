import json

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def correspondence_settings(user_id: int, checked: bool = False):

    prev_callback_data = json.dumps({'source': 'cs', 'action': 'prev'})
    all_callback_data = json.dumps({'source': 'cs', 'action': 'all', 'id': user_id, 's': checked})
    last_callback_data = json.dumps({'source': 'cs', 'action': 'last', 'id': user_id, 's': checked})
    checked_callback_data = json.dumps({'source': 'cs', 'action': f'checked_{checked}', 'id': user_id})

    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='все', callback_data=all_callback_data),
         InlineKeyboardButton(text='последние 30', callback_data=last_callback_data)],

        [InlineKeyboardButton(text=f'✅  С датой' if checked else '❌  С датой', callback_data=checked_callback_data)],
        [InlineKeyboardButton(text='назад', callback_data=prev_callback_data)]
    ])

