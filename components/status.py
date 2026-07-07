import streamlit as st
from backend.database import database_status


def status_badge(online: bool) -> str:
    css_class = "online" if online else "offline"
    label = "ONLINE" if online else "OFFLINE"
    return f'<span class="status-badge {css_class}">● {label}</span>'


def status_panel():

    st.subheader("System Health")

    db = database_status()

    col1, col2, col3 = st.columns(3, gap="large")

    def health_card(title, online):
        st.markdown(
            f"""
<div class="status-card">
<div class="status-label">{title}</div>
{status_badge(online)}
</div>
""",
            unsafe_allow_html=True,
        )

    with col1:
        health_card("Database", db)
    with col2:
        health_card("ESP32 Connection", True)
    with col3:
        health_card("Dashboard Service", True)