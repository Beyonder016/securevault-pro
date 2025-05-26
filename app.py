import streamlit as st
import base64
from utils.encryption import encrypt_file, decrypt_file
from utils.hashing import sha256_hash
from utils.keygen import derive_key, generate_salt, encode_salt, decode_salt
from utils.file_handler import save_uploaded_file
from utils.visuals import launch_screen, set_background
from utils.qrgen import generate_qr_code

# ========== Launch ==========
st.set_page_config(page_title="SecureVault", page_icon="🔐", layout="wide")
set_background("assets/bg.gif")
launch_screen()

st.markdown(
    "<h2 style='text-align: center;'>🔐 SecureVault – Encrypt. Hash. Protect.</h2>",
    unsafe_allow_html=True,
)

# ========== Sidebar Layout ==========
st.sidebar.markdown("<h2 style='text-align:center;'>🛡️ SecureVault</h2>", unsafe_allow_html=True)
st.sidebar.markdown("Built for secure hashing and encryption 💾")

# Sidebar action selector with modern UX
with st.sidebar.expander("⚙️ Select Function", expanded=True):
    option = st.radio(
        "Choose a task:",
        ["Generate Hash", "Encrypt File", "Decrypt File"],
        index=0,
        key="action_radio"
    )

# Reset state when switching actions
if "last_action" not in st.session_state:
    st.session_state.last_action = ""

if option != st.session_state.last_action:
    st.session_state.last_action = option
    st.session_state.pop("file_uploader", None)
    st.session_state.pop("passphrase", None)
    st.session_state.pop("last_salt", None)
    st.rerun()

# Sidebar instructions
with st.sidebar.expander("📖 How to Use", expanded=False):
    st.markdown("""
    1. **Upload a file** (any format).
    2. **Enter a secret passphrase**.
    3. Choose:
       - 🔍 **Hash** to verify integrity.
       - 🔐 **Encrypt** to protect the file.
       - 🔓 **Decrypt** using a passphrase + salt.
    4. Copy the output salt or hash securely.
    """)

# GitHub footer (🎯 UPDATE with your link below)
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align:center'>
  <p style='font-size: 14px;'>🔓 This project is open source.<br>
  View it on <a href="https://github.com/yourusername/yourrepo" target="_blank" style="text-decoration: none; font-weight:bold;'>GitHub ↗</a></p>
</div>
""", unsafe_allow_html=True)

# ========== Main Input Form ==========
with st.form("securevault_form"):
    file = st.file_uploader("Upload a file", type=None, key="file_uploader")
    passphrase = st.text_input("Enter your secret passphrase", type="password", key="passphrase")

    salt_input = ""
    if option == "Decrypt File":
        salt_input = st.text_input("Enter the salt used during encryption")

    submitted = st.form_submit_button("🔐 Run SecureVault")

# ========== Action Logic ==========
if submitted and file and passphrase:
    temp_file_path = save_uploaded_file(file)

    if option == "Generate Hash":
        hash_digest = sha256_hash(temp_file_path)
        st.success("SHA-256 Hash Generated")
        st.code(hash_digest)
        qr = generate_qr_code(hash_digest)
        st.image(qr)

    elif option == "Encrypt File":
        salt = generate_salt()
        encoded_salt = encode_salt(salt)
        key = derive_key(passphrase, salt)
        out_path = encrypt_file(temp_file_path, key)

        with open(out_path, "rb") as f:
            st.download_button("Download Encrypted File", f, file_name="encrypted_file")

        st.success("File Encrypted Successfully!")
        st.session_state["last_salt"] = encoded_salt
        st.markdown("**Salt for Decryption (copy this!):**")
        st.code(encoded_salt, language="none")

    elif option == "Decrypt File":
        if not salt_input:
            st.warning("Salt is required to decrypt the file.")
        else:
            try:
                salt = decode_salt(salt_input)
                key = derive_key(passphrase, salt)
                out_path = decrypt_file(temp_file_path, key)
                with open(out_path, "rb") as f:
                    st.download_button("Download Decrypted File", f, file_name="decrypted_file")
                st.success("File Decrypted Successfully!")
            except Exception as e:
                st.error(f"Decryption failed: {str(e)}")

# ========== Persistent Salt Display ==========
elif "last_salt" in st.session_state and option == "Encrypt File":
    st.markdown("**Salt for Decryption (copy this!):**")
    st.code(st.session_state["last_salt"], language="none")
