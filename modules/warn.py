import discord
from discord.ext import commands
import os
import sys
import json
import asyncio

# Borrowed from GriffinG1/Midnight
# I'll learn one day ;)
# For now, I need something functional.

with open('roles.json','r') as f:
    roles = json.load(f)
admin_role = roles['admin']
mod_role = roles['mod']

with open('channels.json','r') as f:
    channels = json.load(f)
log_channel = channels['log_channel_id']

class Warns:
    """
    Warning commands
    """
    def __init__(self, bot):
        self.bot = bot
        with open('warns.json', 'r+') as f:
            self.warns = json.load(f)
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    def find_user(self, user, ctx):
        found_member = self.bot.guild.get_member(user)
        if not found_member:
            found_member = self.bot.guild.get_member_named(user)
        if not found_member:
            try:
                found_member = ctx.message.mentions[0]
            except IndexError:
                pass
        if not found_member:
            return None
        else:
            return found_member

    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True)
    async def warn(self, ctx, member, *, reason="No reason given."):
        """
        Warn a member.
        """
        found_member = self.find_user(member, ctx)
        if not found_member:
            await ctx.send(":x: I couldn't find that user!")
        else:
            owner = ctx.guild.owner
            if admin_role in found_member.roles or mod_role in found_member.roles and not ctx.author == owner:
                return await ctx.send(":x: You cannot warn a staff member!")
            try:
                self.warns[str(found_member.id)]
            except KeyError:
                self.warns[str(found_member.id)] = []
            self.warns[str(found_member.id)].append(reason)
            reply_msg = "Warned user {}#{}. This is warn {}.".format(found_member.name, found_member.discriminator, len(self.warns[str(found_member.id)]))
            private_message = "You have been warned by user {}#{}. The given reason was: `{}`\nThis is warn {}.".format(ctx.author.name, ctx.author.discriminator, reason, len(self.warns[str(found_member.id)]))
            if len(self.warns[str(found_member.id)]) >= 5:
                private_message += "\nYou were banned due to this warn.\nIf you feel that you did not deserve this ban, send a direct message to a staff member."
                try:
                    await found_member.send(private_message)
                except discord.Forbidden:
                    pass
                await self.bot.guild.ban(found_member, delete_message_days=0, reason="5+ warns, see logs for details.")
                reply_msg += " As a result of this warn, the user was banned."

            elif len(self.warns[str(found_member.id)]) == 4:
                private_message += "\nYou were kicked due to this warn."
                try:
                    await found_member.send(private_message)
                except discord.Forbidden:
                    pass
                await found_member.kick(reason="4 warns, see logs for details.")
                reply_msg += " As a result of this warn, the user was kicked. The next warn will automatically ban the user."

            elif len(self.warns[str(found_member.id)]) == 3:
                private_message += "\nYou were kicked due to this warn."
                try:
                    await found_member.send(private_message)
                except discord.Forbidden:
                    pass
                await found_member.kick(reason="3 warns, see logs for details.")
                reply_msg += " As a result of this warn, the user was kicked. The next warn will automatically kick the user."

            elif len(self.warns[str(found_member.id)]) == 2:
                private_message += "\nYour next warn will automatically kick you."
                try:
                    await found_member.send(private_message)
                except discord.Forbidden:
                    pass
                reply_msg += " The next warn will automatically kick the user."

            else:
                try:
                    await found_member.send(private_message)
                except:
                    pass
            await ctx.send(reply_msg)
            embed = discord.Embed(description="{0.name}#{0.discriminator} warned user <@{1.id}> | {1.name}#{1.discriminator}".format(ctx.author, found_member))
            embed.add_field(name="Reason given", value="• " + reason)
            await self.bot.send_message(discord.Object(id=log_channel), embed=embed)
            with open("warns.json", "w+") as f:
                json.dump(self.warns, f, indent=2)

    @commands.command(pass_context=True)
    async def listwarns(self, ctx, *, member=None):
        """List a member's warns."""
        if member is None:
            found_member = ctx.author
        else:
            found_member = self.find_user(member, ctx)
        if not found_member:
            await ctx.send(":x: I couldn't find that member!")
        else:
            if not admin_role in found_member.roles or mod_role in found_member.roles and not ctx.author == ctx.guild.owner and not ctx.message.author == found_member:
                await ctx.send(":x: I'm sorry {}, I can't let you do that.".format(ctx.message.author.name))
            else:
                try:
                    user_warns = self.warns[str(found_member.id)]
                    if user_warns:
                        embed = discord.Embed(title="Warns for user {}#{}".format(found_member.name, found_member.discriminator), description="")
                        for warn in user_warns:
                            embed.description += "• {}\n".format(warn)
                        embed.set_footer(text="There are {} warns in total.".format(len(user_warns)))
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(":x: That user has no warns!")
                except KeyError:
                    await ctx.send(":x: That user has no warns!")

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True)
    async def clearwarns(self, ctx, *, member):
        """Clear a member's warns."""
        found_member = self.find_user(member, ctx)
        if not found_member:
            await ctx.send(":x: I couldn't find that user!")
        else:
            try:
                if self.warns[str(found_member.id)]:
                    self.warns[str(found_member.id)] = []
                    with open("warns.json", "w+") as f:
                        json.dump(self.warns, f)
                    await ctx.send("Cleared the warns of user {}#{}.".format(found_member.name, found_member.discriminator))
                    embed = discord.Embed(description="{0.name}#{0.discriminator} cleared warns of user <@{1.id}> | {1.name}#{1.discriminator}".format(ctx.author, found_member))
                    await self.bot.send_message(discord.Object(id=log_channel), embed=embed)
                    try:
                        await found_member.send("All your warns have been cleared.")
                    except discord.errors.Forbidden:
                        pass
                else:
                    await ctx.send(":x: That user has no warns!")
            except KeyError:
                await ctx.send(":x: That user has no warns!")

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True)
    async def unwarn(self, ctx, member, *, index=-1):
        """Take a specific warn off a user."""
        found_member = self.find_user(member, ctx)
        if not found_member:
            await ctx.send(":x: I couldn't find that user!")
        else:
            try:
                if self.warns[str(found_member.id)]:
                    if index > len(self.warns[str(found_member.id)]) or index == -1:
                        return await ctx.send("{} doesn't have a warn numbered `{}`!".format(found_member, index))
                    reason = self.warns[str(found_member.id)][index-1]
                    self.warns[str(found_member.id)].pop(index-1)
                    with open("warns.json", "w+") as f:
                        json.dump(self.warns, f)
                    await ctx.send("Removed `{}` warn of user {}#{}.".format(reason, found_member.name, found_member.discriminator))
                    embed = discord.Embed(description="{} took a warn off of user <@{}> | {}\n{}".format(ctx.author, found_member.id, found_member, reason))
                    embed.add_field(name="Removed Warn", value="• " + reason)
                    await self.bot.send_message(discord.Object(id=log_channel), embed=embed)
                else:
                    await ctx.send(":x: That user has no warns!")
            except KeyError:
                await ctx.send(":x: That user has no warns!")

def setup(bot):
    bot.add_cog(Warns(bot))
