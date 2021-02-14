# bot.py
import os, discord, urllib.request, urllib.error, urllib.parse, json, ssl
from dotenv import load_dotenv
from discord.ext import tasks

url_udcc="https://www.dining.iastate.edu/wp-json/dining/menu-hours/get-single-location/?slug=union-drive-marketplace-2-2"
url_windows="https://www.dining.iastate.edu/wp-json/dining/menu-hours/get-single-location/?slug=friley-windows-2-2"
url_seasons="https://www.dining.iastate.edu/wp-json/dining/menu-hours/get-single-location/?slug=seasons-marketplace-2-2"

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {
        'User-Agent':user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }

ssl._create_default_https_context = ssl._create_unverified_context

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

udcc = [[[]for c in range(3)] for r in range(6)]
windows = [[[]]for r in range(2) for r in range(4)]
seasons = [[[]for c in range(3)] for r in range(6)]

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@tasks.loop(seconds=10800)
async def load_menus():
    global udcc
    global windows
    global seasons

    print('Reloading Menus...')
    gcontext = ssl.SSLContext()
    request=urllib.request.Request(url_windows,None,headers)
    with urllib.request.urlopen(request, context=gcontext) as url:
        data = json.loads(url.read().decode())

    udcc = [[[]for c in range(3)] for r in range(6)]
    windows = [[[]]for r in range(2) for r in range(4)]
    seasons = [[[]for c in range(3)] for r in range(6)]
    
    windows_bar = {'Simmer': 0, 'Zest': 1, 'Slice\'s': 2, 'Savor': 3}
    windows_time = {'Lunch': 0, 'Dinner': 1}
    for time in data[0]["menus"]:
        for bar in time["menuDisplays"]:
            for food in bar['categories'][0]['menuItems']:
                windows[windows_bar.get(bar['name'])][windows_time.get(time['section'])].append(food['name'])

    request=urllib.request.Request(url_udcc,None,headers)
    with urllib.request.urlopen(request) as url:
        data = json.loads(url.read().decode())
    udcc_bar = {'Cardinal Canteen': 0, 'Picoso': 1, 'Dagwood\'s': 2, 'Parma\'s': 3, 'Sugar Sugar': 4, 'Sprout': 5}
    udcc_time = {'Breakfast': 0, 'Lunch': 1, 'Dinner': 2}
    for time in data[0]["menus"]:
        for bar in time["menuDisplays"]:
            for food in bar['categories'][0]['menuItems']:
                udcc[udcc_bar.get(bar['name'])][udcc_time.get(time['section'])].append(food['name'])

    request=urllib.request.Request(url_seasons,None,headers)
    with urllib.request.urlopen(request) as url:
        data = json.loads(url.read().decode())
    seasons_time = {'Lunch': 0, 'Dinner': 1, 'Daily Menu': 2}
    seasons_bar = {'Hickory\'s': 0, 'Wood Grill': 1, 'Bonsai': 2, 'Cocoa Bean': 3, 'Olive Branch': 4, 'Bushel Basket': 5}
    for time in data[0]["menus"]:
        for bar in time["menuDisplays"]:
            for food in bar['categories'][0]['menuItems']:
                seasons[seasons_bar.get(bar['name'])][seasons_time.get(time['section'])].append(food['name'])
    print("Complete!")

