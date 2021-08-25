# bot.py
import os, discord, urllib.request, urllib.error, urllib.parse, json, ssl, asyncio
from dotenv import load_dotenv
from discord.ext import tasks, commands
from discord import utils
from constants import *

udcc = [[[]for _ in range(3)] for _ in range(8)]
windows = [[[]for _ in range(2)] for _ in range(7)]
seasons = [[[]for _ in range(4)] for _ in range(7)]
mu = [[[]for _ in range(3)] for _ in range(7)]

CENTERS = {0:udcc,1:windows,2:seasons}
gcontext = ssl.SSLContext()
load_dotenv()
ssl._create_default_https_context = ssl._create_unverified_context
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix="!", help_command=None)

# INTERNAL FUNCTIONS

def match_args(arg, args):
    """returns if arg is in args"""
    if arg is None:
        return False
    elif arg.lower() in args:
        return True
    else:
        return False

def give_menu(arg, center):
    """returns the menu in a formatted way, at time ,[arg], and at place,[center]"""
    sorted_foods = []
    embed = discord.Embed(
        title=TITLES[center],
        color=0xE51837
    )
    embed.set_thumbnail(url=THUMBNAIL[center])
    if is_closed(center, arg):
        embed.description = "Closed for " +  TIME_NAMES[center][TIMES[center].get(arg)]
    else:
        embed.description = TIME_NAMES[center][TIMES[center].get(arg)]
        counter = 0
        for station in CENTERS.get(center):
            if station[TIMES[center].get(arg)]:
                sorted_foods.append([STATIONS[center][counter],""])
                for food in station[TIMES[center].get(arg)]:
                    sorted_foods[counter][1] += food + "\n"
                counter += 1
        sorted_foods.sort(key=lambda x:len(x[1]), reverse=True)
        for foods in sorted_foods:
            embed.add_field(name=foods[0], value=foods[1])
    return embed

def is_closed(center,time):
    """returns whether [center] is closed during [time]"""
    for station in CENTERS.get(center):
        try:
            if any(station[TIMES[center].get(time.title())]):
                return False
        except TypeError:
            return True
    return True

def search_for(ctx, substring, time):
    """returns the formatted response when searching for [substring] at [time]."""
    open_centers = (center for center in range(3) if not is_closed(center,time))
    index = 0
    embed = discord.Embed(
        title="Search Results",
        description=substring + " @ " + time.title(),
        color=0xE51837
    )
    sorted_foods = []
    for center in open_centers:
        sorted_foods.append([TITLES[index],""])
        for station in CENTERS.get(center):
            matched_foods = (food for food in station[TIMES[center].get(time.title())] if substring.lower() in food.lower())
            for food in matched_foods:
                sorted_foods[index][1] += food + "\n"
        index += 1
    sorted_foods.sort(key=lambda x:len(x[1]), reverse=True)
    for foods in sorted_foods:
        if foods[1] == "":
            sorted_foods.remove(foods)
            continue
        embed.add_field(name=foods[0], value=foods[1])
    if len(sorted_foods) <= 1:
        embed.add_field(name="Error", value="Not Found")
    return embed

@tasks.loop(hours=2)
async def load_menus():
    """Pulls JSON data from website and pushes them to arrays"""
    global udcc
    global windows
    global seasons
    global mu
    global CENTERS

    udcc = [[[]for _ in range(3)] for _ in range(8)]
    windows = [[[]for _ in range(2)] for _ in range(7)]
    seasons = [[[]for _ in range(4)] for _ in range(7)]
    mu = [[[]for _ in range(3)] for _ in range(7)]
    CENTERS = {0:udcc,1:windows,2:seasons,3:mu}
    building_index = 0

    print('Reloading Menus...')
    for url in URLS:
        request=urllib.request.Request(url,None,HEADERS)
        with urllib.request.urlopen(request, context=gcontext) as url:
            data = json.loads(url.read().decode())
        for time in data[0]["menus"]:
            if time['section'] not in TIMES[building_index]:
                continue
            for station in time["menuDisplays"]:
                found_foods = [foods for subfood in station['categories'] for foods in subfood['menuItems']]
                for food in found_foods:
                    await add_food(building_index,station['name'],time,food['name'])
        building_index += 1
    print(CMP)

async def add_station(building_index, station_name):
    """checks to see if station exists, if not add it."""
    if station_name in STATIONS[building_index]:
        return True
    else:
        STATIONS[building_index].append(station_name)
        return False

async def add_food(building_index,station_name,time,food_name):
    """adds food to arrays"""
    await add_station(building_index,station_name)
    CENTERS.get(building_index)[STATIONS[building_index].index(station_name)][TIMES[building_index].get(time['section'])].append(food_name)

