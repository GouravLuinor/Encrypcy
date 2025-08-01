import streamlit as st
from cryptography.fernet import Fernet
import streamlit.components.v1 as components

st.set_page_config(page_title="Encrypt/Decrypt", layout="centered")

# ----------------- Custom Styles ----------------- #
st.markdown("""
<style>
.stApp {
    background-color: #121212;
    padding: 20px;
}

h1, h2, h3, h4, h5 {
    color: #08d9d6 !important;
}

textarea {
    font-size: 16px !important;
}

.output-box {
    background-color: #1c1c1c;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #444;
    font-family: monospace;
    font-size: 16px;
    color: #ffffff;  /* Set to pure white */
    white-space: pre-wrap;
    word-wrap: break-word;
    margin-bottom: 10px;
}

.decrypted-box {
    background-color: #222;
    padding: 22px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 20px;
    color: #08d9d6;
    text-align: center;
    margin-bottom: 10px;
    border: 1px solid #444;
}

.copy-btn {
    background: linear-gradient(to right, #08d9d6, #00a9b8);
    color: white;
    padding: 8px 16px;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    font-size: 15px;
    font-weight: 600;
    transition: transform 0.2s ease, background 0.3s ease;
    margin-bottom: 20px;
}

.copy-btn:hover {
    transform: scale(1.05);
    background: linear-gradient(to right, #00a9b8, #08d9d6);
}

.fade-msg {
    color: #12ffb0;
    font-size: 14px;
    animation: fadeout 2s ease-out forwards;
    margin-top: 8px;
    font-weight: 500;
}

@keyframes fadeout {
    0%   { opacity: 1; }
    80%  { opacity: 1; }
    100% { opacity: 0; }
}
</style>
""", unsafe_allow_html=True)

# ----------------- Copy Component ----------------- #
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
                    setTimeout(() => {{
                        msg.style.display = 'none';
                    }}, 2000);
                }});
            }}
        </script>
    """, height=200)

# ----------------- Title & Layout ----------------- #
st.title("🔐 GOURAV is CHAD")

tab1, tab2 = st.tabs(["🔒 Encrypt", "🔓 Decrypt"])

# ----------------- ENCRYPT ----------------- #
with tab1:
    st.subheader("🔒 Generate Encrypted Text")
    input_text = st.text_area("Enter your message:", height=150, placeholder="Type something to encrypt...")

    if st.button("🚀 Encrypt"):
        if input_text.strip():
            key = Fernet.generate_key()
            fernet = Fernet(key)
            encrypted = fernet.encrypt(input_text.encode()).decode()
            st.success("✅ Successfully Encrypted!")

            render_copyable("Encrypted Text", encrypted, "enc_output")
            render_copyable("Key", key.decode(), "key_output")
        else:
            st.warning("⚠️ Please enter some text to encrypt.")

# ----------------- DECRYPT ----------------- #
with tab2:
    st.subheader("🔓 Decrypt Encrypted Text")
    encrypted_input = st.text_area("Paste Encrypted Text", height=150)
    key_input = st.text_area("Paste Key", height=100)

    if st.button("🛠️ Decrypt"):
        try:
            f = Fernet(key_input.encode())
            decrypted = f.decrypt(encrypted_input.encode()).decode()
            st.success("✅ Successfully Decrypted!")
            st.markdown(f"""<div class="decrypted-box">{decrypted}</div>""", unsafe_allow_html=True)
            render_copyable("Decrypted Text", decrypted, "decrypted_copy_box")
        except Exception as e:
            st.error("❌ Decryption failed. Please verify your key and encrypted message.")
