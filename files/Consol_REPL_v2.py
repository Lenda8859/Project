import csv
import requests
from math import radians, sin, cos, sqrt, atan2

def download_csv_from_github(url, local_filename):
    response = requests.get(url)
    response.raise_for_status()
    with open(local_filename, 'wb') as f:
        f.write(response.content)

def load_zip_data(file_path):
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
                    'широта': float(lat),
                    'долгота': float(lon),
                    'город': city,
                    'штат': state,
                    'округ': county
                }
            #else:
                #print(f"Пропуск почтового индекса {zip_code} из-за отсутствия координат")

    return zip_data

def loc(zip_code, zip_data):
    if zip_code in zip_data:
        location = zip_data[zip_code]
        print(f"Почтовый индекс {zip_code} находится в {location['город']}, {location['штат']}, {location['округ']} округе")
        print(f"Координаты: ({location['широта']}°, {location['долгота']}°)")
    else:
        print("Неверный или неизвестный почтовый индекс")

def zip_code_by_city(city, state, zip_data):
    found_zip_codes = [zip_code for zip_code, info in zip_data.items() if info['город'].lower() == city.lower() and info['штат'].lower() == state.lower()]
    if found_zip_codes:
        print(f"Следующие почтовые индексы найдены для {city}, {state}: {', '.join(found_zip_codes)}")
    else:
        print(f"Почтовые индексы не найдены для {city}, {state}")

def haversin(lat1, lon1, lat2, lon2):
    R = 3958.8 # Радиус земли в милях
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def dist(zip1, zip2, zip_data):
    if zip1 in zip_data and zip2 in zip_data:
        lat1, lon1 = zip_data[zip1]['широта'], zip_data[zip1]['долгота']
        lat2, lon2 = zip_data[zip2]['широта'], zip_data[zip2]['долгота']
        distance = haversin(lat1, lon1, lat2, lon2)
        print(f"Расстояние между {zip1} и {zip2} составляет {distance:.2f} миль")
    else:
        print(f"Невозможно определить расстояние между {zip1} и {zip2}")

def repl(zip_data):
    while True:
        command = input("Введите команду ('loc', 'zip', 'dist', 'end') => ").strip().lower()
        if command == 'loc':
            zip_code = input("Введите почтовый индекс для поиска => ").strip()
            loc(zip_code, zip_data)
        elif command == 'zip':
            city = input("Введите название города для поиска => ").strip()
            state = input("Введите название штата для поиска => ").strip()
            zip_code_by_city(city, state, zip_data)
        elif command == 'dist':
            zip1 = input("Введите первый почтовый индекс => ").strip()
            zip2 = input("Введите второй почтовый индекс => ").strip()
            dist(zip1, zip2, zip_data)
        elif command == 'end':
            print("Завершено")
            break
        else:
            print("Неверная команда, попробуйте еще раз")

# Загрузка CSV файла с GitHub и запуск основной функции
file_url = 'https://raw.githubusercontent.com/Lenda8859/Project/main/zip_codes_states.csv'
local_file_path = 'zip_codes_states.csv'
download_csv_from_github(file_url, local_file_path)
zip_data = load_zip_data(local_file_path)

repl(zip_data)
