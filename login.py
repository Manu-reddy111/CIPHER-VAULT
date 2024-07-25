from tkinter import *
from tkinter import messagebox as ms
import tkinter as tk
import sqlite3 
import os
import subprocess
import numpy
from tkinter import ttk
from alg import UserHome

# Create main window
root = tk.Tk()
root.title("CIPHER VAULT-Login Page")
root.geometry("750x400")
root.resizable(width=False, height=False)

# Set background image
background_image = tk.PhotoImage(file="pic1.png")  # Replace with your image file
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

root.iconbitmap('img/loginlogo.ico')
# Create frame for login interface on the right side
login_frame = ttk.Frame(root, padding=(20, 10))
login_frame.place(relx=0.58, rely=0.05 ,anchor='nw')

# Labels and buttons inside the login frame
login_label = ttk.Label(login_frame, text="USER LOGIN", font=("Times New Roman", 20, "bold"))
login_label.pack(pady=20)

def Search():
    if username_entry.get() == '': 
        ms.showerror('Oops', 'Enter Username !!')
        
    elif password_entry.get() == '':
        ms.showerror('Oops', 'Enter Password !!')
        
    else:
        global username
        username = username_entry.get()
        global password
        password = password_entry.get()

        # Making connection
        conn = sqlite3.connect('Database.db')

        # Creating cursor
        with conn:
            cursor = conn.cursor()

        # Searching for users
        find_user = ('SELECT * FROM users WHERE Username = ? AND Password = ?')
        cursor.execute(find_user,(username, password))
        results = cursor.fetchall()

        # if user then new window
        if results:
            root.destroy()
            print("welcome")
            UserHome(username).mainloop()
            
        # if user do not exist
        else:
            ms.showerror('Oops','User Not Found !! Check Username and Password Again !!')



username_label = ttk.Label(login_frame, text="Username:",font=("Times New Roman", 12, "bold"))
username_label.pack(pady=5)

username_entry = ttk.Entry(login_frame, width=30)
username_entry.pack(pady=5)

password_label = ttk.Label(login_frame, text="Password:",font=("Times New Roman", 12, "bold"))
password_label.pack(pady=5)

password_entry = ttk.Entry(login_frame, show="*", width=30)
password_entry.pack(pady=5)

login_button = ttk.Button(login_frame, text="Login" ,command=Search,width=18)
login_button.pack(pady=20)

def onclick(event):
    root.destroy()
    subprocess.call("python register.py ")

def onsubmit(event):
    root.destroy()
    subprocess.call("python forgot.py ")

fp=ttk.Label(login_frame, text="Forgot Password" ,font=("Times New Roman", 12), cursor="hand2")
fp.bind("<Button-1>",onsubmit)
fp.pack(pady=5)

register=ttk.Label(login_frame, text="Not A Member?? REGISTER!!" ,font=("Times New Roman", 14, "bold"), cursor="hand2")
register.bind("<Button-1>",onclick)
register.pack(pady=5)
# Run the application
root.mainloop()
