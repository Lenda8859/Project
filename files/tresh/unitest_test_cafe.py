import unittest
import logging
from unitest_script_cafe import Cafe

logger = logging.getLogger('testLogger')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('test_cafe.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class TestCafe(unittest.TestCase):
    def setUp(self):
        self.cafe = Cafe()

    def test_order_success(self):
        logger.info("Тестирование успешного заказа...")
        result = self.cafe.order('coffee')
        self.assertTrue(result)
        self.assertEqual(self.cafe.get_statistics()['coffee'], 1)

    def test_order_failure(self):
        logger.info("Тестирование неудачного заказа...")
        result = self.cafe.order('mocha')
        self.assertFalse(result)
        self.assertNotIn('mocha', self.cafe.get_statistics())

    def test_multiple_orders(self):
        logger.info("Тестирование нескольких заказов...")
        self.cafe.order('coffee')
        self.cafe.order('latte')
        self.cafe.order('coffee')
        self.cafe.order('coffee')
        self.cafe.order('coffee')
        self.cafe.order('coffee')
        self.cafe.order('latte')
        status = self.cafe.get_statistics()
        self.assertEqual(status['coffee'], 5)
        self.assertEqual(status['latte'], 2)

if __name__ == '__main__':
    unittest.main()
