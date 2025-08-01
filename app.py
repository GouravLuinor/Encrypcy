import streamlit as st
from cryptography.fernet import Fernet
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Secure Text Encryptor",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- INSTRUCTIONS SIDEBAR ---
# A collapsible sidebar serves as the "sliding window" for instructions.
with st.sidebar:
    st.header("App Instructions")
    st.markdown("""
    This application allows you to securely encrypt and decrypt text messages using a robust encryption key.
    
    **🔒 Encrypt**
    1. Type or paste your message into the text area. The message must not exceed 40 words.
    2. Click the "🔐 Encrypt Text" button.
    3. The encrypted message and a unique key will be generated.
    4. Copy both the encrypted text and the key. You will need both to decrypt the message.
    
    **🔓 Decrypt**
    1. Go to the "Decrypt" tab.
    2. Paste the encrypted message into the first text area.
    3. Paste the corresponding key into the second text area.
    4. Click the "🔓 Decrypt Text" button.
    5. The original message will be displayed.
    6. Share the link with a friend.
    7. Generate a encrypted message and key & send them.
    8. BEST PART NO ONE WITHOUT THE APP LINK CAN KNOW
       ABOUT YOUR SECRET CONVERSATION. ENJOY...""")
    

# --- CUSTOM CSS FOR A PROFESSIONAL UI ---
# This CSS is updated for a new light theme with contrasting boxes.
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    body, .stApp {
        background-color: #f0f2f6; /* Lighter background */
        color: #333333; /* Darker text for readability */
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #0077b6; /* A new, deep blue for a professional look */
        font-weight: 700;
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        color: #555555 !important;
        background-color: #e0e2e6;
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    .stTabs [data-baseweb="tab-list"] button:hover {
        background-color: #c7c9cf;
        color: #0077b6 !important;
    }

    .stTabs [aria-selected="true"] button {
        background-color: #ffffff;
        border-bottom: 3px solid #0077b6;
        color: #0077b6 !important;
    }

    /* New CSS to make text area labels bold and black */
    .stTextArea label {
        font-weight: 700;
        color: #000000 !important;
    }

    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 1px solid #c7c9cf;
        border-radius: 8px;
        padding: 12px;
        font-family: 'Courier New', monospace;
        font-size: 15px;
        min-height: 140px;
    }

    .stButton>button {
        background: linear-gradient(135deg, #0077b6, #005f98);
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

    /* Contrasting box for output */
    .output-box, .decrypted-box {
        background-color: #2c313a;
        padding: 16px;
        border-radius: 12px;
        font-size: 16px;
        font-family: 'Courier New', monospace;
        border: 1px solid #444;
        margin-bottom: 12px;
        white-space: pre-wrap;
        word-wrap: break-word;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    .output-box {
        color: #ffffff;
    }

    .decrypted-box {
        color: #55f3c7; /* A bright color to stand out */
        font-weight: bold;
        text-align: center;
        font-size: 18px;
        background-color: #2c313a;
    }
    
    .copy-btn {
        background: none;
        border: 1px solid #0077b6;
        color: #0077b6;
        padding: 8px 18px;
        font-weight: 600;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
        margin-top: 5px;
        font-size: 14px;
    }

    .copy-btn:hover {
        background: #0077b6;
        color: #fff;
    }

    .fade-msg {
        color: #16a34a;
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
def render_copyable(label: str, value: str, box_id: str):
    """Renders a text box with a copy button using Streamlit components."""
    components.html(f"""
        <div class="output-box" id="{box_id}">{value}</div>
        <button class="copy-btn" onclick="copyToClipboard('{box_id}', '{box_id}-msg')">📋 Copy {label}</button>
        <div id="{box_id}-msg" class="fade-msg" style="display:none;">✅ Copied!</div>
        <script>
            function copyToClipboard(id, msgId) {{
                const el = document.getElementById(id);
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
st.title("🔐 GOURAV is CHAD ; )")

tab1, tab2 = st.tabs(["🔒 Encrypt", "🔓 Decrypt"])

# --- ENCRYPT TAB ---
with tab1:
    st.subheader("Encrypt Text")
    input_text = st.text_area(
        "Enter your message:",
        height=140,
        placeholder="Type the message to encrypt (max 40 words)..."
    )

    if st.button("🔐 Encrypt Text", key="encrypt_button"):
        # Check for word limit
        if not input_text.strip():
            st.warning("⚠️ Please enter some text to encrypt.")
        elif len(input_text.strip().split()) > 40:
            st.warning("⚠️ The message must be 40 words or less.")
        else:
            key = Fernet.generate_key()
            fernet = Fernet(key)
            encrypted = fernet.encrypt(input_text.encode()).decode()

            st.success("✅ Your message has been encrypted successfully!")
            
            render_copyable("Encrypted Text", encrypted, "encrypted")
            render_copyable("Encryption Key", key.decode(), "key")

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
                f = Fernet(key_input.encode())
                decrypted = f.decrypt(encrypted_input.encode()).decode()

                st.success("✅ Decryption successful!")
                
                st.markdown(f"""<div class="decrypted-box">{decrypted}</div>""", unsafe_allow_html=True)
                render_copyable("Decrypted Text", decrypted, "decrypted-copy")
            else:
                st.warning("⚠️ Please provide both the encrypted text and the key to decrypt.")
        except Exception:
            st.error("❌ Decryption failed. Please check if the encrypted text and key are correct.")
