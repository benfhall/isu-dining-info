# bot.py
import os, discord, logging, sys
from discord.ext import commands
from dotenv import load_dotenv

from constants import *
from food import *


dining_halls = []

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

load_dotenv()
logger = logging.getLogger('discord')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

def match_args(arg, args):
    """returns if arg is in args"""
    if arg is None:
        return False
    elif arg.lower() in args:
        return True
    else:
        return False
    
async def menu_pagination(ctx, embeds, d: DiningHall, sec:int):
    """function to print pagination embeds"""
    total_pages = len(d.sections[sec].menus)
    def check(reaction, user):
        """check for reaction"""
        return reaction.message.id == msg.id and user == ctx.author
    async def add_reactions():
        for x in range(total_pages):
            if index != x:
                await msg.add_reaction(EMOJIS[x])
    index = 0
    msg = await ctx.channel.send(embed=embeds[index])
    await add_reactions()
    while True:
        try:
            reaction, _ = await bot.wait_for('reaction_add', timeout=20.0, check=check)
            for x in range(total_pages):
                if reaction.emoji == EMOJIS[x]:
                    index = x
                    await msg.edit(embed=embeds[index]) # do asap for faster reaction speed...
                await msg.remove_reaction(EMOJIS[x], bot.user) #remove bot reaction
            await add_reactions()
            try:
                await msg.remove_reaction(EMOJIS[index],ctx.author)
            except discord.errors.Forbidden:
                perms = await ctx.channel.send("```Please give me \"Manage Messages\" permissions in roles so I can remove your reaction's for you!```")
                await asyncio.sleep(5)
                await perms.delete()
        except asyncio.TimeoutError:
            break

def give_menu(d: DiningHall, section: int, mSelect: int):
    """returns the menu in a formatted way, at time ,[arg], and at place,[center]"""
    menu = d.sections[section]
    embed = discord.Embed(
        title=d.name + " @ " + menu.name,
        color=0xE51837,
        description=menu.menus[mSelect].name
    )
    embed.set_thumbnail(url=d.thumbnail_uri)
    for foodlist in menu.menus[0].foods:
        embed.add_field(name=foodlist[mSelect],value=foodlist[mSelect])
    return embed

# DISCORD COMMANDS

@bot.event
async def on_ready():
    """load data when connected to discord."""
    logger.info(f'{bot.user} has connected to Discord!')
    for URL in URLS:
        globals()['dining_halls'].append(DiningHall(URL))
    for d in dining_halls:
        await d.fetch_data()
        await d.populate()

@bot.command(pass_context=True)
async def udcc(ctx, section):
    """command for giving udcc menu, given time, [arg]."""
    # check if section exists
    dining_hall = globals()['dining_halls'][0]
    FOUND_SECTION = False
    for s in dining_hall:
        if s.name == section:
            FOUND_SECTION=True
            break

    embeds = []
    for x in range(len(dining_hall.sections[section].menus)):
        embeds.append(give_menu(dining_hall,section,x-1))

    await menu_pagination(ctx, embeds, dining_hall, section)
    

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