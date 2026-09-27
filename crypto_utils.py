"""
crypto_utils.py
----------------
This file contains all the encryption, decryption, encoding, and hashing
logic used by the Flask app. Keeping this separate from app.py makes the
code easier to read and easier to explain during evaluation.

Algorithms included (10 total):

Classical / Symmetric / Asymmetric Encryption (reversible with the right key):
- Caesar Cipher    -> classical substitution cipher, key = number
- Vigenere Cipher  -> classical polyalphabetic cipher, key = word
- AES (CBC mode)   -> modern symmetric encryption, key = passphrase
- DES (CBC mode)   -> legacy symmetric encryption, key = passphrase
- Triple DES (3DES)-> stronger legacy symmetric encryption, key = passphrase
- RSA              -> asymmetric encryption, key = passphrase (used to
                      deterministically regenerate the same key pair, see note below)

Encoding (reversible, NOT security):
- Base64
- Hexadecimal

Hashing (one-way, NOT reversible):
- MD5
- SHA-256
"""

import base64
import hashlib
from Crypto.Cipher import AES, DES, DES3, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


class CryptoError(Exception):
    """Custom exception so app.py can catch our errors and return clean messages."""
    pass


# ---------------------------------------------------------------------------
# Caesar Cipher
# ---------------------------------------------------------------------------
def caesar_encrypt(text, shift):
    """Shift every letter forward by `shift` positions. Non-letters are left unchanged."""
    shift = shift % 26
    result = []
    for char in text:
        if char.isupper():
            result.append(chr((ord(char) - 65 + shift) % 26 + 65))
        elif char.islower():
            result.append(chr((ord(char) - 97 + shift) % 26 + 97))
        else:
            result.append(char)
    return "".join(result)


def caesar_decrypt(text, shift):
    """Decryption is just encryption with the shift reversed."""
    return caesar_encrypt(text, -shift)


# ---------------------------------------------------------------------------
# Vigenere Cipher
# ---------------------------------------------------------------------------
def _vigenere_transform(text, key, decrypt=False):
    if not key or not key.isalpha():
        raise CryptoError("Vigenere key must contain letters only (e.g. 'KEY').")
    key = key.upper()
    result = []
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - 65
            if decrypt:
                shift = -shift
            if char.isupper():
                result.append(chr((ord(char) - 65 + shift) % 26 + 65))
            else:
                result.append(chr((ord(char) - 97 + shift) % 26 + 97))
            key_index += 1  # only advance the key on actual letters
        else:
            result.append(char)
    return "".join(result)


def vigenere_encrypt(text, key):
    """Each letter is shifted by the corresponding letter of a repeating keyword."""
    return _vigenere_transform(text, key, decrypt=False)


def vigenere_decrypt(text, key):
    return _vigenere_transform(text, key, decrypt=True)


# ---------------------------------------------------------------------------
# Shared helper: turn a user-provided passphrase into a fixed-length key.
# AES needs 16/24/32 byte keys and DES needs an 8 byte key. Instead of asking
# the student/user to type raw byte keys, we let them type any passphrase
# and derive a proper-length key from it using SHA-256/MD5. This is a common,
# easy-to-explain approach for student projects.
# ---------------------------------------------------------------------------
def _derive_key(passphrase, length):
    if length == 8:
        # DES needs an 8-byte key -> use first 8 bytes of an MD5 hash
        return hashlib.md5(passphrase.encode()).digest()[:8]
    # AES-256 needs a 32-byte key -> use a SHA-256 hash directly
    return hashlib.sha256(passphrase.encode()).digest()[:length]


# ---------------------------------------------------------------------------
# AES (CBC mode)
# ---------------------------------------------------------------------------
def aes_encrypt(text, passphrase):
    if not passphrase:
        raise CryptoError("AES requires a secret key/passphrase.")
    key = _derive_key(passphrase, 32)  # AES-256
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext_bytes = cipher.encrypt(pad(text.encode(), AES.block_size))
    # Prepend the IV to the ciphertext so decryption can retrieve it later.
    # Everything is then base64-encoded so it prints as safe, readable text.
    combined = iv + ciphertext_bytes
    return base64.b64encode(combined).decode()


