import tkinter as tk
from tkinter import ttk
import os
import requests

def getInfo(call):
  call = call.rstrip("\n")
  call = call.rstrip("')")
  r = requests.get(call)
  if r.status_code == 204:
    return {'name': 'Null'}
  return r.json()

def set_key():
    global KEY
    try:
        with open('key.txt', 'r') as f:
            KEY = f.readline()

            key_check_url = f'https://api.hypixel.net/counts?key={KEY}'
            key_check = getInfo(key_check_url)
        f.close()

        if key_check['success'] == False:
            print("Invalid API key. https://developer.hypixel.net/dashboard")
            with open('key.txt', 'w') as f:
                f.write(input("Paste your API key: "))
            f.close()
            set_key()
    except Exception as e:
        print(f"ERROR: {e}")
        print("Invalid API key. https://developer.hypixel.net/dashboard")
        with open('key.txt', 'w') as f:
            f.write(input("Paste your API key: "))
        f.close()
        set_key()

    f.close()

    return(KEY)