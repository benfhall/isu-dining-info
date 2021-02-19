# bot.py
import os, discord, urllib.request, urllib.error, urllib.parse, json, ssl
from dotenv import load_dotenv
from discord.ext import tasks, commands
import numpy as np
from file_mgr import *
from constants import *

udcc = [[[]for _ in range(3)] for _ in range(8)]
windows = [[[]for _ in range(2)] for _ in range(7)]
seasons = [[[]for _ in range(4)] for _ in range(7)]
food_list = np.array([[]for _ in range(3)])
food_likes = np.array([[[]]for _ in range(3)])
food_dislikes = np.array([[[]]for _ in range(3)])
CENTERS = {0:udcc,1:windows,2:seasons}

gcontext = ssl.SSLContext()
load_dotenv()
ssl._create_default_https_context = ssl._create_unverified_context
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix="!", help_command=None)

@tasks.loop(seconds=10800)
async def load_menus():
    """Pulls JSON data from website and pushes them to arrays"""
    global udcc
    global windows
    global seasons
    global food_likes
    global food_dislikes
    global food_list
    global CENTERS

    food_list = [[]for _ in range(3)]
    food_likes = ([[[]]for _ in range(3)])
    food_dislikes = ([[[]]for _ in range(3)])
    udcc = [[[]for _ in range(3)] for _ in range(8)]
    windows = [[[]for _ in range(2)] for _ in range(7)]
    seasons = [[[]for _ in range(4)] for _ in range(7)]
    CENTERS = {0:udcc,1:windows,2:seasons}
    building_index = 0

    print('Reloading Menus...')
    for url in URLS:
        request=urllib.request.Request(url,None,HEADERS)
        with urllib.request.urlopen(request, context=gcontext) as url:
            data = json.loads(url.read().decode())
        for time in data[0]["menus"]:
            for station in time["menuDisplays"]:
                found_foods = [foods for subfood in station['categories'] for foods in subfood['menuItems']]
                for food in found_foods:
                    await add_food(building_index,station,time,food)
        building_index += 1
    print(CMP)

async def add_food(building_index,station,time,food):
    """adds food to arrays"""
    try:
        CENTERS.get(building_index)[STATIONS[building_index].get(station['name'])][TIMES[building_index].get(time['section'])].append(food['name'])
    except TypeError:
        CENTERS.get(building_index)[len(STATIONS[building_index]-1)][TIMES[building_index].get(time['section'])].append(food['name'])
        print("err")
    if food['name'] not in food_list[building_index]:
            food_list[building_index].append(food['name'])
            food_likes[building_index].append([])
            food_dislikes[building_index].append([])

def match_args(arg, args):
    """returns if arg is in args"""
    if arg is None:
        return False
    elif arg.lower() in args:
        return True
    else:
        return False

def recommend_meals(center,rating_score,rated_food):
    """recommends meal, based on ranking at [center]"""
    response = "```"
    try:
        max_index = rating_score.index(max(rating_score))
        if rating_score[max_index] != 0:
            response += "Your peers recommend the following dishes: \n\n"
            for _ in range(3):
                max_index = rating_score.index(max(rating_score))
                if rating_score[max_index] == 0:
                    break
                response += rated_food[max_index] + " (+" + str(rating_score[max_index]) + ")\n"
                rated_food.pop(max_index)
                rating_score.pop(max_index)
            response += "\n"
    except ValueError:
        pass
    return response + "Recommend your favorite dishes with the command, !upvote [dish] and !downvote [dish]```"

