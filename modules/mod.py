import discord
from discord.ext import commands
import json
import time

with open('channels.json') as f:
    settings = json.load(f)
log_channel = settings['log_channel_id']

with open('roles.json') as f:
    roles = json.load(f)
admin_role = roles['admin']
mod_role = roles['mod']

class Mod:
    """
    Moderation commands.
    """
    def __init__(self, bot):
        self.bot = bot
        print('Module "{}" loaded'.format(self.__class__.__name__))

    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context="True",brief="Kicks a member.")
    async def kick(self, ctx, member : discord.Member):
        """
        Kicks a specified member.
        """
        if ctx.message.author == member:
            await self.bot.say(':x: You can\'t kick yourself!')
        elif admin_role in member.roles or mod_role in member.roles:
            await self.bot.say(':x: You can\'t kick a mod/admin!')
        else:
            await self.bot.kick(member)
            embed = discord.Embed(title="Member kicked by {}".format(ctx.message.author.name), description="Name: {0.name}\nID: {0.id}".format(member), color=0xFFF110)
            await self.bot.send_message(discord.Object(id=log_channel), embed=embed)
            await self.bot.say(':white_check_mark: Kicked user successfully! This action has been logged.')

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True,brief="Bans a member.")
    async def ban(self, ctx, member : discord.Member):
        """
        Bans a specified member.
        """
        if ctx.message.author == member:
            await self.bot.say(':x: You can\'t ban yourself!')
        elif admin_role in member.roles or mod_role in member.roles:
            await self.bot.say(':x: You can\'t ban a mod/admin!')
        else:
            await self.bot.ban(member)
            embed = discord.Embed(title="Member banned by {}".format(ctx.message.author.name), description="Name: {0.name}\nID: {0.id}".format(member), color=0xFF9710)
            await self.bot.send_message(discord.Object(id=log_channel), embed=embed)
            await self.bot.say(':hammer: Banned user successfully! This action has been logged.')

    @commands.has_permissions(manage_messages=True)
    @commands.command(pass_context=True, brief="Clean specified number of messages")
    async def purge(self, ctx, amount=0):
        await self.bot.delete_message(ctx.message)
        channel = ctx.message.channel
        messages = []
        if int(amount) > 1:
            async for message in self.bot.logs_from(ctx.message.channel, limit=int(amount)):
                messages.append(message)
            await self.bot.delete_messages(messages)
            message = await self.bot.say(':white_check_mark: Complete! Deleted {} messages.'.format(amount))
            time.sleep(5)
            await self.bot.delete_message(message)
        else:
            await self.bot.say('Please provide a number between 2 and 100!')

def setup(bot):
    bot.add_cog(Mod(bot))
