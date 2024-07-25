from tkinter import *
import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
import subprocess
import numpy

def Register():
    Reg = tk.Tk()
    Reg.title("CIPHER VAULT-User Register")
    Reg.geometry('1036x568')
    Reg.resizable(width=False, height=False)
    Reg.iconbitmap('img/reglogo.ico')

    # Background Image
    bg_image = tk.PhotoImage(file='pic2.png')
    background_label = tk.Label(Reg, image=bg_image)
    background_label.place(relwidth=1, relheight=1)

    
    # Top Frame
    frame = tk.LabelFrame(Reg, padx=20,pady=10)
    frame.place(relx=0.635, rely=0 ,anchor='nw')

    top_frame = tk.Label(frame, text="USER REGISTRATION", font=('Cosmic', 23, 'bold'))
    top_frame.pack(pady=20)

    # Database Function
    def database(arg=None):
        name = name_entry.get()
        email = email_entry.get()
        mobile = mobile_entry.get()
        try:
            mobile = int(mobile)
        except ValueError:
            messagebox.showerror('Oops', 'Please Enter a Valid Phone Number !!!')
            return

        username = username_entry.get()
        password = password_entry.get()
        confirm = confirm_entry.get()

        if any(not entry for entry in (name, email, mobile, username, password, confirm)):
            messagebox.showerror('Oops', 'Please Fill All The Input Fields')
            return

        if password != confirm:
            messagebox.showerror('Oops', 'Password Does Not Match!!!')
            return

        conn = sqlite3.connect('Database.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY,FullName TEXT NOT NULL, Email TEXT NOT NULL, Mobile TEXT NOT NULL, Username TEXT NOT NULL, Password TEXT NOT NULL)')
            cursor.execute('INSERT INTO Users (FullName, Email, Mobile, Username, Password) VALUES (?,?,?,?,?)', (name, email, mobile, username, password))
            conn.commit()
            messagebox.showinfo('Successful', 'Account Created Successfully!! Now You Can Login To System!!')
            Reg.destroy()
            subprocess.call("python login.py ")
    # Main Frame for Input Fields
 

    # Labels and Entry Fields
    labels_font = ('Arial', 12, 'bold')
    entries_font = ('Arial', 10, 'normal')

    name_label = tk.Label(frame, text='Full Name', font=labels_font,  fg='black')
    name_label.pack( pady=5)
    name_entry = tk.Entry(frame, font=entries_font, bg='white')
    name_entry.pack( pady=5)

    email_label = tk.Label(frame, text='Email', font=labels_font,  fg='black')
    email_label.pack( pady=5)
    email_entry = tk.Entry(frame, font=entries_font, bg='white')
    email_entry.pack(pady=5)

    mobile_label = tk.Label(frame, text='Mobile No.', font=labels_font,  fg='black')
    mobile_label.pack( pady=5)
    mobile_entry = tk.Entry(frame, font=entries_font, bg='white')
    mobile_entry.pack(pady=5)

    username_label = tk.Label(frame, text='Username', font=labels_font,  fg='black')
    username_label.pack( pady=5)
    username_entry = tk.Entry(frame, font=entries_font, bg='white')
    username_entry.pack(pady=5)

    password_label = tk.Label(frame, text='Password', font=labels_font,  fg='black')
    password_label.pack(pady=5)
    password_entry = tk.Entry(frame, font=entries_font, show='*', bg='white')
    password_entry.pack( pady=5)

    confirm_label = tk.Label(frame, text='Confirm Password', font=labels_font, fg='black')
    confirm_label.pack( pady=5)
    confirm_entry = tk.Entry(frame, font=entries_font, show='*', bg='white')
    confirm_entry.pack( pady=5)

    
    submit_button = tk.Button(frame, text='Register', command=database, width=10, bd='3', font=('Times', 12, 'bold'), bg='white', fg='black', relief='groove', justify='center', pady='5')
    submit_button.pack(pady=20)

    # Quit Button
    #quit_button = tk.Button(Reg, text="Quit", width=10, command=Reg.destroy, bd='3', font=('Times', 12, 'bold'), bg='black', fg='white', relief='groove', justify='center', pady='5')
    #quit_button.place(anchor='sw', rely=0.85, relx=0.84)

    # Database Function
    def database(arg=None):
        name = name_entry.get()
        email = email_entry.get()
        mobile = mobile_entry.get()
        try:
            mobile = int(mobile)
        except ValueError:
            messagebox.showerror('Oops', 'Please Enter a Valid Phone Number !!!')
            return

        username = username_entry.get()
        password = password_entry.get()
        confirm = confirm_entry.get()

        if any(not entry for entry in (name, email, mobile, username, password, confirm)):
            messagebox.showerror('Oops', 'Please Fill All The Input Fields')
            return

        if password != confirm:
            messagebox.showerror('Oops', 'Password Does Not Match!!!')
            return

        conn = sqlite3.connect('Database.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS Users (FullName TEXT NOT NULL, Email TEXT NOT NULL, Mobile TEXT NOT NULL, Username TEXT NOT NULL, Password TEXT NOT NULL)')
            cursor.execute('INSERT INTO Users (FullName, Email, Mobile, Username, Password) VALUES (?,?,?,?,?)', (name, email, mobile, username, password))
            conn.commit()
            messagebox.showinfo('Successful', 'Account Created Successfully!! Now You Can Login To System!!')
            Reg.destroy()

    Reg.mainloop()

Register()
