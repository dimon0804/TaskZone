import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

import config as cfg
from handlers.user import router 
from database.models import async_main

async def main() -> None:
    load_dotenv()
    default = DefaultBotProperties(parse_mode='HTML', link_preview_is_disabled=True)
    bot = Bot(token=cfg.BOT_TOKEN, default=default)
    dp = Dispatcher(storage=MemoryStorage())
    await async_main()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    if cfg.DEBUG:
        logging.info("Bot started")

if __name__ == "__main__":
    try:
        if cfg.DEBUG:
            logging.basicConfig(level=logging.INFO)
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
