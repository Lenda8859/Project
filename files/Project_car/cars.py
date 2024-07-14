import json
import logging
from datetime import datetime, timedelta

logging.basicConfig(filename='service_car.log', level=logging.INFO)

class Car:
    def __init__(self, make, model, year, mileage, last_service_date, issues):
        """
        Инициализация автомобиля.

        Args:
            make (str): Марка автомобиля.
            model (str): Модель автомобиля.
            year (int): Год выпуска.
            mileage (int): Пробег автомобиля в километрах.
            last_service_date (str): Дата последнего ТО в формате 'YYYY-MM-DD'.
            issues (list): Список поломок.
        """
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.last_service_date = datetime.strptime(last_service_date, '%Y-%m-%d')
        self.issues = issues

    def needs_service(self):
        """
        Проверяет, нужно ли автомобилю ТО.

        Returns:
            bool: True, если автомобилю нужно ТО, иначе False.
        """
        next_service_date = self.last_service_date + timedelta(days=365)
        if datetime.now() > next_service_date or self.mileage >= 15000:
            logging.info(f"{self.make} {self.model} нуждается в ТО.")
            return True
        else:
            logging.info(f"{self.make} {self.model} не нуждается в ТО.")
            return False

    def report_issues(self):
        """
        Возвращает список поломок автомобиля.

        Returns:
            list: Список поломок.
        """
        if self.issues:
            logging.info(f"{self.make} {self.model} имеет поломки: {', '.join(self.issues)}")
        else:
            logging.info(f"{self.make} {self.model} не имеет поломок.")
        return self.issues

    def calculate_next_service_date(self):
        """
        Рассчитывает дату следующего ТО.

        Returns:
            str: Дата следующего ТО в формате 'YYYY-MM-DD'.
        """
        next_service = self.last_service_date + timedelta(days=365)
        logging.info(f"Следующая дата ТО для {self.make} {self.model} это {next_service.strftime('%Y-%m-%d')}.")
        return next_service.strftime('%Y-%m-%d')


def load_cars_from_file(file_path):
    """
    Загружает данные об автомобилях из файла JSON.

    Args:
        file_path (str): Путь к файлу JSON.

    Returns:
        list: Список объектов Car.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            car_data = json.load(file)
            cars = [Car(**data) for data in car_data]
            return cars
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Ошибка при загрузке данных из файла: {e}")
        return []

# Пример использования
if __name__ == '__main__':
    cars = load_cars_from_file('cars.json')

    for car in cars:
        print(f"{car.make} {car.model}:")
        print("  Нужно ТО:", car.needs_service())
        print("  Сообщенные поломки:", car.report_issues())
        print("  Следующая дата ТО:", car.calculate_next_service_date())
        print()
