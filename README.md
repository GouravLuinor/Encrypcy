# Encrypcy

A lightweight Streamlit application for encrypting and decrypting short text messages using Fernet authenticated symmetric encryption.

The app generates a unique encryption key for each message and allows the original text to be recovered only with the corresponding encrypted token and key.

> **Note:** Encrypcy is an educational utility project. Anyone who obtains both the encrypted text and its corresponding key can decrypt the message.

---

## Features

* Encrypt short text messages of up to 40 words
* Generate a new Fernet key during encryption
* Copy encrypted text and keys directly from the interface
* Decrypt messages using the matching token and key
* Handle invalid or mismatched decryption inputs gracefully
* Escape user-controlled output before rendering it in HTML
* Run through an interactive Streamlit interface
* Support VS Code Dev Containers and GitHub Codespaces

---

## How It Works

### Encryption

1. Enter a text message.
2. Click **Encrypt Text**.
3. The app generates a Fernet key.
4. The message is encrypted into a URL-safe token.
5. Save both the encrypted text and the generated key.

### Decryption

1. Open the **Decrypt** tab.
2. Paste the encrypted text.
3. Paste the corresponding key.
4. Click **Decrypt Text**.
5. The original message is displayed if the token and key are valid.

---

## Tech Stack

* Python
* Streamlit
* `cryptography`
* Fernet authenticated symmetric encryption

---

## Project Structure

```text
Encrypcy/
├── .devcontainer/
│   └── devcontainer.json
├── .gitignore
├── app.py
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone git@github.com:GouravLuinor/Encrypcy.git
cd Encrypcy
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the Application

```bash
python -m streamlit run app.py
```

Then open the local URL displayed by Streamlit, typically:

```text
http://localhost:8501
```

---

## Security Notes

* The encryption key must be protected separately from the encrypted message.
* Anyone with both the encrypted token and its matching key can decrypt the message.
* Share keys through a separate trusted channel when possible.
* The application does not provide identity verification, secure key exchange, or persistent key management.
* This project should not be treated as a complete end-to-end secure messaging system.

---

## Future Improvements

* Password-derived encryption keys
* Expiring encrypted messages
* QR-based key sharing
* Automated tests
* Improved key-management workflows
* Deployment with a public demo
