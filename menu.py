import os, discord, urllib.request, urllib.error, urllib.parse, json
from dotenv import load_dotenv

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

udcc_cc_b, udcc_cc_l, udcc_cc_d, udcc_p_b, udcc_p_l, udcc_p_d, udcc_d_b, udcc_d_l, udcc_d_d, udcc_pa_b, udcc_pa_l, udcc_pa_d = [],[],[],[],[],[],[],[],[],[],[],[]
windows_s_l, windows_s_d, windows_z_l, windows_z_d, windows_sl_l, windows_sl_d, windows_sv_l, windows_sv_d = [],[],[],[],[],[],[],[]

request=urllib.request.Request(url_windows,None,headers)
with urllib.request.urlopen(request) as url:
    data = json.loads(url.read().decode())

for time in data[0]["menus"]:
    for bar in time["menuDisplays"]:
        for food in bar['categories'][0]['menuItems']:
            if bar['name'] == "Simmer":
                if time['section'] == "Lunch":
                    windows_s_l.append(food['name'])
                if time['section'] == "Dinner":
                    windows_s_d.append(food['name'])
            if bar['name'] == "Zest":
                if time['section'] == "Lunch":
                    windows_z_l.append(food['name'])
                if time['section'] == "Dinner":
                    windows_z_d.append(food['name'])
            if bar['name'] == "Slice":
                if time['section'] == "Lunch":
                    windows_sl_l.append(food['name'])
                if time['section'] == "Dinner":
                    windows_sl_d.append(food['name'])
            if bar['name'] == "Savor":
                if time['section'] == "Lunch":
                    windows_sv_l.append(food['name'])
                if time['section'] == "Dinner":
                    windows_sv_d.append(food['name'])

request=urllib.request.Request(url_udcc,None,headers)
with urllib.request.urlopen(request) as url:
    data = json.loads(url.read().decode())

for time in data[0]["menus"]:
    for bar in time["menuDisplays"]:
        for food in bar['categories'][0]['menuItems']:
            if bar['name'] == "Cardinal Canteen":
                if time['section'] == "Breakfast":
                    udcc_cc_b.append(food['name'])
                if time['section'] == "Lunch":
                    udcc_cc_l.append(food['name'])
                if time['section'] == "Dinner":
                    udcc_cc_d.append(food['name'])
            if bar['name'] == "Picoso":
                if time['section'] == "Breakfast":
                    udcc_p_b.append(food['name'])
                if time['section'] == "Lunch":
                    udcc_p_l.append(food['name'])
                if time['section'] == "Dinner":
                    udcc_p_d.append(food['name'])
            if bar['name'] == "Dagwood's":
                if time['section'] == "Breakfast":
                    udcc_d_b.append(food['name'])
                if time['section'] == "Lunch":
                    udcc_d_l.append(food['name'])
                if time['section'] == "Dinner":
                    udcc_d_d.append(food['name'])
            if bar['name'] == "Parma's":
                if time['section'] == "Breakfast":
                    udcc_pa_b.append(food['name'])
                if time['section'] == "Lunch":
                    udcc_pa_l.append(food['name'])
                if time['section'] == "Dinner":
                    udcc_pa_d.append(food['name'])