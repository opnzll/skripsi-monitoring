"""
System status components.

Displays health information for the monitoring system.
"""

import logging

import streamlit as st

from backend.services import get_system_status

# ==========================================================
# LOGGER
# ==========================================================

logger = logging.getLogger(__name__)

# ==========================================================
# CACHE
# ==========================================================

@st.cache_data(ttl=5, show_spinner=False)
def load_system_status() -> dict:
    """
    Load current system status.
    """
    return get_system_status()

# ==========================================================
# STATUS BADGE
# ==========================================================

def status_badge(online: bool) -> str:
    """
    Return HTML badge for online/offline status.
    """

    css_class = "online" if online else "offline"
    label = "ONLINE" if online else "OFFLINE"

    return (
        f'<span class="status-badge {css_class}">'
        f"● {label}"
        f"</span>"
    )

# ==========================================================
# HEALTH CARD
# ==========================================================

def health_card(title: str, online: bool) -> None:
    """
    Display a single health card.
    """

    st.markdown(
        f"""
        <div class="status-card">
            <div class="status-label">{title}</div>
            {status_badge(online)}
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==========================================================
# STATUS PANEL
# ==========================================================

def status_panel() -> None:
    """
    Display overall system health.
    """

    st.subheader("System Health")

    try:

        status = load_system_status()

        database_online = status.get("database", False)

        # Untuk saat ini masih mengikuti status database.
        # Nantinya bisa diganti jika sudah ada endpoint
        # khusus untuk ESP32 dan Dashboard Service.
        esp32_online = database_online
        dashboard_online = database_online

        col1, col2, col3 = st.columns(3, gap="large")

        with col1:
            health_card("Database", database_online)

        with col2:
            health_card("ESP32 Connection", esp32_online)

        with col3:
            health_card("Dashboard Service", dashboard_online)

    except Exception:

        logger.exception("Failed to display system status.")

        st.error("Unable to load system status.")