from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# Главное меню (Inline версия)
main_inline = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='🔮 Получить предсказание', callback_data='get_prediction'),
        InlineKeyboardButton(text='📚 О картах Таро', callback_data='about_tarot')
    ],
    [
        InlineKeyboardButton(text='✨ Популярные расклады', callback_data='popular_spreads'),
        InlineKeyboardButton(text='👤 Мой профиль', callback_data='profile')
    ],
    [
        InlineKeyboardButton(text='❓ Помощь', callback_data='help')
    ]
])

# Главное меню (Reply клавиатура - появляется внизу)
main_reply = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='🔮 Получить предсказание')],
        [KeyboardButton(text='📚 О картах Таро'), KeyboardButton(text='✨ Популярные расклады')],
        [KeyboardButton(text='❓ Помощь'), KeyboardButton(text='👤 Мой профиль')]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

# Меню раскладов
spreads_main = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='🎴 Одна карта', callback_data='spread_one'),
        InlineKeyboardButton(text='🕒 Прошлое-Настоящее-Будущее', callback_data='spread_three')
    ],
    [
        InlineKeyboardButton(text='💖 Расклад на отношения', callback_data='spread_love'),
        InlineKeyboardButton(text='💼 Расклад на карьеру', callback_data='spread_career')
    ],
    [
        InlineKeyboardButton(text='🌙 Личный совет', callback_data='spread_advice'),
        InlineKeyboardButton(text='🎯 Свободный вопрос', callback_data='spread_custom')
    ],
    [
        InlineKeyboardButton(text='⬅️ Назад', callback_data='back_to_main')
    ]
])

themes = ['💖 Любовь и отношения', '💼 Карьера и деньги', '🏥 Здоровье', 
          '👥 Общение', '🎯 Личностный рост', '🌙 Общий расклад']

async def inline_themes():
    """Генератор инлайн-клавиатуры с темами"""
    keyboard = InlineKeyboardBuilder()
    for theme in themes:
        keyboard.add(InlineKeyboardButton(text=theme, callback_data=f'theme_{themes.index(theme)}'))
    keyboard.add(InlineKeyboardButton(text='⬅️ Назад', callback_data='back_to_spreads'))
    return keyboard.adjust(2).as_markup()

profile_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='📊 История раскладов', callback_data='history'),
        InlineKeyboardButton(text='⭐ Избранные предсказания', callback_data='favorites')
    ],
    [
        InlineKeyboardButton(text='⚙️ Настройки', callback_data='settings'),
        InlineKeyboardButton(text='💎 Премиум', callback_data='premium')
    ],
    [
        InlineKeyboardButton(text='⬅️ Назад', callback_data='back_to_main')
    ]
])

help_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='📖 Как работать с ботом', callback_data='help_howto'),
        InlineKeyboardButton(text='🎴 Виды раскладов', callback_data='help_spreads')
    ],
    [
        InlineKeyboardButton(text='📚 Значения карт', callback_data='help_cards'),
        InlineKeyboardButton(text='❓ Частые вопросы', callback_data='help_faq')
    ],
    [
        InlineKeyboardButton(text='📞 Поддержка', callback_data='help_support'),
        InlineKeyboardButton(text='⬅️ Назад', callback_data='back_to_main')
    ]
])

feedback_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='⭐ 1', callback_data='rate_1'),
        InlineKeyboardButton(text='⭐ 2', callback_data='rate_2'),
        InlineKeyboardButton(text='⭐ 3', callback_data='rate_3'),
        InlineKeyboardButton(text='⭐ 4', callback_data='rate_4'),
        InlineKeyboardButton(text='⭐ 5', callback_data='rate_5')
    ]
])

back_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ Назад', callback_data='back_to_main')]
])

cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='❌ Отмена')]],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Старая функция inline_level 
levels = ['💖 Расклад на отношения', '💼 Расклад на карьеру', '🌙 Личный совет']

async def inline_level():
    keyboard = InlineKeyboardBuilder()
    for level in levels:
        keyboard.add(InlineKeyboardButton(text=level, callback_data=f'level_{levels.index(level)}'))
    return keyboard.adjust(2).as_markup()