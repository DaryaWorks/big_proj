from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable
from typing_extensions import Awaitable


class TestMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, dict[str, any]], Awaitable[any]],  # для внутренниго
                       event: TelegramObject, # тип объекта 
                       data: dict[str, any]) -> any:
        print('Действия до одного обработчика')
        result = await handler(event, data) # наш обработчик
        print('Действия после обработчика')
        return result
