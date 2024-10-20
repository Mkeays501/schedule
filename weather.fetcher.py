import requests # type: ignore
from typing import Dict

def get_weather(city_name: str, api_key: str) -> None:
    """
    Fetches and prints the weather data for the given city.

    Args:
        city_name (str): The name of the city to fetch the weather for.
        api_key (str): The OpenWeatherMap API key.

    Returns:
        None
    """
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    complete_url = f"{base_url}?q={city_name}&appid={api_key}&units=metric"
    try:
        response = requests.get(complete_url)
        response.raise_for_status()
        data: Dict[str, any] = response.json()

        if data["cod"] != "404":
            main = data["main"]
            weather = data["weather"][0]
            wind = data["wind"]

            temperature = main["temp"]
            pressure = main["pressure"]
            humidity = main["humidity"]
            weather_description = weather["description"]
            wind_speed = wind["speed"]

            print(f"Weather in {city_name}:")
            print(f"Temperature: {temperature} °C")
            print(f"Pressure: {pressure} hPa")
            print(f"Humidity: {humidity}%")
            print(f"Description: {weather_description.capitalize()}")
            print(f"Wind Speed: {wind_speed} m/s")
        else:
            print("City Not Found!")
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            print("Error: Unauthorized. Please check your API key.")
        else:
            print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    api_key = "29481b718b7affd6d901146f2b7712c7"  # Replace with your OpenWeatherMap API key
    city_name = input("Enter city name: ")
    get_weather(city_name, api_key)

