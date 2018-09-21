import discord
from discord.ext import commands
import json

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

    @commands.has_permissions(ban_members=True)
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
            await self.bot.say(':white_check_mark: Kicked user successfully!')

def setup(bot):
    bot.add_cog(Mod(bot))