def aes_decrypt(ciphertext_b64, passphrase):
    if not passphrase:
        raise CryptoError("AES requires the same secret key/passphrase used to encrypt.")
    try:
        combined = base64.b64decode(ciphertext_b64)
        iv, ciphertext_bytes = combined[:16], combined[16:]
        key = _derive_key(passphrase, 32)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext_bytes = unpad(cipher.decrypt(ciphertext_bytes), AES.block_size)
        return plaintext_bytes.decode()
    except (ValueError, KeyError):
        raise CryptoError("Decryption failed. Wrong key or corrupted ciphertext.")


# ---------------------------------------------------------------------------
# DES (CBC mode) - included for educational comparison with AES.
# ---------------------------------------------------------------------------
def des_encrypt(text, passphrase):
    if not passphrase:
        raise CryptoError("DES requires a secret key/passphrase.")
    key = _derive_key(passphrase, 8)
    iv = get_random_bytes(8)
    cipher = DES.new(key, DES.MODE_CBC, iv)
    ciphertext_bytes = cipher.encrypt(pad(text.encode(), DES.block_size))
    combined = iv + ciphertext_bytes
    return base64.b64encode(combined).decode()


def des_decrypt(ciphertext_b64, passphrase):
    if not passphrase:
        raise CryptoError("DES requires the same secret key/passphrase used to encrypt.")
    try:
        combined = base64.b64decode(ciphertext_b64)
        iv, ciphertext_bytes = combined[:8], combined[8:]
        key = _derive_key(passphrase, 8)
        cipher = DES.new(key, DES.MODE_CBC, iv)
        plaintext_bytes = unpad(cipher.decrypt(ciphertext_bytes), DES.block_size)
        return plaintext_bytes.decode()
    except (ValueError, KeyError):
        raise CryptoError("Decryption failed. Wrong key or corrupted ciphertext.")


# ---------------------------------------------------------------------------
# Triple DES / 3DES (CBC mode) - a stronger successor to plain DES that
# applies the DES cipher three times with a longer, 24-byte key. Still
# considered legacy today (AES is preferred), but a step up from DES.
# ---------------------------------------------------------------------------
def _derive_des3_key(passphrase):
    # DES3 needs a 24-byte key. We build 24 bytes from two different hashes
    # of the passphrase, then fix up "key parity" so PyCryptodome accepts it,
    # and make sure the three 8-byte sub-keys aren't accidentally identical
    # (DES3 rejects degenerate keys where that happens).
    part1 = hashlib.sha256(passphrase.encode()).digest()[:16]
    part2 = hashlib.md5((passphrase + "extra").encode()).digest()[:8]
    raw_key = part1 + part2
    try:
        return DES3.adjust_key_parity(raw_key)
    except ValueError:
        # Extremely unlikely degenerate case - tweak the passphrase and retry once.
        raw_key = hashlib.sha256((passphrase + "!").encode()).digest()[:24]
        return DES3.adjust_key_parity(raw_key)


def des3_encrypt(text, passphrase):
    if not passphrase:
        raise CryptoError("Triple DES requires a secret key/passphrase.")
    key = _derive_des3_key(passphrase)
    iv = get_random_bytes(8)
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    ciphertext_bytes = cipher.encrypt(pad(text.encode(), DES3.block_size))
    combined = iv + ciphertext_bytes
    return base64.b64encode(combined).decode()


def des3_decrypt(ciphertext_b64, passphrase):
    if not passphrase:
        raise CryptoError("Triple DES requires the same secret key/passphrase used to encrypt.")
    try:
        combined = base64.b64decode(ciphertext_b64)
        iv, ciphertext_bytes = combined[:8], combined[8:]
        key = _derive_des3_key(passphrase)
        cipher = DES3.new(key, DES3.MODE_CBC, iv)
        plaintext_bytes = unpad(cipher.decrypt(ciphertext_bytes), DES3.block_size)
        return plaintext_bytes.decode()
    except (ValueError, KeyError):
        raise CryptoError("Decryption failed. Wrong key or corrupted ciphertext.")


