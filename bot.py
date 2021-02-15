# bot.py
import os, discord, urllib.request, urllib.error, urllib.parse, json, ssl
from dotenv import load_dotenv
from discord.ext import tasks, commands

BAR_TITLES = [["\n**Cardinal Canteen**:\n","\n**Picoso**:\n","\n**Dagwood's**:\n","\n**Parma's**:\n","\n**Sugar Sugar**:\n","\n**Sprout**:\n","\n**Saikuron**:\n","\n\n"],["\n**Simmer**\n","\n**Zest**:\n","\n**Slice**:\n","\n**Savor**:\n","\n**Chopped**\n","\n**Delish**\n","\n\n"],["\n**Hickory's**\n","\n**Wood Grill**:\n","\n**Bonsai**:\n","\n**Cocoa Bean**:\n","\n**Olive Branch**:\n","\n**Bushel Basket**:\n","\n\n"]]
CLOSED = ["\nLooks like "," is closed for ", " or you need to reload the menus!"]
TITLES = ["**Union Drive Marketplace**","**Friley Windows**","**Seasons Marketplace**"]
OFFSET = [0,1,0]
ALL_TIMES = ["breakfast","lunch","dinner","daily"]
MEAL_NAME = ["**Breakfast**","**Lunch**","**Dinner**","**Daily**"]

BARS = [{'Cardinal Canteen': 0, 'Picoso': 1, 'Dagwood\'s': 2, 'Parma\'s': 3, 'Sugar Sugar': 4, 'Sprout': 5, 'Saikuron': 6, "":7},{'Simmer': 0, 'Zest': 1, 'Slice': 2, 'Savor': 3,'Chopped':4,'Delish':5,'':6},{'Hickory\'s': 0, 'Wood Grill': 1, 'Bonsai': 2, 'Cocoa Bean': 3, 'Olive Branch': 4, 'Bushel Basket': 5,'':6}]
TIMES = [{'Breakfast': 0, 'Lunch': 1, 'Dinner': 2},{'Lunch': 0, 'Dinner': 1},{'Breakfast':0,'Lunch': 1, 'Dinner': 2, 'Daily Menu': 3}]

INVALID_USAGE = "**Invalid Usage.**\n*use !help for help.*"
URLS = ["https://www.dining.iastate.edu/wp-json/dining/menu-hours/get-single-location/?slug=union-drive-marketplace-2-2","https://www.dining.iastate.edu/wp-json/dining/menu-hours/get-single-location/?slug=friley-windows-2-2","https://www.dining.iastate.edu/wp-json/dining/menu-hours/get-single-location/?slug=seasons-marketplace-2-2"]
HEADERS = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }

udcc = [[[]for c in range(3)] for r in range(8)]
windows = [[[]for c in range(2)] for r in range(6)]
seasons = [[[]for c in range(4)] for r in range(6)]
food_list = [[]for c in range(3)]
food_likes = [[[]]for c in range(3)]
food_dislikes = [[[]]for c in range(3)]
BUILDINGS = {0:udcc,1:windows,2:seasons}

gcontext = ssl.SSLContext()
load_dotenv()
ssl._create_default_https_context = ssl._create_unverified_context
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix="!", help_command=None)

