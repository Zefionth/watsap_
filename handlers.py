from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from recommendations import get_recommendations

async def start(update: Update, context: CallbackContext) -> None:
    """Отправляет приветственное сообщение с кнопками выбора категории."""
    keyboard = [
        [
            InlineKeyboardButton("Поиск аниме", callback_data='search_anime'),
            InlineKeyboardButton("Поиск фильмов", callback_data='search_movies')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Привет! Выберите категорию для поиска:", reply_markup=reply_markup
    )

async def handle_message(update: Update, context: CallbackContext) -> None:
    """Обрабатывает текстовые сообщения пользователя и отправляет рекомендации."""
    await update.message.reply_text("Ваш запрос обрабатывается…")
    query = update.message.text  # Получаем текст запроса

    # Определяем категорию поиска (аниме или фильмы)
    category = context.user_data.get('category', 'movies')  # Значение по умолчанию - "фильмы"

    # Получаем рекомендации в зависимости от категории
    recommendations = get_recommendations(query, category)

    if recommendations:
        context.user_data['recommendations'] = recommendations
        context.user_data['current_index'] = 0 
        await send_recommendation(update.message, context)
    else:
        await update.message.reply_text(
            "Извините, я не смог найти подходящие результаты. "
            "Попробуйте описать запрос по-другому. Для выбора другой категории напишите /start"
        )

async def send_recommendation(message, context: CallbackContext) -> None:
    """Отправляет текущую рекомендацию пользователю."""
    current_index = context.user_data['current_index']
    recommendations = context.user_data['recommendations']
    
    # Проверка, есть ли еще рекомендации
    if current_index < len(recommendations):
        item = recommendations[current_index]
        keyboard = [[InlineKeyboardButton("Далее", callback_data="next")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await message.reply_text(f"{item}", reply_markup=reply_markup)
    else:
        await message.reply_text(
            "Больше рекомендаций нет. "
            "Можете попробовать написать запрос по-другому или на другую тему. "
            "Для выбора другой категории напишите /start"
        )

async def button(update: Update, context: CallbackContext) -> None:
    """Обрабатывает нажатия на кнопки выбора категории и кнопку 'Далее'."""
    query = update.callback_query
    await query.answer()

    # Если выбрана категория "аниме"
    if query.data == 'search_anime':
        context.user_data['category'] = 'anime'
        await query.edit_message_text(text="Введите описание или название аниме для поиска.")
    
    # Если выбрана категория "фильмы"
    elif query.data == 'search_movies':
        context.user_data['category'] = 'movies'
        await query.edit_message_text(text="Введите описание или название фильма для поиска.")

    # Обработка кнопки "Далее" для показа следующей рекомендации
    elif query.data == 'next':
        context.user_data['current_index'] += 1
        await send_recommendation(query.message, context)
