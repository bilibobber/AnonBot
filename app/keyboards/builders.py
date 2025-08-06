import json

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

test_users = [('@sdgwerg', f'{str(i)}' + '00000' + f'{str(i)}') for i in range(51)]


async def correspondence_with_user(users: list, current_page: int = 0):
    keyboard = InlineKeyboardBuilder()

    next_callback_data = json.dumps({'source': 'cwu', 'action': 'next', 'page': current_page})
    prev_callback_data = json.dumps({'source': 'cwu', 'action': 'prev', 'page': current_page})

    start = current_page * 8
    stop = start + 8

    counter = 1
    for user in users[start:stop]:
        content_button = InlineKeyboardButton(text=f'{str(user[0])[-4:]} | {user[1]}',
                                              url="https://www.google.com")
        counter += 1
        if counter % 2 == 0:
            keyboard.row(content_button)
        else:
            keyboard.add(content_button)
    keyboard.row(
        InlineKeyboardButton(text='<-Назад', callback_data=prev_callback_data),
        InlineKeyboardButton(text='Далее->', callback_data=next_callback_data))

    return keyboard.as_markup()
