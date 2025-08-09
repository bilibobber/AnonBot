import json

from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.builders import correspondence_with_user
from core.database.queries import get_names, get_count, get_correspondence
from app.keyboards.inline import correspondence_settings

correspondence_router = Router()


@correspondence_router.callback_query(F.data.func(lambda json_str: json.loads(json_str)['source'] == 'cwu'))
async def keyboard_cwu(callback: CallbackQuery):
    max_pages = -((get_count()) // -8)
    json_data = json.loads(callback.data)
    if json_data['action'] == 'next':
        current_page = (json_data['page'] + 1) if (json_data['page'] + 1) < max_pages else 0

    elif json_data['action'] == 'prev':
        current_page = (json_data['page'] - 1) if (json_data['page'] - 1) >= 0 else max_pages - 1

    elif json_data['action'] == 'content':
        await callback.message.edit_text('Выбери формат переписки.',
                                         reply_markup=correspondence_settings(json_data['id']))
        return
    else:
        return

    new_keyboard = correspondence_with_user(get_names(), current_page)

    await callback.message.edit_text(
        f'Выбери пользователя, переписку с которым хочешь увидеть.\nСтраница {current_page + 1}/{max_pages}',
        reply_markup=await new_keyboard)


@correspondence_router.callback_query(F.data.func(lambda json_str: json.loads(json_str)['source'] == 'cs'))
async def keyboard_cs(callback: CallbackQuery):
    json_data = json.loads(callback.data)
    new_state = False

    if json_data['action'][:7] == 'checked':
        current_state = json_data['action'].split('_')[1] == "True"
        new_state = not current_state

        await callback.message.edit_text('Выбери формат переписки.',
                                         reply_markup=correspondence_settings(json_data['id'], new_state))
        return

    elif json_data['action'] == 'all':
        correspondence = get_correspondence(json_data["id"], 'all')

    elif json_data['action'] == 'last':
        correspondence = get_correspondence(json_data["id"], 5)

    elif json_data['action'] == 'prev':
        max_pages = -(get_count() // -8)
        await callback.message.edit_text(
            f'Выбери пользователя, переписку с которым хочешь увидеть\nСтраница 1/{max_pages}',
            reply_markup=await correspondence_with_user(get_names()))
        return
    else:
        return

    await callback.message.answer('ПЕРЕПИСКА')
    while True:
        try:
            text, date, is_admin = next(correspondence)
            message = ('<b>Админ</b>\n' if is_admin else '') + f'{text}\n' + (date[:-6] if json_data['s'] else '')
            await callback.message.answer(message)
        except StopIteration:
            break
