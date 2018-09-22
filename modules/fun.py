import discord
from discord.ext import commands
import json
from datetime import datetime

class Fun:
    """
    Fun stuff
    """
    def __init__(self, bot):
        self.bot = bot
        print('Module "{}" loaded'.format(self.__class__.__name__))

    @commands.command(pass_context=True, brief="Gain daily 150 credits")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        """
        This command adds 150 credits to your wallet. Can only be used once per day.
        """
        user = ctx.message.author.id
        with open('wallets.json') as f:
            wallets = json.load(f)
        if user not in wallets:
            wallets[user] = 0
        balance = int(wallets[user]) + 150
        wallets[user] = balance
        with open('wallets.json', 'w') as f:
            json.dump(wallets, f, indent=2, sort_keys=True)
        await self.bot.say(':moneybag: Wallet updated successfully! Your balance is now {}'.format(balance))

    @commands.command(pass_context=True, brief="Get user information")
    async def userinfo(self, ctx, member=None):
        """
        Get information about a certain user, or yourself, if no user is specified
        """
        with open('wallets.json') as f:
            wallets = json.load(f)
        if member == None:
            member = ctx.message.author
        balance = wallets[member.id]
        embed = discord.Embed(title="User information: {}".format(member.name), description=None, color=0x42F448)
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.add_field(name="ID", value=str(ctx.message.author.id))
        embed.add_field(name="Joined Server", value=str(ctx.message.author.joined_at))
        embed.add_field(name="Joined Discord", value=str(ctx.message.author.created_at))
        embed.add_field(name="Status", value=str(ctx.message.author.status).capitalize())
        embed.add_field(name="Highest Role", value=ctx.message.author.top_role)
        embed.add_field(name="Wallet Balance", value=balance)
        await self.bot.say(embed=embed)

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True, hidden=True, aliases=['givecredit','gc'])
    async def givecredits(self, ctx, member: discord.Member, amount=0):
        member = member.id
        with open('wallets.json') as f:
            wallets = json.load(f)
        if member not in wallets:
            wallets[member] = 0
        balance = int(wallets[member]) + amount
        wallets[member] = balance
        with open('wallets.json', 'w') as f:
            json.dump(wallets, f, indent=2, sort_keys=True)
        await self.bot.say(':moneybag: Wallet updated successfully! Your balance is now {} after being given {} credits.'.format(balance, amount))

def setup(bot):
    bot.add_cog(Fun(bot))
