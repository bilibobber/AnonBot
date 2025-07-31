from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from core.bot.__init__ import bot

user_router = Router()


@user_router.message(CommandStart())
async def handle_start(message: Message):
    await message.reply('')


@user_router.message(Command('msg'))
async def handle_msg(message: Message):
    user_message = f'<b>{message.from_user.id} @{message.from_user.username}:</b>\n {message.text.removeprefix('/msg ')}'
    admin_ids = [1689195799]
    try:
        for admin_id in admin_ids:
            await bot.send_message(text=user_message,
                                   chat_id=admin_id)
    except Exception as e:
        print(f'Error: {e}')
        await message.reply('Sorry, you message was not sent.')


@user_router.message(Command('id'))
async def handle_id(message: Message):
    await message.reply(str(message.from_user.id))