# ---------------------------------------------------------------------------
# RSA (asymmetric encryption)
# ---------------------------------------------------------------------------
# RSA normally uses a randomly generated public/private key PAIR rather than
# a typed passphrase. To keep this tool's UI consistent with the other
# algorithms (one text/passphrase field), we deterministically regenerate the
# SAME key pair from the passphrase every time, using a seeded pseudo-random
# byte generator in place of RSA.generate()'s normal random source.
#
# IMPORTANT (explain this in the demo/report): real-world RSA keys must be
# generated with a truly random source and are never derived from a
# password. This deterministic approach is purely a teaching convenience so
# a single passphrase field can both "encrypt" (using the derived public
# key) and "decrypt" (by re-deriving the same private key).
# ---------------------------------------------------------------------------
def _seeded_randfunc(passphrase):
    """Returns a function that produces a deterministic byte stream from passphrase."""
    counter = [0]

    def randfunc(n):
        out = b""
        while len(out) < n:
            counter[0] += 1
            block = hashlib.sha256(f"{passphrase}:{counter[0]}".encode()).digest()
            out += block
        return out[:n]

    return randfunc


def _generate_rsa_key(passphrase):
    if not passphrase:
        raise CryptoError("RSA requires a secret passphrase (used to derive the key pair).")
    return RSA.generate(2048, randfunc=_seeded_randfunc(passphrase))


def rsa_encrypt(text, passphrase):
    key = _generate_rsa_key(passphrase)
    cipher = PKCS1_OAEP.new(key.publickey())
    try:
        ciphertext_bytes = cipher.encrypt(text.encode())
    except ValueError:
        raise CryptoError(
            "Text is too long for RSA-2048 encryption (max ~190 bytes). "
            "Try a shorter message or use AES for longer text."
        )
    return base64.b64encode(ciphertext_bytes).decode()


def rsa_decrypt(ciphertext_b64, passphrase):
    key = _generate_rsa_key(passphrase)
    cipher = PKCS1_OAEP.new(key)
    try:
        ciphertext_bytes = base64.b64decode(ciphertext_b64)
        plaintext_bytes = cipher.decrypt(ciphertext_bytes)
        return plaintext_bytes.decode()
    except (ValueError, KeyError):
        raise CryptoError("Decryption failed. Wrong passphrase or corrupted ciphertext.")


# ---------------------------------------------------------------------------
# Base64 - this is ENCODING, not encryption. No key is used, and it provides
# zero confidentiality. It is included so students can compare it against
# real encryption and clearly explain the difference.
# ---------------------------------------------------------------------------
def base64_encode(text):
    return base64.b64encode(text.encode()).decode()


def base64_decode(encoded_text):
    try:
        return base64.b64decode(encoded_text).decode()
    except Exception:
        raise CryptoError("Invalid Base64 text. Cannot decode.")


# ---------------------------------------------------------------------------
# Hexadecimal - like Base64, this is ENCODING, not encryption. No key, and
# it is even easier to read/reverse by eye than Base64.
# ---------------------------------------------------------------------------
def hex_encode(text):
    return text.encode().hex()


def hex_decode(hex_text):
    try:
        cleaned = hex_text.strip().replace(" ", "")
        return bytes.fromhex(cleaned).decode()
    except ValueError:
        raise CryptoError("Invalid hexadecimal text. Cannot decode.")


# ---------------------------------------------------------------------------
# MD5 - this is HASHING, not encryption. Like SHA-256 it is one-way and has
# no decrypt function. MD5 is included alongside SHA-256 so students can
# compare an older, now cryptographically broken hash function against a
# current, secure one.
# ---------------------------------------------------------------------------
def md5_hash(text):
    return hashlib.md5(text.encode()).hexdigest()


# ---------------------------------------------------------------------------
# SHA-256 - this is HASHING, not encryption. It is one-way: there is no
# decrypt function for it, on purpose, because hashes cannot be reversed.
# ---------------------------------------------------------------------------
def sha256_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()
