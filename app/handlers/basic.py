from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

basic_router = Router()


@basic_router.message(CommandStart())
async def handle_start(message: Message):
    await message.answer('Hello! To send message to admin:\n/msg &lt;message&gt;')
