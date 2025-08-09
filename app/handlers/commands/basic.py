import os

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.keyboards.builders import correspondence_with_user
from core.database.queries import get_names, get_count
basic_router = Router()


@basic_router.message(Command('get_cor'))
async def get_correspondence_keyboard(message: Message):
    max_pages = -(get_count() // -8)
    await message.answer(f'Выбери пользователя, переписку с которым хочешь увидеть\nСтраница 1/{max_pages}',
                         reply_markup=await correspondence_with_user(get_names()))
