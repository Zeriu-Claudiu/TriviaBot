from discord.ext import commands

# bot token
token_file = open("bot_secret", 'r')
TOKEN = token_file.read()

client = commands.Bot(command_prefix="!")


@client.event
async def on_ready():
    print('bot is online')






client.run(TOKEN)
