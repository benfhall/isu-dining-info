import urllib.request, urllib.error, urllib.parse, json, ssl

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

print(udcc)