from aiogram import BaseMiddleware, types
from aiogram.fsm.context import FSMContext
from typing import Any, Callable, Dict, Optional
from typing_extensions import Awaitable
from datetime import datetime, timedelta
from collections import defaultdict
import time


class ReadingLimiterMiddleware(BaseMiddleware):
    
    def __init__(self, max_readings: int = 5, time_window: int = 3600):
        super().__init__()
        self.max_readings = max_readings
        self.time_window = time_window  
        self.user_readings = defaultdict(list)
    
    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: Dict[str, Any]
    ) -> Any:
        
        # Всегда пропускаем команды и помощь
        if await self._should_skip_message(event):
            return await handler(event, data)
        
        if not event.from_user:
            return await handler(event, data)
        
        user_id = event.from_user.id
        
        # Очищаем старые записи
        self._clean_old_readings(user_id)
        
        # Проверяем лимит только для запросов на расклады
        if await self._is_reading_related(event, data):
            if not self._can_make_reading(user_id):
                remaining_time = self._get_remaining_time(user_id)
                await event.answer(
                    "❌ Вы превысили лимит раскладов!\n\n"
                    f"Можно сделать только {self.max_readings} раскладов в час.\n"
                    f"Следующий расклад будет доступен через {remaining_time}\n\n"
                    "Используйте раздел '✨ Популярные расклады' для бесплатных предсказаний 🔮"
                )
                return
            
            self._register_reading(user_id)
        
        return await handler(event, data)
    
    async def _should_skip_message(self, event: types.Message) -> bool:
        """Пропускает команды и служебные сообщения"""
        if not event.text:
            return False
            
        if event.text.startswith('/'):
            return True
        
        main_menu_buttons = ['📚 О картах Таро', '❓ Помощь', '👤 Мой профиль', '✨ Популярные расклады']
        if event.text in main_menu_buttons:
            return True
        
        if event.text == '❌ Отмена':
            return True
            
        return False
    
    async def _is_reading_related(self, event: types.Message, data: Dict[str, Any]) -> bool:
        """Определяет, связано ли сообщение с созданием расклада"""

        if event.text == '🔮 Получить предсказание':
            return True
        
        state: Optional[FSMContext] = data.get('state')
        if state is not None:
            current_state = await state.get_state()
            if current_state and "TarotReading:waiting_for_question" in current_state:
                return True
            
        return False
    
    def _clean_old_readings(self, user_id: int):
        """Удаляет старые записи раскладов"""
        now = time.time()
        self.user_readings[user_id] = [
            ts for ts in self.user_readings[user_id] 
            if now - ts < self.time_window
        ]
    
    def _can_make_reading(self, user_id: int) -> bool:
        """Проверяет, может ли пользователь сделать расклад"""
        return len(self.user_readings[user_id]) < self.max_readings
    
    def _register_reading(self, user_id: int):
        """Регистрирует выполнение расклада"""
        self.user_readings[user_id].append(time.time())
    
    def _get_remaining_time(self, user_id: int) -> str:
        """Возвращает оставшееся время до следующего расклада"""
        if not self.user_readings[user_id]:
            return "сейчас"
        
        readings = sorted(self.user_readings[user_id])
        if len(readings) >= self.max_readings:
            oldest_valid_reading = readings[0]
            remaining = self.time_window - (time.time() - oldest_valid_reading)
            
            if remaining <= 0:
                return "сейчас"
            elif remaining < 60:
                return f"{int(remaining)} секунд"
            elif remaining < 3600:
                minutes = int(remaining / 60)
                return f"{minutes} минут"
            else:
                hours = int(remaining / 3600)
                minutes = int((remaining % 3600) / 60)
                return f"{hours} часов {minutes} минут"
        
        return "сейчас"
    
    def get_remaining_readings(self, user_id: int) -> int:
        """Возвращает оставшееся количество раскладов"""
        self._clean_old_readings(user_id)
        return max(0, self.max_readings - len(self.user_readings[user_id]))
    
    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Возвращает полную статистику пользователя"""
        self._clean_old_readings(user_id)
        return {
            'readings_count': len(self.user_readings[user_id]),
            'limit': self.max_readings,
            'remaining': self.max_readings - len(self.user_readings[user_id]),
            'next_reading_in': self._get_remaining_time(user_id)
        }