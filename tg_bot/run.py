import asyncio 
import sys
import os

from aiogram import Bot, Dispatcher
from loguru import logger

# print(f"path = {sys.path}")
# добавить через sys.path(..) чтобы выйти на папку выше 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(f"path = {sys.path}")

from config import TOKEN
from handlers.handlers import router

def setup_logging():
    """Настройка логирования с помощью loguru"""

    log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    
    # Логи в консоль
    logger.add(
        sys.stderr,
        format=log_format,
        level="INFO",
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    
    # Логи в файл 
    logger.add(
        "logs/bot.log",
        format=log_format,
        level="DEBUG",
        rotation="10 MB",  
        retention="10 days",  
        compression="zip", 
        backtrace=True,
        diagnose=True
    )
    
    # Отдельный файл для ошибок
    logger.add(
        "logs/errors.log",
        format=log_format,
        level="ERROR",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        backtrace=True,
        diagnose=True
    )
    
    logger.info("Logging setup completed")

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    try:
        logger.info("Starting bot...")
        dp.include_router(router)
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot stopped with error: {e}")
        raise

if __name__ == '__main__': 
    os.makedirs("logs", exist_ok=True)
    
    setup_logging()
    
    try:
        logger.info("Bot started successfully")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        print('Bot stopped')
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")
    finally:
        logger.info("Bot shutdown completed")