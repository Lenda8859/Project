import sqlite3
from Model_Airport import AirportModel


def test_get_filtered_airports():
    # Путь к базе данных
    db_path = r'D:\_ITMO\Python-Расширенные возможности\Python\Exercises1\data_dump.sql'

    # Создаем экземпляр модели
    model = AirportModel(db_path)

    # Выполняем запросы
    min_lat, max_lat = 49.0, 50.0
    min_lon, max_lon = -93.0, -92.0
    print(f"Filtering airports with lat: ({min_lat}, {max_lat}) and lon: ({min_lon}, {max_lon})")

    airports = model.get_filtered_airports(min_lat, max_lat, min_lon, max_lon)
    print(f"Filtered airports: {airports}")


def test_get_routes():
    # Путь к базе данных
    db_path = r'D:\_ITMO\Python-Расширенные возможности\Demo\files\Project_air\air_base.bd'

    # Создаем экземпляр модели
    model = AirportModel(db_path)

    # Выполняем запросы
    source_city = 'Dryden'
    destination_city = 'Toronto'
    print(f"Getting routes from city: {source_city} to city: {destination_city}")

    routes = model.get_routes(source_city, destination_city)
    print(f"Routes: {routes}")


def test_get_flights_from_city():
    # Путь к базе данных
    db_path = r'D:\_ITMO\Python-Расширенные возможности\Python\Exercises1\data_dump.sql'

    # Создаем экземпляр модели
    model = AirportModel(db_path)

    # Выполняем запросы
    city = 'Dryden'
    print(f"Getting flights from city: {city}")

    flights = model.get_flights_from_city(city)
    print(f"Flights: {flights}")


if __name__ == "__main__":
    test_get_filtered_airports()
    test_get_routes()
    test_get_flights_from_city()
