import logging

logging.basicConfig(filename='orders.log', level=logging.INFO)

class Cafe:
    def __init__(self):
        self.menu = {
            'coffee': 0,
            'tea': 0,
            'latte': 0,
            'espresso': 0
        }

    def order(self, drink):
        if drink in self.menu:
            self.menu[drink] += 1
            logging.info(f"Заказ принят: {drink}")
            return True
        else:
            logging.warning(f"Напиток не найден в меню: {drink}")
            return False

    def get_statistics(self):
        return self.menu

# Пример использования
if __name__ == '__main__':
    cafe = Cafe()
    cafe.order('coffee')
    cafe.order('latte')
    cafe.order('tea')
    cafe.order('coffee')
    cafe.order('espresso')
    cafe.order('mocha')  # Этот напиток не в меню
    print(cafe.get_statistics())
