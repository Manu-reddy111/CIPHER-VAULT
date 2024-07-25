from tkinter import *
from tkinter import ttk, filedialog, messagebox
import sqlite3
import os
from Crypto.Cipher import AES
import hashlib
import subprocess
from Crypto.Random import get_random_bytes
from view_users import ViewHome
# Create or connect to the SQLite database
conn = sqlite3.connect('Clouds.db')
cursor = conn.cursor()

# Create tables if they do not exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    filename TEXT,
    filekey TEXT,
    encrypted BLOB,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS sharefiles (
    id INTEGER PRIMARY KEY,
    owner INTEGER,
    filename TEXT,
    filekey TEXT,
    encrypted BLOB,
    shared_with INTEGER,
    FOREIGN KEY(owner) REFERENCES users(id),
    FOREIGN KEY(shared_with) REFERENCES users(id)
)
''')

conn.commit()

from tkinter import Toplevel, ttk, filedialog, messagebox, Label, PhotoImage

def show_file_tree_window(user_id):
    file_tree_window = Toplevel()
    file_tree_window.title("FILE TREE")
    file_tree_window.geometry("900x600")
    file_tree_window.resizable(width=False, height=False)
    file_tree_window.iconbitmap('img/logo.ico')

    # Load and place the background image
    background_image = PhotoImage(file="pic6.png")
    background_label = Label(file_tree_window, image=background_image)
    background_label.image = background_image  # Keep a reference to avoid garbage collection
    background_label.place(relwidth=1, relheight=1)

    file_tree = ttk.Treeview(file_tree_window, columns=("ID", "Filename", "Filekey"), show="headings")
    file_tree.heading("ID", text="ID")
    file_tree.heading("Filename", text="Filename")
    file_tree.heading("Filekey", text="Filekey")
    file_tree.pack(padx=20, pady=20)

    received_file_tree = ttk.Treeview(file_tree_window, columns=("ID", "Owner", "Received Filename", "Filekey"), show="headings")
    received_file_tree.heading("ID", text="ID")
    received_file_tree.heading("Owner", text="Owner")
    received_file_tree.heading("Received Filename", text="Received Filename")
    received_file_tree.heading("Filekey", text="Filekey")
    received_file_tree.pack(padx=20, pady=20)

    conn = sqlite3.connect('Clouds.db')
    c = conn.cursor()
    c.execute('SELECT id, filename, filekey FROM files WHERE user_id = ?', (user_id,))
    files = c.fetchall()
    for file in files:
        file_tree.insert("", "end", values=(file[0], file[1], file[2]))
    conn.close()

    connn = sqlite3.connect('Database.db')
    cn = connn.cursor()
    cn.execute('SELECT id FROM users WHERE FullName = ?', (user_id,))
    recipient = cn.fetchone()
    if recipient:
        con = sqlite3.connect('Clouds.db')
        cc = con.cursor()
        cc.execute('SELECT id, owner, filename, filekey FROM sharefiles WHERE shared_with = ?', (recipient[0],))
        shared_files = cc.fetchall()
        for file in shared_files:
            received_file_tree.insert("", "end", values=(file[0], file[1], file[2], file[3]))
        con.close()

    selected_file = {"table": None, "values": None}

    def on_file_tree_select(event):
        selected_item = file_tree.selection()
        if selected_item:
            selected_file["table"] = "file_tree"
            selected_file["values"] = file_tree.item(selected_item)["values"]

    def on_received_file_tree_select(event):
        selected_item = received_file_tree.selection()
        if selected_item:
            selected_file["table"] = "received_file_tree"
            selected_file["values"] = received_file_tree.item(selected_item)["values"]

    file_tree.bind("<<TreeviewSelect>>", on_file_tree_select)
    received_file_tree.bind("<<TreeviewSelect>>", on_received_file_tree_select)

    def destroy_file_tree_window():
        file_tree_window.destroy()

    return file_tree_window, destroy_file_tree_window, selected_file



def UserHome(user_id):
    system = Tk()
    system.title("CIPHER VAULT")
    system.geometry("800x600")
    system.resizable(width=False, height=False)
    
    skey = StringVar()
    dd = StringVar()

    # Load the background image
    # Note: Replace "pic4.png" with your actual image file path
    background_image = PhotoImage(file="pic4.png")
    background_label = Label(system, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    system.iconbitmap('img/logo.ico')

    def encrypt_and_upload(file_path, key):
        if file_path:
            with open(file_path, 'rb') as f:
                file_data = f.read()
        encrypted_data = encrypt_file(file_data, key)
        if encrypted_data:
            conn = sqlite3.connect('Clouds.db')
            c = conn.cursor()
            filename = os.path.basename(file_path)
            c.execute('INSERT INTO files (user_id, filename, filekey, encrypted) VALUES (?, ?, ?, ?)',
                      (user_id, filename, key, encrypted_data))
            c.execute('INSERT INTO sharefiles (owner, filename, filekey, encrypted) VALUES (?, ?, ?, ?)',
                      (user_id, filename, key, encrypted_data))
            conn.commit()
            conn.close()
            messagebox.showinfo("Upload", "File uploaded and encrypted successfully!")

    def encrypt(data, key):
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
        return base64.b64encode(nonce + tag + ciphertext).decode('utf-8')

    def decrypt(data, key):
        data = base64.b64decode(data)
        nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode('utf-8')

    def encrypt_file(file_data, key):
        key = hashlib.sha256(key.encode()).digest()
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(file_data)
        return nonce + ciphertext

    def decrypt_file(encrypted_data, key):
        key = hashlib.sha256(key.encode()).digest()
        nonce = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt(ciphertext)

    

    def showfiles():
        file_tree_window, destroy_file_tree_window, selected_file = show_file_tree_window(user_id)
        system.selected_file = selected_file  # Store the selected file in the system to make it accessible globally within UserHome

    def ShareFile():
        if hasattr(system, 'selected_file'):
            selected_file = system.selected_file  # Access the stored selected file from system
            if selected_file["values"]:
                file_id = selected_file["values"][0]
                file_key = selected_file["values"][2]
                recipient_username = dd.get()
                conn = sqlite3.connect('Database.db')
                c = conn.cursor()
                c.execute('SELECT id FROM users WHERE FullName = ?', (recipient_username,))
                recipient = c.fetchone()
                if recipient:
                    con = sqlite3.connect('Clouds.db')
                    cc = con.cursor()
                    cc.execute('UPDATE sharefiles SET shared_with = ? WHERE id = ?', (recipient[0], file_id))
                    con.commit()
                    messagebox.showinfo("Share", "File shared successfully!")
                    destroy_file_tree_window()  # Close the window
                else:
                    messagebox.showerror("Share Error", "Recipient username not found")
                conn.close()

    def DownloadFile():
        if hasattr(system, 'selected_file'):
            selected_file = system.selected_file  # Access the stored selected file from system
            if selected_file["values"]:
                file_id = selected_file["values"][0]
                file_key = selected_file["values"][2]
                conn = sqlite3.connect('Clouds.db')
                c = conn.cursor()
                c.execute('SELECT encrypted FROM files WHERE id = ?', (file_id,))
                encrypted_data = c.fetchone()[0]
                conn.close()

                file_path = filedialog.asksaveasfilename(filetypes=[("Text files", "*.txt")])
                if file_path:
                    decrypt_success = decrypt_file(encrypted_data,file_key)
                    if decrypt_success:
                        messagebox.showinfo("Download", "File downloaded and decrypted successfully!")
                        #destroy_file_tree_window()  # Close the window



    def upload_file():
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            
            key = skey.get()
            if len(key) == 8:
                encrypt_and_upload(file_path, key)
            else:
                messagebox.showerror("Key Error", "Key must be 8 characters long")

    def ViewUsers():
        ViewHome(user_id).mainloop()

    def Logout():
        system.destroy()
        subprocess.call("python login.py ")

    # Widgets on the main window
    user_label = Label(system, text="SERVICES", font=("Times New Roman", 24, "bold"))
    user_label.place(x=300,y=0)

    upload_label = Label(system, text="Upload File",font=('times', 13, 'bold'), bg="white").place(x=10, y=100)
    upload_label_t = Label(system, text="Enter 8-digit Key:",font=('times', 13, 'bold') ,bg="white").place(x=10, y=140)
    entry_key = Entry(system, textvariable=skey).place(x=10, y=180)
    upload_button = Button(system, text="Upload File", font=('times', 16, 'bold'),command=upload_file,width=18)
    upload_button.place(x=10, y=220)

    username_label = Label(system, text="username:",font=('times', 13, 'bold') ,bg="white").place(x=500, y=130)
    username_display = Label(system, text=user_id, font=('times', 13, 'bold'), fg="Dark Blue", bg="white").place(x=600, y=130)

    recipient_label = Label(system, text="Enter recipient username:",font=('times', 13, 'bold'), bg="white").place(x=10, y=320)
    entry_recipient = Entry(system, textvariable=dd).place(x=10, y=360)

    file_tree_button = Button(system, text="Show Files", font=('times', 16, 'bold'),command=showfiles,width=18)
    file_tree_button.place(x=10, y=270)

    share_button = Button(system, text="Share File",font=('times', 16, 'bold'),bg='white' ,command=ShareFile,width=18)
    share_button.place(x=10, y=400)

    download_button = Button(system, text="Download File",font=('times', 16, 'bold'),bg='white' ,command=DownloadFile,width=18)
    download_button.place(x=10, y=450)

    view_users_button = Button(system, text="View Users", font=('times', 16, 'bold'),command=ViewUsers,width=18)
    view_users_button.place(x=10, y=500)

    logout_button = Button(system, text="Logout",font=('times', 16, 'bold'), command=Logout,width=18)
    logout_button.place(x=10, y=550)

    system.mainloop()


# Run the application
#UserHome(1)  # Replace with the actual user ID or parameter as needed
