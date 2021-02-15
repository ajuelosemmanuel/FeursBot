import discord, asyncio, random, os
import speech_recognition as sr
from discord.ext import commands
from discord import File
from config import token
from feetlinks import pied
from pathlib import Path
from discord.ext.tasks import loop
from pytube import YouTube
from googletrans import Translator
from moviepy.editor import *
from pydub import AudioSegment
from pydub.silence import split_on_silence

number_txt_file = Path.cwd() / 'number.txt'
number_txt_file.touch(exist_ok=True)
number = int(number_txt_file.open('r').read() or 0)
waves_folder = (Path.cwd() / 'recordings')
waves_file_format = "recording{}.wav"
waves_folder.mkdir(parents=True, exist_ok=True)
sr_folder = (Path.cwd() / 'sr')
sr_folder.mkdir(parents=True, exist_ok=True)
sr_file_format = "sr{}{}.wav"

discord.opus.load_opus("opus")

client = commands.Bot(command_prefix = '.')
client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Jmarche pas encore bb'))
    print("[Bot Status] Bot is now ON.")

@client.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title = "Help", description = "Use .help <command> for extended information.")
    em.add_field(name = "Voice", value = "join, leave, feurTestVoc")
    em.add_field(name = "Fun", value = "ching, pieds, banger")
    em.add_field(name = "Misc", value = "servers, compOrale")
    await ctx.send(embed = em)

@help.command()
async def join(ctx):
    em = discord.Embed(title = "Join", description = "Make the bot join the voice channel you're in (requires you to be in a voice channel).")
    em.add_field(name = "**Syntax**", value = ".join")
    await ctx.send(embed = em)

@help.command()
async def leave(ctx):
    em = discord.Embed(title = "Leave", description = "Make the bot leave the voice channel you're in (requires you to be in a voice channel).")
    em.add_field(name = "**Syntax**", value = ".leave")
    await ctx.send(embed = em)

@help.command()
async def feurTestVoc(ctx):
    em = discord.Embed(title = "FeurTestVoc", description = "!!NOT WORKING WELL!! Make the bot listen to what you say and he'll write down what he heard (requires you to be in a voice channel). He only understands French, and it's not working well at the moment.")
    em.add_field(name = "**Syntax**", value = ".feurTestVoc")
    await ctx.send(embed = em)

@help.command()
async def ching(ctx):
    em = discord.Embed(title = "Ching", description = "-_-")
    em.add_field(name = "**Syntax**", value = ".ching")
    await ctx.send(embed = em)

@help.command()
async def pieds(ctx):
    em = discord.Embed(title = "Pieds", description = "Sends a random feet pic.")
    em.add_field(name = "**Syntax**", value = ".pieds")
    await ctx.send(embed = em)

@help.command()
async def banger(ctx):
    em = discord.Embed(title = "Banger", description = "Plays an ABSOLUTE banger in the vc (requires you to be in a voice channel).")
    em.add_field(name = "**Syntax**", value = ".banger")
    await ctx.send(embed = em)

@help.command()
async def servers(ctx):
    em = discord.Embed(title = "Servers", description = "Writes the number of servers Feurs is in.")
    em.add_field(name = "**Syntax**", value = ".servers")
    await ctx.send(embed = em)

@help.command()
async def compOrale(ctx):
    em = discord.Embed(title = "CompOrale", description = "Given a youtube link and a language, will write what is said in the video in the chat - language format : https://cloud.google.com/speech-to-text/docs/languages")
    em.add_field(name = "**Syntax**", value = ".compOrale <youtube_url> <lang>")
    em.add_field(name = "**Exemple**", value = ".compOrale  https://www.youtube.com/watch?v=A13GOPxm0d4&ab_channel=PolarbearSuburbs de-DE")
    await ctx.send(embed = em)

@help.command()
async def translate(ctx):
    em = discord.Embed(title = "Translate", description = "Translates a message in a given language (format for supported languages : https://cloud.google.com/translate/docs/languages ). The -pronunciation option will provide a pronunciation if possible. It will not work on long messages and on not supported languages.")
    em.add_field(name = "**Syntax**", value = ".translate <message> [option : -pronunciation] <language>")
    await ctx.send(embed = em)

@client.command(pass_context=True)
async def compOrale(ctx, url, lang):
    mp4 = YouTube(url).streams.get_highest_resolution().download()
    mp3 = mp4.split(".mp4", 1)[0] + f".wav"
    video_clip = VideoFileClip(mp4)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(mp3)
    audio_clip.close()
    video_clip.close()
    os.remove(mp4)
    r = sr.Recognizer()
    sound = AudioSegment.from_wav(mp3)
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened, language=lang)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                await ctx.send(text)
    os.remove(mp3)