@tasks.loop(seconds=10800)
async def load_menus():
    global udcc
    global windows
    global seasons
    global BARS
    global TIMES
    global BUILDINGS

    udcc = [[[]for c in range(3)] for r in range(8)]
    windows = [[[]for c in range(2)] for r in range(7)]
    seasons = [[[]for c in range(4)] for r in range(7)]

    BARS = [{'Cardinal Canteen': 0, 'Picoso': 1, 'Dagwood\'s': 2, 'Parma\'s': 3, 'Sugar Sugar': 4, 'Sprout': 5, 'Saikuron': 6, "":7},{'Simmer': 0, 'Zest': 1, 'Slice': 2, 'Savor': 3, 'Chopped': 4, 'Delish': 5,'':6},{'Hickory\'s': 0, 'Wood Grill': 1, 'Bonsai': 2, 'Cocoa Bean': 3, 'Olive Branch': 4, 'Bushel Basket': 5,'':6}]
    TIMES = [{'Breakfast': 0, 'Lunch': 1, 'Dinner': 2},{'Lunch': 0, 'Dinner': 1},{'Breakfast':0,'Lunch': 1, 'Dinner': 2, 'Daily Menu': 3}]
    BUILDINGS = {0:udcc,1:windows,2:seasons}
    cindex = 0

    print('Reloading Menus...')
    for url in URLS:
        request=urllib.request.Request(url,None,HEADERS)
        with urllib.request.urlopen(request, context=gcontext) as url:
            data = json.loads(url.read().decode())
        for mealtime in data[0]["menus"]:
            for bar in mealtime["menuDisplays"]:
                for food_type in bar['categories']:
                    for food in food_type['menuItems']:
                        try: 
                            BUILDINGS.get(cindex)[BARS[cindex].get(bar['name'])][TIMES[cindex].get(mealtime['section'])].append(food['name'])
                            if food['name'] in food_list[cindex]:
                                food_list[cindex].append(food['name'])
                                food_likes[cindex].append([])
                                food_dislikes[cindex].append([])
                        except TypeError:
                            print("Err: Bar name mismatch, putting in general category.")
                            BUILDINGS.get(cindex)[len(BARS[cindex]-1)][TIMES[cindex].get(mealtime['section'])].append(food['name'])
                            if food['name'] in food_list[cindex]:
                                food_list[cindex].append(food['name'])
                                food_likes[cindex].append([])
                                food_dislikes[cindex].append([])

        cindex += 1
    print("Complete!")
    
def match_args(arg, args):
    if arg is None:
        return False
    elif arg.lower() in args:
        return True
    else:
        return False

def give_menu(arg, place):
    counter = 0
    rating_score = []
    rated_food = []
    response = ""
    if is_closed(place, arg):
        response += CLOSED[0] + TITLES[place] + CLOSED[1] + MEAL_NAME[TIMES[place].get(arg)+OFFSET[place]] + CLOSED[2]
    else:
        response += MEAL_NAME[TIMES[place].get(arg)+OFFSET[place]] + " at " + TITLES[place] + "\n"
        for bar in BUILDINGS.get(place):
            if bar[TIMES[place].get(arg)]:  
                response += BAR_TITLES[place][counter]
                counter += 1
                for food in bar[TIMES[place].get(arg)]:
                    rating_score.append(get_score(food,place))
                    rated_food.append(food)
                    response += food + "\n"
    try:
        max_index = rating_score.index(max(rating_score))
        if rating_score[max_index] != 0:
            response += "```Your peers recommend the following dishes: \n\n"
            for x in range(3):
                max_index = rating_score.index(max(rating_score))
                if rating_score[max_index] == 0:
                    break
                response += rated_food[max_index] + " (+" + str(rating_score[max_index]) + ")\n"
                rated_food.pop(max_index)
                rating_score.pop(max_index)
            response += "\n\nRecommend your favorite dishes with the command, !upvote [dish] and !downvote [dish]```"
    except ValueError:
        pass
    return response

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await load_menus()

@bot.command(pass_context=True)
async def help(ctx, time=None):
    await ctx.channel.send("""```
![building] [time]      :   find the menu for given [time] at given [building]
!search [term] [time]   :   searches for [term] at all dining centers, given [time].
!tendies [time] :   searches for tender, [time] is optional.
!nuggies [time] :   searches for nugget, [time] is optional.
!wingies [time]   :   searches for wing, [time] is optional.
!reload         :   reloads the menu.
!help           :   displays options and usage of commands.\n
    [building]  :   udcc/windows/seasons
    [time]      :   breakfast/lunch/dinner (breakfast not available for Windows)
```""")

@bot.command(pass_context=True)
async def udcc(ctx, arg=None):
    args = ["breakfast","lunch","dinner"]
    if match_args(arg, args):
        response = give_menu(arg.capitalize(), 0)
    else:
        response = INVALID_USAGE
    await ctx.channel.send(response)

@bot.command(pass_context=True)
async def windows(ctx, arg=None):
    args = ["lunch","dinner"]
    if match_args(arg, args):
        response = give_menu(arg.capitalize(), 1)
    else:
        response = INVALID_USAGE
    await ctx.channel.send(response)

