from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import keyboards as kb
from tg_bot.middlelwares import TestMiddleware

router = Router() 

# для middleware 
router.message.outer_middleware(TestMiddleware())

# FSM для регистрации пользователя
class Reg(StatesGroup):
    name = State()
    number = State()

# FSM для создания расклада
class TarotReading(StatesGroup):
    waiting_for_question = State()
    choosing_spread = State()
    confirming_reading = State()

# обработчик команды старт
# @router.message(CommandStart())
# async def cmd_start(message: Message):
#     welcome_text = f"""
# ✨ Добро пожаловать, {message.from_user.first_name}! ✨

# Я — ваш цифровой таролог. 🔮

# Что я умею:
# • Давать предсказания по картам Таро
# • Проводить разные типы раскладов
# • Помогать найти ответы на ваши вопросы

# Выберите действие в меню ниже:
#     """
#     await message.answer_photo(
#         photo="/Users/rabotyazheva/Desktop/big_proj/tg_bot/IMG_1148.JPG",
#         caption=welcome_text,
#         reply_markup=kb.main_reply  
#     )
@router.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = f"""
✨ Добро пожаловать, {message.from_user.first_name} ✨

Я — твой личный таролог 🔮

Что я умею:
• Давать предсказания по картам Таро
• Проводить разные типы раскладов на твоего тюбика
• Помогать найти ответы на одни и те же вопросы

Выберите действие в меню ниже:
    """
    
    try:
        # Правильное использование FSInputFile
        photo = FSInputFile("/Users/rabotyazheva/Desktop/big_proj/tg_bot/IMG_1148.JPG")
        
        await message.answer_photo(
            photo=photo,
            caption=welcome_text,
            reply_markup=kb.main_reply  
        )
    except Exception as e:
        # Если возникла ошибка с фото, отправляем только текст
        print(f"Ошибка при отправке фото: {e}")
        await message.answer(
            welcome_text,
            reply_markup=kb.main_reply  
        )


# Обработчики главного меню
@router.message(F.text == '🔮 Получить предсказание')
async def get_prediction(message: Message):
    await message.answer(
        "Выберите тип расклада:",
        reply_markup=kb.spreads_main
    )

@router.message(F.text == '📚 О картах Таро')
async def about_tarot(message: Message):
    await message.answer(
        "Таро — это система символов, которая помогает заглянуть вглубь себя...",
        reply_markup=kb.help_keyboard
    )

@router.message(F.text == '✨ Популярные расклады')
async def popular_spreads(message: Message):
    await message.answer(
        "Вот самые популярные расклады:",
        reply_markup=await kb.inline_themes()
    )

@router.message(F.text == '❓ Помощь')
async def help_command(message: Message):
    await message.answer(
        "Чем я могу вам помочь?",
        reply_markup=kb.help_keyboard
    )

@router.message(F.text == '👤 Мой профиль')
async def my_profile(message: Message):
    await message.answer(
        "Ваш профиль:",
        reply_markup=kb.profile_keyboard
    )

