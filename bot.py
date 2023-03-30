# bot.py
import os, discord
from discord.ext import commands
from dotenv import load_dotenv

from constants import *
from food import *

dining_halls = []

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

def match_args(arg, args):
    """returns if arg is in args"""
    if arg is None:
        return False
    elif arg.lower() in args:
        return True
    else:
        return False

def give_menu(d: DiningHall):
    """returns the menu in a formatted way, at time ,[arg], and at place,[center]"""
    menu = d.sections[0]
    embed = discord.Embed(
        title=d.name + " @ " + menu.name,
        color=0xE51837,
        description=menu.menus[0].name
    )
    embed.set_thumbnail(url=d.thumbnail_uri)
    for foodlist in menu.menus[0].foods:
        embed.add_field(name=foodlist[0],value=foodlist[1])
    return embed

# DISCORD COMMANDS

@bot.event
async def on_ready():
    """load data when connected to discord."""
    print(f'{bot.user} has connected to Discord!')
    for URL in URLS:
        globals()['dining_halls'].append(DiningHall(URL))
    for d in dining_halls:
        await d.fetch_data()
        await d.populate()

@bot.command(pass_context=True)
async def udcc(ctx, arg="dinner"):
    """command for giving udcc menu, given time, [arg]."""
    args = ["breakfast","lunch","dinner"]
    embed = give_menu(globals()['dining_halls'][0])
    await ctx.channel.send(embed=embed)
    globals()['dining_halls'][0].dump_data()
    

@bot.command(pass_context=True)
async def reload(ctx):
    """discord command for reloading menus."""
    embed = discord.Embed(
        title="Reloading Menus...",
        color=0xE51837
    )
    msg = await ctx.channel.send(embed=embed)
    for d in dining_halls:
        await d.fetch_data()
        await d.populate()
    embed.title="Successfully Reloaded Menus!"
    await msg.edit(embed=embed)

bot.run(DISCORD_TOKEN)