@client.event
async def on_message(message):
    UDCC = ["\n**Cardinal Canteen**\n","\n**Picoso**:\n","\n**Dagwood's**:\n","\n**Parma's**:\n","\n**Sugar Sugar**:\n","\n**Sprout**:\n"]
    WINDOWS = ["\n**Simmer**\n","\n**Zest**:\n","\n**Slice**:\n","\n**Savor**:\n"]
    SEASONS = ["\n**Hickory's**\n","\n**Wood Grill**:\n","\n**Bonsai**:\n","\n**Cocoa Bean**:\n","\n**Olive Branch**:\n","\n**Bushel Basket**:\n"]
    CLOSED_UDCC = "\nLooks like Union Drive Marketplace is closed, or you need to reload the menus!"
    CLOSED_WINDOWS = "\nLooks like Friley Windows is closed, or you need to reload the menus!"
    CLOSED_SEASONS = "\nLooks like Seasons Marketplace is closed, or you need to reload the menus!"

    if '!reload' in message.content.lower():
        load_menus()
        await message.channel.send("Reloaded Menus!")
    if '!help' in message.content.lower():
        response = ""
        response = "!**<building>** **<time>** - *find the menu for given <time> at given <building>*\n\n**<time>** - Breakfast/Lunch/Dinner *(breakfast not available for Windows)*\n\n**<building>** - windows/udcc\n\n!**reload** - *reloads the menu.*\n\n!**tendies <time>** - *checks if there are tendies, given time.*"
        await message.channel.send(response)
    if '!udcc breakfast' in message.content.lower():
        counter = 0
        closed = 1
        response = "**Breakfast** at **Union Drive Marketplace:** \n"
        for bar in udcc[0]:
            if not bar:
                closed = 1
            else:
                closed = 0
                break
        if closed == 1:
            response += CLOSED_UDCC
        else:
            for bar in udcc:
                response += UDCC[counter]
                counter += 1
                for food in bar[0]:
                    response += food
                    response += "\n"
        await message.channel.send(response)
    if '!udcc lunch' in message.content.lower():
        counter = 0
        closed = 1
        response = "**Lunch** at **Union Drive Marketplace:** \n"
        for bar in udcc[1]:
            if not bar:
                closed = 1
            else:
                closed = 0
                break
        if closed == 1:
            response += CLOSED_UDCC
        else:
            for bar in udcc:
                response += UDCC[counter]
                counter += 1
                for food in bar[1]:
                    response += food
                    response += "\n"
        await message.channel.send(response)
    if '!udcc dinner' in message.content.lower():
        counter = 0
        closed = 1
        response = "**Dinner** at **Union Drive Marketplace:** \n"
        for bar in udcc[2]:
            if not bar:
                closed = 1
            else:
                closed = 0
                break
        if closed == 1:
            response += CLOSED_UDCC
        else:
            for bar in udcc:
                response += UDCC[counter]
                counter += 1
                for food in bar[2]:
                    response += food
                    response += "\n"
        await message.channel.send(response)
    if '!windows lunch' in message.content.lower():
        counter = 0
        closed = 1
        response = "**Lunch** at **Friley Windows:** \n"
        for bar in windows[0]:
            if not bar:
                closed = 1
            else:
                closed = 0
                break
        if closed == 1:
            response += CLOSED_WINDOWS
        else:
            for bar in windows:
                response += WINDOWS[counter]
                counter += 1
                for food in bar[0]:
                    response += food
                    response += "\n"
        await message.channel.send(response)
    if '!windows dinner' in message.content.lower():
        counter = 0
        closed = 1
        response = "**Dinner** at **Friley Windows:** \n"
        for bar in windows[1]:
            if not bar:
                closed = 1
            else:
                closed = 0
                break
        if closed == 1:
            response += CLOSED_WINDOWS
        else:
            for bar in windows:
                response += WINDOWS[counter]
                counter += 1
                for food in bar[1]:
                    response += food
                    response += "\n"
        await message.channel.send(response)
    if '!seasons lunch' in message.content.lower():
        counter = 0
        closed = 1
        response = "**Lunch** at **Seasons Marketplace:** \n"
        for bar in seasons[0]:
            if not bar:
                closed = 1
            else:
                closed = 0
                break
        if closed == 1:
            response += CLOSED_SEASONS
        else:
            for bar in seasons:
                response += SEASONS[counter]
                counter += 1
                for food in bar[0]:
                    response += food
                    response += "\n"
        await message.channel.send(response)
    if '!seasons dinner' in message.content.lower():
        counter = 0
        closed = 1
        response = "**Dinner** at **Seasons Marketplace:** \n"
        for bar in seasons[1]:
            if not bar:
                closed = 1
            else:
                closed = 0
                break
        if closed == 1:
            response += CLOSED_SEASONS
        else:
            for bar in seasons:
                response += SEASONS[counter]
                counter += 1
                for food in bar[1]:
                    response += food
                    response += "\n"
        await message.channel.send(response)
    if '!seasons daily' in message.content.lower():
        counter = 0
        closed = 1
        response = "**Daily Menu** at **Seasons Marketplace:** \n"
        for bar in seasons[2]:
            if not bar:
                closed = 1
            else:
                closed = 0
                break
        if closed == 1:
            response += CLOSED_SEASONS
        else:
            for bar in seasons:
                response += SEASONS[counter]
                counter += 1
                for food in bar[2]:
                    response += food
                    response += "\n"
        await message.channel.send(response)
    if '!tendies dinner' in message.content.lower():
        response = ""
        closed = 1
        for bar in udcc[2]:
            if not bar:
                closed = 1
            else:
                closed = 0
                break
        if closed == 0:
            for bar in udcc:
                for food in bar[2]:
                    if "tender" in food.lower():
                        print(food)
                        response += "Union Drive Marketplace has " + food + ".\n"
        closed = 1
        for bar in windows[1]:
            if not bar:
                closed = 1
            else:
                closed = 0
                break
        if closed == 0:      
            for bar in windows:
                for food in bar[1]:
                    if "tender" in food:
                        response += "Friley Windows has " + food + ".\n"
        closed = 1
        for bar in seasons[1]:
            if not bar:
                closed = 1
            else:
                closed = 0
                break
        if closed == 0:
            for bar in seasons:
                for food in bar[1]:
                    if "tender" in food:
                        response += "Seasons Marketplace has " + food + ".\n"
        if response == "":
            response += "None of the given dining centers has Tendies :("
        await message.channel.send(response)
    if '!tendies lunch' in message.content.lower():
        response = ""
        closed = 1
        for bar in udcc[1]:
            if not bar:
                closed = 1
            else:
                closed = 0
                break
        if closed == 0:
            for bar in udcc:
                for food in bar[1]:
                    if "tender" in food.lower():
                        print(food)
                        response += "Union Drive Marketplace has " + food + ".\n"
        closed = 1
        for bar in windows[0]:
            if not bar:
                closed = 1
            else:
                closed = 0
                break
        if closed == 0:      
            for bar in windows:
                for food in bar[0]:
                    if "tender" in food:
                        response += "Friley Windows has " + food + ".\n"
        closed = 1
        for bar in seasons[0]:
            if not bar:
                closed = 1
            else:
                closed = 0
                break
        if closed == 0:
            for bar in seasons:
                for food in bar[0]:
                    if "tender" in food:
                        response += "Seasons Marketplace has " + food + ".\n"
        if response == "":
            response += "None of the given dining centers has Tendies :("
        await message.channel.send(response)

load_menus.start()
client.run(TOKEN)
