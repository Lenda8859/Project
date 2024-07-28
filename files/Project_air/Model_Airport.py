
import mysql.connector
from typing import List, Tuple

class AirportDatabase:
    """
     Класс для работы с базой данных аэропортов.

     Атрибуты:
         connection: Подключение к базе данных.
         cursor: Курсор для выполнения SQL-запросов.
     """
    def __init__(self, user: str, password: str, host: str, database: str, port: int = 3306):
        """
        Инициализация подключения к базе данных.

        Параметры:
                user: Имя пользователя для подключения к базе данных.
                password: Пароль пользователя для подключения к базе данных.
                host: Хост базы данных.
                database: Имя базы данных.
                port: Порт подключения к базе данных (по умолчанию 3306).
        """
        self.connection = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            database=database,
            port=port
        )
        self.cursor = self.connection.cursor()

    def get_unique_latitudes(self) -> List[float]:
        # Получить уникальные значения широты из базы данных
        query = "SELECT DISTINCT latitude FROM airports ORDER BY latitude"
        self.cursor.execute(query)
        return [row[0] for row in self.cursor.fetchall()]

    def get_unique_longitudes(self) -> List[float]:
        # Получить уникальные значения долготы из базы данных
        query = "SELECT DISTINCT longitude FROM airports ORDER BY longitude"
        self.cursor.execute(query)
        return [row[0] for row in self.cursor.fetchall()]

    def get_airports_within_coordinates(self, min_lat: float, max_lat: float, min_lon: float, max_lon: float) -> List[Tuple[str, str, float, float, str, str, float, str]]:
        # Получить список аэропортов в заданных координатах
        query = ("SELECT city, country, latitude, longitude, iata, icao, elevation, region FROM airports "
                 "WHERE latitude BETWEEN %s AND %s AND longitude BETWEEN %s AND %s")
        self.cursor.execute(query, (min_lat, max_lat, min_lon, max_lon))
        return self.cursor.fetchall()

    def get_airports_by_city(self, city: str) -> List[Tuple[str, str, str, str, str, str, str, str]]:
        """
        Получить список аэропортов по городу.

            Параметры:
                city: Название города.

                Возвращает:
                Список кортежей с данными об аэропортах.
                Данные по городам, региону, IATA ICAO, широте , долготе.
        """
        if city:
            query = """
            SELECT 
                airport,
                city,
                country,
                latitude,
                longitude,
                iata,
                icao,
                elevation,
                region
            FROM 
                airports
            WHERE 
                city = %s
            """
            self.cursor.execute(query, (city,))
        else:
            query = """
            SELECT 
                airport,
                city,
                country,
                latitude,
                longitude,
                iata,
                icao,
                elevation,
                region
            FROM 
                airports
            """
            self.cursor.execute(query)  # Эта строка была пропущена
        return self.cursor.fetchall()


    def get_airports_by_country(self, country: str) -> List[Tuple[str, str, float, float, str, str, float, str]]:
        # Получить список аэропортов в указанной стране
        query = ("SELECT airport, city, country, latitude, longitude, iata, icao, elevation, region FROM airports "
                 "WHERE country LIKE %s")
        self.cursor.execute(query, (f"%{country}%",))
        return self.cursor.fetchall()

    def get_airports_by_name(self, airport: str) -> List[Tuple[str, str, str, str, str, str, str, str]]:
        if airport:
            query = """
            SELECT 
                airport,
                city,
                country,
                latitude,
                longitude,
                iata,
                icao,
                elevation,
                region
            FROM 
                airports
            WHERE 
                airport = %s
            """
            self.cursor.execute(query, (airport,))
        else:
            query = """
            SELECT 
                airport,
                city,
                country,
                latitude,
                longitude,
                iata,
                icao,
                elevation,
                region
            FROM 
                airports
            """
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_airlines_by_icao(self, icao: str) -> List[Tuple[str, str, str, str, str]]:
        # Получить список авиалиний по ICAO
        query = ("SELECT name, icao, callsign, active, country FROM airlines WHERE icao LIKE %s")
        self.cursor.execute(query, (f"%{icao}%",))
        return self.cursor.fetchall()

    def get_airlines_by_callsign(self, callsign: str) -> List[Tuple[str, str, str, str, str]]:
        # Получить список авиалиний по позывному (callsign)
        query = ("SELECT name, icao, callsign, active, country FROM airlines WHERE callsign LIKE %s")
        self.cursor.execute(query, (f"%{callsign}%",))
        return self.cursor.fetchall()

    def get_airlines_by_name(self, name: str) -> List[Tuple[str, str, str, str, str]]:
        # Получить список авиалиний по названию
        query = ("SELECT name, icao, callsign, active, country FROM airlines WHERE name LIKE %s")
        self.cursor.execute(query, (f"%{name}%",))
        return self.cursor.fetchall()

    def get_airlines_by_country(self, country: str) -> List[Tuple[str, str, str, str, str]]:
        # Получить список авиалиний по стране
        query = ("SELECT name, icao, callsign, active, country FROM airlines WHERE country LIKE %s")
        self.cursor.execute(query, (f"%{country}%",))
        return self.cursor.fetchall()

    def get_flights_between_cities(self, city1: str, city2: str) -> List[
        Tuple[str, str, str, str, str, str, str, str, str]]:
        """
        Получить список рейсов между двумя городами.

        Параметры:
                   city1: Название первого города.
                   city2: Название второго города.

        Возвращает:
                   Список кортежей с данными о рейсах.
        """
        query = """
           SELECT 
               r.airline,
               r.src_airport,
               a1.city AS source_city,
               a1.country AS source_country,
               a1.airport AS source_airport,
               r.dst_airport,
               a2.city AS dest_city,
               a2.country AS dest_country,
               a2.airport AS dest_airport
           FROM 
               routes r
           JOIN 
               airports a1 ON r.src_airport = a1.iata
           JOIN 
               airports a2 ON r.dst_airport = a2.iata
           WHERE 
               a1.city = %s AND a2.city = %s
           """
        self.cursor.execute(query, (city1, city2))
        return self.cursor.fetchall()

    def get_all_flights(self) -> List[Tuple[str, str, str, str, str, str, str, str, str]]:
        """
        Получить список всех рейсов.

        Возвращает:
            Список кортежей с данными о рейсах.
        """
        query = """
        SELECT 
            r.airline,
            r.src_airport,
            a1.city AS source_city,
            a1.country AS source_country,
            a1.airport AS source_airport,
            r.dst_airport,
            a2.city AS dest_city,
            a2.country AS dest_country,
            a2.airport AS dest_airport
        FROM 
            routes r
        JOIN 
            airports a1 ON r.src_airport = a1.iata
        JOIN 
            airports a2 ON r.dst_airport = a2.iata
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_flights_from_city(self, city: str) -> List[Tuple[str, str]]:
        # Получить список рейсов из указанного города
        query = ("""
            SELECT r.src_airport, r.dst_airport, a1.city AS source_city, a2.city AS dest_city
            FROM routes r
            JOIN airports a1 ON r.src_airport = a1.iata
            JOIN airports a2 ON r.dst_airport = a2.iata
            WHERE a1.city = %s
                """)
        self.cursor.execute(query, (city,))
        return self.cursor.fetchall()

    def close(self):
        """
        Закрыть подключение к базе данных.
        """
        self.cursor.close()
        self.connection.close()
