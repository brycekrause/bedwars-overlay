import tkinter as tk
from tkinter import ttk
import os
from key import apiWindow
from getStats import getStats

# Get the path to the latest.log file
home_directory = os.path.expanduser("~")
name = os.path.basename(home_directory) 
client = '.lunarclient'
logs = f"C:/Users/{name}/{client}/offline/multiver/logs/latest.log"


danger_icon = "⚠︎"

def overlayWindow():
    global content_frame
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
    root.geometry("580x630")

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

    # Add column labels 
    name_label = tk.Label(content_frame, text="NAME", fg='white', bg="black", font=("Helvetica", 12, 'bold')) 
    name_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")   
    tag_label =  tk.Label(content_frame, text="TAG", fg='white', bg="black", font=("Helvetica", 12, 'bold')) 
    tag_label.grid(row=0, column=1, padx=20, pady=10, sticky="w")   
    ws_title_label =  tk.Label(content_frame, text="WS", fg='white', bg="black", font=("Helvetica", 12, 'bold')) 
    ws_title_label.grid(row=0, column=2, padx=20, pady=10, sticky="w")   
    fkdr_title_label = tk.Label(content_frame, text="FKDR", fg='white', bg="black", font=("Helvetica", 12, 'bold')) 
    fkdr_title_label.grid(row=0, column=3, padx=20, pady=10, sticky="e") 
    wlr_title_label = tk.Label(content_frame, text="WLR", fg='white', bg="black", font=("Helvetica", 12, 'bold')) 
    wlr_title_label.grid(row=0, column=4, padx=20, pady=10, sticky="e") 


    apiSuccess_label = tk.Label(content_frame, text="API key set successfully!", fg='lightgreen', bg="black", font=("Helvetica", 12, 'bold')) 
    apiSuccess_label.grid(row=1, column=0, padx=20, pady=10, sticky="e") 

    root.after(3000, apiSuccess_label.destroy)

    # Configure the grid to evenly space the columns 
    content_frame.grid_columnconfigure(0, weight=2) # Name
    content_frame.grid_columnconfigure(1, weight=1) # Tag
    content_frame.grid_columnconfigure(2, weight=1) # WS
    content_frame.grid_columnconfigure(3, weight=1) # FKDR
    content_frame.grid_columnconfigure(4, weight=1) # WLR

    root.mainloop()




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

def callback():
    set_key()

def set_key():
    global KEY
    try:
        with open('key.txt', 'r') as f:
            KEY = f.readline()

            key_check_url = f'https://api.hypixel.net/counts?key={KEY}'
            key_check = getInfo(key_check_url)
        f.close()

        if key_check['success'] == False:
            apiWindow(set_key)
    except Exception:
        apiWindow(set_key)

    overlayWindow()



def create_labels(name, star_color, ws, fkdr, wlr, unknown):
    global row

    name_label = tk.Label(content_frame, text=name, fg=star_color, bg="black", font=("Helvetica", 12, 'bold')) 
    name_label.grid(row=row, column=0, padx=20, pady=5, sticky='w') 
    fkdr_color = "white"
    ws_color = "white"
    wlr_color = "white"


    if fkdr < 2:
        fkdr_color = "#AAAAAA"
    elif fkdr >= 2 and fkdr < 4:
        fkdr_color = "white"
    elif fkdr >= 4 and fkdr <= 6:
        fkdr_color = "yellow"
    elif fkdr > 6 and fkdr <= 8:
        fkdr_color = "green"
    elif fkdr > 8:
        fkdr_color = "red"

    if wlr < 1:
        wlr_color = "#AAAAAA"
    elif wlr >= 1 and wlr < 2:
        wlr_color = "white"
    if wlr >= 2 and wlr <= 4:
        wlr_color = "yellow"
    elif wlr > 4 and wlr <= 6:
        wlr_color = "green"
    elif wlr > 6:
        wlr_color = "red"

    try:
        if ws == 0:
            ws_color = "#AAAAAA"
        elif ws >= 1 and ws < 10:
            ws_color = "white"
        if ws >= 10 and ws <= 25:
            ws_color = "yellow"
        elif ws > 25 and ws <= 50:
            ws_color = "green"
        elif ws > 50:
            ws_color = "red"
    except TypeError: # if player not found or WS API disabled
        ws_color = "white"

    if fkdr >= 8:
        danger_label = tk.Label(content_frame, text=f"{danger_icon}", fg='red', bg="black", font=("Helvetica", 12, 'bold'))
        danger_label.grid(row=row, column=1, padx=20, pady=5, sticky='w')
    else:
        if unknown:
            danger_label = tk.Label(content_frame, text="⍰", fg='yellow', bg="black", font=("Helvetica", 12, 'bold'))
            danger_label.grid(row=row, column=1, padx=20, pady=5, sticky='w')
        else:
            danger_label = tk.Label(content_frame, text="", fg='red', bg="black", font=("Helvetica", 12, 'bold'))
            danger_label.grid(row=row, column=1, padx=20, pady=5, sticky='w')

    ws_label = tk.Label(content_frame, text=ws, fg=ws_color, bg="black", font=("Helvetica", 12, 'bold')) 
    ws_label.grid(row=row, column=2, padx=20, pady=5)
    fkdr_label = tk.Label(content_frame, text=fkdr, fg=fkdr_color, bg="black", font=("Helvetica", 12, 'bold')) 
    fkdr_label.grid(row=row, column=3, padx=20, pady=5)
    wlr_label = tk.Label(content_frame, text=wlr, fg=wlr_color, bg="black", font=("Helvetica", 12, 'bold')) 
    wlr_label.grid(row=row, column=4, padx=20, pady=5)

    labels.append(name_label)
    labels.append(danger_label)
    labels.append(ws_label)
    labels.append(fkdr_label)
    labels.append(wlr_label)

    row += 1

def delete_labels():
    for label in labels:
        label.destroy()

def sortPlayers(statsArr):
    statsArr.sort(key=lambda x: x['fkdr'], reverse=True) # change this
    for player in statsArr:
        create_labels(player['name'], player['star_color'], player['ws'], player['fkdr'], player['wlr'], player['unknown'])

def command_detected(players_arr):
    global row, statsArr, start_time
    row = 1
    delete_labels()
    statsArr = []

    player_count = len(players_arr)
    wait_label = tk.Label(content_frame, text=f"Gathering data..." , fg='white', bg="black", font=("Helvetica", 12, 'bold')) 
    wait_label.grid(row=row, column=0, padx=20, pady=5, sticky='e')

    labels.append(wait_label)

    for player in players_arr:
        getStats(player, statsArr, KEY)

    delete_labels()
    row = 1
    sortPlayers(statsArr)


def log_monitor():
    global row, statsArr

    with open(logs, 'r') as file:
        file.seek(0, 2)
        while True:
            line = file.readline()
            if "ONLINE:" in line:
                players = line.split("ONLINE: ")[1]
                players_arr = players.split(", ")
                command_detected(players_arr)
            elif ("('bw " and "')") in line:
                try:
                    players = line.split("('bw ")[1].split("')")[0].split(" ")
                    command_detected(players)
                except IndexError as e:
                    pass

def start_threading():
    thread = threading.Thread(target=log_monitor) 
    thread.daemon = True # This makes sure the thread will exit when the main program exits
    thread.start()

start_threading()
set_key()
