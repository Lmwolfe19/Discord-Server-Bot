import youtube_dl
import discord
import os
from discord.ext import commands
from discord.utils import get

class Voice(commands.Cog):
    def __init__ (self, client):
         self.client = client
         self.voiceClients = {}
         self.players = {}

    # Commands
    @commands.command(pass_context=True, aliases=['j'])
    async def join(self, ctx):
        """Bot joins current voice channel. Use: '.join'"""
        voice_channel = ctx.author.voice.channel
        voice_state = get(self.client.voice_clients, guild=ctx.guild)

        if voice_state and voice_state.is_connected():
            await voice_state.move_to(voice_channel)
        else:
            voice_state = await voice_channel.connect()

        await ctx.send(f'Connected to: {voice_channel}')

        #self.voiceClients[ctx.guild.id] = await voice_channel.connect()

    @commands.command(pass_context=True, aliases=['l'])
    async def leave(self, ctx):
        """Bot leaves current voice channel. Use: '.leave'"""
        voice_channel = ctx.author.voice.channel
        voice_state = get(self.client.voice_clients, guild=ctx.guild)

        if voice_state and voice_state.is_connected():
            await voice_state.disconnect()
            await ctx.send(f'Disconnected from: {voice_channel}')
        else:
            await ctx.send("I don't think I'm in a voice channel...")

    @commands.command(pass_context=True, aliases=['p'])
    async def play(self, ctx, url: str):
        """W.I.P. -- Bot plays audio of given URL. Use: '.play <url>'"""
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                print("Removed old song file")
        except PermissionError:
            print("Tried to delete song file, but it's being played.")
            await ctx.send("I can't do that: that music is playing.")
            return

        await ctx.send("Preparing your song now.")

        voice_state = get(self.client.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])

        global name
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                print(f'Renamed file: {file}\n')
                os.rename(file, "song.mp3")

        voice_state.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print('Song has finished playing.'))
        voice_state.source = discord.PCMVolumeTransformer(voice_state.source)
        voice_state.source.volume = .1

        #nname = name.rsplit("-", 2)
        #await ctx.send(f'Playing: {nname}')
        print('Playing.\n')

    @commands.command(pass_context=True, aliases=['pa'])
    async def pause(self, ctx):
        voice_state = get(self.client.voice_clients, guild=ctx.guild)

        if voice_state and voice_state.is_playing():
            print("Music paused")
            voice_state.pause()
            await ctx.send("Music paused")
        else:
            print("Music not playing - failed pause.")
            await ctx.send("Music not playing!")

    @commands.command(pass_context=True, aliases=['r'])
    async def resume(self, ctx):
        voice_state = get(self.client.voice_clients, guild=ctx.guild)

        if voice_state and voice_state.is_paused():
            print("Music resumed.")
            voice_state.resume()
            await ctx.send("Music resumed.")
        else:
            print("Music not paused.")
            await ctx.send("Music is not paused you dingus.")

def setup(client):
    client.add_cog(Voice(client))

