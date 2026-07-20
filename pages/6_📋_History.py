"""
History page for Smart Energy Monitoring.

Displays historical monitoring data with search,
filter, and CSV export functionality.
"""

from __future__ import annotations

import logging

import pandas as pd
import streamlit as st

# ==========================================================
# AUTHENTICATION
# ==========================================================

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/🔐_Login.py")

# ==========================================================
# COMPONENTS
# ==========================================================

from components.cards import metric_card
from components.footer import render_footer
from components.header import render_header
from components.sidebar import render_sidebar

# ==========================================================
# SERVICES
# ==========================================================

from backend.services import get_history_data

# ==========================================================
# LOGGER
# ==========================================================

logger = logging.getLogger(__name__)

# ==========================================================
# CONSTANTS
# ==========================================================

DEFAULT_ROWS = 100

ROW_OPTIONS = [
    50,
    100,
    250,
    500,
]

TIMEZONE = "Asia/Jakarta"

CSV_FILENAME = "monitoring_history.csv"

# ==========================================================
# HELPERS
# ==========================================================

def convert_timezone(
    df: pd.DataFrame,
    column: str,
) -> pd.DataFrame:
    """
    Convert UTC timestamp to local timezone.
    """

    if df.empty:
        return df

    df = df.copy()

    df[column] = (
        pd.to_datetime(df[column])
        .dt.tz_localize("UTC")
        .dt.tz_convert(TIMEZONE)
    )

    return df


def search_dataframe(
    df: pd.DataFrame,
    keyword: str,
) -> pd.DataFrame:
    """
    Filter dataframe using keyword.
    """

    if not keyword:
        return df

    keyword = keyword.lower()

    mask = (
        df.astype(str)
        .apply(lambda col: col.str.lower())
        .apply(lambda col: col.str.contains(keyword))
        .any(axis=1)
    )

    return df.loc[mask]

# ==========================================================
# FILTER
# ==========================================================

left, right = st.columns([3, 1])

with left:

    keyword = st.text_input(

        label="🔍 Search Data",

        placeholder="Search voltage, current, power...",

    )

with right:

    rows = st.selectbox(

        label="Rows",

        options=ROW_OPTIONS,

        index=ROW_OPTIONS.index(DEFAULT_ROWS),

    )

# ==========================================================
# LOAD DATA
# ==========================================================

try:

    history = get_history_data(rows)

    df = history["history"]

    last_update = history["last_update"]

    if df.empty:

        logger.warning(
            "History page requested but dataset is empty."
        )

        st.warning(
            "No historical data available."
        )

        st.stop()

    df = convert_timezone(
        df,
        "created_at",
    )

    if last_update is not None:

        last_update = pd.DataFrame(
            {
                "last_update": [
                    last_update,
                ]
            }
        )

        last_update = convert_timezone(
            last_update,
            "last_update",
        )

except Exception:

    logger.exception(
        "Failed loading history data."
    )

    st.error(
        "Unable to load monitoring history."
    )

    st.stop()

# ==========================================================
# SEARCH
# ==========================================================

df = search_dataframe(
    df,
    keyword,
)

if df.empty:

    st.info(
        "No matching records found."
    )

    st.stop()

# ==========================================================
# KPI
# ==========================================================

last = (
    last_update.iloc[0]["last_update"]
    if last_update is not None
    else None
)

c1, c2, c3, c4 = st.columns(4)

with c1:

    metric_card(
        title="Displayed",
        value=len(df),
        icon="📄",
    )

with c2:

    metric_card(
        title="Columns",
        value=len(df.columns),
        icon="📊",
    )

with c3:

    metric_card(
        title="Latest Voltage",
        value=f"{df.iloc[0]['voltage']:.2f}",
        unit="V",
        icon="⚡",
    )

with c4:

    metric_card(
        title="Last Update",
        value=(
            last.strftime("%H:%M:%S")
            if last is not None
            else "-"
        ),
        icon="🕒",
    )

st.divider()

# ==========================================================
# TABLE
# ==========================================================

st.subheader(
    "📑 Historical Dataset"
)

st.caption(
    f"Displaying {len(df):,} monitoring records."
)

st.dataframe(

    df,

    use_container_width=True,

    hide_index=True,

)

st.divider()

# ==========================================================
# EXPORT
# ==========================================================

st.subheader(
    "⬇ Export Dataset"
)

st.caption(
    "Download the filtered monitoring dataset as CSV."
)

csv = df.to_csv(
    index=False,
).encode("utf-8")

st.download_button(

    label="Download CSV",

    data=csv,

    file_name=CSV_FILENAME,

    mime="text/csv",

    use_container_width=True,

)

logger.info(

    "History dataset ready for export (%d rows).",

    len(df),

)

st.divider()

# ==========================================================
# FOOTER
# ==========================================================

render_footer()