import unittest
from unittest.mock import Mock, patch
from telegram import Update
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
if __name__ == '__main__':
    unittest.main()
