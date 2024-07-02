import csv
from math import radians, sin, cos, sqrt, atan2


class ZipCodeData:
    def __init__(self, file_path):
        # Инициализация: загружаем данные из файла
        self.zip_data = self.load_zip_data(file_path)

    def load_zip_data(self, file_path):
        # Загружаем данные из CSV файла
        zip_data = {}
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                zip_code = row['zip_code']
                lat = row['latitude']
                lon = row['longitude']
                city = row['city']
                state = row['state']
                county = row['county']

                if lat and lon:
                    zip_data[zip_code] = {
                        'latitude': float(lat),
                        'longitude': float(lon),
                        'city': city,
                        'state': state,
                        'county': county
                    }
        return zip_data

    def loc(self, zip_code):
        # Находим информацию о почтовом индексе
        location = self.zip_data.get(zip_code)
        if location:
            return (
                f"Почтовый индекс {zip_code} находиться в {location['city']}, {location['state']}, {location['county']} округе. "
                f"Координаты: ({location['latitude']}°, {location['longitude']}°)")
        else:
            return "Неверный или неизвестный почтовый индекс"

    def zip(self, city, state):
        # Находим почтовые индексы по городу и штату
        found_zip_codes = [zip_code for zip_code, info in self.zip_data.items()
                           if info['city'].lower() == city.lower() and info['state'].lower() == state.lower()]
        if found_zip_codes:
            return f"Следущтй почтовый индекс найденный для {city}, {state}: {', '.join(found_zip_codes)}"
        else:
            return f"Почтовый индекс не найден для {city}, {state}"

    def haversin(self, lat1, lon1, lat2, lon2):
        # Рассчитываем расстояние между двумя точками по их координатам
        R = 3958.8  # Радиус Земли в милях
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    def dist(self, zip1, zip2):
        # Находим расстояние между двумя почтовыми индексами
        location1 = self.zip_data.get(zip1)
        location2 = self.zip_data.get(zip2)
        if location1 and location2:
            lat1, lon1 = location1['latitude'], location1['longitude']
            lat2, lon2 = location2['latitude'], location2['longitude']
            distance = self.haversin(lat1, lon1, lat2, lon2)
            return f"Расстояние между {zip1} и {zip2} составляет {distance:.2f} миль"
        else:
            return "Невозможно определить расстояние между почтовыми индексами"


# Пример использования
file_path = r'D:\_ITMO\Python-Расширенные возможности\Demo\files\zip_codes_states.csv'
zipcode_data = ZipCodeData(file_path)
print(zipcode_data.loc('19465'))
print(zipcode_data.zip('Portland', 'ME'))
print(zipcode_data.dist('19465', '12180'))

if __name__ == '__main__':
    # Тестирование
    import unittest


    class TestZipCodeData(unittest.TestCase):
        def setUp(self):
            # Создаем объект ZipCodeData с тестовыми данными
            self.zipcode_data = ZipCodeData('test_zip_codes.csv')
            self.zipcode_data.zip_data = {
                '19465': {'latitude': 40.239, 'longitude': -75.595, 'city': 'Phoenixville', 'state': 'PA',
                          'county': 'Chester'},
                '12180': {'latitude': 42.728, 'longitude': -73.691, 'city': 'Troy', 'state': 'NY',
                          'county': 'Rensselaer'}
            }

        def test_loc(self):
            # Тестируем метод loc
            self.assertEqual(self.zipcode_data.loc('19465'),
                             "Zip code 19465 is located in Phoenixville, PA, Chester county. Coordinates: (40.239°, -75.595°)")
            self.assertEqual(self.zipcode_data.loc('99999'), "Invalid or unknown zip code")

        def test_zip(self):
            # Тестируем метод zip
            self.assertEqual(self.zipcode_data.zip('Phoenixville', 'PA'), "Zip codes found for Phoenixville, PA: 19465")
            self.assertEqual(self.zipcode_data.zip('Nonexistent', 'NY'), "No zip codes found for Nonexistent, NY")

        def test_dist(self):
            # Тестируем метод dist
            self.assertEqual(self.zipcode_data.dist('19465', '12180'),
                             "The distance between 19465 and 12180 is 204.14 miles")
            self.assertEqual(self.zipcode_data.dist('19465', '99999'),
                             "Unable to determine distance between the given zip codes")


    unittest.main()