import datetime as dt
import requests
import tkinter as tk
from tkinter import messagebox


# Temperature conversion
def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = (celsius * 9/5) + 32
    return celsius, fahrenheit


# Fetch weather data
def fetch_weather():
    CITY = city_entry.get()

    if CITY == "":
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY

    try:
        response = requests.get(url).json()

        if response.get("cod") != 200:
            messagebox.showerror("Error", "City not found!")
            return

        temp_kelvin = response['main']['temp']
        temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)

        feels_like_kelvin = response['main']['feels_like']
        feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)

        humidity = response['main']['humidity']
        wind_speed = response['wind']['speed']
        description = response['weather'][0]['description']

        sunrise_time = dt.datetime.utcfromtimestamp(
            response['sys']['sunrise'] + response['timezone']
        )

        info_text.delete(1.0, tk.END)
        info_text.insert(tk.END, f"Weather Information for {CITY}\n\n")

        selected_options = [option_vars[i].get() for i in range(6)]

        if selected_options[0]:
            info_text.insert(tk.END,
                f"Temperature: {temp_celsius:.2f}°C / {temp_fahrenheit:.2f}°F\n")

        if selected_options[1]:
            info_text.insert(tk.END,
                f"Feels Like: {feels_like_celsius:.2f}°C / {feels_like_fahrenheit:.2f}°F\n")

        if selected_options[2]:
            info_text.insert(tk.END,
                f"Humidity: {humidity}%\n")

        if selected_options[3]:
            info_text.insert(tk.END,
                f"Wind Speed: {wind_speed} m/s\n")

        if selected_options[4]:
            info_text.insert(tk.END,
                f"Weather: {description}\n")

        if selected_options[5]:
            info_text.insert(tk.END,
                f"Sunrise Time: {sunrise_time}\n")

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong\n{e}")


# Exit function
def on_exit():
    root.destroy()


# API details
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = "YOUR_API_KEY_HERE"


# GUI Window
root = tk.Tk()
root.title("Python Weather Explorer")
root.geometry("500x500")
root.configure(bg="#e6e6e6")


# City input
city_label = tk.Label(root, text="Enter City Name:", bg="#e6e6e6", font=("Arial", 12))
city_label.pack(pady=5)

city_entry = tk.Entry(root, width=30, font=("Arial", 12))
city_entry.pack(pady=5)


# Options frame
options_frame = tk.Frame(root, bg="#e6e6e6")
options_frame.pack(pady=10)

option_vars = [tk.BooleanVar() for _ in range(6)]

option_labels = [
    "Temperature",
    "Feels Like Temperature",
    "Humidity",
    "Wind Speed",
    "Weather Description",
    "Sunrise Time"
]

for i, label in enumerate(option_labels):
    tk.Checkbutton(
        options_frame,
        text=label,
        variable=option_vars[i],
        bg="#e6e6e6"
    ).grid(row=i, column=0, sticky="w")


# Fetch button
fetch_button = tk.Button(
    root,
    text="Fetch Weather",
    command=fetch_weather,
    bg="#4CAF50",
    fg="white",
    width=20
)
fetch_button.pack(pady=10)


# Text output
info_text = tk.Text(root, height=12, width=65)
info_text.pack(pady=10)


# Exit button
exit_button = tk.Button(
    root,
    text="Exit",
    command=on_exit,
    bg="#ff3333",
    fg="white",
    width=20
)
exit_button.pack(pady=10)


# Start program
root.mainloop()
