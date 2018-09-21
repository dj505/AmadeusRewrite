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

@bot.event
async def on_ready():
    print('{0.user} is up and running!'.format(bot))

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.errors.CommandNotFound):
        embed = discord.Embed(title='Error!', description='I cannot find that command!', color=0xFF0000)
        embed.set_thumbnail(url='https://i.imgur.com/z2xfrsH.png')
        await bot.send_message(ctx.message.channel, embed=embed)
    elif isinstance(error, commands.errors.CheckFailure):
        embed = discord.Embed(title='Permissions error!', description='You do not have permission to use this command.', color=0xFF0000)
        embed.set_thumbnail(url='https://i.imgur.com/z2xfrsH.png')
        await bot.send_message(ctx.message.channel, embed=embed)
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        formatter = commands.formatter.HelpFormatter()
        # await bot.send_message(ctx.message.channel, "{} You are missing required arguments.\n{}".format(ctx.message.author.mention, formatter.format_help_for(ctx, ctx.command)[0]))
        embed = discord.Embed(title='Error!', description='You are missing required arguments.', color=0xFF0000)
        embed.add_field(name='Usage', value='{}'.format(ctx.message.author.mention, formatter.format_help_for(ctx, ctx.command)[0]))
        embed.set_thumbnail(url='https://i.imgur.com/z2xfrsH.png')
        await bot.send_message(ctx.message.channel, embed=embed)
    elif isinstance(error, commands.errors.CommandOnCooldown):
        try:
            await bot.delete_message(ctx.message)
        except discord.errors.NotFound:
            pass
        message = await bot.send_message(ctx.message.channel, "{} This command was used {:.2f}s ago! Please ry again in {:.2f}s.".format(ctx.message.author.mention, error.cooldown.per - error.retry_after, error.retry_after))
        await asyncio.sleep(10)
        await bot.delete_message(message)
    else:
        embed = discord.Embed(title='Error!', description='An error occured processing that command.', color=0xFF0000)
        embed.set_thumbnail(url='https://i.imgur.com/z2xfrsH.png')
        print('Ignoring exception in command {0.command} in {0.message.channel}'.format(ctx))
        tb = traceback.format_exception(type(error), error, error.__traceback__)
        print(''.join(tb))
        await bot.send_message(ctx.message.channel, embed=embed)

#@bot.event
#async def on_error(event_method, *args, **kwargs):
#    if isinstance(args[0], commands.errors.CommandNotFound):
#        return
#    print("Ignoring exception in {}".format(event_method))
#    tb = traceback.format_exc()
#    error_trace = "".join(tb)
#    print(error_trace)
#    if bot.log_channel:
#        embed = discord.Embed(description=error_trace)
#        await bot.log_channel.send("An error occurred while processing `{}`.".format(event_method), embed=embed)

modules = [
    'modules.load',
    'modules.logging',
    'modules.testing',
    'modules.xkcd',
    'modules.mod'
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
