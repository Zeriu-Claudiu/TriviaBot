from discord.ext import commands

# bot token
token_file = open("bot_secret", 'r')
TOKEN = token_file.read()

client = commands.Bot(command_prefix="!")


@client.event
async def on_ready():
    print('bot is online')


@client.command(aliases=['Salut', 'SALUT'])
async def salut(ctx):
    print(f'Utilizatorul {ctx.author.nick} a folosit comanda "salut".')
    await ctx.send(f'Salut, {ctx.author.mention}, have nice day')

#commands are defined before running
client.run(TOKEN)
