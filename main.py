import discord
import requests
import json
import asyncio

# import base64

from datetime import datetime
from discord.ext import commands

# global variables
correct = ''
lobby = []
question_flag = False
answer_window = 30

# bot token
token_file = open("bot_secret", 'r')
TOKEN = token_file.read()

# database initialization
pass

# intents allows us to access member attributes
intents = discord.Intents.default()
intents.members = True
# creating the bot
client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    # server = client.get_guild(848948035505225778)
    server = discord.utils.get(client.guilds, name='TriviaBot Server')
    global trivia_channel
    trivia_channel = discord.utils.get(server.text_channels, name='trivia-game')
    # print(server.id)
    global player_role
    player_role = discord.utils.get(server.roles, name='Player')
    # print(client.intents.members)
    # print(player_role.id)
    # print(player_role.members)

    print('bot is online')
    # end of init

# @client.command(aliases=['Salut', 'SALUT'])
# async def salut(ctx):
#     print(f'Utilizatorul {ctx.author.nick} a folosit comanda "salut".')
#     await ctx.send(f'Salut, {ctx.author.mention}, have nice day')


@client.command()
async def test(ctx):
    pass

    # message_reference = discord.MessageReference.from_message(ctx.message)
    # print(message_reference.message_id)
    # print(f'Question flag: {question_flag}')

    # await reply(reference=message_reference)
    # await ctx.reply(reference=ctx.message['id'])
    # await ctx.message.reply("text")


@client.command(aliases=['q'])
async def question(ctx):
    await ctx.message.delete()
    # this is where I check for who is playing - who has player role
    global lobby
    lobby = (discord.utils.get(ctx.guild.roles, name="Player")).members
    for each in lobby:
        each.answer_flag = False
    # await ctx.send(content='')
    global question_flag
    question_flag = True
    # request quiz in format json
    r = requests.get('https://opentdb.com/api.php?amount=1&type=boolean')
    # stringify
    quiz = json.loads(r.text)
    # memorat raspunsul la intrebare in variabila globala
    global correct
    correct = quiz['results'][0]["correct_answer"]
    intrebare = quiz['results'][0]['question']
    await trivia_channel.send(content=f"True or False: {intrebare}")

    # await asyncio.sleep(1)
    # await ctx.message.add_reaction('✔️')
    # await ctx.message.add_reaction('❌')


@client.listen()
async def on_message(message):
    if message.author.bot:
        if 'True or False: ' in message.content:
            global timer_start
            timer_start = int(datetime.now().timestamp())
            await message.add_reaction('👍')
            await message.add_reaction('👎')
            await asyncio.sleep(answer_window)
            await message.delete()
            global question_flag
            question_flag = False


@client.listen()
async def on_reaction_add(reaction, user):
    # dictionar raspunsuri
    answer = {'👍': 'True', '👎': 'False'}
    print('test1')
    if not user.bot:
        print('test2')
        if user.id in lobby:  # Teoretic, aici pot verifica daca a fost dat raspunsul
            # print('test3')
            # print(f'lobby: {lobby}')

            # inregistrarea perioadei de raspuns pentru timed score
            acum = int(datetime.now().timestamp())

            # if acum - timer_start >= answer_window:
            #     await reaction.message.channel.send(content=f'{user.mention} too late to answer!')

            if answer[reaction.emoji] == correct and not user.answer_flag:
                # print('test4 True')

                # Totul functioneaza pana aici, dar trebuie sa gasesc o metoda pentru:
                # a face un scor bazat pe timp
                # a limita perioada de raspuns - se sterge intrebarea dupa 30 sec - variabila answer_window
                # a reseta un flag de raspuns la intrebare noua to prevent double-answer

                player_score = acum - timer_start
                await reaction.message.channel.send(content=f'{user.mention} Correct! You got {player_score} points!')
            else:
                # print('test4 False')

                await reaction.message.channel.send(content=f'{user.mention} Wrong answer, better luck next time!')


# Aici am testat sa vad daca se pot inregistra multiple instante de on_message
# @client.listen()
# async def on_message(message):
#     if not message.author.bot:
#         await message.reply(content=f'Finally, a human!')


@client.command(aliases=['j'])
async def join(ctx):
    await ctx.message.author.add_roles(player_role)
    await trivia_channel.send(content=f"Welcome to the Trivia game! Please wait for next round.")


@client.command(aliases=['x'])
async def quit_game(ctx):
    await ctx.message.author.remove_roles(player_role)


# obsolete

# @client.event
# async def on_member_update(before, after):
#     # print(before.roles.name)
#     # print(after.roles)
#     for other in after.roles:
#         for each in before.roles:
#             if 'Player' not in each.name and "Player" in other.name:
#                 lobby.append(after.id)
#                 # print(f' adding to: {lobby}')
#                 break
#             if 'Player' not in other.name and 'Player' in each.name:
#                 lobby.pop(-1)
#                 # print(f'removed: {lobby}')
#                 break

# if 'Player' not in before.roles and "Player" in after.roles:
#     lobby.append(after.id)
#     print(lobby)
#
# if 'Player' in before.roles and "Player" not in after.roles:
#     lobby.pop(after.id)
#     print(lobby)


# # commands are defined before running
client.run(TOKEN)

# planuri de perspectiva si idei
"""
- script for product presentation
- rules channel with opt-in
- help command text + help channel
- multiple modalitati de scoring - timed, batch answers
- integrare gspread sa nu se piarda scoruri daca programul se opreste
- logging detaliat, poate reusesc sa folosesc eficient decoratorul facut la curs
- nu in ultimul rand, sa fac bazele alea de date!
"""
