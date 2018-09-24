import discord
from discord.ext import commands
import youtube_dl

players = {}
queues = {}

def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()

class Voice:
    """
    Experimental Music Commands
    """
    def __init__(self, bot):
        self.bot = bot
        print('Module "{}" loaded'.format(self.__class__.__name__))

    @commands.command(pass_context=True)
    async def join(self, ctx):
        channel = ctx.message.author.voice.voice_channel
        await self.bot.join_voice_channel(channel)

    @commands.command(pass_context=True, aliases=["dc","disconnect","exit"])
    async def leave(self, ctx):
        if ctx.message.author.voice.voice_channel:
            server = ctx.message.server
            voice_client = self.bot.voice_client_in(server)
            await voice_client.disconnect()
        else:
            await self.bot.say(":x: You are not in a voice channel!")

    @commands.command(pass_context=True)
    async def play(self, ctx, url):
        server = ctx.message.server
        voice_client = self.bot.voice_client_in(server)
        player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
        players[server.id] = player
        player.start()

    @commands.command(pass_context=True)
    async def pause(self, ctx):
        if ctx.message.author.voice.voice_channel:
            id = ctx.message.server.id
            players[id].pause()
        else:
            await self.bot.say(":x: You are not in a voice channel!")

    @commands.command(pass_context=True)
    async def resume(self, ctx):
        if ctx.message.author.voice.voice_channel:
            id = ctx.message.server.id
            players[id].resume()
        else:
            await self.bot.say(":x: You are not in a voice channel!")

    @commands.command(pass_context=True)
    async def queue(self, ctx, url):
        server = ctx.message.server
        voice_client = self.bot.voice_client_in(server)
        player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
        if server.id in queues:
            queues[server.id].append(player)
        else:
            queues[server.id] = [player]
        await self.bot.say(":white_check_mark: Video queued!")

def setup(bot):
    bot.add_cog(Voice(bot))
