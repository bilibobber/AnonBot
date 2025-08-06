import json

from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.builders import correspondence_with_user
from core.database.queries import get_names, get_count

callbacks_router = Router()


@callbacks_router.callback_query(F.data.func(lambda json_str: json.loads(json_str)['source'] == 'cwu'))
async def keyboard_pagination(callback: CallbackQuery):
    max_pages = -((get_count()) // -8)
    current_page = 0
    json_data = json.loads(callback.data)
    if json_data['action'] == 'next':
        current_page = (json_data['page'] + 1) if (json_data['page'] + 1) < max_pages else 0

    elif json_data['action'] == 'prev':
        current_page = (json_data['page'] - 1) if (json_data['page']-1) >= 0 else max_pages-1

    new_keyboard = correspondence_with_user(get_names(), current_page)


    await callback.message.edit_text(f'Выбери пользователя, переписку с которым хочешь увидеть.\nСтраница {current_page+1}/{max_pages}',
                                     reply_markup=await new_keyboard)