# Обработчики инлайн-кнопок для предсказаний
@router.callback_query(F.data == 'get_prediction')
async def process_prediction_callback(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(
        "Выберите тип расклада:",
        reply_markup=kb.spreads_main
    )

@router.callback_query(F.data == 'about_tarot')
async def process_about_tarot(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(
        "🃏 *Карты Таро* — это древняя система символов, которая помогает:\n\n"
        "• 💭 Лучше понять себя и свои желания\n"
        "• 🔍 Увидеть скрытые аспекты ситуации\n"
        "• 🧭 Найти направление для развития\n"
        "• 🌟 Получить совет для принятия решений\n\n"
        "Каждая карта — это архетип, несущий глубокий смысл и мудрость.",
        parse_mode="Markdown",
        reply_markup=kb.back_button
    )

@router.callback_query(F.data == 'popular_spreads')
async def process_popular_spreads(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(
        "✨ Популярные расклады:",
        reply_markup=await kb.inline_themes()
    )

@router.callback_query(F.data == 'profile')
async def process_profile(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(
        f"👤 *Ваш профиль*\n\n"
        f"Имя: {callback_query.from_user.first_name}\n"
        f"ID: {callback_query.from_user.id}\n\n"
        f"📊 Статистика:\n"
        f"• Раскладов сделано: 0\n"
        f"• Избранных предсказаний: 0",
        parse_mode="Markdown",
        reply_markup=kb.profile_keyboard
    )

# Обработчики конкретных раскладов
@router.callback_query(F.data.startswith('spread_'))
async def process_spread_selection(callback_query: CallbackQuery, state: FSMContext):
    spread_type = callback_query.data
    
    spread_names = {
        'spread_one': '🎴 Расклад на одну карту',
        'spread_three': '🕒 Прошлое-Настоящее-Будущее',
        'spread_love': '💖 Расклад на отношения',
        'spread_career': '💼 Расклад на карьеру',
        'spread_advice': '🌙 Личный совет',
        'spread_custom': '🎯 Свободный вопрос'
    }
    
    spread_name = spread_names.get(spread_type, 'Расклад')
    
    await callback_query.answer(f"Выбран: {spread_name}")
    
    # Сохраняем тип расклада в состоянии
    await state.update_data(spread_type=spread_type, spread_name=spread_name)
    await state.set_state(TarotReading.waiting_for_question)
    
    await callback_query.message.edit_text(
        f"Вы выбрали: *{spread_name}*\n\n"
        f"📝 Теперь задайте ваш вопрос или опишите ситуацию:",
        parse_mode="Markdown",
        reply_markup=kb.cancel_keyboard
    )

# Обработчик тем для раскладов
@router.callback_query(F.data.startswith('theme_'))
async def process_theme_selection(callback_query: CallbackQuery, state: FSMContext):
    theme_index = int(callback_query.data.split('_')[1])
    themes = ['💖 Любовь и отношения', '💼 Карьера и деньги', '🏥 Здоровье', 
              '👥 Общение', '🎯 Личностный рост', '🌙 Общий расклад']
    
    selected_theme = themes[theme_index]
    
    await callback_query.answer(f"Тема: {selected_theme}")
    
    # Здесь можно сгенерировать предсказание
    await callback_query.message.edit_text(
        f"🔮 *{selected_theme}*\n\n"
        f"Ваше предсказание:\n\n"
        f"*Карта: Сила*\n"
        f"Эта карта говорит о внутренней силе и гармонии...\n\n"
        f"Помните: Таро показывает возможные пути, но выбор всегда за вами! 💫",
        parse_mode="Markdown",
        reply_markup=kb.feedback_keyboard
    )

# Навигация назад
@router.callback_query(F.data == 'back_to_main')
async def back_to_main(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(
        "Главное меню:",
        reply_markup=kb.main_inline
    )

@router.callback_query(F.data == 'back_to_spreads')
async def back_to_spreads(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(
        "Выберите тип расклада:",
        reply_markup=kb.spreads_main
    )

# Обработка состояний FSM для раскладов
@router.message(TarotReading.waiting_for_question)
async def process_question(message: Message, state: FSMContext):
    user_data = await state.get_data()
    spread_name = user_data.get('spread_name', 'Расклад')
    
    await message.answer(
        f"🔮 *{spread_name}*\n\n"
        f"*Ваш вопрос:* {message.text}\n\n"
        f"*Предсказание:*\n"
        f"Карты говорят, что вас ждут позитивные изменения...\n\n"
        f"💫 *Совет:* Доверьтесь своей интуиции!",
        parse_mode="Markdown",
        reply_markup=kb.feedback_keyboard
    )
    
    await state.clear()

@router.message(F.text == '❌ Отмена')
async def cancel_action(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    
    await state.clear()
    await message.answer(
        "Действие отменено.",
        reply_markup=kb.main_reply
    )

@router.callback_query(F.data.startswith('rate_'))
async def process_rating(callback_query: CallbackQuery):
    rating = callback_query.data.split('_')[1]
    await callback_query.answer(f"Спасибо за оценку: {rating} ⭐")
    await callback_query.message.edit_text(
        "Благодарим за обратную связь! 💫"
    )

@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer(
        "Помощь по использованию бота:",
        reply_markup=kb.help_keyboard
    )

@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer("🃏 Красивое изображение! Но я работаю с картами Таро, а не с фотографиями 😊")