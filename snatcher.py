import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient
from cryptography.fernet import Fernet


# Generate a key for encryption/decryption
# Guarantees that a message encrypted using it cannot be manipulated or read without the key
key = Fernet.generate_key()

# Initializes a Fernet object with the generated encryption key
# Ciper object is what will be used to encrypt
cipher = Fernet(key)

# MongoDB setup
# Port 27017 is the default port used by MongoDB to listen for client connections
client = MongoClient("mongodb://localhost:27017/")


db = client["credit_card_db"]
collection = db["credit_cards"]

# Function to add a credit card to the database
def add_credit_card(card_number):
    encrypted_card = cipher.encrypt(card_number.encode())
    collection.insert_one({"encrypted_card": encrypted_card})
    messagebox.showinfo("Success", "Credit card number added!")


# Function to search for a credit card in the database
def search_credit_card():
    search_number = search_entry.get()
    encrypted_search = cipher.encrypt(search_number.encode())
    result = collection.find_one({"encrypted_card": encrypted_search})

    if result:
        messagebox.showinfo("Result", "Credit card number found in the database.")
    else:
        messagebox.showinfo("Result", "Credit card number not found.")





# GUI setup
app = tk.Tk()
app.title("Credit Card Manager")
app.geometry("800x400")

# Frame for centering
center_frame = tk.Frame(app)
center_frame.pack(expand = True, fill='both')

# Input field for adding credit card numbers
add_label = tk.Label(center_frame, text="Enter Credit Card Number:")
add_label.pack()
add_entry = tk.Entry(center_frame, show="*")
add_entry.pack()

add_button = tk.Button(center_frame, text="Add Credit Card", command=lambda: add_credit_card(add_entry.get()))
add_button.pack()

# Search functionality
search_label = tk.Label(center_frame, text="Search Credit Card Number:")
search_label.pack()
search_entry = tk.Entry(center_frame)
search_entry.pack()

search_button = tk.Button(center_frame, text="Search", command=search_credit_card)
search_button.pack()

# GUI loop
app.mainloop()