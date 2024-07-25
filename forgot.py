import sqlite3
from tkinter import Tk, Label, Entry, Button, messagebox

# Create the database and user table (run this once to create the table)
def create_db():
    conn = sqlite3.connect('Database.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        email TEXT NOT NULL,
        mobile TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Function to handle forgot password
def forgot_password():
    username = entry_username.get()
    email = entry_email.get()
    mobile = entry_mobile.get()

    conn = sqlite3.connect('Database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username=? AND email=? AND mobile=?', (username, email, mobile))
    result = cursor.fetchone()
    conn.close()

    if result:
        password = result[0]
        messagebox.showinfo("Your Password", f"Your password is: {password}")
    else:
        messagebox.showerror("Error", "No matching user found.")
    app.destroy()
    subprocess.call("python login.py ")

# Create the main application window
app = Tk()
app.title("Forgot Password")
app.geometry('400x300')
app.configure(background='#3B2C35')
app.resizable(width=False, height=False)

Label(app, text="Username:").grid(row=0, column=0, padx=10, pady=10)
entry_username = Entry(app)
entry_username.grid(row=0, column=1, padx=10, pady=10)

Label(app, text="Email:").grid(row=1, column=0, padx=10, pady=10)
entry_email = Entry(app)
entry_email.grid(row=1, column=1, padx=10, pady=10)

Label(app, text="Mobile:").grid(row=2, column=0, padx=10, pady=10)
entry_mobile = Entry(app)
entry_mobile.grid(row=2, column=1, padx=10, pady=10)

Button(app, text="Submit", command=forgot_password).grid(row=3, column=0, columnspan=2, pady=20)

create_db()  # Create the database and table
app.mainloop()
