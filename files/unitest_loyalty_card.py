import logging

logging.basicConfig(filename='loyalty_card.log', level=logging.INFO)

class LoyaltyCard:
    def __init__(self, card_number):
        self.card_number = card_number
        self.points = 0
        self.discount = 0.0
        logging.info(f"Создана карта: {card_number}")

    def add_points(self, points):
        self.points += points
        logging.info(f"На карту {self.card_number} добавлено {points} баллов. Всего баллов: {self.points}")

    def add_discount(self, discount):
        self.discount += discount
        logging.info(f"На карту {self.card_number} добавлено {discount*100}% скидки. Всего скидка: {self.discount*100}%")

    def purchase(self, amount):
        logging.info(f"Покупка на сумму {amount} с карты {self.card_number}")
        if self.discount > 0:
            discounted_amount = amount * (1 - self.discount)
            logging.info(f"Скидка применена. Сумма после скидки: {discounted_amount}")
            return discounted_amount
        return amount

# Пример использования
if __name__ == '__main__':
    card = LoyaltyCard('12345')
    card.add_points(100)
    card.add_discount(0.1)
    print(f"Сумма к оплате после скидки: {card.purchase(100)}")
