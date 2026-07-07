# components/empty_state.py
import streamlit as st

def empty_state(title: str, desc: str = "", icon: str = "📭"):
    st.markdown(
        f"""
<div class="empty-state">
    <div class="empty-icon">{icon}</div>
    <div class="empty-title">{title}</div>
    <div class="empty-desc">{desc}</div>
</div>
""",
        unsafe_allow_html=True,
    )