import discord
from discord.ext import commands
import json

class Fun:
    """
    Fun stuff
    """
    def __init__(self, bot):
        self.bot = bot
        print('Module "{}" loaded'.format(self.__class__.__name__))

    @commands.command(pass_context=True, brief="Gain daily 150 credits")
    @commands.cooldown(1, 86400.0, commands.BucketType.user)
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
            json.dump(wallets, f)
        await self.bot.say(':moneybag: Wallet updated successfully! Your balance is now {}'.format(balance))


def setup(bot):
    bot.add_cog(Fun(bot))
