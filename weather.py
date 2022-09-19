from tkinter import *
from tkinter import font
import requests
from datetime import datetime
from configparser import ConfigParser

# Initialise window

root = Tk()
root.geometry("500x500")
root.resizable(0, 0)
root.title("Python weather app")

city_value = StringVar()


def _get_api_key():
    config = ConfigParser()
    config.read("secrets.ini")
    return config["openweather"]["api_key"]

# format to local time


def format_time_to_location(utc):
    local_time = datetime.utcfromtimestamp(utc)
    return local_time.time()

# fetch weather


def showWeather():
    api_key = _get_api_key()
    city_name = city_value.get()

    weather_url = 'https://api.openweathermap.org/data/2.5/weather?q=' + \
        city_name + '&appid=' + api_key

    response = requests.get(weather_url)
    weather_info = response.json()
    tfield.delete('1.0', 'end')

    if weather_info['cod'] == 200:
        kelvin = 273

        temp = int(weather_info['main']['temp'] - kelvin)
        feels_like = int(weather_info['main']['feels_like'] - kelvin)
        pressure = weather_info['main']['pressure']
        humidity = weather_info['main']['humidity']
        wind_speed = weather_info['wind']['speed']
        sunrise = weather_info['sys']['sunrise']
        sunset = weather_info['sys']['sunset']
        timezone = weather_info['timezone']
        cloudy = weather_info['clouds']['all']
        description = weather_info['weather'][0]['description']

        sunrise_time = format_time_to_location(sunrise + timezone)
        sunset_time = format_time_to_location(sunset + timezone)

        weather = f'Weather of {city_name}:  \n - temperature of: {temp} degrees Celsius,  \n - feels like: {feels_like} degrees Celsius,  \n - pressure: {pressure},  \n - humidity: {humidity},  \n - wind speed: {wind_speed}, \n - description: {description} \n - cloudy: {cloudy}, \n - sunrise at: {sunrise_time}, \n - sunset at: {sunset_time}, \n - timezone: {timezone}'
        tfield.insert(INSERT, weather)


input_label = Label(root, text='Please enter a city',
                    font='arial 14 bold', pady=20).pack()
input_city = Entry(root, textvariable=city_value, width=24).pack()

Button(root, command=showWeather, text='Check weather', padx=5, pady=10).pack()

# display output

weather_now = Label(root, text='The weather is:',
                    font='arial 12 bold', padx=5).pack(pady=10)

tfield = Text(root, width=50, height=15)
tfield.pack()

root.mainloop()
