"""
Application configuration.

Loads configuration values from Streamlit Secrets.
"""

from __future__ import annotations

import logging

import streamlit as st

# ==========================================================
# LOGGER
# ==========================================================

logger = logging.getLogger(__name__)

# ==========================================================
# HELPER
# ==========================================================

def _get_secret(key: str) -> str:
    """
    Retrieve a required secret from Streamlit Secrets.
    """

    try:

        value = st.secrets[key]

        if value in ("", None):
            raise ValueError(
                f"Secret '{key}' is empty."
            )

        return str(value)

    except KeyError:

        logger.exception(
            "Missing required secret: %s",
            key,
        )

        raise RuntimeError(
            f"Missing required secret '{key}'. "
            "Please check your secrets.toml."
        )

# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================

DB_HOST = _get_secret("DB_HOST")

DB_PORT = int(
    _get_secret("DB_PORT")
)

DB_USER = _get_secret("DB_USER")

DB_PASSWORD = _get_secret("DB_PASSWORD")

DB_NAME = _get_secret("DB_NAME")