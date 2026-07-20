"""
Login page for Smart Energy Monitoring.
"""

from __future__ import annotations

import logging

import streamlit as st

from backend.auth import authenticate

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

st.set_page_config(

    page_title="Login",

    page_icon="🔐",

    layout="centered",

    initial_sidebar_state="collapsed",

)

load_css()

initialize_session()

if st.session_state.logged_in:

    st.switch_page(
        LOGIN_REDIRECT,
    ) 

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

    username = st.text_input(
        "Username",
    )

    password = st.text_input(
        "Password",
        type="password",
    )

    login_button = st.button(
        "Login",
        use_container_width=True,
        type="primary",
    )

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