import os

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from core.database.queries import update_correspondence
from core.bot.__init__ import bot

from dotenv import load_dotenv
load_dotenv()

user_router = Router()

IS_ADMIN = False


@user_router.message(Command('msg'))
async def handle_msg(message: Message):
    msg = message.text
    try:
        msg_parts = msg.split(' ')
        msg = ' '.join(msg_parts[1:])
        if not msg:
            raise Exception()

    except Exception:
        await message.reply('<b>Ошибка.</b>\nСообщение должно быть вида\n/msg &lt;message&gt.')
        return
    msg = f'<b>{message.from_user.id} @{message.from_user.username}:</b>\n{msg}'
    admin_ids = [os.getenv('ADMIN_ID')]
    try:
        for admin_id in admin_ids:
            await bot.send_message(text=msg,
                                   chat_id=admin_id)
    except Exception as e:
        print(f'Error: {e}')
        await message.reply('Sorry, you message was not sent.')

    update_correspondence(message.from_user.id, msg, str(message.date.astimezone()), IS_ADMIN,
                          '@' + str(message.from_user.username))
