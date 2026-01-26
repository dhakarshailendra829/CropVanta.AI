import streamlit as st
import hashlib

def hash_password(password: str):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_password():
    """Returns True if the user had the correct password."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        password = st.sidebar.text_input("Admin Password", type="password")
        if password == "shelu#123": 
            st.session_state["authenticated"] = True
            return True
        return False
    return True