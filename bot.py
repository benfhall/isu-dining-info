# bot.py
import os, discord, urllib.request, urllib.error, urllib.parse, json, ssl
from dotenv import load_dotenv
from discord.ext import tasks

url_udcc="https://www.dining.iastate.edu/wp-json/dining/menu-hours/get-single-location/?slug=union-drive-marketplace-2-2"
url_windows="https://www.dining.iastate.edu/wp-json/dining/menu-hours/get-single-location/?slug=friley-windows-2-2"
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {
        'User-Agent':user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

udcc_cc, udcc_p, udcc_d, udcc_pa = [[] for r in range(3)],[[] for r in range(3)],[[] for r in range(3)],[[] for r in range(3)]
windows_s, windows_z, windows_sl, windows_sv = [[] for r in range(2)],[[] for r in range(2)],[[] for r in range(2)],[[] for r in range(2)]

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@tasks.loop(seconds=10800)
async def load_menus():
    global udcc_cc
    global udcc_p
    global udcc_d 
    global udcc_pa
    global windows_s
    global windows_z
    global windows_sl
    global windows_sv

    print('Reloading Menus...')
    gcontext = ssl.SSLContext()
    request=urllib.request.Request(url_windows,None,headers)
    with urllib.request.urlopen(request, context=gcontext) as url:
        data = json.loads(url.read().decode())

    udcc_cc, udcc_p, udcc_d, udcc_pa = [[] for r in range(3)],[[] for r in range(3)],[[] for r in range(3)],[[] for r in range(3)]
    windows_s, windows_z, windows_sl, windows_sv = [[] for r in range(2)],[[] for r in range(2)],[[] for r in range(2)],[[] for r in range(2)]
    options_windows = {'Lunch': 0, 'Dinner': 1}
    for time in data[0]["menus"]:
        for bar in time["menuDisplays"]:
            for food in bar['categories'][0]['menuItems']:
                if bar['name'] == "Simmer":
                    windows_s[options_windows.get(time['section'])].append(food['name'])
                if bar['name'] == "Zest":
                    windows_z[options_windows.get(time['section'])].append(food['name'])
                if bar['name'] == "Slice":
                    windows_sl[options_windows.get(time['section'])].append(food['name'])
                if bar['name'] == "Savor":
                    windows_sv[options_windows.get(time['section'])].append(food['name'])

    request=urllib.request.Request(url_udcc,None,headers)
    with urllib.request.urlopen(request) as url:
        data = json.loads(url.read().decode())

    options_udcc = {'Breakfast': 0, 'Lunch': 1, 'Dinner': 2}
    for time in data[0]["menus"]:
        for bar in time["menuDisplays"]:
            for food in bar['categories'][0]['menuItems']:
                if bar['name'] == "Cardinal Canteen":
                    udcc_cc[options_udcc.get(time['section'])].append(food['name'])
                if bar['name'] == "Picoso":
                    udcc_p[options_udcc.get(time['section'])].append(food['name'])
                if bar['name'] == "Dagwood's":
                    udcc_d[options_udcc.get(time['section'])].append(food['name'])
                if bar['name'] == "Parma's":
                    udcc_pa[options_udcc.get(time['section'])].append(food['name'])
    print("Complete!")

@client.event
async def on_message(message):
    PICOSO = "\n**Picoso**:\n"
    DAGWOOD = "\n**Dagwood's**:\n"
    PARMA = "\n**Parma's**:\n"
    SLICE = "\n**Slice**:\n"
    ZEST = "\n**Zest**:\n"
    SAVOR = "\n**Savor**:\n"
    if '!reload' in message.content.lower():
        load_menus()
        await message.channel.send("Reloaded Menus!")
    if '!help' in message.content.lower():
        response = "!**<time>**_**<building>** - *find the menu for given <time> at given <building>*\n\n**<time>** - Breakfast/Lunch/Dinner *(breakfast not available for Windows)*\n\n**<building>** - windows/udcc\n\n!**reload** - *reloads the menu.*"
        await message.channel.send(response)
    if '!breakfast_udcc' in message.content.lower():
        response = "**Breakfast** at **Union Market Drive:** \n\n**Cardinal Canteen**: \n"
        for food in udcc_cc[0]:
            response += food
            response += "\n"

        response += PICOSO
        for food in udcc_p[0]:
            response += food
            response += "\n"

        response += DAGWOOD
        for food in udcc_d[0]:
            response += food
            response += "\n"

        response += PARMA
        for food in udcc_pa[0]:
            response += food
            response += "\n"
        
        await message.channel.send(response)
    if '!lunch_udcc' in message.content.lower():
        response = "**Lunch** at **Union Market Drive:** \n\n**Cardinal Canteen**: \n"
        for food in udcc_cc[1]:
            response += food
            response += "\n"

        response += PICOSO
        for food in udcc_p[1]:
            response += food
            response += "\n"

        response += DAGWOOD
        for food in udcc_d[1]:
            response += food
            response += "\n"

        response += PARMA
        for food in udcc_pa[1]:
            response += food
            response += "\n"
        await message.channel.send(response)
    if '!dinner_udcc' in message.content.lower():
        response = "**Dinner** at **Union Market Drive:** \n\n**Cardinal Canteen**: \n"
        for food in udcc_cc[2]:
            response += food
            response += "\n"

        response += PICOSO
        for food in udcc_p[2]:
            response += food
            response += "\n"

        response += DAGWOOD
        for food in udcc_d[2]:
            response += food
            response += "\n"

        response += PARMA
        for food in udcc_pa[2]:
            response += food
            response += "\n"
        await message.channel.send(response)
    if '!lunch_windows' in message.content.lower():
        response = "**Lunch** at **Friley Windows:** \n\n**Simmer**: \n"
        for food in windows_s[0]:
            response += food
            response += "\n"

        response += ZEST
        for food in windows_z[0]:
            response += food
            response += "\n"

        response += SLICE
        for food in windows_sl[0]:
            response += food
            response += "\n"

        response += SAVOR
        for food in windows_sv[0]:
            response += food
            response += "\n"
        await message.channel.send(response)
    if '!dinner_windows' in message.content.lower():
        response = "**Dinner** at **Friley Windows:** \n\n**Simmer**: \n"
        for food in windows_s[1]:
            response += food
            response += "\n"

        response += ZEST
        for food in windows_z[1]:
            response += food
            response += "\n"

        response += SLICE
        for food in windows_sl[1]:
            response += food
            response += "\n"

        response += SAVOR
        for food in windows_sv[1]:
            response += food
            response += "\n"
        await message.channel.send(response)

load_menus.start()
client.run(TOKEN)
