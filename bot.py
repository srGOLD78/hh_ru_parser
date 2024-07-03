from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, filters
import db
from db import save_vacancies, save_candidates, get_filtered_vacancies,create_database,clear_vacancies,clear_candidates,remove_duplicates_vacancies,remove_duplicates_candidates
from vacancies_parser import fetch_vacancies
from candidates_parser import fetch_candidates


TOKEN = "6867396131:AAF0uuuYw26_CKSiDZK69KRgRHDV_4DaQvA"

# Основные переменные для хранения состояний
WAITING_FOR_VACANCY_QUERY = "WAITING_FOR_VACANCY_QUERY"
WAITING_FOR_CANDIDATE_QUERY = "WAITING_FOR_CANDIDATE_QUERY"
WAITING_FOR_CANDIDATE_FILTERS = "WAITING_FOR_CANDIDATE_FILTERS"
WAITING_FOR_VACANCY_FILTERS = "WAITING_FOR_VACANCY_FILTERS"



# Функция для команды /start и главного меню
async def start(update: Update, context: CallbackContext) -> None:
    await main_menu(update, context)


# Функция для отображения главного меню
async def main_menu(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Поиск вакансий", callback_data='search_vacancies'),
            InlineKeyboardButton("Поиск соискателей", callback_data='search_candidates'),
        ],
        [
            InlineKeyboardButton("Аналитика", callback_data='analytics'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Выберите действие:', reply_markup=reply_markup)


# Функция для обработки нажатий на кнопки меню
async def menu_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'search_vacancies':
        await query.message.reply_text("Пожалуйста, введите название вакансии для поиска.")
        context.user_data['state'] = WAITING_FOR_VACANCY_QUERY
    elif query.data == 'search_candidates':
        await query.message.reply_text("Пожалуйста, введите название должности для поиска соискателей.")
        context.user_data['state'] = WAITING_FOR_CANDIDATE_QUERY
    elif query.data == 'analytics':
        await analytics(update, context)


# Обработчик текстовых сообщений
async def handle_text(update: Update, context: CallbackContext) -> None:
    state = context.user_data.get('state')

    if state == WAITING_FOR_VACANCY_QUERY:
        query = update.message.text
        await search_vacancies(update, context, query)
    elif state == WAITING_FOR_CANDIDATE_QUERY:
        query = update.message.text
        await search_candidates(update, context, query)
    elif state == WAITING_FOR_VACANCY_FILTERS:
        filters_text = update.message.text
        filters = parse_filters(filters_text)

        if not filters:
            await update.message.reply_text("Фильтры некорректны. Пожалуйста, попробуйте снова.")
            return
        await apply_filters_vacancies(update, context, filters)
    elif state == WAITING_FOR_CANDIDATE_FILTERS:
        filters_text = update.message.text
        filters = parse_filters(filters_text)  # Парсим фильтры из ввода пользователя

        if not filters:
            await update.message.reply_text("Фильтры некорректны. Пожалуйста, попробуйте снова.")
            return

        await apply_filters_candidates(update, context, filters)
    else:
        await update.message.reply_text("Пожалуйста, выберите действие из меню.")


# Функция для поиска вакансий
async def search_vacancies(update: Update, context: CallbackContext, query: str) -> None:
    await update.message.reply_text(f"Ищу вакансии по запросу: {query}")
    clear_vacancies()

    # Поиск вакансий
    vacancies = await fetch_vacancies(query, pages=70)
    if vacancies:
        save_vacancies(vacancies)
        await update.message.reply_text(
            "Вакансии сохранены. Введите фильтры в формате: `ключ значение`, например "
        "`city Москва, salary 100000-150000, experience 2-5`")
        context.user_data['state'] = WAITING_FOR_VACANCY_FILTERS
    else:
        response = "Вакансии не найдены."
        await update.message.reply_text(response, parse_mode='Markdown')
        context.user_data['state'] = None  # Сброс состояния
async def search_candidates(update: Update, context: CallbackContext, query: str) -> None:
    await update.message.reply_text(f"Ищу соискателей по запросу: {query}")
    clear_candidates()

    # Поиск соискателей
    candidates = await fetch_candidates(query, pages=70)
    if candidates:
        save_candidates(candidates)
        await update.message.reply_text(
            "Соискатели сохранены. Введите фильтры в формате: `ключ значение`, например "
        "`age 30-40,experience 10-20, salary 100000-150000,`")
        context.user_data['state'] = WAITING_FOR_CANDIDATE_FILTERS
    else:
        response = "Соискатели не найдены."
        await update.message.reply_text(response, parse_mode='Markdown')
        context.user_data['state'] = None  # Сброс состояния



# Функция для аналитики
async def analytics(update: Update, context: CallbackContext) -> None:
    vacancies_count = db.count_vacancies()
    candidates_count = db.count_candidates()
    average_salary_vacancies = db.calculate_average_salary_vacancies()
    average_salary_candidates = db.calculate_average_salary_candidates()

    response = (
        f"Аналитика:\n"
        f"Количество вакансий: {vacancies_count}\n"
        f"Количество соискателей: {candidates_count}\n"
        f"Средняя зарплата по вакансиям: {average_salary_vacancies:,.0f}\n"
        f"Средняя зарплата по соискателям: {average_salary_candidates:,.0f}\n"
    )

    await update.callback_query.message.reply_text(response)


# Функция для парсинга фильтров из пользовательского ввода
def parse_filters(filters_text):
    filters = {}
    parts = filters_text.split(',')

    for part in parts:
        elements = part.strip().split()
        if len(elements) != 2:
            print(f"Некорректный фильтр: '{part}'. Ожидается формат 'ключ значение'.")
            continue

        key, value = elements
        if '-' in value:
            try:
                filters[key] = tuple(map(int, value.split('-')))
            except ValueError:
                print(f"Некорректное значение диапазона: '{value}'. Ожидается формат 'число-число'.")
                continue
        else:
            filters[key] = value

    return filters


# Функция для применения фильтров и вывода результатов
async def apply_filters_vacancies(update: Update, context: CallbackContext, filters: dict) -> None:
    filtered_vacancies = get_filtered_vacancies(filters)
    remove_duplicates_vacancies()
    if filtered_vacancies:
        response = "Вакансии с применёнными фильтрами:\n\n"
        for idx, vacancy in enumerate(filtered_vacancies[:20], 1):  # Ограничим вывод первыми 20 вакансиями
            response += f"{idx}. [{vacancy['title']}]({vacancy['link']}) в {vacancy['company']}\n Город: {vacancy['city']}\n Зарплата: {vacancy['salary']}\n Опыт: {vacancy['experience']}\n"
    else:
        response = "Вакансии с применёнными фильтрами не найдены."

    await update.message.reply_text(response, parse_mode='Markdown')
    context.user_data['state'] = None  # Сброс состояния

async def apply_filters_candidates(update: Update, context: CallbackContext, filters: dict) -> None:
    filtered_candidates = db.get_filtered_candidates(filters)
    remove_duplicates_candidates()
    if filtered_candidates:
        response = "Соискатели с применёнными фильтрами:\n\n"
        for idx, candidate in enumerate(filtered_candidates[:20], 1):  # Ограничим вывод первыми 20 вакансиями
            response += f"{idx}. [{candidate['title']}]({candidate['link']})\n - Опыт: {candidate['experience']}\n - Зарплата:{candidate['salary']}\n - Возраст: {candidate['age']}\n"
    else:
        response = "Соискатели с применёнными фильтрами не найдены."

    await update.message.reply_text(response, parse_mode='Markdown')
    context.user_data['state'] = None  # Сброс состояния


# Глобальный обработчик ошибок
async def error_handler(update: Update, context: CallbackContext) -> None:

    if update.message:
        await update.message.reply_text("Произошла ошибка, попробуйте снова позже.")
    elif update.callback_query:
        await update.callback_query.message.reply_text("Произошла ошибка, попробуйте снова позже.")


if __name__ == '__main__':
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(menu_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    application.add_error_handler(error_handler)


    application.run_polling()
