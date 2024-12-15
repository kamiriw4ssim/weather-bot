import discord

import requests

import os



# Get your Discord token and weather API key from environment variables
TOKEN = os.getenv("TOKEN") or ""
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY") or ""

# Initialize the bot client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Function to get weather data
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        return None  # Invalid city name or other error

    main = data["main"]
    weather = data["weather"][0]
    temp = main["temp"]
    description = weather["description"]

    return f"The weather in {city} is {temp}°C with {description}."

# Event when the bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print(f"TOKEN: {TOKEN[:5]}...") 
    print(f"WEATHER_API_KEY: {WEATHER_API_KEY[:5]}...")

# Event when the bot receives a message
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!weather"):
        city = message.content[len("!weather "):].strip()  # Extract the city name
        if not city:
            await message.channel.send("Please provide a city name.")
            return

        weather_info = get_weather(city)
        if weather_info:
            await message.channel.send(weather_info)
        else:
            await message.channel.send(f"Could not find weather information for {city}. Please try again.")

# Run the bot
client.run(TOKEN)

