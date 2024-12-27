import tkinter as tk
from tkinter import ttk
import os
import requests

def apiWindow(callback):
    keyWindow = tk.Tk()
    keyWindow.title("Set API Key")
    keyWindow.geometry("300x300")

    def close_window():
        keyWindow.destroy()
        return
    
    def submit():
        KEY = str(key_entry.get())
        with open('key.txt', 'w') as f:
            f.write(KEY)
        close_window()

    def start_drag(event): 
        keyWindow.x = event.x 
        keyWindow.y = event.y 

    def do_drag(event): 
        deltax = event.x - keyWindow.x 
        deltay = event.y - keyWindow.y 
        keyWindow.geometry(f"+{keyWindow.winfo_x() + deltax}+{keyWindow.winfo_y() + deltay}")

    # Make the window transparent
    keyWindow.attributes('-alpha', 0.8)

    # Remove all window decorations (including title bar)
    keyWindow.overrideredirect(True)

    # Always on top
    keyWindow.attributes('-topmost', True)

    # Add a frame to act as the window's header
    header_frame = tk.Frame(keyWindow, bg='black', relief='raised', bd=0)
    header_frame.pack(fill=tk.X)

    # Add buttons to the header frame
    close_button = tk.Button(header_frame, text='X', bg="black", fg="white", highlightthickness=0, bd=0, command=close_window)
    close_button.pack(side=tk.RIGHT)

    # Bind the header frame to the drag functions 
    keyWindow.bind("<Button-1>", start_drag) 
    keyWindow.bind("<B1-Motion>", do_drag)

    # Create the main content of the window
    content_frame = tk.Frame(keyWindow, bg='black')
    content_frame.pack(fill=tk.BOTH, expand=True)

    title_label = tk.Label(content_frame, text="Invalid Hypixel API Key.", fg='white', bg="black", font=("Helvetica", 12, 'bold')) 
    title_label.pack(side='top', fill='x', padx=10, pady=10)

    key_entry = tk.Entry(content_frame, width=40)
    key_entry.pack(pady=10)

    submit_button = tk.Button(content_frame, text="Submit", command=submit)
    submit_button.pack(pady=10)

    keyWindow.mainloop()
    return

def getInfo(call):
  r = requests.get(call)
  if r.status_code == 204:
    return {'name': 'Null'}
  return r.json()