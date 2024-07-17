import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from app import app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_autocomplete(self):
        # Тестирование автодополнения с корректным вводом
        response = self.app.get('/autocomplete?term=new')
        data = response.get_json()
        self.assertEqual(data, ['New York'])

        # Тестирование автодополнения с частичным совпадением
        response = self.app.get('/autocomplete?term=sa')
        data = response.get_json()
        self.assertEqual(data, ['San Antonio', 'San Diego', 'San Jose'])

        # Тестирование автодополнения с регистронезависимостью
        response = self.app.get('/autocomplete?term=LoS')
        data = response.get_json()
        self.assertEqual(data, ['Los Angeles'])

    # Добавил один из возможных тестов.


if __name__ == '__main__':
    unittest.main()
