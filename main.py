import discord
import requests
import json
import asyncio

# import base64

from datetime import datetime
from discord.ext import commands


# bot token
token_file = open("bot_secret", 'r')
TOKEN = token_file.read()

# creating the bot
client = commands.Bot(command_prefix="!")
comanda_salut = 'salut'
pseudonim = []
correct = ''


@client.event
async def on_ready():
    print('bot is online')


@client.command(aliases=['Salut', 'SALUT'])
async def salut(ctx):
    print(f'Utilizatorul {ctx.author.nick} a folosit comanda "salut".')
    await ctx.send(f'Salut, {ctx.author.mention}, have nice day')


@client.command()
async def test(ctx):
    print(ctx.message.content)
    print(ctx.author)
    print(ctx.message.id)

    message_reference = discord.MessageReference.from_message(ctx.message)
    print(message_reference.message_id)

    # await ctx.message.add_reaction('♦️')
    # await ctx.message.add_reaction('♦️')
    # await ctx.message.add_reaction('♣️')
    # await ctx.message.add_reaction('♥️')
    # await ctx.message.add_reaction('♠️')
    # await reply(reference=message_reference)
    # await ctx.reply(reference=ctx.message['id'])
    await ctx.message.reply("text")


@client.command(aliases=['q'])
async def question(ctx):
    r = requests.get('https://opentdb.com/api.php?amount=1&type=boolean')
    # r = requests.get('https://opentdb.com/api.php?amount=10&encode=')
    quiz = json.loads(r.text)
    global correct
    correct = quiz['results'][0]["correct_answer"]
    intrebare = quiz['results'][0]['question']
    # print(quiz['results'][0]['question'])
    await ctx.send(content=f"True or False: {intrebare}")
    # await asyncio.sleep(1)
    # global delete_flag
    # delete_flag = True
    # await ctx.message.add_reaction('✔️')
    # await ctx.message.add_reaction('❌')


# @client.command()
# async def join(ctx):
#     pass
# #    ctx.message.author


@client.listen()
async def on_reaction_add(reaction, user):
    answer = {'👍': 'True', '👎': 'False'}
    # print('test1')
    if not user.bot:
        # print('test2')
        for each in user.roles:
            if each.name == 'Player':
                # print('test3')
                acum = int(datetime.now().timestamp())
                if acum - timer_start >= 1:
                    await reaction.message.channel.send(content=f'{user.mention} too late to answer!')
                if answer[reaction.emoji] == correct:

                    # Totul functioneaza pana aici, dar trebuie sa gasesc o metoda pentru:
                    # a face un scor bazat pe timp
                    # a limita perioada de raspuns
                    # a reseta un flag de raspuns la intrebare noua - prevent double-answer

                    # print('test4 True')

                    player_score = acum - timer_start
                    print(f'Score: {player_score}')
                else:
                    print('test4 False')
                    await reaction.message.channel.send(content=f'{user.mention} Wrong answer, better luck next time!')


@client.listen()
async def on_message(message):
    if message.author.bot:
        if 'True or False: ' in message.content:
            global timer_start
            timer_start = int(datetime.now().timestamp())
            await message.add_reaction('👍')
            await message.add_reaction('👎')
            await asyncio.sleep(30)
            await message.delete()


# Aici am testat sa vad daca se pot inregistra multiple instante de on_message
# In hindsight, era destul de previzibil. Cred ca on_message e un template inherited.

# @client.listen()
# async def on_message(message):
#     if not message.author.bot:
#         await message.reply(content=f'Finally, a human!')


# # commands are defined before running
client.run(TOKEN)
