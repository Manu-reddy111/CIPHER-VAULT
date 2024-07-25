from tkinter import *
from tkinter import messagebox as ms
import tkinter as tk
import sqlite3 
import os
import subprocess
import numpy
from tkinter import ttk

# Create main window
root = tk.Tk()
root.title("CIPHER VAULT-Login Page")
root.geometry("600x400")
root.resizable(width=False, height=False)

# Set background image
background_image = tk.PhotoImage(file="pic1.png")  # Replace with your image file
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

root.iconbitmap('img/loginlogo.ico')
# Create frame for login interface on the right side
login_frame = ttk.Frame(root, padding=(20, 10))
login_frame.place(relx=0.6, rely=0.15 ,anchor='nw')

# Labels and buttons inside the login frame
login_label = ttk.Label(login_frame, text="Upload Files", font=("Arial", 20, "bold"))
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
        conn = sqlite3.connect('Cloud.db')

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
            
        # if user do not exist
        else:
            ms.showerror('Oops','User Not Found !! Check Username and Password Again !!')




login_button = ttk.Button(login_frame, text="Upload" ,command=Search)
login_button.pack(pady=20)


# Run the application
root.mainloop()
