"""
Login page for Smart Energy Monitoring.
"""

from __future__ import annotations

import logging

import streamlit as st

from backend.auth import authenticate
from backend.database import get_statistics

# ==========================================================
# LOGGER
# ==========================================================

logger = logging.getLogger(__name__)

# ==========================================================
# CONSTANTS
# ==========================================================

APP_TITLE = "Smart Energy Monitoring"

APP_SUBTITLE = (
    "Electrical Monitoring System Based on IoT"
)

LOGIN_REDIRECT = "app.py"

# A single AC sine cycle, hand-authored so the stroke-dash
# animation length in CSS lines up with the path length.
WAVEFORM_SVG = """
<svg viewBox="0 0 320 100" preserveAspectRatio="none">
    <path
        class="auth-wave-path"
        d="M0,50 C20,10 40,10 60,50 C80,90 100,90 120,50
           C140,10 160,10 180,50 C200,90 220,90 240,50
           C260,10 280,10 300,50 C310,70 320,60 320,50"
    />
</svg>
"""

# ==========================================================
# HELPERS
# ==========================================================

def initialize_session() -> None:
    """
    Initialize session state.
    """

    st.session_state.setdefault(
        "logged_in",
        False,
    )

    st.session_state.setdefault(
        "user",
        None,
    )


def load_css() -> None:
    """
    Load application stylesheet.
    """

    with open(
        "assets/style.css",
        encoding="utf-8",
    ) as css:

        st.markdown(
            f"<style>{css.read()}</style>",
            unsafe_allow_html=True,
        )


def get_logged_readings_label() -> str:
    """
    Live readings count for the visual panel. Falls back to a
    static label if the database is unreachable so the login
    screen never breaks on a DB hiccup.
    """

    try:

        stats = get_statistics()

        if stats.empty or stats.iloc[0]["total_data"] is None:

            return "Live telemetry"

        total = int(stats.iloc[0]["total_data"])

        return f"{total:,}"

    except Exception:

        logger.exception(
            "Failed to load reading count for login screen."
        )

        return "Live telemetry"


st.set_page_config(

    page_title="Login",

    page_icon="🔐",

    layout="wide",

    initial_sidebar_state="collapsed",

)

load_css()

initialize_session()

if st.session_state.logged_in:

    st.switch_page(
        LOGIN_REDIRECT,
    )

# ==========================================================
# AUTH SHELL — left: form, right: decorative panel
# ==========================================================

with st.container(key="auth_shell"):

    col_form, col_visual = st.columns([1, 1])

    with col_form:

        st.markdown(
            """
<div class="auth-left">
    <div class="auth-brand">
        <div class="auth-brand-mark"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg></div>
        <div class="auth-brand-name">Smart Energy Monitoring</div>
    </div>
    <div class="auth-heading">Welcome back</div>
    <div class="auth-subheading">Sign in to view live electrical readings and analytics.</div>
</div>
""",
            unsafe_allow_html=True,
        )

        username = st.text_input(
            "Username",
            placeholder="Enter your username",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
        )

        st.markdown(
            '<span class="auth-forgot">Forgot your password? Contact your administrator.</span>',
            unsafe_allow_html=True,
        )

        login_button = st.button(
            "Log in",
            use_container_width=True,
            type="primary",
        )

        st.markdown(
            '<div class="auth-fineprint">Access is limited to authorized users of this monitoring system.</div>',
            unsafe_allow_html=True,
        )

    with col_visual:

        readings_label = get_logged_readings_label()

        st.markdown(
            f"""
<div class="auth-visual">
    <div class="auth-visual-copy">
        <div class="auth-visual-title">Every watt, tracked.</div>
        <div class="auth-visual-sub">
            Real-time voltage, current and power readings from your
            ESP32 &amp; PZEM-004T sensor, visualized the moment they arrive.
        </div>
    </div>
    <div class="auth-wave">{WAVEFORM_SVG}</div>
    <div>
        <div class="auth-stat">{readings_label}</div>
        <div class="auth-stat-label">readings logged so far</div>
        <div class="auth-badges">
            <span class="auth-badge">ESP32</span>
            <span class="auth-badge">PZEM-004T</span>
            <span class="auth-badge">MySQL</span>
            <span class="auth-badge">K-Means</span>
        </div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

# ==========================================================
# LOGIN HANDLING
# ==========================================================

if login_button:

    # --------------------------------------------------
    # VALIDATION
    # --------------------------------------------------

    if not username.strip():

        st.warning(
            "Please enter your username."
        )

        st.stop()

    if not password:

        st.warning(
            "Please enter your password."
        )

        st.stop()

    # --------------------------------------------------
    # AUTHENTICATION
    # --------------------------------------------------

    try:

        user = authenticate(
            username,
            password,
        )

        if user:

            st.session_state.logged_in = True

            st.session_state.user = user

            logger.info(
                "User '%s' logged in successfully.",
                username,
            )

            st.success(
                "Login successful."
            )

            st.switch_page(
                LOGIN_REDIRECT,
            )

        else:

            logger.warning(
                "Failed login attempt for user '%s'.",
                username,
            )

            st.error(
                "Invalid username or password."
            )

    except Exception:

        logger.exception(
            "Unexpected login error."
        )

        st.error(
            "Unable to process login."
        )