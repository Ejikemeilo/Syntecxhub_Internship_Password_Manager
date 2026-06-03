# 🔐 Password Manager

A lightweight, terminal-based password manager written in Python. It encrypts and stores your passwords locally using a master password — nothing is sent to the cloud.

---

## Features

- AES encryption via the `cryptography` library (Fernet)
- Master password-derived key using PBKDF2 with 100,000 iterations
- Add, retrieve, delete, and search saved credentials
- All data stored locally in an encrypted file

---

## Requirements

- Python 3.7+
- `cryptography` library

Install the dependency with:

```bash
pip install cryptography
```

---

## Usage

Run the script from your terminal:

```bash
python password_manager.py
```

You will be prompted to enter your **master password**. This is the single password that locks and unlocks all your stored credentials. **Do not forget it** — there is no recovery option.

### Menu Options

| Option | Action |
|--------|--------|
| `1` | Add a new password |
| `2` | Retrieve a saved password |
| `3` | Delete a saved password |
| `4` | Search passwords by keyword |
| `5` | Exit |

---

## How It Works

### Key Derivation
When you enter your master password, the script uses **PBKDF2-HMAC-SHA256** with a randomly generated salt (stored in `salt.key`) to derive a 32-byte encryption key. This makes brute-force attacks significantly harder.

### Encryption
Passwords are stored in `passwords.enc` — a Fernet-encrypted JSON file. Fernet uses AES-128-CBC with HMAC-SHA256 for authenticated encryption, meaning the file cannot be tampered with or read without the correct master password.

### Local Files

| File | Purpose |
|------|---------|
| `salt.key` | Random salt used to derive your encryption key |
| `passwords.enc` | Your encrypted password vault |

> ⚠️ Keep both files in the same directory as the script. If `salt.key` is lost or deleted, your vault cannot be decrypted even with the correct master password.

---

## Security Notes

- Your master password is **never stored** anywhere — it is only used in-memory to derive the encryption key.
- Passwords are printed in **plain text** to the terminal when retrieved. Be mindful of your surroundings.
- This tool is intended for **personal, local use**. For team or enterprise use, consider a dedicated secrets manager.
- Back up `salt.key` and `passwords.enc` securely if you wish to preserve your vault.

---

## Example Session

```
Enter master password: ••••••••
Unlocked!

--- Password Manager ---
1. Add password
2. Get password
3. Delete password
4. Search
5. Exit
Choose (1-5): 1
Website/App name: github.com
Username: johndoe
Password: mySecurePass123
Saved password for github.com!
```

---

## Author
Ilo C. Ejikeme


## License

This project is for personal use. Feel free to modify and extend it as needed.
