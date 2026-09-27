"""
app.py
------
Main Flask application. Serves the single page UI and exposes three
JSON API endpoints used by static/script.js:

    POST /encrypt   -> encrypt or encode plaintext
    POST /decrypt   -> decrypt or decode ciphertext
    POST /hash      -> one-way SHA-256 hash (no decrypt route exists for this)

All the actual algorithm logic lives in crypto_utils.py so this file
stays focused on request handling and validation.
"""

from flask import Flask, render_template, request, jsonify
import crypto_utils

app = Flask(__name__)

# Algorithms that need a text/number key from the user.
ALGORITHMS_REQUIRING_KEY = {"caesar", "vigenere", "aes", "des", "des3", "rsa"}

# Algorithms that support decryption (MD5 and SHA-256 intentionally excluded
# -- hashes are one-way and cannot be reversed).
REVERSIBLE_ALGORITHMS = {"caesar", "vigenere", "aes", "des", "des3", "rsa", "base64", "hex"}

# Hash algorithms have no decrypt route at all.
HASH_ALGORITHMS = {"md5", "sha256"}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/encrypt", methods=["POST"])
def encrypt():
    data = request.get_json(silent=True) or {}
    algorithm = data.get("algorithm", "")
    text = data.get("text", "")
    key = data.get("key", "")

    error = _validate_common(algorithm, text, key)
    if error:
        return jsonify({"error": error}), 400

    try:
        if algorithm == "caesar":
            shift = _parse_caesar_shift(key)
            result = crypto_utils.caesar_encrypt(text, shift)
        elif algorithm == "vigenere":
            result = crypto_utils.vigenere_encrypt(text, key)
        elif algorithm == "aes":
            result = crypto_utils.aes_encrypt(text, key)
        elif algorithm == "des":
            result = crypto_utils.des_encrypt(text, key)
        elif algorithm == "des3":
            result = crypto_utils.des3_encrypt(text, key)
        elif algorithm == "rsa":
            result = crypto_utils.rsa_encrypt(text, key)
        elif algorithm == "base64":
            result = crypto_utils.base64_encode(text)
        elif algorithm == "hex":
            result = crypto_utils.hex_encode(text)
        elif algorithm == "md5":
            result = crypto_utils.md5_hash(text)
        elif algorithm == "sha256":
            result = crypto_utils.sha256_hash(text)
        else:
            return jsonify({"error": "Unknown algorithm selected."}), 400

        return jsonify({"result": result})

    except crypto_utils.CryptoError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Something went wrong while processing your request."}), 500


@app.route("/decrypt", methods=["POST"])
def decrypt():
    data = request.get_json(silent=True) or {}
    algorithm = data.get("algorithm", "")
    text = data.get("text", "")
    key = data.get("key", "")

    if algorithm in HASH_ALGORITHMS:
        label = "MD5" if algorithm == "md5" else "SHA-256"
        return jsonify({"error": f"{label} is a one-way hash. It cannot be decrypted."}), 400

    if algorithm not in REVERSIBLE_ALGORITHMS:
        return jsonify({"error": "Unknown or unsupported algorithm for decryption."}), 400

    if not text.strip():
        return jsonify({"error": "Please enter the ciphertext you want to decrypt."}), 400

    if algorithm in ALGORITHMS_REQUIRING_KEY and not str(key).strip():
        return jsonify({"error": "This algorithm requires the original key to decrypt."}), 400

    try:
        if algorithm == "caesar":
            shift = _parse_caesar_shift(key)
            result = crypto_utils.caesar_decrypt(text, shift)
        elif algorithm == "vigenere":
            result = crypto_utils.vigenere_decrypt(text, key)
        elif algorithm == "aes":
            result = crypto_utils.aes_decrypt(text, key)
        elif algorithm == "des":
            result = crypto_utils.des_decrypt(text, key)
        elif algorithm == "des3":
            result = crypto_utils.des3_decrypt(text, key)
        elif algorithm == "rsa":
            result = crypto_utils.rsa_decrypt(text, key)
        elif algorithm == "base64":
            result = crypto_utils.base64_decode(text)
        elif algorithm == "hex":
            result = crypto_utils.hex_decode(text)
        else:
            return jsonify({"error": "Unknown algorithm selected."}), 400

        return jsonify({"result": result})

    except crypto_utils.CryptoError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Decryption failed. Please check your ciphertext and key."}), 500


def _validate_common(algorithm, text, key):
    """Shared validation rules for the /encrypt route."""
    if not algorithm:
        return "Please select an encryption method."
    if not text.strip():
        return "Please enter some text to encrypt."
    if algorithm in ALGORITHMS_REQUIRING_KEY and not str(key).strip():
        if algorithm == "caesar":
            return "Please enter a numeric shift value for Caesar Cipher."
        if algorithm == "vigenere":
            return "Please enter a letters-only keyword for Vigenere Cipher."
        return "Please enter a secret key/passphrase for this algorithm."
    return None


def _parse_caesar_shift(key):
    try:
        return int(key)
    except (TypeError, ValueError):
        raise crypto_utils.CryptoError("Caesar Cipher shift must be a whole number.")


if __name__ == "__main__":
    app.run(debug=True)