@bot.command(pass_context=True)
async def seasons(ctx, arg=None):
    args = ["breakfast","lunch","dinner","daily"]
    if match_args(arg, args):
        response = give_menu(arg.capitalize(), 2)
    else:
        response = INVALID_USAGE
    await ctx.channel.send(response)

def is_closed(place,time):
    for bar in BUILDINGS.get(place)[TIMES[place].get(time.capitalize())]:
        if not not bar:
            return False
    return False

def search_for(substring, time):
    response = ""
    if match_args(time,ALL_TIMES) and substring is not None:
        for place in range(3):
            if not is_closed(place,time):
                for bar in BUILDINGS.get(place):
                    for food in bar[TIMES[place].get(time.capitalize())]:
                        if substring.lower() in food.lower():
                            response += TITLES[place] + " has: *" + food + "* for " + MEAL_NAME[TIMES[place].get(time.capitalize())+OFFSET[place]] + ".\n"
        if response == "":
            response = "Search term: **" + substring + "** not found at **" + time + "**.\n" 
    else:
        response = "**Invalid Usage.** Please add a valid search term or time period.\n*use !help for help.*"
    return response

@bot.command(pass_context=True)
async def search(ctx, substring=None, time=None):
    await ctx.channel.send(search_for(substring,time))

@bot.command(pass_context=True)
async def tendies(ctx, time=None):
    if time is None:
        response = search_for("tender", "lunch") + search_for("tender", "dinner")
    elif match_args(time,ALL_TIMES):
        response = search_for("tender",time)
    else:
        response = INVALID_USAGE
    await ctx.channel.send(response)

@bot.command(pass_context=True)
async def nuggies(ctx, time=None):
    if time is None:
        response = search_for("nugget", "lunch") + search_for("nugget", "dinner")
    elif match_args(time,ALL_TIMES):
        response = search_for("nugget",time)
    else:
        response = INVALID_USAGE
    await ctx.channel.send(response)

@bot.command(pass_context=True)
async def wingies(ctx, time=None):
    if time is None:
        response = search_for("wing", "lunch") + search_for("wing", "dinner")
    elif match_args(time,ALL_TIMES):
        response = search_for("wing",time)
    else:
        response = INVALID_USAGE
    await ctx.channel.send(response)

@bot.command(pass_context=True)
async def reload(ctx, time=None):
    await load_menus()
    await ctx.channel.send("Reloaded menus!")

async def vote(arg, food, ctx):
    ARR = {1:food_likes,-1:food_dislikes}
    VOTE_ALIGN = {1:"upvote",-1:"downvote"}
    index = 0
    f_index = 0
    if food is None:
        await ctx.channel.send(INVALID_USAGE)
    else:
        for centers in food_list:
            for meal in centers:
                if food in meal:
                    await ctx.channel.send("Did you mean: *" + meal + "* from *" + TITLES[index] + "*? (y/n)")
                    msg = await bot.wait_for('message')
                    if msg.content == 'y':
                        if (msg.author.id not in ARR.get(arg)[index][f_index]):
                            ARR.get(arg)[index][f_index].append(msg.author.id)
                            try:
                                ARR.get(arg*(-1))[index][f_index].remove(msg.author.id)
                            except ValueError:
                                pass
                            await ctx.channel.send(VOTE_ALIGN.get(arg).capitalize() + ' Sent!')
                            break
                        else:
                            await ctx.channel.send('You can\'t ' + VOTE_ALIGN.get(arg) + ' a food you\'ve already ' + VOTE_ALIGN.get(arg) + 'd!')
                            break        
                f_index += 1
            index += 1

@bot.command(pass_context=True)
async def upvote(ctx, food=None):
    await vote(1, food, ctx)

@bot.command(pass_context=True)
async def downvote(ctx, food=None):
    await vote(-1, food, ctx)

def get_score(food, centers):
    score, f_index, index = 0,0,0
    for meal in food_list[centers]:
        if food in meal:
            score += len(food_likes[centers][f_index])
            score -= len(food_dislikes[centers][f_index])
        f_index += 1
    return score

@bot.command(pass_context=True)
async def save(ctx):
    await save_likes()

@bot.command(pass_context=True)
async def open(ctx):
    await open_likes()
                          
bot.run(DISCORD_TOKEN)