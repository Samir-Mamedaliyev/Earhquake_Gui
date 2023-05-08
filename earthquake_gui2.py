import tkinter as tk
from tkinter import ttk
import requests
from datetime import datetime


def geocode(city):
    # Формируем URL для запроса геоданных города
    url = f'https://nominatim.openstreetmap.org/search/{city}?format=json&limit=1'

    # Отправляем запрос и получаем ответ в формате JSON
    response = requests.get(url).json()

    # Если ответ содержит результаты, извлекаем координаты города
    if len(response) > 0:
        latitude = response[0]['lat']
        longitude = response[0]['lon']
        return latitude, longitude
    else:
        return None


def search_earthquake():
    # Получаем название города из текстового поля
    city = city_entry.get()

    # Получаем координаты города
    coordinates = geocode(city)
    if coordinates is None:
        results_text.insert(
            'end', f'Не удалось найти координаты города {city}\n')
        return

    # Устанавливаем период времени, за который нужно получить данные о землетрясениях
    start_time = '2020-01-01'
    end_time = '2022-02-01'

    # Получаем данные о землетрясениях в указанной области и за указанный период времени
    latitude, longitude = coordinates
    url = f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_time}&endtime={end_time}&latitude={latitude}&longitude={longitude}&maxradiuskm=100'
    response = requests.get(url).json()

    # Обрабатываем результаты
    if 'features' in response:
        for feature in response['features']:
            magnitude = feature['properties']['mag']
            time = feature['properties']['time']
            results_text.insert(
                'end', f'Magnitude: {magnitude} произошло в {datetime.now().strftime("%H:%M:%S %d-%m-%Y")}\n')
    else:
        results_text.insert('end', 'Нет данных о землетрясениях\n')


# Код интерфейса
root = tk.Tk()

root.geometry('800x300')
root.title('Earthquake')

city_label = ttk.Label(root, text='Town: ')


magnitude_label = ttk.Label(root, text='Results:')
magnitude_label.pack()
                     
city_entry = ttk.Entry(root, width=20)
city_entry.focus()

search_button = ttk.Button(root, text='Cancel', command=root.destroy)

cancel_button = ttk.Button(root, text='Search', command=search_earthquake)

results_text = tk.Text(root, height=5, width=50)

city_label.pack(side='left', padx=0)
city_entry.pack(side='left', padx=5)
results_text.pack(side='left', padx=12,pady=5)
cancel_button.pack(side='left', padx=10)
search_button.pack(side='left', padx=15)

root.mainloop()
