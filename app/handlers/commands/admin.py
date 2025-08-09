from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from core.database.queries import update_correspondence, get_user_id
from core.bot.__init__ import bot

admin_router = Router()

IS_ADMIN = True


@admin_router.message(Command('msg_adm'))
async def handle_msg(message: Message):
    msg = message.text

    try:
        msg_parts = msg.split(' ')
        user_identifier = int(msg_parts[1]) if msg_parts[1].isdigit() else get_user_id(msg_parts[1])
        msg = ' '.join(msg_parts[2:])
        print(msg_parts[1:][0], len(msg_parts[1:][0]))
        if not msg_parts[1].isdigit():
            if msg_parts[1][0][0] != '@':
                raise Exception
            elif len(msg_parts[1:][0]) > 33:
                raise Exception

    except Exception:
        await message.reply('<b>Ошибка.</b>\nСообщение должно быть вида\n/msg_adm &lt;username/user_id&gt &lt;message&gt.')
        return

    if not msg:
        await message.reply('<b>Ошибка.</b>\nСообщение не должно быть пустым.')
        return

    admin_message = f'<b>Ответ админа:</b>\n{msg}'
    try:
        await bot.send_message(text=admin_message,
                               chat_id=user_identifier,)
    except Exception as e:
        print(f'Error: {e}')
        await message.reply('<b>Ошибка.</b>\nНе получилось отправить сообщение.')

    update_correspondence(user_identifier, msg, str(message.date.astimezone()), IS_ADMIN)
