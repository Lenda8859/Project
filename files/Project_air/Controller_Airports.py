from Model_Airport import AirportDatabase
from View_Airports import AirportView
from tkinter import Tk

class AirportController:
    """
    Контроллер для управления взаимодействием между моделью и представлением.
    """
    def __init__(self, db_config):
        """
        Инициализация контроллера и установка базы данных и представления.

        Параметры: db_config: Конфигурация для подключения к базе данных.
        """
        self.db = AirportDatabase(**db_config)
        self.root = Tk()
        self.view = AirportView(self.root)
        self.view.set_filter_command(self.apply_filter)
        self.view.set_city_search_command(self.search_by_city)
        self.view.set_country_search_command(self.search_by_country)
        self.view.set_airport_search_command(self.search_by_airport)
        self.view.set_airline_search_command(self.search_by_airline)
        self.view.set_flight_search_command(self.search_flights)

        # Заполнение координат для выпадающих списков
        latitudes = self.db.get_unique_latitudes()
        longitudes = self.db.get_unique_longitudes()
        if latitudes and longitudes:
            self.view.populate_coordinates(latitudes, longitudes)

    def apply_filter(self):
        """
        Применить фильтр для поиска аэропортов по координатам.
        """
        min_lat, max_lat, min_lon, max_lon = self.view.get_coordinates()
        if min_lat is not None and max_lat is not None and min_lon is not None and max_lon is not None:
            airports = self.db.get_airports_within_coordinates(min_lat, max_lat, min_lon, max_lon)
            self.view.display_airports(airports)

    def search_by_city(self):
        """
        Найти аэропорты по городу.
        """
        city = self.view.get_city()
        airports = self.db.get_airports_by_city(city)
        self.view.display_airports(airports)

    def search_by_country(self):
        """
        Найти аэропорты по стране.
        """
        country = self.view.get_country()
        airports = self.db.get_airports_by_country(country)
        self.view.display_airports(airports)

    def search_by_airport(self):
        """
        Найти аэропорты по названию аэропорта.
        """
        airport = self.view.get_airport()
        airports = self.db.get_airports_by_name(airport)
        self.view.display_airports(airports)

    def search_by_airline(self):
        """
        Найти авиалинии по названию авиалинии.
        """
        airline = self.view.get_airline()
        airlines = self.db.get_airlines_by_name(airline)
        self.view.display_airlines(airlines)

    def search_flights(self):
        """
        Найти рейсы между двумя городами или все рейсы из одного города.
        """
        city1, city2 = self.view.get_cities()
        if city1 and city2:
            flights = self.db.get_flights_between_cities(city1, city2)
        elif city1:
            flights = self.db.get_flights_from_city(city1)
        elif city2:
            flights = self.db.get_flights_from_city(city2)
        else:
            flights = self.db.get_all_flights()
        self.view.display_flights(flights)

    def run(self):
        """
        Запустить главный цикл приложения.
        """
        self.root.mainloop()

    def close(self):
        """
        Закрыть базу данных при завершении работы приложения.
        """
        self.db.close()

if __name__ == "__main__":
    db_config = {
        'user': 'KsuLenda',
        'password': 'mazda885889',
        'host': '127.0.0.1',
        'database': 'air_base',
        'port': 3306
    }
    controller = AirportController(db_config)
    controller.run()
    controller.close()
