import tkinter as tk
from tkinter import ttk
import os

#TODO: 
    # paste api key in gui rather than terminal


def close_window():
    root.destroy()

def start_drag(event): 
    root.x = event.x 
    root.y = event.y 

def do_drag(event): 
    deltax = event.x - root.x 
    deltay = event.y - root.y 
    root.geometry(f"+{root.winfo_x() + deltax}+{root.winfo_y() + deltay}")
                  
root = tk.Tk()
root.title("HyOverlay")
root.geometry("330x630")

# Make the window transparent
root.attributes('-alpha', 0.8)

# Remove all window decorations (including title bar)
root.overrideredirect(True)

# Always on top
root.attributes('-topmost', True)

# Add a frame to act as the window's header
header_frame = tk.Frame(root, bg='black', relief='raised', bd=0)
header_frame.pack(fill=tk.X)

# Add buttons to the header frame
close_button = tk.Button(header_frame, text='X', bg="black", fg="white", highlightthickness=0, bd=0, command=close_window)
close_button.pack(side=tk.RIGHT)

# Bind the header frame to the drag functions 
root.bind("<Button-1>", start_drag) 
root.bind("<B1-Motion>", do_drag)

# Create the main content of the window
content_frame = tk.Frame(root, bg='black')
content_frame.pack(fill=tk.BOTH, expand=True)

#Add column labels 
labels = ["Name", "FKDR"] 
label1 = tk.Label(content_frame, text="Name", fg='white', bg="black", font=("Helvetica", 12, 'bold')) 
label1.grid(row=0, column=0, padx=20, pady=10, sticky="w") 
label2 = tk.Label(content_frame, text="FKDR", fg='white', bg="black", font=("Helvetica", 12, 'bold')) 
label2.grid(row=0, column=1, padx=20, pady=10, sticky="e") 

# Configure the grid to evenly space the columns 
content_frame.grid_columnconfigure(0, weight=1) 
content_frame.grid_columnconfigure(1, weight=1) 

import requests
import threading

row = 1
labels = []

def getInfo(call):
  call = call.rstrip("\n")
  call = call.rstrip("')")
  r = requests.get(call)
  if r.status_code == 204:
    return {'name': 'Null'}
  return r.json()

# set api key
def set_key():
    try:
        with open('key.txt', 'r') as f:
            KEY = f.readline()

            key_check_url = f'https://api.hypixel.net/counts?key={KEY}'
            key_check = getInfo(key_check_url)
        f.close()

        with open('key.txt', 'w') as f:
            if key_check['success'] == False:
                print("Invalid API key.")
                with open('key.txt', 'w') as f:
                    f.write(input("Paste your API key: "))
    except Exception as e:
        print(f"ERROR: {e}")
        print("Invalid API key.")
        f.write(input("Paste your API key: "))

    f.close()

    print("Welcome to HYOVERLAY!")
    print("Use '/bw' to check individual stats")
    print("Example: /bw Dewier WarOG")

set_key()


def create_labels(name, star_color, fkdr):
    global row

    name_label = tk.Label(content_frame, text=name, fg=star_color, bg="black", font=("Helvetica", 12, 'bold')) 
    name_label.grid(row=row, column=0, padx=20, pady=5, sticky='w') 

    fkdr_label = tk.Label(content_frame, text=fkdr, fg='white', bg="black", font=("Helvetica", 12, 'bold')) 
    fkdr_label.grid(row=row, column=1, padx=20, pady=5, sticky='e')

    labels.append(name_label)
    labels.append(fkdr_label)

    row += 1

def delete_labels():
    for label in labels:
        label.destroy()

def getStats(user):
    global row
    mojangurl = "https://api.mojang.com/users/profiles/minecraft/" + user
    mojanginfo = getInfo(mojangurl)
    try:
        uuid = mojanginfo["id"]
        hypixelurl = f"https://api.hypixel.net/player?key={KEY}&uuid=" + uuid
        hypixelinfo = getInfo(hypixelurl)
        try:
            ign = hypixelinfo['player']['displayname']
        except:
            ign = "NICK"
        try:
            star = hypixelinfo['player']['achievements']['bedwars_level']
        except:
            star = 0
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
        except:
            bwfkdr = bwfinalkills

    except:
        print("User not found")
        ign = "NICK"
        star = 0
        bwfkdr = 0

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

    create_labels(name, star_color, bwfkdr)

home_directory = os.path.expanduser("~")
name = os.path.basename(home_directory) 

client = '.lunarclient'

logs = f"C:/Users/{name}/{client}/offline/multiver/logs/latest.log"

def log_monitor():
    global row

    with open(logs, 'r') as file:
        file.seek(0, 2)
        while True:
            line = file.readline()
            if "ONLINE:" in line:
                players = line.split("ONLINE: ")[1]
                players_arr = players.split(", ")
                row = 1
                delete_labels()
                for x in players_arr:
                    getStats(x)
            elif "('bw" in line:
                players = line.split("('bw ")[1]
                players_arr = players.split(" ")
                row = 1
                delete_labels()
                for x in players_arr:
                    getStats(x)


def start_threading():
    thread = threading.Thread(target=log_monitor) 
    thread.daemon = True # This makes sure the thread will exit when the main program exits
    thread.start()

start_threading()

root.mainloop()