def give_menu(arg, center):
    """returns the menu in a formatted way, at time ,[arg], and at place,[center]"""
    rating_score = []
    rated_food = []
    counter = 0
    response = ""
    if is_closed(center, arg):
        response += CLOSED[0] + TITLES[center] + CLOSED[1] + TIME_NAME[TIMES[center].get(arg)+OFFSET[center]] + CLOSED[2]
    else:
        response += TIME_NAME[TIMES[center].get(arg)+OFFSET[center]] + " at " + TITLES[center] + "\n"
        for station in CENTERS.get(center):
            if station[TIMES[center].get(arg)]:
                response += STATION_TITLES[center][counter]
                counter += 1
                for food in station[TIMES[center].get(arg)]:
                    rating_score.append(get_score(food,center))
                    rated_food.append(food)
                    response += food + "\n"
    return response + recommend_meals(center,rating_score,rated_food)

@bot.event
async def on_ready():
    """load data when connected to discord."""
    print(f'{bot.user} has connected to Discord!')
    await load()
    await load_menus()

@bot.command(pass_context=True)
async def help(ctx, time=None):
    """prints user help info"""
    await ctx.channel.send("""```
![center] [time]      :   find the menu for given [time] at given [center]
!search [term] [time]   :   searches for [term] at all dining centers, given [time].
!tendies [time] :   searches for tender, [time] is optional.
!nuggies [time] :   searches for nugget, [time] is optional.
!wingies [time]   :   searches for wing, [time] is optional.
!upvote [food]    :   upvotes [food].
!downvote [food]  :   downvotes [food].
!reload         :   reloads the menu.
!help           :   displays options and usage of commands.\n
    [center]  :   udcc/windows/seasons
    [time]      :   breakfast/lunch/dinner (breakfast not available for Windows)
```""")

@bot.command(pass_context=True)
async def udcc(ctx, arg=None):
    """command for giving udcc menu, given time,[arg]."""
    args = ["breakfast","lunch","dinner"]
    if match_args(arg, args):
        response = give_menu(arg.capitalize(), 0)
    else:
        response = INVALID_USAGE
    await ctx.channel.send(response)

@bot.command(pass_context=True)
async def windows(ctx, arg=None):
    """command for giving windows menu, given time,[arg]."""
    args = ["lunch","dinner"]
    if match_args(arg, args):
        response = give_menu(arg.capitalize(), 1)
    else:
        response = INVALID_USAGE
    await ctx.channel.send(response)

@bot.command(pass_context=True)
async def seasons(ctx, arg=None):
    """command for giving seasons menu, given time,[arg]."""
    args = ["breakfast","lunch","dinner","daily"]
    if match_args(arg, args):
        response = give_menu(arg.capitalize(), 2)
    else:
        response = INVALID_USAGE
    await ctx.channel.send(response)

def is_closed(center,time):
    """returns whether [center] is closed during [time]"""
    for station in CENTERS.get(center):
        if any(station[TIMES[center].get(time.capitalize())]):
            return False
    return True

def search_for(substring, time):
    """returns the formatted response when searching for [substring] at [time]."""
    response = ""
    if match_args(time,ALL_TIMES) and substring is not None:
        open_centers = (center for center in range(3) if not is_closed(center,time))
        for center in open_centers:
            for station in CENTERS.get(center):
                matched_foods = (food for food in station[TIMES[center].get(time.capitalize())] if substring.lower() in food.lower())
                for food in matched_foods:
                    response += TITLES[center] + " has: *" + food + "* for " + TIME_NAME[TIMES[center].get(time.capitalize())+OFFSET[center]] + ".\n"
        if response == "":
            response = "Search term: **" + substring + "** not found at **" + time + "**.\n"
    else:
        response = INVALID_USAGE
    return response

@bot.command(pass_context=True)
async def search(ctx, substring=None, time=None):
    """discord command for searching for [substring] at [time]."""
    await ctx.channel.send(search_for(substring,time))

@bot.command(pass_context=True)
async def tendies(ctx, time=None):
    """discord command for searching for tenders at [time]."""
    if time is None:
        response = search_for("tender", "lunch") + search_for("tender", "dinner")
    elif match_args(time,ALL_TIMES):
        response = search_for("tender",time)
    else:
        response = INVALID_USAGE
    await ctx.channel.send(response)

