#Создание консольных приложений вида REPL


import csv
def load_zip_date(file_path):
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
            else:
                print(f"Пропуск почтового индекса {zip_code} из-за отсутствия координат")