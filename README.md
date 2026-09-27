# Web-Based Text Encryption Tool

A single-page web application built with **Flask (Python)** and **vanilla HTML/CSS/JavaScript** that lets a user enter plain text, choose an algorithm, and see the resulting output — while clearly distinguishing between **encryption**, **encoding**, and **hashing**.

## Features

**10 algorithms across 3 categories:**

**Encryption (reversible with the correct key)**
- **Caesar Cipher** — classical substitution cipher, key = a number
- **Vigenere Cipher** — classical polyalphabetic cipher, key = a keyword
- **AES (CBC mode)** — modern symmetric encryption, key = passphrase
- **DES (CBC mode)** — legacy symmetric encryption, key = passphrase
- **Triple DES (3DES)** — stronger legacy symmetric encryption, key = passphrase
- **RSA** — asymmetric encryption, key = passphrase (see note below)

**Encoding (reversible, but NOT secure)**
- **Base64**
- **Hexadecimal**

**Hashing (one-way, no decrypt option)**
- **MD5**
- **SHA-256**

- Input validation (empty text, missing algorithm, missing/invalid key)
- Decrypt support wherever technically applicable
- Copy-to-clipboard button
- Reset/clear button
- Clean, responsive UI

## Project Structure

```
text-encryption-tool/
├── app.py                  # Flask routes (/, /encrypt, /decrypt)
├── crypto_utils.py          # All algorithm implementations
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
├── README.md
├── REPORT.md
├── DEMO_SCRIPT.md
└── TEST_CHECKLIST.md
```

## Setup & Run Instructions

**1. Requirements**
- Python 3.9+

**2. Create a virtual environment (recommended)**
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
python app.py
```

**5. Open in your browser**
```
http://127.0.0.1:5000
```

## How to Use

1. Type or paste text into the **Input Text** box.
2. Select an algorithm from the dropdown.
3. If a key is required (Caesar shift, AES/DES passphrase), enter it in the field that appears.
4. Click **Encrypt** (or **Decrypt** to reverse it, where supported).
5. Use **Copy Result** to copy the output, or **Reset** to start over.

## Notes on Security Design

- AES, DES, and Triple DES keys are passphrases typed by the user; they are converted internally into fixed-length keys using a hash function (SHA-256/MD5) since these ciphers require exact-length keys (32/8/24 bytes). This is a standard, simple approach for educational projects.
- A random IV (Initialization Vector) is generated for every AES/DES/3DES encryption and stored alongside the ciphertext (prepended, then Base64-encoded), which is standard practice for CBC mode.
- **RSA is special**: real-world RSA uses a randomly generated public/private key *pair*, never a password. To keep this tool's UI consistent (one passphrase field for every algorithm), the app deterministically regenerates the *same* key pair from the passphrase every time, using a seeded pseudo-random byte stream in place of true randomness. This is called out clearly in the UI and report — it's a teaching convenience, not something you'd do in production RSA.
- Base64 and Hexadecimal are intentionally labeled as **encoding**, not encryption, both in the UI and the code comments, because they involve no secret key and provide no confidentiality.
- MD5 and SHA-256 have no decrypt function anywhere in the codebase — these are hashes, not ciphers. MD5 is included specifically so it can be compared against SHA-256 as an example of a hash function that is now considered cryptographically broken.

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python (Flask)
- **Encryption library:** PyCryptodome
