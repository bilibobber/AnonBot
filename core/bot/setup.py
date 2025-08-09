import logging
import sys

from . import dp, bot

from app.handlers.commands.user import user_router
from app.handlers.commands.admin import admin_router
from app.handlers.commands.basic import basic_router
from app.handlers.callbacks.correspondence import correspondence_router


async def start_polling() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    try:
        dp.include_router(user_router)
        dp.include_router(admin_router)
        dp.include_router(basic_router)
        dp.include_router(correspondence_router)

        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logging.warning("Bot stopped by admin!")
    finally:
        await bot.session.close()