@client.command()
async def translate(ctx, *args):
    translator = Translator(service_urls=['translate.googleapis.com'])
    args = list(args)
    destLang = args.pop(-1)
    if args[-1] == "-pronunciation":
        args.pop(-1)
        msg = " ".join(args[:])
        await ctx.send(translator.translate(msg, dest=destLang).text)
        await ctx.send(translator.translate(msg, dest=destLang).pronunciation)
    else:
        msg = " ".join(args[:])
        await ctx.send(translator.translate(msg, dest=destLang).text)

@client.command()
async def join(ctx):
    author = ctx.message.author
    channel = author.voice.channel
    await channel.connect()
    print("i'm in the voice channel")

@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()
    print("i'm out of the voice channel")

@client.command()
async def ching(ctx):
    await ctx.send('chong')

@client.command()
async def pieds(ctx):
    await ctx.send(f'{random.choice(pied)}')

@client.command()
async def servers(ctx):
  servers = list(client.guilds)
  await ctx.send(f"Connected on {str(len(servers))} servers")

@client.command()
async def feurTestVoc(ctx, me_only: bool = True):
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()
    sr_file = sr_folder / sr_file_format.format(ctx.author, number)
    sr_file.touch()
    fp = sr_file.open('rb')
    if not me_only:
        ctx.voice_client.listen(discord.UserFilter(discord.WaveSink(str(sr_file)), ctx.author))
    else:
        ctx.voice_client.listen(discord.WaveSink(str(sr_file)))
    await asyncio.sleep(7)
    ctx.voice_client.stop_listening()
    r = sr.Recognizer()
    with sr.AudioFile(fp) as source:
        print("Allez parle :")
        audio = r.record(source)
        try:
            text = r.recognize_google(audio, language="fr-FR")
            await ctx.send("Tu viens de dire : {}".format(text))
            print("Tu viens de dire : {}".format(text))
            if text.endswith('quoi'):
                voice = ctx.channel.guild.voice_client
                voice.play(discord.FFmpegPCMAudio(executable="YOURFFMPEGPATH", source="./audio/feurManu.mp3"))
        except:
            await ctx.send("j'ai pas capté le sang")

@client.command()
async def banger(ctx):
    await ctx.author.voice.channel.connect()
    voice = ctx.channel.guild.voice_client
    voice.play(discord.FFmpegPCMAudio(executable="YOURFFMPEGPATH", source="./audio/tektonik.mp3"))

@loop(seconds=4)
async def save_number_loop():
    global number
    with number_txt_file.open('w') as fp:
        fp.write(str(number))
    if len(list(waves_folder.iterdir())) > 10:
        print("Deleting recording files as the recording file's count got above 10.")
        for item in waves_folder.iterdir():
            # print(item)
            item.unlink()
        number = 0

@client.event
async def on_message(message):
    if (message.author.bot):
        return
    else:
        msg = message.content.lower()
        if msg.endswith( "quoi" ):
            rndm=random.randint(0, 99)
            if rndm <= 4 :
                await message.channel.send(content=None, tts=False, embed=None, file=File('./images/feur.jpg'), files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
            elif rndm == 69 :
                await message.channel.send(content=None, tts=False, embed=None, file=File('./videos/feur.mp4'), files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
            else :
                await message.channel.send(content="feur", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if msg.endswith( "bon" ):
            await message.channel.send(content="duelle", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if msg.endswith( "toi" ):
            rndm=random.randint(0,1)
            if rndm == 1:
                await message.channel.send(content="ture", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
            else:
                await message.channel.send(content="lettes", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if msg.endswith( "oui" ):
            await message.channel.send(content="stiti", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if msg.endswith( "non" ):
            await message.channel.send(content="bril", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if msg.endswith( "ouais" ) or msg.endswith( "oe" ) or msg.endswith( "ouai" ):
            await message.channel.send(content="stern", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if msg.endswith( "yo" ):
            await message.channel.send(content="plait", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if msg.endswith( "tg" ):
            rndm=random.randint(0,1)
            if rndm == 1:
                await message.channel.send(content="v", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
            else:
                await message.channel.send(content="rard Depardieu ^^", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if (msg == "v" ):
            await message.channel.send(content="tt", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if (msg ==  "a" ) or (msg == "ah" ):
            await message.channel.send(content="beille", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if msg.endswith( "moi" ):
            await message.channel.send(content="ssonneuse", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if msg.endswith( "hein" ):
            await message.channel.send(content="2 3 soleil", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if msg.endswith( "si" ):
            await message.channel.send(content="tron", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if msg.endswith( "qui" ):
            await message.channel.send(content="rikou", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if msg.endswith( "ça" ) or msg.endswith( "sa" ):
            await message.channel.send(content="lope", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if (msg == "re" ):
            await message.channel.send(content="nard", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if msg.endswith( "mais" ):
            await message.channel.send(content="téo", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        if msg.endswith( "vois" ):
            await message.channel.send(content="ture", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
        #if (msg == "!wa" ):
            #await message.channel.send(content="rex le giga dog ? bah non c'est plutôt toi le chien avec tes filles manga", tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
    await client.process_commands(message)

client.run(token)
