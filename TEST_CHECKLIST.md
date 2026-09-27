# Test Checklist

## Input Validation
- [ ] Clicking Encrypt with empty text box shows an error and does not crash.
- [ ] Clicking Encrypt with no algorithm selected shows "Please select an algorithm."
- [ ] Selecting Caesar/AES/DES and leaving the key field empty shows an appropriate error.
- [ ] Entering a non-numeric value for Caesar's shift shows "shift must be a whole number."
- [ ] Entering invalid/corrupted ciphertext for AES/DES decrypt shows a clean error (not a crash/stack trace).
- [ ] Entering invalid Base64 text for decode shows "Invalid Base64 text."

## Encryption / Decryption Correctness
- [ ] Caesar: Encrypt "Hello World" with shift 3 → decrypt with shift 3 → returns original text.
- [ ] Caesar: Non-letter characters (numbers, punctuation, spaces) remain unchanged.
- [ ] AES: Encrypt text with a passphrase → decrypt with the SAME passphrase → returns original text.
- [ ] AES: Decrypt with the WRONG passphrase → shows a decryption failed error, not a crash.
- [ ] DES: Encrypt/decrypt round trip works the same way as AES.
- [ ] Base64: Encode then decode returns the original text exactly.
- [ ] SHA-256: Hashing the same input twice always produces the same hash (deterministic).
- [ ] SHA-256: The Decrypt button is disabled/unavailable for this algorithm.

## UI / UX
- [ ] Key input field appears only for Caesar, AES, and DES.
- [ ] Key input field is hidden for Base64 and SHA-256.
- [ ] The info note under the dropdown correctly identifies each algorithm as Encryption, Encoding, or Hashing.
- [ ] Copy Result button copies the output text to the clipboard and shows a "Copied!" confirmation.
- [ ] Reset button clears input, output, key field, and dropdown selection.

## Responsiveness
- [ ] Layout looks correct and usable on a desktop-width browser window.
- [ ] Layout adjusts correctly on a narrow/mobile-width window (fields stack vertically, no horizontal overflow).
- [ ] Buttons remain tappable/clickable at small screen widths.

## Backend / Server
- [ ] `python app.py` starts the Flask server without errors.
- [ ] The homepage (`/`) loads correctly at `http://127.0.0.1:5000`.
- [ ] `/encrypt` and `/decrypt` return proper JSON responses with correct HTTP status codes (200 for success, 400 for validation errors).
