import requests

def get_aircraft_data():
    url = 'https://opensky-network.org/api/states/all'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('states', [])
    return []


# def get_flight_trajectory(icao24, start_time, end_time):
#     """
#     Получение данных о траектории полета по ICAO24 и меткам времени UNIX.
#     """
#     url = f"https://opensky-network.org/api/flights/aircraft?icao24={icao24}&begin={start_time}&end={end_time}"
#     response = requests.get(url)
#
#     if response.status_code == 200:
#         return response.json()  # Возвращаем список полётов
#     else:
#         return []
#
# import requests

def get_flight_trajectory(icao24, start_time_unix, end_time_unix):
    # URL API
    api_url = 'https://opensky-network.org/api/flights/aircraft'

    # Формирование параметров запроса
    params = {
        'icao24': icao24,
        'begin': start_time_unix,
        'end': end_time_unix
    }

    print(f"Запрос к API: {api_url}, Параметры: {params}")

    try:
        # Запрос данных у API
        response = requests.get(api_url, params=params)

        # Вывод статуса ответа
        print(f"Статус ответа API: {response.status_code}")

        # Обработка ошибки 404 (данные не найдены)
        if response.status_code == 404:
            print("Данные о полёте не найдены для данного временного интервала.")
            return []

        # Проверка успешности запроса
        if response.status_code == 200:
            # Вывод данных, полученных от API
            print(f"Ответ API (данные): {response.json()}")
            return response.json()
        else:
            # Логирование ошибки в случае неудачного запроса
            print(f"Ошибка API: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        # Логирование исключения в случае ошибки запроса
        print(f"Исключение при запросе к API: {e}")
        return []

def get_active_aircrafts():
    # URL для запроса всех активных самолётов
    url = 'https://opensky-network.org/api/states/all'

    try:
        # Запрос к API
        response = requests.get(url)
        if response.status_code == 200:
            aircrafts = response.json().get('states', [])
            return aircrafts
        else:
            print(f"Ошибка API: {response.status_code}")
            return []
    except Exception as e:
        print(f"Исключение при запросе к API: {e}")
        return []