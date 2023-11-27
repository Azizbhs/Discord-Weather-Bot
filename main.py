import discord
import os
from discord.ext import commands
import aiohttp

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents = intents)

API = 'YOUR_WEATHER_API_KEY'
WEATHER_API_ENDPOINT = 'https://api.openweathermap.org/data/2.5/weather'

@client.event
async def on_ready():
    print('{0.user} is logged in!'.format(client))

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return
    
    if msg.content.startswith('!hello'):
        await msg.channel.send('Hello sir!')

@client.command()
async def weather(ctx: commands.Context, *, city):
    url = "http://api.weatherapi.com/v1/current.json" 
    params = {
        "key": os.getenv('KEY'),     #can be wrong
        "q": city
    }
    
    async with aiohttp.ClientSession() as session: 
        async with session.get(url, params=params) as res:
           data = await res.json()

           location = data["location"]["name"]
           temp_c = data["current"]["temp_c"]
           temp_f = data["current"]["temp_f"]
           humidity = data["current"]["humidity"]
           wind_kph = data["current"]["wind_kph"]
           condition = data["current"]["condition"]["text"]
           image_url = "http:" + data["current"]["condition"]["icon"]

           embed = discord.Embed(title=f"weather for {location}", description=f"The condition in {location} is {condition}")
           embed.add_field(name="Temperature", value=f"C: {temp_c} | F: {temp_f}")
           embed.add_field(name="Humidity", value=f"{humidity}")
           embed.add_field(name="Wind Speeds", value=f"{wind_kph}")
           embed.set_thumbnail(url=image_url)

           await ctx.send(embed=embed)


client.run(os.getenv('token'))