STATION_TITLES = [
    ["\n**Cardinal Canteen**:\n","\n**Picoso**:\n","\n**Dagwood's**:\n","\n**Parma's**:\n","\n**Sugar Sugar**:\n","\n**Sprout**:\n","\n**Saikuron**:\n","\n\n"],
    ["\n**Simmer**\n","\n**Zest**:\n","\n**Slice**:\n","\n**Savor**:\n","\n**Chopped**\n","\n**Delish**\n","\n\n"],
    ["\n**Hickory's**\n","\n**Wood Grill**:\n","\n**Bonsai**:\n","\n**Cocoa Bean**:\n","\n**Olive Branch**:\n","\n**Bushel Basket**:\n","\n\n"]]

CLOSED = ["\nLooks like "," is closed for ", " or you need to reload the menus!"]
TITLES = ["**Union Drive Marketplace**","**Friley Windows**","**Seasons Marketplace**"]
OFFSET = [0,1,0]
CMP = "Complete!"
ALL_TIMES = ["breakfast","lunch","dinner","daily"]
TIME_NAME = ["**Breakfast**","**Lunch**","**Dinner**","**Daily**"]

STATIONS = [
        {'Cardinal Canteen': 0, 'Picoso': 1, 'Dagwood\'s': 2, 'Parma\'s': 3,'Sugar Sugar': 4, 'Sprout': 5, 'Saikuron': 6, "":7},
        {'Simmer': 0, 'Zest': 1, 'Slice': 2, 'Savor': 3, 'Chopped': 4, 'Delish': 5,'':6},
        {'Hickory\'s': 0, 'Wood Grill': 1, 'Bonsai': 2,'Cocoa Bean': 3, 'Olive Branch': 4, 'Bushel Basket': 5,'':6}]
TIMES = [
    {'Breakfast': 0, 'Lunch': 1, 'Dinner': 2},
    {'Lunch': 0, 'Dinner': 1},
    {'Breakfast':0,'Lunch': 1, 'Dinner': 2, 'Daily Menu': 3}]

STATION = [
    {'Cardinal Canteen': 0, 'Picoso': 1, 'Dagwood\'s': 2, 'Parma\'s': 3,'Sugar Sugar': 4, 'Sprout': 5, 'Saikuron': 6, "":7},
    {'Simmer': 0, 'Zest': 1, 'Slice': 2, 'Savor': 3,'Chopped':4,'Delish':5,'':6},
    {'Hickory\'s': 0, 'Wood Grill': 1, 'Bonsai': 2, 'Cocoa Bean': 3, 'Olive Branch': 4, 'Bushel Basket': 5,'':6}]
TIMES = [
    {'Breakfast': 0, 'Lunch': 1, 'Dinner': 2},
    {'Lunch': 0, 'Dinner': 1},
    {'Breakfast':0,'Lunch': 1, 'Dinner': 2, 'Daily Menu': 3}]

INVALID_USAGE = "**Invalid Usage.**\n*use !help for help.*"
URLS = [
    "https://www.dining.iastate.edu/wp-json/dining/menu-hours/get-single-location/?slug=union-drive-marketplace-2-2",
    "https://www.dining.iastate.edu/wp-json/dining/menu-hours/get-single-location/?slug=friley-windows-2-2",
    "https://www.dining.iastate.edu/wp-json/dining/menu-hours/get-single-location/?slug=seasons-marketplace-2-2"]
HEADERS = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }