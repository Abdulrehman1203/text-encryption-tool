# Project Report: Web-Based Text Encryption Tool

## 1. Introduction

This project implements a web-based application that allows a user to protect or transform text using five different techniques: Caesar Cipher, AES, DES, Base64, and SHA-256. A key learning objective of this project is understanding that these five techniques are **not all the same kind of operation** — some are encryption, one is encoding, and one is hashing. This report explains each technique and clarifies which category it belongs to.

## 2. Encryption vs. Encoding vs. Hashing

| Property | Encryption | Encoding | Hashing |
|---|---|---|---|
| Purpose | Confidentiality (hide data) | Data format conversion | Integrity / verification |
| Reversible? | Yes, with the correct key | Yes, no key needed | No — one-way only |
| Needs a key? | Yes | No | No |
| Example in this project | AES, DES, Caesar | Base64 | SHA-256 |

## 3. Caesar Cipher (Encryption)

The Caesar Cipher is one of the oldest known encryption techniques. Each letter in the plaintext is shifted a fixed number of positions down the alphabet. For example, with a shift of 3, "A" becomes "D".

- **Type:** Classical symmetric encryption
- **Key:** A single integer (the shift value)
- **Strength:** Very weak — there are only 26 possible shifts, so it can be broken instantly by brute force. Included here purely for educational purposes to demonstrate the basic idea of substitution ciphers.

## 4. AES — Advanced Encryption Standard (Encryption)

AES is a modern, widely used symmetric-key block cipher adopted as a U.S. government standard in 2001. This project uses **AES-256 in CBC (Cipher Block Chaining) mode**.

- **Type:** Modern symmetric encryption
- **Key:** A secret passphrase, converted internally into a 256-bit key using SHA-256
- **IV (Initialization Vector):** A random 16-byte value generated for every encryption so that encrypting the same text twice produces different ciphertext
- **Strength:** Considered secure for real-world use when implemented correctly with a strong key

## 5. DES — Data Encryption Standard (Encryption)

DES was the U.S. government's official encryption standard from 1977 until it was replaced by AES. It is a symmetric block cipher using a 56-bit effective key.

- **Type:** Legacy symmetric encryption
- **Key:** A secret passphrase, converted internally into an 8-byte (64-bit, 56 effective bits) key
- **Strength:** Weak by modern standards — its small key size makes it vulnerable to brute-force attacks with modern computing power. It is included in this project purely to let students compare an older cipher against AES.

## 6. Base64 (Encoding — NOT Encryption)

Base64 converts binary or text data into an ASCII string made up of 64 printable characters. It is commonly used to safely transmit data over text-based protocols such as email or JSON.

- **Type:** Encoding
- **Key:** None
- **Important distinction:** Base64 provides **no confidentiality**. Anyone can decode Base64 text instantly without any secret information — it is a format transformation, not a security mechanism. This project deliberately labels it as "Encoding" rather than "Encryption" in the UI to reinforce this distinction.

## 7. SHA-256 (Hashing — NOT Encryption)

SHA-256 (Secure Hash Algorithm, 256-bit) takes an input of any length and produces a fixed-size 256-bit (64 hex character) output called a hash or digest.

- **Type:** Cryptographic hash function
- **Key:** None
- **Important distinction:** Hashing is **one-way** — there is no mathematical way to recover the original text from its hash. This is why the application intentionally does **not** offer a "Decrypt" option for SHA-256. Hashing is used for purposes like verifying data integrity or storing password fingerprints, not for hiding data that needs to be retrieved later.

## 8. Conclusion

This project demonstrates three fundamentally different categories of text transformation. Caesar Cipher, AES, and DES are all encryption algorithms of varying strength and era, Base64 is an encoding scheme with no security value, and SHA-256 is a one-way hash used for integrity rather than confidentiality. Understanding these distinctions is essential in cybersecurity, since misapplying one technique in place of another (for example, assuming Base64 "protects" data) is a common real-world security mistake.
