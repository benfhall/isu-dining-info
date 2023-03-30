import requests, json, asyncio, logging
from constants import *

class DiningHall():
    uri = ""
    raw_data = []
    
    name = ""
    thumbnail_uri = ""
    dietary_type = []
    sections = []

    def __init__(self, uri):
        self.uri = uri

    def dump_data(self):
        with open("sample.json", "w") as outfile:
            outfile.write(json.dumps(self.raw_data[0]["menus"][0], indent=4))

    async def fetch_data(self):
        r = requests.get(self.uri, headers=HEADERS)
        r.raise_for_status()
        if r.status_code != 204:
            self.raw_data = r.json()

    async def populate(self):
        """populate class with data from json response"""
        self.dietary_type = []
        self.sections = []

        self.name = self.raw_data[0]["title"]
        self.thumbnail_uri = self.raw_data[0]["gallery"][0]
        for diet in self.raw_data[0]["dietaryType"]:
            self.dietary_type.append(diet)

        for s in self.raw_data[0]["menus"]:
            newS = Section(s)
            self.sections.append(newS)

class Section():
    name = ""
    emoji = ""
    menus = []

    def __init__(self, section_data):
        self.menus = []
        self.name = section_data["section"]
        for m in section_data["menuDisplays"]:
            self.menus.append(Menu(m))
            

class Menu():
    name = ""
    foods = []

    def __init__(self, menu_data):
        #TODO
        self.name = menu_data["name"]
        self.foods = []
        for category in menu_data["categories"]:
            foodlist = ""
            for item in category["menuItems"]:
                foodlist += item["name"] + "\n"

            self.foods.append([category["category"], foodlist])
    
    def __str__(self):
        return self.name + " " + self.foods