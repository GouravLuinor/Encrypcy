import streamlit as st
from cryptography.fernet import Fernet
import streamlit.components.v1 as components

st.set_page_config(page_title="🔐 Encrypt / Decrypt", layout="centered")

# --- Custom Styling ---
st.markdown("""
<style>
body {
    font-family: 'Segoe UI', sans-serif;
}
.stTextArea textarea {
    font-size: 16px !important;
}
.output-box {
    background-color: #2b2b2b;
    padding: 16px;
    border-radius: 12px;
    margin-bottom: 8px;
    border: 1px solid #444;
    font-family: monospace;
    font-size: 16px;
    color: #f1f1f1;
    white-space: pre-wrap;
    word-wrap: break-word;
    box-shadow: 0 0 8px rgba(0,0,0,0.3);
}
.copy-btn {
    background-color: #08d9d6;
    color: #000;
    font-weight: 600;
    padding: 8px 14px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 15px;
    transition: background 0.2s ease;
    margin-bottom: 25px;
}
.copy-btn:hover {
    background-color: #00bfb1;
}
</style>
""", unsafe_allow_html=True)

# --- JavaScript Copy Box Function ---
def render_copyable(label: str, value: str, box_id: str):
    components.html(f"""
        <div class="output-box" id="{box_id}">{value}</div>
        <button class="copy-btn" onclick="copyToClipboard('{box_id}')">📋 Copy {label}</button>
        <script>
            function copyToClipboard(id) {{
                const text = document.getElementById(id).innerText;
                navigator.clipboard.writeText(text).then(function() {{
                    console.log("Copied!");
                }}, function(err) {{
                    alert("Failed to copy: " + err);
                }});
            }}
        </script>
    """, height=170)

# --- App Title & Layout ---
st.title("🔐 GOURAV is CHAD")

tab1, tab2 = st.tabs(["🔒 Encrypt", "🔓 Decrypt"])

# --- ENCRYPT SECTION ---
with tab1:
    st.subheader("🔒 Generate Encrypted Text")
    input_text = st.text_area("Enter your message:", height=150)

    if st.button("Encrypt"):
        if input_text.strip():
            key = Fernet.generate_key()
            fernet = Fernet(key)
            encrypted = fernet.encrypt(input_text.encode()).decode()
            st.success("✅ Encrypted successfully!")

            render_copyable("Encrypted Text", encrypted, "enc_box")
            render_copyable("Key", key.decode(), "key_box")
        else:
            st.warning("Please enter some text to encrypt.")

# --- DECRYPT SECTION ---
with tab2:
    st.subheader("🔓 Decrypt Encrypted Text")
    encrypted_input = st.text_area("Paste Encrypted Text", height=150)
    key_input = st.text_area("Paste Key", height=100)

    if st.button("Decrypt"):
        try:
            f = Fernet(key_input.encode())
            decrypted = f.decrypt(encrypted_input.encode()).decode()
            st.success("✅ Decrypted successfully!")
            render_copyable("Decrypted Text", decrypted, "dec_box")
        except Exception as e:
            st.error("❌ Decryption failed. Please check your inputs.")
