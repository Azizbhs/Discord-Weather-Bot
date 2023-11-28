import discord
import os
from discord.ext import commands
import aiohttp
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('token')
key = os.getenv('KEY')


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('{0.user} is logged in!'.format(bot))

@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return
    
    if msg.content.startswith('!hello'):
        await msg.channel.send('Hello sir!')

@bot.command()
async def weather(ctx: commands.Context, *, city):
    url = "http://api.weatherapi.com/v1/current.json" 
    params = {
        "key": key,
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


bot.run(token)