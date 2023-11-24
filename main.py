import discord

client = discord.Client()

@client.event
async def on_ready():
    print('{0.user} is here!'.format(client))

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return
    
    if msg.content.startswith('!hello'):