# Demo Video Script (approx. 3–4 minutes)

## 1. Intro (15–20 seconds)
"Hi, this is my project for [course name] — a Web-Based Text Encryption Tool. It lets a user encrypt, decrypt, encode, or hash text using five different techniques, and it's built with a Python Flask backend and a plain HTML/CSS/JavaScript frontend."

## 2. Show the UI (15 seconds)
- Open the browser at `http://127.0.0.1:5000`
- Point out: input box, algorithm dropdown, key field, Encrypt/Decrypt/Reset buttons, output box, Copy button.

## 3. Demonstrate Caesar Cipher (30 seconds)
- Type: `Hello World`
- Select **Caesar Cipher**, enter shift `3`
- Click **Encrypt** → show ciphertext
- Click **Decrypt** with the same shift → show it returns to the original text
- Say: "Caesar Cipher is a classical encryption technique — simple, but easy to break."

## 4. Demonstrate AES (30–40 seconds)
- Type: `Confidential Report 2026`
- Select **AES**, enter a passphrase, e.g. `mySecret123`
- Click **Encrypt** → show ciphertext
- Click **Decrypt** with the same key → show original text returns
- Say: "AES is a modern, strong encryption standard used in real-world systems today."

## 5. Demonstrate DES (20–30 seconds)
- Same text, select **DES**, same passphrase
- Encrypt then decrypt
- Say: "DES is the older standard AES replaced — I included it so I could compare an outdated cipher with a modern one."

## 6. Demonstrate Base64 (20 seconds)
- Select **Base64**
- Encrypt (encode) then decode
- Say: "Base64 is NOT encryption — it's just encoding. Notice it needs no key at all, and anyone can decode it instantly. I made sure the UI labels it correctly as encoding, not encryption."

## 7. Demonstrate SHA-256 (20 seconds)
- Select **SHA-256**, click **Encrypt** (generate hash)
- Point out the **Decrypt** button is disabled/greyed out
- Say: "SHA-256 is a one-way hash. There's intentionally no decrypt option here, because hashes can't be reversed — this is a core distinction in cybersecurity."

## 8. Show validation (15–20 seconds)
- Try clicking Encrypt with empty text → show error message
- Try AES with no key → show error message
- Say: "The app validates input so it doesn't fail silently or crash."

## 9. Wrap-up (10–15 seconds)
- Show the Copy button working
- Say: "That covers encryption, decryption, encoding, hashing, and validation — thanks for watching."
