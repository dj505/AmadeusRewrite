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
    '''
    Moderation commands.
    '''
    def __init__(self, bot):
        self.bot = bot
        print('Module "{}" loaded'.format(self.__class__.__name__))

    @commands.has_permissions(kick_members=True)
    @commands.command
    async def kick(self, ctx, member, *, reason="No reason given."):
        """Kicks a member."""
        if admin_role in member.roles or mod_role in user.roles:
            await self.bot.say(':x: This user is an admin or admin, and cannot be kicked!')
        elif user == ctx.message.author:
            await self.bot.say(':x: You can\'t kick yourself!')
        else:
            kickmessage = await self.bot.say(':white_check_mark: Goodbye, {0.mention}!'.format(user))
            embed = discord.Embed(title="Member kicked by {0.name}#{0.discriminator}".format(ctx.message.author), description="{0.mention}\nName: {0.name}#{0.discriminator}\nID:{0.id}".format(member), color=0xFF9710)
            embed.set_thumbnail(url=member.avatar_url)
            await bot.send_message(discord.Object(id=log_channel), embed=embed)
            await self.bot.edit_message(kickmessage, "\nAdmin note: Successfully logged this action!")

def setup(bot):
    bot.add_cog(Mod(bot))
