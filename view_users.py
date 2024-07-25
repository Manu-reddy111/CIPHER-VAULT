from tkinter import *
from tkinter import messagebox as ms
import tkinter as tk
import sqlite3
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import messagebox, filedialog
from Crypto.Cipher import AES
import sqlite3
import base64
import os
import tkinter
import hashlib
import os
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
import hashlib
import os
import re

conn = sqlite3.connect('Clouds.db')
c = conn.cursor()
conn.close()

def ViewHome(user_id):
    # system = tk.Tk() 
    system = tkinter.Tk()
    system.geometry('500x500')
    system.configure(background='#3B2C35')
    system.resizable(width=False, height=False)
    system.title('CIPHER VAULT ')
    usern=tk.StringVar()
     

    system.iconbitmap('img/loginlogo.ico')
    def showusers():
        for row in file_tree.get_children():
            file_tree.delete(row)
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        c.execute('SELECT id, FullName FROM Users ')

        files = c.fetchall()
        for file in files:
            file_tree.insert("", "end", values=(file[0], file[1]))
        conn.close()


    # Show files table
    file_tree = ttk.Treeview(system, columns=("ID", "FullName"), show="headings")
    file_tree.heading("ID", text="ID")
    file_tree.heading("FullName", text="User Name")
    file_tree.pack()
    showusers()
    

    

