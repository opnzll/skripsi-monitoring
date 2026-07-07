from backend.database import (

    get_latest,

    get_last,

    get_statistics,

    get_history,

    get_today,

    get_last_timestamp,

    database_status

)

# ==========================================================
# DASHBOARD SERVICE
# ==========================================================

def get_dashboard_data():

    latest = get_latest()

    if latest.empty:

        return None

    latest = latest.iloc[0]

    stats = get_statistics().iloc[0]

    history = get_last(120)

    last_update = get_last_timestamp().iloc[0]["last_update"]

    return {

        "latest": latest,

        "stats": stats,

        "history": history,

        "last_update": last_update

    }

# ==========================================================
# HISTORY SERVICE
# ==========================================================

def get_history_data(limit=200):

    history = get_history(limit)

    last_update = get_last_timestamp()

    return {

        "history": history,

        "last_update": last_update

    }

# ==========================================================
# ANALYTICS SERVICE
# ==========================================================

def get_analytics_data():

    dataset = get_last(500)

    statistics = get_statistics()

    return {

        "dataset": dataset,

        "statistics": statistics

    }

# ==========================================================
# DATABASE STATUS SERVICE
# ==========================================================

def get_system_status():

    return {

        "database": database_status()

    }