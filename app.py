import streamlit as st

st.set_page_config(
    page_title="Smart Energy Monitoring",
    page_icon="⚡",
    layout="wide"
)

if st.session_state.get("logged_in", False):
    st.switch_page("pages/1_📊_Monitoring.py")
else:
    st.switch_page("pages/🔐_Login.py")