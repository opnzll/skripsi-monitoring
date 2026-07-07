import streamlit as st
from backend.auth import authenticate

st.set_page_config(
    page_title="Login",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

with open("assets/style.css", encoding="utf-8") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.logged_in:
    st.switch_page("app.py")

st.markdown(
    """
<div class="login-card">
    <div class="login-logo">⚡</div>
    <div class="login-title">Smart Energy Monitoring</div>
    <div class="login-subtitle">Electrical Monitoring System Based on IoT</div>
</div>
""",
    unsafe_allow_html=True,
)

_, mid, _ = st.columns([1, 2, 1])

with mid:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login", use_container_width=True, type="primary")

    if login_btn:
        user = authenticate(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.user = user
            st.success("Login successful.")
            st.rerun()
        else:
            st.error("Invalid username or password.")