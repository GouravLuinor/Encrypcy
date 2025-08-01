import streamlit as st
from cryptography.fernet import Fernet
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Secure Text Encryptor",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- CUSTOM CSS FOR A PROFESSIONAL UI ---
# This CSS is carefully designed to provide a clean, modern, dark theme.
# It uses a cool blue accent color and Inter font for a professional look.
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    body, .stApp {
        background-color: #0d1117;
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #00aaff;
        font-weight: 700;
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        color: #e0e0e0 !important;
        background-color: #1a1d21;
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    .stTabs [data-baseweb="tab-list"] button:hover {
        background-color: #2c313a;
        color: #00aaff !important;
    }

    .stTabs [aria-selected="true"] button {
        background-color: #161a1e;
        border-bottom: 3px solid #00aaff;
        color: #00aaff !important;
    }

    .stTextArea textarea {
        background-color: #161a1e !important;
        color: #e0e0e0 !important;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 12px;
        font-family: 'Courier New', monospace;
        font-size: 15px;
        min-height: 140px;
    }

    .stButton>button {
        background: linear-gradient(135deg, #00aaff, #006aff);
        color: #fff;
        font-weight: 600;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.3);
    }

    .stAlert {
        border-radius: 8px;
        font-weight: 500;
        padding: 12px;
    }

    .output-box, .decrypted-box {
        background-color: #1f2228;
        padding: 16px;
        border-radius: 12px;
        font-size: 16px;
        font-family: 'Courier New', monospace;
        border: 1px solid #333;
        margin-bottom: 12px;
        white-space: pre-wrap;
        word-wrap: break-word;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    .output-box {
        color: #ffffff;
    }

    .decrypted-box {
        color: #00aaff;
        font-weight: bold;
        text-align: center;
        font-size: 18px;
        background-color: #1f2228;
    }
    
    .copy-btn {
        background: none;
        border: 1px solid #00aaff;
        color: #00aaff;
        padding: 8px 18px;
        font-weight: 600;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
        margin-top: 5px;
        font-size: 14px;
    }

    .copy-btn:hover {
        background: #00aaff;
        color: #fff;
    }

    .fade-msg {
        color: #22c55e;
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

# --- COPY UTILITY FUNCTION ---
# This function is used to render the output boxes with an integrated copy button.
def render_copyable(label: str, value: str, box_id: str):
    """Renders a text box with a copy button using Streamlit components."""
    # The navigator.clipboard.writeText is more reliable in modern browsers.
    # The custom HTML component is used because Streamlit's native components
    # don't provide a direct copy-to-clipboard button.
    components.html(f"""
        <div class="output-box" id="{box_id}">{value}</div>
        <button class="copy-btn" onclick="copyToClipboard('{box_id}', '{box_id}-msg')">📋 Copy {label}</button>
        <div id="{box_id}-msg" class="fade-msg" style="display:none;">✅ Copied!</div>
        <script>
            function copyToClipboard(id, msgId) {{
                const el = document.getElementById(id);
                // Create a temporary textarea to hold the text to be copied
                const tempTextarea = document.createElement('textarea');
                tempTextarea.value = el.innerText;
                document.body.appendChild(tempTextarea);
                tempTextarea.select();
                document.execCommand('copy');
                document.body.removeChild(tempTextarea);
                
                const msg = document.getElementById(msgId);
                msg.style.display = 'block';
                msg.style.animation = 'fadeout 2s ease-out forwards';
                setTimeout(() => {{ msg.style.display = 'none'; msg.style.animation = ''; }}, 2000);
            }}
        </script>
    """, height=180)

# --- UI LAYOUT ---
st.title("🔐 GOURAV is CHAD")

# Tabs for easy switching between encrypt and decrypt modes
tab1, tab2 = st.tabs(["🔒 Encrypt", "🔓 Decrypt"])

# --- ENCRYPT TAB ---
with tab1:
    st.subheader("Encrypt Text")
    input_text = st.text_area(
        "Enter your message:",
        height=140,
        placeholder="Type the message you want to encrypt securely..."
    )

    if st.button("🔐 Encrypt Text", key="encrypt_button"):
        if input_text.strip():
            # Generate a new Fernet key and encrypt the text
            key = Fernet.generate_key()
            fernet = Fernet(key)
            encrypted = fernet.encrypt(input_text.encode()).decode()

            st.success("✅ Your message has been encrypted successfully!")
            
            # Display the encrypted text and key with copy buttons
            render_copyable("Encrypted Text", encrypted, "encrypted")
            render_copyable("Encryption Key", key.decode(), "key")
        else:
            st.warning("⚠️ Please enter some text to encrypt.")

# --- DECRYPT TAB ---
with tab2:
    st.subheader("Decrypt Text")
    encrypted_input = st.text_area(
        "Paste Encrypted Text:",
        height=130,
        placeholder="Paste the encrypted message here..."
    )
    key_input = st.text_area(
        "Paste Key:",
        height=100,
        placeholder="Paste the encryption key here..."
    )

    if st.button("🔓 Decrypt Text", key="decrypt_button"):
        try:
            if encrypted_input.strip() and key_input.strip():
                # Initialize Fernet with the provided key and decrypt
                f = Fernet(key_input.encode())
                decrypted = f.decrypt(encrypted_input.encode()).decode()

                st.success("✅ Decryption successful!")
                
                # Display the decrypted text in a prominent box
                st.markdown(f"""<div class="decrypted-box">{decrypted}</div>""", unsafe_allow_html=True)
                render_copyable("Decrypted Text", decrypted, "decrypted-copy")
            else:
                st.warning("⚠️ Please provide both the encrypted text and the key to decrypt.")
        except Exception:
            # Handle potential errors from invalid keys or ciphertext
            st.error("❌ Decryption failed. Please check if the encrypted text and key are correct.")
