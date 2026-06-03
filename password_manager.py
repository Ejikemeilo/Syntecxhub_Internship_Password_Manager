import json
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
SALT_FILE = "salt.key"
DATA_FILE = "passwords.enc"

def get_key(master_password):
    # Load or create a "salt" (random bytes that make the key unique)
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, "rb") as f:
            salt = f.read()
    else:
        salt = os.urandom(16)
        with open(SALT_FILE, "wb") as f:
            f.write(salt)

    # Derive a strong key from the master password
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return Fernet(key)
def load_passwords(fernet):
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "rb") as f:
        encrypted = f.read()
    try:
        decrypted = fernet.decrypt(encrypted)
        return json.loads(decrypted)
    except:
        print("Wrong master password!")
        exit()

def save_passwords(fernet, data):
    encrypted = fernet.encrypt(json.dumps(data).encode())
    with open(DATA_FILE, "wb") as f:
        f.write(encrypted)
def add_password(data, fernet):
    site = input("Website/App name: ")
    user = input("Username: ")
    pwd  = input("Password: ")
    data[site] = {"username": user, "password": pwd}
    save_passwords(fernet, data)
    print(f"Saved password for {site}!")

def get_password(data):
    site = input("Website/App name: ")
    if site in data:
        print(f"  Username: {data[site]['username']}")
        print(f"  Password: {data[site]['password']}")
    else:
        print("Not found.")

def delete_password(data, fernet):
    site = input("Website/App name to delete: ")
    if site in data:
        del data[site]
        save_passwords(fernet, data)
        print(f"Deleted {site}.")
    else:
        print("Not found.")

def search_passwords(data):
    keyword = input("Search keyword: ").lower()
    results = [s for s in data if keyword in s.lower()]
    if results:
        print(f"Found: {results}")
    else:
        print("No matches.")
def main():
    master = input("Enter master password: ")
    fernet = get_key(master)
    data   = load_passwords(fernet)
    print("Unlocked!\n")

    while True:
        print("\n--- Password Manager ---")
        print("1. Add password")
        print("2. Get password")
        print("3. Delete password")
        print("4. Search")
        print("5. Exit")
        
        choice = input("Choose (1-5): ")
        
        if   choice == "1": add_password(data, fernet)
        elif choice == "2": get_password(data)
        elif choice == "3": delete_password(data, fernet)
        elif choice == "4": search_passwords(data)
        elif choice == "5": break
        else: print("Invalid choice.")

main()