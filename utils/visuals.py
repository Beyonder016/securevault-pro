# utils/visuals.py
import streamlit as st
import base64

def set_background(gif_path: str):
    with open(gif_path, "rb") as f:
        data_url = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/gif;base64,{data_url}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def launch_screen():
    st.markdown(
        """
        <div style="text-align:center; padding: 30px 0;">
            <h1 style="font-size:3.2em; color:#00ffd0;">Welcome to SecureVault</h1>
            <p style="font-size:1.2em; color:#cccccc;">A crazy-cool tool for encryption, decryption & file integrity.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
