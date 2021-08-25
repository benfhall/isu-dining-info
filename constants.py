TITLES = ["Union Drive Marketplace","Friley Windows","Seasons Marketplace","Memorial Union Food Court"]
THUMBNAIL = [
    "https://i.imgur.com/WyZ5ie1.png",
    "https://i.imgur.com/JB7opTP.png",
    "https://i.imgur.com/HJou7mT.png",
    "https://i.imgur.com/x8ahz6h.png"]
CMP = "Complete!"
TIME_NAMES = [
    ["Breakfast","Lunch","Dinner"],
    ["Lunch","Dinner"],
    ["Breakfast","Lunch","Dinner"],
    ["Lunch","Daily","Bakery"]
    ]
STATIONS = [
    [],
    [],
    [],
    []
    ]
TIMES = [
    {'Breakfast': 0, 'Lunch': 1, 'Dinner': 2},
    {'Lunch': 0, 'Dinner': 1},
    {'Breakfast':0,'Lunch': 1, 'Dinner': 2},
    {'Lunch':0,'Daily Menu':1,'Bakery Menu':2}
    ]
URLS = [
    "https://www.dining.iastate.edu/wp-json/dining/menu-hours/get-single-location/?slug=union-drive-marketplace-2-2",
    "https://www.dining.iastate.edu/wp-json/dining/menu-hours/get-single-location/?slug=friley-windows-2-2",
    "https://www.dining.iastate.edu/wp-json/dining/menu-hours/get-single-location/?slug=seasons-marketplace-2-2",
    "https://www.dining.iastate.edu/wp-json/dining/menu-hours/get-single-location/?slug=memorial-union-food-court-2"
    ]
HEADERS = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }
