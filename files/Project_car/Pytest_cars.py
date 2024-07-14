import pytest
import logging
from cars import Car, load_cars_from_file
from datetime import datetime, timedelta

# Настройка логирования для тестов
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('test_car.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def load_test_data(file_path):
    """
    Загружает данные об автомобилях из текстового файла.

    Args:
        file_path (str): Путь к текстовому файлу.

    Returns:
        list: Список данных об автомобилях.
    """
    cars = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith('#') or not line.strip():
                    continue
                data = line.strip().split(',')
                if len(data) < 5:
                    logging.warning(f"Некорректная строка в файле: {line.strip()}")
                    continue
                make = data[0]
                model = data[1]
                year = int(data[2])
                mileage = int(data[3])
                last_service_date = data[4]
                issues = data[5:]
                cars.append((make, model, year, mileage, last_service_date, issues))
    except FileNotFoundError as e:
        logging.error(f"Файл не найден: {e}")
    return cars

@pytest.fixture
def car_data():
    return [
        ("Toyota", "Camry", 2018, 16000, "2023-01-15", ["brake pads", "engine oil"]),
        ("Honda", "Civic", 2017, 14000, "2022-06-10", ["air filter"]),
        ("Ford", "Focus", 2019, 10000, "2023-07-20", [])
    ]

@pytest.fixture
def invalid_car_data():
    return [
        ("Toyota", "Camry", 2018, 16000, "invalid-date", ["brake pads", "engine oil"]),
        ("", "", 0, 0, "", [])
    ]

def test_car_maintenance(car_data, caplog):
    """
    Тестирует класс Car, проверяя логирование и корректность методов.

    Использует caplog для проверки сообщений лога.

    Args:
        car_data (list): Список данных об автомобилях.
        caplog (LogCaptureFixture): Фикстура для захвата логов.
    """
    for make, model, year, mileage, last_service_date, issues in car_data:
        car = Car(make, model, year, mileage, last_service_date, issues)

        with caplog.at_level(logging.INFO):
            # Проверка необходимости ТО
            needs_service = car.needs_service()
            expected_service_msg = f"{make} {model} нуждается в ТО." if needs_service else f"{make} {model} не нуждается в ТО."
            assert expected_service_msg in caplog.text

            # Проверка списка поломок
            reported_issues = car.report_issues()
            if issues:
                expected_issues_msg = f"{make} {model} имеет поломки: {', '.join(issues)}"
            else:
                expected_issues_msg = f"{make} {model} не имеет поломок."
            assert expected_issues_msg in caplog.text
            assert reported_issues == issues

            # Проверка даты следующего ТО
            next_service = car.calculate_next_service_date()
            expected_next_service_date = (datetime.strptime(last_service_date, '%Y-%m-%d') + timedelta(days=365)).strftime(
                '%Y-%m-%d')
            expected_next_service_msg = f"Следующая дата ТО для {make} {model} это {expected_next_service_date}."
            assert expected_next_service_msg in caplog.text
            assert next_service == expected_next_service_date

def test_car_maintenance_invalid_data(invalid_car_data, caplog):
    """
    Тестирует класс Car с некорректными данными, проверяя корректность обработки ошибок.

    Использует caplog для проверки сообщений лога.

    Args:
        invalid_car_data (list): Список некорректных данных об автомобилях.
        caplog (LogCaptureFixture): Фикстура для захвата логов.
    """
    for make, model, year, mileage, last_service_date, issues in invalid_car_data:
        try:
            car = Car(make, model, year, mileage, last_service_date, issues)
            with caplog.at_level(logging.INFO):
                # Проверка необходимости ТО
                needs_service = car.needs_service()
                expected_service_msg = f"{make} {model} нуждается в ТО." if needs_service else f"{make} {model} не нуждается в ТО."
                assert expected_service_msg in caplog.text

                # Проверка списка поломок
                reported_issues = car.report_issues()
                if issues:
                    expected_issues_msg = f"{make} {model} имеет поломки: {', '.join(issues)}"
                else:
                    expected_issues_msg = f"{make} {model} не имеет поломок."
                assert expected_issues_msg in caplog.text
                assert reported_issues == issues

                # Проверка даты следующего ТО
                next_service = car.calculate_next_service_date()
                expected_next_service_date = (datetime.strptime(last_service_date, '%Y-%m-%d') + timedelta(days=365)).strftime(
                    '%Y-%m-%d')
                expected_next_service_msg = f"Следующая дата ТО для {make} {model} это {expected_next_service_date}."
                assert expected_next_service_msg in caplog.text
                assert next_service == expected_next_service_date
        except ValueError as e:
            logging.error(f"Ошибка создания объекта Car: {e}")

# Пример использования
if __name__ == '__main__':
    # Проверка загрузки данных для тестов
    cars = load_test_data('car_data.txt')
    for car in cars:
        print(car)
