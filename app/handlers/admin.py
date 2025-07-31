from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from core.bot.__init__ import bot

admin_router = Router()


@admin_router.message(CommandStart())
async def handle_start(message: Message):
    await message.reply('')


@admin_router.message(Command('msg_adm'))
async def handle_msg(message: Message):
    msg = message.text
    msg_parts = msg.split(' ')
    user_id = int(msg_parts[1])
    msg = ''.join(msg_parts[2:])

    print()
    admin_message = f'<b>Ответ админа:</b>\n{msg}'
    try:
        await bot.send_message(text=admin_message,
                               chat_id=user_id)
    except Exception as e:
        print(f'Error: {e}')
        await message.reply('Sorry, you message was not sent.')

