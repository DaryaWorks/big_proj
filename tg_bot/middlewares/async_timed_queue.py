# import asyncio
# from collections import deque
# from datetime import timedelta, datetime


# class AsyncTimedQueue[T: datetime]:
#     def __init__(self, max_age: timedelta):
#         self.max_age = max_age
#         self.q = deque[T]()
#         self._lock = asyncio.Lock()

#     @classmethod
#     def get_now(cls):
#         return datetime.now()

#     @classmethod
#     def get_age(cls, item: T) -> datetime:
#         return item

#     async def clear_old(self):
#         async with self._lock:
#             current_time = self.get_now()
#             while self.q and (current_time - self.get_age(self.q[0])) > self.max_age:
#                 self.q.popleft()

#     async def put(self, item: T) -> None:
#         await self.clear_old()
#         async with self._lock:
#             # async push
#             self.q.append(item)

#     async def peek(self) -> T | None:
#         await self.clear_old()
#         async with self._lock:
#             # async get
#             return self.q[0] if self.q else None

#     async def get_len(self) -> int:
#         await self.clear_old()
#         return len(self.q)


# middlewares/async_timed_queue.py
import asyncio
import time
from datetime import datetime, timedelta
from typing import Generic, TypeVar, List, Coroutine, Any
from collections import defaultdict

T = TypeVar('T')

class AsyncTimedQueue(Generic[T]):
    """
    Простая очередь с временными метками для ограничения частоты запросов
    """
    
    def __init__(self, max_age: timedelta):
        self.max_age = max_age
        self._items: List[tuple[datetime, T]] = []
    
    async def put(self, item: T) -> None:
        """Добавляет элемент с текущей временной меткой"""
        now = datetime.now()
        self._items.append((now, item))
        await self._cleanup()
    
    async def _cleanup(self) -> None:
        """Удаляет устаревшие элементы"""
        now = datetime.now()
        self._items = [(ts, item) for ts, item in self._items 
                      if now - ts < self.max_age]
    
    async def get_len(self) -> int:
        """Возвращает количество элементов в очереди"""
        await self._cleanup()
        return len(self._items)
    
    async def peek(self) -> datetime | None:
        """Возвращает временную метку первого элемента"""
        await self._cleanup()
        if self._items:
            return self._items[0][0]
        return None