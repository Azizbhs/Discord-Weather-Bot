import discord
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents = intents)

@client.event
async def on_ready():
    print('{0.user} is here!'.format(client))

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return
    
    if msg.content.startswith('!hello'):
        await msg.channel.send('Hello sir!')

client.run(os.getenv('token'))