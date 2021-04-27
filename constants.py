STATION_TITLES = [
    ["Cardinal Canteen","Parma's","Saikuron","Picoso","Dagwood's","Sugar Sugar","Sprout","Other"],
    ["Simmer","Zest","Slice","Savor","Chopped","Delish","Other"],
    ["Hickory's","Wood Grill","Bonsai","Cocoa Bean","Olive Branch","Bushel Basket","Other"]]
TITLES = ["Union Drive Marketplace","Friley Windows","Seasons Marketplace"]
THUMBNAIL = ["https://i.imgur.com/WyZ5ie1.png","https://i.imgur.com/JB7opTP.png","https://i.imgur.com/HJou7mT.png"]
OFFSET = [0,1,0]
CMP = "Complete!"
ALL_TIMES = ["breakfast","lunch","dinner","daily"]
TIME_NAME = ["Breakfast","Lunch","Dinner","Daily"]
TIMES = [
    {'Breakfast': 0, 'Lunch': 1, 'Dinner': 2},
    {'Lunch': 0, 'Dinner': 1},
    {'Breakfast':0,'Lunch': 1, 'Dinner': 2, 'Daily Menu': 3}]
STATIONS = [
    {'Cardinal Canteen': 0, 'Parma\'s': 1, 'Saikuron': 2, 'Picoso': 3, 'Dagwood\'s': 4, 'Sugar Sugar': 5, 'Sprout': 6, "":7},
    {'Simmer': 0, 'Zest': 1, 'Slice': 2, 'Savor': 3,'Chopped':4,'Delish':5,'':6},
    {'Hickory\'s': 0, 'Wood Grill': 1, 'Bonsai': 2, 'Cocoa Bean': 3, 'Olive Branch': 4, 'Bushel Basket': 5,'':6}]
TIMES = [
    {'Breakfast': 0, 'Lunch': 1, 'Dinner': 2},
    {'Lunch': 0, 'Dinner': 1},
    {'Breakfast':0,'Lunch': 1, 'Dinner': 2}]
INVALID_USAGE = "**Invalid Usage.***use !help for help.*"
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
