import discord
from discord.ext import commands
import json
import sys, traceback
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

with open('settings.json') as f:
    settings = json.load(f)
token = settings['token']
prefix = settings['prefix']
description = settings['description']

client = discord.Client()
bot = commands.Bot(pm_help=True, command_prefix=prefix, description=description)

@client.event
async def on_ready():
    print('{0.user} is up and running!'.format(client))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        pass  # ...don't need to know if commands don't exist
    elif isinstance(error, discord.ext.commands.NoPrivateMessage):
        await ctx.send("You cannot use this command in DMs!")
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        formatter = commands.formatter.HelpFormatter()
        await ctx.send("You are missing required arguments.\n{}".format(formatter.format_help_for(ctx, ctx.command)[0]))
    elif isinstance(error, discord.ext.commands.errors.CheckFailure):
        await ctx.send("You don't have permission to use this command.")
    else:
        if ctx.command:
            await ctx.send("An error occurred while processing the `{}` command.".format(ctx.command.name))
        print('Ignoring exception in command {0.command} in {0.message.channel}'.format(ctx))
        tb = traceback.format_exception(type(error), error, error.__traceback__)
        error_trace = "".join(tb)
        print(error_trace)
        if bot.log_channel:
            embed = discord.Embed(description=error_trace)
            await bot.log_channel.send("An error occurred while processing the `{}` command in channel `{}`.".format(ctx.command.name, ctx.message.channel), embed=embed)

@bot.event
async def on_error(event_method, *args, **kwargs):
    if isinstance(args[0], commands.errors.CommandNotFound):
        return
    print("Ignoring exception in {}".format(event_method))
    tb = traceback.format_exc()
    error_trace = "".join(tb)
    print(error_trace)
    if bot.log_channel:
        embed = discord.Embed(description=error_trace)
        await bot.log_channel.send("An error occurred while processing `{}`.".format(event_method), embed=embed)

modules = [
    'modules.load',
    'modules.logging',
    'modules.testing',
    'modules.xkcd'
]

failed_modules = []

for extension in modules:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print('{} failed to load.\n{}: {}'.format(extension, type(e).__name__, e))
        failed_addons.append([extension, type(e).__name__, e])
if not failed_modules:
    print('All modules loaded!')

bot.run(token)
