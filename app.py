import streamlit as st
from cryptography.fernet import Fernet
import streamlit.components.v1 as components

st.set_page_config(page_title="Encrypt/Decrypt", layout="centered")

st.markdown("""
    <style>
    textarea {
        font-size: 16px !important;
    }
    .box {
        background-color: #f5f5f5;
        padding: 12px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-bottom: 8px;
        font-family: monospace;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    .copy-btn {
        background-color: #008CBA;
        color: white;
        padding: 6px 10px;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-size: 14px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)


def copy_box(label, value, box_id):
    st.markdown(f"<div class='box' id='{box_id}'>{value}</div>", unsafe_allow_html=True)
    components.html(f"""
        <button class="copy-btn" onclick="copyToClipboard('{box_id}')">Copy {label}</button>
        <script>
        function copyToClipboard(id) {{
            var range = document.createRange();
            range.selectNode(document.getElementById(id));
            window.getSelection().removeAllRanges();
            window.getSelection().addRange(range);
            try {{
                document.execCommand('copy');
                window.getSelection().removeAllRanges();
                alert('{label} copied!');
            }} catch(err) {{
                alert('Copy failed');
            }}
        }}
        </script>
    """, height=40)


st.title("🔐 GOURAV is CHAD")
tab1, tab2 = st.tabs(["Encrypt", "Decrypt"])

# Encrypt tab
with tab1:
    st.subheader("Generate Encrypted Code")
    user_text = st.text_area("Enter your sentence:", height=150)

    if st.button("Encrypt"):
        if user_text.strip():
            key = Fernet.generate_key()
            fernet = Fernet(key)
            encrypted = fernet.encrypt(user_text.encode()).decode()
            st.success("Encryption successful!")

            copy_box("Encrypted Text", encrypted, "encrypted")
            copy_box("Key", key.decode(), "key")
        else:
            st.warning("Please enter a valid sentence to encrypt.")

# Decrypt tab
with tab2:
    st.subheader("Decode Encrypted Code")
    encrypted_input = st.text_area("Enter encrypted text:", height=150)
    key_input = st.text_area("Enter the key:", height=100)

    if st.button("Decrypt"):
        try:
            fernet = Fernet(key_input.encode())
            decrypted = fernet.decrypt(encrypted_input.encode()).decode()
            st.success("Decryption successful!")
            copy_box("Decrypted Text", decrypted, "decrypted")
        except Exception as e:
            st.error("Invalid key or ciphertext.")
