#Importing libraries
import discord
from discord.ext import commands
from sys import argv
import json

def check_owner(ctx):
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    ownerid = settings["bot_owner"]
    return ctx.message.author.id == ownerid

class Load:
    """
    Load commands.
    """
    def __init__(self, bot):
        self.bot = bot
        print('Module "{}" loaded'.format(self.__class__.__name__))

    @commands.command(hidden=True)
    @commands.check(check_owner)
    async def load(self, *, module : str):
        """Loads an addon."""
        try:
            if module[0:7] != "modules.":
                module = "modules." + module
            self.bot.load_extension(module)
            embed = discord.Embed(title='Extension loaded!', description='Extension "{}" has been loaded successfully.'.format(module), color=0x00ff99)
            embed.set_thumbnail(url='https://i.imgur.com/TVtrqXR.png')
            await self.bot.say(embed=embed)
        except Exception as e:
            embed = discord.Embed(title='Extension load failed!', description='Extension "{}" has failed to load.'.format(module), color=0xFF0000)
            embed.add_field(name='Error', value='\n{}: {}\n'.format(type(e).__name__, e), inline=True)
            embed.set_thumbnail(url='https://i.imgur.com/z2xfrsH.png')
            await self.bot.say(embed=embed)

    @commands.command(hidden=True)
    @commands.check(check_owner)
    async def unload(self, *, module : str):
        """Unloads an addon."""
        try:
            if module[0:7] != "modules.":
                module = "modules." + module
            if module == "modules.load":
                embed = discord.Embed(title='Woops!', description='I don\'t think you want to unload that!', color=0xFF0000)
                embed.set_thumbnail(url='https://i.imgur.com/z2xfrsH.png')
                await self.bot.say(embed=embed)
            else:
                self.bot.unload_extension(module)
                embed = discord.Embed(title='Extension unloaded!', description='Extension "{}" has been unloaded successfully.'.format(module), color=0x00ff99)
                embed.set_thumbnail(url='https://i.imgur.com/TVtrqXR.png')
                await self.bot.say(embed=embed)
        except Exception as e:
            embed = discord.Embed(title='Extension unload failed!', description='Extension "{}" has failed to unload.'.format(module), color=0xFF0000)
            embed.add_field(name='Error', value='\n{}: {}\n'.format(type(e).__name__, e), inline=True)
            embed.set_thumbnail(url='https://i.imgur.com/z2xfrsH.png')
            await self.bot.say(embed=embed)

    @commands.command(name='reload', hidden=True)
    @commands.check(check_owner)
    async def _reload(self, *, module : str):
        """Reloads an addon."""
        try:
            if module[0:7] != "modules.":
                module = "modules." + module
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
            embed = discord.Embed(title='Extension reloaded!', description='Extension "{}" has been reloaded successfully.'.format(module), color=0x00ff99)
            embed.set_thumbnail(url='https://i.imgur.com/TVtrqXR.png')
            await self.bot.say(embed=embed)
        except Exception as e:
            embed = discord.Embed(title='Extension reload failed!', description='Extension "{}" has failed to reload.'.format(module), color=0xFF0000)
            embed.add_field(name='Error', value='\n{}: {}\n'.format(type(e).__name__, e), inline=True)
            embed.set_thumbnail(url='https://i.imgur.com/z2xfrsH.png')
            await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Load(bot))
