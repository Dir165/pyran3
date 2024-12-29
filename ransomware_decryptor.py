import os
import cryptography
import cryptography.fernet
import json
import pathlib
import re

def decrypt(key, data):
    f = cryptography.fernet.Fernet(key)
    original_data = f.decrypt(data)
    return original_data

def main():
    # Set the decryption key
    key = "mrdirweb33lizscriptkiddle"

    # Start the GUI
    window = tk.Tk()
    # Set the window title
    window.title("Ransomware Decryptor!")

    # Set the window size
    window.geometry("400x150")

    # Define the font
    font = tkFont.Font(
        family="Calibri", size=14, weight="bold"
    )

    # Create a label
    label = tk.Label(
        window,
        text="Ransomware Decryptor in Action!",
        bg="#43F443",
        fg="white",
        font=font,
    )

    # Create a load button
    loadBtn = tk.Button(
        window,
        text="Load Key and Decrypt",
        command=lambda: decrypt_files(key),
        width=50,
        font=font,
    )

    # Place the widgets
    label.place(x=10, y=60)
    loadBtn.place(x=220, y=100)

    # Start the tkinter event loop
    window.mainloop()

def decrypt_files(key):
    print("Attempting decryption...")

    if not os.path.exists(r"C:\encrypted"):
        raise Exception("Missing encrypted directory.")

    encrypted_files_dir = pathlib.Path(r"C:\encrypted")
    decrypted_files_dir = pathlib.Path(r"C:\decrypted")

    os.makedirs(decrypted_files_dir, exist_ok=True)

    decrypted_files = []

    for file_path in encrypted_files_dir.glob("**/*"):
        if ".enc" not in file_path.suffix:
            continue

        base_name, ext = file_path.stem.rsplit(".", 1)

        original_file_path = decrypted_files_dir / Path(base_name)

        decrypted_file_path = original_file_path
        decrypted_file_path.suffix = ""

        if os.path.isfile(original_file_path):
            continue

        data = open(file_path, "rb").read()
        original_data = decrypt(key, data)

        open(decrypted_file_path, "wb").write(original_data)
        decrypted_files.append((file_path, decrypted_file_path))

    print("Decryption complete.")
    print("Decrypted files:")
    for file_path, decrypted_file_path in decrypted_files:
        print(f"{file_path} -> {decrypted_file_path}")

if __name__ == "__main__":
    main()