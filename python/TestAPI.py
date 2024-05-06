import requests
import time

def get_weather(api_key, city):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  
    }

    try:
        while True:
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                weather_data = response.json()

                weather_description = weather_data['weather'][0]['description']
                temperature = weather_data['main']['temp']
                humidity = weather_data['main']['humidity']

                print(f"Weather in {city}:")
                print(f"Description: {weather_description}")
                print(f"Temperature: {temperature} °C")
                print(f"Humidity: {humidity}%")
            else:
                print(f"Error: Failed to retrieve weather data (HTTP {response.status_code})")
                
            # Pause execution for 1 minute
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\nExiting...")
    except requests.RequestException as e:
        print(f"Error: {e}")

api_key = 'c321147f32bb6d31e61b897e4d724a3e'
city = 'Leiria'  
get_weather(api_key, city)
