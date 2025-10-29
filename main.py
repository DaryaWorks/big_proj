import asyncio 
import sys
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger
from openai import OpenAI

# добавить через sys.path(..) чтобы выйти на папку выше 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tg_bot.config import TOKEN
from model.config import HUGGINGFACEHUB_API_TOKEN
from tg_bot.handlers.handlers import router

from tg_bot.middlewares.middlelwares import ModelMiddleware

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

class TarotModel:
    def __init__(self, api_key: str):
        self.client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=api_key,
        )
        self.model_name = "deepseek-ai/DeepSeek-R1:novita"
        logger.info("✅ Модель Tarot инициализирована")
    
    async def generate_prediction(self, question: str, spread_type: str, spread_name: str) -> str:
        """
        Генерирует предсказание на основе вопроса пользователя и типа расклада
        """
        try:
            # Промпт для модели
            prompt = self._build_prompt(question, spread_type, spread_name)
            
            logger.info(f"🔄 Генерируем предсказание для: {question}")
            
            # Асинхронный вызов модели с правильной передачей аргументов
            loop = asyncio.get_event_loop()
            completion = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": "Ты - опытный таролог с многолетним стажем. Ты делаешь точные и мудрые предсказания по картам Таро. Твои ответы всегда полны эмпатии и духовной мудрости. Отвечай на русском языке."
                        },
                        {
                            "role": "user", 
                            "content": prompt
                        }
                    ],
                    max_tokens=1000,
                    temperature=0.7
                )
            )
            
            if (completion and 
            completion.choices and 
            len(completion.choices) > 0 and 
            completion.choices[0].message and 
            completion.choices[0].message.content):
            
                prediction = completion.choices[0].message.content
                logger.info("✅ Предсказание успешно сгенерировано")
                return prediction.strip()
            else:
                logger.warning("❌ Модель вернула пустой ответ")
                return self._get_fallback_prediction(question, spread_name)
            
        except Exception as e:
            logger.error(f"❌ Ошибка при генерации предсказания: {e}")
            return self._get_fallback_prediction(question, spread_name)
    
    def _build_prompt(self, question: str, spread_type: str, spread_name: str) -> str:
        """Создает промпт для модели на основе вопроса и расклада"""
        
        spread_descriptions = {
            'spread_one': "Расклад на одну карту - показывает суть ситуации",
            'spread_three': "Расклад Прошлое-Настоящее-Будущее - показывает развитие ситуации во времени", 
            'spread_love': "Расклад на отношения - помогает понять чувства и перспективы отношений",
            'spread_career': "Расклад на карьеру - показывает профессиональные перспективы и возможности",
            'spread_advice': "Расклад личный совет - дает мудрый совет для текущей ситуации",
            'spread_custom': "Свободный расклад - универсальное предсказание для любого вопроса"
        }
        
        spread_desc = spread_descriptions.get(spread_type, "Тарологический расклад")
        
        prompt = f"""
        Сделай тарологический расклад "{spread_name}".

        Описание расклада: {spread_desc}
        Вопрос пользователя: "{question}"

        Сгенерируй подробное, мудрое и эмпатичное предсказание. Структура:
        1. Краткая интерпретация расклада
        2. Основное предсказание (2-3 абзаца)
        3. Практический совет
        4. Общий вывод

        Будь точным, но добрым. Не используй негативные формулировки, вместо этого предлагай пути решения.
        Длина ответа: 300-500 слов.
        Отвечай на русском языке.
        """
        
        return prompt
    
    def _get_fallback_prediction(self, question: str, spread_name: str) -> str:
        """Запасное предсказание если модель не работает"""
        return f"""
🔮 *{spread_name}*

*Ваш вопрос:* {question}

*Предсказание:*
Карты указывают, что в вашей ситуации есть скрытые возможности для роста. 
Сейчас важно прислушаться к своей интуиции и довериться внутреннему голосу.

*Совет:*
Проявите терпение и будьте внимательны к знакам судьбы. Иногда ответы приходят 
неожиданным образом - через сны, случайные встречи или внутренние озарения.

*Вывод:*
Время перемен приносит новые возможности. Доверьтесь мудрости карт и собственной интуиции.
        """

async def main():
    try:
        logger.info("🚀 Starting bot with AI model...")
        
        # Инициализация бота
        bot = Bot(token=TOKEN)
        dp = Dispatcher(storage=MemoryStorage())
        
        # Инициализация модели Tarot
        logger.info("🔮 Initializing Tarot model...")
        tarot_model = TarotModel(api_key=HUGGINGFACEHUB_API_TOKEN)
        
        # Добавляем middleware для передачи модели
        model_middleware = ModelMiddleware(tarot_model)
        
        # Подключаем middleware ко всем типам сообщений
        router.message.middleware(model_middleware)
        router.callback_query.middleware(model_middleware)
        
        # Регистрируем роутеры
        dp.include_router(router)
        
        logger.info("🤖 Bot is ready to work!")
        logger.info("🔮 AI model is connected and ready to generate predictions!")
        
        # Запускаем бота
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"❌ Bot stopped with error: {e}")
        raise

if __name__ == '__main__': 
    os.makedirs("logs", exist_ok=True)
    
    setup_logging()
    
    try:
        logger.info("🎯 Starting application...")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⏹️ Bot stopped by user")
        print('Bot stopped')
    except Exception as e:
        logger.critical(f"💥 Unexpected error: {e}")
    finally:
        logger.info("🔚 Bot shutdown completed")