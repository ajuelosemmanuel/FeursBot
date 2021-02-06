import discord
from discord.ext import commands
import random
from discord import File
from config import token
from feetlinks import pied

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Jmarche pas encore bb'))
    print("[Bot Status] Bot is now ON.")


@client.command()
async def ching(ctx):
    await ctx.send('chong')

@client.command()
async def pieds(ctx):
    await ctx.send(f'{random.choice(pied)}')

@client.event
async def on_message(message):
    if (message.author.bot):
        a=1
    else:
        msgcont = message.content.lower()
        if message.content.endswith( "quoi" ):
            rndm=random.randint(0, 99)
            if rndm <= 4 :
                await message.channel.send(content=None, tts=False, embed=None, file=File('./images/feur.jpg'), files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
            elif rndm == 69 :
                await message.channel.send(content=None, tts=False, embed=None, file=File('./videos/feur.mp4'), files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
            else :
                await message.channel.send(content="feur", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if message.content.endswith( "bon" ):
            await message.channel.send(content="duelle", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if message.content.endswith( "toi" ):
            rndm=random.randint(0,1)
            if rndm == 1:
                await message.channel.send(content="ture", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
            else:
                await message.channel.send(content="lettes", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if message.content.endswith( "oui" ):
            await message.channel.send(content="stiti", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if message.content.endswith( "non" ):
            await message.channel.send(content="bril", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if message.content.endswith( "ouais" ) or message.content.endswith( "oe" ) or message.content.endswith( "ouai" ):
            await message.channel.send(content="stern", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if message.content.endswith( "yo" ):
            await message.channel.send(content="plait", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if message.content.endswith( "tg" ):
            rndm=random.randint(0,1)
            if rndm == 1:
                await message.channel.send(content="v", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
            else:
                await message.channel.send(content="rard Depardieu ^^", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if (message.content == "v" ):
            await message.channel.send(content="tt", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if (message.content ==  "a" ) or (message.content == "ah" ):
            await message.channel.send(content="beille", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if message.content.endswith( "moi" ):
            await message.channel.send(content="ssoneuse", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if message.content.endswith( "hein" ):
            await message.channel.send(content="2 3 soleil", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if message.content.endswith( "si" ):
            await message.channel.send(content="tron", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if message.content.endswith( "qui" ):
            await message.channel.send(content="rikou", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if message.content.endswith( "ça" ) or message.content.endswith( "sa" ):
            await message.channel.send(content="lope", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if (message.content == "re" ):
            await message.channel.send(content="nard", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
    await client.process_commands(message)


client.run(token)