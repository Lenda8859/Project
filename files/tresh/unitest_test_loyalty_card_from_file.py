import unittest
import logging
from unitest_loyalty_card import LoyaltyCard

# Настройка логирования для тестов
logger = logging.getLogger('fileTestLogger')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('test_loyalty_card_from_file.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class TestLoyaltyCardFromFile(unittest.TestCase):

    def setUp(self):
        self.card = None

    def test_process_input_file(self):
        logger.info("Тестирование на основе файла ввода...")
        with open('input_data.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                key, value = line.strip().split(': ')
                if key == 'card_number':
                    self.card = LoyaltyCard(value)
                    self.assertIsNotNone(self.card)
                elif key == 'add_points':
                    points = int(value)
                    self.card.add_points(points)
                    self.assertEqual(self.card.points, points)
                elif key == 'add_discount':
                    discount = float(value)
                    self.card.add_discount(discount)
                    self.assertEqual(self.card.discount, discount)
                elif key == 'purchase':
                    amount = float(value)
                    result = self.card.purchase(amount)
                    expected_amount = amount * (1 - self.card.discount)
                    self.assertEqual(result, expected_amount)


if __name__ == '__main__':
    unittest.main()
