import streamlit as st
from cryptography.fernet import Fernet

# --- Page Config ---
st.set_page_config(page_title="Encrypt / Decrypt App", page_icon="🔐", layout="centered")

# --- Custom CSS ---
st.markdown("""
<style>
body {
    background-color: #f9f9f9;
}
h1 {
    text-align: center;
    color: #333333;
}
textarea {
    font-size: 16px !important;
}
.copy-btn {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 6px 12px;
    margin-top: 5px;
    border-radius: 8px;
    cursor: pointer;
}
.copy-btn:hover {
    background-color: #45a049;
}
.output-box {
    background: #ffffff;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-family: monospace;
    white-space: pre-wrap;
    word-wrap: break-word;
}
</style>
""", unsafe_allow_html=True)

# --- JavaScript for copy ---
copy_js = """
<script>
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(function() {
    alert('Copied to clipboard!');
  }, function() {
    alert('Failed to copy text.');
  });
}
</script>
"""
st.markdown(copy_js, unsafe_allow_html=True)

# --- App Title ---
st.title("🔐 Encrypt / Decrypt Tool")

# Tabs
tab1, tab2 = st.tabs(["Encrypt", "Decrypt"])

# --- Encrypt Section ---
with tab1:
    st.subheader("Generate Encrypted Code")
    text = st.text_area("Enter a sentence (English):", height=150, placeholder="Type something here...")

    if st.button("Encrypt"):
        if text.strip() != "":
            key = Fernet.generate_key()
            fernet = Fernet(key)
            encrypted_text = fernet.encrypt(text.encode()).decode()

            st.success("Encryption successful!")

            # Encrypted Text Display with Copy Button
            st.markdown(f"""
            <div class='output-box'>{encrypted_text}</div>
            <button class="copy-btn" onclick="copyToClipboard('{encrypted_text}')">Copy Encrypted Text</button>
            """, unsafe_allow_html=True)

            # Key Display with Copy Button
            st.markdown(f"""
            <div class='output-box'>{key.decode()}</div>
            <button class="copy-btn" onclick="copyToClipboard('{key.decode()}')">Copy Key</button>
            """, unsafe_allow_html=True)

        else:
            st.warning("Please enter a sentence to encrypt.")

# --- Decrypt Section ---
with tab2:
    st.subheader("Decode Encrypted Code")
    encrypted_input = st.text_area("Enter Encrypted Text:", height=150, placeholder="Paste encrypted text here...")
    key_input = st.text_area("Enter Key:", height=100, placeholder="Paste key here...")

    if st.button("Decrypt"):
        try:
            fernet = Fernet(key_input.encode())
            decrypted_text = fernet.decrypt(encrypted_input.encode()).decode()
            st.success("Decryption successful!")

            st.markdown(f"""
            <div class='output-box'>{decrypted_text}</div>
            <button class="copy-btn" onclick="copyToClipboard('{decrypted_text}')">Copy Decrypted Text</button>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error("Invalid key or encrypted text. Please check and try again.")
