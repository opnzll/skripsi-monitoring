"""
Service layer for Smart Energy Monitoring.

Service layer bertugas mengambil data dari database,
melakukan validasi, kemudian mengembalikan data yang siap
digunakan oleh halaman Streamlit.
"""

from datetime import datetime
import logging

import pandas as pd

from backend.database import (
    database_status,
    get_history,
    get_last,
    get_last_timestamp,
    get_latest,
    get_statistics,
)

# ==========================================================
# LOGGER
# ==========================================================

logger = logging.getLogger(__name__)

# ==========================================================
# CONSTANTS
# ==========================================================

DEFAULT_HISTORY_LIMIT = 200
DASHBOARD_HISTORY_LIMIT = 120
ANALYTICS_LIMIT = 500

# Data dianggap masih realtime jika < 10 detik
FRESH_DATA_THRESHOLD = 10

# ==========================================================
# HELPER
# ==========================================================

def _first_row(df: pd.DataFrame) -> pd.Series | None:
    """
    Mengambil baris pertama DataFrame.

    Returns
    -------
    pd.Series | None
    """

    if df.empty:
        return None

    return df.iloc[0]


# ==========================================================
# DASHBOARD SERVICE
# ==========================================================

def get_dashboard_data() -> dict | None:
    """
    Mengambil seluruh data Dashboard.
    """

    try:

        latest_df = get_latest()

        latest = _first_row(latest_df)

        if latest is None:

            logger.warning("No monitoring data found.")

            return None

        statistics = _first_row(get_statistics())

        history = get_last(DASHBOARD_HISTORY_LIMIT)

        timestamp = _first_row(get_last_timestamp())

        last_update = None

        if timestamp is not None:

            last_update = timestamp["last_update"]

        return {

            "latest": latest,

            "stats": statistics,

            "history": history,

            "last_update": last_update,

        }

    except Exception:

        logger.exception("Failed to load dashboard data.")

        return None


# ==========================================================
# HISTORY SERVICE
# ==========================================================

def get_history_data(
    limit: int = DEFAULT_HISTORY_LIMIT,
) -> dict:
    """
    Mengambil histori monitoring.
    """

    try:

        timestamp = _first_row(get_last_timestamp())

        return {

            "history": get_history(limit),

            "last_update": (
                timestamp["last_update"]
                if timestamp is not None
                else None
            ),

        }

    except Exception:

        logger.exception("Failed to load history.")

        return {

            "history": pd.DataFrame(),

            "last_update": None,

        }


# ==========================================================
# ANALYTICS SERVICE
# ==========================================================

def get_analytics_data() -> dict:
    """
    Mengambil dataset Analytics.
    """

    try:

        return {

            "dataset": get_last(ANALYTICS_LIMIT),

            "statistics": get_statistics(),

        }

    except Exception:

        logger.exception("Failed to load analytics.")

        return {

            "dataset": pd.DataFrame(),

            "statistics": pd.DataFrame(),

        }


# ==========================================================
# SYSTEM STATUS
# ==========================================================

def get_system_status() -> dict:
    """
    Mengambil status kesehatan sistem.
    """

    try:

        database_online = database_status()

        timestamp = _first_row(get_last_timestamp())

        last_update = None
        seconds = None
        fresh_data = False

        if timestamp is not None:

            last_update = timestamp["last_update"]

            if last_update is not None:

                seconds = (
                    datetime.now() - last_update
                ).total_seconds()

                fresh_data = (
                    seconds <= FRESH_DATA_THRESHOLD
                )

        return {

            "database": database_online,

            "last_update": last_update,

            "last_update_seconds": seconds,

            "fresh_data": fresh_data,

        }

    except Exception:

        logger.exception("Failed to get system status.")

        return {

            "database": False,

            "last_update": None,

            "last_update_seconds": None,

            "fresh_data": False,

        }
    
# ==========================================================
# CLUSTERING SERVICE
# ==========================================================

def get_clustering_data(limit: int = 2500) -> pd.DataFrame:
    try:
        return get_last(limit)
    except Exception:
        logger.exception("Failed to load clustering dataset.")
        return pd.DataFrame()