import requests
import time

def getInfo(call):
  r = requests.get(call)
  return r.json()

def getStats(user, statsArr, KEY):
    mojangurl = "https://api.mojang.com/users/profiles/minecraft/" + user.rstrip("\n")
    time.sleep(0.5)
    mojanginfo = getInfo(mojangurl)
    try:
        uuid = mojanginfo["id"]
        hypixelurl = f"https://api.hypixel.net/player?key={KEY}&uuid=" + uuid
        hypixelinfo = getInfo(hypixelurl)
        
        unknown = False
        try:
            ign = hypixelinfo['player']['displayname']
        except:
            ign = user.replace("')", "")
        try:
            star = hypixelinfo['player']['achievements']['bedwars_level']
        except:
            star = 0
        try:
            wins = hypixelinfo['player']['stats']['Bedwars']['wins_bedwars']
        except:
            wins = 0
        try:   
            losses = hypixelinfo['player']['stats']['Bedwars']['losses_bedwars']
        except:
            losses = 0
        try:
            wlr = round(wins / losses, 2)
        except ZeroDivisionError:
            wlr = wins
        try:
            winstreak = hypixelinfo['player']['stats']['Bedwars']['winstreak']
        except:
            winstreak = "?"
        try:
            bwfinalkills = hypixelinfo['player']['stats']['Bedwars']['final_kills_bedwars']
        except:
            bwfinalkills = 0
        try:
            bwfinaldeaths = hypixelinfo['player']['stats']['Bedwars']['final_deaths_bedwars']
        except:
            bwfinaldeaths = 0
        try:
            bwfkdr = round(bwfinalkills / bwfinaldeaths, 2)
        except ZeroDivisionError:
            bwfkdr = bwfinalkills

    except Exception as e:
        try:
            if mojanginfo['error'] == "CONSTRAINT_VIOLATION":
                print(mojanginfo['error'], "retrying...")
                print(mojanginfo)
                time.sleep(10)
                getStats(user.replace("\n", ""), statsArr, KEY)
        except KeyError:
            try:
                if mojanginfo['errorMessage'] == f"Couldn't find any profile with name {user}":
                    ign = user.replace("')", "")
                    star = 0
                    wlr = 0
                    winstreak = 0
                    bwfkdr = 0
                    unknown = True
                    print(f"[ERROR] {ign}\t {e}")
                    print(mojanginfo)
            except:
                print(mojanginfo + " retrying...")
                time.sleep(10)
                getStats(user.replace("\n", ""), statsArr, KEY)                

    name = f"[{star}✫] {ign}"

    if star <= 99:
        star_color = "#AAAAAA"
    elif star >= 100 and star <= 199:
        star_color = "#FFFFFF"
    elif star >= 200 and star <= 299:
        star_color = "#FFAA00"
    elif star >= 300 and star <= 399:
        star_color = "#55FFFF"
    elif star >= 400 and star <= 499:
        star_color = "#00AA00"
    elif star >= 500 and star <= 599:
        star_color = "#00AAAA"
    elif star >= 600 and star <= 699:
        star_color = "#AA0000"
    elif star >= 700 and star <= 799:
        star_color = "#FF55FF"
    elif star >= 800 and star <= 899:
        star_color = "#5555FF"
    elif star >= 900 and star <= 999:
        star_color = "#AA00AA"
    elif star >= 1000:
        star_color = "#FFFF55"

    statsArr.append(
        {
            "name": name,
            "star_color": star_color,
            "ws": winstreak,
            "fkdr": bwfkdr,
            "wlr": wlr,
            "unknown": unknown
        }
    )