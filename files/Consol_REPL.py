#Создание консольных приложений вида REPL

import csv
<<<<<<< HEAD
import requests
import io
=======
import os
>>>>>>> 29c515b431a0c46d576edf118894d49faef3895f

def load_zip_date(file_path):
    zip_data = {}
    response = requests.get(file_path)
    if response.status_code == 200:
        csvfile = io.StringIO(response.text)
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
        print(f"Почтовый индекс {zip_code} находиться в {location['город']}, {location['штат']}, {location['округ']}, округе")
        print(f"Координаты: ({location['широта']}°, {location['долгота']}°)")
    else:
        print("Неверный или неизвестный почтовый индекс")

<<<<<<< HEAD
file_path = 'https://raw.githubusercontent.com/Lenda8859/Project/main/files/zip_codes_states.csv'
=======
file_path = './zip_codes_states.csv'
>>>>>>> 29c515b431a0c46d576edf118894d49faef3895f
zip_data = load_zip_date(file_path)


#print(zip_data['00603'])

def zip(city, state, zip_data):
    found_zip_codes = [zip_code for zip_code, info in zip_data.items() if info['город'].lower() and info['штат'].lower() == state.lower()]
    if found_zip_codes:
        print(f"Следущий почтовый индекс найденный для {city}, {state}: {', '.join(found_zip_codes)}")
    else:
        print(f"Почтовый индекс не найден для {city}, {state}")

from math import radians, sin, cos, sqrt, atan2

def haversin(lat1, lon1, lat2, lon2):
    R = 3958.8 # Радиус земли в милях
    dlat = radians(lat2-lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def dist(zip1, zip2, zip_data):
    if zip1 in zip_data and zip2 in zip_data:
        lat1, lon1 = zip_data[zip1]['широта'], zip_data[zip1]['долгота']
        lat2, lon2 = zip_data[zip2]['широта'], zip_data[zip2]['долгота']
        distance = haversin(lat1, lon1, lat2, lon2)
        print(f"Расстояние между {zip1} и {zip2} составляет {distance:.2f} миль")
    else:
        print(f"Невозможно определить расстояние между {zip1} и {zip2}")

#dist('19465', '12180', zip_data)

#zip1 = input("Введите почтовый индекс: ")
#zip2 = input("Введите почтовый индекс: ")

#dist(zip1, zip2, zip_data)

def repl(zip_data):
    while True:
        command = input("command ('loc', 'zip', 'dist', 'end') => ").strip().lower()
        if command == 'loc':
            zip_code = input("Введите почтовый индекс для поиска =>").strip()
            loc(zip_code, zip_data)
        elif command == 'zip':
            city = input("Введите название города для поиска =>").strip()
            stat = input("Введите название штата для поиска =>").strip()
            zip(city, stat, zip_data)
        elif command == 'dist':
            zip1 = input("Введите первый почтовый индекс =>").strip()
            zip2 = input("Введите второй почтовый индекс =>").strip()
            dist(zip1, zip2, zip_data)
        elif command == 'end':
            print("Done")
            break
        else:
            print("Invalid command, ignoring")

repl(zip_data)




