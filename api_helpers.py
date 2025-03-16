import requests
import datetime

# OpenWeather API (Get API Key from https://openweathermap.org/api)
OPENWEATHER_API_KEY = "5ad3ec78c422edd88c77f4df954bfc61"

# ChatGPT API (Get API Key from https://openai.com/)
OPENAI_API_KEY = "your_openai_api_key"

def get_weather(city):
    """Fetches weather information using OpenWeather API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        return "Couldn't fetch weather data."

    weather = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    return f"The weather in {city} is {weather} with a temperature of {temp}°C."

def search_wikipedia(query):
    """Fetches a short summary from Wikipedia."""
    search_term = query.replace("Tell me about", "").replace("Search Wikipedia for", "").strip()
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{search_term}"
    response = requests.get(url)
    data = response.json()

    if "extract" in data:
        return data["extract"]
    return "Sorry, I couldn't find anything on Wikipedia."

def get_time():
    """Returns the current time and date."""
    now = datetime.datetime.now()
    return f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}"

def ask_chatgpt(query):
    """Fetches a response from OpenAI's ChatGPT API."""
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    data = {"model": "gpt-4", "messages": [{"role": "user", "content": query}]}
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    return "ChatGPT is not available right now."
