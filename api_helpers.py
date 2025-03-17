import wikipediaapi
import requests
import datetime
import pytz

# OpenWeather API Key
OPENWEATHER_API_KEY = "5ad3ec78c422edd88c77f4df954bfc61"

def search_wikipedia(query):
    """Search Wikipedia using wikipedia-api."""
    wiki = wikipediaapi.Wikipedia("en")
    page = wiki.page(query)
    
    if page.exists():
        return page.summary[:300]  # Limit to 300 characters
    return "Sorry, I couldn't find anything on Wikipedia."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def get_weather(city):
    """Fetch weather data from OpenWeather API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        
        if data["cod"] == 200:
            weather = data["weather"][0]["description"].capitalize()
            temp = data["main"]["temp"]
            return f"The weather in {city} is {weather} with a temperature of {temp}°C."
        else:
            return "Couldn't fetch weather details. Please check the city name."
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

def get_current_time():
    """Returns the current time in IST (Indian Standard Time)."""
    try:
        ist = pytz.timezone("Asia/Kolkata")
        current_time = datetime.datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current time in IST is {current_time}."
    except Exception as e:
        return f"Error fetching time: {str(e)}"
