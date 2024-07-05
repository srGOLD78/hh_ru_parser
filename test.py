import unittest
from unittest.mock import Mock, patch
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import bot


class TestBotFunctions(unittest.TestCase):

    @patch('bot.save_vacancies')
    def test_save_vacancies(self, mock_save_vacancies):
        update = Mock(spec=Update)
        context = Mock(spec=CallbackContext)

        bot.save_vacancies(update, context)

        mock_save_vacancies.assert_called_once()

    @patch('bot.fetch_vacancies')
    def test_fetch_vacancies(self, mock_fetch_vacancies):
        update = Mock(spec=Update)
        context = Mock(spec=CallbackContext)

        bot.fetch_vacancies(update, context)

        mock_fetch_vacancies.assert_called_once()

    @patch('bot.fetch_candidates')
    def test_fetch_candidates(self, mock_fetch_candidates=None):
        update = Mock(spec=Update)
        context = Mock(spec=CallbackContext)

        bot.fetch_candidates(update, context)

        mock_fetch_candidates.assert_called_once()

    @patch('bot.save_candidates')
    def test_save_candidates(self, mock_save_candidates=None):
        update = Mock(spec=Update)
        context = Mock(spec=CallbackContext)
        bot.save_candidates(update, context)
        mock_save_candidates.assert_called_once()
    @patch('bot.main_menu')
    async def test_start(self, mock_main_menu):
        update = Mock(spec=Update)
        context = Mock(spec=CallbackContext)
        await bot.start(update, context)
        mock_main_menu.assert_called_once_with(update, context)

    @patch('telegram.Update')
    @patch('telegram.CallbackQuery')
    async def test_main_menu(self, mock_update, mock_callback_query):
        update = mock_update
        context = Mock(spec=CallbackContext)
        await bot.main_menu(update, context)
        mock_callback_query.message.reply_text.assert_called_with(
            'Выберите действие:',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Поиск вакансий", callback_data='search_vacancies'),
                 InlineKeyboardButton("Поиск соискателей", callback_data='search_candidates')],
                [InlineKeyboardButton("Аналитика", callback_data='analytics')]
            ])
        )

    @patch('bot.search_vacancies')
    @patch('bot.search_candidates')
    @patch('bot.analytics')
    async def test_menu_handler(self, mock_analytics, mock_search_candidates, mock_search_vacancies):
        query = Mock()
        query.data = 'search_vacancies'
        update = Mock()
        update.callback_query = query
        context = Mock(spec=CallbackContext)
        await bot.menu_handler(update, context)
        mock_search_vacancies.assert_called_once()
        query.data = 'search_candidates'
        await bot.menu_handler(update, context)
        mock_search_candidates.assert_called_once()
        query.data = 'analytics'
        await bot.menu_handler(update, context)
        mock_analytics.assert_called_once()
    @patch('bot.search_vacancies')
    @patch('bot.search_candidates')
    async def test_handle_text_vacancies(self, mock_search_vacancies, mock_search_candidates):
        update = Mock()
        context = Mock()
        context.user_data = {'state': bot.WAITING_FOR_VACANCY_QUERY}
        update.message.text = "Программист"
        await bot.handle_text(update, context)
        mock_search_vacancies.assert_called_once_with(update, context, "Программист")
        context.user_data = {'state': bot.WAITING_FOR_CANDIDATE_QUERY}
        update.message.text = "Менеджер"
        await bot.handle_text(update, context)
        mock_search_candidates.assert_called_once_with(update, context, "Менеджер")
    @patch('bot.parse_filters')
    @patch('bot.apply_filters_vacancies')
    async def test_apply_filters_vacancies(self, mock_apply_filters_vacancies, mock_parse_filters):
        update = Mock()
        context = Mock()
        context.user_data = {'state': bot.WAITING_FOR_VACANCY_FILTERS}
        update.message.text = "city Москва, salary 100000-150000, experience 2-5"
        mock_parse_filters.return_value = {'city': 'Москва', 'salary': (100000, 150000), 'experience': (2, 5)}
        await bot.handle_text(update, context)
        mock_apply_filters_vacancies.assert_called_once_with(update, context,
                                                             {'city': 'Москва', 'salary': (100000, 150000),
                                                              'experience': (2, 5)})
    @patch('bot.analytics')
    async def test_analytics(self, mock_analytics):
        update = Mock()
        context = Mock()
        await bot.analytics(update, context)
        mock_analytics.assert_called_once_with(update, context)
    @patch('bot.search_vacancies')
    @patch('db.clear_vacancies')
    async def test_search_vacancies(self, mock_clear_vacancies, mock_search_vacancies):
        update = Mock()
        context = Mock()
        query = "Developer"
        await bot.search_vacancies(update, context, query)
        mock_clear_vacancies.assert_called_once()
        mock_search_vacancies.assert_called_once_with(query, pages=3)
    @patch('bot.search_candidates')
    @patch('db.clear_candidates')
    async def test_search_candidates(self, mock_clear_candidates, mock_search_candidates):
        update = Mock()
        context = Mock()
        query = "Manager"
        await bot.search_candidates(update, context, query)
        mock_clear_candidates.assert_called_once()
        mock_search_candidates.assert_called_once_with(query, pages=3)
if __name__ == '__main__':
    unittest.main()
