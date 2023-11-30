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

@bot.command()
async def hello(ctx):
    await ctx.send('Hello sir! hope you are having a great day!')  

@bot.command()
async def weather(ctx: commands.Context, *, city):
    print("Weather command invoked with city:", city)

    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": key,
        "q": city
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as res:
            data = await res.json()
            
            print("API Response:", data)  # Add this line for debugging

            location = data.get("location", {}).get("name")
            if not location:
                print("Error: Location not found in API response.")
                await ctx.send("Error: Location not found.")
                return

            temp_c = data.get("current", {}).get("temp_c")
            temp_f = data.get("current", {}).get("temp_f")
            humidity = data.get("current", {}).get("humidity")
            wind_kph = data.get("current", {}).get("wind_kph")
            condition = data.get("current", {}).get("condition", {}).get("text")
            image_url = "http:" + data.get("current", {}).get("condition", {}).get("icon")

            embed = discord.Embed(title=f"Weather for {location}", description=f"The condition in {location} is {condition}")
            embed.add_field(name="Temperature", value=f"C: {temp_c} | F: {temp_f}")
            embed.add_field(name="Humidity", value=f"{humidity}")
            embed.add_field(name="Wind Speeds", value=f"{wind_kph}")
            embed.set_thumbnail(url=image_url)

            await ctx.send(embed=embed)


bot.run(token)