@bot.command(pass_context=True)
async def nuggies(ctx, time=None):
    """discord command for searching for nuggets at [time]."""
    if time is None:
        response = search_for("nugget", "lunch") + search_for("nugget", "dinner")
    elif match_args(time,ALL_TIMES):
        response = search_for("nugget",time)
    else:
        response = INVALID_USAGE
    await ctx.channel.send(response)

@bot.command(pass_context=True)
async def wingies(ctx, time=None):
    """discord command for searching for wings at [time]."""
    if time is None:
        response = search_for("wing", "lunch") + search_for("wing", "dinner")
    elif match_args(time,ALL_TIMES):
        response = search_for("wing",time)
    else:
        response = INVALID_USAGE
    await ctx.channel.send(response)

@bot.command(pass_context=True)
async def reload(ctx, time=None):
    """discord command for reloading menus."""
    await load_menus()
    await ctx.channel.send("Reloaded menus!")

async def append_vote(ctx, food, centers, meal, index, f_index, arg):
    """append given vote to arrays"""
    VOTE_ALIGN = {1:"upvote",-1:"downvote"}
    if food not in meal:
        return
    ARR = {1:food_likes,-1:food_dislikes}
    await ctx.channel.send("Did you mean: *" + meal + "* from *" + TITLES[index] + "*? (y/n)")
    msg = await bot.wait_for('message')
    if msg.content.lower() == 'y':
        if msg.author.id not in ARR.get(arg)[index][f_index]:
            ARR.get(arg)[index][f_index].append(msg.author.id)
            try:
                ARR.get(arg*(-1))[index][f_index].remove(msg.author.id)
            except ValueError:
                pass
            await ctx.channel.send(VOTE_ALIGN.get(arg).capitalize() + ' Sent!')
            return True
        await ctx.channel.send('You can\'t ' + VOTE_ALIGN.get(arg) + ' a food you\'ve already ' + VOTE_ALIGN.get(arg) + 'd!')
        should_complete = True
    else:
        should_complete = False
    return should_complete

async def vote(arg, food, ctx):
    """adds author to likes/dislikes array for [food]"""
    index = 0
    f_index = 0
    class Exit(Exception):
        """custom exception class for detecting item is found"""
        pass
    if food is None:
        await ctx.channel.send(INVALID_USAGE)
        return
    try:
        for centers in food_list:
            for meal in centers:
                if await append_vote(ctx, food, centers, meal, index, f_index, arg):
                    raise Exit
                f_index += 1
            index += 1
            f_index = 0
        await ctx.channel.send("Couldn't find given food.")
    except Exit:
        pass

@bot.command(pass_context=True)
async def upvote(ctx, food=None):
    """discord command that adds author to likes array for [food]"""
    await vote(1, food, ctx)

@bot.command(pass_context=True)
async def downvote(ctx, food=None):
    """discord command that adds author to dislikes array for [food]"""
    await vote(-1, food, ctx)

def get_score(food, centers):
    """returns the score of [food] at [center]."""
    score, f_index, index = 0,0,0
    for meal in food_list[centers]:
        if food in meal:
            score += len(food_likes[centers][f_index])
            score -= len(food_dislikes[centers][f_index])
        f_index += 1
    return score

@tasks.loop(seconds=1800)
async def save():
    """saves arrays to file"""
    print("Saving...")
    await save_scores('food_likes',food_likes)
    await save_scores('food_dislikes',food_dislikes)
    await save_scores('food_list',food_list)
    print(CMP)

async def load():
    """loads arrays from file"""
    print("Loading...")
    global food_likes
    global food_dislikes
    global food_list
    food_likes = await load_scores('food_likes')
    food_dislikes = await load_scores('food_dislikes')
    food_list = await load_scores('food_list')
    print(CMP)

@bot.command(pass_context=True)
async def manual_save(ctx):
    """discord command for saving"""
    if ctx.message.author.name == 'Swidex':
        await save()

bot.run(DISCORD_TOKEN)