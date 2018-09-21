# A simple logging module
import discord
from discord.ext import commands
import json
import asyncio

with open('channels.json') as f:
    settings = json.load(f)
log_channel = settings['log_channel_id']

class Logging:
    '''
    Some simple logging stuff.
    '''
    def __init__(self, bot):
        self.bot = bot
        print('Module "{}" loaded'.format(self.__class__.__name__))

    async def on_message_delete(self, message):
        if message.author != self.bot.user:
            embed = discord.Embed(title="Message deleted in {}".format(message.channel.name), description="Author: {}\n".format(message.author.name) + "Content: `{}`".format(str(message.content)), color=0xFF0000)
            embed.set_thumbnail(url=message.author.avatar_url)
            await self.bot.send_message(discord.Object(id=log_channel), embed=embed)

    async def on_message_edit(self, message, edited):
        if message.author == self.bot.user:
            return
        if message.author.bot:
            return
        if message.content == edited.content:
            return
        embed = discord.Embed(title="Message edited in {}".format(message.channel.name), description="Author: {}\n".format(message.author.name) + "Before: `{}`\n".format(str(message.content)) + "After: `{}`".format(str(edited.content)), color=0xFFF110)
        embed.set_thumbnail(url=message.author.avatar_url)
        await self.bot.send_message(discord.Object(id=log_channel), embed=embed)

    async def on_member_join(self, member):
        embed = discord.Embed(title="Member joined!", description="{0.mention}\nName: {0.name}#{0.discriminator}\nID: {0.id}".format(member), color=0x59F442)
        embed.set_thumbnail(url=member.avatar_url)
        await self.bot.send_message(discord.Object(id=log_channel), embed=embed)

    async def on_member_leave(self, member):
        embed = discord.Embed(title="Member left or was kicked", description="{0.mention}\nName: {0.name}#{0.discriminator}\nID: {0.id}".format(member), color=0xFF9710)
        embed.set_thumbnail(url=member.avatar_url)
        await self.bot.send_message(discord.Object(id=log_channel), embed=embed)

def setup(bot):
    bot.add_cog(Logging(bot))
