import requests
from datetime import datetime

url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?'


start_time = input('Start_date: ')
end_time = input('End_date: ')
latitude = input('Latitude: ')
longitude = input('Longitude: ')
max_radius_km = input('Enter the radius:')
min_magnitude = input('Enter the min magnitude: ')

response = requests.get(url, headers={'Accept': 'application/json'}, params={
    'format': 'geojson',
    'starttime': start_time,
    'endtime': end_time,
    'latitude': latitude,
    'longitude': longitude,
    'maxradiuskm': max_radius_km,
    'minmagnitude': min_magnitude

})
if response.status_code != 200:
    print(f"Error: Received status code {response.status_code}")
    exit()

data = response.json()


earthquake_list = data['features']
count = 0
for earthquake in earthquake_list:
    time_in_milliseconds = earthquake['properties']['time']
    time_in_seconds = time_in_milliseconds / 1000
    date_time = datetime.fromtimestamp(
        time_in_seconds).strftime('%Y-%m-%d %H:%M:%S')
    print(
        f"{count}. Place: {earthquake ['properties']['place']}. Magnitude: {earthquake ['properties']['mag']}. Time:{date_time}")
    count += 1


# ПОПЫТКА 1
# import requests

# # получаем данные от пользователя
# start_date = input("Введите начальную дату в формате ГГГГ-ММ-ДД: ")
# end_date = input("Введите конечную дату в формате ГГГГ-ММ-ДД: ")
# min_magnitude = input("Введите минимальную магнитуду землетрясения: ")
# max_radius = input("Введите максимальный радиус поиска в километрах: ")
# countries = input("Введите имена стран через запятую: ").split(",")


# # формируем запрос к API
# url =f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date}&endtime={end_date}&magnitude={min_magnitude}'
# response = requests.get(url)


# # обрабатываем полученные данные
# if response.status_code != 200:
#     raise Exception("Ошибка: Не удалось получить данные с сервера")

# data = response.json()
# for feature in data['features']:
#     place = feature['properties']['place']
#     time = feature['properties']['time']
#     magnitude = feature['properties']['magnitude']
#     for country in countries:
#         if country.strip().lower() in place.lower():
#             print(f"Землетрясение в {place} произошло {time}. Магнитуда: {magnitude}")
#             break

# ПОПЫТКА 2
# import requests

# url= 'https://earthquake.usgs.gov/fdsnws/event/1/query?'
# params =  {


# 'startdate': "1990-01-01",
# 'endtime': "2022-04-04",
# 'latitude':39,
# 'longitude':60,
# 'max_radius':180
# }
# countries = ['Indonesia','United States','Russia','Turkmenistan','Turkey']


# for country in countries:
#     url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?'
# responce = requests.get(url, headers={'Accept':'application/json'})
# data = responce.json()

# for feature in data['features']:
#     if country in feature['properties']['place']:
#         print(f"Землятресение в {country}произошло в {feature['properties']['time']}")
