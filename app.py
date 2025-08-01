import streamlit as st
from cryptography.fernet import Fernet
import streamlit.components.v1 as components

st.set_page_config(page_title="Secure Text Encryptor", layout="centered")

# ----------------- Custom CSS ----------------- #
st.markdown("""
<style>
body, .stApp {
    background-color: #0f1117;
    color: #ffffff;
    font-family: 'Segoe UI', sans-serif;
}

h1, h2, h3, h4, h5, h6 {
    color: #21f3c7;
}

textarea {
    font-size: 15px !important;
}

.output-box, .decrypted-box {
    background-color: #1a1d23;
    padding: 16px;
    border-radius: 12px;
    font-size: 16px;
    font-family: 'Courier New', monospace;
    border: 1px solid #333;
    margin-bottom: 12px;
    white-space: pre-wrap;
    word-wrap: break-word;
}

.output-box {
    color: #ffffff;
}

.decrypted-box {
    color: #21f3c7;
    font-weight: bold;
    text-align: center;
    font-size: 18px;
}

.copy-btn {
    background: linear-gradient(135deg, #21f3c7, #18c1b1);
    border: none;
    color: #000;
    padding: 8px 18px;
    font-weight: 600;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
    margin-top: -5px;
    font-size: 14px;
}

.copy-btn:hover {
    transform: scale(1.05);
    background: linear-gradient(135deg, #18c1b1, #21f3c7);
}

.fade-msg {
    color: #16f1a9;
    font-size: 14px;
    animation: fadeout 2s ease-out forwards;
    margin-top: 6px;
    font-weight: 500;
}

@keyframes fadeout {
    0% { opacity: 1; }
    80% { opacity: 1; }
    100% { opacity: 0; }
}
</style>
""", unsafe_allow_html=True)

# ----------------- Copy Utility ----------------- #
def render_copyable(label: str, value: str, box_id: str):
    components.html(f"""
        <div class="output-box" id="{box_id}">{value}</div>
        <button class="copy-btn" onclick="copyToClipboard('{box_id}', '{box_id}-msg')">📋 Copy {label}</button>
        <div id="{box_id}-msg" class="fade-msg" style="display:none;">✅ Copied!</div>
        <script>
            function copyToClipboard(id, msgId) {{
                const el = document.getElementById(id);
                navigator.clipboard.writeText(el.innerText).then(function() {{
                    const msg = document.getElementById(msgId);
                    msg.style.display = 'block';
                    msg.style.animation = 'fadeout 2s ease-out forwards';
                    setTimeout(() => {{ msg.style.display = 'none'; }}, 2000);
                }});
            }}
        </script>
    """, height=180)

# ----------------- UI Layout ----------------- #
st.title("🔐 GOURAV is CHAD")
tab1, tab2 = st.tabs(["🔒 Encrypt", "🔓 Decrypt"])

# ----------------- ENCRYPT ----------------- #
with tab1:
    st.subheader("🔒 Encrypt Text")
    input_text = st.text_area("Enter your message:", height=140, placeholder="Type message to encrypt...")

    if st.button("🔐 Encrypt Text"):
        if input_text.strip():
            key = Fernet.generate_key()
            fernet = Fernet(key)
            encrypted = fernet.encrypt(input_text.encode()).decode()
            st.success("✅ Encrypted Successfully")
            render_copyable("Encrypted Text", encrypted, "encrypted")
            render_copyable("Encryption Key", key.decode(), "key")
        else:
            st.warning("⚠️ Please enter text to encrypt.")

# ----------------- DECRYPT ----------------- #
with tab2:
    st.subheader("🔓 Decrypt Text")
    encrypted_input = st.text_area("Paste Encrypted Text", height=130)
    key_input = st.text_area("Paste Key", height=100)

    if st.button("🔓 Decrypt Text"):
        try:
            f = Fernet(key_input.encode())
            decrypted = f.decrypt(encrypted_input.encode()).decode()
            st.success("✅ Decrypted Successfully")
            st.markdown(f"""<div class="decrypted-box">{decrypted}</div>""", unsafe_allow_html=True)
            render_copyable("Decrypted Text", decrypted, "decrypted-copy")
        except Exception:
            st.error("❌ Invalid input or key. Decryption failed.")
