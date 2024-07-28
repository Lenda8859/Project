import unittest
from model_airport import AirportModel

class TestAirportModel(unittest.TestCase):
    def setUp(self):
        self.model = AirportModel(
            host='localhost',
            user='your_username',
            password='your_password',
            database='your_database'
        )

    def tearDown(self):
        self.model.close_connection()

    def test_get_filtered_airports(self):
        min_lat, max_lat = 49.0, 50.0
        min_lon, max_lon = -93.0, -92.0
        airports = self.model.get_filtered_airports(min_lat, max_lat, min_lon, max_lon)
        # Assertions to check the result

    def test_get_flights_from_city(self):
        city = 'Dryden'
        flights = self.model.get_flights_from_city(city)
        # Assertions to check the result

    def test_get_routes(self):
        source_city = 'Dryden'
        destination_city = 'Toronto'
        routes = self.model.get_routes(source_city, destination_city)
        # Assertions to check the result

if __name__ == '__main__':
    unittest.main()
