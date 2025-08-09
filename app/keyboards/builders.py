import json

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


async def correspondence_with_user(users: list, current_page: int = 0):
    keyboard = InlineKeyboardBuilder()

    next_callback_data = json.dumps({'source': 'cwu', 'action': 'next', 'page': current_page})
    prev_callback_data = json.dumps({'source': 'cwu', 'action': 'prev', 'page': current_page})
    content_callback_data = {'source': 'cwu', 'action': 'content', 'id': None}

    start = current_page * 8
    stop = start + 8

    counter = 1
    for user in users[start:stop]:
        content_callback_data['id'] = user[0]
        content_button = InlineKeyboardButton(text=f'{str(user[0])[-4:]} | {user[1]}',
                                              callback_data=json.dumps(content_callback_data))
        counter += 1
        if counter % 2 == 0:
            keyboard.row(content_button)
        else:
            keyboard.add(content_button)
    keyboard.row(
        InlineKeyboardButton(text='<-Назад', callback_data=prev_callback_data),
        InlineKeyboardButton(text='Далее->', callback_data=next_callback_data))

    return keyboard.as_markup()
