import discord
from discord.ext import commands
import random
from discord import File
from config import token

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Jmarche pas encore bb'))
    print("[Bot Status] Bot is now ON.")

@client.event
async def on_message(message):
    msgcont = message.content.lower()
    if message.content.endswith( "quoi" ):
        rndm=random.randint(0, 99)
        if rndm <= 4 :
            await message.channel.send(content=None, tts=False, embed=None, file=File('./images/feur.jpg'), files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        elif rndm == 69 :
            await message.channel.send(content=None, tts=False, embed=None, file=File('./videos/feur.mp4'), files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        else :
            await message.channel.send(content="feur", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)


client.run(token)