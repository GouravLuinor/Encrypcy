import streamlit as st
from cryptography.fernet import Fernet
import streamlit.components.v1 as components

st.set_page_config(page_title="Encrypt / Decrypt", layout="centered", initial_sidebar_state="collapsed")

# -- Custom style for layout --
st.markdown("""
    <style>
        .box {
            background-color: #1e1e1e;
            padding: 10px;
            border-radius: 10px;
            border: 1px solid #444;
            margin-bottom: 5px;
            font-family: monospace;
            font-size: 15px;
            color: white;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .copy-btn {
            background-color: #08d9d6;
            color: black;
            padding: 6px 12px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# -- Copy button component --
def render_copyable(label: str, text: str, tag_id: str):
    components.html(f"""
        <div class="box" id="{tag_id}">{text}</div>
        <button class="copy-btn" onclick="copyToClipboard('{tag_id}')">📋 Copy {label}</button>
        <script>
            function copyToClipboard(id) {{
                const el = document.getElementById(id);
                if (!navigator.clipboard) {{
                    alert("Clipboard API not available");
                    return;
                }}
                navigator.clipboard.writeText(el.innerText).then(function() {{
                    console.log("Copied!");
                }}, function(err) {{
                    alert("Failed to copy");
                }});
            }}
        </script>
    """, height=150)

st.title("🔐 GOURAV is CHAD")

tab1, tab2 = st.tabs(["Encrypt", "Decrypt"])

with tab1:
    st.subheader("Encrypt Message")
    input_text = st.text_area("Enter your sentence:", height=150)

    if st.button("Encrypt"):
        if input_text.strip():
            key = Fernet.generate_key()
            fernet = Fernet(key)
            encrypted = fernet.encrypt(input_text.encode()).decode()
            st.success("Encryption successful!")

            render_copyable("Encrypted Text", encrypted, "enc_text")
            render_copyable("Key", key.decode(), "key_text")
        else:
            st.warning("Please enter a valid sentence.")

with tab2:
    st.subheader("Decrypt Message")
    encrypted_input = st.text_area("Encrypted Text", height=150)
    key_input = st.text_area("Key", height=100)

    if st.button("Decrypt"):
        try:
            f = Fernet(key_input.encode())
            decrypted = f.decrypt(encrypted_input.encode()).decode()
            st.success("Decryption successful!")
            render_copyable("Decrypted Text", decrypted, "decrypted_text")
        except Exception as e:
            st.error("Invalid key or ciphertext. Please check your inputs.")
