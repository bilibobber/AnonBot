import logging
import sys

from . import dp, bot

from app.handlers.user import user_router
from app.handlers.admin import admin_router
from app.handlers.basic import basic_router


async def start_polling() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    try:
        dp.include_router(user_router)
        dp.include_router(admin_router)
        dp.include_router(basic_router)

        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logging.warning("Bot stopped by admin!")
    finally:
        await bot.session.close()
