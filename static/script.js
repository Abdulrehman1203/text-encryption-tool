/*
  script.js
  ---------
  Handles all frontend behaviour:
  - Showing/hiding the key field depending on the chosen algorithm
  - Showing a short info note (encryption vs encoding vs hashing)
  - Sending encrypt/decrypt requests to the Flask backend
  - Displaying results, errors, and copy-to-clipboard feedback
*/

const algorithmSelect = document.getElementById("algorithm");
const keyField = document.getElementById("keyField");
const keyInput = document.getElementById("keyInput");
const keyLabel = document.getElementById("keyLabel");
const algoInfo = document.getElementById("algoInfo");

const inputText = document.getElementById("inputText");
const outputText = document.getElementById("outputText");
const errorMsg = document.getElementById("errorMsg");
const copyConfirm = document.getElementById("copyConfirm");

const encryptBtn = document.getElementById("encryptBtn");
const decryptBtn = document.getElementById("decryptBtn");
const resetBtn = document.getElementById("resetBtn");
const copyBtn = document.getElementById("copyBtn");

// Info text shown per algorithm so users understand what category it belongs to.
const ALGO_INFO = {
  caesar: "Type: Classical Encryption (reversible). Key = a whole number shift, e.g. 3.",
  vigenere: "Type: Classical Encryption (reversible). Key = a letters-only keyword, e.g. KEY.",
  aes: "Type: Modern Encryption (reversible). Key = any secret passphrase.",
  des: "Type: Legacy Encryption (reversible, weak by modern standards). Key = any secret passphrase.",
  des3: "Type: Legacy Encryption, stronger than DES (reversible). Key = any secret passphrase.",
  rsa: "Type: Asymmetric Encryption (reversible). Key = a secret passphrase used to regenerate the same key pair — real RSA keys are normally random, not password-derived. Key generation may take a moment.",
  base64: "Type: Encoding, NOT encryption. No key needed. Anyone can decode it — it provides no security.",
  hex: "Type: Encoding, NOT encryption. No key needed. Even easier to read/reverse by eye than Base64.",
  md5: "Type: One-way Hashing (older, cryptographically broken). No key needed. Cannot be decrypted.",
  sha256: "Type: One-way Hashing. No key needed. Cannot be decrypted/reversed — used to verify integrity, not to hide data."
};

// Algorithms that don't support a "Decrypt" action.
const NO_DECRYPT = ["md5", "sha256"];

// Algorithms that need a key/shift input field.
const NEEDS_KEY = ["caesar", "vigenere", "aes", "des", "des3", "rsa"];

algorithmSelect.addEventListener("change", () => {
  const algo = algorithmSelect.value;
  clearError();

  if (!algo) {
    keyField.style.display = "none";
    algoInfo.style.display = "none";
    return;
  }

  // Show/hide key field
  if (NEEDS_KEY.includes(algo)) {
    keyField.style.display = "block";
    if (algo === "caesar") {
      keyLabel.textContent = "Shift (number)";
      keyInput.type = "number";
      keyInput.placeholder = "e.g. 3";
    } else if (algo === "vigenere") {
      keyLabel.textContent = "Keyword (letters only)";
      keyInput.type = "text";
      keyInput.placeholder = "e.g. KEY";
    } else {
      keyLabel.textContent = "Secret Key";
      keyInput.type = "text";
      keyInput.placeholder = "Enter a passphrase";
    }
  } else {
    keyField.style.display = "none";
    keyInput.value = "";
  }

  // Show algorithm info note
  algoInfo.textContent = ALGO_INFO[algo] || "";
  algoInfo.style.display = "block";

  // Disable decrypt button for one-way hashes
  decryptBtn.disabled = NO_DECRYPT.includes(algo);
  decryptBtn.style.opacity = decryptBtn.disabled ? "0.5" : "1";
  decryptBtn.style.cursor = decryptBtn.disabled ? "not-allowed" : "pointer";
});

encryptBtn.addEventListener("click", () => runRequest("/encrypt"));
decryptBtn.addEventListener("click", () => runRequest("/decrypt"));

async function runRequest(endpoint) {
  clearError();
  outputText.value = "";
  copyConfirm.textContent = "";

  const algorithm = algorithmSelect.value;
  const text = inputText.value;
  const key = keyInput.value;

  // Basic frontend validation (backend re-validates too, for safety).
  if (!algorithm) {
    showError("Please select an algorithm.");
    return;
  }
  if (!text.trim()) {
    showError("Please enter some text.");
    return;
  }
  if (endpoint === "/decrypt" && NO_DECRYPT.includes(algorithm)) {
    const label = algorithm === "md5" ? "MD5" : "SHA-256";
    showError(`${label} is a one-way hash and cannot be decrypted.`);
    return;
  }
  if (NEEDS_KEY.includes(algorithm) && !String(key).trim()) {
    if (algorithm === "caesar") {
      showError("Please enter a numeric shift value.");
    } else if (algorithm === "vigenere") {
      showError("Please enter a letters-only keyword.");
    } else {
      showError("Please enter a secret key/passphrase.");
    }
    return;
  }

  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ algorithm, text, key })
    });

    const data = await response.json();

    if (!response.ok) {
      showError(data.error || "Something went wrong.");
      return;
    }

    outputText.value = data.result;
  } catch (err) {
    showError("Could not reach the server. Is the Flask app running?");
  }
}

copyBtn.addEventListener("click", () => {
  if (!outputText.value) {
    showError("Nothing to copy yet.");
    return;
  }
  navigator.clipboard.writeText(outputText.value).then(() => {
    copyConfirm.textContent = "Copied!";
    setTimeout(() => (copyConfirm.textContent = ""), 2000);
  });
});

resetBtn.addEventListener("click", () => {
  inputText.value = "";
  outputText.value = "";
  keyInput.value = "";
  algorithmSelect.value = "";
  keyField.style.display = "none";
  algoInfo.style.display = "none";
  clearError();
  copyConfirm.textContent = "";
});

function showError(msg) {
  errorMsg.textContent = msg;
}

function clearError() {
  errorMsg.textContent = "";
}
