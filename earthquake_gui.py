import tkinter as tk
from tkinter import ttk

import requests


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
    city = earthquake.get()

    # Получаем координаты города
    coordinates = geocode(city)
    if coordinates is None:
        # Выводим сообщение об ошибке в текстовое поле
        results_text.insert(
            'end', f'Не удалось найти координаты города {city}')
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
            # Выводим результаты в текстовое поле
            results_text.insert(
                'end', f'Землетрясение магнитуды {magnitude} произошло в {time}\n')
    else:
        # Выводим сообщение об ошибке в текстовое поле
        results_text.insert('end', 'Нет данных о землетрясениях')


# Код интерфейса
root = tk.Tk()

root.geometry('1000x400')
root.title('Earthquake')

earthquake = tk.StringVar(root)


# Text
earthquake_town = ttk.Label(root, text='Town: ')

earthquake_magnitude = ttk.Label(root, text='Magnitude: ')


# Input
earthquake_entry = ttk.Entry(root, width=20, textvariable=earthquake)
earthquake_entry.focus()

# Button
greeting_button = ttk.Button(root, text='Search', command=search_earthquake)

# Cancel button
cancel_button = ttk.Button(root, text='Cancel', command=root.destroy)

earthquake_town.pack(side='left', padx=0)
earthquake_entry.pack(side='left',padx=10)
greeting_button.pack(side='left',padx=15)
cancel_button.pack(side='left',padx=20)
earthquake_magnitude.pack(side='left', padx=20, expand=True)

root.mainloop()