async def menu_pagination(ctx, embeds, reactions, starting):
    """function to print pagination embeds"""
    def check(reaction, user):
        """check for reaction"""
        return reaction.message.id == msg.id and user == ctx.author
    index = starting
    msg = await ctx.channel.send(embed=embeds[index])
    for x in range(len(reactions)):
        if index != x:
            await msg.add_reaction(reactions[x])
    while True:
        try:
            reaction, _ = await bot.wait_for('reaction_add', timeout=20.0, check=check)
            for x in range(len(reactions)):
                if reaction.emoji == reactions[x]:
                    await msg.add_reaction(reactions[index])
                    index = x
            await msg.remove_reaction(reactions[index],bot.user)
            try:
                await msg.remove_reaction(reactions[index],ctx.author)
            except discord.errors.Forbidden:
                perms = await ctx.channel.send("```Please give me \"Manage Messages\" permissions in roles so I can remove your reaction's for you!```")
                await asyncio.sleep(5)
                await perms.delete()
            await msg.edit(embed=embeds[index])
        except asyncio.TimeoutError:
            break

# DISCORD COMMANDS

@bot.event
async def on_ready():
    """load data when connected to discord."""
    print(f'{bot.user} has connected to Discord!')
    await load_menus.start()

@bot.command(pass_context=True)
async def help(ctx, time=None):
    """prints user help info"""
    embed = discord.Embed(
        title="ISU Dining Help",
        color=0xE51837
    )
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.add_field(name="Commands", value="Find the commands [here](https://github.com/Swidex/isu-dining-info)")
    embed.add_field(name="Invite", value="Invite this bot [here](https://discord.com/api/oauth2/authorize?client_id=810022244071374890&permissions=3221612608&scope=bot)")
    await ctx.channel.send(embed=embed)

@bot.command(pass_context=True)
async def udcc(ctx, arg="dinner"):
    """command for giving udcc menu, given time, [arg]."""
    args = ["breakfast","lunch","dinner"]
    if not match_args(arg, args):
        arg = "dinner"
    embeds = [give_menu(args[0].title(),0),give_menu(args[1].title(),0),give_menu(args[2].title(),0)]
    for embed in embeds:
        embed.set_footer(text="🥞 for breakfast\n🥪 for lunch\n🍖 for dinner")
    await menu_pagination(ctx, embeds, ['🥞','🥪','🍖'], TIMES[0].get(arg.title()))

@bot.command(pass_context=True)
async def windows(ctx, arg="dinner"):
    """command for giving windows menu, given time,[arg]."""
    args = ["lunch","dinner"]
    if not match_args(arg, args):
        arg = "dinner"
    embeds = [give_menu(args[0].title(),1),give_menu(args[1].title(),1)]
    for embed in embeds:
        embed.set_footer(text="🥪 for lunch\n🍖 for dinner")
    await menu_pagination(ctx, embeds, ['🥪','🍖'], TIMES[1].get(arg.title()))

@bot.command(pass_context=True)
async def seasons(ctx, arg="dinner"):
    """command for giving seasons menu, given time,[arg]."""
    args = ["breakfast","lunch","dinner"]
    if not match_args(arg, args):
        arg = "dinner"
    embeds = [
        give_menu(args[0].title(),2),
        give_menu(args[1].title(),2),
        give_menu(args[2].title(),2)
        ]
    for embed in embeds:
        embed.set_footer(text="🥞 for breakfast\n🥪 for lunch\n🍖 for dinner")
    await menu_pagination(ctx, embeds, ['🥞','🥪','🍖'], TIMES[2].get(arg.title()))

@bot.command(pass_context=True)
async def mu(ctx):
    """command for giving mu menu."""
    embed = give_menu("Lunch",3)
    await ctx.channel.send(embed=embed)

@bot.command(pass_context=True)
async def search(ctx, substring=None, time="dinner"):
    """discord command for searching for [substring] at [time]."""
    args = ["breakfast","lunch","dinner"]
    if not match_args(time, args):
        time = "dinner"
    embeds = [search_for(ctx, substring, "breakfast"),search_for(ctx, substring, "lunch"),search_for(ctx, substring, "dinner")]
    for embed in embeds:
        embed.set_footer(text="🥞 for breakfast\n🥪 for lunch\n🍖 for dinner")
    await menu_pagination(ctx, embeds, ['🥪','🕓','🍞'], TIMES[0].get(time.title()))

@bot.command(pass_context=True)
async def tendies(ctx, time="dinner"):
    """discord command for searching for tenders at [time]."""
    await search(ctx, "tender", time)

@bot.command(pass_context=True)
async def nuggies(ctx, time="dinner"):
    """discord command for searching for nuggets at [time]."""
    await search(ctx, "nugget", time)

@bot.command(pass_context=True)
async def wingies(ctx, time="dinner"):
    """discord command for searching for wings at [time]."""
    await search(ctx, "wing", time)

@bot.command(pass_context=True)
async def reload(ctx):
    """discord command for reloading menus."""
    embed = discord.Embed(
        title="Reloading Menus...",
        color=0xE51837
    )
    msg = await ctx.channel.send(embed=embed)
    await load_menus()
    embed.title="Successfully Reloaded Menus!"
    await msg.edit(embed=embed)

bot.run(DISCORD_TOKEN)